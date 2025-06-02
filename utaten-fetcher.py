#!/usr/bin/python3
import sys
import re

if __name__ != "__main__":
    sys.exit(0)

try:
    import requests
    from lxml import etree
except ImportError as e:
    print(f"Missing dependency: {e.name}. Please install it with pip.")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python script.py <URL>")
    sys.exit(1)

url = sys.argv[1]

if not url.startswith("https://utaten.com/lyric/"):
    print("Error: URL must start with 'https://utaten.com/lyric/'")
    sys.exit(1)

# Make the HTTP GET request
response = requests.get(url)
response.raise_for_status()  # Raise an error for bad status codes

# Parse HTML with lxml's etree directly
# Find the only div with class="hiragana"
elements = etree.HTML(response.text).xpath('//div[@class="hiragana"]')

# Validate XPath result
if not elements:
    raise Exception("No element with class 'hiragana' found.")
elif len(elements) > 1:
    raise Exception(
        "Multiple elements with class 'hiragana' found. Expected exactly one."
    )

# Apply replacements
processed_html = (
    re.sub(
        '<div class="hiragana">[\\s\\n ]*'
        "|[\\s\\n ]*</div>"
        '|<span class="ruby"><span class="rb">',
        "",
        etree.tostring(elements[0], encoding="unicode", method="html"),
    )
    .replace('</span><span class="rt">', "(")
    .replace("</span></span>", ")")
    .replace("<br>", "\n")
    .replace("<br/>", "\n")
    .replace("\n\n\n", "\n\n--\n")
)

# Output the cleaned-up string
print(processed_html)
