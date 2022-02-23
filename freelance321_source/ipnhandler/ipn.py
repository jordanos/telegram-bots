from flask import Flask, request, Response
import requests, os
from backend import Db, Formatter, IPN
from config import *
from lang_dict import *

db = Db(db_host, db_port, db_user, db_password, db_database)
fm = Formatter()
ip = IPN()

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def respond():
    text = request.get_data().decode("utf-8")
    ipn = ip.get_dict_of_req(text)
    js = ip.change_to_json(ipn)
    if ip.check_ipn(js):
        chat_id = ip.get_chat_id(js["MerchantOrderId"])
        price = float(js["TotalAmount"])
        bot = db.get_bot_profile()
        cut = bot["yenepay_cut"]/100
        price = price - (price * cut)
        price = round(price, 1)
        if db.create_deposit(chat_id=chat_id, price=price, paid=True):
            user = db.get_user_profile(chat_id)
            formatted_text = fm.alert_message(text_balance_updated_plus(user=user, price=price)[user["lang"]])
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={formatted_text}&parse_mode=HTML"
            ret = requests.get(url)
    else:
        Response(status=500)
    return Response(status=200)



if __name__ == "__main__":
    app.run(debug=False)