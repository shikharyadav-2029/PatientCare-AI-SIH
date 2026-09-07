import urllib.request
import os

base_url = os.environ.get("BASE_URL", f"http://localhost:{os.environ.get('PORT', 5000)}")

urls = [
    f"{base_url}/index.html",
    f"{base_url}/styles.css",
    f"{base_url}/app.js",
    f"{base_url}/api/cases"
]

for url in urls:
    with urllib.request.urlopen(url, timeout=5) as res:
        data = res.read()
        print(f"{url} -> Status {res.status}, Size {len(data)} bytes")
print("ALL ASSETS ACCESSIBLE!")
