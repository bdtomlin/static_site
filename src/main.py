import os
import shutil


def main():
    print("Removing previous files...")
    empty_public()
    print("Copying files from static...")
    copy_static()


def empty_public():
    if os.path.exists(path("public")):
        shutil.rmtree(path("public"))

    os.mkdir(path("public"))


def copy_static(dirname="static"):
    dir = path(dirname)
    for entry in os.scandir(dir):
        if entry.name.startswith("."):
            continue

        if entry.is_file():
            print(f"{dir}/{entry.name}")
            dest = dest_from_src(entry.path)
            shutil.copy(entry.path, dest)
        if entry.is_dir():
            dest = dest_from_src(entry.path)
            os.mkdir(dest)
            copy_static(f"{dirname}/{entry.name}")


def dest_from_src(src):
    static_path = path("static")
    public_path = path("public")

    return src.replace(static_path, public_path)


def path(path):
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, f"../{path}")
    return os.path.normpath(path)


main()
