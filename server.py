#!/usr/bin/python

from flask import Flask
from flask import request
from flask import abort
import setup as ethereumctf

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "/chal1_name for chal1 /chall2 for chal2 and /chal3 for chal4"

@app.route('/example', methods=['GET'])
def example():
    return "Here is the address you need to hack: " + ethereumctf.deploy_new('example') + "\n"

@app.route('/example', methods=['POST'])
def example_test():
    if not request.args or not 'address' in request.args:
        abort(400)
    address_to_test = request.args['address']
    if(ethereumctf.check_address_for_victory(address_to_test)):
        return "YOU WIN THE FLAG: eThCtF{flagsrock}\n"
    else:
        return "FAIL! No flags for you. :(\n"

if __name__ == '__main__':
    app.run(debug=True, port=3000)

