import psycopg2
from telegram.utils.helpers import mention_html
from config import *
import datetime
import uuid


# Formatter for displaying texts
class Formatter():
    def format_profile(self, profile: dict) -> str:
        membership = "<i>Not a member</i>"
        membership_expire = ""
        if profile["expire_date"] != None:
                dt = profile["expire_date"]
                expire_date = "{}/{}/{}".format(dt.day, dt.month, dt.year)
                membership_expire = "\n<b>Membership expire date:</b>  <i>{}</i>".format(expire_date)
        if profile["membership"] == 1:
            membership = "<i>Standard</i>"  
        elif profile["membership"] == 2:
            membership = "<i>Elite</i>"

        text = """
<u>Profile</u>

<b>ID:</b>  {}
<b>Nickname:</b>  {}
<b>Gender:</b>  {}
<b>Horoscope:</b>  {}
<b>Interest:</b>  {}
<b>Location:</b>  {}
<b>invite points:</b>  {}

<b>Conversations:</b>  {}
<b>Rate:</b>  {}/10

<b>Membership type:</b>  {} {}

""".format(profile["chat_id"], profile["nickname"], profile["gender"], profile["horoscope"], profile["interest"], profile["location"], profile["invites"], profile["conversations"], profile["rate"], membership, membership_expire)
        return text

    def format_interest_counter(self, data: dict, total_users: int) -> str:
        text = """
<u>Count of people waiting to talk</u>
"""
        interests = list_of_interests
        for interest in interests:
            for i in interest:
                text += "\n<b>{}:</b>  {} <i>people are waiting...</i>".format(i[0], data[i[0]])
        
        text += "\n" + f"Total number of users: {total_users}"

        return text

    def first_time_text(self, profile: dict) -> str:
        text = """
<u>Profile</u>

<b>Gender:</b>  {}
<b>Nickname:</b>  {}
<b>Horoscope:</b>  {}
<b>Location:</b>  {}
<b>Interest:</b>  {}

""".format(profile["gender"], profile["nickname"], profile["horoscope"], profile["location"], profile["interest"])
        return text

    def generate_merchant_order_id(self, chat_id: int) -> str:
        uid = uuid.uuid4()
        uid = str(uid)
        chat_id = str(chat_id)
        size = len(chat_id)
        x = f"{size}{chat_id}{uid}"
        return x

    def generate_link(self, chat_id: int) -> str:
        merchant_order_id = self.generate_merchant_order_id(chat_id=chat_id)
        success_url = f"https://t.me/{bot_username}?start="
        standard_link = f"https://www.yenepay.com/checkout/Home/Process/?ItemName=deposit&ItemId={chat_id}&UnitPrice={standard_price}&Quantity=1&Process=Express&ExpiresAfter=1&DeliveryFee=0&HandlingFee=0&Tax1=&Tax2=&Discount=&SuccessUrl={success_url}&IPNUrl={ipn_url}&MerchantId={merchant_id}&MerchantOrderId={merchant_order_id}"
        elite_link = f"https://www.yenepay.com/checkout/Home/Process/?ItemName=deposit&ItemId={chat_id}&UnitPrice={elite_price}&Quantity=1&Process=Express&ExpiresAfter=1&DeliveryFee=0&HandlingFee=0&Tax1=&Tax2=&Discount=&SuccessUrl={success_url}&IPNUrl={ipn_url}&MerchantId={merchant_id}&MerchantOrderId={merchant_order_id}"
        return [standard_link, elite_link]
    
    def format_users_list(self, data: list, offset: int) -> str:
        users = "No,   chat_id, memebrship, contact\n"
        for i,user in enumerate(data):
            contact = mention_html(user[0], "user")
            users += "{}:  {}    {}  {}\n".format(offset+i, user[0], user[1], contact)

        return users
    
    def format_bot_status(self, data: dict) -> str:
        text = """
<b>Users count:</b>  {}
<b>Members count:</b>  {}
<b>Waiting count:</b>  {}
<b>Chatting count:</b>  {}
<b>Male count:</b>  {}
<b>Female count:</b>  {}
""".format(data["users_count"], data["members_count"], data["waiting_count"], data["chatting_count"], data["male_count"], data["female_count"])

        return text












# Backend with postgres
class Db():
    def __init__(self, db_host: str, db_port: str, db_user: str, db_password: str, db_database: str) -> None:
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_database = db_database
    
    def change_db(self, db_host: str,  db_port: str, db_user: str, db_password: str, db_database: str) -> None:
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_password = db_password
        self.db_database = db_database

    def connect(self):
        return psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_password, database=self.db_database, sslmode="require")
   
    # Executes a query
    def run_query(self, query: str) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute(query)
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret
    
    # Executes a query and returns a single list
    def run_query_fetchone(self, query: str):
        connection = self.connect()
        cursor = connection.cursor()
        ret = []
        try:
            cursor.execute(query)
            ret = cursor.fetchone()
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret
    
    # Executes a query and returns a multiple lsit
    def run_query_fetchall(self, query: str):
        connection = self.connect()
        cursor = connection.cursor()
        ret = []
        try:
            cursor.execute(query)
            ret = cursor.fetchall()
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # check if user is registered in the db
    def is_user_registered(self, chat_id: int) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            # check if the chat_id exists
            cursor.execute("SELECT EXISTS (SELECT chat_id FROM users WHERE chat_id = {})".format(chat_id))
            results = cursor.fetchone()[0]
            if results == True:
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # check if user is registered in the db
    def is_user_admin(self, chat_id: int) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            # check if the chat_id exists
            cursor.execute("SELECT EXISTS (SELECT chat_id FROM admins WHERE chat_id = {})".format(chat_id))
            results = cursor.fetchone()[0]
            if results == True:
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # check if user is super admin
    def is_super_admin(self, chat_id: int) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            # check if the chat_id exists
            cursor.execute("SELECT EXISTS (SELECT chat_id FROM admins WHERE chat_id = {} AND super=TRUE)".format(chat_id))
            results = cursor.fetchone()[0]
            if results == True:
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # registers a user
    def register(self, chat_id: int, lang: str, gender: str) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("INSERT INTO users(chat_id, lang, gender) VALUES(%s, %s, %s)", (chat_id, lang, gender))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # returns a dictionary holding user attributes
    def get_profile_dict(self, result: list) -> dict:
        dict_obj = {
            "chat_id": result[0],
            "lang": result[1].rstrip(),
            "gender": result[2].rstrip(),
            "partner_gender": result[3].rstrip(),
            "nickname": result[4].rstrip(),
            "location": result[5].rstrip(),
            "partner_location": result[6].rstrip(),
            "horoscope": result[7].rstrip(),
            "partner_horoscope": result[8].rstrip(),
            "interest": result[9].rstrip(),
            "conversations": result[10],
            "rate": result[11],
            "invites": result[12],
            "searching_partner": result[13],
            "partner_id": result[14],
            "status": result[15].rstrip(),
            "membership": result[16],
            "start_time": result[17],
            "nickname_time": result[18],
            "expire_date": result[19],
            "last_active": result[20],
            "registered_at": result[21],
        }
        return dict_obj

    # returns a dictionary holding user attributes
    def get_user_profile(self, chat_id: int) -> dict:
        connection = self.connect()
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT chat_id, lang, gender, partner_gender, nickname, location, partner_location, horoscope, partner_horoscope, interest, conversations, rate, invites, searching_partner, partner_id, status, membership, start_time, nickname_time, expire_date, last_active, registered_at FROM users WHERE chat_id = {}".format(chat_id))
            result = cursor.fetchone()
            ret = self.get_profile_dict(result)
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret
    
    # changes the location of a user
    def change_location(self, chat_id: int, location: str) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE users SET location='{}' WHERE chat_id={}".format(location, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # changes the interest of a user
    def change_interest(self, chat_id: int, interest: str) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE users SET interest='{}' WHERE chat_id={}".format(interest, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # starts a new conversation
    def start_conv(self, chat_id: int) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            profile = self.get_user_profile(chat_id=chat_id)
            if not profile["searching_partner"] and profile["partner_id"] == -1:
                d = datetime.datetime.now()
                cursor.execute("UPDATE users SET searching_partner=TRUE, start_time='{}' WHERE chat_id={}".format(d, chat_id))
                connection.commit()
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # pairs a user with another random chat finder
    def pair_user(self, chat_id: int) -> int:
        # Try to pair a user with a member first if no member found, pair it with any user
        connection = self.connect()
        cursor = connection.cursor()
        ret = -1
        try:
            profile = self.get_user_profile(chat_id=chat_id)
            if profile["searching_partner"]:
                # Check if an active user with the same chatting interest exists
                # If True pair them and return partner_id, if False return -1
                if profile["membership"] >= 1:
                    gender_filter_membership = ""
                    gender_filter_all = ""
                    if profile["partner_gender"] != "None":
                        gender_filter_membership = "and gender='{}' and (partner_gender='{}' or partner_gender='None')".format(profile["partner_gender"], profile["gender"])
                        gender_filter_all = "and gender='{}'".format(profile["partner_gender"])
                    query_membership = "SELECT chat_id FROM users WHERE searching_partner=TRUE and interest='{}' and chat_id!={} and membership>=1 {} ORDER BY start_time".format(profile["interest"], chat_id, gender_filter_membership)
                    query_all = "SELECT chat_id FROM users WHERE searching_partner=TRUE and interest='{}' and chat_id!={}  and membership=0 {} ORDER BY start_time".format(profile["interest"], chat_id, gender_filter_all)
                    cursor.execute(query_membership)
                    partner_id = cursor.fetchone()
                    if partner_id != None:
                        partner_id = partner_id[0]
                        cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(partner_id, chat_id))
                        cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(chat_id, partner_id))
                        connection.commit()
                        ret = partner_id             
                    else:
                        cursor.execute(query_all)
                        partner_id = cursor.fetchone()
                        if partner_id != None:
                            partner_id = partner_id[0]
                            cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(partner_id, chat_id))
                            cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(chat_id, partner_id))
                            connection.commit()
                            ret = partner_id
                else:
                    cursor.execute("SELECT chat_id FROM users WHERE searching_partner=TRUE and interest='{}' and chat_id!={} and (partner_gender='{}' or partner_gender='None') and membership>=1 ORDER BY start_time".format(profile["interest"], chat_id, profile["gender"]))
                    partner_id = cursor.fetchone()
                    if partner_id != None:
                        partner_id = partner_id[0]
                        cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(partner_id, chat_id))
                        cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(chat_id, partner_id))
                        connection.commit()
                        ret = partner_id             
                    else:
                        cursor.execute("SELECT chat_id FROM users WHERE searching_partner=TRUE and interest='{}' and chat_id!={} and membership=0 ORDER BY start_time".format(profile["interest"], chat_id))
                        partner_id = cursor.fetchone()
                        if partner_id != None:
                            partner_id = partner_id[0]
                            cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(partner_id, chat_id))
                            cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(chat_id, partner_id))
                            connection.commit()
                            ret = partner_id 
                        # elif profile["interest"] == "Anything":
                        #     cursor.execute("SELECT chat_id FROM users WHERE searching_partner=TRUE and chat_id!={} ORDER BY start_time".format(chat_id))
                        #     partner_id = cursor.fetchone()
                        #     if partner_id != None:
                        #         partner_id = partner_id[0]
                        #         cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(partner_id, chat_id))
                        #         cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id={} WHERE chat_id={}".format(chat_id, partner_id))
                        #         connection.commit()
                        #         ret = partner_id


        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # ends a conversation 
    def end_conv(self, chat_id: int) -> bool:
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            profile = self.get_user_profile(chat_id=chat_id)
            if not profile["searching_partner"] and profile["partner_id"] != -1:
                partner_profile = self.get_user_profile(chat_id=profile["partner_id"])
                rate = round((profile["rate"] + default_rate)/(profile["conversations"] + 1), 1)
                partner_rate = round((partner_profile["rate"] + default_rate)/(partner_profile["conversations"] + 1), 1)
                cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id=-1, conversations=conversations+1, rate={} WHERE chat_id={}".format(rate, chat_id))
                cursor.execute("UPDATE users SET searching_partner=FALSE, partner_id=-1, conversations=conversations+1, rate={}  WHERE chat_id={}".format(partner_rate, profile["partner_id"]))
                connection.commit()
                ret = True
            elif profile["searching_partner"]:
                cursor.execute("UPDATE users SET searching_partner=FALSE WHERE chat_id={}".format(chat_id))
                connection.commit()
                ret = False
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # checks if a user can change nickname
    def can_change_nickname(self, profile: dict) -> bool:
        # see if users nickname is none if None - return True
        # see if last nickname change was 7 days ago if True - return True
        # return False if both are false 
        try:
            if profile["nickname_time"] == None:
                return True
            else:
                ret = datetime.datetime.now() - profile["nickname_time"]
                if ret.days >= 7:
                    return True
            return False
        except Exception as e:
            return False

    # changes nickname of a user
    def change_nickname(self, chat_id: int, nickname: str) -> bool:
        # gets todays date, updates nickname and updates nickname_time, return True if all goes alright
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            today = datetime.datetime.now()
            today = today.__str__()
            cursor.execute("UPDATE users SET nickname='{}', nickname_time='{}' WHERE chat_id={}".format(nickname, today, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # returns remaining days for changing nickname
    def get_change_nickname_remaining_days(self, profile: dict) -> int:
        # compute remaining days, then return
        ret = datetime.datetime.now() - profile["nickname_time"]
        return 7 - ret.days

    # returns interest count of users 
    def get_interest_counter(self) -> dict:
        # gets todays date, updates nickname and updates nickname_time, return True if all goes alright
        connection = self.connect()
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT interest,count(*) FROM users WHERE searching_partner=TRUE GROUP BY interest")
            rows = cursor.fetchall()
            interest_dict = {}
            for interest in list_of_interests:
                for i in interest:
                    interest_dict[i[0]] = 0

            if rows != None:
                for row in rows:
                    interest_dict[row[0]] = row[1]
            ret = interest_dict
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # rates a user
    def rate(self, profile: dict, rate: int) -> bool:
        # computes rate for a user and updates the rate
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            old_rate = profile["rate"]
            conversations = profile["conversations"]
            new_rate = ((old_rate * conversations) - default_rate + rate)/conversations
            rate = round(new_rate, 1)
            cursor.execute("UPDATE users SET rate={} WHERE chat_id={}".format(rate, profile["chat_id"]))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    def get_expire_date(self, dt, member_type) -> datetime.datetime:
        now = datetime.datetime.now()
        ex_days = 7
        if member_type == 2:
            ex_days = 30
        elif member_type == -1:
            ex_days = 1
        if dt != None:
            if dt > now:
                new_dt = dt - now
                ex_days = new_dt.days + ex_days
            else:
                pass
        else:
            pass
        expire_date = now + datetime.timedelta(days=ex_days)
        return expire_date

    # upgrades a membership and returns an int(membership type)
    def upgrade_membership(self, chat_id: int, price: float) -> int:
        connection = self.connect()
        cursor = connection.cursor()
        ret = 0
        try:
            if price >= invite_price:
                profile = self.get_user_profile(chat_id=chat_id)
                if price == standard_price:
                    expire_date = self.get_expire_date(profile["expire_date"], 1)
                    cursor.execute("UPDATE users SET membership={}, expire_date='{}' WHERE chat_id={}".format(1, expire_date, chat_id))
                    connection.commit()
                    ret = 1
                elif price == elite_price:
                    expire_date = self.get_expire_date(profile["expire_date"], 2)
                    cursor.execute("UPDATE users SET membership={}, expire_date='{}' WHERE chat_id={}".format(2, expire_date, chat_id))
                    connection.commit()
                    ret = 2
                elif price == invite_price:
                    expire_date = self.get_expire_date(profile["expire_date"], -1)
                    cursor.execute("UPDATE users SET membership={}, expire_date='{}' WHERE chat_id={}".format(1, expire_date, chat_id))
                    connection.commit()
                    ret = 1
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # adds invite point
    def add_invite_point(self, chat_id: int) -> bool:
        # adds invite point to a user and checks he/she invited [invite_upgrade] memebers
        # if True - returns True
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE users SET invites=invites+1 WHERE chat_id={}".format(chat_id))
            connection.commit()
            profile = self.get_user_profile(chat_id=chat_id)
            if profile["invites"] == invite_upgrade:
                if self.upgrade_membership(chat_id=chat_id, price=invite_price) >= 1:
                    ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # changes partner gender
    def change_gender_filter(self, chat_id: int, gender: str) -> bool:
        # Check if the user is eligiable to access this feature, if True - change partner gender
        connection = self.connect()
        cursor = connection.cursor()
        ret = False
        try:
            profile = self.get_user_profile(chat_id=chat_id)
            if profile["membership"] >= 1:
                cursor.execute("UPDATE users SET partner_gender='{}' WHERE chat_id={}".format(gender, chat_id))
                connection.commit()
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # Retutns users list (limited by 100 users)
    def get_users(self, status: str, offset: int, limit: int) -> list:
        connection = self.connect()
        cursor = connection.cursor()
        ret = []
        try:
            cursor.execute("SELECT chat_id, membership FROM users WHERE status=%s LIMIT %s OFFSET %s", (status, limit, offset))
            users = cursor.fetchall()
            if users != None:
                ret = users
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # Retutns bot status
    def get_bot_status(self) -> dict:
        connection = self.connect()
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT COUNT(*) FROM users")
            users_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users WHERE membership>=1")
            members_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users WHERE searching_partner=TRUE")
            waiting_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users WHERE partner_id != (-1)")
            chatting_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users WHERE gender='Male'")
            male_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users WHERE gender='Female'")
            female_count = cursor.fetchone()[0]
            ret = {
                "users_count": users_count,
                "members_count": members_count,
                "waiting_count": waiting_count,
                "chatting_count": chatting_count,
                "male_count": male_count,
                "female_count": female_count,
            }
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret