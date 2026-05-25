# Extracting Post Content from Facebook

When the user pastes a Facebook iframe embed code like:

```html
<iframe src="https://www.facebook.com/plugins/post.php?href=https%3A%2F%2Fwww.facebook.com%2FEmpowerDreams.SocialMedia%2Fposts%2Fpfbid0..." ...></iframe>
```

The `href` query param inside the iframe `src` is the post permalink (URL-decode if needed).

## Two URLs, two purposes

| URL form | Best for |
|---|---|
| `https://www.facebook.com/plugins/post.php?href=<URL-encoded permalink>&show_text=true&width=500` | Quick verification — clean rendering with date, author, first ~200 chars of text. Truncates at "...See more". |
| `https://www.facebook.com/<page>/posts/<pfbid...>` | Full text extraction via DOM. Required if the post has more than ~200 chars. |

## Steps

1. Navigate Claude in Chrome to the plugin URL first. This confirms which post it is and shows the date (e.g., "about 3 months ago" → calculate the approximate date).

2. Confirm with the user which date the post corresponds to (Facebook's relative date "3 months ago" isn't exact).

3. Navigate to the regular permalink to get the full text.

4. Click any "See more" buttons:
   ```javascript
   const seeMores = Array.from(document.querySelectorAll('div[role="button"], span'))
     .filter(el => {
       const t = (el.textContent || '').trim();
       return t === 'See more' || t === '… See more' || t === 'See More';
     });
   for (const c of seeMores) {
     try { c.click(); } catch(e) {}
   }
   ({clicked: seeMores.length})
   ```

5. Extract the post text by finding the largest `[dir="auto"]` block:
   ```javascript
   (async () => {
     await new Promise(r => setTimeout(r, 1500));  // let "See more" expand
     const candidates = [];
     document.querySelectorAll('div[dir="auto"], span[dir="auto"]').forEach(el => {
       const t = (el.innerText || '').trim();
       if (t.length > 80 && t.length < 5000 && !t.includes('Most relevant')) {
         candidates.push({len: t.length, text: t});
       }
     });
     candidates.sort((a, b) => b.len - a.len);
     return candidates.slice(0, 3);  // top 3 — usually the longest is the post body
   })()
   ```

## Known limitations

**Images cannot be downloaded programmatically.** Three layers block it:
- Cowork's URL filter strips Facebook CDN URLs (signed `?_nc_cat=...&oh=...` query strings look like sensitive tokens)
- CORS blocks `fetch()` for image bytes
- Tainted-canvas restrictions block `toDataURL()` extraction

The user must save images manually from Facebook (right-click → Save image as) into a folder Claude has access to.

**Facebook scrolling is unreliable.** The admin page's infinite-scroll feed times out the CDP `Runtime.evaluate` after ~45 seconds. Don't try to scroll back months. If the user wants a specific old post, ask for the iframe embed or permalink directly.

**Multiple Claude conversations conflict.** If the user has a Claude in Chrome sidebar conversation open AND Cowork is calling `Claude_in_Chrome` tools, the extension can serve only one at a time. Ask the user to close the sidebar before driving Chrome from Cowork.

**Chrome extension permissions** must be set to "On all sites" in `chrome://extensions/` → Claude for Chrome → Details → Site access. If reads come back as "Permission denied by user" or "permission_required: <domain>", that's the setting to fix.

**The "Claude started debugging this browser" banner** must NOT be cancelled. Clicking Cancel terminates the debugger session and returns "Permission denied by user" for all subsequent reads. Leave the banner alone.
