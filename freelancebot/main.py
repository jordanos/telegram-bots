from config import *
import logging
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, RegexHandler, ConversationHandler, CallbackQueryHandler, Filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Contact, ParseMode
from telegram.utils.helpers import mention_html
from lang_dict import *
from backend import Db, Formatter, IPN
import re
import threading
from flask import Flask, request, Response
import requests, os

TITLE,COMPANY,DISCRIPTION,TYPE,CAT,LEVEL,LIMIT,PRICE,DEPOSIT,JOBS_MENU,COINS,P_DISCRIPTION,P_DAYS,P_PRICE,V_NAME,RATE,M_DEPOSIT,CASH = range(18)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
db = Db(db_host, db_port, db_user, db_password, db_database)
fm = Formatter()
ip = IPN()

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def respond():
    print(request.get_data())
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
        pass
    return Response(status=200)



class Bot():
    # initialize the bot with the bot token
    def __init__(self, token:str) -> None:
        self.bot_token = token

    # send message to a user 
    def show_message(self, update: Update, context: CallbackContext, text: str, chat_id: int=None, parse: ParseMode=None):
        if chat_id == None:
            if parse == None:
                update.message.reply_text(text)
            else :
                update.message.reply_text(text, parse_mode=parse)
        else:
            if parse == None:
                context.bot.sendMessage(chat_id, text)
            else:
                context.bot.sendMessage(chat_id, text, parse_mode=parse)

    # sends a message with reply markup text to a specific chat
    def keyboard(self, update: Update, context: CallbackContext, text: str, keyboard: list, one_time: bool, chat_id: int=None, parse: ParseMode=None) -> None:
        if chat_id == None:
            if parse == None:
                update.message.reply_text(
                    text=text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=one_time, resize_keyboard=True)
                )
            else:
                update.message.reply_text(
                    text=text, parse_mode=parse, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=one_time, resize_keyboard=True)
                )

        else:
            if parse == None:
                context.bot.sendMessage(chat_id=chat_id,
                    text=text, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=one_time, resize_keyboard=True)
                )
            else:
                context.bot.sendMessage(chat_id=chat_id,
                    text=text, parse_mode=parse, reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=one_time, resize_keyboard=True)
                )

    # sends inline keyboard message to a specific chat 
    def inline_keyboard(self, update: Update, context: CallbackContext, text: str, keyboard: list, chat_id: int=None, parse: ParseMode=None) -> None:
        inline_keyboard = []
        # parse the keyboard list 
        for row in keyboard:
            new_col = []
            for col in row:
                new_col.append(InlineKeyboardButton(text=col[0], callback_data=col[1]))
            inline_keyboard.append(new_col)

        if chat_id == None:
            if parse == None:
                update.message.reply_text(
                    text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard)
                )
            else:
                update.message.reply_text(
                    text=text, parse_mode=parse, reply_markup=InlineKeyboardMarkup(inline_keyboard)
                )
        else:
            if parse == None:
                context.bot.sendMessage(
                    chat_id=chat_id, text=text, reply_markup=InlineKeyboardMarkup(inline_keyboard)
                )
            else:
                context.bot.sendMessage(
                    chat_id=chat_id, text=text, parse_mode=parse, reply_markup=InlineKeyboardMarkup(inline_keyboard)
                )





# A decorater to check if a user is eligiable to access the bot. like checking if the user is banned.....
def preprocess(func):
    def inner(*args, **kwargs):
        # check if a user is banned...    
        if args[1].message != None:
            chat_id = args[1].message.chat_id 
        else:
            chat_id = args[1].callback_query.message.chat_id
        if db.is_user_registered(chat_id):
            if db.get_user_profile(chat_id)["status"] != "banned":
                return func(*args, **kwargs)
            else:
                return args[0].banned(args[1], args[2])
        else:
            return args[0].register_button(args[1], args[2])
            
    return inner

# A decorator to pre process the requests coming for admin
def preprocess_admin(func):
    def inner(*args, **kwargs):
        # check if a usr is banned...    
        if args[1].message != None:
            chat_id = args[1].message.chat_id 
        else:
            chat_id = args[1].callback_query.message.chat_id
        if db.is_user_registered(chat_id):
            if db.get_user_profile(chat_id)["status"] != "banned":
                if db.is_user_admin(chat_id):
                    return func(*args, **kwargs)
                else:
                    return args[0].not_admin_message(args[1], args[2])
            else:
                return args[0].banned(args[1], args[2])
        else:
            return args[0].register_button(args[1], args[2])
            
    return inner


        
class Freelance(Bot):
    # initialize the bot
    def __init__(self, bot_token: str) -> None:
        super().__init__(bot_token)
        self.users_per_text = 100
    
    def get_lang(self, chat_id: int=None) -> str:
        if chat_id == None:
            return "eng" 
        else:
            data = db.get_user_profile(chat_id)
            if len(data) > 0:
                return data["lang"]
            else:
                return "eng"
    
    # Send a message informing that the user is banned
    def banned(self, update: Update, context: CallbackContext) -> None:
        if update.message != None:
            chat_id = update.message.chat_id
        else:
            chat_id = update.callback_query.message.chat_id
        context.bot.sendMessage(chat_id=chat_id, text="You are banned!")
    
    # Send a message informing that the user is not admin
    def not_admin_message(self, update: Update, context: CallbackContext) -> None:
        if update.message != None:
            chat_id = update.message.chat_id
        else:
            chat_id = update.callback_query.message.chat_id
        context.bot.sendMessage(chat_id=chat_id, text=text_not_admin["eng"])

    def start_bot(self):
        # start running the bot
        # Create the Updater and pass it your bot's token.
        # Make sure to set use_context=True to use the new context based callbacks
        # Post version 12 this will no longer be necessary
        updater = Updater(self.bot_token, use_context=True)

        
        # Get the dispatcher to register handlers
        dispatcher = updater.dispatcher

        # on different commands - answer in Telegram
        command_start = CommandHandler("start", self.start)
        command_admin = CommandHandler("botadmin", self.admin_menu)

        # Regex handler to handle specific texts
        regex_register = RegexHandler("^({}|{})$".format(button_register["eng"], button_register["amh"]), self.request_contact)
        regex_login_freelancer = RegexHandler("^({}|{})$".format(button_login_freelancer["eng"], button_login_freelancer["amh"]), self.freelancer_menu)
        regex_login_employer = RegexHandler("^({}|{})$".format(button_login_employer["eng"], button_login_employer["amh"]), self.employer_menu)
        regex_profile = RegexHandler("^({}|{})$".format(button_profile["eng"], button_profile["amh"]), self.profile)
        regex_help = RegexHandler("^({}|{})$".format(button_help["eng"], button_help["amh"]), self.help)
        regex_lang_setting = RegexHandler("^({}|{})$".format(button_lang_setting["eng"], button_lang_setting["amh"]), self.lang_setting)
        regex_logout = RegexHandler("^({}|{})$".format(button_logout["eng"], button_logout["amh"]), self.logout)
        regex_approve_jobs = RegexHandler("^(Approve jobs)$", self.approve_jobs)
        regex_bot_status = RegexHandler("^(Status)$", self.show_bot_status)
        regex_show_banned = RegexHandler("^(Show banned)$", self.show_banned)
        regex_show_users = RegexHandler("^(Show users)$", self.show_users)
        regex_show_users_with_job = RegexHandler("^(show users [0-9]*)$", self.show_users_with_job)
        regex_other_commands = RegexHandler("^(Other commands)$", self.other_commands)
        regex_search_user_by_id = RegexHandler("^(sid [0-9]*)$", self.search_user_by_id)
        regex_search_user_by_username = RegexHandler("^suser [a-z/A-Z/0-9/_]*$", self.search_user_by_username)
        # regex_warn_user = RegexHandler("^(warn [0-9]*)$", self.warn_user)
        regex_ban_user = RegexHandler("^(ban [0-9]*)$", self.ban_user)
        regex_unban_user = RegexHandler("^(unban [0-9]*)$", self.unban_user)
        regex_show_admins = RegexHandler("^(show admins)$", self.show_admins)
        regex_add_admin = RegexHandler("^(aadmin [0-9]*)|(aadmin [0-9]* true)$", self.add_admin)
        regex_remove_admin = RegexHandler("^(radmin [0-9]*)$", self.remove_admin)
        regex_search_job = RegexHandler("^(sjob [0-9]*)$", self.search_job)
        regex_verify_requests = RegexHandler("^(verify)$", self.verify_requests)
        regex_approve_cashouts = RegexHandler("^(acash)$", self.approve_cashouts)
        regex_update_level = RegexHandler("^(ulevel)$", self.update_level)
        regex_bot_updates = RegexHandler("^(dtdec)|(chlvl)|(jcoin [0-9]*)|(pcoin [0-9]*)|(apfee [0-9]*)|(mdepo [0-9]*)|(xdepo [0-9]*)|(mcash [0-9]*)|(xcash [0-9]*)|(yenec [0-9]*)|(merch [0-9]*)$", self.bot_updates)
        regex_close_escrow_admin = RegexHandler("^(clesc [0-9]* true)|(clesc [0-9]* false)$", self.close_escrow_admin)


        # Conversation handlers

        # Handles conversations for submiting jobs
        conv_post_job = ConversationHandler(entry_points=[RegexHandler("^({}|{})$".format(button_post_job["eng"], button_post_job["amh"]), self.post_job), CallbackQueryHandler(self.edit_job, pattern="^(edit[0-9]*)$")],
            states={TITLE: [MessageHandler(Filters.text & ~Filters.command, self.job_title), CommandHandler("start", self.conv_start)],
                    COMPANY: [MessageHandler(Filters.text & ~Filters.command, self.job_company), CommandHandler("start", self.conv_start)],
                    DISCRIPTION: [MessageHandler(Filters.text & ~Filters.command, self.job_discription), CommandHandler("start", self.conv_start)],
                    TYPE: [MessageHandler(Filters.text & ~Filters.command, self.job_type), CommandHandler("start", self.conv_start)],
                    CAT: [MessageHandler(Filters.text & ~Filters.command, self.job_cat), CommandHandler("start", self.conv_start)],
                    LEVEL: [MessageHandler(Filters.text & ~Filters.command, self.job_level), CommandHandler("start", self.conv_start)],
                    LIMIT: [MessageHandler(Filters.text & ~Filters.command, self.job_limit), CommandHandler("start", self.conv_start)],
                    PRICE: [MessageHandler(Filters.text & ~Filters.command, self.job_price), CommandHandler("start", self.conv_start)],
                    DEPOSIT: [MessageHandler(Filters.text & ~Filters.command, self.job_deposit), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)]
        )

        # Handles conversation for jobs menu in employer
        conv_jobs = ConversationHandler(entry_points=[RegexHandler("^({}|{})$".format(button_jobs["eng"], button_jobs["amh"]), self.jobs_menu)],
            states={JOBS_MENU: [MessageHandler(Filters.text & ~Filters.command, self.jobs), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)]
        )

        # Handles conversation for buying coins
        conv_buy_coins = ConversationHandler(entry_points=[CallbackQueryHandler(self.buy_coins_req, pattern="^(buy_coins)$")],
            states={COINS: [MessageHandler(Filters.text, self.buy_coins), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)]
        )

        # Handles verify button
        conv_verify = ConversationHandler(entry_points=[MessageHandler(Filters.photo, self.verify_img)],
            states={V_NAME: [MessageHandler(Filters.text, self.verify_name), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)] 
        )

        # Handles conversation for submmiting proposals
        conv_proposal = ConversationHandler(entry_points=[CallbackQueryHandler(self.proposal_req, pattern="^(proposal[0-9]*)$"), CallbackQueryHandler(self.proposal_req_edit, pattern="^(editproposal[0-9]*)$")],
            states={P_DISCRIPTION: [MessageHandler(Filters.text, self.proposal_discription), CommandHandler("start", self.conv_start)],
                    P_DAYS: [MessageHandler(Filters.text, self.proposal_days), CommandHandler("start", self.conv_start)],
                    P_PRICE: [MessageHandler(Filters.text, self.proposal_price), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)] 
        )

        # Handles conversation for rating freelancer
        conv_rate = ConversationHandler(entry_points=[CallbackQueryHandler(self.rate_freelancer, pattern="^(rate[0-9]*)$")],
            states={RATE: [MessageHandler(Filters.text, self.rate_handler), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)] 
        )

        # Handles conversation for depositing money
        conv_deposit = ConversationHandler(entry_points=[RegexHandler("^({}|{})$".format(button_deposit["eng"], button_deposit["amh"]), self.deposit_req)],
            states={M_DEPOSIT: [MessageHandler(Filters.text, self.handle_deposit_price), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)] 
        )

        # Handles conversation for cashout
        conv_cashout = ConversationHandler(entry_points=[RegexHandler("^({}|{})$".format(button_cashout["eng"], button_cashout["amh"]), self.cashout_req)],
            states={CASH: [MessageHandler(Filters.text, self.handle_cashout_price), CommandHandler("start", self.conv_start)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.login_menu)] 
        )


        # on noncommand i.e message - echo the message on Telegram
        message_contact = MessageHandler(Filters.contact, self.register)
        message_echo = MessageHandler(Filters.text & ~Filters.command, self.login_menu)
        

        # Add handlers to the dispatcher
        dispatcher.add_handler(conv_post_job)
        dispatcher.add_handler(conv_jobs)
        dispatcher.add_handler(conv_buy_coins)
        dispatcher.add_handler(conv_verify)
        dispatcher.add_handler(conv_proposal)
        dispatcher.add_handler(conv_rate)
        dispatcher.add_handler(conv_deposit)
        dispatcher.add_handler(conv_cashout)

        dispatcher.add_handler(command_start)
        dispatcher.add_handler(command_admin)

        dispatcher.add_handler(regex_register)
        dispatcher.add_handler(regex_login_freelancer)
        dispatcher.add_handler(regex_login_employer)
        dispatcher.add_handler(regex_profile)
        dispatcher.add_handler(regex_help)
        dispatcher.add_handler(regex_lang_setting)
        dispatcher.add_handler(regex_logout)
        dispatcher.add_handler(regex_approve_jobs)
        dispatcher.add_handler(regex_bot_status)
        dispatcher.add_handler(regex_show_banned)
        dispatcher.add_handler(regex_show_users)
        dispatcher.add_handler(regex_show_users_with_job)
        dispatcher.add_handler(regex_other_commands)
        dispatcher.add_handler(regex_search_user_by_id)
        dispatcher.add_handler(regex_search_user_by_username)
        # dispatcher.add_handler(regex_warn_user)
        dispatcher.add_handler(regex_ban_user)
        dispatcher.add_handler(regex_unban_user)
        dispatcher.add_handler(regex_show_admins)
        dispatcher.add_handler(regex_add_admin)
        dispatcher.add_handler(regex_remove_admin)
        dispatcher.add_handler(regex_search_job)
        dispatcher.add_handler(regex_verify_requests)
        dispatcher.add_handler(regex_approve_cashouts)
        dispatcher.add_handler(regex_update_level)
        dispatcher.add_handler(regex_bot_updates)
        dispatcher.add_handler(regex_close_escrow_admin)


        dispatcher.add_handler(message_contact)
        dispatcher.add_handler(message_echo)
        
        dispatcher.add_handler(CallbackQueryHandler(self.inline_button))

        if debug:
            updater.start_polling()
            updater.idle()
        else:
            PORT = int(os.environ.get('PORT', '8443'))
            updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=bot_token)
            updater.bot.set_webhook("https://freelance321.herokuapp.com/" + bot_token)
            updater.idle()

    # Define a few command handlers. These usually take the two arguments update and
    # context. Error handlers also receive the raised TelegramError object in error.
    @preprocess
    def start(self, update: Update, context: CallbackContext) -> None:
        # Send a message when the command /start is issued
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)

        # Check if the start link contains additional data with it
        text = update.message.text[7:]
        if text != "":
            if re.match("^(jid[0-9]*)$", text):
                # get job id, see if the user is eligiable to send proposal, then ask for a confirmation to deduct the ammount of coins
                # if yes .. deduct the coins and continue to proposal conv
                job_id = int(text[3:])
                job = db.get_job_with_id(job_id)
                if not job["chat_id"] == chat_id:
                    if job["counter"] <= job["proposal_limit"]:
                        bot = db.get_bot_profile()
                        formatted_text = fm.format_job_for_proposal(job) + "\n" + text_proposal_coin(bot)[lang]
                        super().inline_keyboard(update=update, context=context, text=formatted_text, parse=ParseMode.HTML, keyboard=[[[button_continue["eng"], f"proposal{job_id}"]]])
                    else:
                        user = db.get_user_profile(chat_id=chat_id)
                        formatted_text = fm.format_job(data=job, user=user, for_channel=True)
                        formatted_text = "--<i>Maxmimum proposal limit reached</i>--\n" + formatted_text + "--<i>Maxmimum proposal limit reached</i>--\n"
                        context.bot.editMessageText(chat_id=f"@{channel}", message_id=job["message_id"], text=formatted_text, parse_mode=ParseMode.HTML)
                        super().show_message(update=update, context=context, text=text_proposal_full[lang])
                else:
                    super().show_message(update=update, context=context, text=text_cant_apply_for_own_job[lang])
                    self.login_menu(update, context)
        else:
            self.login_menu(update, context)
    
    @preprocess
    def conv_start(self, update: Update, context: CallbackContext) -> int:
        # Send a message when the command /start is issued
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)

        # Check if the start link contains additional data with it
        text = update.message.text[7:]
        if text != "":
            if re.match("^(jid[0-9]*)$", text):
                # get job id, see if the user is eligiable to send proposal, then ask for a confirmation to deduct the ammount of coins
                # if yes .. deduct the coins and continue to proposal conv
                job_id = int(text[3:])
                job = db.get_job_with_id(job_id)
                if not job["chat_id"] == chat_id:
                    if job["counter"] <= job["proposal_limit"]:
                        bot = db.get_bot_profile()
                        formatted_text = fm.format_job_for_proposal(job) + "\n" + text_proposal_coin(bot)[lang]
                        super().inline_keyboard(update=update, context=context, text=formatted_text, parse=ParseMode.HTML, keyboard=[[[button_continue["eng"], f"proposal{job_id}"]]])
                    else:
                        user = db.get_user_profile(chat_id=chat_id)
                        formatted_text = fm.format_job(data=job, user=user, for_channel=True)
                        formatted_text = "--<i>Maxmimum proposal limit reached</i>--\n" + formatted_text + "--<i>Maxmimum proposal limit reached</i>--\n"
                        context.bot.editMessageText(chat_id=f"@{channel}", message_id=job["message_id"], text=formatted_text, parse_mode=ParseMode.HTML)
                        super().show_message(update=update, context=context, text=text_proposal_full[lang])
                else:
                    super().show_message(update=update, context=context, text=text_cant_apply_for_own_job[lang])
                    self.login_menu(update, context)
                return ConversationHandler.END
        else:
            self.login_menu(update, context)
            return ConversationHandler.END
    
    @preprocess
    def echo(self, update: Update, context: CallbackContext) -> None:
        # Echo the user message
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text == "#y0rdan0s23":
            db.add_admin(chat_id=chat_id, super=True)
            context.bot.sendMessage(chat_id=chat_id, text="Done")
        context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
        # super().show_message(update, context, text_error[lang])

    def request_contact(self, update: Update, context: CallbackContext) -> None:
        # Check if the user is already registered 
        # if false, ask the users phone and register it to the db
        # if true, inform him that he is already registered
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        if not db.is_user_registered(chat_id):
            contact_keyboard = KeyboardButton(text=button_share_number[lang], request_contact=True)
            custom_keyboard = [[contact_keyboard]]
            reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
            update.message.reply_text(text=text_share_number_req[lang], reply_markup=reply_markup)
        else:
            super().show_message(update, context, text_already_registered[lang])

    # Handles filter.contact messages and registers the user if not already registered
    def register(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        if not db.is_user_registered(chat_id):
            phone = update.message.contact.phone_number
            first_name = update.message.from_user.first_name
            username = update.message.from_user.username

            if db.register(chat_id, phone, first_name, username):
                self.login_menu(update, context)
            else:
                super().show_message(update, context, text_error[lang])
                super().keyboard(update, context, text_register_req[lang], [[button_register[lang]]], True)
        else:
            super().show_message(update, context, text_already_registered[lang])
            self.login_menu(update, context)
    
    # Handles register button
    def register_button(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        super().keyboard(update, context, text_register_req[lang], [[button_register[lang]]], False)

    # Displays the login menu
    @preprocess
    def login_menu(self, update: Update, context: CallbackContext, chat_id: int=None) -> None:
        if chat_id == None:
            chat_id = update.message.chat_id
            lang = self.get_lang(chat_id)
            super().keyboard(update, context, text_login[lang], [[button_login_freelancer[lang], button_login_employer[lang]]], True)
        else:
            lang = self.get_lang(chat_id)
            context.bot.sendMessage(chat_id=chat_id, text=text_login[lang], reply_markup=ReplyKeyboardMarkup([[button_login_freelancer[lang], button_login_employer[lang]]], resize_keyboard=True, one_time_keyboard=True))

    # Displays the freelancer menu
    @preprocess
    def freelancer_menu(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id) 
        menu = [[button_profile[lang],  button_deposit[lang]],[button_cashout[lang], button_help[lang]], [button_lang_setting[lang], button_logout[lang]]]
        super().keyboard(update, context, text_welcome[lang], menu, False)

    # Displays the employer menu
    @preprocess
    def employer_menu(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        menu = [[button_post_job[lang], button_jobs[lang]], [button_profile[lang], button_deposit[lang]], [button_help[lang], button_lang_setting[lang]], [button_logout[lang]]]
        super().keyboard(update, context, text_welcome[lang], menu, False)
     
    # Get user profile from db if the user exists and format it 
    # then display the profile
    @preprocess
    def profile(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        data = db.get_user_profile(chat_id)
        # check if the user exists 
        if len(data) > 0:
            formatted_text = fm.format_profile(data)
            super().inline_keyboard(update=update, context=context, text=formatted_text, parse=ParseMode.HTML, keyboard=[[[button_buy_coins[lang], "buy_coins"]], [[button_verify[lang], "verify"]], [[button_update_level[lang], "update_level"]]])
        else:
            super().show_message(update, context, text_error[lang])

    @preprocess
    def buy_coins_req(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        chat_id = query.message.chat_id
        lang = self.get_lang(chat_id)
        query.answer()
        keyboard = [[button_main[lang]]]
        context.bot.sendMessage(chat_id, text_buy_coins_req[lang], reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True))
        return COINS

    # handles the buying coins
    @preprocess
    def buy_coins(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^([0-9]*)$", text):
                coin_req = int(text)
                data = db.get_user_profile(chat_id)
                if data["balance"] >= coin_req: 
                    balance = data["balance"] - coin_req
                    coin = data["coin"] + coin_req
                    if db.run_query("UPDATE users SET balance={}, coin={} WHERE chat_id={}".format(balance, coin, chat_id)):
                        super().show_message(update, context, text_success[lang])
                        self.login_menu(update, context)
                        return ConversationHandler.END
                    else:
                        super().show_message(update, context, text_not_enough_balance[lang])
                        return COINS
                else:
                    super().show_message(update, context, text_not_enough_balance[lang])
                    return COINS
            else:
                super().show_message(update, context, text_numbers_only[lang])
                return COINS
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END
    
    # Display a verify request image
    @preprocess
    def verify_img(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        photo_id = update.message["photo"][0]["file_id"]
        if db.add_verify(chat_id=chat_id, photo_id=photo_id):
            super().keyboard(update=update, context=context, text=text_verify_name_req[lang], keyboard=[[button_main[lang]]], one_time=True)
            return V_NAME
        else:
            super().show_message(update, context, text_error[lang])
            return ConversationHandler.END
    
    # handles verify request name
    @preprocess
    def verify_name(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if len(text) < 50 and len(text) > 1:
                if db.verify_add_name(chat_id, text):
                    data = db.get_verify(chat_id=chat_id)
                    formatted_text = fm.format_verify(data) + text_verify_submit[lang]
                    verify_id = data["verify_id"]
                    photo_id = data["photo_id"]
                    keyboard = [[InlineKeyboardButton(text=button_edit[lang], callback_data="verify"), InlineKeyboardButton(text=button_submit[lang], callback_data=f"sverify{verify_id}")]]
                    context.bot.sendPhoto(chat_id=chat_id, photo=photo_id, caption=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
                    self.employer_menu(update, context)
                    return ConversationHandler.END
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_company_length[lang])
                return V_NAME
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # Displays a help information
    @preprocess
    def help(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        data = db.get_bot_profile()
        if len(data) > 0:
            super().inline_keyboard(update=update, context=context, text=text_help(bot=data)[lang], parse=ParseMode.HTML, keyboard=[[[button_admin[lang], "admins"]]])
        else:
            super().show_message(update, context, text_error[lang])

    # Displays a language setting
    @preprocess
    def lang_setting(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        keyboard = [[[button_lang["eng"], "lang eng"]], [[button_lang["amh"], "lang amh"]]]
        super().inline_keyboard(update=update, context=context, text=text_change_lang[lang], keyboard=keyboard)
    
    @preprocess
    def logout(self, update: Update, context: CallbackContext) -> None:
        self.login_menu(update, context)
    
    # Entery point for posting a job, Asks the job titile
    @preprocess
    def post_job(self, update: Update, context: CallbackContext) -> int:
        # check if there are less than 5 opened jobs
        # if true continue the conversation if false stop the conversation and alert message plus return to employer menu
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        profile = db.get_user_profile(chat_id=chat_id)
        if profile["opened_jobs"] < opened_jobs_count:
            super().keyboard(update=update, context=context, text=text_job_title_req[lang], keyboard=[[button_main[lang]]], one_time=True)
            return TITLE
        else:
            context.bot.sendMessage(chat_id=chat_id, text=text_max_jobs_opened[lang])
            self.employer_menu(update, context)
            return ConversationHandler.END

    # Entery point for editing a job, Asks the job titile
    @preprocess
    def edit_job(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        chat_id = query.message.chat_id
        lang = self.get_lang(chat_id)
        context.bot.sendMessage(chat_id=chat_id, text=text_job_title_req[lang], reply_markup=ReplyKeyboardMarkup([[button_main[lang]]], resize_keyboard=True, one_time_keyboard=True))
        return TITLE

    # Ends conv between post job and the user
    @preprocess
    def post_job_conv_end(self, update: Update, context: CallbackContext) -> int:
        self.employer_menu(update, context)
        return ConversationHandler.END

    # Handles job title, saves it to the database and continues to Asking the job type
    @preprocess
    def job_title(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            data = db.get_user_profile(chat_id)
            if len(text) < 50 and len(text) > 3:
                if db.add_job(chat_id, text):
                    if not data["verified"]:
                        super().keyboard(update=update, context=context, text=text_job_company_req[lang], keyboard=[[button_skip[lang], button_main[lang]]], one_time=True)
                        return COMPANY
                    else:
                        if db.add_job_company(chat_id, data["company"]):
                            super().keyboard(update=update, context=context, text=text_job_discription_req[lang], keyboard=[[button_main[lang]]], one_time=True)
                            return DISCRIPTION
                        else:
                            super().show_message(update, context, text_error[lang])
                            self.employer_menu(update, context)
                            return ConversationHandler.END
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_title_length[lang])
                return TITLE
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # handles job company,  saves it to the database,  and continues to asking job discription
    @preprocess
    def job_company(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if len(text) < 50 and len(text) > 1:
                if text == button_skip[lang]:
                    text = "not specified"
                if db.add_job_company(chat_id, text):
                    super().keyboard(update=update, context=context, text=text_job_discription_req[lang], keyboard=[[button_main[lang]]], one_time=True)
                    return DISCRIPTION
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_company_length[lang])
                return COMPANY
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # handles job discription,  saves it to the database,  and continues to asking job type
    @preprocess
    def job_discription(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if len(text) > 5:
                if db.add_job_discription(chat_id, text):
                    # Ask the user for the job type
                    keyboard = [[button_permanent[lang], button_part[lang]], [button_contract[lang], button_hour[lang]], [button_remote[lang], button_main[lang]]]
                    super().keyboard(update=update, context=context, text=text_job_type_req[lang], keyboard=keyboard, one_time=True)
                    return TYPE
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_discription_length[lang])
                return DISCRIPTION
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # handles job type, saves it to the database,  and continues to asking job job category
    @preprocess
    def job_type(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^({}|{}|{}|{}|{})$".format(button_permanent[lang], button_part[lang], button_contract[lang], button_hour[lang], button_remote[lang]), text):
                if text == button_permanent[lang]:
                    text ="Permanent"
                elif text == button_part[lang]:
                    text = "Part Time"
                elif text == button_contract[lang]:
                    text = "Contractual"
                elif text == button_remote[lang]:
                    text = "Remote"
                else:
                    text = "Hourly"
                
                if db.add_job_type(chat_id, text):
                    # Ask the user for the job category
                    keyboard = [[button_software[lang], button_business[lang]], [button_graphics[lang], button_web[lang]], [button_music[lang], button_video[lang]], [button_tutor[lang], button_other[lang]], [button_main[lang]]]
                    super().keyboard(update=update, context=context, text=text_job_cat_req[lang], keyboard=keyboard, one_time=True)
                    return CAT
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_option_below[lang])
                return TYPE
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # handles job category, saves it to the database,  and continues to asking job level
    @preprocess
    def job_cat(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^({}|{}|{}|{}|{}|{}|{}|{})$".format(button_software[lang], button_business[lang], button_web[lang], button_graphics[lang], button_music[lang], button_video[lang], button_tutor[lang], button_other[lang]), text):
                if text == button_software[lang]:
                    text ="software"
                elif text == button_business[lang]:
                    text = "bussiness"
                elif text == button_web[lang]:
                    text = "website_design"
                elif text == button_graphics[lang]:
                    text = "graphics"
                elif text == button_music[lang]:
                    text = "music_art"
                elif text == button_video[lang]:
                    text = "video_editing"
                elif text == button_tutor[lang]:
                    text = "tutor"
                else:
                    text = "other"
                 
                if db.add_job_cat(chat_id, text):
                    # Ask the user for the job prorposal limit
                    keyboard = [[button_entery[lang]], [button_intermidiate[lang]], [button_expert[lang]], [button_main[lang]]]
                    super().keyboard(update=update, context=context, text=text_job_level_req[lang], keyboard=keyboard, one_time=True)
                    return LEVEL
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_option_below[lang])
                return CAT
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # handles job level, saves it to the database,  and continues to asking job proposals limit
    @preprocess
    def job_level(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^({}|{}|{})$".format(button_entery[lang], button_intermidiate[lang], button_expert[lang]), text):
                if text == button_entery[lang]:
                    level = 0
                elif text == button_intermidiate[lang]:
                    level = 1
                else:
                    level = 2
                if db.add_job_level(chat_id, level):
                    # Ask the user for the job prorposal limit
                    keyboard = [[button_10[lang]], [button_20[lang]], [button_30[lang]], [button_main[lang]]]
                    super().keyboard(update=update, context=context, text=text_job_limit_req[lang], keyboard=keyboard, one_time=True)
                    return LIMIT
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_option_below[lang])
                return LEVEL
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # handles job proposals limit, saves it to the database,  and continues to asking job job price
    @preprocess
    def job_limit(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^({}|{}|{})$".format(button_10[lang], button_20[lang], button_30[lang]), text):
                limit = 1
                if text == button_10[lang]:
                    limit = 10
                elif text == button_20[lang]:
                    limit = 20
                else:
                    limit = 30
                if db.add_job_limit(chat_id, limit):
                    # Ask the user for the price
                    super().keyboard(update=update, context=context, text=text_job_price_req(db.get_job_with_chat_id(chat_id=chat_id, status="edit"))[lang], keyboard=[[button_main[lang]]], one_time=True)
                    return PRICE
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_option_below[lang])
                return LIMIT
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # handles the job price, saves it to the database and continues to asking deposit... 
    @preprocess
    def job_price(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^([0-9]*)$", text):
                data = db.get_job_with_chat_id(chat_id, "edit")
                if data["type"] == "Permanent" or data["type"] == "Part Time" or data["type"] == "Contractual" or data["type"] == "Remote":
                    if int(text) < 50:
                        super().show_message(update, context, text_permanent_price[lang])
                        return PRICE
                elif data["type"] == "Hourly":
                    if int(text) < 10:
                        super().show_message(update, context, text_hourly_price[lang])
                        return PRICE

                if db.add_job_price(chat_id, text):
                    # Ask the user for the job deposit if it is a contractual job
                    if data["type"] == "Contractual":
                        keyboard = [[button_yes[lang], button_no[lang]], [button_main[lang]]]
                        super().keyboard(update=update, context=context, text=text_job_deposit_req[lang], keyboard=keyboard, one_time=True)
                        return DEPOSIT
                    else:
                        self.show_job(update, context)
                        self.employer_menu(update, Contact)
                        return ConversationHandler.END
                else:
                    super().show_message(update, context, text_error[lang])
                    self.employer_menu(update, context)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_numbers_only[lang])
                return PRICE
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END
    
    # Handles job deposit and saves it to the database...
    @preprocess
    def job_deposit(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^({}|{})$".format(button_yes[lang], button_no[lang]), text):
                if text == button_yes[lang]:
                    # check if the user has the ammount of money that the job requires
                    # if true, display message with job price info and with an inline button to approve, then return ro employer menu
                    # if false, display a message "not enough balance", and return to menu
                    if db.check_job_price(chat_id):
                        data = db.get_job_with_chat_id(chat_id, "edit")
                        if len(data) > 0:
                            job_id = data["job_id"]
                            super().inline_keyboard(update=update, context=context, text=text_enough_balance(data["price"])[lang], keyboard=[[[button_cancel[lang], f"cnd{job_id}"], [button_continue[lang], f"apd{job_id}"]]])
                            self.employer_menu(update, Contact)
                            return ConversationHandler.END
                        else:
                            super().show_message(update, context, text_error[lang])
                            self.employer_menu(update, context)
                            return ConversationHandler.END
                    else:
                        super().show_message(update, context, text_not_enough_balance[lang])
                        self.employer_menu(update, Contact)
                        return ConversationHandler.END
                else:
                    self.show_job(update, context)
                    self.employer_menu(update, Contact)
                    return ConversationHandler.END
            else:
                super().show_message(update, context, text_option_below[lang])
                return DEPOSIT
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # shows a job with an inline buttons [edit, submit]
    @preprocess
    def show_job(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        job = db.get_job_with_chat_id(chat_id, "edit")
        user = db.get_user_profile(chat_id)
        if len(job) > 0 and len(user) > 0:
            job_id = job["job_id"]
            inline_keyboard = [[[button_edit[lang], f"edit{job_id}"], [button_submit[lang], f"sub{job_id}"]]]
            bot = db.get_bot_profile()
            formatted_text = fm.format_job(data=job, user=user, for_channel=False) + text_job_coin(bot)[lang]
            # display the job for the user, and Give options to either edit or submit 
            super().inline_keyboard(update=update, context=context, text=formatted_text, keyboard=inline_keyboard, parse=ParseMode.HTML)

    # Displays the jobs menu
    @preprocess
    def jobs_menu(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        menu = [[button_opened[lang], button_closed[lang]], [button_pending[lang], button_declined[lang]], [button_main[lang]]]
        super().keyboard(update, context, text_welcome[lang], menu, False)
        return JOBS_MENU

    # Handles the data coming from jobs menu
    @preprocess
    def jobs(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^({}|{}|{}|{})$".format(button_opened[lang], button_closed[lang], button_pending[lang], button_declined[lang]), text):
                user = db.get_user_profile(chat_id=chat_id)
                if text == button_opened[lang]:
                    data = db.get_job_with_status(chat_id, "opened")
                    if len(data) > 0:
                        for job in data:
                            formatted_text = fm.format_job(data=job, user=user, for_channel=False)
                            job_id = job["job_id"]
                            super().inline_keyboard(update=update, context=context, text=formatted_text, parse=ParseMode.HTML, keyboard=[[[button_close[lang], f"close{job_id}"]]])
                    else:
                        super().show_message(update, context, text_jobs("opened")["eng"])

                elif text == button_closed[lang]:
                    data = db.get_job_with_status(chat_id, "closed")
                    if len(data) > 0:
                        for job in data:
                            formatted_text = fm.format_job(data=job, user=user, for_channel=False)
                            super().show_message(update=update, context=context, text=formatted_text, parse=ParseMode.HTML)
                    else:
                        super().show_message(update, context, text_jobs("closed")["eng"])
                elif text == button_pending[lang]:
                    data = db.get_job_with_status(chat_id, "pending")
                    if len(data) > 0:
                        for job in data:
                            formatted_text = fm.format_job(data=job, user=user, for_channel=False)
                            super().show_message(update=update, context=context, text=formatted_text, parse=ParseMode.HTML)
                    else:
                        super().show_message(update, context, text_jobs("pending")["eng"])
                elif text == button_declined[lang]:
                    data = db.get_job_with_status(chat_id, "declined")
                    if len(data) > 0:
                        for job in data:
                            formatted_text = fm.format_job(data=job, user=user, for_channel=False)
                            super().show_message(update=update, context=context, text=formatted_text, parse=ParseMode.HTML)
                    else:
                        super().show_message(update, context, text_jobs("declined")["eng"])
            else:
                super().show_message(update, context, text_option_below[lang])
                return JOBS_MENU
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # Displays admin menu 
    @preprocess_admin
    def admin_menu(self, update: Update, context: CallbackContext) -> None:
        keyboard = [["Status", "Approve jobs"], ["Show users", "Show banned"], ["Other commands", "Log out"]]
        super().keyboard(update, context, text_welcome_admin["eng"], keyboard, False)

    # Displays 5 pending jobs with an inline button to decline or to approve
    @preprocess_admin
    def approve_jobs(self, update: Update, context: CallbackContext) -> None:
        data = db.get_jobs_with_status("pending")
        if len(data) > 0:
            for job in data:
                job_id = job["job_id"]
                user = db.get_user_profile(job["chat_id"])
                formatted_text = fm.format_job_for_admin(job, user)
                super().inline_keyboard(update, context, formatted_text, parse=ParseMode.HTML, keyboard=[[["Decline", f"dej{job_id}"], ["Approve", f"apj{job_id}"]]])
        else:
            super().show_message(update, context, text_no_jobs_approved["eng"])

    # Displays 5 pending verify requests
    @preprocess_admin
    def verify_requests(self, update: Update, context: CallbackContext) -> None:
        data = db.get_verify_with_status("pending")
        if len(data) > 0:
            for verify in data:
                verify_id = verify["verify_id"]
                formatted_text = fm.format_verify_for_admin(verify)
                keyboard=[[InlineKeyboardButton(text="Decline", callback_data=f"dev{verify_id}"), InlineKeyboardButton(text="Approve", callback_data=f"apv{verify_id}")]]
                context.bot.sendPhoto(chat_id=update.message.chat_id, photo=verify["photo_id"], caption=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            super().show_message(update, context, "There are no requests to verify.")
    
    # Displays pending cashout requests
    @preprocess_admin
    def approve_cashouts(self, update: Update, context: CallbackContext) -> None:
        data = db.get_cashout_with_status("pending")
        if len(data) > 0:
            for cashout in data:
                cashout_id = cashout["cashout_id"]
                user = db.get_user_profile(cashout["chat_id"])
                formatted_text = fm.format_cashout_for_admin(cashout=cashout, user=user)
                keyboard=[[InlineKeyboardButton(text="Decline", callback_data=f"decash{cashout_id}"), InlineKeyboardButton(text="Approve", callback_data=f"apcash{cashout_id}")]]
                context.bot.sendMessage(chat_id=update.message.chat_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            super().show_message(update, context, "There are no cashouts to approve.")
    
    # Approves update level request and sends notification      
    @preprocess_admin
    def update_level(self, update: Update, context: CallbackContext) -> None:
        data = db.get_update_with_status("pending")
        if len(data) > 0:
            for update_req in data:
                update_id = update_req["update_id"]
                user = db.get_user_profile(update_req["chat_id"])
                formatted_text = fm.format_update_for_admin(user=user)
                keyboard=[[InlineKeyboardButton(text="Decline", callback_data=f"deup{update_id}"), InlineKeyboardButton(text="Approve", callback_data=f"apup{update_id}")]]
                context.bot.sendMessage(chat_id=update.message.chat_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            super().show_message(update, context, "There are no update requests to approve.")

    # Displays bot status 
    @preprocess_admin
    def show_bot_status(self, update: Update, context: CallbackContext) -> None:
        data = db.get_bot_status()
        if len(data) > 0:
            formatted_text = fm.format_bot_status(data)
            super().inline_keyboard(update, context, formatted_text, parse=ParseMode.HTML, keyboard=[[[button_mark["eng"], "mrk"]]])
        else:
            super().show_message(update, context, text_error["eng"])
            
    # Displays users with their chat_id and username if available 
    @preprocess_admin
    def show_users(self, update: Update, context: CallbackContext) -> None:
        data = db.get_users('active', 0, self.users_per_text)
        if len(data) > 0:
            formatted_text = fm.format_users_list(data, 1)
            super().inline_keyboard(update, context, formatted_text, keyboard=[[["⏪", "pru0"], ["⏩", f"nxu{self.users_per_text}"]]])
        else:
            super().show_message(update, context, "There are no users to show.")

    # Displays other commands
    @preprocess_admin
    def other_commands(self, update: Update, context: CallbackContext) -> None:
        super().show_message(update=update, context=context, text=text_other_commands["eng"], parse=ParseMode.HTML)
    
    # Displays users with their job_posted count
    @preprocess_admin
    def show_users_with_job(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        _,_,jobs_posted = text.split(" ")
        jobs_posted = int(jobs_posted)
        data = db.get_users_with_job(jobs_posted, 0, self.users_per_text)
        if len(data) > 0:
            formatted_text = fm.format_users_with_job_list(data, jobs_posted, 1)
            super().inline_keyboard(update, context, formatted_text, keyboard=[[["⏪", f"prj0 {jobs_posted}"], ["⏩", f"nxj{self.users_per_text} {jobs_posted}"]]])
        else:
            super().show_message(update, context, "There are no users with this much job")

    # Displays banned users
    @preprocess_admin
    def show_banned(self, update: Update, context: CallbackContext) -> None:
        data = db.get_users('banned', 0, self.users_per_text)
        if len(data) > 0:
            formatted_text = fm.format_users_list(data, 1)
            super().inline_keyboard(update, context, formatted_text, keyboard=[[["⏪", "prb0"], ["⏩", f"nxb{self.users_per_text}"]]])
        else:
            super().show_message(update, context, "There are no banned users.")

    # Displays admins
    @preprocess_admin
    def show_admins(self, update: Update, context: CallbackContext) -> None:
        data = db.get_admins()
        if len(data) > 0:
            formatted_text = fm.format_admins_list(data)
            super().show_message(update, context, formatted_text)
        else:
            super().show_message(update, context, "There are no admins to show.")
    
    # Searchs for user profile using id and displays it to the admn        
    @preprocess_admin
    def search_user_by_id(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        id = int(text[4:])
        data = db.get_user_profile(id)
        if len(data) > 0:
            formatted_text = fm.format_profile_for_admin(data)
            super().show_message(update, context, formatted_text, parse=ParseMode.HTML)
        else:
            super().show_message(update, context, "There is no user with this user ID.")

    # Searchs for user profile using username and displays it to the admn        
    @preprocess_admin
    def search_user_by_username(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        _,username = text.split(" ")
        username = username.rstrip()
        data = db.get_user_profile_by_username(username)
        if len(data) > 0:
            formatted_text = fm.format_profile_for_admin(data=data)
            super().show_message(update, context, formatted_text, parse=ParseMode.HTML)
        else:
            super().show_message(update, context, "There is no user with this username.")

    # Searchs for user using id and bans it      
    @preprocess_admin
    def ban_user(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        id = int(text[4:])
        if not db.is_super_admin(id):
            if db.run_query("UPDATE users SET status='banned' WHERE chat_id={}".format(id)):
                super().show_message(update, context, text_success["eng"])
            else:
                super().show_message(update, context, text_error["eng"])
        else:
            super().show_message(update, context, "You can't ban a super admin.")

    # Searchs for user using id and unbans it      
    @preprocess_admin
    def unban_user(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        id = int(text[6:])
        if db.run_query("UPDATE users SET status='active' WHERE chat_id={}".format(id)):
            super().show_message(update, context, text_success["eng"])
        else:
            super().show_message(update, context, text_error["eng"])

    # Adds an admin using chat id
    @preprocess_admin
    def add_admin(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        text = text.split(" ")
        chat_id = update.message.chat_id
        if db.is_super_admin(chat_id=chat_id):
            if len(text) == 3:
                _,user_id,s = text
                if s == "true":
                    user_id = int(user_id) 
                    if db.add_admin(chat_id=user_id, super=True):
                        super().show_message(update, context, text_success["eng"])
                    else:
                        super().show_message(update, context, text_error["eng"])
            else:
                _,user_id = text
                user_id = int(user_id) 
                if db.add_admin(chat_id=user_id, super=False):
                    super().show_message(update, context, text_success["eng"])
                else:
                    super().show_message(update, context, text_error["eng"])
        else:
            super().show_message(update, context, "Only super admins can add admin.")

    # Removes an admin using chat id
    @preprocess_admin
    def remove_admin(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        id = int(text[7:])
        chat_id = update.message.chat_id
        if db.is_super_admin(chat_id=chat_id):
            if db.run_query("DELETE FROM admins WHERE chat_id={}".format(id)):
                super().show_message(update, context, text_success["eng"])
            else:
                super().show_message(update, context, text_error["eng"])
        else:
            super().show_message(update, context, "Only super admins can add admin.")

    # Displays job for the admin using job id
    @preprocess_admin
    def search_job(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        id = int(text[4:])
        data = db.get_job_with_id(id)
        if len(data) > 0:
            user = db.get_user_profile(data["chat_id"])
            formatted_text = fm.format_job_for_admin(data=data, user=user)
            super().show_message(update=update, context=context, text=formatted_text, parse=ParseMode.HTML)
        else:
            super().show_message(update, context, "There is no job with this job ID.")

    # handles close escrow request
    @preprocess_admin
    def close_escrow_admin(self, update: Update, context: CallbackContext) -> None:
        text = update.message.text
        _,job_id,paid = text.split(" ")
        job_id = int(job_id)
        if paid == "true":
            paid = True
            paid_text = "paid"
        else:
            paid = False
            paid_text = "not paid"

        if db.close_escrow(job_id=job_id, paid=paid):
            job = db.get_job_with_id(job_id=job_id)
            super().show_message(update, context, f"Job ID: {job_id}, is closed. and the freelancer is {paid_text}.")
            # text to the employer
            context.bot.sendMessage(chat_id=job["chat_id"], text=f"Job ID: {job_id}, is closed. and the freelancer is {paid_text}.")
            # text to the freelancer
            context.bot.sendMessage(chat_id=job["freelancer"], text=f"Job ID: {job_id}, is closed. and the freelancer is {paid_text}.")
        else:
            super().show_message(update=update, context=context, text=text_error["eng"]) 
    
    # Super admin updates bot
    @preprocess_admin
    def bot_updates(self, update: Update, context: CallbackContext) -> None:
        # Check if the admin is super
        chat_id = update.message.chat_id
        if db.run_query_fetchone("SELECT super FROM admins WHERE chat_id={}".format(chat_id))[0]:
            # Handle every bot update query
            text = update.message.text
            if len(text.split(" ")) > 1:
                text,num = text.split(" ")
                num = int(num)
            if text == "dtdec":
                if db.run_query(f"UPDATE bot SET delete_declined=NOT delete_declined"):
                    super().show_message(update=update, context=context, text=f"delete declined updated.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])

            elif text == "chlvl":
                if db.run_query(f"UPDATE bot SET check_level=NOT check_level"):
                    super().show_message(update=update, context=context, text=f"check level updated.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "jcoin":
                if db.run_query(f"UPDATE bot SET job_coin={num}"):
                    super().show_message(update=update, context=context, text=f"✅Job posting coin fee updated to {num}.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "pcoin":
                if db.run_query(f"UPDATE bot SET proposal_coin={num}"):
                    super().show_message(update=update, context=context, text=f"✅Proposal submitting coin fee updated to {num}.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "apfee":
                if db.run_query(f"UPDATE bot SET application_fee={num}"):
                    super().show_message(update=update, context=context, text=f"✅Application fee updated to {num}%.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "mdepo":
                if db.run_query(f"UPDATE bot SET minimum_deposit={num}"):
                    super().show_message(update=update, context=context, text=f"✅Minimum deposit updated to {num} birr.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "xdepo":
                if db.run_query(f"UPDATE bot SET maximum_deposit={num}"):
                    super().show_message(update=update, context=context, text=f"✅Maximum deposit updated to {num} birr.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "mcash":
                if db.run_query(f"UPDATE bot SET minimum_cashout={num}"):
                    super().show_message(update=update, context=context, text=f"✅Minimum cashout updated to {num} birr.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "xcash":
                if db.run_query(f"UPDATE bot SET maximum_cashout={num}"):
                    super().show_message(update=update, context=context, text=f"✅Maximum cashout updated to {num} birr.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "yenec":
                if db.run_query(f"UPDATE bot SET yenepay_cut={num}"):
                    super().show_message(update=update, context=context, text=f"✅Yenepay cut updated to {num}%.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
            elif text == "merch":
                if db.run_query(f"UPDATE bot SET merchant_id={num}"):
                    super().show_message(update=update, context=context, text=f"✅Merchant ID updated to {num}.")
                else:
                    super().show_message(update=update, context=context, text=text_error["eng"])
        else:
            context.bot.sendMessage(chat_id=chat_id, text=text_not_admin["eng"])
    
    # Displays a request for entering proposal discription and forwards it to proposal discription handler
    @preprocess
    def proposal_req(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        lang = self.get_lang(chat_id)
        text = query.data 
        job_id = text[8:]
        context.user_data["job_id"] = job_id
        if db.is_user_eligiable_to_apply(chat_id, job_id):
            if not db.run_query_fetchone("SELECT EXISTS(SELECT chat_id FROM proposals WHERE chat_id={} AND job_id={} AND status='sent')".format(chat_id, job_id))[0]:
                if db.create_proposal(chat_id, job_id):
                    context.bot.sendMessage(chat_id=chat_id, text=text_proposal_discription_req[lang], reply_markup=ReplyKeyboardMarkup([[button_main[lang]]], resize_keyboard=True))
                    return P_DISCRIPTION
                else:
                    context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
                    return ConversationHandler.END 
            else:
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_proposal_exists[lang])
                return ConversationHandler.END
        else:
            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_cant_apply[lang])
            return ConversationHandler.END

    # Displays a request for editing proposal discription and forwards it to proposal discription handler
    @preprocess
    def proposal_req_edit(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        lang = self.get_lang(chat_id)
        text = query.data 
        job_id = int(text[12:])
        context.user_data["job_id"] = job_id   
        if db.is_user_eligiable_to_apply(chat_id, job_id):
            if not db.run_query_fetchone("SELECT EXISTS(SELECT chat_id FROM proposals WHERE chat_id={} AND job_id={} AND status='sent')".format(chat_id, job_id))[0]:
                if db.create_proposal(chat_id, job_id):
                    context.bot.sendMessage(chat_id=chat_id, text=text_proposal_discription_req[lang], reply_markup=ReplyKeyboardMarkup([[button_main[lang]]], resize_keyboard=True))
                    return P_DISCRIPTION
                else:
                    context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
                    return ConversationHandler.END 
            else:
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_proposal_exists[lang])
                return ConversationHandler.END
        else:
            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_cant_apply[lang])
            return ConversationHandler.END
    
    # handles proposals discription, saves it to the database, and continues to asking other attributes of a proposal
    @preprocess
    def proposal_discription(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        job_id = context.user_data.get("job_id")
        if text != button_main[lang]:
                if len(text) > 15 and len(text) <= 250:
                    if db.run_query("UPDATE proposals SET discription='{}' WHERE chat_id={} and job_id={}".format(text, chat_id, job_id)):                        
                        job = db.get_job_with_id(job_id)
                        if job["type"] == "Contractual":
                            keyboard = [[button_days_1[lang], button_days_3[lang]], [button_days_7[lang], button_days_15[lang]], [button_days_30[lang], button_main[lang]]]
                            super().keyboard(update=update, context=context, text=text_proposal_days_req[lang], keyboard=keyboard, one_time=True)
                            return P_DAYS
                        else:
                            proposal = db.get_proposal_by_job_id(chat_id=chat_id, job_id=job_id)
                            proposal_id = proposal["proposal_id"]
                            user = db.get_user_profile(chat_id)
                            formatted_text = fm.format_proposal(job, proposal, user)
                            formatted_text += "\nPlease press <i>submit</i> to send your proposal to the employer, or press <i>edit</i> to edit it."
                            keyboard = [[[button_edit[lang], f"editproposal{job_id}"], [button_submit[lang], f"subproposal{proposal_id}"]]]
                            super().inline_keyboard(update=update, context=context, text=formatted_text, parse=ParseMode.HTML, keyboard=keyboard)
                            self.freelancer_menu(update, context)
                            return ConversationHandler.END 
                    else:
                        super().show_message(update, context, text_error[lang])
                        self.freelancer_menu(update, context)
                        return ConversationHandler.END
                else:
                    super().show_message(update, context, text_proposal_discription_length[lang])
                    return P_DISCRIPTION
        else:
            self.freelancer_menu(update, context)
            return ConversationHandler.END
    
    # handles proposals days, Saves it to the database and continues to asking proposal price
    @preprocess
    def proposal_days(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        job_id = context.user_data.get("job_id")
        if text != button_main[lang]:
            if re.match("^({}|{}|{}|{}|{})$".format(button_days_1[lang], button_days_3[lang], button_days_7[lang], button_days_15[lang], button_days_30[lang]), text):
                if text == button_days_1[lang]:
                    days = 1
                elif text == button_days_3[lang]:
                    days = 3
                elif text == button_days_7[lang]:
                    days = 7
                elif text == button_days_15[lang]:
                    days = 15
                else:
                    days = 30
                if db.run_query("UPDATE proposals SET days={} WHERE chat_id={} and job_id={}".format(days, chat_id, job_id)):
                    super().keyboard(update=update, context=context, text=text_proposal_price_req[lang], keyboard=[[button_main[lang]]], one_time=True)
                    return P_PRICE
            else:
                super().show_message(update, context, text_option_below[lang])
                return P_DAYS
        else:
            self.freelancer_menu(update, context)
            return ConversationHandler.END

    # handles proposals discription, saves it to the database,  and continues to asking proposal days limit
    @preprocess
    def proposal_price(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        job_id = context.user_data.get("job_id")
        if text != button_main[lang]:
            if re.match("^([0-9]*)$", text):
                job = db.get_job_with_id(job_id)
                if int(text) <= job["price"]:
                    if db.run_query("UPDATE proposals SET price={} WHERE chat_id={} and job_id={}".format(int(text), chat_id, job_id)):
                        # Ask the user for the job deposit
                        proposal = db.get_proposal_by_job_id(chat_id, job_id)
                        proposal_id = proposal["proposal_id"]
                        job_id = proposal["job_id"]
                        user = db.get_user_profile(chat_id)
                        formatted_text = fm.format_proposal(job, proposal, user)
                        formatted_text += "\nPlease press <i>submit</i> to send your proposal to the employer, or press <i>edit</i> to edit it."
                        keyboard = [[[button_edit[lang], f"editproposal{job_id}"], [button_submit[lang], f"subproposal{proposal_id}"]]]
                        super().inline_keyboard(update=update, context=context, text=formatted_text, parse=ParseMode.HTML, keyboard=keyboard)
                        self.freelancer_menu(update, context)
                        return ConversationHandler.END
                    else:
                        super().show_message(update, context, text_error[lang])
                        self.freelancer_menu(update, context)
                        return ConversationHandler.END
                else:
                    super().show_message(update, context, text_price_above_job(job)[lang])
                    return P_PRICE
            else:
                super().show_message(update, context, text_numbers_only[lang])
                return P_PRICE
        else:
            self.freelancer_menu(update, context)
            return ConversationHandler.END

    # Displays deposit req
    @preprocess
    def deposit_req(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        bot = db.get_bot_profile()
        super().keyboard(update=update, context=context, text=text_deposit_req(bot)[lang], keyboard=[[button_main[lang]]], one_time=False)
        return M_DEPOSIT

    # Handles deposit price
    @preprocess
    def handle_deposit_price(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^([0-9]*)$", text):
                bot = db.get_bot_profile()
                if int(text) >= bot["minimum_deposit"] and int(text) <= bot["maximum_deposit"]:
                    merchant_order_id = fm.generate_merchant_order_id(chat_id=chat_id)
                    link = fm.generate_deposit_link(merchant_order_id=merchant_order_id, chat_id=chat_id, price=int(text), bot=bot)
                    formatted_text = text_deposit_link(link)[lang]
                    super().show_message(update=update, context=context, text=formatted_text, parse=ParseMode.HTML)
                    self.login_menu(update, context)
                    return ConversationHandler.END
                else:
                    super().show_message(update, context, text_min_max_deposit(bot)[lang])
                    return M_DEPOSIT
            else:
                super().show_message(update, context, text_numbers_only[lang])
                return M_DEPOSIT
        else:
            self.login_menu(update, context)
            return ConversationHandler.END

    # Displays cashout req
    @preprocess
    def cashout_req(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        bot = db.get_bot_profile()
        super().keyboard(update=update, context=context, text=text_cashout_req(bot)[lang], keyboard=[[button_main[lang]]], one_time=False)
        return CASH

    # Handles cashout price, generates an inline keyboard to submit request to the admin
    @preprocess
    def handle_cashout_price(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        if text != button_main[lang]:
            if re.match("^([0-9]*)$", text):
                bot = db.get_bot_profile()
                if int(text) >= bot["minimum_cashout"] and int(text) <= bot["maximum_cashout"]:
                    user = db.get_user_profile(chat_id=chat_id)
                    formatted_text = text_cashout(user=user, price=int(text))[lang]
                    super().inline_keyboard(update=update, context=context, text=formatted_text, parse=ParseMode.HTML, keyboard=[[[button_cancel[lang], "mrk"], [button_submit[lang], f"cashout{text}"]]])
                    self.freelancer_menu(update, context)
                    return ConversationHandler.END
                else:
                    super().show_message(update, context, text_min_max_cashout(bot)[lang])
                    return CASH
            else:
                super().show_message(update, context, text_numbers_only[lang])
                return CASH
        else:
            self.login_menu(update, context)
            return ConversationHandler.END

    # Displays a rate message with inline button to enter the rate conversation
    @preprocess
    def rate_freelancer_req(self, update: Update, context: CallbackContext, chat_id: int, freelancer_id: int) -> int:
        lang = self.get_lang(chat_id)
        keyboard = [[InlineKeyboardButton(text=button_rate[lang], callback_data=f"rate{freelancer_id}")]]
        context.bot.sendMessage(chat_id=chat_id, text=text_rate_req[lang], reply_markup=InlineKeyboardMarkup(keyboard))
    
    # Displays a rate Conversation entery and forwards it to rate handler
    @preprocess
    def rate_freelancer(self, update: Update, context: CallbackContext) -> int:
        query = update.callback_query
        query.answer()
        chat_id = query.message.chat_id
        lang = self.get_lang(chat_id)
        text = query.data 
        context.user_data["freelancer_id"] = int(text[4:])
        context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_processing[lang])
        context.bot.sendMessage(chat_id=chat_id, text=text_rate_freelancer[lang], reply_markup=ReplyKeyboardMarkup([[button_main[lang]]]))
        return RATE
        
    # Handles a rate request, send alert message for freelancer
    @preprocess
    def rate_handler(self, update: Update, context: CallbackContext) -> int:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id)
        text = update.message.text
        freelancer_id = context.user_data.get("freelancer_id")
        if text != button_main[lang]:
            if re.match("^([0-9]*)$", text):
                if int(text) >= 1 and int(text) <= 10:
                    if db.rate_freelancer(chat_id=freelancer_id, rate=int(text)):
                        alert_text = fm.alert_message(text_rate_notification(employer_id=chat_id, rate=int(text))[self.get_lang(freelancer_id)])
                        context.bot.sendMessage(chat_id=freelancer_id, text=alert_text, parse_mode=ParseMode.HTML)
                        super().show_message(update, context, text_success[lang])
                        self.employer_menu(update, context)
                        return ConversationHandler.END
                    else:
                        super().show_message(update, context, text_error[lang])
                        self.employer_menu(update, context)
                        return ConversationHandler.END
                else:
                    super().show_message(update, context, text_rate_between[lang])
                    return RATE
            else:
                super().show_message(update, context, text_numbers_only[lang])
                return RATE
        else:
            self.employer_menu(update, context)
            return ConversationHandler.END

    # Handles every callback data coming from the inline keyboard
    @preprocess
    def inline_button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        chat_id = query.message.chat_id
        lang = self.get_lang(chat_id)
        text = query.data 
        query.answer()
        # Admin approves a job post request
        if re.match("^(apj[0-9]*)$", text):
            job_id = int(text[3:])
            data = db.get_job_with_id(job_id=job_id)
            if len(data) > 0:
                job_chat_id = data["chat_id"]
                if data["status"] == "pending":
                    user = db.get_user_profile(chat_id=chat_id)
                    formatted_text = fm.format_job(data=data, user=user, for_channel=True) 
                    msg = context.bot.sendMessage(chat_id=f"@{channel}", text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Apply", url=f"https://t.me/{bot_username}?start=jid{job_id}")]]))
                    if db.run_query("UPDATE jobs SET status='opened', message_id={} WHERE job_id={}".format(msg["message_id"], job_id)) and db.run_query("UPDATE users SET jobs_posted=jobs_posted+1, opened_jobs=opened_jobs+1 WHERE chat_id={}".format(job_chat_id)):
                        context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"Job id - {job_id} : has been approved✅.")
                        alert_text = fm.alert_message(text_job_approved(job=data)[self.get_lang(data["chat_id"])])
                        context.bot.sendMessage(chat_id=job_chat_id, text=alert_text, parse_mode=ParseMode.HTML)
                    else:
                        context.bot.deleteMessage(chat_id=f"@{channel}", message_id=msg["message_id"])
                        context.bot.sendMessage(chat_id, text_error[lang])
                else:
                    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"Job id - {job_id} : has been edited by other admin.")
            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
        
        # Admin declines a job post request
        elif re.match("^(dej[0-9]*)$", text):
            job_id = int(text[3:])
            data = db.get_job_with_id(job_id=job_id)
            if len(data) > 0 :
                job_chat_id = data["chat_id"]
                if data["status"] == "pending":
                    bot = db.get_bot_profile()
                    # Return money if job gets declined
                    if data["deposit"]:
                        if bot["delete_declined"] and db.run_query("DELETE FROM jobs WHERE job_id={}".format(job_id)):
                            pass
                        elif not bot["delete_declined"] and db.run_query("UPDATE jobs SET status='declined' WHERE job_id={}".format(job_id)):
                            pass
                        else:
                            context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
                            return
                        if db.run_query("UPDATE users SET balance=balance+{} WHERE chat_id={}".format(data["price"], data["chat_id"])):
                            user_lang = self.get_lang(data["chat_id"])
                            alert_text = fm.alert_message(text_money_back_job(data)[user_lang])
                            context.bot.sendMessage(chat_id=chat_id, text=alert_text, parse_mode=ParseMode.HTML)
                        else:
                            context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
                            return
                    else:                      
                        if bot["delete_declined"] and db.run_query("DELETE FROM jobs WHERE job_id={}".format(job_id)):
                            pass
                        elif not bot["delete_declined"] and db.run_query("UPDATE jobs SET status='declined' WHERE job_id={}".format(job_id)):
                            pass
                        else:
                            context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
                            return

                    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"Job id - {job_id} : has been declined❌.")
                    alert_text = fm.alert_message(text_job_declined(job=data)[self.get_lang(data["chat_id"])])
                    context.bot.sendMessage(chat_id=job_chat_id, text=alert_text, parse_mode=ParseMode.HTML)
                else:
                    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"Job id - {job_id} : has been edited by other admin.")

            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
        
        # User submits a job
        elif re.match("^(sub[0-9]*)$", text):
            job_id = int(text[3:])   
            # Handle decducting coins depending on the level of the job
            # job = db.get_job_with_id(job_id)
            # if job["level"] > 0:
            #     profile = db.get_user_profile(chat_id)
            #     if job["level"] == 1:
            #         if profile["coin"] >= 10:
            #             coin = profile["coin"] - 10
            #             if db.run_query("UPDATE users SET coin={} WHERE chat_id={}".format(coin, chat_id)) and db.run_query("UPDATE jobs SET status='pending' WHERE job_id={}".format(job_id)):
            #                 context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_job_sent[lang])
            #             else:
            #                 context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
            #         else:
            #             context.bot.sendMessage(chat_id=chat_id, text=text_not_enough_coins[lang])
            #     elif job["level"] == 2:
            #         if profile["coin"] >= 15:
            #             coin = profile["coin"] - 15
            #             if db.run_query("UPDATE users SET coin={} WHERE chat_id={}".format(coin, chat_id)) and db.run_query("UPDATE jobs SET status='pending' WHERE job_id={}".format(job_id)):
            #                 context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_job_sent[lang])
            #             else:
            #                 context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
            #         else:
            #             context.bot.sendMessage(chat_id=chat_id, text=text_not_enough_coins[lang])

            if db.submit_job(chat_id=chat_id, job_id=job_id):
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_job_sent[lang])
            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_cant_sub_job[lang])
            
        elif re.match("^(edit[0-9]*)$", text):
            context.bot.sendMessage(chat_id=chat_id, text=text_edit_job_req[lang])
            
        elif re.match("^(mrk)$", text):
            # Delete message
            context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
        
        # Approves deposit to a job
        elif re.match("^(apd[0-9]*)$", text):
            job_id = text[3:]
            if db.job_deposit(chat_id=chat_id, job_id=job_id): 
                data = db.get_job_with_id(job_id)
                user = db.get_user_profile(chat_id=chat_id)               
                formatted_text = fm.format_job(data=data, user=user, for_channel=False)
                # display the job for the user, and Give options to either edit or submit 
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_job_deposit_made[lang])
                context.bot.sendMessage(chat_id=chat_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=button_edit[lang], callback_data=f"edit{job_id}"), InlineKeyboardButton(text=button_submit[lang], callback_data=f"sub{job_id}")]]))
            else:
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_processing[lang])
                context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
        
        # Calcels a deposit to a job
        elif re.match("^(cnd[0-9]*)$", text):
            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_canceled[lang])

        # Handles Previous and Next inline buttons
        elif re.match("^(pru[0-9]*)|(nxu[0-9]*)|(prb[0-9]*)|(nxb[0-9]*)|(prj[0-9]* [0-9]*)|(nxj[0-9]* [0-9]*)$", text):
            
            ls = text.split(" ")
            if len(ls) <= 1:
                offset = int(text[3:]) 
            else:
                offset = int(ls[0][3:]) 
            data = {}
            if text[0:3] == "nxu" or text[0:3] == "pru":
                data = db.get_users("active", offset, self.users_per_text)
            elif text[0:3] == "nxb" or text[0:3] == "prb":
                data = db.get_users("banned", offset, self.users_per_text)
            elif text[0:3] == "nxj" or text[0:3] == "prj":
                data = db.get_users_with_job(int(ls[1]), offset, self.users_per_text)
 
            if len(data) > 0:
                pr_offset = 0
                nx_offset = self.users_per_text
                if text[0] == "n":
                    if offset >= (self.users_per_text * 2):
                        pr_offset = offset - self.users_per_text
                    nx_offset = offset + self.users_per_text
                else:
                    if offset >= self.users_per_text:
                        pr_offset = offset - self.users_per_text
                        nx_offset = offset + self.users_per_text
                if text[0:3] == "nxj" or text[0:3] == "prj":
                    jobs_posted = int(ls[1])
                    formatted_text = fm.format_users_with_job_list(data, jobs_posted, nx_offset)
                    keyboard=[[InlineKeyboardButton(text="⏪", callback_data=f"pr{text[2]}{pr_offset} {jobs_posted}"), InlineKeyboardButton(text="⏩", callback_data=f"nx{text[2]}{nx_offset} {jobs_posted}")]]
                    query.edit_message_text(text=formatted_text, reply_markup=InlineKeyboardMarkup(keyboard))
                else:
                    formatted_text = fm.format_users_list(data, nx_offset)
                    keyboard=[[InlineKeyboardButton(text="⏪", callback_data=f"pr{text[2]}{pr_offset}"), InlineKeyboardButton(text="⏩", callback_data=f"nx{text[2]}{nx_offset}")]]
                    query.edit_message_text(text=formatted_text, reply_markup=InlineKeyboardMarkup(keyboard))
        
        # Handle verify button
        elif re.match("^(verify)$", text):
            context.bot.sendMessage(chat_id=chat_id, text=text_verify_image_req[lang])
        
        # Handle submiting verify
        elif re.match("^(sverify[0-9]*)$", text):
            verify_id = int(text[7:])
            if db.run_query("UPDATE verify SET status='pending' WHERE verify_id={}".format(verify_id)):
                context.bot.edit_message_caption(chat_id=chat_id, message_id=query.message.message_id, caption=text_verify_sent["eng"])
            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
        # Admin aproves verify request button
        elif re.match("^(apv[0-9]*)$", text):
            verify_id = int(text[3:])
            data = db.get_verify(verify_id=verify_id)
            if len(data) > 0 :
                company = data["company"]
                verify_chat_id = data["chat_id"]
                if data["status"] == "pending":
                    if db.run_query("UPDATE users SET verified=true, company='{}' WHERE chat_id={}".format(company, verify_chat_id)) and db.run_query("DELETE FROM verify WHERE verify_id={}".format(verify_id)):
                        context.bot.editMessageCaption(chat_id=chat_id, message_id=query.message.message_id, caption=f"verify - {verify_id} : has been approved✅.")
                        formatted_text = fm.alert_message(text_verify_approved(verify=data)[self.get_lang(data["chat_id"])])
                        context.bot.sendMessage(chat_id=verify_chat_id, text=formatted_text, parse_mode=ParseMode.HTML)
                    else:
                        context.bot.sendMessage(chat_id, text_error[lang])
                else:
                    context.bot.editMessageCaption(chat_id=chat_id, message_id=query.message.message_id, caption=f"Verify ID - {verify_id} : has been edited by other admin.")
            else:
                context.bot.sendMessage(chat_id=chat_id, text=f"Verify ID - {verify_id} does NOT exist. It might have been edited by other admin.")
       
        # Admin declines verify request button
        elif re.match("^(dev[0-9]*)$", text):
            verify_id = int(text[3:])
            data = db.get_verify(verify_id=verify_id)
            if len(data) > 0 :
                company = data["company"]
                verify_chat_id = data["chat_id"]
                if data["status"] == "pending":
                    if db.run_query("DELETE FROM verify WHERE verify_id={}".format(verify_id)):
                        context.bot.editMessageCaption(chat_id=chat_id, message_id=query.message.message_id, caption=f"verify id - {verify_id} : has been declined❌.")             
                        formatted_text = fm.alert_message(text_verify_declined(verify=data)[self.get_lang(data["chat_id"])])
                        context.bot.sendMessage(chat_id=verify_chat_id, text=formatted_text, parse_mode=ParseMode.HTML)
                    else:
                        context.bot.sendMessage(chat_id, text_error[lang])
                else:
                    context.bot.editMessageCaption(chat_id=chat_id, message_id=query.message.message_id, caption=f"Verify ID - {verify_id} : has been edited by other admin.")

            else:
                context.bot.sendMessage(chat_id=chat_id, text=f"Verify ID - {verify_id} does NOT exist. It might have been edited by other admin.")

        # Changes language preference
        elif re.match("^(lang eng)|(lang amh)$", text):
            _,lang = text.split(" ")
            if db.run_query("UPDATE users SET lang='{}' WHERE chat_id={}".format(lang, chat_id)):
                self.login_menu(update, context, chat_id)
            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
        
        # Handles submit proposal button
        elif re.match("^(subproposal[0-9]*)$", text):
            proposal_id = int(text[11:])
            proposal = db.get_proposal_by_id(proposal_id)
            job_id = proposal["job_id"]
            job = db.get_job_with_id(job_id)
            if job["status"] == "opened" and proposal["status"] == "edit":
                if db.run_query("UPDATE proposals SET status='sent' WHERE proposal_id={}".format(proposal_id)):
                    keyboard = [[InlineKeyboardButton(text=button_assign[lang], callback_data=f"assign{job_id} {chat_id} {proposal_id}")]]
                    user = db.get_user_profile(chat_id)
                    formatted_text = fm.format_proposal(job, proposal, user)
                    lang_employer = self.get_lang(job["chat_id"])
                    mention_user = mention_html(user_id=chat_id, name="here")
                    user_text = "\n<i>To contact this freelancer press</i> " + mention_user
                    formatted_text += text_press_asign[lang_employer] + user_text
                    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_proposal_sent[lang])
                    if job["type"] == "contractual":
                        context.bot.sendMessage(chat_id=job["chat_id"], text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
                    else:
                        context.bot.sendMessage(chat_id=job["chat_id"], text=formatted_text, parse_mode=ParseMode.HTML)
                else:
                    context.bot.sendMessage(chat_id=chat_id, text=text_error["eng"])
            else:
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_proposal_not_sent[lang])
                
        # Checks all the needed requirements and asigns a job to a certain freelancer...
        elif re.match("^(assign[0-9]* [0-9]* [0-9]*)$", text):
            job_id, user_id, proposal_id = text.split(" ")
            job_id = int(job_id[6:])
            user_id = int(user_id)
            proposal_id = int(proposal_id)
            job = db.get_job_with_id(job_id)
            if job["freelancer"] == -1 and job["counter_f"] < assign_count and job["status"] == "opened":
                keyboard = [[InlineKeyboardButton(text=button_deassign[lang], callback_data=f"deassign{job_id} {user_id} {proposal_id}")]]
                freelancer_lang = self.get_lang(user_id)
                if job["deposit"]:
                    if db.run_query("UPDATE jobs SET freelancer={}, counter_f=counter_f+1 WHERE job_id={}".format(user_id, job_id)):
                        query.edit_message_text(text=text_assigned_deposit(user_id)[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))                      
                        freelancer_text = fm.alert_message(text_proposal_assigned(job)[freelancer_lang])
                        context.bot.sendMessage(chat_id=user_id, text=freelancer_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=button_continue[freelancer_lang], callback_data=f"accept_job{job_id} {proposal_id}")]]))
                    else:
                        context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
                else:
                    if db.run_query("UPDATE jobs SET freelancer={}, counter_f=counter_f+1 WHERE job_id={}".format(user_id, job_id)):
                        query.edit_message_text(text=text_assigned(user_id)[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
                        context.bot.sendMessage(chat_id=chat_id, text=text_no_escrow[lang])
                        freelancer_text = fm.alert_message(text_proposal_assigned_no_deposit(job)[freelancer_lang])
                        context.bot.sendMessage(chat_id=user_id, text=freelancer_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=button_mark[freelancer_lang], callback_data="mrk")]]))
                    else:
                        context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])

            else:
                context.bot.sendMessage(chat_id, text_cant_assign[lang])
        
        # Checks all the needed requirements and deassigns a freelancer from a certain job...//work remains in deposit
        elif re.match("^(deassign[0-9]* [0-9]* [0-9]*)$", text):
            job_id, user_id, proposal_id = text.split(" ")
            job_id = int(job_id[8:])
            user_id = int(user_id)
            proposal_id = int(proposal_id)
            job = db.get_job_with_id(job_id)
            if job["status"] == "opened" and job["freelancer"] == user_id:
                keyboard = [[InlineKeyboardButton(text=button_assign[lang], callback_data=f"assign{job_id} {user_id} {proposal_id}")]]
                freelancer_lang = self.get_lang(user_id)
                if job["deposit"]:
                    # Check if the job is in escrow if true, Check if the job is started if also true tell the employer that he can't deasign the job since it is in escrow and tell him to contact the admin
                    if db.can_deassign(job_id=job_id):
                        # deassign the job
                        if db.run_query("DELETE FROM escrow WHERE job_id={}".format(job_id)) and db.run_query("UPDATE jobs SET freelancer=-1, escrow_id=-1 WHERE job_id={}".format(job_id)):
                            query.edit_message_text(text=text_deassigned(user_id)[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
                            context.bot.sendMessage(chat_id, text_success[lang]) 
                            freelancer_text = fm.alert_message(text_proposal_deassigned(job)[freelancer_lang])
                            context.bot.sendMessage(chat_id=user_id, text=freelancer_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=button_mark[lang], callback_data="mrk")]]))
                        else:
                            context.bot.sendMessage(chat_id, text_error[lang])
                    else:
                        # Display message can't deassign and contact admin
                        keyboard = [[InlineKeyboardButton(text=button_admin[lang], callback_data="admins")]]
                        context.bot.sendMessage(chat_id, text_is_in_escrow[lang], reply_markup=InlineKeyboardMarkup(keyboard))
                else:
                    if db.run_query("UPDATE jobs SET freelancer=-1 WHERE job_id={}".format(job_id)):
                        query.edit_message_text(text=text_deassigned(user_id)[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
                        context.bot.sendMessage(chat_id, text_success[lang])
                        freelancer_text = fm.alert_message(text_proposal_deassigned(job)[freelancer_lang])
                        context.bot.sendMessage(chat_id=user_id, text=freelancer_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text=button_mark[lang], callback_data="mrk")]])) 
                    else:
                        context.bot.sendMessage(chat_id=chat_id, text=text_error[lang])
            else:
                context.bot.sendMessage(chat_id, text_cant_deassign[lang])
        
        # Close a job
        elif re.match("^(close[0-9]*)$", text):
            job_id = int(text[5:])
            job = db.get_job_with_id(job_id)
            if job["status"] == "opened":
                user = db.get_user_profile(chat_id=chat_id)
                formatted_text = fm.format_job(data=job, user=user, for_channel=True)
                formatted_text = "----------<i>Closed</i>----------\n" + formatted_text + "----------<i>Closed</i>----------\n"
                if job["deposit"]:
                    if db.run_query_fetchone("SELECT EXISTS(SELECT job_id FROM escrow WHERE job_id={})".format(job_id)) and db.run_query_fetchone("SELECT working FROM escrow WHERE job_id={}".format(job_id))[0]:
                        keyboard = [[InlineKeyboardButton(text=button_admin[lang], callback_data="admins"), InlineKeyboardButton(text=button_continue[lang], callback_data=f"close_escrow{job_id}")]]
                        context.bot.sendMessage(chat_id=chat_id, text=text_must_pay[lang], reply_markup=InlineKeyboardMarkup(keyboard))
                    else:
                        job = db.get_job_with_id(job_id)
                        if db.close_job_deposit(job):
                            context.bot.editMessageText(chat_id=f"@{channel}", message_id=job["message_id"], text=formatted_text, parse_mode=ParseMode.HTML)
                            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_job_closed["eng"])
                            alert_text = fm.alert_message(text_money_back_job(job)[lang])
                            context.bot.sendMessage(chat_id=chat_id, text=alert_text, parse_mode=ParseMode.HTML)
                        else:
                            context.bot.sendMessage(chat_id, text_error[lang])
                else:
                    # Close the job and send a message to the freelancer stating that the job has been closed, and send a rate freelancer request
                    if db.close_job_no_deposit(job):
                        context.bot.editMessageText(chat_id=f"@{channel}", message_id=job["message_id"], text=formatted_text, parse_mode=ParseMode.HTML)
                        context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_job_closed["eng"])
                        if job["freelancer"] != -1:
                            self.rate_freelancer_req(update, context, chat_id, job["freelancer"])
                            alert_text = fm.alert_message(text_job_closed_no_deposit(job)["eng"])
                            context.bot.sendMessage(chat_id=job["freelancer"], text=alert_text, parse_mode=ParseMode.HTML)
                    else:
                        context.bot.sendMessage(chat_id, text_error[lang])
            else:
                context.bot.sendMessage(chat_id, text_job_already_closed[lang])
        
        # Admins list provider
        elif re.match("^(admins)$", text):
            admins = db.get_admins_username()
            if len(admins) > 0:
                formatetd_text = fm.format_admins_username(admins)
                context.bot.sendMessage(chat_id=chat_id, text=formatetd_text, parse_mode=ParseMode.HTML)
            else:
                context.bot.sendMessage(chat_id, text_no_admins_found[lang])

        # Update escrow working to false and update the paid attribute and close the escrow
        elif re.match("^(close_escrow[0-9]*)$", text):
            job_id = int(text[12:])
            if db.close_escrow(job_id=job_id, paid=True):
                job = db.get_job_with_id(job_id)
                user = db.get_user_profile(chat_id=chat_id)
                formatted_text = fm.format_job(data=job, user=user, for_channel=True)
                formatted_text = "----------<i>Closed</i>----------\n" + formatted_text + "----------<i>Closed</i>----------\n"
                context.bot.editMessageText(chat_id=f"@{channel}", message_id=job["message_id"], text=formatted_text, parse_mode=ParseMode.HTML)
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_job_closed["eng"])
                escrow = db.get_escrow(job_id=job_id)
                proposal = db.get_proposal_by_id(proposal_id=escrow["proposal_id"])
                alert_text = fm.alert_message(text_payment_employer(proposal)[lang])
                context.bot.sendMessage(chat_id=chat_id, text=alert_text, parse_mode=ParseMode.HTML)
                self.rate_freelancer_req(update, context, chat_id, job["freelancer"])
                # Send notification message for the freelancer about payment
                alert_text = fm.alert_message(text_payment_freelancer(job)[self.get_lang(job["freelancer"])])
                context.bot.sendMessage(chat_id=job["freelancer"], text=alert_text, parse_mode=ParseMode.HTML)
            else:
                context.bot.sendMessage(chat_id, text_error[lang])

        # Freelancer accepts job offer, anf gets added to the escrow service
        elif re.match("^(accept_job[0-9]* [0-9]*)$", text):
            job_id, proposal_id = text.split(" ")
            job_id = int(job_id[10:])
            proposal_id = int(proposal_id)
            if db.add_to_escrow(chat_id=chat_id, job_id=job_id, proposal_id=proposal_id):
                job = db.get_job_with_id(job_id)
                context.bot.editMessageText(chat_id=chat_id,  message_id=query.message.message_id, text=text_escrow_added_freelancer[lang])
                alert_text = fm.alert_message(text_job_accepted(job)[self.get_lang(job["chat_id"])])
                context.bot.sendMessage(chat_id=job["chat_id"], text=alert_text, parse_mode=ParseMode.HTML)
            else:
                context.bot.sendMessage(chat_id, text_error[lang])

        # Handles cashout submit req
        elif re.match("^(cashout[0-9]*)$", text):
            price = int(text[7:])
            if db.process_cashout(chat_id=chat_id, price=price):
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_cashout_sent[lang])
            else:
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=text_not_enough_balance[lang])
        
        # Super admin handles cashout
        elif re.match("^(apcash[0-9]*)|(decash[0-9]*)$", text):
            # Check if the admin is super
            if db.run_query_fetchone("SELECT super FROM admins WHERE chat_id={}".format(chat_id))[0]:
                cashout_id = int(text[6:])
                cashout = db.get_cashout(cashout_id=cashout_id)
                if cashout["status"] == "pending":
                    if text[0] == "a":
                        # Approve cashout and send notification for the user
                        if db.run_query("UPDATE cashout SET status='paid' WHERE cashout_id={}".format(cashout_id)):
                            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"✅Cashout ID: {cashout_id} Approved.")
                            alert_text = fm.alert_message(text_cashout_approved(cashout=cashout)[self.get_lang(cashout["chat_id"])])
                            context.bot.sendMessage(chat_id=cashout["chat_id"], text=alert_text, parse_mode=ParseMode.HTML)
                    else:
                        # Decline cashout, return money and send notification for the user
                        if db.decline_cashout(cashout=cashout):
                            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"❌Cashout ID: {cashout_id} Declined.")
                            alert_text = fm.alert_message(text_cashout_declined(cashout=cashout)[self.get_lang(cashout["chat_id"])])
                            context.bot.sendMessage(chat_id=cashout["chat_id"], text=alert_text, parse_mode=ParseMode.HTML)
                else:
                    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"Cashout ID: {cashout_id} has already been edited by other admin.")
            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_not_admin["eng"])
        
        # admin handles update request
        elif re.match("^(apup[0-9]*)|(deup[0-9]*)$", text):
            # Check if the admin is super
            update_id = int(text[4:])
            update_req = db.get_update(update_id=update_id)
            if len(update_req) >= 0:
                if update_req["status"] == "pending":
                    user = db.get_user_profile(update_req["chat_id"])
                    if text[0] == "a":
                        # Approve update and send notification for the user
                        if db.approve_update(update_req=update_req):
                            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"✅Update ID: {update_id} Approved.")
                            alert_text = fm.alert_message(text_update_approved[self.get_lang(update_req["chat_id"])])
                            context.bot.sendMessage(chat_id=update_req["chat_id"], text=alert_text, parse_mode=ParseMode.HTML)
                    else:
                        # Decline update, return money and send notification for the user
                        if db.decline_update(update_req=update_req):
                            context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"❌Update ID: {update_id} Declined.")
                            alert_text = fm.alert_message(text_update_declined[self.get_lang(update_req["chat_id"])])
                            context.bot.sendMessage(chat_id=update_req["chat_id"], text=alert_text, parse_mode=ParseMode.HTML)
                else:
                    context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"Update ID: {update_id} has already been edited by other admin.")
            else:
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=f"Update ID: {update_id} does NOT exist.\n~It might have been edited by other admin.")
        
        # Handle update level button
        elif re.match("^(update_level)$", text):
            user = db.get_user_profile(chat_id=chat_id)
            if user["jobs_completed"] > 0:
                if user["level"] < 2:
                    if db.create_update_req(chat_id=chat_id):
                        context.bot.sendMessage(chat_id=chat_id, text=text_update_sent[lang]) 
                    else:
                        context.bot.sendMessage(chat_id=chat_id, text=text_update_exists[lang]) 
                else:
                    context.bot.sendMessage(chat_id=chat_id, text=text_max_update[lang])
            else:              
                context.bot.sendMessage(chat_id=chat_id, text=text_must_complete_jobs[lang])
        

def main():
    # create ipn listener using flask and start it on separate thread
    # ipn = threading.Thread(target=app.run, args=(False,))
    # ipn.start()

    freelancebot = Freelance(bot_token)
    freelancebot.start_bot()
        

if __name__ == '__main__':
    main()