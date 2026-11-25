# IPTV Channel Extractor Pro — Improvement Roadmap

Preserve the existing working application and improve it incrementally. Do not rewrite the project unnecessarily.

## Reliability and playlist handling
- Add local M3U/M3U8 file import alongside online playlist URLs.
- Improve parsing for quoted attributes, escaped characters, missing metadata, and varied playlist formats.
- Handle invalid URLs, timeouts, retries, redirects, and provider-specific HTTP errors clearly.
- Use bounded concurrency for stream checks and support cancellation without freezing the UI.

## User interface
- Add consistent dark and light themes.
- Add configurable UI scaling and player-independent zoom controls where relevant.
- Improve large-playlist responsiveness with background work and clear progress feedback.
- Add sortable columns, country/language/group filters, and useful context-menu actions.

## Diagnostics and exports
- Distinguish reachable, unreachable, and unknown results.
- Show latency, HTTP status, error details, and check timestamps.
- Make it clear that HTTP reachability is not the same as successful video playback.
- Support CSV and JSON export, including selected rows and filtered results.

## Quality assurance and release
- Add parser and URL-checking unit tests using safe test fixtures.
- Verify cancellation, large playlists, malformed input, and network failures.
- Keep GitHub Actions building the Windows executable and publishing a versioned release on tags.
- Record the executable size and SHA-256 checksum for each release.

Do not implement DRM circumvention, paywall bypass, or geographic-access circumvention. Respect playlist ownership and provider terms.
