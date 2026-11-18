#!/usr/bin/env python3
"""Import posts from a Teletype blog into Zola page bundles.

    python3 scripts/teletype-import.py https://blog.antono.info [uri ...]

Each post becomes content/blog/YYYY/MM/DD/<slug>/index.en.md (+ its images).
The date is the UTC publication date. Teletype's article JSON is read from the
`window.__INITIAL_STATE__` blob embedded in every post page, so this needs no
API token. Run scripts/mirror-translations.py afterwards.

Conversion is meant to be lossless for what Teletype renders: text that
Teletype showed literally (e.g. `**bold**` typed as plain text) is escaped so
Markdown shows it literally too. Non-breaking spaces used for indentation in
code blocks are turned into plain spaces (they render the same).
"""

import html
import json
import re
import sys
import unicodedata
import urllib.request
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content" / "blog"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) zola-import"}

# Teletype URIs that are random ids get a slug from the title instead.
RANDOM_URI = re.compile(r"^[A-Za-z0-9]{9}$")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def state_of(page: str) -> dict:
    m = re.search(r"window\.__INITIAL_STATE__=(\{.*?\});window\.__PUBLIC", page, re.S)
    if not m:
        raise ValueError("no __INITIAL_STATE__ on page")
    return json.loads(m.group(1))


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ---------------------------------------------------------------- parsing


class Node:
    def __init__(self, tag, attrs=None):
        self.tag = tag
        self.attrs = dict(attrs or [])
        self.children = []

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)


class TreeBuilder(HTMLParser):
    VOID = {"hr", "br", "image"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        # <image ...> may or may not wrap a <caption>; treat it as a container
        # until </image> or the next sibling block closes it.
        if tag not in ("hr", "br"):
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].children.append(Node(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


# ---------------------------------------------------------------- rendering

MD_SPECIAL = re.compile(r"([\\`*\[\]<>|~]|(?<![A-Za-z0-9])_|_(?![A-Za-z0-9]))")


def escape_text(s: str) -> str:
    s = MD_SPECIAL.sub(r"\\\1", s)
    # "&lt;" typed literally must not become an entity.
    return re.sub(r"&(?=#?\w+;)", r"\\&", s)


def escape_line_start(s: str) -> str:
    # Things that would turn a paragraph into a heading/list/quote/rule.
    s = re.sub(r"^(\s*)([#>+=-])", r"\1\\\2", s)
    return re.sub(r"^(\s*\d+)([.)])(\s)", r"\1\\\2\3", s)


def code_span(s: str) -> str:
    n = max((len(m) for m in re.findall(r"`+", s)), default=0) + 1
    fence = "`" * n
    pad = " " if s.startswith("`") or s.endswith("`") else ""
    return f"{fence}{pad}{s}{pad}{fence}"


class Renderer:
    def __init__(self, link_map, topic_map, images):
        self.link_map = link_map  # old URL path (uri) -> "@/blog/.../index.en.md"
        self.topic_map = topic_map  # topic_id -> tag slug
        self.images = images  # list of (url, filename) to download

    # inline ---------------------------------------------------------------

    def inline(self, node) -> str:
        out = []
        for c in node.children:
            if isinstance(c, str):
                out.append(escape_text(c))
                continue
            inner = self.inline(c)
            if c.tag == "strong":
                out.append(self.wrap(inner, "**"))
            elif c.tag == "em":
                out.append(self.wrap(inner, "*"))
            elif c.tag == "code":
                out.append(self.code(c))
            elif c.tag == "a":
                out.append(f"[{inner}]({self.href(c.attrs.get('href', ''))})")
            elif c.tag == "br":
                out.append("\\\n")
            else:
                raise ValueError(f"unknown inline tag <{c.tag}>")
        return "".join(out)

    def code(self, node) -> str:
        # Teletype allows links inside inline code (<code><a>Ok</a></code>).
        # Markdown doesn't, so a linked piece becomes [`Ok`](url) instead.
        parts = []
        for c in node.children:
            if isinstance(c, str):
                parts.append(code_span(c) if c else "")
            elif c.tag == "a":
                parts.append(f"[{code_span(c.text())}]({self.href(c.attrs.get('href', ''))})")
            else:
                parts.append(code_span(c.text()))
        return "".join(parts)

    @staticmethod
    def wrap(inner, mark):
        # Markdown emphasis can't start/end with whitespace: keep it outside.
        m = re.match(r"^(\s*)(.*?)(\s*)$", inner, re.S)
        lead, body, trail = m.groups()
        return f"{lead}{mark}{body}{mark}{trail}" if body else inner

    def href(self, url: str) -> str:
        url = url.strip()  # browsers ignore surrounding whitespace in href
        m = re.match(r"^https?://blog\.antono\.info/?\?topic_id=(\d+)$", url)
        if m:
            return f"/en/tags/{self.topic_map[m.group(1)]}/"
        m = re.match(r"^https?://blog\.antono\.info/([^/?#]+)/?(?:\?cda=.*)?$", url)
        if m and m.group(1) in self.link_map:
            return self.link_map[m.group(1)]
        if m:
            raise ValueError(f"link to unknown post: {url}")
        return url.replace(" ", "%20").replace(")", "%29")

    # blocks ---------------------------------------------------------------

    def blocks(self, node) -> list[str]:
        out = []
        for c in node.children:
            if isinstance(c, str):
                if c.strip():
                    raise ValueError(f"stray text in document: {c!r}")
                continue
            block = self.block(c)
            if block is not None:
                out.append(block)
        return out

    def block(self, n):
        tag = n.tag
        if tag == "p":
            text = self.inline(n).strip()
            return escape_line_start(text) if text else None
        if tag in ("h1", "h2", "h3", "h4"):
            level = {"h1": 1, "h2": 2, "h3": 3, "h4": 4}[tag]
            return "#" * level + " " + self.inline(n).strip()
        if tag == "blockquote":
            text = self.inline(n).strip()
            return "\n".join("> " + line if line else ">" for line in text.split("\n"))
        if tag == "pre":
            code = n.text().replace(" ", " ").rstrip("\n")
            code = "\n".join(l.rstrip() for l in code.split("\n"))  # trailing spaces cause horizontal scroll
            n_ticks = max((len(m) for m in re.findall(r"`{3,}", code)), default=2) + 1
            fence = "`" * n_ticks
            return f"{fence}{n.attrs.get('lang', '')}\n{code}\n{fence}"
        if tag in ("ul", "ol"):
            items = []
            for i, li in enumerate(c for c in n.children if not isinstance(c, str)):
                if li.tag != "li":
                    raise ValueError(f"<{li.tag}> inside <{tag}>")
                marker = f"{i + 1}." if tag == "ol" else "-"
                text = self.inline(li).strip()
                items.append(f"{marker} {text}")
            return "\n".join(items)
        if tag == "hr":
            return "---"
        if tag == "image":
            src = n.attrs["src"]
            name = src.rsplit("/", 1)[-1]
            self.images.append((src, name))
            caption = next((c for c in n.children if not isinstance(c, str) and c.tag == "caption"), None)
            cap = self.inline(caption).strip() if caption else ""
            img = f"![]({name})"
            return f"{img}\n*{cap}*" if cap else img
        if tag in ("tags", "tag"):
            return None  # handled as taxonomy
        raise ValueError(f"unknown block tag <{tag}>")


# ---------------------------------------------------------------- output


def toml_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def iso(ts: str) -> str:
    d = datetime.fromisoformat(ts.replace("Z", "+00:00"))
    return d.isoformat(timespec="seconds").replace("+00:00", "Z")


def post_dir(article, slug) -> Path:
    d = datetime.fromisoformat(article["published_at"].replace("Z", "+00:00"))
    return CONTENT / f"{d:%Y}" / f"{d:%m}" / f"{d:%d}" / slug


def main():
    base = sys.argv[1].rstrip("/")
    uris = sys.argv[2:]

    home = state_of(fetch(base + "/").decode())
    blog = next(iter(home["blog_articles"]["items"].values()))
    published = blog["sections"]["published"]
    if not uris:
        uris = [a["uri"] for a in blog["articles"]]  # first page only (10)
    if len(uris) < published:
        print(f"warning: blog has {published} published posts, importing {len(uris)}", file=sys.stderr)

    articles = {}
    for uri in uris:
        st = state_of(fetch(f"{base}/{uri}").decode())
        (art,) = st["articles"]["items"].values()
        articles[uri] = art

    slugs = {
        uri: slugify(a["title"]) if RANDOM_URI.match(uri) else slugify(uri)
        for uri, a in articles.items()
    }
    link_map = {
        uri: "@/" + str(post_dir(a, slugs[uri]).relative_to(ROOT / "content")) + "/index.en.md"
        for uri, a in articles.items()
    }
    topic_map = {}
    for a in articles.values():
        for t in a.get("topics") or []:
            topic_map[str(t["id"])] = slugify(t["uri"])

    for uri, a in articles.items():
        images = []
        tb = TreeBuilder()
        tb.feed(a["text"])
        (doc,) = [c for c in tb.root.children if not isinstance(c, str)]
        body = "\n\n".join(Renderer(link_map, topic_map, images).blocks(doc)) + "\n"

        tags = [slugify(t["uri"]) for t in a.get("topics") or []]
        tags += [slugify(t.text()) for t in _find(doc, "tag")]
        tags = list(dict.fromkeys(tags))

        fm = [
            "+++",
            f"title = {toml_str(a['title'])}",
            f"date = {iso(a['published_at'])}",
        ]
        if a.get("last_edited_at") and a["last_edited_at"] != a["published_at"]:
            fm.append(f"updated = {iso(a['last_edited_at'])}")
        fm.append(f"aliases = [{toml_str('/' + uri + '/')}]")
        fm += ["", "[taxonomies]", f"tags = [{', '.join(toml_str(t) for t in tags)}]"]
        fm += ["", "[extra]", 'lang = "en"', f"teletype = {toml_str(base + '/' + uri)}", "+++", ""]

        out = post_dir(a, slugs[uri])
        out.mkdir(parents=True, exist_ok=True)
        (out / "index.en.md").write_text("\n".join(fm) + body, encoding="utf-8")
        for src, name in images:
            if not (out / name).exists():
                (out / name).write_bytes(fetch(src))
        print(f"{uri} -> {out.relative_to(ROOT)} ({len(images)} images)")


def _find(node, tag):
    for c in node.children:
        if isinstance(c, str):
            continue
        if c.tag == tag:
            yield c
        yield from _find(c, tag)


if __name__ == "__main__":
    main()
