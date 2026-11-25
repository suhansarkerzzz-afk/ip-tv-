# Product Requirements — IPTV Channel Extractor Pro

This document separates the **current source-code baseline** from the **requested product direction**. A requirement listed here is not implemented unless the Current Status column says Implemented and the implementation has been verified.

## 1. Product direction

Build a dependable Windows IPTV playlist manager/extractor with a responsive interface, clear diagnostics, and reliable playback options. Preserve existing working behavior and improve incrementally.

## 2. User-requested product requirements

| ID | Requirement | Requested behavior | Current status |
|---|---|---|---|
| PR-01 | Playlist input | Load online M3U/M3U8 playlist URLs | Implemented (basic) |
| PR-02 | Local playlist input | Open local M3U/M3U8 files | Not implemented |
| PR-03 | Metadata extraction | Extract channel name, group, country, language, logo, TVG ID, stream URL | Implemented (basic parser) |
| PR-04 | Built-in playback | Play a selected channel inside the application | Not implemented |
| PR-05 | External playback | Offer VLC/system player option | Only opens URL through OS handler; no dedicated VLC selector |
| PR-06 | Buffering | Provide configurable 5–10 second initial buffer/preload where supported by the chosen playback engine | Not implemented |
| PR-07 | Favorites | Save and revisit favorite channels | Not implemented |
| PR-08 | Diagnostics | Show latency, HTTP status, playback status, and error details | Only basic Working/Dead/Unknown HTTP check |
| PR-09 | Search/filter | Search by country, language, and group as well as channel name/URL | Search covers name, group, country, language, URL; dedicated filters not implemented |
| PR-10 | Appearance | Dark and light themes | Dark styling exists; theme toggle is not a functional theme switch |
| PR-11 | UI scaling | Adjustable interface scale from 80% to 150% | Not implemented |
| PR-12 | Player zoom | Adjustable player zoom when an embedded player exists | Not implemented; no embedded player |
| PR-13 | Large playlists | Remain responsive and avoid freezing with large playlists | Network load is in a worker thread; large-list performance has not been benchmarked or optimized |
| PR-14 | Invalid URLs | Validate inputs and show useful errors | Basic Requests errors only; validation needs improvement |
| PR-15 | Remove trial-like UI | Do not present fake trial or placeholder restrictions | No trial system is present in current source |

## 3. Playback design decision required before implementation

A built-in player requires choosing and documenting a playback engine. Candidate approaches include:
- VLC/libVLC integration, subject to packaging, runtime availability, and licensing review.
- An alternative supported media backend if VLC integration is unsuitable.
- External player launch as a fallback.

Do not assume a player dependency is installed on every target computer. Define:
- Supported protocols and codecs.
- Whether the player is bundled or separately installed.
- How buffering is configured and what the 5–10 second setting means.
- How playback errors differ from URL reachability errors.
- How to package and test the selected backend.

A buffer duration is a target configuration, not a guarantee against buffering: network speed, stream encoding, provider behavior, and player capabilities affect playback.

## 4. Diagnostics vocabulary

Keep these states separate:

- **Not checked:** no reachability test has been run.
- **Reachable:** endpoint returned a response accepted by the checker.
- **Unreachable:** endpoint could not be contacted or returned a disqualifying response.
- **Playback playing:** the media engine confirms active playback.
- **Playback buffering:** the media engine reports buffering.
- **Playback error:** the media engine reports a playback failure, with an error detail where available.

Never label a stream "Playing" based only on an HTTP response. The current Working/Dead/Unknown values are legacy simplified reachability states.

## 5. Acceptance criteria for future work

- Existing playlist parsing and export behavior must have regression tests before refactoring.
- Large playlists must not block the Tkinter event loop.
- Stop/cancel must have documented behavior and bounded response time.
- No worker thread may directly create, update, or destroy Tkinter widgets.
- A playback state must come from the player engine, not the HTTP checker.
- Theme and scaling settings must visibly affect the entire interface and persist after restart if persistence is added.
- Exports must clearly specify whether they include all, filtered, or selected channels.
- Errors must be actionable without exposing private playlist credentials in logs.
- Build artifacts must be tested on a clean Windows environment before release claims.

## 6. Scope boundaries

Unless the product owner explicitly changes scope, do not add:
- DRM or subscription bypass.
- Credential harvesting or unauthorized playlist access.
- Geographic restriction evasion.
- Cloud accounts, remote admin panels, or subscription billing as prerequisites for the desktop extractor.
- Automatic upload of users' private playlist URLs or channel lists.

