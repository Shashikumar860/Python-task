from flask import Flask, render_template, request, jsonify
from gemini_service import generate, get_gemini_info

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    question = data.get("message", "")

    answer = generate(question)

    return jsonify({
        "response": answer
    })

@app.route("/gemini-info")
def gemini_info():
    return jsonify(get_gemini_info())

if __name__ == "__main__":
    app.run(debug=True)



# ========================================================
# Run : python app.py
# ========================================================