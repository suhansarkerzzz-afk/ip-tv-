# Architecture Notes — IPTV Channel Extractor Pro

## 1. Current architecture at a glance

The current prototype is intentionally small and is implemented in one file, `main.py`.

```text
User
 |
 v
Tkinter / ttk GUI (App)
 |                 |
 | load URL        | search / select / export
 v                 v
Requests worker    In-memory channel dictionaries
 |                 |
 v                 +--> Treeview display
M3U text           +--> CSV / JSON export
 |
 v
M3U parser
 |
 v
Deduplication
 |
 v
Queue message --> Tkinter main thread --> update table and counters

Check action:
channel list --> sequential range GET worker --> status updates --> queue --> GUI refresh
```

## 2. Main class and responsibilities

### `App`

The `App` class currently owns nearly all application responsibilities:

- Window setup and theme styling: `__init__`, `build_style`.
- Widget creation: `build_ui`.
- Theme/help dialogs: `toggle_theme`, `help`.
- Reset: `clear_all`.
- EXTINF attribute extraction and M3U parsing: `parse_attr`, `parse_m3u`.
- Online playlist loading: `load`, `_load_worker`.
- Search and table rendering: `apply_filter`, `refresh_table`, `update_stats`.
- Selected row operations: `selected_channel`, `copy_selected`, `open_selected`.
- URL checking: `check_all`, `stop_checks`, `_check_worker`.
- Export: `export_json`, `export_csv`.
- Worker-to-GUI message processing: `process_queue`.

This is simple to understand but creates tight coupling. Future refactoring should split parsing, network access, data models, and UI into separate modules without changing user-visible behavior unexpectedly.

## 3. Current data flow

### Playlist load

1. User enters a URL and clicks LOAD PLAYLIST.
2. `load()` checks whether Requests is available.
3. A daemon thread runs `_load_worker(url)`.
4. The worker downloads the response with a 90-second timeout and a custom User-Agent.
5. `parse_m3u(response.text)` extracts entries and removes duplicates.
6. The worker posts a `("loaded", channels, response_size)` tuple to `msgq`.
7. `process_queue()`, running on the Tkinter event loop, receives the message.
8. The app replaces `self.channels`, applies the current search, and refreshes the Treeview.

### Parsing rules in current code

- An entry begins when a line starts with `#EXTINF` (case-insensitive).
- The display name is the text after the first comma, or `Unknown` if no comma exists.
- The parser reads double-quoted `group-title`, `tvg-country`, `tvg-language`, `tvg-logo`, and `tvg-id` attributes.
- The next non-comment line beginning with http://, https://, rtmp://, or rtsp:// becomes the entry URL.
- Deduplication key is `(name.casefold(), url.strip())`.

### Search

Search is in-memory and case-insensitive. It checks name, group, country, language, and URL. It does not currently search logo or ID. The Treeview is rebuilt when the search changes.

### URL check

1. User clicks CHECK ALL.
2. A daemon worker iterates through all channels sequentially.
3. For each URL it sends Requests GET with `Range: bytes=0-1023`, timeout 8 seconds, and redirects enabled.
4. Status becomes Working for 200, 206, 301, 302, 307, or 308; other responses and exceptions become Dead.
5. Progress tuples are posted to `msgq`; a final checked tuple is posted when the loop ends or is stopped.
6. The GUI updates progress, table, and counters.

**Caution:** The current worker mutates channel dictionaries directly. A safer future design is for workers to emit immutable result messages such as `("check_result", channel_id, status, http_status, elapsed_ms, error)`, and let the GUI thread apply those results.

## 4. UI widgets and commands

| UI control | Handler | Effect |
|---|---|---|
| Playlist URL field | `self.url` | Holds source URL |
| LOAD PLAYLIST | `load` | Starts download/parse worker |
| CLEAR | `clear_all` | Clears in-memory data and rows |
| Search field | `apply_filter` via trace | Filters visible rows |
| Clear Search | sets search to empty | Restores all rows |
| COPY SELECTED URL | `copy_selected` | Copies first selected URL |
| OPEN STREAM | `open_selected` | Opens first selected URL externally |
| CHECK ALL | `check_all` | Starts sequential URL checks |
| STOP | `stop_checks` | Requests stop between URLs |
| EXPORT CSV | `export_csv` | Writes all channel dictionaries |
| EXPORT JSON | `export_json` | Writes all channel dictionaries |
| Theme | `toggle_theme` | Currently flips a flag and shows dialog |
| Help | `help` | Displays usage/limitations dialog |

## 5. Dependencies

Runtime:
- Python standard library: csv, json, re, threading, time, queue, webbrowser, pathlib, tkinter, urllib.
- Third-party: Requests, constrained by `requirements.txt` to major version 2.

Build:
- PyInstaller, installed by `build_exe.bat` or GitHub Actions.
- GitHub Actions uses checkout and setup-python actions and uploads the built EXE artifact.

Note: `time` and `urlparse` are currently imported but unused. Remove unused imports during a cleanup change only when appropriate.

## 6. Suggested future module layout

Do not perform a large rewrite just to create this structure. Introduce modules incrementally when there are tests to protect behavior.

```text
src/
  iptv_extractor/
    __init__.py
    app.py              # Tkinter application and composition
    models.py           # Channel record / status types
    m3u_parser.py       # Pure parsing functions
    playlist_client.py  # Download and local-file loading
    stream_checker.py  # HTTP reachability checks
    exporters.py        # CSV and JSON serialization
    settings.py         # Local preferences
tests/
  fixtures/
    sample_playlist.m3u
  test_m3u_parser.py
  test_exporters.py
```

## 7. Stable boundaries to preserve

- Keep parser functions independent from Tkinter so they can be tested without opening a window.
- Keep network operations out of the GUI event loop.
- Only the Tkinter main thread should touch widgets.
- Treat channel data as structured records, not Treeview row strings.
- Do not equate an HTTP response with successful playback.
- Keep secrets and private playlist URLs out of logs and commits.
