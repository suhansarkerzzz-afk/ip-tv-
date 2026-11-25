# Contributing / Working Agreement

## Before you edit
1. Pull the latest `main` branch.
2. Read `README.md`, `PROJECT_GUIDE.md`, `PRODUCT_REQUIREMENTS.md`, and `ARCHITECTURE.md`.
3. Inspect current code and workflow; do not rely only on an old description.
4. Identify the smallest safe change and list the files it will affect.

## Code rules
- Preserve working behavior; avoid unnecessary rewrites.
- Keep parsing and data transformations testable without starting Tkinter.
- Do not block the Tkinter main event loop with network calls or large file operations.
- Only the main thread may update Tkinter widgets.
- Use explicit timeouts for network requests.
- Bound concurrency; never launch one thread per channel.
- Keep errors understandable and avoid logging playlist secrets.
- Do not mark a channel as playing based on HTTP status alone.
- Keep dependencies minimal and document any new dependency and its packaging impact.

## Tests
- Use local M3U fixtures and mocked HTTP responses.
- Do not make automated tests depend on public IPTV services or real private streams.
- Record exactly which tests ran and their result.
- If Windows or player-engine testing was not available, say so.

## Commits
Use short, descriptive commit messages, for example:
- `Add M3U parser unit tests`
- `Fix cancellation handling in stream checker`
- `Add local playlist file import`

Do not bundle unrelated changes into one commit.

## Pull request / handoff summary
Include:
- Purpose and behavior change.
- Files changed.
- Test commands and actual results.
- Build status and environment.
- Known limitations and follow-up work.
