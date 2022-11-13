from flask import Blueprint, jsonify, request, render_template
from src.api import helpers
import json

api = Blueprint('api', __name__)
ERROR_MESSAGE = "There seems to have been an error in processing your request :("


@api.route('/', methods=['GET'])
def default():
    try:
        ret = helpers.default()
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)


@api.route("/home", methods=['GET'])
def home():
    try:
        brands = helpers.get_brands(array=True)
        offers = helpers.get_offers(array=True)
        users = helpers.get_users()
        ret_json = {
            "brands": brands,
            "offers": offers,
            "users": users
        }
    except Exception as e:
        return "This is awkward... the server seems to be busy. Please try again in a few minutes"
    return jsonify(ret_json)

    

@api.route('/get_brands', methods=['GET'])
def get_brands():
    try:
        ret = helpers.get_brands()
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)

@api.route('/get_offers', methods=['GET'])
def get_offers():
    try:
        ret = helpers.get_offers()
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)

@api.route('/get_users', methods=['GET'])
def get_users():
    try:
        ret = helpers.get_users()
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)


@api.route('/get_rewards', methods=['GET'])
def get_rewards():
    try:
        ret = helpers.get_rewards(array=True)
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)


@api.route('/add_points', methods=['POST'])
def add_points():
    request_json = json.loads(request.data)
    try:
        uid = request_json['userID']
    except KeyError:
        return jsonify("userID key not provided in request data")
    try:
        table = request_json['table']
    except KeyError:
        return jsonify("table key not provided in request data")
    try:
        ret = helpers.add_points(uid, table)
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)


@api.route('/add_points_manual', methods=['POST'])
def add_points_manual():
    request_json = json.loads(request.data)
    try:
        uid = request_json['userID']
    except KeyError:
        return jsonify("userID key not provided in request data")
    try:
        pts = request_json['points']
    except KeyError:
        return jsonify("points key not provided in request data")
    try:
        ret = helpers.add_points_manual(uid, pts)
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)


@api.route('/redeem', methods=['POST'])
def subtract_points():
    request_json = json.loads(request.data)
    try:
        uid = request_json['userID']
    except KeyError:
        return jsonify("userID key not provided in request data")
    try:
        r_id = request_json['rewardID']
        cost = helpers.get_rewards()[r_id]['cost']
    except (KeyError, TypeError) as e:
        return jsonify(f"points key not provided in request data : '{request_json}': {str(e)}")
    try:
        ret = helpers.subtract_points(uid, cost)
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)



@api.route("/scan", methods=['POST'])
def scan_receipt():
    request_json = json.loads(request.data)
    try:
        im = request_json['Image']
    except KeyError:
        return jsonify("'Image' key not provided in request data")
    try:
        uid = request_json['userID']
    except KeyError:
        return jsonify("'userID' key not provided in request data")
    try:
        ret = helpers.scan_receipt(im, uid)
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)
