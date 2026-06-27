import os
import requests
from pathlib import Path
from flask import Flask, send_from_directory, abort

app = Flask(__name__)

origin = "https://kawaiiyuri.com/fishy/"

ROOT = Path(__file__).resolve().parent


@app.route("/", defaults={"file": "index.html"})
@app.route("/<path:file>")
def serve(file):
    file = os.path.normpath(file).replace("\\", "/")

    if file.startswith("../") or file.startswith("/"):
        abort(403)

    local_path = ROOT / file

    if not local_path.exists():
        url = origin + file

        print(f"Downloading {url}")

        r = requests.get(url, stream=True)

        if r.status_code != 200:
            abort(404)

        local_path.parent.mkdir(parents=True, exist_ok=True)

        with open(local_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

    return send_from_directory(ROOT, file)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)