from flask import Flask, render_template
import requests

app = Flask(__name__)


@app.route('/')
def index():
    response = requests.get(url="http://localhost:9080/crawl.json?start_requests=true&spider_name=best_selling").json()
    items = response.get('items')
    return render_template('index.html', games=items)


@app.template_filter()
def filter_platform(platforms):
    if platforms:
        return ', '.join([translate_platform(platform) for platform in platforms])
    return ""


def translate_platform(platform):
    if platform == "win":
        return "Windows"
    elif platform == "linux":
        return "Linux"
    elif platform == "mac":
        return "Mac OS"
    elif platform == "vr_supported":
        return "VR"
    else:
        return "Other Platforms"


if __name__ == '__main__':
    app.run(debug=True)
