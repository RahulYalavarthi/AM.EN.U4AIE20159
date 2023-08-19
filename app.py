from flask import Flask, request, jsonify
import requests
import time
import concurrent.futures

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get("numbers", [])
    except requests.exceptions.Timeout:
        pass  # Ignore timeouts
    except requests.exceptions.RequestException:
        pass  # Ignore other request errors
    return []

@app.route("/numbers", methods=["GET"])
def get_numbers():
    urls = request.args.getlist("url")

    merged_numbers = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            merged_numbers.extend(future.result())

    merged_numbers = sorted(list(set(merged_numbers)))
    return jsonify({"numbers": merged_numbers})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008)
