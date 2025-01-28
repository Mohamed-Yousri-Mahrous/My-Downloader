import Video_Downloading, Playlist_Downloading, os


def welcome():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 80)
    print(" Welcome to My Downloader Program ".center(80, "="))
    print(" Created by : Mohamed Yousri ".center(80, "="))
    print("=" * 80)


def exit():
    print("Goodbye!")
    os._exit(0)


def main():

    while True:
        try:
            welcome()
            actions = {
                "1": Video_Downloading.main,
                "2": Playlist_Downloading.main,
                "3": exit,
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
            exit()

        except Exception as e:
            print(f"An Error Occurred: {e}")
            input("Press Enter to Continue...")


if __name__ == "__main__":
    main()
