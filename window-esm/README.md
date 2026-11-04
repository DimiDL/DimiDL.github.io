# Browser window ESM migration tracker

Tracks porting the legacy `.js` browser-window category consumers in
`browser/components/BrowserComponents.manifest` to ES modules
(meta bug 2045664).

`index.html` is a static page. It reads `data.json` and, on every load, fetches
the status, assignee and resolution date of every listed bug from the Bugzilla
REST API. There is no build step; host the directory on GitHub Pages or any
static server (`python3 -m http.server` works locally).

## Adding a bug

Set the item's `bug` field in `data.json` to the bug number and push. Any
RESOLVED or VERIFIED bug counts as done; the burndown is built from each bug's
`cf_last_resolved` date.

## Refreshing line counts

    ./update-lines.py /path/to/gecko --rev origin/bookmarks/central

Items with an `object` count only that object's top-level definition in the
file; other items count the whole file.
