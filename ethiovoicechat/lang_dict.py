from config import *
from telegram.utils.helpers import mention_html


# Buttons

button_lang = {
    "eng": "ð¬ð§English",
    "amh": "ðªð¹á áá­á",
}

button_male = {
    "eng": "ð¨Male",
    "amh": "ð¨Male",
}

button_female = {
    "eng": "ð©Female",
    "amh": "ð©Female",
}

button_start = {
    "eng": "ð¢Start conversation",
    "amh": "ð¢Start conversation",
}

button_end = {
    "eng": "ð´End conversation",
    "amh": "ð´End conversation",
}

button_profile = {
    "eng": "ðView profile",
    "amh": "ðView profile",
}

button_settings = {
    "eng": "ð§Settings",
    "amh": "ð§Settings",
}

button_menu = {
    "eng": "ðMenu",
    "amh": "ðMenu",
}

button_back = {
    "eng": "ðBack",
    "amh": "ðBack",
}



# Texts

text_lang_changed = {
    "eng": "You changed your language preference to ð¬ð§English.",
    "amh": "á¨ááá áá­á«á áá° ðªð¹á áá­á á°áá­á¯áá¢",
}

text_gender_req = {
    "eng": "Please select your gender.",
    "amh": "á¥á£á­á á¨á¥á­á¶á áá³ á­áá¨á¡á¢",
}

text_menu = {
    "eng": "<i>Please select from the options below.</i>",
    "amh": "<i>á¥á£á­á á¨á³á½ á«ááµ á áá«á®á½ ááµá¥ á­áá¨á¡á¡á¡</i>",
}

text_cant_start_conv = {
    "eng": """-You can NOT start a new conversation while you are already having one or while you are searching for a new partner.
-You must end the conversation first.

<i>~press the <b>End conversation</b> button to end the current conversation.</i>""",
    
    "amh": """-ááµááá áá­á­áµ(conversation) á¥á«á¨á á¨áá áá­á á á²áµ á áá­ á¥á¨ááá á¨áá á£ á á²áµ áá­á­áµ áááá­ á á­á½ááá¡á¡
-ááááªá« á«áµááá©áµá áá­á­áµ áá¨á¨áµ/ááá á áá¥ááµá¡á¡

<i>~áá­á­á±á ááá ááá/ááá°á¨á <b>End conversation</b> á¨áááá ááá á­á«áá¡á¡</i>""",
}

text_no_conversations = {
    "eng": """<b>Conversation ended.</b>
<i>You have got no more conversations to end.</i>""",

    "amh": """<b>áá­á­á± á°á áááá¡á¡</b>
<i>á¨á áá á¨áá«áá­á¡áµ á°á¨ááª áá­á­á¶á½ á¨áááµáá¢</i>""",
}

text_no_partner = {
    "eng": """<b>You do NOT have any partner to chat with.</b>
    
<i>~Please press the <b>Start conversation</b> button from the menu and wait a while until we find you a random partner.</i>""",

    "amh": """<b>á¨ááá«á©á áµ á áá­ á¨áááµáá¢</b>
    
<i>~á¥á£á­áá á¨ááá¨á«áï¼menuï¼ áá­ <b>Start conversation</b> á¨áááá ááá á­á«áá á áá«á­ á áá­ á¥áµá­ááááá áµá¨áµ áµáá½ á­á á¥áá¡á¡</i>""",
}

text_change_nickname_req = {
    "eng": """<b>Please tell me your nickname?</b>
~Your nickname will be shown to your partners while chatting.
<i>example - abebe, miki, betty, almaz</i>""",

    "amh": """<b>á¥á£á­áá áµáááµá áá­áá áá½á áµáááµá á­ááá©á?</b>
~á ááá«á©á áµ áá áá½á áµáá áá£áá°á¨á£á á­á³á«áá¡á¡
<i>áá³á :- á á á  á£ ááª á£ á¤á²</i>""",
}

text_change_nickname_canceled = {
    "eng": "You canceled your request for changing your nickname.",
    "amh": "áá½á áµáááµá áááá¨á­ á«áá¨á¡áµá á¥á«á á°á­áááá¡á¡",
}

text_error = {
    "eng": "ðSomething went wrong while processing your request.",
    "amh": "ðSomething went wrong while processing your request.",
}

text_location_req = {
    "eng": "<b>Please choose your current location from the options below.</b>",
    "amh": "<b>á¥á£á­áá á áá á«áá áµá á¦á³ á¨á³á½ á«ááµ á áá«á®á½ á­áá¨á¡ á¡á¡</b>",
}

text_interest_req = {
    "eng": """<b>Please choose your interest of topic from the options below.</b>
<i>~We will use this to find your random partner.</i>""",

    "amh": """<b>á¥á£á­áá á¨áá á á³á½ á«ááµ á áá«á®á½ ááµá¥ áááá«á¨áµ á¨ááááá áµá á­áá° á­áá¨á¡á¡á¡</b>
<i>~á­áá á­áá° á¨áá­á­áµ á áá­áá ááááá á¥áá ááá á³ááá¢</i>""",
}

text_horoscope_req = {
    "eng": "<b>Please choose your horoscope(zodiac sign) from the options below.</b>",
    "amh": "<b>á¥á£á­áá á¨áá á á³á½ á«ááµ á áá«á®á½ ááµá¥ á¨á¥á­áµáá á¨á®á¨á¥ ááá­áµ(zodiac sign) á­áá¨á¡á¢</b>",
}

text_under_devt = {
    "eng": "This feature is under development and will be available soon.",
    "amh": "á­á áá­á« á áá°á«áµ áá­ á«á á²áá á£ á áá­á¡á á°áá£á­ áá­ á­áááá¡á¡",
}

text_upgrade_membership = {
    "eng": """You should upgrade your membership to Standard or Elite.
<u>Benefits of upgrading membership.</u>
-You will find chatting partners faster(<i>partners are paired with users that are not memebrs after we check that there are no more elite/standard members waiting for partners</i>).
-You will have the ability to filter your partners by gender.
-Your partners will know that you are a vip member when you get paired for a voice chat session.
-You will unlock other many features.

<b>Standard membership:</b>  costs only {} birr and expires after 1 week.
<b>Elite membership:</b>  costs only {} birr and expires after 1 month.

Press one of the buttons and it will redirect you to <b>YenePay</b> website. you can complete the payment there. 
When you complete the payment, We will upgrade your membership to your choice of membership type and send you a confirmation text.
<i>It only takes about 1 minute, so please consider upgrading your membership.</i>

<b>If you don't have a yenepay account You only need a phone number to create a new one. and you can connect it with (CBE Birr, Amole, Hello cash).
You can also transfer money from your bank account(CBE birr, Amole, Hello cash) to your YenePay account.</b>

<i>You can use standard membership for 1 day if you invite {} members</i>
""".format(standard_price, elite_price, invite_upgrade),

    "amh": """á á£áááµáá áá° (Standard áá­á Elite) áá»á»á á áá¥ááµá¡á¡
<u>á á£áááµá á¨áá»á»á á¥ááá½</u>
-á áá«á­ á áá®á½á á áá¥ááµ á«ááá(<i>á áá«á­ á áá®á½ á¨ á¥á­á¶ áá­ á¨áá£áá©áµ á£ ááááªá« á á£á á¨áá á°á áááá½ áá­ á°á£áá¨á á¨á°á¨á áá</i>)á¡á¡
-á¨á áá®á áá³ á¨ááá¨á¥ á½áá³ á­áá®á³áá¡á¡
-á¨ á áá«á­ á áá® áá­ á²á£áá© á£ á áá® á¨ vip á á£á áááá¹á á«áááá¡á¡
-á¥áá ááá½ á°á¨ááª á¥á á¥ááá¥ááá½á á«áááá¢

<b>Standard á á£áááµ:</b>  ááªá {} á¥á­ á¥á» á²áá á¨ 1 á³áááµ á áá ááá á«á ááá¢
<b>Elite á á£áááµ:</b>  ááªá {} á¥á­ á¥á» á²áá á¨ 1 áá­ á áá ááá á«á ááá¢

á¨áá­á«áá¹ ááµá¥ á áá±á ááá á²á«á á£ áá° <b>YenePay</b> áµá¨ áá½ á­áá«áá³áá¢ á­áá«áá á¥áá« áá ááá á­á½ááá¢ 
á­áá«áá á²á«á ááá á á£áááµáá áá° áá¨á¡áµ á¨á á£áááµ áá­ááµ á á»á½áá á¨áá¨ááá« á½áá á¥ááá­ááá³ááá¡á¡
<i>á¨áááµá°á á¢á á 1 á°áá á¥á» áµááá á£ á¥á£á­áá á á£áááµáá ááá»á»á á«áµá¡á áµá¡á¡</i>

<b>á¨ yenepay á á«áááµï¼accountï¼ á¨ááááµ á á²áµ áááá£áµ áµáá­ áá¥á­ á¥á» á á ááá¢ á á«áááµ á«áá¡ á áá á¨ (CBE á¥á­ á£ á áá á£ áá á«á½) áá­ áá«ááááµ á­á½áá á¡á¡
á¥áá²áá á¨á£áá­ áá³á¥á (CBE á¥á­ á£ á áá á£ áá á«á½) áá° YenePay á á«áááµá áááá¥ ááµá°ááá á­á½ááá¢</b>

<i>{} á á£ááµá á¨áá á standard á á£áááµá á 1 áá áá áá á­á½áá</i>
""".format(standard_price, elite_price, invite_upgrade),
}

text_gender_filter = {
    "eng": """
You can filter your random partner gender by selecting one of the buttons.
<i>If you don't mind chatting with any gender please select Both.</i> 
""",

    "amh": """
á áá±á ááá á ááá¨á¥ á¨á áá®á áá³ ááá¨á¥ á­á½ááá¡á¡
<i>á¨ááááá áá³ áá­ ááá«á¨áµ á¨áááá á¨áá á¥á£á­áá Both á¨áááá ááá á­áá¨á¡á¡á¡</i> 
""",
}

text_not_memeber = {
    "eng": """
<b>You need to be a standard/elite member to access this feature.</b>
<i>You can upgrade your membership type by selecting the <b>Profile</b> option and pressing <b>Upgrade memebership</b> button.</i>
""",

    "amh": """
<b>á­ááá áá­á« ááá áá standard/elite á á£á ááá á áá¦áµá¡á¡</b>
<i>á¨ <b>Profile</b> á áá«á­á á ááá¨á¥ á¥á <b>Upgrade memebership</b> áááá á áá«á á¨á á£áááµáá á á­ááµ áá»á»á á­á½ááá¡á¡</i>
""",
}

text_invite_notification = {
    "eng": """
ð <b>NOTOFICATION</b>

Dear user, Thank you for inviting <b>{}</b> members.
Your membership type is updated to <b>Standard</b> for 1 day.

<i>Thank you for using our platform.</i>
""".format(invite_upgrade),

    "amh": """
ð <b>NOTOFICATION</b>

ááµ á°á áá á£ <b>{}</b> á á£ááµá áµááá á á¥ááá°ááááá¡á¡
á¨á á£áááµá á á­ááµ á 1 áá áá° <b>Standard</b> á°á»á½ááá¢

<i>á¨á¥áá áµááá¨á¡ á¥ááá°ááááá¡á¡</i>
""".format(invite_upgrade),
    }





# Static and long texts
text_about = {
    "eng": """
Hello, I am jordan and I am a programmer based in Addis Ababa, Ethiopia.
I made this bot to let everybody discusss on their favorite topic.

<i>I believe that we sometimes express ourselves freely to someone we don't know (a stranger).</i>
That is why I made this random stranger voice chat bot.

I wish you a memorable chatting session. cheersð».

<b>Join our channel for updates</b> @{}
""".format(channel_username),

    "amh": """
á°áá áá­á³á á¥á£áááá¢ á¨ááá¨á á á²áµ á á á£ ááµá¥ á²áá á£ áµá«á¬ á°á programmer ááá¢
á­ááá á¦áµ á¨á°á«ááµ ááá á°á á ááááá á­ááµ áá­ áá» áá á¥áá²áá«á­ á áá°á¥ ááá¢

<i>á áá³áá´ á¨á­á¶áá á¨áááá¸á á°áá½ áá­ á  á ááµ á­ááµ ááªá« áá» ááá á¥ááá«áá á¥á¬ á áµá£ááá¢</i>
á­ááá á¦áµ á¨á°á«ááµ á á áá­áá«áµ ááá¢

á áªá áá á¥áá°ááá«á¹ á°áµá á á°á­ááá. cheersð».

<b>á á³á²áµ ááá®á½á ááµá áááá á»ááá½áá á­áááá </b> @{}
""".format(channel_username),
}







# Text with values

def text_first_time() -> dict:
    admin_username_html = mention_html(admin_chat_id, "ADMIN")
    text = {
        "eng": """ðhi, Nice to meet you. I see that its your first time using this bot. Here are the most valuable things you need to know.

<b>First of all, this bot completely respects your privacy and none of the messages you send will be stored on our server.</b>
<b>Plus, the random voice chat partners you meet won't know who you are. This bot makes you totally anonymous.</b>

~You should change your nickname by pressing <b>Change nickname</b> button. It is displayed as your name while chatting with strangers.
~You should also change your horoscope by pressing <b>Change horoscope</b> button. Other users will see your horoscope while chatting.
~You can change your location by pressing <b>Change location</b> button.
<b>~You must change your interest as it is used to find you a partner with common interest. Please press Change interest button.</b>

-You can visit your profile and notice the changes you made by pressing the <i>Profile</i> button from the main menu.
-Anything you probably want to change can be found in the <i>Settings</i> option.


After you finished setting up your profile, You can chat with another stranger by pressing the <i>Start conversation</i> button from the main menu.
ð»enjoy.
IF YOU HAVE ANY QUESTION, PLEASE CONTACT THE {}.
    """.format(admin_username_html),

        "amh": """ðá°áá áµáá°áááá á°áµ á¥áááá¢ á­ááá á¦áµ á²á áá áááááªá« áá á¥áá°áá á á­á»ááá¡á¡ ááá á«áá¥ááµ á á£á á áá ááá®á½ á¨áá á á³á½ á°áá­áá¨ááá¡á¡

<b>á ááááªá« á£ á­á á¦áµ á¨á¥á­áµáá áááááµ áá á áá á¨áá«á¨á¥á­ á²áá á¨áá³á¸á ááá¥á­á¶á½ áá«á¨á á áá³á¸áá á¥á áá­ á á­ááá¡áá¡á¡</b>
<b>á á°á¨ááªá á£ á¨áá«ááá¸á á¨áá­á­áµ á áá®á½ á¨á¥á­á¶á ááááµ á á«áááá¡á¡</b>

~<b>Change nickname</b> áááá á áá«á áá½á áµááá áááá¥ á áá¥ááµá¡á¡ á¨á á²áµ á°áá½ áá­ á ááá«á©á áµ áá á¥áá° áµáá áá ááá± á­á³á«áá¡á¡
~á¥áá²áá <b>Change horoscope</b> áááá á áá«á á¨á®á¨á¥ ááá­á¶á áááá¥ á áá¥ááµá¡á¡ á¨ááá½ á°á áááá½ áá­ á²áá«á© á¨á®á¨á¥ ááá­á¶á á«á©á³áá¡á¡
~<b>Change location</b> áááá á áá«á á háá á«áá áµá á¨á°á áááá¥ á­á½ááá¡á¡
<b>~á¨áá« ááááµ á«áá á¨áá­á­áµ á áá­ áááááµ á£ á¥á­á¶ ááá«á¨áµ á¨ááááá áµá á­ááµ áááá¥ á áá¦áµá¢ á¥á£á­áá Change interest á¨áááá ááá á­á«á á¡á¡</b>

-á¨ááá ááá¨á« ááµá¥ <i>Profile</i> á¨áááá ááá á áá«á áµá á¥á­á¶ á«ááá áá¨á ááá¥ááµ á¥á á«á°á¨ááµá ááá¦á½ áá¥ áááµ á­á½áá á¡á¡
-áááá£áµ áááá¥ á¨áááááµ ááááá ááá­ á«á <i>Settings</i> á¨áááá ááá á ááá«áµ áááá¥ á­á½ááá¡á¡


áµá á¥á­á¶ á¨áá«áµááááá áá¨á á ááá¨á á¨á¨á¨á± á áá á¨ááá ááá¨á« ááµá¥ <i>Start conversation</i> á¨áááá áááá á áá«á á¨áá á°á áá­ á áá¨á¡áµ á­ááµ ááá«á¨áµ á­á½ááá¡á¡
ð»áá á á
ááááá á¥á«á á«áááµ á¥á£á­á {} á«áááá©á¡á¡
    """.format(admin_username_html),
    }
    return text

def text_settings() -> dict:
    admin_username_html = mention_html(admin_chat_id, "Admin")
    text = {
    "eng": """
<u>Settings menu</u>

<i>You can filter your voice chat partners by gender by pressing <b>Filter partners by gender</b>button, if you are standard/elite member or if you have more than {} invite points.</i>   

<i>~Your invite link can be found in the profile option.</i>
For any kind of question, please contact the {}.
<b>Please Join Our Channel @{}</b>.
""".format(invite_upgrade, admin_username_html, channel_username),

    "amh": """
<u>Settings menu</u>

<i>standard/elite á á£á á¨áá áá­á {} á¨áá¥á£ áá¥á¦á½ á«ááµ á£ <b>Filter partners by gender</b> á¨áááá ááá á áá«á á¨á áá®á áá³ ááá¨á¥ á­á½ááá¢</i>   

<i>~á¨áá¥á£ ááá­ á profile á áá«á­ ááµá¥ á­áááá¢</i>
áááááá áá­ááµ á¥á«á á¥á£á­áá {} á«áááá©á¢
<b>á¥á£á­áá á»ááá½áá á­áááá @{}</b>
""".format(invite_upgrade, admin_username_html, channel_username),
}

    return text

def text_searching(profile: dict) -> dict:
    text = {
        "eng": "ð<i>Searching for a partner with interest: <b>{}</b> ...</i>".format(profile["interest"]),
        "amh": "ð<i>á¨áá­á­áµ á áá­ á¥á¨ááá© ááá¢ á¨áá­á­áµ á­ááµ áá­á«: <b>{}</b> ...</i>".format(profile["interest"]),
    }
    return text

def text_paired(profile: dict) -> dict:
    vip = ""
    if profile["membership"] >= 1:
        vip = "ð<b>VIP MEMBER</b>ð¥ð¥ð¥"
    text = {
        "eng": """{}
ð¥Partner found!
-Your partner nickname is <b>{}</b>, horoscope: <b>{}</b>, has been into <b>{}</b> conversations, has a rate of <b>{}/10</b> and he/she is from <b>{}</b>.

<b>-Send a voice message saying hello or any voice to start the conversation</b>.

<i>~You can end the conversation by pressing the <b>End conversation</b> button.</i>""".format(vip, profile["nickname"], profile["horoscope"], profile["conversations"], profile["rate"], profile["location"]),

    "amh": """{}
ð¥á¨áá­á­áµ á áá­ á°ááá·á!
-á¨á£áá°á¨á£á áá½á áµá <b>{}</b> áá á£ á¨á®á¨á¥ ááá­áµ: <b>{}</b> á£ <b>{}</b> áá­á­á¶á½á á áµá­ááá á£ <b>{}/10</b> á°á¨á á°á°á·á¸áá á¥á á¥á±/á¥á· á«ááµ <b>{}</b> ááá¢

<b>-áá­á­á±á ááááá­ á°áá áá­á áááááá ááá­ á áááá­ á¨áµáá áááá­áµ á­áá©</b>.

<i>~<b>End conversation</b> áááá á áá«á áá­á­á±á ááá¨á¥ á­á½ááá¢</i>""".format(vip, profile["nickname"], profile["horoscope"], profile["conversations"], profile["rate"], profile["location"]),
    }
    return text

def text_conversation_ended(profile: dict) -> dict:
    text = {
        "eng": """<b>The conversation with partner: <i>{}</i> is closed</b>.
Join our channel for updates @{}.

<i>~Please press <b>Start conversation</b> button to start a new conversation with another random user.</i>

<b>-Rate {} out of 10 base on the conversation you had, from the options bellow.</b>""".format(profile["nickname"], channel_username, profile["nickname"]),

        "amh": """<b>á¨á£áá°á¨á£ <i>{}</i> áá­ á¨áá á¨á áá­á­áµ á°ááá·áá¢</b>
á á³á²áµ áá¨ááá½á ááµá áááá á£ á»ááá½áá á­áááá @{}.

<i>~á¨áá á°á áá áá­ á á²áµ áá­á­áµ ááááá­ á¥á£á­á <b>Start conversation</b> á¨áááá áááá á­á«áá¢</i>

<b>-á¨áá á á³á½ á«ááµ á áá«á®á½ ááµá¥ á{} á áá á¨á áá­á­áµ áá­ á°ááµá­á³á¹ á¨ 10 á°á¨á á­áµá¡á¢</b>""".format(profile["nickname"], channel_username, profile["nickname"]),
    }
    return text

def text_cant_change_nickname(days: int) -> dict:
    text = {
        "eng": """You can NOT change your nickname at this time.
Please try again after <b>{} days</b>.

<i>~Remember you can change your nickname once in a week.</i>""".format(days),

        "amh": """áá½á áµááá á áá áá áááá¥ á á­á½ááá¢
á¥á£á­á á¨ <b>{} áááµ</b> á áá á¥áá°áá á­áá­á©á¢

<i>~á«áµá³áá± áá½á áµááá á á³áááµ á ááµ áá á¥á» áá áááá¥ á¨áá½ááµá¡á¡</i>""".format(days),
    }
    return text

def text_nickname_updated(nickname: str) -> dict:
    text = {
        "eng": """You changed your nickname to <b>{}</b>.
        
<i>~You can change your nickname again after a week.</i>""".format(nickname),

        "amh": """áá½á áµááá áá° <b>{}</b> á ááááá.
        
<i>~á¨á³áááµ á áá áá½á áµááá á¥áá°áá áááá¥ á­á½ááá¡á¡</i>""".format(nickname),
    }
    return text

def text_nickname_length_error() -> dict:
    text = {
        "eng": """You can NOT have a nickname less than <b>{}</b> and more than <b>{}</b> characters.
Please try again.""".format(nickname_length_min, nickname_length_max),

        "amh": """á¨ <b>{}</b> á«áá° á¥á á¨ <b>{}</b> á¨á áá  áá á«áá áá½á áµá ááá­ááµ á á­á½ááá¢
á¥á£á­á á¥áá°áá á­áá­á©.""".format(nickname_length_min, nickname_length_max),
    }
    return text

def text_rate_success(profile: dict, rate: int) -> dict:
    text = {
        "eng": """<b>The conversation with partner: <i>{}</i> is closed</b>.
Join our channel for updates @{}.

<i>~Please press <b>Start conversation</b> button to start a new conversation with another random user.</i>

You rated <b>{}</b>, {}/10.""".format(profile["nickname"], channel_username, profile["nickname"], rate),

        "amh": """<b>á¨á£áá°á¨á£ <i>{}</i> áá­ á¨áá á¨á áá­á­áµ á°ááá·áá¢</b>
á á³á²áµ áá¨ááá½á ááµá áááá á£ á»ááá½áá á­áááá @{}.

<i>~á¨áá á°á áá áá­ á á²áµ áá­á­áµ ááááá­ á¥á£á­á <b>Start conversation</b> á¨áááá áááá á­á«áá¢</i>

á <b>{}</b> á£ {}/10 á°á¨á á°á¥á°áá á¡á¡""".format(profile["nickname"], channel_username, profile["nickname"], rate),
    }
    return text

def text_invite(link: str) -> dict:
    text = {
        "eng": """<b>This is your invitation link...</b>
{}

<i>~Earn invitation points by sharing the link for friends, family and groups.</i>
<i>~{} Invite points will upgrade your membership to standard for 1 day and help you to unlock extra features like: filtering voice chat partners with gender.</i>""".format(link, invite_upgrade),
        "amh": """<b>á­á á¨á¥á­áµá á¨áá¥á£ á ááá áá ...</b>
{}

<i>~ááá°áá½ á£ áá¤á°á°á¥ á¥á áá¡áµá ááá©á á ááá«áµ á¨áá¥á£ áá¥á¦á½á á«ááá¡á¡</i>
<i>~{} á¨áá¥á£ áá¥á¦á½á ááááµ áá° standard á á£áááµ á 1 áá á¨áá«á¸ááá® á²áá á á°á¨ááªá á á­á¨áµ á«á á¥ááá¥ááá½á á¥ááµá³áá á­á¨á³áá³áá¢-á¨áá­á­áµ á áá®á½á á áá³ ááá¨á¥ á­á½ááá¡á¡</i>""".format(link, invite_upgrade),
    }
    return text

def text_membership_upgraded(profile: dict) -> dict:
    membership = "<i>Not a member</i>"
    if profile["membership"] == 1:
        membership = "Standard"  
    elif profile["membership"] == 2:
        membership = "Elite"

    expire_date = ""
    if profile["expire_date"] != None:
            dt = profile["expire_date"]
            expire_date = "{}/{}/{}".format(dt.day, dt.month, dt.year)
    text = {
        "eng": """
ð <b>NOTOFICATION</b>

Dear {}, You have upgraded your membership type to <b>{}</b>.
You can use all the {} membership features until <b>{}</b>.

<i>Thank you for using our platform.</i>
""".format(profile["nickname"], membership, membership, expire_date),

        "amh": """
ð <b>NOTOFICATION</b>

ááµ {} á£ á¨á á£áááµáá á á­ááµ áá° <b>{}</b> á á»á½áááá¢
á¥áµá¨ <b>{}</b> áµá¨áµ áááá {} á¨á á£áááµ á£ááªá«áµá áá áá á­á½ááá¢

<i>á¨á¥áá áµááá¨á¡ á¥ááá°ááááá¡á¡</i>
""".format(profile["nickname"], membership, membership, expire_date),
    }
    return text


# Promotion texts

text_promo_none = {
    "amh": """
<b>á á²áµ áá</b>ð¤­ð¤­ð¤­

á¥áµá«áá ááá á á­ááµ áá­á­áµ á áá°á¨ááá¢ áá¬ á áªá á¥á á¥á á°á áááá½ áµááá¡ /start_conversation á¨áááá á ááá«áµ á¨á á²áµ á°á áá­ á­á°áááá¢ ð

<i>"Your Network is your Networth"</i>
"""
}


text_promo_once = {
    "amh": """
<b>á á²áµ áá</b>ð¤­ð¤­ð¤­

á¥áµá«áá ááá á á­ááµ áá­á­áµ á áá°á¨ááá¢ áá¬ á áªá á¥á á¥á á°á áááá½ áµááá¡ /start_conversation á¨áááá á ááá«áµ á¨á á²áµ á°á áá­ á­á°áááá¢ ð 

<i>"Your Network is your Networth"</i>
"""
}

text_promo_twice = {
    "amh": """
<b>á á²áµ áá</b>ð¤­ð¤­ð¤­

á°ááá áááá á¥ááá á£ ááá? áá¬ á¥á á¥á á áªá á°á áááá½ áµááá¡ á¥áµá² <b>Start conversation</b> á¨áááá áááá á áá«á áá³ á áá¢

á áá«á­ á°á á¶á áááááµ á¨ááá áá­á áá³á¸á áááµ á­áá á´áµ ááá¨á¥ á«á°á á£ á¨áµá­ <b>Upgrade membership</b> á¨áááá á­á«áá¢

<i>"Your Network is your Networth"</i>
"""
}
