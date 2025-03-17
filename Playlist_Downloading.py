import os
from pathlib import Path
import yt_dlp
import re
from Video_Downloading import Video
import os


class Playlist(Video):
    VALID_URL_PREFIX = "https://youtube.com/playlist?list="
    INVALID_VIDEO_TITLES = {"[Private video]", "[Deleted video]"}

    def __init__(self):
        super().__init__()

    def setup_folder(self, title):
        try:
            safe_title = re.sub(r'[\\/:*?"<>|]', "-", title)
            folder_path = self.download_path / safe_title
            folder_path.mkdir(parents=True, exist_ok=True)
            os.chdir(folder_path)
            return safe_title
        except AttributeError:
            self.download_path = Path.home() / "Downloads"
            return self.setup_folder(title)

    def get_info(self, url):
        try:
            info_option = {**self.info_option, "extract_flat": True}

            with yt_dlp.YoutubeDL(info_option) as youtube_playlist:
                playlist_info = youtube_playlist.extract_info(url, download=False)

            playlist_title = playlist_info["title"]

            self.logger.info(f"You are downloading the playlist: {playlist_title}\n")
            self.logger.info(f"From ({playlist_info['channel']}) Channel on YouTube\n")
            self.logger.info(
                f"Total videos in the playlist: {playlist_info['playlist_count']}\n"
            )

            self.setup_folder(playlist_title)
            self.logger.info(
                f"The playlist will be Saved in the folder >> {Path.cwd()}\n"
            )

            return playlist_info["entries"]

        except Exception as e:
            self.logger.error(f"Error getting playlist info: {str(e)}")
            input("Press Enter to Continue...")
            return None

    def create_video_index(self, videos):
        for index, video in enumerate(videos, start=1):
            video["playlist_index"] = index

        print(f" Now downloading the playlist ... ".center(self.width, "="), end="\n\n")
        return videos

    def playlist_process(self, videos):
        try:

            total_videos = len(videos)

            for index, video in enumerate(videos, start=1):
                try:
                    if video["title"] in self.INVALID_VIDEO_TITLES:
                        self.logger.warning(f"skipped video {index}-{video['title']}\n")
                        continue

                    self._download_single_video(video, index, total_videos)

                except KeyboardInterrupt:
                    self.logger.info("Program interrupted by user")
                    self.exit_program()

                except Exception as e:
                    self.logger.error(f"Error downloading video {index}: {str(e)}")
                    print(f"An error occurred: {e}")
                    continue

            self.logger.info(
                " All Videos Downloaded Successfully ".center(self.width, "=")
            )
            input("Press Enter To continue ...")
        except Exception as e:
            self.logger.error(f"Error in playlist download: {str(e)}")
            input("Press Enter to Continue...")

    def _delete_partial_download(self, file_name):
        """Delete any existing partial download files"""
        try:
            part_file = Path(f"{file_name}.part")
            if part_file.exists():
                self.logger.info(f"Removing partial download: {part_file}")
                os.remove(part_file)
        except Exception as e:
            self.logger.error(f"Error deleting partial download: {str(e)}")

    def _download_single_video(self, video, index, total_videos):
        try:
            file_name = f"{video['playlist_index']} - {video['title']}.mp4"
            # Delete any partial downloads before starting
            self._delete_partial_download(file_name)

            self.logger.info(
                f"Downloading video {index} of {total_videos}: {video['title']}\n"
            )

            video_option = {**self.download_option, "outtmpl": file_name}

            with yt_dlp.YoutubeDL(video_option) as video_download:
                video_download.download([video["url"]])

        except yt_dlp.utils.DownloadError as e:
            self.logger.error(f"Download failed for video {index}: {str(e)}")
        except KeyError as e:
            self.logger.error(f"Missing required video information: {str(e)}")
        except Exception as e:
            self.logger.error(f"Unexpected error downloading video {index}: {str(e)}")

    def download_playlist(self):
        try:
            Video.welcome(self, "Playlist Downloading")
            url = input("Enter the URL of the playlist >> ").strip()

            self.logger.debug(f"Processing Url >> {url}\n")
            if not url:
                self.logger.error("[Error]: Empty URL provided")
                raise ValueError("URL cannot be empty.")

            print(" Loading ... ".center(self.width, "=").title(), end="\n\n")

            if not url.startswith(self.VALID_URL_PREFIX):
                self.logger.error(
                    f"Invalid URL format, Please check that Your URL starts with >> {self.VALID_URL_PREFIX}"
                )
                input("Press Enter to Continue...")
                return

            videos = self.get_info(url)
            if not videos:
                self.logger.warning("No videos found in playlist")
                input("Press Enter to Continue...")
                return

            indexed_videos = self.create_video_index(videos)
            self.playlist_process(indexed_videos)

        except ValueError as ve:
            self.logger.error(f"ValueError: {str(ve)}")
            input("Press Enter to Continue...")
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            input("Press Enter to Continue...")


if __name__ == "__main__":
    Playlist().download_playlist()
