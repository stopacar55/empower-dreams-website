# Empower Dreams Website — Project Notes for Claude Code

## What this is
Public website for the Empower Dreams nonprofit, served from
https://empowerdreams.org. Static HTML/CSS/JS, no build step,
deployed via GitHub Pages directly from the `main` branch.

## Repo layout
- `index.html` — homepage
- `about.html`, `blog.html`, `donate.html` — top-level pages
- `blog/` — individual blog posts (one HTML file each)
- `team/` — team member pages
- `images/` — all image assets
- `styles.css` — shared sitewide styles
- `pages.css` — styles specific to non-homepage pages
- `main.js` — shared JavaScript (mobile menu, scroll reveals, etc.)
- `CNAME` — maps GitHub Pages to empowerdreams.org. Do not change without updating DNS.
- `DEPLOYMENT-INSTRUCTIONS.md` — how the site is deployed (reference only)

## Deployment
- Every merge to `main` on the upstream `Empower-Dreams/empower-dreams-website` repo triggers a GitHub Pages rebuild.
- Live updates appear at empowerdreams.org within ~1–2 minutes.
- There is no staging environment. Treat `main` as production.

## Workflow conventions
- **Never commit directly to `main`.** All changes go through a branch and a pull request.
- Branch prefixes: `pas/<description>` for Pas; the other collaborator uses his own prefix. Use lowercase, hyphen-separated descriptions.
- The other person reviews and merges PRs — two pairs of eyes before anything reaches production.
- Keep commits focused: one logical change per commit when practical.
- Commit messages: short imperative summary line (e.g. "Fix donate button alignment on mobile"), optional body for context.

## Local preview
Plain HTML, no build step. Any of these work:
- `open index.html` — quick view in default browser (no live reload).
- `python3 -m http.server 8000` then visit http://localhost:8000 — recommended; closer to how the live site serves files.

## Style guidelines
- Existing color and typography choices live in `styles.css`. Match them rather than introducing new ones.
- Images should be reasonably compressed before adding to `images/`.

## When using Claude Code on this repo
- Read this file first.
- Prefer minimal, reviewable diffs over sweeping rewrites.
- For copy or content changes, surface the proposed text in the chat before editing the file when the change is non-trivial.
- For visual or layout changes, mention what to test in the browser after the edit.
- Before any `git commit`, run `git status` and `git diff --staged` and wait for explicit confirmation.
- Never run `git push --force` or `--force-with-lease`.
- Never push to `main` directly. Work on a branch and open a PR.
