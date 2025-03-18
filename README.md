# 🎥 My YouTube Downloader

A powerful, user-friendly Python application for downloading YouTube content seamlessly. Built with performance and reliability in mind, this tool makes video downloading a breeze.

## ✨ Key Features

- 📹 **Video Downloads**: Download individual YouTube videos in highest quality
- 📑 **Playlist Support**: Batch download entire playlists efficiently
- 🎯 **Smart Quality Selection**: Automatically selects best available quality
- 📂 **Organized Storage**: Structured file management with playlist organization
- 📝 **Advanced Logging**: Comprehensive tracking and error reporting
- 🔄 **Smart Package Management**: Automatic dependency handling
- 🚀 **Download Recovery**: Resume interrupted downloads automatically
- ⚡ **High Performance**: Optimized downloads powered by yt-dlp

## 🚀 Getting Started

### Prerequisites

- Python 3.6+
- pip (Python package installer)

### Installation Steps

1. Clone the repository:

```bash
git clone https://github.com/yourusername/My-Downloader.git
cd My-Downloader
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

### Detailed Usage Guide

#### Starting the Application

1. Open your terminal/command prompt
2. Navigate to the project directory:

```bash
cd c:\path\to\My-Downloader
```

3. Run the main program:

```bash
python My_Downloader.py
```

#### Using the Main Menu

The program presents three options:

```
==========================================
         Welcome to My Downloader
==========================================
           [1] Download a Video
         [2] Download a Playlist
               [3] Exit
==========================================
```

#### Downloading a Single Video

1. Select option `[1]` from the main menu
2. Enter the YouTube video URL when prompted
3. Wait for the download to complete
4. Videos are saved to your Downloads folder

Example URL format:

```
https://www.youtube.com/watch?v=VIDEO_ID
```

#### Downloading a Playlist

1. Select option `[2]` from the main menu
2. Enter the YouTube playlist URL
3. The program will:
   - Create a folder with the playlist name
   - Download all videos sequentially
   - Number files according to playlist order

Required playlist URL format:

```
https://youtube.com/playlist?list=PLAYLIST_ID
```

#### Download Location

- Single videos: Saved to `%USERPROFILE%\Downloads`
- Playlists: Saved to `%USERPROFILE%\Downloads\[Playlist_Name]`

#### Progress Tracking

The program provides:

- Real-time download progress
- Video title and channel information
- Duration details
- Success/failure notifications

#### Log Files

- Location: `Download.log` in the program directory
- Contains detailed operation logs
- Useful for troubleshooting

#### Error Handling

The program automatically:

- Skips unavailable videos in playlists
- Removes partial downloads on failure
- Retries failed downloads
- Reports errors in the log file

#### Exiting the Program

- Select option `[3]` from the main menu
- Or press `Ctrl+C` at any time

### Tips for Best Results

1. Ensure stable internet connection
2. Check available disk space
3. Verify URL format before pasting
4. Keep the program updated
5. Check logs if issues occur
