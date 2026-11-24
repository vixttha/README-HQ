"""Check rendered Markdown destinations against the selected Git tree."""

from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from io import BytesIO
import posixpath
import re
import unicodedata
from urllib.parse import unquote, urlsplit

from markdown_it import MarkdownIt
from markdown_it.rules_inline import autolink, html_inline, image, link
from PIL import Image

from hq_data import REGULAR_MODES, SHA, physical_lines


MARKDOWN = {".md", ".markdown", ".mdown", ".mkdn"}
README_FORMATS = [".md", ".markdown", ".mdown", ".mkdn", ".rst", ".adoc", ".asciidoc", ".asc", ".txt", ""]
IMAGE_FORMATS = {".png": "PNG", ".gif": "GIF", ".jpg": "JPEG", ".jpeg": "JPEG", ".webp": "WEBP"}
LINE_RANGE = re.compile(r"L([0-9]+)(?:-L([0-9]+))?")
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

    def handle_starttag(self, tag, options):
        attrs = dict(options)
        line = self.line + self.getpos()[0] - 1
        if tag == "a":
            if attrs.get("name"):
                self.anchors.add(attrs["name"])
            if attrs.get("href"):
                self.controls.append([attrs["href"], line, bool((attrs.get("aria-label") or "").strip())])
        if tag in {"source", "img"} and "srcset" in attrs:
            srcset = attrs["srcset"] or ""
            try:
                sources = image_sources(srcset)
            except ValueError:
                self.links.append(Link(srcset, line, coverage_gap="unsupported image source list"))
            else:
                self.links.extend(Link(url, line, True) for url in sources)
        if tag == "img" and attrs.get("src"):
            self.links.append(Link(attrs["src"], line, True))
            if self.controls and (attrs.get("alt") or "").strip():
                self.controls[-1][2] = True

    def handle_data(self, data):
        if self.controls and data.strip():
            self.controls[-1][2] = True

    def handle_endtag(self, tag):
        if tag == "a" and self.controls:
            path, line, named = self.controls.pop()
            self.links.append(Link(path, line, unnamed=not named))


def inline_links(children, line):
    links = []
    for index, token in enumerate(children):
        occurrence = line + token.meta.get("source_line_offset", 0)
        if token.type == "image":
            links.append(Link(token.attrGet("src"), occurrence, True))
        elif token.type == "link_open":
            end = next((i for i in range(index + 1, len(children)) if children[i].type == "link_close"), len(children))
            name = "".join(item.content for item in children[index + 1:end]
                           if item.type in {"text", "code_inline", "image"})
            links.append(Link(token.attrGet("href"), occurrence, unnamed=not name.strip()))
    return links


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


def same_repo_target(tree, url):
    if url.scheme != "https" or url.hostname != "github.com" or not tree.repository:
        return None
    segments = unquote(url.path).strip("/").split("/")
    if len(segments) < 4 or "/".join(segments[:2]).lower() != tree.repository.lower():
        return None
    if segments[2] not in {"blob", "tree", "raw"}:
        return None
    candidates = segments[3:]
    for count in range(len(candidates) - (segments[2] != "tree"), 0, -1):
        ref = "/".join(candidates[:count])
        if SHA.fullmatch(ref) or ref == "HEAD":
            names = [ref]
        else:
            names = [f"refs/heads/{ref}", f"refs/remotes/origin/{ref}", f"refs/tags/{ref}"]
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


def check_fragment(tree, path, commit, fragment, *, plain=False):
    if not fragment:
        return
    entries = tree.entries(commit)
    if path not in entries:
        target = readme_path(entries, path, homepage=not path)
        if not target:
            raise LookupError("directory has no supported README for the fragment")
        path = target
    data = tree.read(path, commit)
    text = data.decode("utf-8")
    if plain or suffix(path) not in MARKDOWN:
        coordinates = LINE_RANGE.fullmatch(fragment)
        if not coordinates:
            raise LookupError("fragment format is unsupported for this file")
        start, end = coordinates.groups()
        first, last = int(start), int(end or start)
        line_count = len(physical_lines(text.removesuffix("\n"))) if text else 0
        if not 1 <= first <= last <= line_count:
            raise ValueError("source line fragment outside the file or reversed")
    elif fragment not in parse_markdown(text)[0]:
        raise ValueError("missing local heading or named anchor")


def verify_media(path, data):
    extension = suffix(path)
    if extension == ".svg":
        from xml.etree import ElementTree
        try:
            element = ElementTree.fromstring(data)
        except ElementTree.ParseError as error:
            raise ValueError("invalid SVG image") from error
        if element.tag.rsplit("}", 1)[-1] != "svg":
            raise ValueError("expected an SVG root")
    elif extension in IMAGE_FORMATS:
        try:
            with Image.open(BytesIO(data)) as image:
                if image.format != IMAGE_FORMATS[extension]:
                    raise ValueError("image type differs from its extension")
                image.verify()
            with Image.open(BytesIO(data)) as image:
                image.load()
        except (OSError, SyntaxError, Image.DecompressionBombError) as error:
            raise ValueError("invalid or unreadable image") from error
    else:
        raise LookupError("media format was not inspected")


def check_document(tree, source, errors, gaps, *, archive_scope=None):
    if suffix(source) not in MARKDOWN:
        gaps.append(f"{source}: link checking for this README format is unavailable")
        return 0
    text = tree.read(source).decode("utf-8")
    _, links, _ = parse_markdown(text)
    count = 0
    for link in links:
        try:
            if link.coverage_gap:
                gaps.append(f"{source}:{link.line}: {link.coverage_gap}")
                continue
            if link.unnamed:
                raise ValueError("link has no accessible name")
            url = urlsplit(link.path)
            target = target_for(tree, source, url)
            if target is None:
                gaps.append(f"{source}:{link.line}: external link not checked: {link.path}")
                continue
            path, commit = target
            entries = tree.entries(commit)
            directory = not path or any(name.startswith(path + "/") for name in entries)
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
                verify_media(path, tree.read(path, commit))
            check_fragment(tree, path, commit, unquote(url.fragment), plain=url.query in {"plain=1", "plain=true"})
            count += 1
        except (ValueError, OSError, KeyError) as error:
            errors.append(f"{source}:{link.line}: {error}: {link.path}")
        except LookupError as error:
            gaps.append(f"{source}:{link.line}: {error}: {link.path}")
    return count
