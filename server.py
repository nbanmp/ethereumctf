#!/usr/bin/python

from flask import Flask
from flask import request
from flask import abort

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "/chal1_name for chal1 /chall2 for chal2 and /chal3 for chal4"

@app.route('/example', methods=['GET'])
def example():
    return "Here is the address you need to hack: "

@app.route('/example', methods=['POST'])
def example_test():
    if not request.args or not 'address' in request.args:
        abort(400)
    address_to_test = request.args['address']

    # Check if the address was one we gave out and if it was successfully pwned.
    return "Here is the address we are testing: " + request.args['address']

if __name__ == '__main__':
    app.run(debug=True, port=3000)

