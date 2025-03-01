import os
import subprocess
import requests
from Video_Downloading import Video
from Playlist_Downloading import Playlist
from importlib.metadata import version

# TODO: STUDY MORE ABOUT IMPORTLIB.METADATA and requests


class MyDownloader(Video):
    def __init__(self):
        self.width = 80
        self.logger = Video.get_logger(self)

    def clear_screen(self):
        self.logger.debug("Clearing screen")
        os.system("cls" if os.name == "nt" else "clear")

    def welcome(self):
        self.logger.info("Displaying Welcome Screen")
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
        self.logger.info(f"Checking latest version for package: {package_name}")
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            version = response.json()["info"]["version"]
            self.logger.debug(f"Latest version for {package_name}: {version}")
            return version
        except requests.RequestException as e:
            self.logger.error(f"Failed to get latest version for {package_name}: {e}")
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
            logging.error("requirements.txt file not found!")
            input("Press Enter to exit...")
            os._exit(1)

    def check_requirements(self):
        """Check and update package requirements from requirements.txt"""
        self.logger.info("Starting requirements check")
        self.clear_screen()
        print(" Checking Requirements ... ".center(self.width, "="))

        packages = self.read_requirement()
        if not packages:
            self.logger.warning("No valid packages found in requirements.txt")
            print("No valid packages found in requirements.txt")
            self.exit_program()

        for package in packages:
            try:
                installed_version = version(package)
                self.logger.info(
                    f"Package {package} installed version: {installed_version}"
                )
                print(
                    f"\n- {package} is installed with version {installed_version}",
                    end="",
                )

                latest_version = self.get_latest_version(package)
                if not latest_version:
                    self.logger.error(f"Could not fetch latest version for {package}")
                    print(f"\n- Error: Could not fetch latest version for {package}")
                    self.exit_program()

                if latest_version != installed_version:
                    self.logger.info(
                        f"Update available for {package}: {latest_version}"
                    )
                    print(
                        f"-\n New version {latest_version} is available for {package}"
                    )
                    if not self.install_package(package, upgrade=True):
                        self.exit_program()
                else:
                    self.logger.info(f"Package {package} is up to date")
                    print(f", its up to date")

            except Exception as e:
                self.logger.error(f"Error installing {package}: {str(e)}")
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
            logging.info(f"Successfully installed {package}")
            print(f"- {package} has been installed successfully!")
            return True
        except subprocess.CalledProcessError:
            logging.error(f"Failed to install {package}")
            print(f"Failed to install {package}.")
            input("Press Enter to exit...")
            return False

    def exit_program(self):
        self.logger.info("Exiting program")
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
                self.logger.info(f"User selected option: {choice}")
                actions.get(choice, self.invalid_option)()

            except KeyboardInterrupt:
                self.logger.warning("Program interrupted by user")
                self.exit_program()

            except Exception as e:
                self.logger.error(f"An error occurred: {str(e)}")
                print(f"An Error Occurred: {e}")
                input("Press Enter to Continue...")

    def invalid_option(self):
        self.logger.warning("Invalid option selected")
        print("Invalid Option! Please try again.")
        input("Press Enter to continue...")


if __name__ == "__main__":
    downloader = MyDownloader()
    downloader.check_requirements()
    downloader.main()
