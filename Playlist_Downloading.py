import os
import yt_dlp
import re, json
from Video_Downloading import Video


class Playlist(Video):
    def __init__(self):
        super().__init__()
        self.logger = self.get_logger()
        self.width = 80

    def check_playlist_title(self, playlist_title):
        # Replace invalid characters with a hyphen
        self.logger.info(f"Checking playlist title: {playlist_title}")
        return re.sub(r'[\\/:*?"<>|]', "-", playlist_title)

    def get_info(self, url):
        try:
            self.logger.info(f"Getting playlist info for URL: {url}")
            playlist_option = {
                "extract_flat": True,
                "quiet": True,
                "no_warnings": True,
            }

            with yt_dlp.YoutubeDL(playlist_option) as youtube_playlist:
                playlist_info = youtube_playlist.extract_info(url, download=False)

            # Display the playlist information in the Terminal
            playlist_title = playlist_info["title"]
            playlist_count = playlist_info["playlist_count"]
            Youtube_channel = playlist_info["channel"]
            self.logger.info(f"Playlist title: {playlist_title}")
            self.logger.info(f"Channel: {Youtube_channel}")
            self.logger.info(f"Video count: {playlist_count}")

            print(
                f" - You are downloading the playlist: {playlist_title}".title(),
                end="\n\n",
            )
            print(f" - From ({Youtube_channel}) Channel on YouTube".title(), end="\n\n")
            print(
                f" - Total videos in the playlist: {playlist_count}".title(), end="\n\n"
            )

            # Check if the playlist title is valid
            playlist_title = self.check_playlist_title(playlist_title)

            # change Directory To User Downloads Folder and Create a Folder with the Playlist Name
            downloads_path = os.path.expanduser("~/Downloads")
            self.logger.info(f"Changing directory to: {downloads_path}")
            os.chdir(downloads_path)

            if not os.path.exists(playlist_title):
                self.logger.info(f"Creating directory: {playlist_title}")
                os.mkdir(playlist_title)
            os.chdir(playlist_title)

            print(
                f" - The playlist will be Saved in the folder >> {os.getcwd()}".title(),
                end="\n\n",
            )

            print(
                f" Now downloading the playlist ... ".center(self.width, "=").title(),
                end="\n\n",
            )
            videos = playlist_info["entries"]

            # manually assign playlist_index To videos information
            for index, video in enumerate(videos, start=1):
                video["playlist_index"] = index

            self.logger.info("Saving playlist info to JSON file")
            with open("playlist_info.json", "w") as f:
                json.dump(videos, f)

            return videos

        except Exception as e:
            self.logger.error(f"Error getting playlist info: {str(e)}")
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")

    def download_playlist(self, videos):
        try:
            self.logger.info("Starting playlist download")
            playlist_option = {
                "format": "best",
                "quiet": True,
                "no_warnings": True,
            }

            for index, video in enumerate(videos, start=1):
                try:
                    if (
                        video["title"] == "[Private video]"
                        or video["title"] == "[Deleted video]"
                    ):
                        self.logger.warning(
                            f"Skipping {video['title']} at index {index}"
                        )
                        print(
                            f"- Downloading video {index} is skipped As it is {video['title']} ".title(),
                            end="\n\n",
                        )
                    else:
                        file_name = f"{video['playlist_index']} - {video['title']}.mp4"
                        self.logger.info(
                            f"Downloading video {index}/{len(videos)}: {video['title']}"
                        )

                        print(
                            f"- Downloading video {index} of {len(videos)} - {video['title']} ".title(),
                            end="\n\n",
                        )

                        video_option = {
                            **playlist_option,
                            "outtmpl": file_name,
                        }

                        with yt_dlp.YoutubeDL(video_option) as video_download:
                            video_download.download([video["url"]])

                except Exception as e:
                    self.logger.error(f"Error downloading video {index}: {str(e)}")
                    print(f"An error occurred: {e}")

            self.logger.info("Playlist download completed successfully")
            print(
                " All videos in the playlist have been downloaded successfully ".center(
                    self.width, "="
                ).title(),
                end="\n\n",
            )

            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Error in playlist download: {str(e)}")
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")

    def main(self):
        try:
            self.logger.info("Starting playlist downloader")
            self.welcome("Playlist Downloading")

            url = input("Enter the URL of the playlist >> ").strip()

            if url:
                self.logger.info(f"Processing URL: {url}")
                print(" Loading ... ".center(self.width, "=").title(), end="\n\n")
                if url.startswith("https://youtube.com/playlist?list="):
                    videos = self.get_info(url)

                    if videos:
                        self.download_playlist(videos)
                    else:
                        self.logger.warning("No videos found in playlist")
                        print("No videos found in the playlist.".title())
                        input("Press Enter to Continue...")

                else:
                    self.logger.error("Invalid URL format")
                    print(
                        "Invalid URL...\nPlease check that Your URL starts with >> https://youtube.com/playlist?list=".title()
                    )
                    input("Press Enter to Continue...")

            else:
                self.logger.error("Empty URL provided")
                raise ValueError("URL cannot be empty.")

        except ValueError as ve:
            self.logger.error(f"ValueError: {str(ve)}")
            print(f"ValueError: {ve}")
            input("Press Enter to Continue...")

        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")


if __name__ == "__main__":
    Playlist().main()
