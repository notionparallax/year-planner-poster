# year-planner-poster

A single-page tool that renders your Google Calendar (and/or Outlook) as a rolling 12-month poster, designed for printing at A0 landscape.

Each month is a row. Each day is a column, aligned on day-of-week. Timed events are displayed as proportionally-sized blocks within a 7 am – 8 pm time window. All-day and multi-day events appear as spanning bars below. Free-status events (`TRANSP:TRANSPARENT`) are shown as outlines only. Events that appear in both calendars are merged into a single split-colour block.

## Usage

### 1. Start the proxy

The iCal feed URLs don't send CORS headers, so a tiny local proxy is needed.

```
python proxy.py
```

This runs at `http://localhost:8765`. Leave it running in the background.

### 2. Serve the page

```
python -m http.server 8080
```

Open `http://localhost:8080` in your browser.

### 3. Get your iCal URL(s)

**Google Calendar:**  
Settings → click a calendar → scroll to *Secret address in iCal format* → copy the `.ics` URL.

**Outlook / Microsoft 365:**  
`outlook.office.com` → Settings → Calendar → Shared calendars → *Publish a calendar* → copy the ICS link.

### 4. Load and print

- Paste each iCal URL into the URL fields, pick a colour per calendar, click **Load calendars**.
- URLs are saved to `localStorage` so they persist across reloads.
- Once loaded, use **Re-render** to instantly re-apply CSS changes without re-fetching.
- Print: browser print dialog → set paper size to A0 landscape → *Save as PDF* for a plotter.

## CSS tweaking

All visual variables are at the top of `index.html`:

| Variable | Default | Effect |
|---|---|---|
| `--label-w` | `50mm` | Width of the month name column |
| `--header-h` | `12mm` | Height of the weekday header row |
| `--month-h` | `67mm` | Minimum height per month row |
| `--daynum-h` | `9mm` | Height of the day-number row within each month |
| `--event-h` | `4.2mm` | Row height for all-day event chips |
| `--weekend-bg` | `#f2f2f2` | Weekend column background tint |

## Running without the proxy (GitHub Pages)

The local proxy is a convenience tool. To host this on GitHub Pages with no server, deploy a **Cloudflare Worker** as a personal CORS proxy:

1. Create a free Cloudflare account and paste this one-file worker:

```js
export default {
  async fetch(request) {
    const url = new URL(request.url).searchParams.get('url');
    if (!url) return new Response('Missing url', { status: 400 });
    const resp = await fetch(url);
    const body = await resp.text();
    return new Response(body, {
      headers: {
        'Content-Type': 'text/calendar',
        'Access-Control-Allow-Origin': '*',
      },
    });
  },
};
```

2. Update the `PROXY` constant at the top of the `<script>` block in `index.html` to your worker URL.

The Cloudflare free tier is 100k requests/day. Because the worker URL is private to you, your secret calendar URLs are never exposed to any public third-party service.

## New repo

This project is a complete rewrite of the layout and data pipeline from [visual-planner.github.io](https://github.com/visual-planner/visual-planner.github.io), which it was originally forked from. If you're forking this for your own use, consider creating a fresh repo rather than keeping the fork relationship.

## Privacy

Your calendar data is fetched directly from Google/Microsoft into your browser via the proxy. It is never stored, transmitted to, or processed by any third party. The iCal feed URLs act as a secret key — treat them like a password and regenerate them if accidentally shared.
