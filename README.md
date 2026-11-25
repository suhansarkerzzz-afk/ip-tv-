# IPTV Channel Extractor Pro

Windows desktop tool for loading M3U playlists, extracting channel metadata, checking stream URL reachability, searching channels, and exporting results.

## Features
- Load an online M3U playlist
- Extract channel name, group, country, language, logo, TVG ID, and stream URL
- Search and deduplicate channels
- Check HTTP reachability (this does not guarantee playback)
- Export results to CSV or JSON

## Run on Windows
1. Install Python 3.11 or newer.
2. Run `install.bat`.
3. Run `start.bat`.

To build a Windows executable, run `build_exe.bat` or use the GitHub Actions workflow in `.github/workflows/build-windows.yml`.

See `PROMPT.md` for the planned improvement roadmap.
