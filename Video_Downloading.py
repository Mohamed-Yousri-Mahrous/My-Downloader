import os
import yt_dlp
import logging
from pathlib import Path
import sys


class Video:
    def __init__(self):
        self.download_path = Path.home() / "Downloads"
        self.width = 80
        self.logger = self.setup_logger()

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    def exit_program(self):
        """Exit the program"""
        print(" Goodbye! ".center(self.width, "="))
        self.logger.debug(" Exiting program ".center(self.width, "="))
        sys.exit(0)

    def welcome(self, program_name):
        self.logger.info(f"Starting {program_name}")
        self.clear_screen()
        border = "=" * self.width
        message = [
            border,
            f" Welcome to the {program_name} program ".center(self.width, "="),
            " Created By Mohamed Yousri ".center(self.width, "="),
            border,
        ]
        print("\n".join(message))

    @staticmethod
    def setup_logger():
        logger = logging.getLogger("Mohamed")
        logger.setLevel(logging.DEBUG)

        if not logger.hasHandlers():
            file_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            console_format = logging.Formatter("[%(levelname)s] - %(message)s")
            handlers = [
                (logging.StreamHandler(), logging.INFO, console_format),
                (
                    logging.FileHandler("Download.log", encoding="utf-8"),
                    logging.DEBUG,
                    file_format,
                ),
            ]

            for handler, level, formatter in handlers:
                handler.setLevel(level)
                handler.setFormatter(formatter)
                logger.addHandler(handler)

        return logger

    def convert_duration(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        if hours == 0:
            return f"{minutes}m {seconds}s"
        elif minutes == 0:
            return f"{seconds}s"
        else:
            return f"{hours}h {minutes}m {seconds}s"

    def get_info(self, url):
        try:
            self.logger.info(f"Fetching video information for URL: {url}")
            url_option = {
                "quiet": True,
                "no_warnings": True,
            }

            with yt_dlp.YoutubeDL(url_option) as youtube_Video:
                video_info = youtube_Video.extract_info(url, download=False)

            video_title = video_info["title"]
            Youtube_channel = video_info["channel"]
            video_duration = video_info["duration"]
            video_duration = self.convert_duration(video_duration)

            self.logger.info(f"Video title: {video_title}")
            self.logger.info(f"Channel: {Youtube_channel}")
            self.logger.info(f"Duration: {video_duration}")

            print(
                f" - You are downloading Video >> {video_title}".title(),
                end="\n\n",
            )
            print(
                f" - From ({Youtube_channel}) Channel on YouTube".title(),
                end="\n\n",
            )
            print(f" - The Video Duration is >> {video_duration}".title(), end="\n\n")
            print(f" - The Video will be Saved in >> {self.download_path}", end="\n\n")
            print(
                f" Now downloading the Video ... ".center(80, "=").title(), end="\n\n"
            )

            return video_info

        except KeyError as ke:
            self.logger.error(f"KeyError while fetching video info: {ke}")
            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Error while fetching video info: {e}")
            input("Press Enter to Continue...")

    def video_process(self, video_info):
        if not video_info:
            self.logger.error("No video information available")
            input("Press Enter to Continue...")
            return

        try:
            video_option = {
                "format": "best",
                "outtmpl": self.download_path / "%(title)s.%(ext)s",
                "quiet": True,
                "no_warnings": True,
            }

            self.logger.info(f"Downloading {video_info['title']} ...\n")

            with yt_dlp.YoutubeDL(video_option) as video_download:
                video_download.download([video_info["webpage_url"]])

            self.logger.debug(f"Successfully downloaded video: {video_info['title']}")
            print(" Video downloaded successfully ".center(80, "="), end="\n\n")
            input("Press Enter to Continue...")

        except yt_dlp.utils.DownloadError as e:
            self.logger.error(f"Download error: {e}")
            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Unexpected error during download: {e}")
            input("Press Enter to Continue...")

    def download_video(self):
        self.welcome("Video Downloading")

        try:
            video_url = input("Enter the URL of the Video >> ").strip()

            if not video_url:
                self.logger.warning("Empty URL provided")
                raise ValueError("URL cannot be empty.")

            self.logger.debug(f"Processing video URL: {video_url}")
            print(" Loading ... ".center(80, "=").title(), end="\n\n")

            info = self.get_info(video_url)

            if info:
                self.video_process(info)

        except ValueError as ve:
            self.logger.error(f"ValueError: {ve}")
            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Unexpected error in main: {e}")
            input("Press Enter to Continue...")


if __name__ == "__main__":
    Video().download_video()
