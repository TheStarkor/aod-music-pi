from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/')
def direction():
    res = random.randint(265, 277)
    return jsonify({'direction': res})

if __name__ == "__main__":
    app.run()