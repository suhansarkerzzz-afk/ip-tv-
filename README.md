# IPTV Channel Extractor Pro

A Windows desktop utility for importing M3U/M3U8 playlists, extracting channel metadata and stream URLs, searching entries, performing basic HTTP reachability checks, and exporting playlist data.

> **Project status:** Early working-source prototype. The source and build workflow are in this repository, but a successful Windows EXE build and end-to-end playback test have not yet been verified. Read [PROJECT_GUIDE.md](PROJECT_GUIDE.md) before changing the code.

## Quick start (Windows)

1. Install Python 3.11 or newer and make sure the `py` launcher is available.
2. Download/clone this repository.
3. Run `install.bat`.
4. Run `start.bat`.

To build an executable locally, run `build_exe.bat`. To build in GitHub, open **Actions → Build Windows EXE → Run workflow**. The workflow artifact is not the same as a committed EXE file.

## Current capabilities

- Load an online M3U/M3U8 playlist from a URL.
- Parse channel name, group, country, language, logo, TVG ID, and stream URL.
- Remove duplicate entries by channel name + URL.
- Search the loaded channel list.
- Copy a selected stream URL or open it using the system's registered handler.
- Run a sequential HTTP range-request check and show Working/Dead/Unknown counts.
- Export channel records as JSON or CSV.

## Documentation for developers and other AI tools

- [PROJECT_GUIDE.md](PROJECT_GUIDE.md) — full product brief, setup, file map, data model, current behavior, limitations, and development workflow.
- [ARCHITECTURE.md](ARCHITECTURE.md) — code structure, data flow, threading model, and technical notes.
- [AI_HANDOFF.md](AI_HANDOFF.md) — copy-ready instructions for another developer or AI assistant to continue the project safely.
- [PROMPT.md](PROMPT.md) — prioritized improvement roadmap.

## Important limitations

- An HTTP response or range request does **not** prove that a channel will play successfully.
- The current app does not contain a built-in video player.
- Local playlist-file import, reliable dark/light theme switching, advanced filters, concurrent checking, and detailed diagnostics are not implemented yet.
- The current theme button only toggles an internal flag and displays a message; it does not fully restyle the interface.
- The current checker is sequential and its status classification is basic.
- Do not claim the app, EXE, or playback has passed testing unless a test has actually been run and recorded.

## Responsible use

Use playlists and stream URLs that you own or are authorized to access. This project is not intended to bypass DRM, subscriptions, authentication, or geographic restrictions.
