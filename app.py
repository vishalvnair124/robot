from flask import Flask, jsonify, render_template,request
from multiprocessing import Process
import datetime
import ollama
import requests

app = Flask(__name__)


def time_now():
    return datetime.datetime.now().strftime("%I:%M:%S")

def date_now():
    year = int(datetime.datetime.now().year)
    month = datetime.datetime.now().strftime("%B")
    date = int(datetime.datetime.now().day)
    return "{} {} {}".format(date, month, year)

def wishontime():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    elif 17 <= hour < 21:
        return "Good evening"
    else:
        return "Good night"


def wishme_text():
    lines = [
        wishontime() + ",",
        "Hi BOSS, I am your bot.",
        "Today is " + date_now(),
        "and now time is " + time_now(),
        "How may I help you today?"
    ]
    return " ".join(lines)




@app.route("/")
def home():
   
    return render_template(
        "face.html",
        talkMsg=wishme_text()
    )


@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    data = request.get_json()
    user_text = data.get("text", "").strip()
    print(f"User said: {user_text}")

    # 🔷 Prepare Ollama API request
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": "mistral",  # or llama3, etc.
        "prompt": user_text,
        "stream": False
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)

        if response.ok:
            response_json = response.json()
            reply = response_json.get("response") or response_json.get("message", "No response key found.")
            reply = reply.strip()
        else:
            print(f"❌ Ollama error {response.status_code}: {response.text}")
            reply = "Sorry, the model returned an error."

    except requests.exceptions.RequestException as e:
        print(f"🚨 Request failed: {e}")
        reply = "Sorry, I could not connect to the model."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
