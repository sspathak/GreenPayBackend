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
