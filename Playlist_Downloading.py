import os
import yt_dlp
import re


class Playlist:

    def Welcome(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 80)
        print(" Welcome to the Playlist Downloading program ".center(80, "=").title())
        print(" Created By Mohamed Yousri ".center(80, "=").title())
        print("=" * 80, end="\n\n")

    def check_playlist_title(self, playlist_title):
        # Replace invalid characters with a hyphen
        return re.sub(r'[\\/:*?"<>|]', "-", playlist_title)

    def get_info(self, url):
        try:
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
            os.chdir(os.path.expanduser("~/Downloads"))
            if not os.path.exists(playlist_title):
                os.mkdir(playlist_title)
            os.chdir(playlist_title)

            print(
                f" - The playlist will be Saved in the folder >> {os.getcwd()}".title(),
                end="\n\n",
            )

            print(
                f" Now downloading the playlist ... ".center(80, "=").title(),
                end="\n\n",
            )
            videos = playlist_info["entries"]

            # manually assign playlist_index To videos information
            for index, video in enumerate(videos, start=1):
                video["playlist_index"] = index

            return videos

        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")

    def download_playlist(self, videos):
        try:

            playlist_option = {
                "format": "best",
                "quiet": True,
                "no_warnings": True,
            }

            for index, video in enumerate(videos, start=1):

                try:

                    file_name = f"{video['playlist_index']} - {video['title']}.mp4"

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
                    print(f"An error occurred: {e}")
                    print(
                        f" retrying to download video {index} of {len(videos)} - {video['title']} again ".center(
                            80, "="
                        ).title(),
                        end="\n\n",
                    )

            print(
                " All videos in the playlist have been downloaded successfully ".center(
                    80, "="
                ).title(),
                end="\n\n",
            )

            input("Press Enter to Continue...")

        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")

    def main(self):
        try:

            self.Welcome()

            url = input("Enter the URL of the playlist >> ").strip()

            if url:

                print(" Loading ... ".center(80, "=").title(), end="\n\n")
                if url.startswith("https://youtube.com/playlist?list="):

                    videos = self.get_info(url)

                    if videos:

                        self.download_playlist(videos)

                    else:

                        print("No videos found in the playlist.".title())
                        input("Press Enter to Continue...")

                else:

                    print(
                        "Invalid URL...\nPlease check that Your URL starts with >> https://youtube.com/playlist?list=".title()
                    )
                    input("Press Enter to Continue...")

            else:

                raise ValueError("URL cannot be empty.")

        except ValueError as ve:
            print(f"ValueError: {ve}")
            input("Press Enter to Continue...")

        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to Continue...")
