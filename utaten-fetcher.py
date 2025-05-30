#!/usr/bin/python3
import sys

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
tree = etree.HTML(response.text)

# Find the only div with class="hiragana"
elements = tree.xpath('//div[@class="hiragana"]')

# Validate XPath result
if not elements:
    raise Exception("No element with class 'hiragana' found.")
elif len(elements) > 1:
    raise Exception(
        "Multiple elements with class 'hiragana' found. Expected exactly one."
    )

# Get inner HTML of the matched div
raw_html = "".join(
    [etree.tostring(el, encoding="unicode", method="html") for el in elements[0]]
)

# Apply replacements
processed_html = raw_html
processed_html = processed_html.replace('<span class="ruby"><span class="rb">', "")
processed_html = processed_html.replace('</span><span class="rt">', "(")
processed_html = processed_html.replace("</span></span>", ")")
processed_html = processed_html.replace("<br>", "\n")
processed_html = processed_html.replace("<br/>", "\n")
processed_html = processed_html.replace("\n\n\n", "\n\n--\n")

# Output the cleaned-up string
print(processed_html)
