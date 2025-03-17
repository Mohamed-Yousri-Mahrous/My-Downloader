from Video_Downloading import Video
from Playlist_Downloading import Playlist
from Requirements_Manager import RequirementsManager


class MyDownloader(Video):
    def __init__(self):
        super().__init__()

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
            "1": lambda: self.download_video(),
            "2": lambda: Playlist().download_playlist(),
            "3": self.exit_program,
        }

        while True:
            try:
                self.display_menu()
                choice = input("Please Choose an Option: ").strip()

                if not choice:
                    self.invalid_option()
                    continue

                action = actions.get(choice)

                if action:
                    action()
                else:
                    self.invalid_option()

            except KeyboardInterrupt:
                print("\n")
                self.logger.info("Program interrupted by user")
                self.exit_program()

            except Exception as e:
                self.logger.error(f"An error occurred: {str(e)}")
                input("Press Enter to Continue...")

    def invalid_option(self):
        self.logger.warning("Invalid option selected")
        input("Press Enter to continue...")


if __name__ == "__main__":
    try:
        downloader = MyDownloader()
        RequirementsManager().check_requirements()
        downloader.main()
    except Exception as e:
        print(f"Fatal error: {e}")
        downloader.exit_program()
