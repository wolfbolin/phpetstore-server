from pdbc import PDBC
from flask import Flask, render_template, redirect, url_for, jsonify, request

db = PDBC.open_db()
web = Flask(__name__)


@web.route('/api/get_class')
def get_class():
    data = PDBC.get_class(db)
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


@web.route('/api/get_list/<cid>')
def get_list(cid):
    data = PDBC.get_list(db, cid)
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


@web.route('/api/get_order/<uid>')
def get_order(uid):
    data = PDBC.get_order(db, uid)
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


@web.route('/api/get_animal/<pid>')
def get_animal(pid):
    data = PDBC.get_animal(db, pid)
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


@web.route('/api/get_user/<uid>')
def get_user(uid):
    data = PDBC.get_user(db, uid)
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


@web.route('/api/login', methods=['POST'])
def login():
    username = request.form.get('username').strip()
    password = request.form.get('password').strip()
    uid = PDBC.login(db, username, password)
    data = {
        'result': '',
        'uid': uid
    }
    if uid != -1:
        data['result'] = 'success'
    else:
        data['result'] = 'error'
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


@web.route('/api/pick_pet', methods=['POST'])
def pick():
    data = {
        'result': 'error'
    }
    uid = request.form.get('uid').strip()
    order = request.form.getlist('list[]')
    for item in order:
        if int(uid) <= 0 or len(order) < 1:
            data['result'] = 'error'
        else:
            result = PDBC.pick_pet(db, uid, order)
            data['result'] = result
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


@web.route('/api/sure_user', methods=['POST'])
def sure_user():
    data = [request.form.get('user_name').strip(),
            request.form.get('user_phone').strip(),
            request.form.get('province').strip(),
            request.form.get('area').strip(),
            request.form.get('city').strip(),
            request.form.get('user_address').strip()]
    data = PDBC.sure_user(db, request.form.get('uid').strip(), data)
    data = jsonify(data)
    data.headers['Access-Control-Allow-Origin'] = '*'
    return data


if __name__ == '__main__':
    web.run()
