from flask import Flask, jsonify, render_template,request
from multiprocessing import Process
import datetime

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

    # 🤖 Example reply logic
    if "time" in user_text.lower():
        reply = f"The time is {datetime.datetime.now().strftime('%H:%M:%S')}"
    else:
        reply = "I heard you say: " + user_text

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
