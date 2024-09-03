import os
import shutil

from markdown_to_html_node import markdown_to_html_node


class SiteBuilder:
    def __init__(self) -> None:
        self.src = self.path("static")
        self.content_path = self.path("content")
        self.dest = self.path("public")
        self.template_path = self.path("template.html")

    def build(self):
        print("Removing previous files...")
        self.empty_public()
        print("Copying files from static...")
        self.copy_static(self.src)
        print("Transforming Markdown...")
        self.transform_markdown(self.content_path)

    def transform_markdown(self, content_path):
        for entry in os.scandir(content_path):
            if entry.is_file() and entry.path.endswith(".md"):
                self.generate_html_from_markdown(entry)
            if entry.is_dir():
                dest = entry.path.replace(self.content_path, self.dest)
                if not os.path.isdir(dest):
                    os.mkdir(dest)
                self.transform_markdown(entry.path)

    def generate_html_from_markdown(self, entry):
        dest = entry.path.replace(self.content_path, self.dest)
        dest = dest.replace(".md", ".html")

        print(f"{entry.path} -> {dest}")

        with open(entry.path) as f:
            md = f.read()

        title = self.extract_title(md)
        content = markdown_to_html_node(md).to_html()

        with open(self.template_path) as f:
            template = f.read()

        page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

        with open(dest, "w") as f:
            f.write(page)

    def extract_title(self, markdown):
        lines = markdown.split("\n")
        for line in lines:
            if line.startswith("# "):
                return line.lstrip("# ")
        raise Exception("Missing H1 header")

    def empty_public(self):
        if os.path.exists(self.dest):
            shutil.rmtree(self.dest)

        os.mkdir(self.dest)

    def copy_static(self, dir):
        for entry in os.scandir(dir):
            if entry.name.startswith("."):
                continue

            if entry.is_file():
                dest = entry.path.replace(self.src, self.dest)
                print(f"{dir}/{entry.name} -> {dest}")
                shutil.copy(entry.path, dest)
            if entry.is_dir():
                dest = entry.path.replace(self.src, self.dest)
                os.mkdir(dest)
                self.copy_static(entry.path)

    def path(self, name):
        dirname = os.path.dirname(__file__)
        path = os.path.join(dirname, f"../{name}")
        return os.path.normpath(path)
