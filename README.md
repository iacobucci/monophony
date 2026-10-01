<p align="center">
  <img src="assets/icon.svg" width="128" height="128" alt="Monophony Icon">
</p>

<h1 align="center">Monophony</h1>

<p align="center">
  <b>A modern, ad-free YouTube Music client crafted with Python, GTK4, and Libadwaita for the Linux desktop.</b>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-0BSD-blue.svg" alt="License"></a>
  <a href="https://www.gnu.org"><img src="https://img.shields.io/badge/Platform-Linux-orange.svg" alt="Platform"></a>
  <a href="https://gitlab.gnome.org/GNOME/libadwaita"><img src="https://img.shields.io/badge/GTK4-Libadwaita-4a90d9.svg" alt="Libadwaita"></a>
</p>

---

## 🌟 Overview

**Monophony** is an open-source, ad-free music streaming application that brings the full catalog of YouTube Music directly to your Linux desktop. Built natively with **GTK4** and **Libadwaita**, Monophony integrates seamlessly with the GNOME ecosystem while offering progressive streaming, gapless radio generation, bidirectional YouTube account sync, offline downloads, and system-wide GNOME search.

---

## ✨ Key Features

### ⚡ Progressive Streaming & Gapless Playback
- **Instant Playback**: Progressive audio streaming starts playback immediately without waiting for entire media files to buffer.
- **Intelligent Prefetching**: Background prefetching proactively extracts streaming URIs and buffers upcoming songs, providing seamless, gapless transitions between tracks.
- **Multi-Level Audio Cache**: Cached streams and extracted URIs are retained for recent and upcoming tracks, allowing instant backward and forward seeking without re-fetching.
- **Priority-Driven Scheduling**: Foreground user actions (searching, pressing play) automatically preempt and pause background tasks (prefetching, sync), ensuring a silky-smooth, lag-free UI at all times.

---

### 📻 YouTube Radio & Endless Discovery
- **Endless Radio from Anything**: Launch a dynamic radio station instantly from any song, artist, or playlist.
- **Seamless Queue Infill**: As playback nears the end of the queue, Monophony fetches fresh recommendations in the background and populates the queue without interrupting audio.
- **Smart Loop Prevention**: Deduplicates tracks and prevents repeating recently played songs in continuous radio mode.

---

### 🔄 YouTube Music Account & Two-Way Sync
- **OAuth Authentication**: Sign in effortlessly using standard Google / YouTube Music TV/device authorization, or import your existing `oauth.json` credentials.
- **Bi-Directional Playlist Sync**: Changes made locally (creating playlists, adding/removing tracks, reordering) synchronize back to YouTube Music via TVHTML5 and YouTube Data API v3 integrations.
- **Liked Songs (LM) Integration**: Full two-way support for your YouTube Music "Liked Songs" library. Like and unlike tracks directly in the player to update your library across devices.
- **Favorite Playlists**: Pin and organize your favorite playlists front and center.
- **No Song Caps**: Robust WEB_REMIX scrapers bypass default 15-song limits to fetch complete, large playlists.

---

### 🔍 GNOME Shell Overview Search Provider
- **Native GNOME Search**: Search Monophony directly from the GNOME Shell overview by pressing the `Super` key and typing your query.
- **Rich Suggestions**: Displays instant interactive suggestions for songs, albums, and playlists right in the desktop overview.
- **One-Click Playback**:
  - Selecting a song begins playback immediately.
  - Selecting an album or playlist loads and starts the collection.
- **Headless D-Bus Daemon**: Runs via an independent background service (`monophony-search-provider`), activating the player on demand with minimal system overhead.

---

### 🎤 Integrated Lyrics Viewer
- **Instant Lyrics Access**: Open the dedicated lyrics viewer with a single click from the bottom player bar or the queue sidebar.
- **Synchronized & Plain Text**: Automatically fetches and formats synchronized or static lyrics directly from YouTube Music for the currently playing track.

---

### 💾 Offline Downloads & Library Management
- **Download Tracks & Playlists**: Download your favorite songs or full albums/playlists to your local storage for offline playback.
- **Offline-First Playback**: Automatically detects downloaded tracks and plays them directly from local disk with zero network bandwidth.
- **Local Playlists**: Create, edit, and organize custom local playlists without requiring a Google account.

---

### 🎨 Native Desktop Integration & Libadwaita Design
- **Modern GNOME Styling**: Clean, adaptive interface compliant with GNOME Human Interface Guidelines (HIG), supporting both light and dark themes.
- **Responsive Layout**: Adapts gracefully across desktop monitors, laptops, and mobile Linux devices (Purism Librem 5, PinePhone).
- **Full MPRIS2 Support**: Control playback, seek, adjust volume, and view high-resolution album artwork via GNOME Quick Settings, lock screen, and keyboard media keys.
- **Background Playback**: Closing the window keeps audio playing in the background; easily restore the window or exit via the dedicated quit control.
- **In-App Log Viewer**: Built-in diagnostic console (`LogWindow`) accessible from the information menu for real-time logging inspection and troubleshooting.
- **Rich Album Artwork**: High-resolution thumbnail caching displays crisp cover art in track rows, search results, and the player bar.

---

## 📸 Screenshots

<p align="center">
  <img src="assets/screenshot1.png" alt="Home and Playlists" width="48%">
  <img src="assets/screenshot2.png" alt="Search Results" width="48%">
</p>

<p align="center">
  <img src="assets/screenshot3.png" alt="Player and Queue" width="75%">
</p>

---

## ⌨️ Command-Line Interface

Monophony supports extensive command-line parameters for scripting, launchers, and external automations:

```bash
# Launch Monophony and search for a query
monophony --search "Daft Punk"

# Play a specific song by YouTube ID
monophony --play-song "k4V3Mo61fJM" --title "Song Title" --artist "Artist Name"

# Play a playlist or album by ID
monophony --play-group "RDCLAK5uy_k..."

# Pass search query directly as arguments
monophony Radiohead Creep
```

---

## 🛠️ Building & Installation

### Requirements
- **Python** 3.10+
- **GTK4** & **Libadwaita** 1.4+
- **GStreamer** 1.0 (with good, bad, and ugly plugins)
- **yt-dlp**
- **ytmusicapi**
- **logboth**

### Flatpak (Recommended)
You can build and test Monophony locally using `flatpak-builder`:

```bash
# Clone the repository
git clone https://github.com/valerio/monophony.git
cd monophony/source

# Build and install Flatpak
make flatpak
```

### Running from Source
```bash
cd source
pip3 install -r requirements-dev.txt
PYTHONPATH=. python3 bin/monophony.py
```

### Running Test Suite
```bash
# Within the Flatpak environment:
flatpak run --command=python3 --filesystem=$(pwd) io.gitlab.zehkira.Monophony -m unittest source/tests/tests.py
```

---

## 📁 Configuration & Paths

Monophony stores its user data and configuration according to XDG specifications:
- **Configuration & Playlists**: `~/.config/monophony/`
  - `settings.json`: General preferences and streaming settings
  - `playlists.json`: Local and synced playlist definitions
  - `oauth.json`: Google / YouTube Music OAuth credentials (when logged in)
- **Cache**: `~/.cache/monophony/` (album art thumbnails, cached stream URIs)
- **Downloads**: `~/Music/` (configurable in settings)

---

## 📜 License

Monophony is free software licensed under the **[0BSD License](LICENSE)** (Zero-Clause BSD). You are free to use, modify, and distribute it for any purpose.

Third-party dependencies and libraries retain their respective licenses (inspectable within the app via *Information → Licenses*).
