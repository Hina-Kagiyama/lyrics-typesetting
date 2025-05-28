#!/usr/bin/python3

if __name__ != "__main__":
    raise ImportError("This script is not meant to be imported. Please run it directly.")

import os

if not os.path.exists("output"):
    os.makedirs("output")

l = [x for x in os.listdir(".") if x.endswith(".typ") and x != "lyrics-show.typ"]
for x in l:
    print(f"Compiling: {x}")
    os.system(f'typst compile "{x}" ./output/"{x[:-4]}".pdf --font-path ./fonts')
