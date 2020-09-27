from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/')
def direction():
    a = [240, 200, 300, 340]
    scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    res = random.choice(a)
    res_scale = random.choice(scale)
    return jsonify({'direction': res, 'scale': res_scale})

if __name__ == "__main__":
    app.run()