import psycopg2
from config import *
import datetime
import uuid



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
            if price >= standard_price:
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