"""Check rendered Markdown destinations against the selected Git tree."""

from collections import Counter
from dataclasses import dataclass
from hashlib import sha256
from html.parser import HTMLParser
from io import BytesIO
from pathlib import Path
import posixpath
import re
import struct
import unicodedata
from urllib.parse import parse_qs, unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.rules_inline import autolink, html_inline, image, link
from PIL import Image

from hq_data import REGULAR_MODES, SHA, physical_lines


MARKDOWN = {".md", ".markdown", ".mdown", ".mkdn"}
README_FORMATS = [".md", ".markdown", ".mdown", ".mkdn", ".rst", ".adoc", ".asciidoc", ".asc", ".org", ".txt", ""]
IMAGE_FORMATS = {".png": "PNG", ".gif": "GIF", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP"}
LFS_HOSTS = (b"version https://git-lfs.github.com/", b"version https://hawser.github.com/")
LFS_POINTER = re.compile(rb"version https://(?:git-lfs|hawser)\.github\.com/spec/v1\n"
                         rb"((?:ext-[0-9]-[a-z0-9][a-z0-9.-]* sha256:[0-9a-f]{64}\n)*)"
                         rb"oid sha256:([0-9a-f]{64})\nsize (0|[1-9][0-9]*)\n")
MAX_CACHED_MEDIA_BYTES = 50 * 1024 * 1024
MAX_MEDIA_FRAMES = 256
MAX_MEDIA_PIXELS = 100_000_000
LINE_RANGE = re.compile(r"L([0-9]+)(?:-L([0-9]+))?")
BARE_WEB = re.compile(r"(?:^|(?<=[\s*_~(]))(?:https?://|www\.)[^\s<>]+")
HTML_VOID_ELEMENTS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
                      "meta", "param", "source", "track", "wbr"}
PARSER = MarkdownIt("commonmark").enable("table").enable("strikethrough")


def locate_inline(rule, kind):
    def located(state, silent):
        start = state.pos
        previous = len(state.tokens)
        matched = rule(state, silent)
        if matched and not silent:
            token = next(item for item in state.tokens[previous:] if item.type == kind)
            token.meta["source_line_offset"] = state.src.count("\n", 0, start)
        return matched
    return located


for rule, kind in ((link, "link_open"), (autolink, "link_open"), (image, "image"), (html_inline, "html_inline")):
    PARSER.inline.ruler.at(rule.__name__, locate_inline(rule, kind))


def suffix(path):
    return posixpath.splitext(path)[1].lower()


def readme_path(entries, directory="", *, homepage=False):
    bases = (".github", "", "docs") if homepage and not directory else (directory,)
    for base in bases:
        names = {}
        for path, (mode, _) in entries.items():
            if posixpath.dirname(path) == base and mode in REGULAR_MODES:
                name = posixpath.basename(path).casefold()
                names.setdefault(name, []).append(path)
        for extension in README_FORMATS:
            matches = names.get("readme" + extension, [])
            if len(matches) > 1:
                raise ValueError(f"{base or '/'}: ambiguous README case variants")
            if matches:
                return matches[0]
    return None


@dataclass(frozen=True)
class Link:
    path: str
    line: int
    image: bool = False
    unnamed: bool = False
    coverage_gap: str | None = None
    diagnostic: str | None = None


def image_sources(value):
    if "data:" in value.lower():
        raise ValueError("unsupported inline image source")
    candidates = []
    remaining = value
    while remaining := remaining.lstrip(" ,\t\r\n\f"):
        match = re.match(r"([^ \t\r\n\f]+)(.*)", remaining, re.DOTALL)
        url, remaining = match.groups()
        if url.endswith(","):
            candidates.append(url.rstrip(","))
            continue
        descriptor, _, remaining = remaining.partition(",")
        descriptor = descriptor.strip()
        if descriptor and not re.fullmatch(r"(?:[1-9]\d*w|(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)x)", descriptor):
            raise ValueError("unsupported image source descriptor")
        candidates.append(url)
    if not candidates:
        raise ValueError("empty image source list")
    return candidates


class HtmlLinks(HTMLParser):
    def __init__(self, line):
        super().__init__(convert_charrefs=True)
        self.line = line
        self.links = []
        self.anchors = set()
        self.controls = []
        self.hidden_elements = []

    def handle_starttag(self, tag, options):
        attrs = dict(options)
        line = self.line + self.getpos()[0] - 1
        aria_label = (attrs.get("aria-label") or "").strip()
        hidden = (bool(self.hidden_elements) or "hidden" in attrs
                  or (attrs.get("aria-hidden") or "").strip().casefold() == "true")
        if hidden and tag not in HTML_VOID_ELEMENTS:
            self.hidden_elements.append(tag)
        if tag == "a":
            if attrs.get("name"):
                self.anchors.add(attrs["name"])
            if attrs.get("href"):
                self.controls.append([attrs["href"], line, hidden or bool(aria_label)])
        if tag == "img" and "alt" not in attrs and not aria_label:
            source = attrs.get("src") or attrs.get("srcset") or "<img>"
            self.links.append(Link(source, line,
                                   diagnostic="HTML image requires an alt attribute or nonempty aria-label"))
        if tag in {"source", "img"} and "srcset" in attrs:
            srcset = attrs["srcset"] or ""
            try:
                sources = image_sources(srcset)
            except ValueError:
                self.links.append(Link(srcset, line, coverage_gap="unsupported image source list"))
            else:
                self.links.extend(Link(url, line, True) for url in sources)
        if tag == "img":
            if attrs.get("src"):
                self.links.append(Link(attrs["src"], line, True))
            if self.controls and not hidden and (aria_label or (attrs.get("alt") or "").strip()):
                self.controls[-1][2] = True

    def handle_data(self, data):
        if self.controls and not self.hidden_elements and data.strip():
            self.controls[-1][2] = True

    def handle_endtag(self, tag):
        for index in range(len(self.hidden_elements) - 1, -1, -1):
            if self.hidden_elements[index] == tag:
                del self.hidden_elements[index:]
                break
        if tag == "a" and self.controls:
            path, line, named = self.controls.pop()
            self.links.append(Link(path, line, unnamed=not named))


def inline_link_has_name(children, line):
    if not any(item.type == "html_inline" for item in children):
        return any(item.content.strip() for item in children if item.type in {"text", "code_inline", "image"})
    html = HtmlLinks(line)
    outer = ["", line, False]
    html.controls.append(outer)
    for item in children:
        if item.type == "html_inline":
            html.feed(item.content)
        elif item.type in {"text", "code_inline", "image"}:
            html.handle_data(item.content)
    html.close()
    return outer[2]


def inline_links(children, line):
    links = []
    current_line = line
    in_link = False
    for index, token in enumerate(children):
        occurrence = line + token.meta.get("source_line_offset", 0)
        if token.type == "image":
            links.append(Link(token.attrGet("src"), occurrence, True))
        elif token.type == "link_open":
            in_link = True
            end = next((i for i in range(index + 1, len(children)) if children[i].type == "link_close"), len(children))
            named = inline_link_has_name(children[index + 1:end], occurrence)
            links.append(Link(token.attrGet("href"), occurrence, unnamed=not named))
        elif token.type == "link_close":
            in_link = False
        elif token.type in {"hardbreak", "softbreak"}:
            current_line += 1
        elif token.type == "text" and not in_link:
            for match in BARE_WEB.finditer(token.content):
                candidate = match[0]
                extra_closers = candidate.count(")") - candidate.count("(")
                end = len(candidate)
                while end:
                    trailing = candidate[end - 1]
                    if trailing == ")" and extra_closers > 0:
                        extra_closers -= 1
                    elif trailing not in "?!.,:*_~":
                        break
                    end -= 1
                address = candidate[:end]
                try:
                    hostname = urlsplit("http://" + address if address.startswith("www.") else address).hostname
                except ValueError:
                    continue
                if hostname and "." in hostname and not hostname.endswith("."):
                    links.append(Link(address, current_line,
                                      coverage_gap=f"bare GFM URL was not checked: {address}"))
    return links


def rendered_table_rows(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    return [lines[token.map[0]] for token in PARSER.parse(text)
            if token.type == "tr_open" and token.map is not None]


def parse_markdown(text):
    anchors = set()
    generated = set()
    counts = Counter()
    links = []
    blocks = PARSER.parse(text)
    line = 1
    for index, token in enumerate(blocks):
        if token.map:
            line = token.map[0] + 1
        if token.type == "heading_open":
            inline = blocks[index + 1]
            heading = "".join(item.content for item in inline.children
                              if item.type in {"text", "code_inline", "image"})
            slug = "".join(char for char in heading.lower().replace(" ", "-")
                           if char in "-_" or unicodedata.category(char)[0] in "LMN")
            candidate = slug
            while candidate in generated:
                counts[slug] += 1
                candidate = f"{slug}-{counts[slug]}"
            generated.add(candidate)
        if token.type not in {"html_block", "inline"}:
            continue
        if token.type == "inline":
            links.extend(inline_links(token.children, line))
            html = HtmlLinks(line)
            for item in token.children:
                if item.type == "html_inline":
                    html.line = line + item.meta.get("source_line_offset", 0) - html.getpos()[0] + 1
                    html.feed(item.content)
                elif item.type in {"text", "code_inline"}:
                    html.handle_data(item.content)
        else:
            html = HtmlLinks(line)
            html.feed(token.content)
        html.close()
        links.extend(html.links)
        anchors.update(html.anchors)
    return anchors | generated, links, blocks


def github_route(url):
    segments = unquote(url.path).strip("/").split("/")
    if url.scheme != "https":
        return []
    if url.hostname == "raw.githubusercontent.com" and len(segments) >= 4:
        return [*segments[:2], "raw", *segments[2:]]
    return segments if url.hostname == "github.com" else []


def same_repo_target(tree, url):
    if not tree.repository:
        return None
    segments = github_route(url)
    if len(segments) < 4 or "/".join(segments[:2]).lower() != tree.repository.lower():
        return None
    if segments[2] not in {"blob", "tree", "raw"}:
        return None
    candidates = segments[3:]
    qualified_raw = segments[2] == "raw" and candidates[:2] in (["refs", "heads"], ["refs", "tags"])
    stop = 2 if qualified_raw else 0
    for count in range(len(candidates) - (segments[2] != "tree"), stop, -1):
        ref = "/".join(candidates[:count])
        if qualified_raw:
            names = [ref.replace("refs/heads/", "refs/remotes/origin/", 1)
                     if candidates[1] == "heads" else ref]
        elif ref == "HEAD":
            try:
                default = tree.git("symbolic-ref", "refs/remotes/origin/HEAD").decode().strip()
            except ValueError:
                continue
            names = [default] if default.startswith("refs/remotes/origin/") else []
        elif SHA.fullmatch(ref):
            names = [ref]
        else:
            remote = f"refs/remotes/origin/{ref}"
            names = [remote, f"refs/tags/{ref}"]
            try:
                tree.resolve(remote)
            except ValueError:
                pass
            else:
                names.append(f"refs/heads/{ref}")
            if re.fullmatch(r"[0-9a-f]{4,39}", ref):
                objects = tree.git("rev-parse", f"--disambiguate={ref}").decode().split()
                if len(objects) == 1:
                    names.append(objects[0])
        resolved = set()
        for name in names:
            try:
                resolved.add(tree.resolve(name))
            except ValueError:
                continue
        if not resolved:
            continue
        if len(resolved) > 1:
            raise ValueError(f"conflicting commits for same-repository ref: {ref}")
        commit = resolved.pop()
        return "/".join(candidates[count:]), commit
    raise LookupError(f"unresolved same-repository ref: {url.path}")


def target_for(tree, source, url):
    if url.scheme or url.netloc:
        return same_repo_target(tree, url)
    raw = unquote(url.path)
    if not raw:
        return source, None
    path = posixpath.normpath(raw.lstrip("/") if raw.startswith("/") else posixpath.join(posixpath.dirname(source), raw))
    if path == ".." or path.startswith("../") or "\\" in path:
        raise ValueError("relative link escapes the selected repository")
    return "" if path == "." else path, None


def check_fragment(tree, path, commit, fragment, *, plain=False, cache=None):
    if not fragment:
        return
    entries = tree.entries(commit)
    if path not in entries:
        target = readme_path(entries, path, homepage=not path)
        if not target:
            raise LookupError("directory has no supported README for the fragment")
        path = target
    line_mode = plain or suffix(path) not in MARKDOWN
    draft = tree.draft and commit is None
    key = (entries[path][1], line_mode)
    available = cache if cache is not None and not draft else {}
    if key not in available:
        text = tree.read(path, commit).decode("utf-8")
        available[key] = ((len(physical_lines(text.removesuffix("\n"))) if text else 0)
                          if line_mode else parse_markdown(text)[0])
    if line_mode:
        coordinates = LINE_RANGE.fullmatch(fragment)
        if not coordinates:
            raise LookupError("fragment format is unsupported for this file")
        start, end = coordinates.groups()
        first, last = int(start), int(end or start)
        if not 1 <= first <= last <= available[key]:
            raise ValueError("source line fragment outside the file or reversed")
    elif fragment not in available[key]:
        raise ValueError("missing local heading or named anchor")


def media_bytes(tree, path, commit):
    data = tree.read(path, commit)
    if not data.startswith(LFS_HOSTS):
        return data
    pointer = LFS_POINTER.fullmatch(data) if len(data) < 1024 else None
    if not pointer:
        raise ValueError("malformed Git LFS media pointer")
    extensions, oid, raw_size = pointer.groups()
    size = int(raw_size)
    if size > (1 << 63) - 1:
        raise ValueError("malformed Git LFS media pointer size")
    if extensions:
        priorities = [line[4] for line in extensions.splitlines()]
        if priorities != sorted(set(priorities)):
            raise ValueError("malformed Git LFS media pointer extension order")
        raise LookupError("Git LFS pointer extensions were not inspected")
    if size > MAX_CACHED_MEDIA_BYTES:
        raise LookupError("Git LFS media object exceeds the offline validation limit")
    digest = oid.decode()
    common = Path(tree.git("rev-parse", "--path-format=absolute", "--git-common-dir").decode().strip())
    cached = common / "lfs" / "objects" / digest[:2] / digest[2:4] / digest
    try:
        if not cached.is_file():
            raise LookupError("Git LFS media object unavailable in the local cache")
        with cached.open("rb") as handle:
            contents = handle.read(size + 1)
    except FileNotFoundError as error:
        raise LookupError("Git LFS media object unavailable in the local cache") from error
    if len(contents) != size or sha256(contents).hexdigest() != digest:
        raise ValueError("cached Git LFS media object does not match the pointer")
    return contents


def verify_media(path, data):
    extension = suffix(path)
    if extension == ".svg":
        from xml.etree import ElementTree
        try:
            element = ElementTree.fromstring(data)
        except ElementTree.ParseError as error:
            raise ValueError("invalid SVG image") from error
        if element.tag != "{http://www.w3.org/2000/svg}svg":
            raise ValueError("expected an SVG root in the SVG namespace")
    elif extension in IMAGE_FORMATS:
        try:
            with Image.open(BytesIO(data)) as image:
                if image.format != IMAGE_FORMATS[extension]:
                    raise ValueError("image type differs from its extension")
                image.verify()
            with Image.open(BytesIO(data)) as image:
                total_pixels = 0
                for frame in range(MAX_MEDIA_FRAMES + 1):
                    try:
                        image.seek(frame)
                    except EOFError:
                        break
                    total_pixels += image.width * image.height
                    if frame == MAX_MEDIA_FRAMES or total_pixels > MAX_MEDIA_PIXELS:
                        raise LookupError("media exceeds the frame or decoded pixel limit")
                    image.load()
                if image.format == "GIF" and not data.rstrip(b"\0").endswith(b";"):
                    raise ValueError("invalid or unreadable image: GIF trailer missing")
        except (OSError, SyntaxError, struct.error, Image.DecompressionBombError) as error:
            raise ValueError("invalid or unreadable image") from error
    else:
        raise LookupError("media format was not inspected")


def check_document(tree, source, errors, gaps, *, archive_scope=None, checked_media=None, source_commit=None):
    if suffix(source) not in MARKDOWN:
        gaps.append(f"{source}: link checking for this README format is unavailable")
        return 0
    text = tree.read(source, source_commit).decode("utf-8")
    _, links, _ = parse_markdown(text)
    count = 0
    anchor_cache = {}
    for link in links:
        try:
            if link.coverage_gap:
                gaps.append(f"{source}:{link.line}: {link.coverage_gap}")
                continue
            if link.diagnostic:
                raise ValueError(link.diagnostic)
            if link.unnamed:
                raise ValueError("link has no accessible name")
            url = urlsplit(link.path)
            target = target_for(tree, source, url)
            if target is None:
                gaps.append(f"{source}:{link.line}: external link not checked: {link.path}")
                continue
            path, selected_commit = target
            commit = selected_commit if selected_commit is not None else source_commit
            entries = tree.entries(commit)
            directory = not path or (path not in entries and any(name.startswith(path + "/") for name in entries))
            if path not in entries and not directory:
                if archive_scope and not link.image and not path.startswith(archive_scope + "/assets/"):
                    gaps.append(f"{source}:{link.line}: original repository route outside import: {link.path}")
                    continue
                raise ValueError("missing tracked local target")
            if path in entries and entries[path][0] not in REGULAR_MODES:
                raise LookupError("target is a Git symlink or submodule")
            if link.image:
                if directory:
                    raise ValueError("image target is a directory")
                contents = media_bytes(tree, path, commit)
                verify_media(path, contents)
                if checked_media is not None:
                    identity = (path, commit or tree.commit, tree.draft and commit is None, sha256(contents).hexdigest())
                    checked_media.add(identity)
            if url.fragment and github_route(url)[2:3] == ["raw"]:
                gaps.append(f"{source}:{link.line}: raw GitHub file fragment was not checked: {link.path}")
            else:
                check_fragment(tree, path, commit, unquote(url.fragment),
                               plain=parse_qs(url.query).get("plain") in (["1"], ["true"]), cache=anchor_cache)
            count += 1
        except (ValueError, OSError, KeyError) as error:
            errors.append(f"{source}:{link.line}: {error}: {link.path}")
        except LookupError as error:
            gaps.append(f"{source}:{link.line}: {error}: {link.path}")
    return count
