import os
from dotenv import load_dotenv
load_dotenv()

def make_register():
    with open("../data/registry.txt", "w") as registry:
        for root, dirs, files in os.walk(os.environ.get("FOLDER_PATH")):
            for file in files:
                if not file.endswith(".txt"):
                    registry.write(f"{file}\n")


def get_register():
    with open("../data/registry.txt", "r") as registry:
        return registry.read().splitlines()


if __name__ == "__main__":
    make_register()