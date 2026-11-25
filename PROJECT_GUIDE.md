# Project Guide — IPTV Channel Extractor Pro

## 1. Project identity

- **Product name:** IPTV Channel Extractor Pro
- **Repository:** https://github.com/suhansarkerzzz-afk/ip-tv-
- **Current target:** Windows desktop
- **Language/runtime:** Python 3.11+ recommended
- **GUI:** Tkinter + ttk (ships with standard Python distributions)
- **HTTP client:** Requests
- **Current entry point:** `main.py`
- **Current maturity:** Early prototype; source is present, but build, packaging, playback, and full regression testing are not yet verified.

## 2. Product purpose

The application is intended to help a user inspect an M3U/M3U8 playlist and organize the channel metadata and stream URLs it contains. The current implementation is an extractor and URL reachability checker, not a full IPTV player or subscription-management platform.

Primary user flow:

1. Paste an authorized online playlist URL.
2. Load and parse its M3U text.
3. Inspect channel metadata and stream URL rows.
4. Search the loaded list.
5. Optionally run a basic HTTP reachability check.
6. Copy/open a selected URL or export records to JSON/CSV.

## 3. Current implemented behavior

| Area | Current behavior |
|---|---|
| Online playlist input | URL field; default is the public iptv-org index playlist |
| Download | Uses Requests in a background thread; timeout is 90 seconds |
| Parsing | Reads `#EXTINF` metadata followed by a supported stream URL |
| Metadata | Channel name, group-title, tvg-country, tvg-language, tvg-logo, tvg-id |
| URL schemes | Parser currently accepts http, https, rtmp, and rtsp |
| Deduplication | Duplicate key is case-folded channel name + URL |
| Search | Searches name, group, country, language, and URL |
| Selection | Multi-select Treeview is enabled; copy/open currently act on the first selected row |
| Copy | Copies selected stream URL to clipboard |
| Open | Sends selected URL to the system's registered URL handler |
| Check | Sequential HTTP GET with Range bytes=0-1023, timeout 8 seconds |
| Status | Basic Working / Dead / Unknown classification |
| Counters | Total, Working, Dead, Unknown |
| Export | JSON and CSV |
| Clear | Clears current in-memory list and table |
| GUI | Tkinter/ttk dark-styled initial layout |

## 4. Not implemented yet (do not describe these as existing features)

- Built-in video playback or VLC integration.
- Local M3U/M3U8 file import.
- Playlist library / multiple saved playlists.
- User accounts, login, cloud sync, or admin server.
- Fully functional light/dark theme switching and persistent theme settings.
- Configurable UI scaling.
- Country, language, and group dropdown filters.
- Sorting controls, favorites, and bulk row actions.
- Concurrent/batched URL checking with safe limits.
- Detailed latency, response headers, error categories, and check timestamps.
- Robust support for all M3U dialects and unusual attribute quoting.
- Automated unit/integration tests.
- Verified packaged Windows executable or signed installer.

These are potential roadmap items, not promises about the current release.

## 5. Installation and operation

### Requirements

- Windows 10/11 recommended.
- Python 3.11 or newer.
- Python launcher command `py -3` available in PATH.
- Internet access for online playlist loading.
- `requests>=2.31,<3` (installed by `install.bat`).

### Run from source

```bat
install.bat
start.bat
```

Or manually:

```bat
py -3 -m pip install -r requirements.txt
py -3 main.py
```

### Build locally

```bat
build_exe.bat
```

The batch file invokes PyInstaller in one-file, windowed mode. Expected output is:

```
dist\IPTV_Channel_Extractor_Pro.exe
```

This output path is expected from the build command; it does not mean the EXE has already been built or checked in.

## 6. Repository file map

| Path | Purpose |
|---|---|
| `main.py` | Entire current Tkinter application: UI, playlist fetch, parsing, filtering, checking, and export |
| `requirements.txt` | Python runtime dependencies |
| `install.bat` | Installs Python dependencies |
| `start.bat` | Starts the application from source |
| `build_exe.bat` | Builds a Windows EXE with PyInstaller |
| `.github/workflows/build-windows.yml` | GitHub Actions Windows build and artifact upload; version tags can publish a release |
| `README.md` | Short project introduction and navigation |
| `PROJECT_GUIDE.md` | This detailed project guide |
| `ARCHITECTURE.md` | Internal code and data-flow notes |
| `AI_HANDOFF.md` | Handoff prompt for another developer or AI |
| `PROMPT.md` | Improvement roadmap |

## 7. Current channel record format

Each parsed channel is represented as a Python dictionary:

| Key | Type | Meaning |
|---|---|---|
| `name` | string | Display name from the EXTINF line |
| `group` | string | `group-title` attribute |
| `country` | string | `tvg-country` attribute |
| `language` | string | `tvg-language` attribute |
| `logo` | string | `tvg-logo` attribute |
| `id` | string | `tvg-id` attribute |
| `status` | string | `Unknown`, `Working`, or `Dead` |
| `url` | string | Stream URL line following EXTINF |

Example:

```json
{
  "name": "Example Channel",
  "group": "News",
  "country": "BD",
  "language": "Bangla",
  "logo": "https://example.invalid/logo.png",
  "id": "example.bd",
  "status": "Unknown",
  "url": "https://example.invalid/live/index.m3u8"
}
```

The example is illustrative only; it is not a real channel or tested URL.

## 8. Important technical limitations and known risks

1. **Parser limitations:** The parser uses a simple regular expression for double-quoted attributes. It may fail on escaped quotes, single-quoted attributes, unusual spacing, EXTINF continuation cases, or metadata lines that do not match the expected layout.
2. **Download memory use:** The online playlist is downloaded into memory as a complete response before parsing. Very large playlists can consume significant RAM.
3. **Check accuracy:** The checker makes a range GET request and treats selected HTTP status codes as Working. This only indicates that the endpoint responded in a way the checker accepts. It does not validate a playable video stream, codec, DRM, authentication, or sustained playback.
4. **False Dead results:** Some providers reject automated clients, range requests, or requests without special headers. Such streams may be marked Dead even if a supported player can access them.
5. **Sequential checks:** One URL is checked at a time, so very large lists can take a long time.
6. **Thread safety:** The worker thread currently updates channel dictionary status values while the GUI thread reads them. Refactor toward immutable result messages and main-thread state updates before adding concurrent checking.
7. **Stop behavior:** Stop is checked between requests; it cannot instantly abort the request currently in progress.
8. **Theme toggle:** The current button flips a Boolean and shows a message, but does not apply a complete light theme.
9. **No built-in player:** Open Stream delegates to the operating system; behavior depends on installed applications and file associations.
10. **Export behavior:** Current exports write the complete channel collection, not only selected rows or the filtered view.

## 9. Recommended development priorities

### P0 — stabilize current code
- Add parser tests for valid, malformed, and mixed-format M3U fixtures.
- Separate parsing and network functions from the Tkinter UI.
- Prevent duplicate simultaneous load/check operations.
- Move all UI updates and channel-state mutation onto the Tkinter main thread via the queue.
- Improve exception messages and validate URL schemes before requests.
- Confirm stop and window-close behavior.

### P1 — practical usability
- Add local file import.
- Add robust EXTINF attribute parsing.
- Add sortable columns and group/country/language filters.
- Make exports reflect all / filtered / selected rows, with an explicit choice.
- Add a proper light theme and persist user settings.

### P2 — diagnostics
- Track HTTP status, elapsed time, error category, and last-check time.
- Distinguish reachable, unreachable, blocked/unsupported, and not checked.
- Add bounded concurrency only after safe cancellation and thread-safe result handling exist.

### P3 — optional player integration
- Decide whether the product should integrate with VLC/libVLC or continue to delegate playback externally.
- If adding a player, document its separate runtime dependencies and licensing.
- Keep playback success separate from URL reachability status.

## 10. Test and release policy

- Do not say "tested", "working", "build passed", or "playback verified" without an actual run and recorded result.
- Before a release, run parser tests, launch the GUI on Windows, test a small authorized playlist, test exports, test cancellation, and build the EXE.
- Record Python version, Windows version, commit SHA, test outcome, EXE size, and SHA-256.
- GitHub Actions artifact availability should be verified in the Actions run. A workflow file existing in the repository is not proof that a workflow has succeeded.

## 11. Privacy and responsible use

- Do not add playlist credentials, private URLs, tokens, or personal playlist data to source control, screenshots, test fixtures, logs, or public issues.
- Use environment variables or local-only configuration for secrets if a future feature requires them.
- Only inspect playlists and stream endpoints the user is authorized to access.
- Do not implement DRM circumvention, subscription bypass, credential theft, or geo-restriction evasion.

## 12. Change management

- Inspect the current source and recent commits before editing.
- Make small, focused commits with descriptive messages.
- Preserve working behavior unless the change explicitly replaces it.
- Update this guide and the architecture notes whenever behavior, dependencies, or file layout changes.
- Add tests for new parser, data, and network behavior.
- Keep the README's feature claims aligned with verified implementation.
