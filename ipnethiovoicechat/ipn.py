from flask import Flask, request, Response
import requests, os
from backend import Db
from config import *
from lang_dict import *
import urllib

db = Db(db_host, db_port, db_user, db_password, db_database)

class IPN():
    def __init__(self):
        self.headers = {"Content-Type": "application/json"}

    def get_dict_of_req(self, text: str) -> dict:
        dc = urllib.parse.parse_qs(text)
        return dc

    def change_to_json(self, data: dict) -> dict:
        ret = {
            "TotalAmount":data["TotalAmount"][0],
            "BuyerId":data["BuyerId"][0],
            "MerchantOrderId":data["MerchantOrderId"][0],
            "MerchantCode":data["MerchantCode"][0],
            "MerchantId":data["MerchantId"][0],
            "TransactionCode":data["TransactionCode"][0],
            "TransactionId":data["TransactionId"][0],
            "Status":data["Status"][0],
            "Currency":data["Currency"][0],
            "Signature":data["Signature"][0]
        }
        return ret

    def check_ipn(self, data: dict) -> bool:
        if int(data["MerchantCode"]) == merchant_id:
            ret = requests.post(url="https://endpoints.yenepay.com/api/verify/ipn/", json=data, headers=self.headers)
            if ret.text == "VERIFIED":
                return True
        return False

    def get_chat_id(self, text: str) -> int:
        if int(text[0]) != 1:
            size = int(text[0])
            chat_id = int(text[1 : size + 1]) 
        else:
            size = int(text[0 : 2])
            chat_id = int(text[2 : size + 2]) 
        return chat_id


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
        member_type = db.upgrade_membership(chat_id=chat_id, price=int(price))
        if member_type > 0:
            profile = db.get_user_profile(chat_id=chat_id)
            formatted_text = text_membership_upgraded(profile=profile)[profile["lang"]]
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={formatted_text}&parse_mode=HTML"
            ret = requests.get(url)
            user_html = f"<a href='tg://user?id={chat_id}'>user</a>"
            membership = "Standard"
            if profile["membership"] == 2:
                membership = "Elite"
            admin_text = f"🔔 <b>NOTOFICATION</b>\n\nThis {user_html} with chat_id:{chat_id}, has upgraded their membership to <b>{membership}</b>"
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={admin_chat_id}&text={admin_text}&parse_mode=HTML"
            ret = requests.get(url)
    else:
        Response(status=500)
    return Response(status=200)



if __name__ == "__main__":
    app.run(debug=False)