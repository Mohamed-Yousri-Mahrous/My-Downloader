import os
from Video_Downloading import Video
from Playlist_Downloading import Playlist


class My_Downloader:
    def welcome(self):
        os.system("cls" if os.name == "nt" else "clear")
        print("=" * 80)
        print(" Welcome to My Downloader Program ".center(80, "="))
        print(" Created by : Mohamed Yousri ".center(80, "="))
        print("=" * 80)

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
                print("=" * 80)
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
    My_Downloader().main()
