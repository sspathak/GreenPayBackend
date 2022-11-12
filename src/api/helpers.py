from src.api.firebase_utils import get_firebase_brands, get_firebase_offers, get_firebase_users


def default():
	return "If you see this, the server is up and running!!!"


def get_brands():
	return get_firebase_brands()


def get_offers():
	return get_firebase_offers()


def get_users():
	return get_firebase_users()
	