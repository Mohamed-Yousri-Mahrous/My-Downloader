import os
import yt_dlp


def Welcome():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 80)
    print(" Welcome to the Video Downloading program ".center(80, "=").title())
    print(" Created By Mohamed Yousri ".center(80, "=").title())
    print("=" * 80, end="\n\n")


def convert_duration(seconds):

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours == 0:
        return f"{minutes}m {seconds}s"
    elif minutes == 0:
        return f"{seconds}s"
    else:
        return f"{hours}h {minutes}m {seconds}s"


def get_info(url):

    try:

        url_option = {
            "quiet": True,
            "no_warnings": True,
        }

        with yt_dlp.YoutubeDL(url_option) as youtube_Video:
            video_info = youtube_Video.extract_info(url, download=False)

        # Display the playlist information in the Terminal
        video_title = video_info["title"]
        Youtube_channel = video_info["channel"]
        video_duration = video_info["duration"]
        video_duration = convert_duration(video_duration)

        print(f" - You are downloading Video >> {video_title}".title(), end="\n\n")
        print(f" - From ({Youtube_channel}) Channel on YouTube".title(), end="\n\n")
        print(f" - The Video Duration is >> {video_duration}".title(), end="\n\n")

        download_path = os.path.expanduser(r"~\Downloads")
        print(f" - The Video will be Saved in >> {download_path}", end="\n\n")

        print(f" Now downloading the Video ... ".center(80, "=").title(), end="\n\n")

        return video_info

    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to Continue...")


def download_video(video_info):
    if not video_info:
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

        print(f"Downloading {video_info['title']} ...", end="\n\n")

        with yt_dlp.YoutubeDL(video_option) as video_download:
            video_download.download([video_info["webpage_url"]])

        print(" Video downloaded successfully ".center(80, "="), end="\n\n")
        input("Press Enter to Continue...")

    except yt_dlp.utils.DownloadError as e:
        print(f"Download error occurred: {e}")
        input("Press Enter to Continue...")

    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to Continue...")


def main():

    Welcome()

    try:
        video_url = input("Enter the URL of the Video >> ").strip()

        if not video_url:
            raise ValueError("URL cannot be empty.")

        print(" Loading ... ".center(80, "=").title(), end="\n\n")

        video_info = get_info(video_url)

        if video_info:
            download_video(video_info)

    except ValueError as ve:
        print(f"ValueError: {ve}")
        input("Press Enter to Continue...")

    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to Continue...")


if __name__ == "__main__":
    main()
