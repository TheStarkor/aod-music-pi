from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/')
def direction():
    a = [240, 200, 300, 340]
    scale = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    size = ['s', 'm', 'l']
    res = random.choice(a)
    res_scale = random.choice(scale)
    res_size = random.choice(size)
    return jsonify({'direction': res, 'scale': res_scale, 'size': res_size})

if __name__ == "__main__":
    app.run()