import subprocess
import requests
from importlib.metadata import version
from Video_Downloading import Video


class RequirementsManager(Video):
    """
    A class to manage Python package requirements for the application.

    This class handles:
    1. Reading requirements from requirements.txt
    2. Checking installed package versions
    3. Fetching latest versions from PyPI
    4. Updating packages when necessary

    Workflow:
    1. Reads requirements.txt file
    2. For each package:
        - Checks current installed version
        - Fetches latest version from PyPI
        - Updates if newer version is available

    Inherits from:
        Video: Base class providing logging and utility functions

    Usage:
        manager = RequirementsManager()
        manager.check_requirements()
    """

    def get_latest_version(self, package_name):
        """
        Fetch the latest version of a package from PyPI.

        Args:
            package_name: Name of the package to check

        Returns:
            str: Latest version number if successful, None otherwise

        Raises:
            RequestException: If PyPI request fails
        """
        url = f"https://pypi.org/pypi/{package_name}/json"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            version = response.json()["info"]["version"]
            return version
        except requests.RequestException as e:
            self.logger.error(f"Failed to get latest version for {package_name}: {e}\n")
            return None

    @staticmethod
    def read_requirement():
        """
        Read and parse requirements.txt file.

        Returns:
            list: List of package names from requirements.txt

        Raises:
            FileNotFoundError: If requirements.txt is not found
        """
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
            self.exit_program()

    def install_package(self, package, upgrade):
        """
        Install or upgrade a Python package using pip.

        Args:
            package: Name of the package to install
            upgrade: Whether to upgrade existing package

        Returns:
            bool: True if installation successful, False otherwise

        Raises:
            CalledProcessError: If pip command fails
        """
        try:
            command = ["pip", "install"]
            if upgrade:
                command.append("--upgrade")
            command.append(package)
            subprocess.run(command, shell=True, check=True, text=True)
            self.logger.info(f"Successfully installed {package}")
            return True
        except subprocess.CalledProcessError:
            self.logger.error(f"Failed to install {package}")
            input("Press Enter to exit...")
            return False

    def check_requirements(self):
        """
        Check and update all package requirements.

        Process:
        1. Read requirements.txt
        2. For each package:
            - Get current version
            - Check latest version
            - Update if needed

        Returns:
            bool: True if all requirements are met, False otherwise

        Example:
            manager = RequirementsManager()
            if manager.check_requirements():
                print("All packages up to date")
            else:
                print("Package update failed")
        """
        self.clear_screen()
        print(" Checking Requirements ...  ".center(self.width, "="))

        packages = self.read_requirement()
        if not packages:
            self.logger.warning("No valid packages found in requirements.txt")
            return False

        for package in packages:
            try:
                installed_version = version(package)
                print(
                    f"\n- {package} is installed with version {installed_version}",
                    end="",
                )

                latest_version = self.get_latest_version(package)
                if not latest_version:
                    self.logger.error(f"Could not fetch latest version for {package}")
                    return False

                if latest_version != installed_version:
                    self.logger.info(
                        f"Update available for {package}: {latest_version}\n"
                    )

                    if not self.install_package(package, upgrade=True):
                        return False
                else:
                    print(f", its up to date")

            except Exception as e:
                self.logger.error(f"Error installing {package}: {str(e)}\n")
                return False

        return True


if __name__ == "__main__":
    manager = RequirementsManager()
    manager.check_requirements()
