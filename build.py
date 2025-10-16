import os
import re
import sys
import json
import stat
import yaml
import shutil
import subprocess
from argparse import ArgumentParser


def copy_template(dir: str) -> None:
        os.makedirs(dir, exist_ok=True)
        shutil.copyfile(f"./templates/template.json", os.path.join(dir, "Jetbrains New UI Dark.json"))
        shutil.copyfile(f"./templates/template.json", os.path.join(dir, "Jetbrains New UI Light.json"))


def fix_file(dir: str, colors: dict) -> None:
        def substitute(template: str, item: dict | str) -> str:
                for key, value in item.items():
                        if isinstance(value, dict):
                                template = substitute(template, value)
                        else:
                                template = re.sub(rf"\"{key}(?!-)", '\"' + value, template)
                return template

        path: str = os.path.join(dir, f"{colors["--name"]}.json")

        with open(path, 'r', encoding="utf-8") as f:
                template: str = f.read()

        theme: str = substitute(template, colors)

        with open(path, 'w', encoding="utf-8") as f:
                f.write(theme)


def fix_version() -> tuple[str, str]:
        with open("package.json", 'r+', encoding="utf-8") as f:
                data = json.load(f)
                f.seek(0)

                if "version" not in data:
                        data["version"] = "1.0.0"
                        json.dump(data, f, indent=2)
                        f.truncate()
        
        with open("package-lock.json", 'r+', encoding="utf-8") as f:
                lock = json.load(f)
                f.seek(0)
                lock["version"]                 = data["version"]
                lock["packages"][""]["version"] = data["version"]
                json.dump(lock, f, indent=2)
                f.truncate()

        return data["version"], data["name"]


if __name__ == "__main__":
        if not os.path.exists("package.json"):
                raise Exception("package.json is missing")
        
        if not os.path.exists("package-lock.json"):
                subprocess.run("npm i", shell=True)

        copy_template("themes")
        with open("./colors/Dark.yaml", 'r', encoding="utf-8") as f:
                fix_file("themes", yaml.safe_load(f))
        with open("./colors/Light.yaml", 'r', encoding="utf-8") as f:
                fix_file("themes", yaml.safe_load(f))

        version, name = fix_version()
        subprocess.run("vsce package", shell=True)

        parser = ArgumentParser(
                prog="Extension Builder",
                description="Builds the .vsix extension")
        parser.add_argument("-I", "--install", action="store_true")
        args = parser.parse_args()
        
        if args.install:
                subprocess.run(f"code --install-extension {name}-{version}.vsix", shell=True)