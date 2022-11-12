import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd

from time import time


def time_decorator(_fancy_print):
    def _timeit(fn):
        def wrap_fn(*args, **kwargs):
            t1 = time()
            res = fn(*args, **kwargs)
            t2 = time()
            print(f"{_fancy_print}{fn.__name__}() took {t2-t1} seconds")
            return res
        return wrap_fn
    return _timeit


def fprint(name):
    return f"[{name}]{' ' * (40 - len(name))}:"


FIREBASE_KEY_PATH = './env/greenpay-backend-firebase-key.json'
FIREBASE_DATA_URL = 'https://greenpay-backend-default-rtdb.firebaseio.com/'
cred = credentials.Certificate(FIREBASE_KEY_PATH)
app = firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATA_URL}, name='flask_x_firebase2')

fancy_print = fprint(__name__)
timeit = time_decorator(fancy_print)


def get_firebase_json():
    print(f"{fancy_print} getting firebase json...", end='')
    ref = db.reference('/', app=app)
    db_json = ref.get()
    print('done')
    return db_json


@timeit
def get_firebase_brands():
    ref = db.reference('/brands', app=app)
    db_json = ref.get()
    return db_json


@timeit
def get_firebase_offers():
    ref = db.reference('/offers', app=app)
    db_json = ref.get()
    return db_json


@timeit
def get_firebase_users():
    ref = db.reference('/users', app=app)
    db_json = ref.get()
    return db_json


def add_points_to_user(points, user):
    ref = db.reference(f'/users/{user}/points', app=app)
    db_json = ref.get()
    try:
        current_pts = int(str(db_json))
    except (TypeError, ValueError) as e:
        return f"FAILED TO UPDATE: db_json value is {db_json}"
    ref.update(current_pts+points)
    return "SUCCESS"

def compute_points(item, price):
    p = price
    if price[0] == '$':
        p = price[1:]
    try:
        pr = float(p)
    except ValueError as e:
        return -1
    return pr * 100


def add_points_firebase(user, table):
    # check if user exists
    users = get_firebase_users()
    if user not in users:
        return "FAIL"
    # check if table is valid
    if type(table) != list:
        return "FAIL"
    pts_to_add = 0
    for r in table:
        if "PRICE" not in r or 'ITEM' not in r:
            return "FAIL"
        # calculate points based on the table
        pts_to_add += compute_points(r['ITEM'], r['PRICE'])
        
    # add points to the account
    res = add_points_to_user(pts_to_add, user)
    # return success
    
    return res


def add_points_firebase_manual(user, pts):
    # check if user exists
    users = get_firebase_users()
    if user not in users:
        return "FAIL 1"
    # check if table is valid
    if type(pts) != int:
        return "FAIL 2"
    # add points to the account
    res = add_points_to_user(pts, user)
    # return success
    
    return res


def subtract_points_firebase(user, pts):
    # check if user exists
    users = get_firebase_users()
    if user not in users:
        return "FAIL"
    # check if user has enough points
    ref = db.reference(f'/users/{user}/points', app=app)
    db_json = ref.get()
    try:
        current_pts = int(str(db_json))
    except (TypeError, ValueError) as e:
        return f"FAILED TO UPDATE: db_json value is {db_json}"
    if current_pts < pts:
        return "FAILED: INSUFFICIENT POINTS"
    # subtract points
    ref.update(current_pts - pts)
    # return success
    return "SUCCESS"
    
#
# @timeit
# def get_firebase_user_swi(usr_id):
#     ref = db.reference(f'/sswip/reviews/{usr_id}', app=app)
#     u_revs = ref.get()
#     if u_revs is None:
#         raise ValueError("Invalid uID")
#     if type(u_reviews) == dict:
#         ids = [[u_rev[rid]['sID'], u_rev[rid]['val']] for rid in u_rev.keys()]
#     else:
#         ids = [[]]
#     return ids


if __name__ == "__main__":

    val = pd.DataFrame(get_firebase_brands())
    print(val)


