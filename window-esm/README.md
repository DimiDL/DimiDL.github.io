# Browser window ESM migration tracker

Tracks porting the legacy `.js` browser-window category consumers in
`browser/components/BrowserComponents.manifest` to ES modules
(meta bug 2088886, part of meta bug 2045664).

`index.html` is a static page. It reads `data.json` and, on every load, fetches
the status, assignee and resolution date of every listed bug from the Bugzilla
REST API. There is no build step; host the directory on GitHub Pages or any
static server (`python3 -m http.server` works locally).

## Adding a bug

Set the item's `bug` field in `data.json` to the bug number and push. Any
RESOLVED or VERIFIED bug counts as done; the burndown is built from each bug's
`cf_last_resolved` date.

## Review groups

Each item's `reviewers` lists the Phabricator groups likely to review its
conversion, most specific first; a trailing `!` marks a group Herald adds as
blocking. They come from `./mach file-info reviewers <path>` (Herald rules and
`mots.yaml`), plus the group that reviewed most of the file's recent history on
mozilla-central where one clearly dominates. Every conversion also edits
`eslint-file-globals.config.mjs`, so Herald adds `#frontend-codestyle-reviewers`
as blocking on top of these.

## Grouping

The table is grouped by the `gBrowserInit` function each consumer is invoked
from, in the order listed in `groups` (the order the functions were ported to
category-manager invocation). An item's `functions` lists every function that
calls it; the item is counted under the first one, and repeated in grey under
the rest.

## Refreshing line counts

    ./update-lines.py /path/to/gecko --rev origin/bookmarks/central

Items with an `object` count only that object's top-level definition in the
file; other items count the whole file.
