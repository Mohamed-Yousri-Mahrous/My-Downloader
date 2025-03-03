import os
import subprocess
import requests
import logging
from importlib.metadata import version


class RequirementsManager:
    def __init__(self, logger):
        self.logger = logger
        self.width = 80

    def get_latest_version(self, package_name):
        self.logger.info(f"Start checking latest version for package: {package_name}")
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            version = response.json()["info"]["version"]
            self.logger.info(f"Latest version for {package_name}: {version}")
            return version
        except requests.RequestException as e:
            print("")
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

    def install_package(self, package, upgrade=False):
        try:
            command = ["pip", "install"]
            if upgrade:
                command.append("--upgrade")
            command.append(package)
            subprocess.run(command, shell=True, check=True, text=True)
            self.logger.info(f"Successfully installed {package}")
            print(f"- {package} has been installed successfully!")
            return True
        except subprocess.CalledProcessError:
            self.logger.error(f"Failed to install {package}")
            input("Press Enter to exit...")
            return False

    def check_requirements(self):
        """Check and update package requirements from requirements.txt"""
        self.logger.info("Starting requirements check")
        self.logger.info(" New session started ".center(self.width, "="))
        print(" Checking Requirements ... ".center(self.width, "="))

        packages = self.read_requirement()
        if not packages:
            self.logger.warning("No valid packages found in requirements.txt")
            return False

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
                    print("")
                    self.logger.error(f"Could not fetch latest version for {package}")
                    return False

                if latest_version != installed_version:
                    self.logger.info(
                        f"Update available for {package}: {latest_version}"
                    )
                    print(
                        f"-\n New version {latest_version} is available for {package}"
                    )
                    if not self.install_package(package, upgrade=True):
                        return False
                else:
                    self.logger.info(f"Package {package} is up to date")
                    print(f", its up to date")

            except Exception as e:
                self.logger.error(f"Error installing {package}: {str(e)}")
                print(f"\n- Error installing {package}: {str(e)}")
                return False

        return True
