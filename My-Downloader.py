import os
import subprocess
import requests
from Video_Downloading import Video
from Playlist_Downloading import Playlist
from importlib.metadata import version

# TODO: STUDY MORE ABOUT IMPORTLIB.METADATA and requests


class MyDownloader:
    def __init__(self):
        self.packages = ["yt_dlp"]
        self.width = 80

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def welcome(self):
        self.clear_screen()
        print("=" * self.width)
        print(" Welcome to My Downloader Program ".center(self.width, "="))
        print(" Created by : Mohamed Yousri ".center(self.width, "="))
        print("=" * self.width)

    # TODO
    def get_latest_version(self, package_name):
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()["info"]["version"]
        except requests.RequestException:
            return None

    def check_requirements(self):
        self.clear_screen()
        print(" Checking Requirements ... ".center(self.width, "="))

        for package in self.packages:
            try:
                installed_version = version(package)
                latest_version = self.get_latest_version(package)
                print(f"- {package} is installed with version {installed_version}")

                # TODO: STUDY MORE ABOUT THIS
                if latest_version and latest_version != installed_version:
                    print(f"- New version {latest_version} is available for {package}")
                    self.install_package(package, upgrade=True)

            except:
                print(f"- Installing {package}...")
                self.install_package(package)

        input("Press Enter to continue...")

    # TODO: STUDY MORE ABOUT THIS
    @staticmethod
    def install_package(package, upgrade=False):
        try:
            command = ["pip", "install"]
            if upgrade:
                command.append("--upgrade")
            command.append(package)
            subprocess.run(command, shell=True, check=True, text=True)
            print(f"- {package} has been installed successfully!")
        except subprocess.CalledProcessError:
            print(f" Failed to install {package}.")

    def exit_program(self):
        print("Goodbye!")
        os._exit(0)

    def main(self):
        actions = {
            "1": Video().main,
            "2": Playlist().main,
            "3": self.exit_program,
        }

        while True:
            try:
                self.welcome()
                print("[1] Download a Video".center(25), end="")
                print("[2] Download a Playlist".center(25), end="")
                print("[3] Exit".center(25))
                print("=" * self.width)

                choice = input("Please Choose an Option: ").strip()
                actions.get(choice, self.invalid_option)()

            except KeyboardInterrupt:
                self.exit_program()

            except Exception as e:
                print(f"An Error Occurred: {e}")
                input("Press Enter to Continue...")

    def invalid_option(self):
        print("Invalid Option! Please try again.")
        input("Press Enter to continue...")


if __name__ == "__main__":
    downloader = MyDownloader()
    downloader.check_requirements()
    downloader.main()
