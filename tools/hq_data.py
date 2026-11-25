"""Read structured evidence and Git objects without working-tree substitution."""

import json
from functools import lru_cache
from hashlib import sha256
import os
from pathlib import Path
import re
import stat
import subprocess
from urllib.parse import urlsplit


SHA = re.compile(r"[0-9a-f]{40}")
REPOSITORY = re.compile(r"[A-Za-z0-9][A-Za-z0-9-]{0,38}/[A-Za-z0-9_.-]{1,100}")
REGULAR_MODES = {"100644", "100755"}


def parse_json(data, source):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"{source}: repeated JSON key {key!r}")
            result[key] = value
        return result

    def finite(value):
        raise ValueError(f"{source}: non-JSON number {value}")

    try:
        return json.loads(data, object_pairs_hook=unique, parse_constant=finite)
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"{source}: {error}") from error


def read_json(path):
    return parse_json(path.read_bytes(), path)


def physical_lines(text):
    return text.split("\n")


def github_repository(remote):
    if remote.startswith("git@github.com:"):
        path = remote.split(":", 1)[1]
    else:
        parts = urlsplit(remote)
        if parts.hostname != "github.com":
            return None
        path = parts.path.strip("/")
    name = path.removesuffix(".git")
    return name if REPOSITORY.fullmatch(name) else None


@lru_cache(maxsize=1)
def local_git_environment_names():
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return frozenset(subprocess.check_output(["git", "rev-parse", "--local-env-vars"],
                                             env=env).decode("ascii").splitlines())


def clean_git_environment():
    """Prevent inherited repository selectors from redirecting explicit Git operations."""
    env = os.environ.copy()
    names = local_git_environment_names()
    for key in list(env):
        if key in names or key.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")):
            env.pop(key, None)
    return env


class UnavailableGitBlob(ValueError):
    """A tracked blob could not be read under the selected Git fetch policy."""


class GitTree:
    def __init__(self, root, ref="HEAD", *, draft=False, allow_git_fetch=False, track_draft_reads=False):
        self.root = Path(root).resolve()
        self.allow_git_fetch = allow_git_fetch
        self.fetched_blobs = set()
        self.commit = self.git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()
        self.draft = draft
        self.track_draft_reads = track_draft_reads
        self.draft_source_digests = {}
        self._entries = {}
        remote = subprocess.run(
            ["git", "remote", "get-url", "origin"], cwd=self.root,
            capture_output=True, text=True, check=False, env=clean_git_environment(),
        )
        self.repository = github_repository(remote.stdout.strip()) if remote.returncode == 0 else None

    def git(self, *args, allow_fetch=False, input_bytes=None):
        env = clean_git_environment()
        if allow_fetch:
            env["GIT_NO_LAZY_FETCH"] = "0"
        else:
            env.update(GIT_NO_LAZY_FETCH="1", GIT_ALLOW_PROTOCOL="")
        result = subprocess.run(["git", "--no-replace-objects", *args], cwd=self.root,
                                env=env, input=input_bytes, capture_output=True)
        if result.returncode:
            raise ValueError(result.stderr.decode("utf-8", "replace").strip() or "Git command failed")
        return result.stdout

    def resolve(self, ref):
        return self.git("rev-parse", "--verify", "--end-of-options", f"{ref}^{{commit}}").decode().strip()

    def entries(self, commit=None):
        revision = commit or self.commit
        draft = self.draft and commit is None
        key = None if draft else revision
        if key not in self._entries:
            entries = {}
            if draft:
                records = self.git("ls-files", "--stage", "-z").split(b"\0")
                for record in filter(None, records):
                    spec, name = record.split(b"\t", 1)
                    mode, digest, stage = spec.decode().split()
                    if stage != "0":
                        raise ValueError("Index has unresolved merge entries")
                    entries[name.decode("utf-8", "surrogateescape")] = (mode, digest)
            else:
                records = self.git("ls-tree", "-r", "-z", revision).split(b"\0")
                for record in filter(None, records):
                    spec, name = record.split(b"\t", 1)
                    mode, _, digest = spec.decode().split()
                    entries[name.decode("utf-8", "surrogateescape")] = (mode, digest)
            self._entries[key] = entries
        return self._entries[key]

    def read(self, path, commit=None):
        mode, digest = self.entries(commit)[path]
        if mode not in REGULAR_MODES:
            raise ValueError(f"{path}: expected a regular tracked file, got mode {mode}")
        if self.draft and commit is None:
            local = self.root
            for part in Path(path).parts:
                local = local / part
                if not local.is_relative_to(self.root):
                    raise ValueError(f"{path}: draft path leaves the repository")
                info = local.lstat()
                if stat.S_ISLNK(info.st_mode) or (
                    getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT
                ):
                    raise ValueError(f"{path}: tracked draft path has a symlink or reparse point")
            body = local.read_bytes()
            if self.track_draft_reads:
                observed = sha256(body).hexdigest()
                if self.draft_source_digests.setdefault(path, observed) != observed:
                    raise ValueError(f"{path}: draft content changed during audit")
            return body
        return self._read_blob(path, digest)

    def materialize_checkout_blobs(self):
        blobs = {digest: path for path, (mode, digest) in self.entries().items() if mode != "160000"}
        if not blobs:
            return
        listing = self.git("cat-file", "--batch-check=%(objectname) %(objecttype)",
                           input_bytes=("\n".join(blobs) + "\n").encode("ascii"))
        for line in listing.decode("ascii").splitlines():
            digest, kind = line.split()
            if kind != "blob":
                self._read_blob(blobs[digest], digest)

    def _read_blob(self, path, digest):
        try:
            return self.git("cat-file", "blob", digest)
        except ValueError as offline_error:
            if not self.allow_git_fetch:
                raise UnavailableGitBlob(f"{path}: Git blob {digest} unavailable with Git fetching disabled") from offline_error
        try:
            body = self.git("cat-file", "blob", digest, allow_fetch=True)
        except ValueError as error:
            raise UnavailableGitBlob(f"{path}: Git blob {digest} unavailable after permitted Git read: {error}") from error
        self.fetched_blobs.add(digest)
        return body
