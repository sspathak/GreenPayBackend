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

@api.route('/get_brands', methods=['GET'])
def get_offers():
    try:
        ret = helpers.get_offers()
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)

@api.route('/get_users', methods=['GET'])
def get_brands():
    try:
        ret = helpers.get_users()
    except Exception as e:
        return jsonify(f"Error code AP01: {e}")
    return jsonify(ret)