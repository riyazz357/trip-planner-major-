import subprocess
import sys  # <-- 1. Import the sys module
from flask import Flask

app = Flask(__name__)

@app.route("/open_chatbot")
def open_chatbot():
    # 2. Use sys.executable instead of the string "python"
    # This ensures the chatbot runs with the same virtual environment
    subprocess.Popen([sys.executable, "chatbot.py"])
    return "Chatbot opened!"

if __name__ == "__main__":
    app.run(debug=True, port=5002)