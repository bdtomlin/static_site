import os
import shutil


def main():
    copy_static()


def copy_static():
    if not os.path.exists("../public"):
        shutil.rmtree("public")
    print(os.listdir())


main()
