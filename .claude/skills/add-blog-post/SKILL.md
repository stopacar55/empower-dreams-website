---
name: add-blog-post
description: Add a new blog post to the EmpowerDreams.org website — turning raw Facebook posts, written drafts, or pasted text into a styled, image-rich blog entry that matches the site's existing design. Use this skill whenever the user wants to publish a new entry on the blog, add a story to empowerdreams.org/blog, convert a Facebook post into a blog post, write up a ministry update for the site, post a field story, or add an entry to the blog grid — even if they don't explicitly say the word "blog". The skill handles the HTML template, image conventions, blog.html card insertion, and reminds Claude of the repo's branch/commit standing rules.
---

# Add a Blog Post to EmpowerDreams.org

This skill captures the proven workflow for adding a new entry to the EmpowerDreams.org blog. The site is a static HTML site managed in a Git repo (`stopacar55/empower-dreams-website`). Each blog entry is a standalone HTML file in `/blog/`, plus a card on `/blog.html`.

## What you need from the user

Before doing anything, you need three things. If any are missing, ask before proceeding:

1. **The post text.** Plain text, in the user's voice. Can be pasted Facebook post, a draft they wrote, dictated notes, etc.
2. **The date.** When the post should appear chronologically.
3. **The images.** Either uploaded into the chat, saved into `~/PicturesForClaude/` (or another folder Claude has access to), or explicit confirmation that the post is text-only.

If the user pastes a Facebook iframe embed (the `<iframe src="...">` kind), the `href=...` URL inside the iframe is the Facebook permalink. You can navigate the Claude in Chrome MCP to `https://www.facebook.com/plugins/post.php?href=<URL-encoded permalink>&show_text=true&width=500` to get a clean rendering of just the post text. Then visit the regular permalink (`https://www.facebook.com/<page>/posts/<pfbid...>`) and use `javascript_tool` with a `[dir="auto"]` selector to grab the full untruncated text. The plugin URL truncates at "...See more"; the full text comes from the regular page DOM. See `references/facebook-extraction.md` for the exact JavaScript snippet.

## Project layout

```
empower-dreams-website/
├── blog.html                      # The blog index page (cards)
├── blog/
│   ├── <slug>.html                # Individual post pages
│   └── videos/                    # Embedded MP4s
├── images/
│   ├── 2025-year-in-review.png    # (etc — featured/banner images)
│   └── blog/                      # Per-post images for new posts
└── styles.css, pages.css, main.js # Shared styles & nav (don't touch)
```

## Standing rules from the repo

**Critical — read these every time:**

- **Never push to `main`.** Always create or work on a `pas/<short-description>` branch.
- **Before any `git commit`, show the user `git status` and `git diff --staged` and wait for their explicit go-ahead.**
- **Never run `git push --force` or `--force-with-lease`.**
- Read the project's `CLAUDE.md` if present. (Currently the standing rules also live in `ChangeNotes` at the project root.)

If you're on `main` when this skill is invoked, create a new branch first:
```
git checkout -b pas/add-blog-<short-description>
```

## Image conventions

These are the user's stated rules — apply them consistently:

| Number of unique images | What to do |
|---|---|
| **1 image** | Use that single image both inside the post and as the blog.html card thumbnail. |
| **2 unique images** | Use both inside the post. For the card thumbnail, create a side-by-side composite via `scripts/make_card_composite.py`. |
| **More than 2 unique images** | Use all inside the post. Use a dedicated cover picture (e.g., `<slug>-cover.png`) for the card thumbnail. If the user didn't provide a cover, ask whether they want to supply one or fall back to the first image. |
| **Duplicates** | Always ignore. Run `md5sum` to detect — users sometimes accidentally copy the same file under multiple names. |
| **No images** | Build the post text-only, or use a poster frame from a video if one's embedded. |

File naming inside `images/blog/`:
- `<slug>-1.jpg`, `<slug>-2.jpg`, ... — individual post images
- `<slug>-card.jpg` — side-by-side composite for the card (2-image case)
- `<slug>-cover.png` — dedicated cover for the card (3+ image case)
- `<slug>-poster.jpg` — extracted video poster frame (video case)

## Step-by-step

### 1. Gather inputs

Confirm you have post text, date, and images. If anything's missing, ask before proceeding.

### 2. Decide the slug and title

Pick a short, hyphenated, descriptive slug (no date prefix — dates live in the file body). Examples from past posts: `audio-bibles-discipleship`, `sudan-crisis`, `peru-ministry-continues`, `christmas-gift-of-gospel`, `katanga-beauty-from-ashes`. Check `blog/` for collisions.

Pick a title from the post text — usually the first compelling sentence or a short headline that captures the story. The title becomes both the `<title>` and the `<h1>` of the page.

### 3. Process the images

```
# Look at each image (use the Read tool on jpg/png files — they render visually)
# Hash-check for duplicates:
md5sum ~/PicturesForClaude/Feb20*.jpg

# Copy + rename to /images/blog/ using your chosen slug:
cp ~/PicturesForClaude/Feb20A.jpg /Users/pas/Claude/empower-dreams-website/images/blog/<slug>-1.jpg
# (repeat for each unique image)

# If exactly 2 non-duplicate images, run the composite script:
python3 .claude/skills/add-blog-post/scripts/make_card_composite.py \
  /images/blog/<slug>-1.jpg \
  /images/blog/<slug>-2.jpg \
  /images/blog/<slug>-card.jpg
```

For videos:
- Remux `.mov` → `.mp4` with `ffmpeg -i input.mov -c copy -movflags +faststart blog/videos/<slug>.mp4` (much faster than re-encoding since it's just a container swap)
- Extract a poster frame: `ffmpeg -i blog/videos/<slug>.mp4 -ss 00:00:03 -vframes 1 -vf "scale=720:-1" images/blog/<slug>-poster.jpg`
- Vertical/portrait videos (reels) should be constrained with `max-width: 480px` in the post HTML so they don't dominate the page.

### 4. Write the blog post HTML

Copy `assets/template.html` and replace the `{{PLACEHOLDERS}}`. The template covers the full structure: navbar, page header (with background image), post body, related-posts grid, footer. Most posts only need to customize:

- `{{TITLE}}` — the post title
- `{{META_DESCRIPTION}}` — 1–2 sentences for SEO/social
- `{{DATE_FULL}}` — e.g., "February 20, 2026"
- `{{CATEGORY}}` — short label, e.g., "Audio Bible Ministry", "Sudan Crisis", "Peru Ministry"
- `{{HEADER_BG_IMAGE}}` — path to header background, e.g., `../images/blog/<slug>-1.jpg`
- `{{INTRO}}` — first paragraph (the hook from the post)
- `{{BODY}}` — the main HTML body — paragraphs, images, highlight boxes, CTAs
- `{{RELATED_*}}` — three related posts (chronologically close or thematically linked)

Save to `blog/<slug>.html`.

### 5. Write the post body well

The user's social posts have a recognizable structure that translates well to blog form. Apply these patterns:

**Hook → story → key insight → call to action.** That's the natural flow. The first paragraph of the FB post is almost always the hook; use it as the `<p class="blog-post-intro">`.

**Use `<div class="highlight-box">`** for callout content: bulleted impact numbers, scripture quotes, Pastor/leader quotes, key promises. These break up walls of text and match the existing site style.

**Use `<figure class="blog-image">`** with these inline styles for full-width images interleaved between paragraphs:
```html
<figure class="blog-image" style="margin: 2rem 0;">
    <img src="../images/blog/<slug>-N.jpg" alt="..." loading="lazy"
         style="width: 100%; border-radius: var(--radius-md); box-shadow: var(--shadow-md);">
</figure>
```

**Convert "Read the full Year In Review" links** that point at FB or external URLs into relative links to existing site posts (typically `2025-year-in-review.html`).

**Convert "Give Monthly" / "Donate" CTAs** to `<a href="../donate.html">Give Monthly</a>`.

**Always preserve the closing boilerplate paragraph:** "Empower Dreams pays no salaries and covers its own operating expenses, so every dollar donated fuels mission impact through our partners."

**Strip Facebook hashtag links.** They have noisy `__cft__` query strings and don't belong on the blog.

### 6. Insert the card on blog.html

Cards on `blog.html` are listed in **reverse chronological order** (newest first). The "2025 Year in Review" featured post sits above the grid and stays there — don't move it.

Find the position by date and insert a new `<a class="blog-card-link">` block. The card looks like:
```html
<!-- {{TITLE}} - {{DATE_FULL}} -->
<a href="blog/<slug>.html" class="blog-card-link">
    <article class="blog-card">
        <div class="blog-card-image">
            <img src="images/blog/<slug>-card.jpg" alt="{{TITLE}}" loading="lazy">
        </div>
        <div class="blog-card-content">
            <div class="blog-meta">
                <span class="blog-date">{{DATE_FULL}}</span>
            </div>
            <h3>{{TITLE}}</h3>
            <p>{{CARD_EXCERPT}}</p>
            <span class="blog-read-more">Read More &rarr;</span>
        </div>
    </article>
</a>
```

The `{{CARD_EXCERPT}}` is 1–2 sentences distilled from the post — usually a rewrite of the intro, more compact and punchy. Aim for ~25 words.

For the `img src`:
- 1-image case: `images/blog/<slug>-1.jpg`
- 2-image case: `images/blog/<slug>-card.jpg` (side-by-side composite)
- 3+ image case: `images/blog/<slug>-cover.png` or whatever cover the user provided

### 7. Verify

Before declaring done, run these checks:
```bash
# Confirm the new file exists and the card got inserted
ls -la blog/<slug>.html
grep "<slug>" blog.html

# Confirm every image the post references actually exists
grep -oE '\.\./images/blog/[^"]+' blog/<slug>.html | sort -u | \
  sed "s|^\.\./||" | xargs -I{} ls -la {}

# Quick HTML smoke test (the file is well-formed and openable)
python3 -m http.server 8000 > /dev/null 2>&1 &
sleep 1 && curl -s -o /dev/null -w "HTTP %{http_code}\n" http://localhost:8000/blog/<slug>.html
```

Tell the user how to view it locally: `file:///Users/pas/Claude/empower-dreams-website/blog.html` in Chrome, or run `python3 -m http.server 8000` themselves.

### 8. Hand off for git

**Do not commit on the user's behalf without showing the diff first.** Follow the Standing Rules: show `git status`, show `git diff --staged`, and wait for the user to explicitly approve before committing. Then they (or you with their go-ahead) push the branch and open a PR.

A typical handoff message:
> Post built and card inserted. Both files are on branch `pas/add-blog-<slug>`. To review the diff before committing:
> ```
> git status
> git diff blog.html blog/<slug>.html
> ```
> Tell me to proceed when you're ready and I'll stage, commit, and push.

## Edge cases & gotchas

**Featured post.** `2025-year-in-review.html` is the featured post above the grid. Don't touch it unless the user explicitly asks to change the featured slot. Newer posts go in the grid above where Year-in-Review's card *would* be — except Year-in-Review isn't in the grid at all, only the featured slot.

**Existing post with the same story.** Sometimes a date will pair with content already covered by an existing deeper post (e.g., a short FB teaser preceded a longer blog write-up). In that case, build a short "field flash" version and link to the existing fuller post with a `<a class="btn btn-primary">Read the Full Story &rarr;</a>` button.

**FB hashtag links.** Strip them — they have noisy `__cft__` query strings and don't render meaningfully on a blog.

**Multi-image carousel posts** (Facebook posts where each image is a designed slide with overlay text). Use ALL the images in narrative order — don't skip any. The slides usually tell the full story without needing matching body text. Body text should add context, not duplicate what's on the images.

**Image URLs from Facebook are blocked** by Cowork's privacy filter (signed tokens look like sensitive query data). Don't try to fetch them programmatically — ask the user to save the images locally to `~/PicturesForClaude/` and tell you when they're ready.

## Files in this skill

- `SKILL.md` — this file
- `assets/template.html` — the blog post template with placeholders
- `scripts/make_card_composite.py` — creates a side-by-side card image from two source images
- `references/facebook-extraction.md` — how to pull post text from a Facebook iframe embed or permalink
- `evals/evals.json` — sample test prompts (for iteration if needed)
