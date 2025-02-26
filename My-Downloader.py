import os
import subprocess
import requests
from Video_Downloading import Video
from Playlist_Downloading import Playlist
from importlib.metadata import version

# TODO: STUDY MORE ABOUT IMPORTLIB.METADATA and requests


class MyDownloader:
    def __init__(self):
        self.width = 80

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")

    def welcome(self):
        self.clear_screen()
        border = "=" * self.width
        messages = [
            border,
            " Welcome to My Downloader Program ".center(self.width, "="),
            " Created by : Mohamed Yousri ".center(self.width, "="),
            border,
        ]
        print("\n".join(messages))

    def get_latest_version(self, package_name):
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()["info"]["version"]
        except requests.RequestException:
            return None

    @staticmethod
    def read_requirement():
        try:
            with open("requirements.txt", "r") as file:
                packages = [
                    line.strip()
                    for line in file
                    if line.strip() and not line.startswith("#")
                ]
            return packages
        except FileNotFoundError:
            print("requirements.txt file not found!")
            input("Press Enter to exit...")
            os._exit(1)

    def check_requirements(self):
        """Check and update package requirements from requirements.txt"""
        self.clear_screen()
        print(" Checking Requirements ... ".center(self.width, "="))

        packages = self.read_requirement()
        if not packages:
            print("No valid packages found in requirements.txt")
            self.exit_program()

        for package in packages:
            try:
                installed_version = version(package)
                print(
                    f"\n- {package} is installed with version {installed_version}",
                    end="",
                )

                latest_version = self.get_latest_version(package)
                if not latest_version:
                    print(f"\n- Error: Could not fetch latest version for {package}")
                    self.exit_program()

                if latest_version != installed_version:
                    print(
                        f"-\n New version {latest_version} is available for {package}"
                    )
                    if not self.install_package(package, upgrade=True):
                        self.exit_program()
                else:
                    print(f", its up to date")

            except Exception as e:
                print(f"\n- Error installing {package}: {str(e)}")
                self.exit_program()

    @staticmethod
    def install_package(package, upgrade=False):
        try:
            command = ["pip", "install"]
            if upgrade:
                command.append("--upgrade")
            command.append(package)
            subprocess.run(command, shell=True, check=True, text=True)
            print(f"- {package} has been installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}.")
            input("Press Enter to exit...")
            return False

    def exit_program(self):
        print(" Goodbye! ".center(self.width, "="))
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
                menu_items = [
                    "[1] Download a Video".center(25),
                    "[2] Download a Playlist".center(25),
                    "[3] Exit".center(25),
                ]
                print("".join(menu_items))
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
