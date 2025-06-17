from flask import Flask
import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    random_number = random.randint(0, 100)
    return f'Hello, World! #{random_number}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
