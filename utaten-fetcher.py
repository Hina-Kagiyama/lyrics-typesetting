#!/usr/bin/python3
import sys

if __name__ != '__main__':
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

# XPath selector for inner content only
sel = '/html/body/div[3]/div[1]/main/article/div[6]/div/div[1]/*'
elements = tree.xpath(sel)

# Validate XPath result
if not elements:
    raise Exception("XPath did not match any elements.")

# Convert elements to HTML string
raw_html = ''.join([etree.tostring(el, encoding='unicode') for el in elements])

# Apply replacements
processed_html = raw_html
processed_html = processed_html.replace('<span class="ruby"><span class="rb">', '')
processed_html = processed_html.replace('</span><span class="rt">', '(')
processed_html = processed_html.replace('</span></span>', ')')
processed_html = processed_html.replace('<br/>', '\n')
processed_html = processed_html.replace('\n\n\n', '\n\n--\n')

# Output the cleaned-up string
print(processed_html)
