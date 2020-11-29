class Color:
    BOLD = "\033[1m"
    END = "\033[0m"


def bold_string(string):
    return Color.BOLD + string + Color.END


if __name__ == "__main__":
    print(Color.BOLD + "Something is bold" + Color.END + "!")
