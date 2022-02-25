debug = True

if debug:
    db_host = "127.0.0.1"
    db_port = "5432"
    db_user = "postgres"
    db_password = "12345"
    db_database = "rand_chat"
else:
    db_host = ""
    db_port = ""
    db_user = ""
    db_password = ""
    db_database = ""


if debug:
    bot_token = ""
else:
    bot_token = ""


ipn_url = "https://ipnethiovoicechat.herokuapp.com/webhook"

list_of_locations = [
    [["Addis Ababa", "AddisAbaba"], ["Harari", "Harari"]],
    [["Afar", "Afar"], ["Oromia", "Oromia"]],
    [["Amhara", "Amhara"], ["Sidama", "Sidama"]],
    [["Benishangul Gumz", "BenishangulGumz"], ["Somali", "Somali"]],
    [["Dire Dawa", "DireDawa"], ["Southern Nations", "SouthernNations"]],
    [["Gambela", "Gambela"], ["Tigray", "Tigray"]],
]

list_of_interests = [
    [["Politics", "Politics"], ["Music & Movies", "Music"]],
    [["Flirt", "Flirt"], ["School life", "SchoolLife"]],
    [["Sex", "Sex"], ["Campus life", "CampusLife"]],
    [["Single life", "Single"], ["Relationship", "Relationship"]],
    [["Roast eachother", "RoastEachother"], ["Work & Bussiness", "Work"]],
    [["Food", "Food"], ["Religion", "Religion"]],
    [["Sports", "Sports"], ["Anything", "Anything"]],
]

list_of_horoscopes = [
    [["Aries", "Aries"], ["Aquarius", "Aquarius"]],
    [["Cancer", "Cancer"], ["Capricorn", "Capricorn"]],
    [["Gemini", "Gemini"], ["Leo", "Leo"]],
    [["Libra", "Libra"], ["Pisces", "Pisces"]],
    [["Sagittarius", "Sagittarius"], ["Scorpio", "Scorpio"]],
    [["Taurus", "Taurus"], ["Virgo", "Virgo"]],
]

list_of_genders = [["👨Male", "Male"], ["👩Female", "Female"], ["👫Both", "None"]]

list_of_rate = [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]

default_rate = 10

nickname_length_min = 2
nickname_length_max = 20
male = "Male"
female = "Female"
invite_upgrade = 5


bot_username = "ethiovoicechatbot"
admin_chat_id = 350831868
admin_username = "jordan5791"
channel_username = "EthioVoiceChat123"

merchant_id = 4464
invite_price = 5
standard_price = 10
elite_price = 15
