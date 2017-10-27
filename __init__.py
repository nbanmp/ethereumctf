from CTFd.plugins import register_plugin_assets_directory, challenges
from CTFd.plugins.keys import get_key_class
from CTFd.models import db, Teams, Solves, Awards, Challenges, WrongKeys, Keys, Tags, Files, Tracking, Pages, Config, Hints, Unlocks, DatabaseError
from CTFd import utils
from CTFd.plugins.challenges import CHALLENGE_CLASSES
from flask import request, render_template, redirect, url_for, abort, jsonify
from CTFd.plugins.ethereumctf import ethereumctf
from urllib.parse import urlparse
import json
import ast

class BaseChallenge(object):
    id = None
    name = None
    templates = {}
    scripts = {}


class CTFdEthereumChallenge(BaseChallenge):
    id = "ethereum"  # Unique identifier used to register challenges
    name = "ethereum"  # Name of a challenge type
    templates = {  # Handlebars templates used for each aspect of challenge editing & viewing
        'create': '/plugins/ethereumctf/assets/ethereum-challenge-create.hbs',
        'update': '/plugins/ethereumctf/assets/ethereum-challenge-update.hbs',
        'modal': '/plugins/ethereumctf/assets/ethereum-challenge-modal.hbs',
    }
    scripts = {  # Scripts that are loaded when a template is loaded
        'create': '/plugins/ethereumctf/assets/ethereum-challenge-create.js',
        'update': '/plugins/ethereumctf/assets/ethereum-challenge-update.js',
        'modal': '/plugins/ethereumctf/assets/ethereum-challenge-modal.js',
    }

    @staticmethod
    def attempt(chal, request):
        """
        This method is used to check whether a given input is right or wrong. It does not make any changes and should
        return a boolean for correctness and a string to be shown to the user. It is also in charge of parsing the
        user's input from the request itself.

        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return: (boolean, string)
        """
        provided_key = request.form['key'].strip()
        chal_keys = Keys.query.filter_by(chal=chal.id).all()
        for chal_key in chal_keys:
            if get_key_class(chal_key.key_type).compare(chal_key.flag, provided_key):
                return True, 'Correct'
        return False, 'Incorrect'

    @staticmethod
    def solve(team, chal, request):
        """
        This method is used to insert Solves into the database in order to mark a challenge as solved.

        :param team: The Team object from the database
        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return:
        """
        provided_key = request.form['key'].strip()
        solve = Solves(teamid=team.id, chalid=chal.id, ip=utils.get_ip(req=request), flag=provided_key)
        db.session.add(solve)
        db.session.commit()
        db.session.close()

    @staticmethod
    def fail(team, chal, request):
        """
        This method is used to insert WrongKeys into the database in order to mark an answer incorrect.

        :param team: The Team object from the database
        :param chal: The Challenge object from the database
        :param request: The request the user submitted
        :return:
        """
        provided_key = request.form['key'].strip()
        wrong = WrongKeys(teamid=team.id, chalid=chal.id, ip=utils.get_ip(request), flag=provided_key)
        db.session.add(wrong)
        db.session.commit()
        db.session.close()


def get_chal_class(class_id):
    """
    Utility function used to get the corresponding class from a class ID.

    :param class_id: String representing the class ID
    :return: Challenge class
    """
    cls = CHALLENGE_CLASSES.get(class_id)
    if cls is None:
        raise KeyError
    return cls


def load(app):
    @app.route('/ethereum/geth_command', methods=['GET'])
    def geth_command():
        command = ''
        command += 'wget http://' + urlparse(request.url).netloc + '/ethereum/genesis.json\n'
        command += 'geth --datadir ~/.ethereum/ctf init genesis.json\n'
        command += ethereumctf.connect_to_geth_command
        return command

    @app.route('/ethereum/genesis.json', methods=['GET'])
    def get_genesis():
        return ethereumctf.genesis_json

    @app.route('/ethereum/faucet', methods=['POST', 'GET'])
    def fauceteth():
        if request.method == 'POST':
            if not request.form or not 'address' in request.form:
                abort(400)
            if ethereumctf.faucet(request.form['address']):
                return "Success! You recieved 1 ether."
            else:
                return "Failure. Wrong address?"
        else: # GET request
            if not request.args or not 'address' in request.args:
                abort(400)
            if ethereumctf.faucet(request.args['address']):
                return "Success"
            else:
                return "Failure"

    @app.route('/ethereum/create', methods=['POST'])
    def create():
        print(request.form) # Debugging
        if not request.form or not 'chal' in request.form:
            abort(400)
        chal = request.form['chal']
        result = ethereumctf.deploy_from_chalid(chal)
        return result

    @app.route('/ethereum/test', methods=['POST'])
    def check():
        if not request.form or not 'address' in request.form or not 'chal' in request.form:
            abort(400)
        address_to_test = request.form['address']
        chalid = request.form['chal']
        result = ethereumctf.check_address_for_victory(chalid, address_to_test)
        if(result):
            return result
        else:
            return "Incorrect"

    # Overriding /admin/chal/<int:chalid>/<prop>
    def admin_get_values(chalid, prop):
        challenge = Challenges.query.filter_by(id=chalid).first_or_404()
        if prop == 'keys':
            chal_keys = Keys.query.filter_by(chal=challenge.id).all()
            json_data = {'keys': []}
            for x in chal_keys:
                json_data['keys'].append({
                    'id': x.id,
                    'key': x.flag,
                    'type': x.key_type,
                    'type_name': get_key_class(x.key_type).name
                })
            return jsonify(json_data)
        elif prop == 'tags':
            tags = Tags.query.filter_by(chal=chalid).all()
            json_data = {'tags': []}
            for x in tags:
                json_data['tags'].append({
                    'id': x.id,
                    'chal': x.chal,
                    'tag': x.tag
                })
            return jsonify(json_data)
        elif prop == 'hints':
            hints = Hints.query.filter_by(chal=chalid)
            json_data = {'hints': []}
            for hint in hints:
                json_data['hints'].append({
                    'hint': hint.hint,
                    'type': hint.type,
                    'chal': hint.chal,
                    'cost': hint.cost,
                    'id': hint.id
                })
        elif prop == 'solidity':
            test_func = ethereumctf.challenges[str(chalid)]['solidity']['source']
            json_data = {'solidity': test_func}
        elif prop == 'test_func':
            test_func = ethereumctf.challenges[str(chalid)]['python_check']
            json_data = {'test_func': test_func}
        elif prop == 'starting_ether':
            result = ethereumctf.challenges[str(chalid)]['starting_value']
            json_data = {'starting_ether': str(result / 1000000000000000000) }
        elif prop == 'args':
            result = ethereumctf.challenges[str(chalid)]['args']
            json_data = {'args': json.dumps(result)}

        return jsonify(json_data)

    # Overriding /admin/chal/new
    def admin_create_chal():
        if request.method == 'POST':
            print("[DEBUG] Post request sent to my modified admin_create_chal")
            files = request.files.getlist('files[]')

            # Create challenge
            chal = Challenges(
                name=request.form['name'],
                description=request.form['desc'],
                value=request.form['value'],
                category=request.form['category'],
                type=request.form['chaltype'],
            )

            if 'hidden' in request.form:
                chal.hidden = True
            else:
                chal.hidden = False

            max_attempts = request.form.get('max_attempts')
            if max_attempts and max_attempts.isdigit():
                chal.max_attempts = int(max_attempts)

            db.session.add(chal)
            db.session.flush()

            # This if added by me
            print("[DEBUG] chal.id: " + str(chal.id))
            if chal.type == 'ethereum':
                solidity=request.form['solidity']
                test_func=request.form['test_func']
                args=request.form['args']
                starting_ether=request.form['starting-ether']
                flag = request.form['key']
                print("[DEBUG] Type is ethereum!")
                if ethereumctf.compile_contract(str(chal.id), solidity, test_func, ast.literal_eval(args), starting_ether, flag):
                    print("[DEBUG] successful compile!")
                else:
                    db.session.rollback()
                    print("[DEBUG] failed compile")
                    return redirect(url_for('admin_challenges.admin_create_chal')) # TODO: Fail better

            db.session.commit()


            flag = Keys(chal.id, request.form['key'], int(request.form['key_type[0]']))
            if request.form.get('keydata'):
                flag.data = request.form.get('keydata')
            db.session.add(flag)

            db.session.commit()

            for f in files:
                utils.upload_file(file=f, chalid=chal.id)

            db.session.commit()
            db.session.close()
            return redirect(url_for('admin_challenges.admin_chals'))
        else:
            return render_template('admin/chals/create.html')

    # Overriding /admin/chal/update
    ###Do stuff
    def admin_update_chal():
        challenge = Challenges.query.filter_by(id=request.form['id']).first_or_404()
        challenge.name = request.form['name']
        challenge.description = request.form['desc']
        challenge.value = int(request.form.get('value', 0)) if request.form.get('value', 0) else 0
        challenge.max_attempts = int(request.form.get('max_attempts', 0)) if request.form.get('max_attempts', 0) else 0
        challenge.category = request.form['category']
        challenge.hidden = 'hidden' in request.form

        if challenge.type == 'ethereum':
            solidity=request.form['solidity']
            test_func=request.form['test_func']
            args=request.form['args']
            starting_ether=request.form['starting-ether']
            if ethereumctf.compile_contract(str(challenge.id), solidity, test_func, ast.literal_eval(args), starting_ether):
                print("[DEBUG] successful compile!")
                # Successful Compile
            else:
                print("[DEBUG] failed compile")
                return redirect(url_for('admin_challenges.admin_chals')) # TODO: Fail better

        db.session.add(challenge)
        db.session.commit()
        db.session.close()
        return redirect(url_for('admin_challenges.admin_chals'))


    ### Register stuff
    app.view_functions['admin_challenges.admin_create_chal'] = admin_create_chal
    app.view_functions['admin_challenges.admin_get_values'] = admin_get_values
    app.view_functions['admin_challenges.admin_update_chal'] = admin_update_chal

    CHALLENGE_CLASSES['ethereum'] = CTFdEthereumChallenge
    register_plugin_assets_directory(app, base_path='/plugins/ethereumctf/assets/')

