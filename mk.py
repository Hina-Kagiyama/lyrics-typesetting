#!/usr/bin/python3

if __name__ != "__main__":
    raise ImportError("This script is not meant to be imported. Please run it directly.")

import os

if not os.path.exists("output"):
    os.makedirs("output")

for x in (x for x in os.listdir("./raw") if x.endswith(".typ")):
    print(f"Compiling: {x}")
    os.system(f'typst compile ./raw/"{x}" ./output/"{x[:-4]}".pdf --font-path ./fonts --root ./')
