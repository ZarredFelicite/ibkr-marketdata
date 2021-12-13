from flask import Flask, render_template, request, flash

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/marketdata", methods=['POST','GET'])
def stock():
    print(request.form['ticker'])
if __name__ == "__main__":
    app.run()
