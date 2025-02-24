import os, subprocess
from Video_Downloading import Video
from Playlist_Downloading import Playlist

# TODO: STUDY MORE ABOUT IMPORTLIB.METADATA
from importlib.metadata import version
import requests


class My_Downloader:
    def __init__(self):
        self.packages = ["yt_dlp"]
        self.width = 80

    def welcome(self):
        os.system("cls" if os.name == "nt" else "clear")
        os.system("mode con: cols=self.width")
        print("=" * self.width)
        print(" Welcome to My Downloader Program ".center(self.width, "="))
        print(" Created by : Mohamed Yousri ".center(self.width, "="))
        print("=" * self.width)

    def get_latest_version(self, package_name):
        url = f"https://pypi.org/pypi/{package_name}/json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data["info"]["version"]
        else:
            return None

    def check_requirements(self):
        try:
            os.system("cls" if os.name == "nt" else "clear")
            print(" Checking Requirements ... ".center(self.width, "="))

            for package in self.packages:

                try:
                    latest_version = self.get_latest_version(package)
                    package_version = version(package)
                    print(f"- {package} is installed with version {package_version}")

                    if latest_version != package_version:
                        print(
                            f"- New version {latest_version} is available for {package}"
                        )
                        print(f"Updating {package}...")
                        subprocess.run(
                            ["pip", "install", "--upgrade", f"{package}"],
                            shell=True,
                            text=True,
                            check=True,
                        )
                        print(f"- {package} has been updated successfully!")

                except:
                    print(f"- Installing {package}...", end="\n\n")
                    subprocess.run(
                        ["pip", "install", f"{package}"],
                        shell=True,
                        text=True,
                        check=True,
                    )

        except Exception as e:
            print(f"⚠️ An error occurred: {e}")

        input("Press Enter to Continue...")

    def exit(self):
        print("Goodbye!")
        os._exit(0)

    def main(self):

        while True:
            try:
                self.welcome()
                actions = {
                    "1": Video().main,
                    "2": Playlist().main,
                    "3": self.exit,
                }
                print(
                    "[1] Download a Video".center(25),
                    "[2] Download a Playlist".center(25),
                    "[3] Exit".center(25),
                )
                print("=" * self.width)
                action = input("Please Choose an Option: ").strip()

                if action in actions:
                    actions[action]()
                else:
                    print("Invalid Option!")
                    input("Press Enter to Continue...")

            except KeyboardInterrupt:
                self.exit()

            except Exception as e:
                print(f"An Error Occurred: {e}")
                input("Press Enter to Continue...")


if __name__ == "__main__":
    My_Downloader().check_requirements()
    # My_Downloader().main()
