import datetime
import requests
# t = "2021-03-5 14:25:47.511913+03"

# dt = datetime.datetime.strptime("2021-03-19 14:25:47.511913", '%Y-%m-%d %H:%M:%S.%f')
# now = datetime.datetime.now()

# print(now)

ret = requests.post("https://ipnethiovoicechat.herokuapp.com/webhook")
print(ret)