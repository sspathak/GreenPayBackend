from src.api.firebase_utils import get_firebase_brands, get_firebase_offers, get_firebase_users, \
	add_points_firebase, add_points_firebase_manual, subtract_points_firebase


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