from config import *
import logging
from telegram.ext import CallbackContext, Updater, CommandHandler, MessageHandler, RegexHandler, ConversationHandler, CallbackQueryHandler, Filters
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Contact, ParseMode
from telegram.utils.helpers import mention_html
from lang_dict import *
from backend import Formatter, Db
import re
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

fm = Formatter()
db = Db(db_host=db_host, db_port=db_port, db_user=db_user, db_password=db_password, db_database=db_database)

inline_keyboards = {
    "settings_menu": [[InlineKeyboardButton(text="Filter partners by gender", callback_data="filgen")],
                    [InlineKeyboardButton(text="Change langauge/ ቋንቋ ለመቀየር", callback_data="chlang")],
                    [InlineKeyboardButton(text="About us", callback_data="about")]],

    "profile_menu": [[InlineKeyboardButton(text="Change nickname", callback_data="nickname")],
                    [InlineKeyboardButton(text="Change horoscope", callback_data="horoscope_req")],
                    [InlineKeyboardButton(text="Change location", callback_data="location_req")],
                    [InlineKeyboardButton(text="Change interest", callback_data="interest_req")],
                    [InlineKeyboardButton(text="Upgrade membership", callback_data="upgrade_req")],
                    [InlineKeyboardButton(text="Get invite link", callback_data="invite_link")]],

    "first_page_menu": [[InlineKeyboardButton(text="Change nickname", callback_data="nickname")],
                        [InlineKeyboardButton(text="Change horoscope", callback_data="horoscope_req_first")],
                        [InlineKeyboardButton(text="Change location", callback_data="location_req_first")],                            
                        [InlineKeyboardButton(text="Change interest", callback_data="interest_req_first")]],
}


NICKNAME = range(1)

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


        
class Random_chat():
    # initialize the bot
    def __init__(self, bot_token: str) -> None:
        self.bot_token = bot_token
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
        command_main_menu = CommandHandler("main_menu", self.main_menu)
        command_admin_menu = CommandHandler("botadmin", self.admin_menu)
        command_start_conv = CommandHandler("start", self.start_conv)
        command_end_conv = CommandHandler("start", self.end_conv)
        command_profile = CommandHandler("start", self.profile)
        command_settings = CommandHandler("start", self.settings)
        # command_admin = CommandHandler("botadmin", self.admin_menu)

        # Regex handler to handle specific texts
        regex_start_conv = RegexHandler("^({})$".format(button_start["eng"]), self.start_conv)
        regex_end_conv = RegexHandler("^({})$".format(button_end["eng"]), self.end_conv)
        regex_profile = RegexHandler("^({})$".format(button_profile["eng"]), self.profile)
        regex_settings = RegexHandler("^({})$".format(button_settings["eng"]), self.settings)
        regex_show_users = RegexHandler("^({})$".format("Show users"), self.show_users)
        regex_bot_status = RegexHandler("^({})$".format("Bot status"), self.bot_status)
        regex_promot = RegexHandler("^({})$".format("Promot"), self.promot)
        regex_get_user = RegexHandler("^({})$".format("sid [0-9]*"), self.get_user)

        # Handles conversation for nickname
        conv_nickname = ConversationHandler(entry_points=[CallbackQueryHandler(self.change_nickname_req, pattern="^(nickname)$")],
            states={NICKNAME: [MessageHandler(Filters.text & ~Filters.command, self.change_nickname), CommandHandler("start", self.start_endconv), CommandHandler("main_menu", self.main_menu_endconv)],
            },
            fallbacks=[RegexHandler("^({})$".format("exit"), self.start_endconv)]
        )


        # on noncommand i.e message - echo the message on Telegram
        message_voice = MessageHandler(Filters.voice, self.voice_handler)

        message_any = MessageHandler(Filters.text & ~Filters.command, self.menu)
        

        # Add handlers to the dispatcher

        # command handlers
        # command handlers
        dispatcher.add_handler(command_start)
        dispatcher.add_handler(command_main_menu)
        dispatcher.add_handler(command_admin_menu)
        dispatcher.add_handler(command_start_conv)
        dispatcher.add_handler(command_end_conv)
        dispatcher.add_handler(command_profile)
        dispatcher.add_handler(command_settings)


        # regex handlers
        dispatcher.add_handler(regex_start_conv)
        dispatcher.add_handler(regex_end_conv)
        dispatcher.add_handler(regex_profile)
        dispatcher.add_handler(regex_settings)
        dispatcher.add_handler(regex_show_users)
        dispatcher.add_handler(regex_bot_status)
        dispatcher.add_handler(regex_promot)
        dispatcher.add_handler(regex_get_user)

        # convereation handlers
        dispatcher.add_handler(conv_nickname)


        # message handlers
        dispatcher.add_handler(message_voice)

        dispatcher.add_handler(message_any)

        # inline button handler
        dispatcher.add_handler(CallbackQueryHandler(self.button_reg_lang, pattern="^(reg [a-z]*)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.button_reg_gen, pattern="^(Male [a-z]*)|(Female [a-z]*)$"))
        dispatcher.add_handler(CallbackQueryHandler(self.inline_button))



        if debug:
            updater.start_polling()
            updater.idle()
        else:
            PORT = int(os.environ.get('PORT', '8443'))
            updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=bot_token)
            updater.bot.set_webhook("https://ethiorandomchat.herokuapp.com/" + bot_token)
            updater.idle()

    # handles admin menu command
    @preprocess_admin
    def admin_menu(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        # Send a message when the command /start is issued
        keyboard = [["Show users", "Bot status"]]
        context.bot.send_message(chat_id=chat_id, text="admin menu", parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=False, resize_keyboard=True))

    # Displays users with their chat_id and username if available 
    @preprocess_admin
    def show_users(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        data = db.get_users('active', 0, self.users_per_text)
        if len(data) > 0:
            formatted_text = fm.format_users_list(data, 1)
            keyboard = [[InlineKeyboardButton(text="⏪", callback_data="pru0"), InlineKeyboardButton(text="⏩", callback_data=f"nxu{self.users_per_text}")]]
            context.bot.send_message(chat_id=chat_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            context.bot.send_message(chat_id=chat_id, text="There are no users to show.", parse_mode=ParseMode.HTML)
    
    # Displays bot status 
    @preprocess_admin
    def bot_status(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        data = db.get_bot_status()
        if len(data) > 0:
            formatted_text = fm.format_bot_status(data)
            context.bot.send_message(chat_id=chat_id, text=formatted_text, parse_mode=ParseMode.HTML)
        else:
            context.bot.send_message(chat_id=chat_id, text=text_error["eng"], parse_mode=ParseMode.HTML)

    # Send promotion messages to every user 
    @preprocess_admin
    def promot(self, update: Update, context: CallbackContext) -> None:
        # get list of users that chatted none, once ,and more than once
        # send promo message to the users when the list arrives
        users = db.run_query_fetchall("SELECT chat_id FROM users WHERE conversations = 0")
        if users != None:
            for chat_id in users:
                context.bot.send_message(chat_id=chat_id, text=text_promo_none["amh"], parse_mode=ParseMode.HTML)
        users = db.run_query_fetchall("SELECT chat_id FROM users WHERE conversations = 1")
        if users != None:
            for chat_id in users:
                context.bot.send_message(chat_id=chat_id, text=text_promo_once["amh"], parse_mode=ParseMode.HTML)
        users = db.run_query_fetchall("SELECT chat_id FROM users WHERE conversations >= 2")
        if users != None:
            for chat_id in users:
                context.bot.send_message(chat_id=chat_id, text=text_promo_twice["amh"], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Upgrade membership", callback_data="upgrade_req")]]))
    
    # Returns a user
    @preprocess_admin
    def get_user(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        text = update.message.text
        _,user_id = text.split(" ")
        user_id = int(user_id)
        user_html = mention_html(user_id, "user")
        fomatted_text = "result " + user_html
        context.bot.send_message(chat_id=chat_id, text=fomatted_text, parse_mode=ParseMode.HTML)

    # handles start command
    @preprocess
    def start(self, update: Update, context: CallbackContext) -> None:
        # Send a message when the command /start is issued
        self.menu(update, context)
    
    # handles main menu command
    @preprocess
    def main_menu(self, update: Update, context: CallbackContext) -> None:
        # Send a message when the command /start is issued
        self.menu(update, context)

    # handles start command
    @preprocess
    def start_endconv(self, update: Update, context: CallbackContext) -> int:
        # Send a message when the command /start is issued
        self.menu(update, context)
        return ConversationHandler.END
    
    # handles main menu command
    @preprocess
    def main_menu_endconv(self, update: Update, context: CallbackContext) -> int:
        # Send a message when the command /start is issued
        self.menu(update, context)
        return ConversationHandler.END

    # Handles register button
    def register_button(self, update: Update, context: CallbackContext) -> None:
        if update.message != None:
            chat_id = update.message.chat_id
            text = update.message.text[7:]
        else:
            chat_id = update.callback_query.message.chat_id
            text = update.callback_query.data 
        # Check if the user has joined via invite link: if True - add a point to the inviter
        keyboard = [[InlineKeyboardButton(text=button_lang["eng"], callback_data="reg eng"), InlineKeyboardButton(text=button_lang["amh"], callback_data="reg amh")]]
        lang_text = "Please choose your language preference.\n\nእባክዎ የቋንቋ ምርጫዎን ይምረጡ።"
        context.bot.sendMessage(chat_id=chat_id, text=lang_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        if text != "":
            if re.match("^(invite[0-9]*)$", text):
                inviter_id = int(text[6:])
                # Add invite point to the inviter and check if they invited == 5 members,
                # if True - make the user standard member for one day, and send notificationm message
                if db.add_invite_point(chat_id=inviter_id):
                    context.bot.sendMessage(chat_id=inviter_id, text=text_invite_notification["eng"], parse_mode=ParseMode.HTML)
    
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
        context.bot.sendMessage(chat_id=chat_id, text="You are not eligiable to access this feature.")

    # handles nickname change request
    @preprocess
    def change_nickname_req(self, update: Update, context: CallbackContext) -> int:
        # check if the user can chnage nickname right now
        # if True - send a request text consisting [back to MENU] button and advance to STATE=NICKNAME
        # if False - a discrption text stating why the user can not change nickname right now, end the conversation
        query = update.callback_query
        chat_id = query.message.chat_id
        query.answer()
        profile = db.get_user_profile(chat_id=chat_id)
        lang = profile["lang"]
        if db.can_change_nickname(profile=profile):
            keyboard = [[button_menu[lang]]]
            context.bot.sendMessage(chat_id=chat_id, text=text_change_nickname_req[lang], parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=False, resize_keyboard=True))
            return NICKNAME
        else:
            days = db.get_change_nickname_remaining_days(profile=profile)
            context.bot.sendMessage(chat_id=chat_id, text=text_cant_change_nickname(days=days)[lang], parse_mode=ParseMode.HTML)
            return ConversationHandler.END  

    # handles nickname change texts
    @preprocess
    def change_nickname(self, update: Update, context: CallbackContext) -> int:
        # check if the nickname is eligiable(length..)
        # if True - update nickname, send a confirmation message, send menu, and end the converstion
        # if False - discribe the problem and ask for nickname again, return NICKNAME state
        chat_id = update.message.chat_id
        text = update.message.text
        lang = self.get_lang(chat_id=chat_id)
        if text == button_menu[lang]:
            context.bot.sendMessage(chat_id=chat_id, text=text_change_nickname_canceled[lang], parse_mode=ParseMode.HTML)
            self.menu(update, context)
            return ConversationHandler.END
        else:
            if len(text) >= nickname_length_min and len(text) <= nickname_length_max:
                nickname = text + str(chat_id)[-5:]
                if db.change_nickname(chat_id=chat_id, nickname=nickname):
                    context.bot.sendMessage(chat_id=chat_id, text=text_nickname_updated(nickname=nickname)[lang], parse_mode=ParseMode.HTML)
                    self.menu(update, context)
                    return ConversationHandler.END
                else:
                    context.bot.sendMessage(chat_id=chat_id, text=text_error["eng"], parse_mode=ParseMode.HTML)
                    self.menu(update, context)
                    return ConversationHandler.END
            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_nickname_length_error()[lang], parse_mode=ParseMode.HTML)
                return NICKNAME 

    # displays menu 
    @preprocess
    def menu(self, update: Update, context: CallbackContext) -> None:
        if update.message != None:
            chat_id = update.message.chat_id
        else:
            chat_id = update.callback_query.message.chat_id
        lang = "eng"
        keyboard = [[button_start[lang], button_end[lang]], [button_profile[lang], button_settings[lang]]]
        context.bot.sendMessage(chat_id=chat_id, text=text_menu[lang], parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(keyboard=keyboard, one_time_keyboard=False, resize_keyboard=True))

    # starts a conversation
    @preprocess
    def start_conv(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id=chat_id)
        # checks if the user is not having a conversation. if true it will search for a conversation partner
        # if false, displays a message that the user is already having a conversation and needs to end it 
        if db.start_conv(chat_id=chat_id):
            profile = db.get_user_profile(chat_id=chat_id)
            context.bot.sendMessage(chat_id=chat_id, text=text_searching(profile=profile)[lang], parse_mode=ParseMode.HTML)
            partner_id = db.pair_user(chat_id=chat_id)
            if partner_id != -1:
                # send a message for both partners describing that they have been paired and can start the conversation
                partner_profile = db.get_user_profile(chat_id=partner_id)
                context.bot.sendMessage(chat_id=chat_id, text=text_paired(profile=partner_profile)[lang], parse_mode=ParseMode.HTML)
                context.bot.sendMessage(chat_id=partner_id, text=text_paired(profile=profile)[partner_profile["lang"]], parse_mode=ParseMode.HTML)
        else:
            context.bot.sendMessage(chat_id=chat_id, text=text_cant_start_conv[lang], parse_mode=ParseMode.HTML)

    # ends a conversation
    @preprocess
    def end_conv(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        # check if the user is still in a conversation if true, end the conversation and send a confromation message to both partners, and rate both partners
        # if false, send an error message stating that the user is not having a conversation
        profile = db.get_user_profile(chat_id=chat_id)
        lang = profile["lang"]
        if db.end_conv(chat_id=chat_id):       
            partner_id = profile["partner_id"]
            partner_profile = db.get_user_profile(chat_id=partner_id)
            keyboard1 = []
            keyboard2 = []
            rate = list_of_rate
            for rate in list_of_rate:
                k1 = []
                k2 = []
                for r in rate:
                    k1.append(InlineKeyboardButton(text=r, callback_data=f"rate{chat_id} {r}"))
                    k2.append(InlineKeyboardButton(text=r, callback_data=f"rate{partner_id} {r}"))
                keyboard1.append(k1)
                keyboard2.append(k2)
            context.bot.sendMessage(chat_id=chat_id, text=text_conversation_ended(profile=partner_profile)[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard2))
            context.bot.sendMessage(chat_id=partner_id, text=text_conversation_ended(profile=profile)[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard1))
        else:
            context.bot.sendMessage(chat_id=chat_id, text=text_no_conversations[lang], parse_mode=ParseMode.HTML)

    # shows the profile of a user
    @preprocess
    def profile(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        profile = db.get_user_profile(chat_id=chat_id)
        formatted_text = fm.format_profile(profile=profile)
        context.bot.sendMessage(chat_id=chat_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboards["profile_menu"]))

    # displays settings
    @preprocess
    def settings(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat_id
        lang = self.get_lang(chat_id=chat_id)
        # Display all the setting menu using inline buttons
        # add gender filter option
        # about us
        context.bot.sendMessage(chat_id=chat_id, text=text_settings()[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboards["settings_menu"]))

    
    # handles voice messages
    @preprocess
    def voice_handler(self, update: Update, context: CallbackContext) -> None:
        # checks if the user has a partner, if True it will forward the message to the partner
        # if False displays an error message
        chat_id = update.message.chat_id
        profile = db.get_user_profile(chat_id=chat_id)
        lang = profile["lang"]
        if not profile["searching_partner"] and profile["partner_id"] != -1:
            voice = update.message["voice"]["file_id"]
            self.send_voice(update=update, context=context, sender_id=chat_id, partner_id=profile["partner_id"], voice=voice)
        else:
            context.bot.sendMessage(chat_id=chat_id, text=text_no_partner[lang], parse_mode=ParseMode.HTML)
    
    # sends voice message to a specific user
    def send_voice(self, update: Update, context: CallbackContext, sender_id: int, partner_id: int, voice: str) -> None:
        nickname = db.get_user_profile(chat_id=sender_id)["nickname"]
        context.bot.sendVoice(chat_id=partner_id, voice=voice, caption=f"<b>nickname:</b> {nickname}", parse_mode=ParseMode.HTML)

    # returns inline keyboard consisiting gender button, with current selection
    def get_gender_buttons(self, selected: str) -> list:
        male = list_of_genders[0][0]
        female = list_of_genders[1][0]
        both = list_of_genders[2][0]
        for i,gender in enumerate(list_of_genders):
            if gender[1] == selected:
                if gender[1] == "Male":
                    male = male + " ✅" 
                elif gender[1] == "Female":
                    female = female + " ✅" 
                else:
                    both = both + " ✅" 
        keyboard = [[InlineKeyboardButton(text=male, callback_data="chgen Male"), InlineKeyboardButton(text=female, callback_data="chgen Female")],
                    [InlineKeyboardButton(text=both, callback_data="chgen None")],
                    [InlineKeyboardButton(text="🔙Back", callback_data="settings")]]
        return keyboard

    # returns list of req inline buttons
    def get_req_buttons(self, ls: list, selected: str, cdata:str, back_button: str) -> list:
        keyboard = []
        for location in ls:
            edited_location0 = location[0][0]
            edited_location1 = location[1][0]
            if selected == edited_location0:
                edited_location0 = "✅ " + edited_location0
            if selected == edited_location1:
                edited_location1 = "✅ " + edited_location1
            keyboard.append([InlineKeyboardButton(text=edited_location0, callback_data=f"{cdata} {location[0][1]}"), InlineKeyboardButton(text=edited_location1, callback_data=f"{cdata} {location[1][1]}")])
        keyboard.append([InlineKeyboardButton(text=button_back["eng"], callback_data=f"{back_button}")])
        return keyboard

    # returns list of change inline buttons
    def get_change_buttons(self, ls: list, selected: str, cdata:str, back_button: str) -> list:
        keyboard = []
        for location in ls:
            edited_location0 = location[0][0]
            edited_location1 = location[1][0]
            if selected == location[0][1]:
                edited_location0 = "✅ " + edited_location0
                new_location = location[0][0]
            if selected == location[1][1]:
                edited_location1 = "✅ " + edited_location1
                new_location = location[1][0]
            keyboard.append([InlineKeyboardButton(text=edited_location0, callback_data=f"{cdata} {location[0][1]}"), InlineKeyboardButton(text=edited_location1, callback_data=f"{cdata} {location[1][1]}")])
        keyboard.append([InlineKeyboardButton(text=button_back["eng"], callback_data=f"{back_button}")])
        return [keyboard, new_location]

    @preprocess
    def inline_button(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        chat_id = query.message.chat_id
        text = query.data 
        query.answer()
        
        # displays list of locations
        if re.match("^(location_req)|(location_req_first)$", text):
            # display change location req with ethio city names in an inline button
            profile = db.get_user_profile(chat_id=chat_id)
            lang = profile["lang"]
            if re.match("^(location_req_first)$", text):
                keyboard = self.get_req_buttons(ls=list_of_locations, selected=profile["location"], cdata="location_change_first", back_button="first_page")
            else:
                keyboard = self.get_req_buttons(ls=list_of_locations, selected=profile["location"], cdata="location_change", back_button="profile")
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_location_req[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        
        # changes location
        elif re.match("^(location_change [a-z/A-Z]*)|(location_change_first [a-z/A-Z]*)$", text):
            # updates location on the database or sends an error message
            _,city = text.split(" ")
            if re.match("^(location_change_first [a-z/A-Z]*)$", text):
                keyboard, new_location = self.get_change_buttons(ls=list_of_locations, selected=city, cdata="location_change_first", back_button="first_page")
            else:
                keyboard, new_location = self.get_change_buttons(ls=list_of_locations, selected=city, cdata="location_change", back_button="profile")

            if db.run_query("UPDATE users SET location='{}' WHERE chat_id={}".format(new_location, chat_id)):
                context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                context.bot.sendMessage(chat_id=chat_id, text=text_error["eng"])

        # displays list of interests
        if re.match("^(interest_req)|(interest_req_first)$", text):
            # displays list of interests with inline buttons
            profile = db.get_user_profile(chat_id=chat_id)
            lang = profile["lang"]
            if re.match("^(interest_req_first)$", text):
                keyboard = self.get_req_buttons(ls=list_of_interests, selected=profile["interest"], cdata="interest_change_first", back_button="first_page")
            else:
                keyboard = self.get_req_buttons(ls=list_of_interests, selected=profile["interest"], cdata="interest_change", back_button="profile")
            interest_counter = db.get_interest_counter()
            total_users = db.run_query_fetchone("SELECT COUNT(*) FROM users")[0]
            formatted_text = text_interest_req[lang] + "\n" + fm.format_interest_counter(data=interest_counter, total_users=total_users)
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        
        # changes interest
        elif re.match("^(interest_change [a-z/A-Z]*)|(interest_change_first [a-z/A-Z]*)$", text):
            # updates location on the database or sends an error message
            _,interest_choice = text.split(" ")
            if re.match("^(interest_change_first [a-z/A-Z]*)$", text):
                keyboard, new_interest = self.get_change_buttons(ls=list_of_interests, selected=interest_choice, cdata="interest_change_first", back_button="first_page")
            else:
                keyboard, new_interest = self.get_change_buttons(ls=list_of_interests, selected=interest_choice, cdata="interest_change", back_button="profile")

            if db.run_query("UPDATE users SET interest='{}' WHERE chat_id={}".format(new_interest, chat_id)):
                lang = self.get_lang(chat_id)
                interest_counter = db.get_interest_counter()
                total_users = db.run_query_fetchone("SELECT COUNT(*) FROM users")[0]
                formatted_text = text_interest_req[lang] + "\n" + fm.format_interest_counter(data=interest_counter, total_users=total_users)
                context.bot.editMessageText(chat_id=chat_id, message_id=query.message.message_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                context.bot.send_message(chat_id=chat_id, text=text_error["eng"])

        # displays list of horoscopes
        elif re.match("^(horoscope_req)|(horoscope_req_first)$", text):
            # display change location req with ethio city names in an inline button
            profile = db.get_user_profile(chat_id=chat_id)
            lang = profile["lang"]
            if re.match("^(horoscope_req_first)$", text):
                keyboard = self.get_req_buttons(ls=list_of_horoscopes, selected=profile["horoscope"], cdata="horoscope_change_first", back_button="first_page")
            else:
                keyboard = self.get_req_buttons(ls=list_of_horoscopes, selected=profile["horoscope"], cdata="horoscope_change", back_button="profile")
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_horoscope_req[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        
        # changes horoscope
        elif re.match("^(horoscope_change [a-z/A-Z]*)|(horoscope_change_first [a-z/A-Z]*)$", text):
            # updates horoscope on the database or sends an error message
            _,horoscope_choice = text.split(" ")
            if re.match("^(horoscope_change_first [a-z/A-Z]*)$", text):
                keyboard, new_horoscope = self.get_change_buttons(ls=list_of_horoscopes, selected=horoscope_choice, cdata="horoscope_change_first", back_button="first_page")
            else:
                keyboard, new_horoscope = self.get_change_buttons(ls=list_of_horoscopes, selected=horoscope_choice, cdata="horoscope_change", back_button="profile")

            if db.run_query("UPDATE users SET horoscope='{}' WHERE chat_id={}".format(new_horoscope, chat_id)):
                context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                context.bot.send_message(chat_id=chat_id, text=text_error["eng"])
        
        # handles rating
        elif re.match("^(rate[0-9]* [0-9]*)$", text):
            # parse the query text then rate the partner at last send a cnfirmation message
            partner_id,rate = text.split(" ")
            partner_id = int(partner_id[4:])
            rate = int(rate)
            profile = db.get_user_profile(chat_id=partner_id)
            lang = profile["lang"]
            if db.rate(profile=profile, rate=rate):
                context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_rate_success(profile=profile, rate=rate)[lang], parse_mode=ParseMode.HTML)
            else:
                context.bot.send_message(chat_id=chat_id, text=text_error["eng"], parse_mode=ParseMode.HTML)

        # generates an invite link
        elif re.match("^(invite_link)$", text):
            # generate invite link and show it to the user
            lang = self.get_lang(chat_id)
            link = f"https://t.me/{bot_username}?start=invite{chat_id}"
            context.bot.send_message(chat_id=chat_id, text=text_invite(link=link)[lang], parse_mode=ParseMode.HTML)
        
        # upgrade membership request handler
        elif re.match("^(upgrade_req)$", text):
            # generate a link to yenepay account payment, [standard plan, elite plan], and present them in an inline button
            # describe what each plan is in the discription text, how they should complete the payment
            lang = self.get_lang(chat_id)
            standard_link, elite_link = fm.generate_link(chat_id=chat_id)
            keyboard = [[InlineKeyboardButton(text="Standard membership", url=standard_link)],
                        [InlineKeyboardButton(text="Elite membership", url=elite_link)],
                        [InlineKeyboardButton(text="🔙Back", callback_data="profile")]]
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_upgrade_membership[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

        # profile page
        elif re.match("^(profile)$", text):
            profile = db.get_user_profile(chat_id=chat_id)
            lang = profile["lang"]
            formatted_text = fm.format_profile(profile=profile)
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboards["profile_menu"]))
        
        # settings page
        elif re.match("^(settings)$", text):
            lang = self.get_lang(chat_id)
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_settings()[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboards["settings_menu"]))

        # first_page
        elif re.match("^(first_page)$", text):
            profile = db.get_user_profile(chat_id=chat_id)
            lang = profile["lang"]
            formatted_text = fm.first_time_text(profile=profile) + text_first_time()[lang]
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboards["first_page_menu"]))

        # shows about us section
        elif re.match("^(about)$", text):
            # show about us text
            lang = self.get_lang(chat_id)
            context.bot.send_message(chat_id=chat_id, text=text_about[lang], parse_mode=ParseMode.HTML)

        # shows change language section
        elif re.match("^(chlang)$", text):
            keyboard = [[InlineKeyboardButton(text=button_lang["eng"], callback_data="lang eng"), InlineKeyboardButton(text=button_lang["amh"], callback_data="lang amh")],
                        [InlineKeyboardButton(text="🔙Back", callback_data="settings")]]
            lang_text = "Please choose your language preference.\n\nእባክዎ የቋንቋ ምርጫዎን ይምረጡ።"
            context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=lang_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
        
        # changes language
        elif re.match("^(lang [a-z]*)$", text):
            _,lang_choice = text.split(" ")
            if db.run_query("UPDATE users SET lang='{}' WHERE chat_id={}".format(lang_choice, chat_id)):
                context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_lang_changed[lang_choice], parse_mode=ParseMode.HTML)
                self.menu(update, context)
            else:
                context.bot.send_message(chat_id=chat_id, text=text_error["eng"], parse_mode=ParseMode.HTML)
        # handles filter by gender req
        elif re.match("^(filgen)$", text):
            profile = db.get_user_profile(chat_id=chat_id)
            lang = profile["lang"]
            if profile["membership"] >= 1:
                keyboard = self.get_gender_buttons(selected=profile["partner_gender"]) 
                context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_gender_filter[lang], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                context.bot.send_message(chat_id=chat_id, text=text_not_memeber[lang], parse_mode=ParseMode.HTML)

        # changes gender of partner while filtering
        elif re.match("^(chgen Male)|(chgen Female)|(chgen None)$", text):
            _,choice= text.split(" ")  
            if db.change_gender_filter(chat_id=chat_id, gender=choice):
                keyboard = self.get_gender_buttons(selected=choice) 
                context.bot.edit_message_reply_markup(chat_id=chat_id, message_id=query.message.message_id, reply_markup=InlineKeyboardMarkup(keyboard))
            else:
                context.bot.send_message(chat_id=chat_id, text=text_error["eng"], parse_mode=ParseMode.HTML)
        
        # Handles Previous and Next inline buttons
        elif re.match("^(pru[0-9]*)|(nxu[0-9]*)$", text):        
            ls = text.split(" ")
            if len(ls) <= 1:
                offset = int(text[3:]) 
            else:
                offset = int(ls[0][3:]) 
            data = {}
            if text[0:3] == "nxu" or text[0:3] == "pru":
                data = db.get_users("active", offset, self.users_per_text)
 
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
                formatted_text = fm.format_users_list(data, offset + 1)
                keyboard=[[InlineKeyboardButton(text="⏪", callback_data=f"pr{text[2]}{pr_offset}"), InlineKeyboardButton(text="⏩", callback_data=f"nx{text[2]}{nx_offset}")]]
                query.edit_message_text(text=formatted_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)
        
    # Handles inline button for unregistered users
    def button_reg_lang(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        chat_id = query.message.chat_id
        text = query.data 
        query.answer()

        _,lang_choice= text.split(" ")
        keyboard = [[InlineKeyboardButton(text=button_male["eng"], callback_data=f"Male {lang_choice}"), InlineKeyboardButton(text=button_female["eng"], callback_data=f"Female {lang_choice}")]]
        context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=text_gender_req[lang_choice], parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

    def button_reg_gen(self, update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        chat_id = query.message.chat_id
        text = query.data 
        query.answer()
        # handles gender registration

        gender,lang_choice= text.split(" ")
        if not db.is_user_registered(chat_id=chat_id):
            if db.register(chat_id=chat_id, lang=lang_choice, gender=gender):
                profile = db.get_user_profile(chat_id=chat_id)
                lang = profile["lang"]
                formatted_text = fm.first_time_text(profile=profile) + text_first_time()[lang]
                context.bot.edit_message_text(chat_id=chat_id, message_id=query.message.message_id, text=formatted_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_keyboards["first_page_menu"]))
                self.menu(update, context)
        else:
            self.menu(update, context)


def main():
    # create ipn listener using flask and start it on separate thread
    # ipn = threading.Thread(target=app.run, args=(False,))
    # ipn.start()

    randchat = Random_chat(bot_token)
    randchat.start_bot()
        

if __name__ == '__main__':
    main()
