# AI / Developer Handoff — IPTV Channel Extractor Pro

Copy this file or the prompt below when asking another AI assistant or developer to continue work on this repository.

## Repository

https://github.com/suhansarkerzzz-afk/ip-tv-

## Product summary

IPTV Channel Extractor Pro is a Windows desktop Python/Tkinter prototype. It currently loads an online M3U/M3U8 playlist, parses channel metadata and stream URLs, deduplicates entries, supports search, copies/opens a selected URL, runs a basic sequential HTTP range-request check, and exports JSON/CSV.

It is currently an extractor and reachability checker. It is **not** a built-in IPTV player.

## Mandatory instructions for the next developer / AI

1. Inspect the repository's current branch, latest commits, all files, and GitHub Actions workflow before making changes.
2. Read `README.md`, `PROJECT_GUIDE.md`, `ARCHITECTURE.md`, and `PROMPT.md`.
3. Treat the code in the repository as the source of truth. These documents describe the current implementation at the time they were written; update them when implementation changes.
4. Do not claim that a feature exists, a test passed, an EXE was built, or playback works unless you actually verified it.
5. Preserve working code and make incremental, focused changes. Do not rewrite the whole app without a clear technical reason.
6. Before changing behavior, explain the problem, the planned change, and files affected.
7. Add automated tests for pure parsing, validation, and export logic. Avoid requiring real IPTV services in tests; use local fixtures and mocked HTTP responses.
8. Keep network requests out of the Tkinter UI thread. Keep all widget updates on the Tkinter main thread.
9. Avoid unbounded parallel requests. Any future concurrency must have a safe limit, cancellation, timeouts, and deterministic result handling.
10. Do not put playlist credentials, private playlist URLs, tokens, or user data in commits, tests, logs, or screenshots.
11. Respect playlist ownership and provider terms. Do not implement DRM, subscription, login, or geographic restriction bypass.
12. At the end, report changed files, commit IDs, tests actually run, build results, known issues, and exact next steps.

## Current verified feature baseline (from source inspection)

- Tkinter/ttk desktop window.
- Online URL load using Requests.
- Basic EXTINF parser with double-quoted attributes.
- Channel fields: name, group, country, language, logo, ID, status, URL.
- Deduplication by case-folded name and URL.
- Search across name, group, country, language, and URL.
- Copy selected URL and open selected URL externally.
- Sequential HTTP range GET checker with basic Working/Dead/Unknown labels.
- CSV and JSON export.
- Windows setup/start/build batch files.
- GitHub Actions workflow to build and upload an EXE artifact; workflow success still needs verification.

## Known issues to address carefully

- Theme toggle does not apply a complete alternate theme.
- Parser is intentionally simple and needs fixture-based tests and robustness.
- URL check status is not playback validation and can produce false Dead results.
- Checker is sequential and cannot immediately abort the current in-flight request.
- Worker thread currently mutates channel dictionaries; move result application to the GUI thread.
- Exports currently include all channels, not only filtered or selected rows.
- Local file import and a built-in player are absent.
- The current source has not been confirmed through a full Windows build or end-to-end playback test.

## Suggested first task

Start with a no-feature-loss stabilization pass:

1. Add `tests/fixtures/sample_playlist.m3u`.
2. Extract parser code into a pure function/module without changing output schema.
3. Add tests for valid entries, missing optional metadata, duplicate entries, comments, malformed EXTINF lines, and supported URL schemes.
4. Add safe URL validation and clearer error categories.
5. Refactor checker workers to return results through the queue instead of mutating shared channel records.
6. Update documentation to match the final behavior.

Do not add a video player, accounts, cloud backend, or large new feature until the existing parser, UI lifecycle, and checker are stable.

---

## Copy-ready task prompt

You are a senior Python desktop application engineer and QA reviewer. Continue the project at https://github.com/suhansarkerzzz-afk/ip-tv-.

First inspect the repository and read README.md, PROJECT_GUIDE.md, ARCHITECTURE.md, AI_HANDOFF.md, and PROMPT.md. Verify the current source rather than trusting claims in old notes. Preserve existing functionality and make small commits. Do not rewrite destructively. Do not claim tests/build/playback succeeded unless actually executed. Keep Tkinter widget access on the main thread; use worker threads only for network/file work and return results through a queue. Add tests with local fixtures and mocked HTTP responses. Clearly separate HTTP reachability from real stream playback. Never commit playlist secrets or private URLs. Respect provider terms and do not bypass DRM, subscriptions, authentication, or geographic restrictions.

Before implementation, provide a concise audit and plan. After implementation, list changed files, commits, tests actually run, build status, remaining limitations, and exact next steps.
