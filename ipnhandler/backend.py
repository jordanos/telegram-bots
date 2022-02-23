import psycopg2
import uuid, urllib, requests
from config import *


# IPN helper
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



# Text formatter

class Formatter():
    def alert_message(self, text: str) -> str:

        formatted_text = """
<b>Notification</b>

{}
        """.format(text)
        return formatted_text
    





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

    # Executes a query
    def run_query(self, query: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_password, database=self.db_database)
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
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_password, database=self.db_database)
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
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_password, database=self.db_database)
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
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_password, database=self.db_database)
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
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_password, database=self.db_database)
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
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user, password=self.db_password, database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            # check if the chat_id exists
            cursor.execute("SELECT EXISTS (SELECT chat_id FROM admins WHERE chat_id = {} and super=true)".format(chat_id))
            results = cursor.fetchone()[0]
            if results == True:
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    def register(self, chat_id: int, phone_number: str, first_name: str, username: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("INSERT INTO users(chat_id,phone_number,first_name,username) VALUES(%s,%s,%s,%s)", (chat_id, phone_number, first_name, username))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    def get_user_profile(self, chat_id: int) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            # check if the chat_id exists
            cursor.execute("SELECT chat_id, phone_number, first_name, username, balance, money_made, company, verified, lang, coin, jobs_completed, jobs_posted, rate, level, status FROM users WHERE chat_id = {}".format(chat_id))
            sql = cursor.fetchone()
            if sql == None or len(sql) == 0:
                ret = {}
            else:
                username = "unknown"
                first_name = "unknown"
                if sql[3] != None:
                    username = sql[3].rstrip()                  
                if sql[2] != None:
                    first_name = sql[2].rstrip()
                    
                ret = {
                    "chat_id": sql[0],
                    "phone_number": sql[1],
                    "first_name": first_name,
                    "username": username,
                    "balance": sql[4],
                    "money_made": sql[5],
                    "company": sql[6].rstrip(),
                    "verified": sql[7],
                    "lang": sql[8].rstrip(),
                    "coin": sql[9], 
                    "jobs_completed": sql[10],
                    "jobs_posted": sql[11],
                    "rate": sql[12],
                    "level": sql[13],
                    "status": sql[14].rstrip(),
                }
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # Gets user profile data usering username
    def get_user_profile_by_username(self, username: str) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            # check if the chat_id exists
            cursor.execute("SELECT chat_id, phone_number, first_name, username, balance, money_made, company, verified, lang, coin, jobs_completed, jobs_posted, rate, level, status FROM users WHERE LOWER(username) = LOWER('{}') ".format(username))
            sql = cursor.fetchone()
            if sql == None or len(sql) == 0:
                ret = {}
            else:
                username = "unknown"
                first_name = "unknown"
                if sql[3] != None:
                    username = sql[3].rstrip()                  
                if sql[2] != None:
                    first_name = sql[2].rstrip()
                    
                ret = {
                    "chat_id": sql[0],
                    "phone_number": sql[1],
                    "first_name": first_name,
                    "username": username,
                    "balance": sql[4],
                    "money_made": sql[5],
                    "company": sql[6].rstrip(),
                    "verified": sql[7],
                    "lang": sql[8].rstrip(),
                    "coin": sql[9], 
                    "jobs_completed": sql[10],
                    "jobs_posted": sql[11],
                    "rate": sql[12],
                    "level": sql[13],
                    "status": sql[14].rstrip(),
                }
        except Exception as e:
            print(e)
        finally:
            connection.close()
        return ret
    
    # Retutns users list (limited by 100 users)
    def get_users(self, status: str, offset: int, limit: int) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = []
        try:
            cursor.execute("SELECT chat_id, username FROM users WHERE status=%s LIMIT %s OFFSET %s", (status, limit, offset))
            users = cursor.fetchall()
            if users != None:
                ret = users
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret
        
    # Retutns users list (with job count)
    def get_users_with_job(self, jobs_posted: int, offset: int, limit: int) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = []
        try:
            cursor.execute("SELECT chat_id, username FROM users WHERE jobs_posted>=%s LIMIT %s OFFSET %s", (jobs_posted, limit, offset))
            users = cursor.fetchall()
            if users != None:
                ret = users
        except Exception as e:
            print(e)
        finally:
            connection.close()

        return ret

    def get_bot_profile(self) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            # check if the chat_id exists
            cursor.execute("SELECT bot, channel, s_channel, p_channel, s_admin, s_group, check_level, job_coin, proposal_coin, application_fee, minimum_deposit, maximum_deposit, minimum_cashout, maximum_cashout, yenepay_cut, merchant_id FROM bot")
            sql = cursor.fetchone()
            if sql == None or len(sql) == 0:
                ret = {}
            else:
                ret = {
                    "bot": sql[0].rstrip(),
                    "channel": sql[1].rstrip(),
                    "s_channel": sql[2].rstrip(),
                    "p_channel": sql[3].rstrip(),
                    "s_admin": sql[4].rstrip(),
                    "s_group": sql[5].rstrip(),
                    "check_level": sql[6],
                    "job_coin": sql[7],
                    "proposal_coin": sql[8],
                    "application_fee": sql[9],
                    "minimum_deposit": sql[10],
                    "maximum_deposit": sql[11],
                    "minimum_cashout": sql[12],
                    "maximum_cashout": sql[13],
                    "yenepay_cut": sql[14],
                    "merchant_id": sql[15],
                }
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # adds admin 
    def add_admin(self, chat_id: int, super: bool=False) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT * FROM users WHERE chat_id={} and status='active'".format(chat_id))
            user = cursor.fetchone()
            if user != None:
                if super:
                    cursor.execute("INSERT INTO admins(chat_id, super) VALUES(%s,TRUE)", (chat_id))
                else:
                    cursor.execute("INSERT INTO admins(chat_id) VALUES({})".format(chat_id))
                connection.commit()
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret
    
    # Retutns admins list
    def get_admins(self) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = []
        try:
            cursor.execute("SELECT chat_id, super FROM admins")
            admins = cursor.fetchall()
            if admins != None:
                ret = admins
        finally:
            connection.close()

        return ret

    # adds a job into a job queue
    def add_job(self, chat_id: int, text: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT job_id FROM jobs WHERE chat_id={} and status='edit'".format(chat_id))
            job_id = cursor.fetchone()
            if job_id != None:
                cursor.execute("UPDATE jobs SET title=%s WHERE job_id=%s", (text, job_id[0]))
            else:
                cursor.execute("INSERT INTO jobs(chat_id, title, status) VALUES(%s, %s, 'edit')", (chat_id, text))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    def add_job_company(self, chat_id: int, text: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            
            cursor.execute("UPDATE jobs SET company=%s WHERE chat_id=%s and status='edit'", (text, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # adds a job discription into a job
    def add_job_discription(self, chat_id: int, text: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE jobs SET discription=%s WHERE chat_id=%s and status='edit'", (text, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret
    
    # adds a job type into a job
    def add_job_type(self, chat_id: int, text: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE jobs SET type=%s WHERE chat_id=%s and status='edit'", (text, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # adds a job category into a job
    def add_job_cat(self, chat_id: int, text: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE jobs SET cat=%s WHERE chat_id=%s and status='edit'", (text, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # adds a job level into a job
    def add_job_level(self, chat_id: int, level: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE jobs SET level=%s WHERE chat_id=%s and status='edit'", (level, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # adds a job proposals limit into a job
    def add_job_limit(self, chat_id: int, limit: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE jobs SET proposal_limit=%s WHERE chat_id=%s and status='edit'", (limit, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # adds a job price into a job
    def add_job_price(self, chat_id: int, price: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE jobs SET price=%s WHERE chat_id=%s and status='edit'", (price, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # checks if the user has enough balance to deposit
    def check_job_price(self, chat_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT price FROM jobs WHERE chat_id={} and status='edit'".format(chat_id))
            price = cursor.fetchone()
            if price != None:
                cursor.execute("SELECT balance FROM users WHERE chat_id={}".format(chat_id))
                balance = cursor.fetchone()
                if balance != None:
                    if balance[0] >= price[0]:
                        ret = True
        except Exception as e:
            price(e)
        finally:
            connection.close()
        
        return ret

    # checks if the user has enough balance and makes a deposit
    def job_deposit(self, chat_id: int, job_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT price FROM jobs WHERE job_id={}".format(job_id))
            price = cursor.fetchone()
            if price != None:
                cursor.execute("SELECT balance FROM users WHERE chat_id={}".format(chat_id))
                balance = cursor.fetchone()
                if balance != None:
                    if balance[0] >= price[0]:
                        cursor.execute("UPDATE jobs SET deposit=true WHERE job_id={}".format(job_id))
                        cursor.execute("UPDATE users SET balance=balance-{} WHERE chat_id={}".format(price[0], chat_id))
                        connection.commit()
                        ret = True
        except Exception as e:
            print(e)
        finally:
            connection.close()
        
        return ret

    # Accepts list of job attributes and returns a dictionary
    def get_job_dict(self, data: list) -> dict:
        ret = {
            "job_id": data[0],
            "chat_id": data[1],
            "title": data[2].rstrip(),
            "company": data[3].rstrip(),
            "discription": data[4].rstrip(),
            "cat": data[5].rstrip(),
            "type": data[6].rstrip(),
            "deposit": data[7],
            "price": data[8],
            "level": data[9],
            "coin": data[10],
            "freelancer": data[11],
            "status": data[12].rstrip(),
            "message_id": data[13],
            "proposal_limit": data[14],
            "counter": data[15],
            "counter_f": data[16],
        }

        return ret

    # Accepts chat_id and status for searching the database and returns an empty dictionary or a dictionary containing job attributes    
    def get_job_with_chat_id(self, chat_id: int, status: str) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT job_id, chat_id, title, company, discription, cat, type, deposit, price, level, coin, freelancer, status, message_id, proposal_limit, counter, counter_f FROM jobs WHERE chat_id=%s and status=%s", (chat_id, status))
            ret = cursor.fetchone()
            if ret == None:
                ret = {}
            else:
                ret = self.get_job_dict(ret)
            
        except Exception as e:
            print(e)
        finally:
            connection.close()
        
        return ret
    
    # Accepts job id for searching the database and returns an empty dictionary or a dictionary containing job attributes
    def get_job_with_id(self, job_id: int) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT job_id, chat_id, title, company, discription, cat, type, deposit, price, level, coin, freelancer, status, message_id, proposal_limit, counter, counter_f FROM jobs WHERE job_id={}".format(job_id))
            ret = cursor.fetchone()
            if ret == None:
                ret = {}
            else:
                ret = self.get_job_dict(ret)         
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # Accepts job status for searching the database and returns an empty list or a list(max length 5) containing jobs dictionary
    def get_jobs_with_status(self, status: str) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ls = []
        try:
            cursor.execute("SELECT job_id, chat_id, title, company, discription, cat, type, deposit, price, level, coin, freelancer, status, message_id, proposal_limit, counter, counter_f FROM jobs WHERE status='{}' ORDER BY job_id ASC LIMIT 5".format(status))
            jobs = cursor.fetchall()
            if jobs == None:
                ls = []
            else:
                for job in jobs:
                    ls.append(self.get_job_dict(job))            
        except Exception as e:
            pass
        finally:
            connection.close()

        return ls

    # Returns a list of opened jobs
    def get_job_with_status(self, chat_id: int, status: str) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ls = []
        try:
            cursor.execute("SELECT job_id, chat_id, title, company, discription, cat, type, deposit, price, level, coin, freelancer, status, message_id, proposal_limit, counter, counter_f FROM jobs WHERE chat_id={} and status='{}'".format(chat_id, status))
            jobs = cursor.fetchall()
            if jobs == None:
                ls = []
            else:
                for ret in jobs:
                    ret = self.get_job_dict(ret)
                    ls.append(ret)  

        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ls

    # Submits a job
    def submit_job(self, chat_id: int, job_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            bot = self.get_bot_profile()
            user = self.get_user_profile(chat_id=chat_id)
            if user["coin"] >= bot["job_coin"]:
                cursor.execute("UPDATE users SET coin=coin-{} WHERE chat_id={}".format(bot["job_coin"], chat_id))
                cursor.execute("UPDATE jobs SET status='pending' WHERE job_id={}".format(job_id))
                connection.commit()
                ret = True 
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # Closes a job with no deposit made
    def close_job_no_deposit(self, job: dict) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("DELETE FROM proposals WHERE job_id={}".format(job["job_id"]))
            cursor.execute("UPDATE jobs SET status='closed' WHERE job_id={}".format(job["job_id"]))
            if job["freelancer"] != -1:
                freelancer = self.get_user_profile(job["freelancer"])
                rate = ((freelancer["rate"] * freelancer["jobs_completed"]) + 5) / (freelancer["jobs_completed"] + 1)
                rate = round(rate, 1)
                cursor.execute("UPDATE users SET jobs_completed=jobs_completed+1, rate={} WHERE chat_id={}".format(rate, job["freelancer"]))
            connection.commit()
            ret = True
        except Exception as e:
            print(e)
        finally:
            connection.close()

        return ret

    # Closes a job with a deposit made
    def close_job_deposit(self, job: dict) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("DELETE FROM proposals WHERE job_id={}".format(job["job_id"]))
            cursor.execute("UPDATE jobs SET status='closed' WHERE job_id={}".format(job["job_id"]))
            cursor.execute("UPDATE users SET balance=balance+{} WHERE chat_id={}".format(job["price"], job["job_id"]))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # Retutns a dictionary object containing bot status or an empty dictionalry if an exception raises
    def get_bot_status(self) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='pending'")
            pending_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='opened'")
            opened_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='closed'")
            closed_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status='declined'")
            declined_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM users")
            users_count = cursor.fetchone()[0]
            cursor.execute("SELECT SUM(balance) AS total FROM users")
            total_balance = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM verify WHERE status='pending'")
            pending_verify_requests = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM cashout WHERE status='pending'")
            pending_cashout = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM deposit")
            deposits = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM update WHERE status='pending'")
            pending_update = cursor.fetchone()[0]
            bot = self.get_bot_profile()
            ret = {
                "pending_count": pending_count,
                "opened_count": opened_count,
                "closed_count": closed_count,
                "declined_count": declined_count,
                "pending_verify_requests": pending_verify_requests,
                "users_count": users_count,
                "total_balance": total_balance,
                "pending_cashout": pending_cashout,
                "deposits": deposits,
                "pending_update": pending_update,
            }
            for key in bot:
                ret[key] = bot[key]
        finally:
            connection.close()

        return ret
    
    # Retutns a dictionary object containing a proposal
    def get_proposal_by_id(self, proposal_id: int) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT proposal_id, chat_id, job_id, discription, days, price, status FROM proposals WHERE proposal_id={}".format(proposal_id))
            proposal = cursor.fetchone()
            ret = {
                "proposal_id": proposal[0],
                "chat_id": proposal[1],
                "job_id": proposal[2],
                "discription": proposal[3].rstrip(),
                "days": proposal[4],
                "price": proposal[5],
                "status": proposal[6].rstrip(),
            }
        finally:
            connection.close()

        return ret
    
    # Retutns a dictionary object containing a proposal
    def get_proposal_by_job_id(self, chat_id: int, job_id: int) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT proposal_id, chat_id, job_id, discription, days, price, status FROM proposals WHERE chat_id={} and job_id={}".format(chat_id, job_id))
            proposal = cursor.fetchone()
            ret = {
                "proposal_id": proposal[0],
                "chat_id": proposal[1],
                "job_id": proposal[2],
                "discription": proposal[3].rstrip(),
                "days": proposal[4],
                "price": proposal[5],
                "status": proposal[6].rstrip(),
            }
        finally:
            connection.close()

        return ret

    # Computes if a user can apply for a certain job
    def is_user_eligiable_to_apply(self, chat_id: int, job_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            bot = self.get_bot_profile()
            cursor.execute("SELECT coin, level FROM users WHERE chat_id={}".format(chat_id))
            user = cursor.fetchone()
            cursor.execute("SELECT status, level FROM jobs WHERE job_id={}".format(job_id))
            job = cursor.fetchone()
            cursor.execute("SELECT proposal_coin FROM bot")
            proposal_coin = cursor.fetchone()[0]
            if job[0].rstrip() == "opened" and user[0] >= proposal_coin:
                if bot["check_level"]:
                    if user[1] >= job[1]:
                        ret = True
                else:
                    ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # Creates a proposal or checks if there is already one
    def create_proposal(self, chat_id: int, job_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT EXISTS(SELECT chat_id FROM proposals WHERE chat_id={} AND job_id={} AND status='edit')".format(chat_id, job_id))
            if cursor.fetchone()[0]:
                pass
            else:
                cursor.execute("SELECT proposal_coin FROM bot")
                proposal_coin = cursor.fetchone()[0]
                cursor.execute("INSERT INTO proposals(chat_id, job_id) VALUES(%s, %s)", (chat_id, job_id))
                cursor.execute("UPDATE users SET coin=coin-{} WHERE chat_id={}".format(proposal_coin, chat_id))
                cursor.execute("UPDATE jobs SET counter=counter+1 WHERE job_id={}".format(job_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret
    
    # Check if a proposal exists
    def proposal_exists(self, chat_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT EXISTS (SELECT chat_id FROM proposals WHERE chat_id = {} AND status='edit')".format(chat_id))
            ret = cursor.fetchone()[0]
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret
    
    # Adds job to escrow
    def add_to_escrow(self, chat_id: int, job_id: int, proposal_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT EXISTS(SELECT job_id FROM escrow WHERE job_id={})".format(job_id))
            if not cursor.fetchone()[0]:
                cursor.execute("SELECT freelancer FROM jobs WHERE job_id={}".format(job_id))
                if cursor.fetchone()[0] == chat_id:
                    cursor.execute("INSERT INTO escrow(job_id, proposal_id, working) VALUES(%s, %s, true)", (job_id, proposal_id))
                    connection.commit()
                    ret = True
        except Exception as e:
            print(e)
        finally:
            connection.close()

        return ret

    # gets escrow using job id
    def get_escrow(self, job_id: int) -> {}:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT escrow_id, job_id, proposal_id, paid, working, time FROM escrow WHERE job_id={}".format(job_id))
            sql = cursor.fetchone()
            if sql != None and len(sql) > 0:
                ret = {
                    "escrow_id": sql[0],
                    "job_id": sql[1],
                    "proposal_id": sql[2],
                    "paid": sql[3],
                    "working": sql[4],
                    "time": sql[5],
                }
                
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # Removes job from escrow
    def close_escrow(self, job_id: int, paid: bool) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            escrow = self.get_escrow(job_id)
            if len(escrow) > 0:
                cursor.execute("SELECT chat_id, price FROM proposals WHERE proposal_id={}".format(escrow["proposal_id"]))
                sql = cursor.fetchone()
                if sql != None and len(sql) > 0: 
                    freelacer_chat_id = sql[0]
                    price = sql[1]
                    cursor.execute("DELETE FROM proposals WHERE job_id={} and proposal_id!={}".format(job_id, escrow["proposal_id"])) 
                    job = self.get_job_with_id(job_id)
                    employer_chat_id = job["chat_id"]
                    if paid:
                        freelancer = self.get_user_profile(freelacer_chat_id)
                        rate = ((freelancer["rate"] * freelancer["jobs_completed"]) + 5) / (freelancer["jobs_completed"] + 1)
                        rate = round(rate, 1)
                        employer_price = job["price"] - price 
                        cursor.execute("UPDATE escrow SET working=FALSE, paid=TRUE WHERE job_id={}".format(job_id))
                        cursor.execute("UPDATE jobs SET status='closed' WHERE job_id={}".format(job_id))
                        cursor.execute("UPDATE users SET balance=balance+{}, jobs_completed=jobs_completed+1, rate={} WHERE chat_id={}".format(price, rate, freelacer_chat_id))
                        cursor.execute("UPDATE users SET balance=balance+{} WHERE chat_id={}".format(employer_price, employer_chat_id))
                    else:
                        cursor.execute("UPDATE users SET balance=balance+{} WHERE chat_id={}".format(price, employer_chat_id))
                        cursor.execute("UPDATE escrow SET working=FALSE, paid=FALSE WHERE job_id={}".format(job_id))
                        cursor.execute("UPDATE jobs SET status='closed' WHERE job_id={}".format(job_id))
                    connection.commit()
                    ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # Check if a freelancer can be deassigned from a job
    def can_deassign(self, job_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = True
        try:
            cursor.execute("SELECT EXISTS (SELECT job_id FROM escrow WHERE job_id={})".format(job_id))
            sql = cursor.fetchone()[0]
            if sql:
                ret = False
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret
    
    # returns admins username
    def get_admins_username(self) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = []
        try:
            cursor.execute("SELECT chat_id FROM admins")
            admins = cursor.fetchall() 
            if admins != None and len(admins) > 0:
                ret = admins
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret
    
    # adds new photo to verify table
    def add_verify(self, chat_id: int, photo_id: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("SELECT EXISTS(SELECT chat_id FROM verify WHERE chat_id={})".format(chat_id))
            sql = cursor.fetchone()[0]
            if sql:
                cursor.execute("UPDATE verify SET photo_id=%s WHERE chat_id=%s", (photo_id, chat_id))
            else:
                cursor.execute("INSERT INTO verify(chat_id, photo_id) VALUES(%s, %s)", (chat_id, photo_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    # Adds company name to verify table
    def verify_add_name(self, chat_id: int, text: str) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE verify SET company='{}' WHERE chat_id={}".format(text, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()

        return ret

    def get_verify_dict(self, data: list) -> dict:
        ret = {
                "verify_id": data[0],
                "chat_id": data[1],
                "photo_id": data[2].rstrip(),
                "company": data[3].rstrip(),
                "status": data[4].rstrip(),
            }
        return ret

    # Returns a dictionary of verify table
    def get_verify(self, chat_id: int=None, verify_id: int=None) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            if chat_id != None:
                cursor.execute("SELECT verify_id, chat_id, photo_id, company, status FROM verify WHERE chat_id={}".format(chat_id))
                sql = cursor.fetchone()
            else:
                cursor.execute("SELECT verify_id, chat_id, photo_id, company, status FROM verify WHERE verify_id={}".format(verify_id))
                sql = cursor.fetchone()
            if sql == None or len(sql) == 0:
                ret = {}
            else:
                ret = self.get_verify_dict(sql)
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret
    
    # Returns a list of opened jobs
    def get_verify_with_status(self, status: str) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ls = []
        try:
            cursor.execute("SELECT verify_id, chat_id, photo_id, company, status FROM verify WHERE status='{}' ORDER BY verify_id ASC LIMIT 5".format(status))
            data = cursor.fetchall()
            if data == None:
                ls = []
            else:
                for verify in data:
                    ls.append(self.get_verify_dict(verify))

        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ls

    def get_cashout_dict(self, data: list) -> dict:
        ret = {
                "cashout_id": data[0],
                "chat_id": data[1],
                "price": data[2],
                "status": data[3].rstrip(),
                "time": data[4],
            }
        return ret

    # Returns a dictionary cashout
    def get_cashout(self, cashout_id: int) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT cashout_id, chat_id, price, status, time FROM cashout WHERE cashout_id={}".format(cashout_id))
            sql = cursor.fetchone()
            if sql != None and len(sql) > 0:
                ret = self.get_cashout_dict(sql)
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # Returns a list of cashout depending on specified status
    def get_cashout_with_status(self, status: str) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ls = []
        try:
            cursor.execute("SELECT cashout_id, chat_id, price, status, time FROM cashout WHERE status='{}' ORDER BY cashout_id ASC LIMIT 5".format(status))
            data = cursor.fetchall()
            if data == None:
                ls = []
            else:
                for cashout in data:
                    ls.append(self.get_cashout_dict(cashout))

        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ls

    def get_update_dict(self, data: list) -> dict:
        ret = {
                "update_id": data[0],
                "chat_id": data[1],
                "status": data[2].rstrip(),
                "time": data[3],
            }
        return ret

    # Returns a dictionary cashout
    def get_update(self, update_id: int) -> dict:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = {}
        try:
            cursor.execute("SELECT update_id, chat_id, status, time FROM update WHERE update_id={}".format(update_id))
            sql = cursor.fetchone()
            if sql != None and len(sql) > 0:
                ret = self.get_update_dict(sql)
        except Exception as e:
            pass
        finally:
            connection.close()
        return ret

    # Returns a list of cashout depending on specified status
    def get_update_with_status(self, status: str) -> list:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ls = []
        try:
            cursor.execute("SELECT update_id, chat_id, status, time FROM update WHERE status='{}' ORDER BY update_id ASC LIMIT 5".format(status))
            data = cursor.fetchall()
            if data == None:
                ls = []
            else:
                for update in data:
                    ls.append(self.get_update_dict(update))

        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ls

    # Rates a freelancer and returns 
    def rate_freelancer(self, chat_id: int, rate: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            user = self.get_user_profile(chat_id)
            if len(user) > 0:
                new_rate = (((user["rate"] * user["jobs_completed"]) - 5) + rate) / user["jobs_completed"]
                rate = round(rate,1)
                cursor.execute("UPDATE users SET rate={} WHERE chat_id={}".format(new_rate, chat_id))
                connection.commit()
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # Rates a freelancer and returns 
    def create_deposit(self, chat_id: int, price: int, paid: bool) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("INSERT INTO deposit(chat_id, price, paid) VALUES(%s, %s, %s)", (chat_id, price, paid))
            cursor.execute("UPDATE users SET balance=balance+{} WHERE chat_id={}".format(price, chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # Process a cashout request 
    def process_cashout(self, chat_id: int, price: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            user = self.get_user_profile(chat_id)
            if user["balance"] >= price:
                cursor.execute("INSERT INTO cashout(chat_id, price) VALUES(%s, %s)", (chat_id, price))
                cursor.execute("UPDATE users SET balance=balance-{} WHERE chat_id={}".format(price, chat_id))
                connection.commit()
                ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret
    
    # Declines a cashout request 
    def decline_cashout(self, cashout: dict) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("UPDATE cashout SET status='declined' WHERE cashout_id={}".format(cashout["cashout_id"]))
            cursor.execute("UPDATE users SET balance=balance+{} WHERE chat_id={}".format(cashout["price"], cashout["chat_id"]))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret
    
    # Approves update request 
    def approve_update(self, update_req: dict) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("DELETE FROM update WHERE update_id={}".format(update_req["update_id"]))
            cursor.execute("UPDATE users SET level=level+1 WHERE chat_id={}".format(update_req["chat_id"]))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # Declines update request 
    def decline_update(self, update_req: dict) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("DELETE FROM update WHERE update_id={}".format(update_req["update_id"]))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # Creates update request 
    def create_update_req(self, chat_id: int) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            cursor.execute("INSERT INTO update(chat_id) VALUES({})".format(chat_id))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    # Creates tables
    def create_tables(self) -> bool:
        connection = psycopg2.connect(host=self.db_host, port=self.db_port, user=self.db_user,password=self.db_password,database=self.db_database)
        cursor = connection.cursor()
        ret = False
        try:
            text = """
    CREATE TABLE users(
    chat_id BIGINT PRIMARY KEY,
    phone_number BIGINT NOT NULL UNIQUE,
    first_name VARCHAR(25) DEFAULT 'unknown',
    username VARCHAR(25) DEFAULT 'unknown',
    balance DOUBLE PRECISION DEFAULT 0 CHECK(balance >= 0), 
    money_made DOUBLE PRECISION DEFAULT 0 CHECK(money_made >= 0),
    company VARCHAR(50) DEFAULT 'unknown',
    verified BOOL DEFAULT FALSE,
    lang CHAR(10) DEFAULT 'eng',
    coin SMALLINT DEFAULT 10 CHECK(coin >= 0),
    jobs_completed SMALLINT DEFAULT 0,
    jobs_posted INT DEFAULT 0,
    rate FLOAT DEFAULT 0, 
    level SMALLINT DEFAULT 0 CHECK(level <= 2),
    status CHAR(10) DEFAULT 'active',
    warning SMALLINT DEFAULT 0,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE admins(
    chat_id BIGINT PRIMARY KEY REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    super bool DEFAULT FALSE,
    ban BOOL DEFAULT TRUE,
    approve BOOL DEFAULT TRUE,
    configure BOOL DEFAULT FALSE,
    process_deposit BOOL DEFAULT FALSE,
    process_payment BOOL DEFAULT FALSE);

CREATE TABLE jobs(
    job_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    title VARCHAR(50)  DEFAULT 'unknown',
    company VARCHAR(50) DEFAULT 'unknown',
    discription TEXT  DEFAULT 'unknown',
    cat CHAR(15)  DEFAULT 'unknown',
    type CHAR(15)  DEFAULT 'unknown',
    deposit BOOL DEFAULT FALSE,
    price DOUBLE PRECISION DEFAULT 0,
    level SMALLINT DEFAULT 0,
    coin SMALLINT DEFAULT 1, 
    freelancer BIGINT DEFAULT -1,
    escrow_id BIGINT DEFAULT -1, 
    status CHAR(10) DEFAULT 'edit',
    message_id BIGINT,
    proposal_limit SMALLINT DEFAULT 1 CHECK(proposal_limit > 0),
    counter SMALLINT DEFAULT 0,
    counter_f SMALLINT DEFAULT 0, 
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE proposals(
    proposal_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    job_id INT NOT NULL REFERENCES jobs ON DELETE CASCADE ON UPDATE CASCADE,
    discription VARCHAR(250) DEFAULT 'unknown',
    price DOUBLE PRECISION DEFAULT 0,
    days SMALLINT DEFAULT 1,
    status CHAR(10) DEFAULT 'edit',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE escrow(
    escrow_id BIGSERIAL PRIMARY KEY,
    job_id INT NOT NULL UNIQUE REFERENCES jobs ON DELETE CASCADE ON UPDATE CASCADE,
    proposal_id INT NOT NULL UNIQUE REFERENCES proposals ON DELETE CASCADE ON UPDATE CASCADE,
    working bool DEFAULT FALSE,
    paid bool DEFAULT FALSE,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE verify(
    verify_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    photo_id TEXT NOT NULL,
    company VARCHAR(50) DEFAULT 'unknown',
    status CHAR(10) DEFAULT 'edit',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE deposit(
    deposit_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    price DOUBLE PRECISION  NOT NULL,
    paid BOOL DEFAULT FALSE,
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE cashout(
    cashout_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    price DOUBLE PRECISION  NOT NULL,
    status CHAR(15) DEFAULT 'pending',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE update(
    update_id BIGSERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE NOT NULL REFERENCES users ON DELETE CASCADE ON UPDATE CASCADE,
    status CHAR(15) DEFAULT 'pending',
    time TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE bot(
    bot VARCHAR(25) NOT NULL,
    channel VARCHAR(25) NOT NULL,
    s_channel VARCHAR(25) NOT NULL,
    p_channel VARCHAR(25) NOT NULL,
    s_admin VARCHAR(25)NOT NULL,
    s_group VARCHAR(25)NOT NULL,
    check_level BOOL DEFAULT FALSE,
    job_coin INT DEFAULT 0,
    proposal_coin INT DEFAULT 0,
    application_fee INT DEFAULT 0,
    minimum_deposit INT DEFAULT 1,
    maximum_deposit INT DEFAULT 2000,
    minimum_cashout INT DEFAULT 1,
    maximum_cashout INT DEFAULT 500,
    yenepay_cut INT DEFAULT 0,
    merchant_id INT DEFAULT 0);


INSERT INTO bot(bot, channel, s_channel, p_channel, s_admin, s_group) VALUES('freelance321bot', 'freelance321', 'freelance321_support', 'freelance321_payment', 'freelance321_admin', 'freelance321_group');
"""
            cursor.execute("{}".format(text))
            connection.commit()
            ret = True
        except Exception as e:
            pass
        finally:
            connection.close()
        
        return ret

    