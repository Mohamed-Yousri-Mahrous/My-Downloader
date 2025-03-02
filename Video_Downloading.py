import os
import yt_dlp
import logging


class Video:
    def __init__(self):
        self.download_path = os.path.expanduser(r"~\Downloads")
        self.width = 80
        self.logger = self.get_logger()

    @staticmethod
    def clear_screen():
        os.system("cls" if os.name == "nt" else "clear")

    def welcome(self, program_name):
        self.logger.info("Starting Video Download")
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
    def get_logger():
        logger = logging.getLogger("Mohamed")
        logger.setLevel(logging.INFO)

        if not logger.hasHandlers():
            handlers = [
                (logging.StreamHandler(), logging.WARNING),
                (logging.FileHandler("Download.log"), logging.INFO),
            ]
            formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

            for handler, level in handlers:
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
            print(f"KeyError: {ke}")
            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Error while fetching video info: {e}")
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")

    def download_video(self, video_info):
        if not video_info:
            self.logger.error("No video information available")
            print("No video information available. Cannot download.")
            input("Press Enter to Continue...")
            return

        try:
            video_option = {
                "format": "best",
                "outtmpl": os.path.join(
                    os.path.expanduser("~/Downloads"), "%(title)s.%(ext)s"
                ),
                "quiet": True,
                "no_warnings": True,
            }

            self.logger.info(f"Starting download for video: {video_info['title']}")
            print(f"Downloading {video_info['title']} ...", end="\n\n")

            with yt_dlp.YoutubeDL(video_option) as video_download:
                video_download.download([video_info["webpage_url"]])

            self.logger.info(f"Successfully downloaded video: {video_info['title']}")
            print(" Video downloaded successfully ".center(80, "="), end="\n\n")
            input("Press Enter to Continue...")

        except yt_dlp.utils.DownloadError as e:
            self.logger.error(f"Download error: {e}")
            print(f"Download error occurred: {e}")
            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Unexpected error during download: {e}")
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")

    def main(self):
        self.welcome("Video Downloading")

        try:
            video_url = input("Enter the URL of the Video >> ").strip()

            if not video_url:
                self.logger.warning("Empty URL provided")
                raise ValueError("URL cannot be empty.")

            self.logger.info(f"Processing video URL: {video_url}")
            print(" Loading ... ".center(80, "=").title(), end="\n\n")

            info = self.get_info(video_url)

            if info:
                self.download_video(info)

        except ValueError as ve:
            self.logger.error(f"ValueError: {ve}")
            print(f"ValueError: {ve}")
            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Unexpected error in main: {e}")
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")


if __name__ == "__main__":
    Video().main()
