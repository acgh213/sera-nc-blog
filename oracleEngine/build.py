#!/usr/bin/env python3
"""
OracleEngine — Static blog generator for sera-nc-blog

Reads markdown posts from blog/drafts/, filters by published: true frontmatter,
converts to HTML, and outputs a complete static site to _site/.
"""

import os
import re
import shutil
import sys
from collections import OrderedDict
from datetime import date, datetime
from pathlib import Path

import markdown
import yaml

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BLOG_TITLE = "Sera"
BLOG_SUBTITLE = "Field notes from the middle space"
POSTS_PER_PAGE = 5

DRAFTS_DIR = Path("blog/drafts")
OUTPUT_DIR = Path("_site")
TEMPLATES_DIR = Path("oracleEngine/templates")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(text):
    """Parse YAML frontmatter delimited by --- from markdown text."""
    if not text.startswith("---"):
        return {}, text

    end = text.find("---", 3)
    if end == -1:
        return {}, text

    front = text[3:end].strip()
    body = text[end + 3:].strip()

    try:
        meta = yaml.safe_load(front) or {}
    except yaml.YAMLError as exc:
        print(f"  Warning: bad frontmatter — {exc}", file=sys.stderr)
        meta = {}

    return meta, body


def excerpt_from_html(html_content, length=220):
    """Extract a plain-text excerpt from HTML content."""
    text = re.sub(r"<[^>]+>", "", html_content)
    text = " ".join(text.split())
    if len(text) <= length:
        return text
    return text[:length].rsplit(" ", 1)[0] + "\u2026"


def format_date(date_val):
    """Format a date value into a human-readable string."""
    if isinstance(date_val, (date, datetime)):
        return date_val.strftime("%B %-d, %Y")
    try:
        d = datetime.strptime(str(date_val), "%Y-%m-%d")
        return d.strftime("%B %-d, %Y")
    except (ValueError, TypeError):
        return str(date_val)


def render_tags(tags):
    """Render a list of tags as HTML <span> elements."""
    return "".join(f'<span class="tag">{t}</span>' for t in (tags or []))


def render_template(template, **kwargs):
    """Simple template rendering — replaces {{key}} placeholders."""
    result = template
    for key, value in kwargs.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result


# ---------------------------------------------------------------------------
# Build pipeline
# ---------------------------------------------------------------------------

def build():
    repo_root = Path.cwd()
    drafts = repo_root / DRAFTS_DIR
    out = repo_root / OUTPUT_DIR
    tpl_dir = repo_root / TEMPLATES_DIR

    if not drafts.exists():
        print(f"Error: drafts directory not found at {drafts}", file=sys.stderr)
        sys.exit(1)

    # Clean and create output directories
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / "posts").mkdir()

    # Load templates and CSS
    css = (tpl_dir / "style.css").read_text(encoding="utf-8")
    post_tpl = (tpl_dir / "post.html").read_text(encoding="utf-8")
    index_tpl = (tpl_dir / "index.html").read_text(encoding="utf-8")
    archive_tpl = (tpl_dir / "archive.html").read_text(encoding="utf-8")

    md_converter = markdown.Markdown(extensions=["extra", "smarty"])

    # -- Phase 1: Parse all published posts --------------------------------

    posts = []
    for md_file in sorted(drafts.glob("*.md")):
        print(f"  Scanning {md_file.name}")
        raw = md_file.read_text(encoding="utf-8")
        meta, body = parse_frontmatter(raw)

        if not meta.get("published", False):
            print(f"    → skipped (not published)")
            continue

        md_converter.reset()
        html_body = md_converter.convert(body)
        slug = md_file.stem

        posts.append({
            "slug": slug,
            "title": meta.get("title", "Untitled"),
            "date": str(meta.get("date", "")),
            "date_display": format_date(meta.get("date")),
            "mode": meta.get("mode", ""),
            "tags": meta.get("tags", []),
            "html_body": html_body,
            "excerpt": excerpt_from_html(html_body),
        })

    # Sort by date ascending so navigation reads chronologically
    posts.sort(key=lambda p: p["date"])

    # -- Phase 2: Render individual post pages -----------------------------

    for i, post in enumerate(posts):
        prev_html = ""
        next_html = ""

        if i > 0:
            prev = posts[i - 1]
            prev_html = (
                f'<a href="{prev["slug"]}.html">'
                f'<span class="nav-label">\u2190 Previous</span>'
                f"{prev['title']}</a>"
            )
        if i < len(posts) - 1:
            nxt = posts[i + 1]
            next_html = (
                f'<a class="next" href="{nxt["slug"]}.html">'
                f'<span class="nav-label">Next \u2192</span>'
                f"{nxt['title']}</a>"
            )

        mode_display = post["mode"].replace("_", " ")

        html = render_template(
            post_tpl,
            styles=css,
            title=post["title"],
            date=post["date_display"],
            mode=mode_display,
            tags=render_tags(post["tags"]),
            content=post["html_body"],
            prev_link=prev_html,
            next_link=next_html,
            blog_title=BLOG_TITLE,
        )

        dest = out / "posts" / f"{post['slug']}.html"
        dest.write_text(html, encoding="utf-8")
        print(f"    → published: {post['title']}")

    # -- Phase 3: Render paginated index pages ------------------------------

    posts_desc = list(reversed(posts))  # newest first for listing
    total_pages = max(1, -(-len(posts_desc) // POSTS_PER_PAGE))

    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * POSTS_PER_PAGE
        page_posts = posts_desc[start : start + POSTS_PER_PAGE]

        # Paths differ for page 1 vs subsequent pages
        if page_num == 1:
            page_path = out / "index.html"
            posts_prefix = "posts/"
            archive_link = "archive/index.html"
            root = ""
        else:
            (out / "page").mkdir(exist_ok=True)
            page_path = out / "page" / f"{page_num}.html"
            posts_prefix = "../posts/"
            archive_link = "../archive/index.html"
            root = "../"

        # Build post listing HTML
        listing_html = ""
        for post in page_posts:
            mode_display = post["mode"].replace("_", " ")
            listing_html += (
                '<article class="post-preview">\n'
                f'  <a href="{posts_prefix}{post["slug"]}.html">\n'
                f"    <h2>{post['title']}</h2>\n"
                "  </a>\n"
                '  <div class="post-meta">\n'
                f"    <time>{post['date_display']}</time>\n"
                f'    <span class="mode">{mode_display}</span>\n'
                "  </div>\n"
                f'  <div class="tags">{render_tags(post["tags"])}</div>\n'
                f'  <p class="excerpt">{post["excerpt"]}</p>\n'
                "</article>\n"
            )

        if not listing_html:
            listing_html = (
                '<div class="empty-state">No published posts yet.</div>'
            )

        # Build pagination HTML
        pagination_html = ""
        if total_pages > 1:
            # "← Newer" link (lower page number = newer posts)
            if page_num > 1:
                if page_num == 2:
                    newer_href = f"{root}index.html"
                else:
                    newer_href = f"{page_num - 1}.html"
                newer_link = f'<a href="{newer_href}">&larr; Newer</a>'
            else:
                newer_link = '<span class="pagination-spacer">&larr; Newer</span>'

            # "Older →" link (higher page number = older posts)
            if page_num < total_pages:
                if page_num == 1:
                    older_href = "page/2.html"
                else:
                    older_href = f"{page_num + 1}.html"
                older_link = f'<a href="{older_href}">Older &rarr;</a>'
            else:
                older_link = '<span class="pagination-spacer">Older &rarr;</span>'

            pagination_html = (
                '<nav class="pagination">\n'
                f"  {newer_link}\n"
                f'  <span class="pagination-info">'
                f"Page {page_num} of {total_pages}</span>\n"
                f"  {older_link}\n"
                "</nav>"
            )

        page_html = render_template(
            index_tpl,
            styles=css,
            posts=listing_html,
            pagination=pagination_html,
            blog_title=BLOG_TITLE,
            blog_subtitle=BLOG_SUBTITLE,
            archive_link=archive_link,
        )
        page_path.write_text(page_html, encoding="utf-8")

    # -- Phase 4: Render archive page (posts grouped by year → month) ------

    (out / "archive").mkdir(exist_ok=True)

    archive_groups = OrderedDict()
    for post in posts_desc:
        try:
            d = datetime.strptime(post["date"], "%Y-%m-%d")
            year = d.year
            month_key = (d.month, d.strftime("%B"))
        except (ValueError, TypeError):
            year = 0
            month_key = (0, "Unknown")

        archive_groups.setdefault(year, OrderedDict()).setdefault(
            month_key, []
        ).append(post)

    archive_content = ""
    for year, months in archive_groups.items():
        archive_content += f'<section class="archive-year">\n<h2>{year}</h2>\n'
        for (_month_num, month_name), month_posts in months.items():
            archive_content += (
                f'<section class="archive-month">\n<h3>{month_name}</h3>\n'
                '<ul class="archive-posts">\n'
            )
            for post in month_posts:
                archive_content += (
                    f"<li><time>{post['date_display']}</time>"
                    f'<a href="../posts/{post["slug"]}.html">'
                    f"{post['title']}</a></li>\n"
                )
            archive_content += "</ul>\n</section>\n"
        archive_content += "</section>\n"

    if not archive_content:
        archive_content = (
            '<div class="empty-state">No published posts yet.</div>'
        )

    archive_html = render_template(
        archive_tpl,
        styles=css,
        archive_content=archive_content,
        blog_title=BLOG_TITLE,
    )
    (out / "archive" / "index.html").write_text(archive_html, encoding="utf-8")

    print(f"\n  Build complete — {len(posts)} post(s), {total_pages} page(s) → {out}/")


if __name__ == "__main__":
    build()
