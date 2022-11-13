from src.api.firebase_utils import get_firebase_brands, get_firebase_offers, get_firebase_users, \
	add_points_firebase, add_points_firebase_manual, subtract_points_firebase
import json
import requests

LAMBDA_URL = "https://a65rjtjnmj.execute-api.us-east-1.amazonaws.com/default/GreenPayExtract"

def default():
	return "If you see this, the server is up and running!!!"



def get_brands(array=False):
	brands_json = get_firebase_brands()
	return [brands_json[i] for i in brands_json.keys()] if array else brands_json


def get_offers(array=False):
	offers_json = get_firebase_offers()
	return [offers_json[i] for i in offers_json.keys()] if array else offers_json


def get_users():
	return get_firebase_users()


def add_points(uid, table):
	return add_points_firebase(uid, table)


def add_points_manual(uid, pts):
	return add_points_firebase_manual(uid, int(pts))


def subtract_points(uid, pts):
	return subtract_points_firebase(uid, int(pts))


def compute_points(item, price):
	p = price
	if price[0] == '$':
		p = price[1:]
	try:
		pr = float(p)
	except ValueError as e:
		return -1
	return pr * 100


def scan_receipt(im, uid):
	# check UID exists
	if uid not in get_users():
		return "USER ID DOES NOT EXIST"
	# check im?
	# send image to lambda
	payload = json.dumps({"Image": im})
	headers = {
		'Content-Type': 'application/json'
	}
	response = requests.request("POST", LAMBDA_URL, headers=headers, data=payload)
	print(response.text)
	# do whatever calculations
	resp_json = json.loads(response.text)
	pts = compute_points(resp_json['items'])
	# get the delta
	usr = get_users()[uid]
	current_pts = usr['points']
	# update the points
	add_points_manual(uid, pts)
	# return the table and the delta
	resp_json['points_added'] = pts
	return resp_json