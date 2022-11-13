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
def get_firebase_rewards():
    ref = db.reference('/rewards', app=app)
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
        current_pts = int(float(str(db_json)))
    except (TypeError, ValueError) as e:
        return f"FAILED TO UPDATE: db_json value is {db_json}"
    
    ref.set(current_pts+points)
    return current_pts+points


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
    
    return pts_to_add


def add_points_firebase_manual(user, pts):
    # check if user exists
    try:
        users = get_firebase_users()
    except Exception as e:
        return "FAIL 0.9"
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
        return "FAILED to subtract points"
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
    d = {"items": [{"PRODUCT_CODE": "007874221044", "ITEM": "GV PREM 18MR", "PRICE": "14.82",
                "EXPENSE_ROW": "GV PREM 18MR 007874221044 14.82 X"},
               {"PRODUCT_CODE": "008180640960", "ITEM": "BED IN n BAG", "PRICE": "34.96",
                "EXPENSE_ROW": "BED IN n BAG 008180640960 34.96 X"},
               {"PRODUCT_CODE": "002700041924", "ITEM": "SNPK Fl LLVR", "PRICE": "3.27",
                "EXPENSE_ROW": "SNPK Fl LLVR 002700041924 F 3.27 0"},
               {"PRODUCT_CODE": "005210004973", "ITEM": "PP ITALIAN", "PRICE": "3.30",
                "EXPENSE_ROW": "PP ITALIAN 005210004973 F 3.30 0"},
               {"PRODUCT_CODE": "007766133596", "ITEM": "SPICE", "PRICE": "4.80",
                "EXPENSE_ROW": "SPICE 007766133596 F 4.80 0"},
               {"PRODUCT_CODE": "005100011215", "ITEM": "PORK N BEANS", "PRICE": "0.86",
                "EXPENSE_ROW": "PORK N BEANS 005100011215 F 0.86 0"},
               {"PRODUCT_CODE": "002700044205", "ITEM": "MANWICH", "PRICE": "1.26",
                "EXPENSE_ROW": "MANWICH 002700044205 F 1.26 0"},
               {"PRODUCT_CODE": "001800013863", "ITEM": "PRG PIZZA", "PRICE": "1.96",
                "EXPENSE_ROW": "PRG PIZZA 001800013863 F 1.96 0"},
               {"PRODUCT_CODE": "003760013878", "ITEM": "CHILI W/BEAN", "PRICE": "3.00",
                "EXPENSE_ROW": "CHILI W/BEAN 003760013878 F 3.00 0"},
               {"PRODUCT_CODE": "007074235324", "ITEM": "PREP PROD CH", "PRICE": "1.98",
                "EXPENSE_ROW": "PREP PROD CH 007074235324 F 1.98 i)"},
               {"PRODUCT_CODE": "007874237047", "ITEM": "CREAM CHEESE", "PRICE": "1.68",
                "EXPENSE_ROW": "CREAM CHEESE 007874237047 F 1.68 0"},
               {"PRODUCT_CODE": "007218056652", "ITEM": "SANDWICH", "PRICE": "3.34",
                "EXPENSE_ROW": "SANDWICH 007218056652 F 3.34 0"},
               {"PRODUCT_CODE": "007874214710", "ITEM": "GVORGCHICKEN", "PRICE": "1.94",
                "EXPENSE_ROW": "GVORGCHICKEN 007874214710 F 1.94 0"},
               {"PRODUCT_CODE": "002400024423", "ITEM": "PCH CHIA", "PRICE": "2.78",
                "EXPENSE_ROW": "PCH CHIA 002400024423 F 2.78 0"},
               {"PRODUCT_CODE": "007874223292", "ITEM": "BREAD BUTTER", "PRICE": "1.97",
                "EXPENSE_ROW": "BREAD BUTTER 007874223292 F 1.97 N"},
               {"PRODUCT_CODE": "078113881115", "ITEM": "OTB 15.25 JA", "PRICE": "3.44",
                "EXPENSE_ROW": "OTB 15.25 JA 078113881115 F 3.44 H"},
               {"PRODUCT_CODE": "004973395011", "ITEM": "HOT SAUCE", "PRICE": "3.18",
                "EXPENSE_ROW": "HOT SAUCE 004973395011 F 3.18 0"},
               {"PRODUCT_CODE": "002620014010", "ITEM": "SJ SMKD DEL", "PRICE": "2.54",
                "EXPENSE_ROW": "SJ SMKD DEL 002620014010 F 2.54 N"},
               {"PRODUCT_CODE": "002840051799", "ITEM": "TOSTITO RSTC", "PRICE": "3.50",
                "EXPENSE_ROW": "TOSTITO RSTC 002840051799 F 3.50 0"},
               {"PRODUCT_CODE": "004190007323", "ITEM": "1 MILK", "PRICE": "2.16",
                "EXPENSE_ROW": "1 MILK 004190007323 F 2.16 0"}],
     "metadata": [{"ADDRESS": "413-586-4231 Mgr ANGELA\n337 RUSSELL ST\nHADLEY MA 01035"}, {"STREET": "337 RUSSELL ST"},
                  {"CITY": "HADLEY"}, {"STATE": "MA"}, {"ZIP_CODE": "01035"},
                  {"ADDRESS_BLOCK": "337 RUSSELL ST\nHADLEY MA 01035"}, {"NAME": "Walmarl:"}, {"NAME": "Walmart+"},
                  {"AMOUNT_PAID": "99.85"}, {"INVOICE_RECEIPT_DATE": "09/16/22"}, {"INVOICE_RECEIPT_DATE": "09/16/22"},
                  {"INVOICE_RECEIPT_ID": "01139"}, {"SUBTOTAL": "96.74"}, {"TAX": "3.11"}, {"TOTAL": "99.05"},
                  {"VENDOR_ADDRESS": "413-586-4231 Mgr ANGELA\n337 RUSSELL ST\nHADLEY MA 01035"},
                  {"VENDOR_NAME": "Walmarl:"}, {"VENDOR_NAME": "Walmart+"}, {"VENDOR_URL": "survey.walmart.com"},
                  {"OTHER": "7RGZP8Y1N0M"}, {"OTHER": "ANGELA"}, {"OTHER": "02683"}, {"OTHER": "000252"},
                  {"OTHER": "03"}, {"OTHER": "6.250"}, {"OTHER": "SU2CEP"}, {"OTHER": "1042000314"},
                  {"OTHER": "A0000000041010"}, {"OTHER": "2573548908906E35"}, {"OTHER": "n SC010906"},
                  {"OTHER": "0.00"}, {"OTHER": "20"}]}
    
    val = add_points_firebase('user1', d["items"])
    print(val)


