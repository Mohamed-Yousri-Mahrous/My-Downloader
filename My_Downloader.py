from Video_Downloading import Video
from Playlist_Downloading import Playlist
from Requirements_Manager import RequirementsManager
import sys


class MyDownloader(Video):
    def __init__(self):
        super().__init__()
        self.req_manager = RequirementsManager(self.logger)

    def check_requirements(self):
        """Check and update package requirements from requirements.txt"""
        self.clear_screen()  # Use instance method instead of class method
        if not self.req_manager.check_requirements():
            self.exit_program()

    def exit_program(self):
        self.logger.info("Exiting program")
        print(" Goodbye! ".center(self.width, "="))
        sys.exit(0)

    def display_menu(self):
        """Display the main menu options"""
        self.welcome("My Downloader")  # Use instance method
        menu_items = [
            "[1] Download a Video".center(26),
            "[2] Download a Playlist".center(26),
            "[3] Exit".center(26),
        ]
        print("".join(menu_items))
        print("=" * self.width)

    def main(self):
        # Initialize actions with instances only when needed
        actions = {
            "1": lambda: Video().main(),
            "2": lambda: Playlist().main(),
            "3": self.exit_program,
        }

        while True:
            try:
                self.display_menu()
                choice = input("Please Choose an Option: ").strip()

                if not choice:
                    self.invalid_option()
                    continue

                self.logger.info(f"User selected option: {choice}")
                action = actions.get(choice)

                if action:
                    action()
                else:
                    self.invalid_option()

            except KeyboardInterrupt:
                self.logger.info("Program interrupted by user")
                print("\nProgram interrupted by user. Exiting...")
                self.exit_program()

            except Exception as e:
                self.logger.error(f"An error occurred: {str(e)}")
                input("Press Enter to Continue...")

    def invalid_option(self):
        self.logger.warning("Invalid option selected")
        input("Press Enter to continue...")


def main():
    """Entry point of the application"""
    try:
        downloader = MyDownloader()
        downloader.check_requirements()
        downloader.main()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
