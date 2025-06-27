from flask import Flask
import os
import random

app = Flask(__name__)

@app.route('/')
def hello_world():
    app_env = os.environ.get("APP_ENV", "default")
    random_number = random.randint(1, 100)
    return f"Hello, World! #{random_number} - Environment: {app_env}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
