from config import *
from telegram.utils.helpers import mention_html


# Buttons

button_lang = {
    "eng": "🇬🇧English",
    "amh": "🇪🇹አማርኛ",
}

button_male = {
    "eng": "👨Male",
    "amh": "👨Male",
}

button_female = {
    "eng": "👩Female",
    "amh": "👩Female",
}

button_start = {
    "eng": "🟢Start conversation",
    "amh": "🟢Start conversation",
}

button_end = {
    "eng": "🔴End conversation",
    "amh": "🔴End conversation",
}

button_profile = {
    "eng": "🗒View profile",
    "amh": "🗒View profile",
}

button_settings = {
    "eng": "🔧Settings",
    "amh": "🔧Settings",
}

button_menu = {
    "eng": "🔙Menu",
    "amh": "🔙Menu",
}

button_back = {
    "eng": "🔙Back",
    "amh": "🔙Back",
}



# Texts

text_lang_changed = {
    "eng": "You changed your language preference to 🇬🇧English.",
    "amh": "የቋንቋ ምርጫዎ ወደ 🇪🇹አማርኛ ተቀይሯል።",
}

text_gender_req = {
    "eng": "Please select your gender.",
    "amh": "እባክዎ የእርሶን ፆታ ይምረጡ።",
}

text_menu = {
    "eng": "<i>Please select from the options below.</i>",
    "amh": "<i>እባክዎ ከታች ካሉት አማራጮች ውስጥ ይምረጡ፡፡</i>",
}

text_cant_start_conv = {
    "eng": """-You can NOT start a new conversation while you are already having one or while you are searching for a new partner.
-You must end the conversation first.

<i>~press the <b>End conversation</b> button to end the current conversation.</i>""",
    
    "amh": """-ቀድሞውኑ ውይይት(conversation) እያረጉ ከሆነ ወይም አዲስ አጋር እየፈለጉ ከሆነ ፣ አዲስ ውይይት መጀመር አይችሉም፡፡
-መጀመሪያ ያስጀመሩትን ውይይት መጨረስ/ማቆም አለብዎት፡፡

<i>~ውይይቱን ለማጠናቀቅ/ለመሰረዝ <b>End conversation</b> የሚለውን ቁልፉ ይጫኑ፡፡</i>""",
}

text_no_conversations = {
    "eng": """<b>Conversation ended.</b>
<i>You have got no more conversations to end.</i>""",

    "amh": """<b>ውይይቱ ተጠናቋል፡፡</b>
<i>ከዚ ሌላ የሚያቋርጡት ተጨማሪ ውይይቶች የሉዎትም።</i>""",
}

text_no_partner = {
    "eng": """<b>You do NOT have any partner to chat with.</b>
    
<i>~Please press the <b>Start conversation</b> button from the menu and wait a while until we find you a random partner.</i>""",

    "amh": """<b>የሚወያዩበት አጋር የለዎትም።</b>
    
<i>~እባክዎን ከመምረጫው（menu） ላይ <b>Start conversation</b> የሚለውን ቁልፍ ይጫኑና አወያይ አጋር እስክናገኝልዎ ድረስ ትንሽ ይጠብቁ፡፡</i>""",
}

text_change_nickname_req = {
    "eng": """<b>Please tell me your nickname?</b>
~Your nickname will be shown to your partners while chatting.
<i>example - abebe, miki, betty, almaz</i>""",

    "amh": """<b>እባክዎን ስምዎትን ወይንም ቅጽል ስምዎትን ይንገሩኝ?</b>
~በሚወያዩበት ጊዜ ቅጽል ስምዎ ለባልደረባዎ ይታያል፡፡
<i>ምሳሌ :- አበበ ፣ ሚኪ ፣ ቤቲ</i>""",
}

text_change_nickname_canceled = {
    "eng": "You canceled your request for changing your nickname.",
    "amh": "ቅጽል ስምዎትን ለመቀየር ያቀረቡትን ጥያቄ ሰርዘዋል፡፡",
}

text_error = {
    "eng": "😔Something went wrong while processing your request.",
    "amh": "😔Something went wrong while processing your request.",
}

text_location_req = {
    "eng": "<b>Please choose your current location from the options below.</b>",
    "amh": "<b>እባክዎን አሁን ያሉበትን ቦታ ከታች ካሉት አማራጮች ይምረጡ ፡፡</b>",
}

text_interest_req = {
    "eng": """<b>Please choose your interest of topic from the options below.</b>
<i>~We will use this to find your random partner.</i>""",

    "amh": """<b>እባክዎን ከዚህ በታች ካሉት አማራጮች ውስጥ ለመወያየት የሚፈልጉበትን ርዕሰ ይምረጡ፡፡</b>
<i>~ይህን ርዕሰ የውይይት አጋርዎን ለመፈለግ እንጠቀምበታለን።</i>""",
}

text_horoscope_req = {
    "eng": "<b>Please choose your horoscope(zodiac sign) from the options below.</b>",
    "amh": "<b>እባክዎን ከዚህ በታች ካሉት አማራጮች ውስጥ የእርስዎን የኮከብ ምልክት(zodiac sign) ይምረጡ።</b>",
}

text_under_devt = {
    "eng": "This feature is under development and will be available soon.",
    "amh": "ይህ ምርጫ በመሰራት ላይ ያለ ሲሆን ፣ በቅርቡም ተግባር ላይ ይውላል፡፡",
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

    "amh": """አባልነትዎን ወደ (Standard ወይም Elite) ማሻሻል አለብዎት፡፡
<u>አባልነትን የማሻሻል ጥቅሞች</u>
-አወያይ አጋሮችን በፍጥነት ያገኛሉ(<i>አወያይ አጋሮች ከ እርሶ ጋር የሚጣመሩት ፣ መጀመሪያ አባል ከሆኑ ተጠቃሚዎች ጋር ተጣምረው ከተረፉ ነው</i>)፡፡
-የአጋሮን ፆታ የመምረጥ ችሎታ ይኖሮታል፡፡
-ከ አወያይ አጋሮ ጋር ሲጣመሩ ፣ አጋሮ የ vip አባል መሆናቹን ያውቃሉ፡፡
-እናም ሌሎች ተጨማሪ ብዙ ጥቅማጥቅሞችን ያገኛሉ።

<b>Standard አባልነት:</b>  ወጪው {} ብር ብቻ ሲሆን ከ 1 ሳምንት በኋላ ጊዜው ያበቃል።
<b>Elite አባልነት:</b>  ወጪው {} ብር ብቻ ሲሆን ከ 1 ወር በኋላ ጊዜው ያበቃል።

ከምርጫዎቹ ውስጥ አንዱን ቁልፍ ሲጫኑ ፣ ወደ <b>YenePay</b> ድረ ገጽ ይመራዎታል። ክፍያውን እዚያ ማጠናቀቅ ይችላሉ። 
ክፍያውን ሲያጠናቅቁ አባልነትዎን ወደ መረጡት የአባልነት ዓይነት አሻሽለን የማረጋገጫ ጽሑፍ እንልክልዎታለን፡፡
<i>የሚወስደው ቢበዛ 1 ደቂቃ ብቻ ስለሆነ ፣ እባክዎን አባልነትዎን ለማሻሻል ያስቡበት፡፡</i>

<b>የ yenepay አካውንት（account） ከሌለዎት አዲስ ለማውጣት ስልክ ቁጥር ብቻ በቂ ነው። አካውንት ካወጡ በኋላ ከ (CBE ብር ፣ አሞሌ ፣ ሄሎ ካሽ) ጋር ሊያገናኙት ይችላሉ ፡፡
እንዲሁም ከባንክ ሂሳብዎ (CBE ብር ፣ አሞሌ ፣ ሄሎ ካሽ) ወደ YenePay አካውንትዎ ገንዘብ ማስተላለፍ ይችላሉ።</b>

<i>{} አባላትን ከጋበዙ standard አባልነትን ለ 1 ቀን መጠቀም ይችላሉ</i>
""".format(standard_price, elite_price, invite_upgrade),
}

text_gender_filter = {
    "eng": """
You can filter your random partner gender by selecting one of the buttons.
<i>If you don't mind chatting with any gender please select Both.</i> 
""",

    "amh": """
አንዱን ቁልፍ በመምረጥ የአጋሮን ፆታ መምረጥ ይችላሉ፡፡
<i>ከማንኛውም ፆታ ጋር መወያየት የሚፈልጉ ከሆነ እባክዎን Both የሚለውን ቁልፍ ይምረጡ፡፡</i> 
""",
}

text_not_memeber = {
    "eng": """
<b>You need to be a standard/elite member to access this feature.</b>
<i>You can upgrade your membership type by selecting the <b>Profile</b> option and pressing <b>Upgrade memebership</b> button.</i>
""",

    "amh": """
<b>ይህንን ምርጫ ለመጠቀም standard/elite አባል መሆን አለቦት፡፡</b>
<i>የ <b>Profile</b> አማራጭን በመምረጥ እና <b>Upgrade memebership</b> ቁልፍን በመጫን የአባልነትዎን አይነት ማሻሻል ይችላሉ፡፡</i>
""",
}

text_invite_notification = {
    "eng": """
🔔 <b>NOTOFICATION</b>

Dear user, Thank you for inviting <b>{}</b> members.
Your membership type is updated to <b>Standard</b> for 1 day.

<i>Thank you for using our platform.</i>
""".format(invite_upgrade),

    "amh": """
🔔 <b>NOTOFICATION</b>

ውድ ተጠቃሚ ፣ <b>{}</b> አባላትን ስለጋበዙ እናመሰግናለን፡፡
የአባልነትዎ አይነት ለ 1 ቀን ወደ <b>Standard</b> ተሻሽሏል።

<i>የእኛን ስለመረጡ እናመሰግናለን፡፡</i>
""".format(invite_upgrade),
    }





# Static and long texts
text_about = {
    "eng": """
Hello, I am jordan and I am a programmer based in Addis Ababa, Ethiopia.
I made this bot to let everybody discusss on their favorite topic.

<i>I believe that we sometimes express ourselves freely to someone we don't know (a stranger).</i>
That is why I made this random stranger voice chat bot.

I wish you a memorable chatting session. cheers🍻.

<b>Join our channel for updates</b> @{}
""".format(channel_username),

    "amh": """
ሰላም ጆርዳን እባላለው። የምኖረው አዲስ አበባ ውስጥ ሲሆን ፣ ስራዬ ደሞ programmer ነው።
ይህንን ቦት የሰራውት ሁሉም ሰው በሚፈልገው ርዕስ ላይ ነጻ ሆኖ እንዲወያይ በማሰብ ነው።

<i>አንዳንዴ ጨርሶውኑ ከማናቃቸው ሰዎች ጋር በ አንድ ርዕስ ዙሪያ ነጻ ሆነን እናወራለን ብዬ አስባለው።</i>
ይሄንን ቦት የሰራውት በዚ ምክኒያት ነው።

አሪፍ ጊዜ እንደሚኖራቹ ተስፋ አደርጋለው. cheers🍻.

<b>አዳዲስ ነገሮችን ቀድሞ ለማወቅ ቻናላችንን ይቀላቀሉ </b> @{}
""".format(channel_username),
}







# Text with values

def text_first_time() -> dict:
    admin_username_html = mention_html(admin_chat_id, "ADMIN")
    text = {
        "eng": """👋hi, Nice to meet you. I see that its your first time using this bot. Here are the most valuable things you need to know.

<b>First of all, this bot completely respects your privacy and none of the messages you send will be stored on our server.</b>
<b>Plus, the random voice chat partners you meet won't know who you are. This bot makes you totally anonymous.</b>

~You should change your nickname by pressing <b>Change nickname</b> button. It is displayed as your name while chatting with strangers.
~You should also change your horoscope by pressing <b>Change horoscope</b> button. Other users will see your horoscope while chatting.
~You can change your location by pressing <b>Change location</b> button.
<b>~You must change your interest as it is used to find you a partner with common interest. Please press Change interest button.</b>

-You can visit your profile and notice the changes you made by pressing the <i>Profile</i> button from the main menu.
-Anything you probably want to change can be found in the <i>Settings</i> option.


After you finished setting up your profile, You can chat with another stranger by pressing the <i>Start conversation</i> button from the main menu.
🍻enjoy.
IF YOU HAVE ANY QUESTION, PLEASE CONTACT THE {}.
    """.format(admin_username_html),

        "amh": """👋ሰላም ስለተገናኘን ደስ ብሎኛል። ይህንን ቦት ሲጠቀሙ ለመጀመሪያ ጊዜ እንደሆነ አይቻለሁ፡፡ ማወቅ ያለብዎት በጣም ጠቃሚ ነገሮች ከዚህ በታች ተዘርዝረዋል፡፡

<b>በመጀመሪያ ፣ ይህ ቦት የእርስዎን ግላዊነት ሙሉ በሙሉ የሚያከብር ሲሆን ከላኳቸው መልእክቶች መካከል አንዳቸውም እኛ ጋር አይቀመጡም፡፡</b>
<b>በተጨማሪም ፣ የሚያገኟቸው የውይይት አጋሮች የእርሶን ማንነት አያውቁም፡፡</b>

~<b>Change nickname</b> ቁልፍን በመጫን ቅጽል ስምዎን መለወጥ አለብዎት፡፡ ከአዲስ ሰዎች ጋር በሚወያዩበት ጊዜ እንደ ስምዎ ሆኖ ለነሱ ይታያል፡፡
~እንዲሁም <b>Change horoscope</b> ቁልፍን በመጫን የኮከብ ምልክቶን መለወጥ አለብዎት፡፡ ከሌሎች ተጠቃሚዎች ጋር ሲወያዩ የኮከብ ምልክቶን ያዩታል፡፡
~<b>Change location</b> ቁልፍን በመጫን አhሁን ያሉበትን ከተማ መለወጥ ይችላሉ፡፡
<b>~የጋራ ፍላጎት ያለው የውይይት አጋር ለማግኘት ፣ እርሶ መወያየት የሚፈልጉበትን ርዕስ መለወጥ አለቦት። እባክዎን Change interest የሚለውን ቁልፍ ይጫኑ ፡፡</b>

-ከዋናው መምረጫ ውስጥ <i>Profile</i> የሚለውን ቁልፍ በመጫን ስለ እርሶ ያለውን መረጃ መጎብኘት እና ያደረጉትን ለውጦች ልብ ማለት ይችላሉ ፡፡
-ምናልባት መለወጥ የሚፈልጉት ማንኛውም ነገር ካለ <i>Settings</i> የሚለውን ቁልፍ በመንካት መለወጥ ይችላሉ፡፡


ስለ እርሶ የሚያስፈልገውን መረጃ አዋቅረው ከጨረሱ በኋላ ከዋናው መምረጫ ውስጥ <i>Start conversation</i> የሚለውን ቁልፍን በመጫን ከሌላ ሰው ጋር በመረጡት ርዕስ መወያየት ይችላሉ፡፡
🍻ዘና በሉ
ማንኛውም ጥያቄ ካለዎት እባክዎ {} ያነጋግሩ፡፡
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

<i>standard/elite አባል ከሆኑ ወይም {} የግብዣ ነጥቦች ካሎት ፣ <b>Filter partners by gender</b> የሚለውን ቁልፍ በመጫን የአጋሮን ፃታ መምረጥ ይችላሉ።</i>   

<i>~የግብዣ ሊንክ በprofile አማራጭ ውስጥ ይገኛል።</i>
ለማንኛውም ዓይነት ጥያቄ እባክዎን {} ያነጋግሩ።
<b>እባክዎን ቻናላችንን ይቀላቀሉ @{}</b>
""".format(invite_upgrade, admin_username_html, channel_username),
}

    return text

def text_searching(profile: dict) -> dict:
    text = {
        "eng": "🔎<i>Searching for a partner with interest: <b>{}</b> ...</i>".format(profile["interest"]),
        "amh": "🔎<i>የውይይት አጋር እየፈለኩ ነው። የውይይት ርዕስ ምርጫ: <b>{}</b> ...</i>".format(profile["interest"]),
    }
    return text

def text_paired(profile: dict) -> dict:
    vip = ""
    if profile["membership"] >= 1:
        vip = "🚁<b>VIP MEMBER</b>🔥🔥🔥"
    text = {
        "eng": """{}
💥Partner found!
-Your partner nickname is <b>{}</b>, horoscope: <b>{}</b>, has been into <b>{}</b> conversations, has a rate of <b>{}/10</b> and he/she is from <b>{}</b>.

<b>-Send a voice message saying hello or any voice to start the conversation</b>.

<i>~You can end the conversation by pressing the <b>End conversation</b> button.</i>""".format(vip, profile["nickname"], profile["horoscope"], profile["conversations"], profile["rate"], profile["location"]),

    "amh": """{}
💥የውይይት አጋር ተገኝቷል!
-የባልደረባዎ ቅጽል ስም <b>{}</b> ነው ፣ የኮከብ ምልክት: <b>{}</b> ፣ <b>{}</b> ውይይቶችን አድርገዋል ፣ <b>{}/10</b> ደረጃ ተሰቷቸዋል እና እሱ/እሷ ያሉት <b>{}</b> ነው።

<b>-ውይይቱን ለመጀመር ሰላም ወይም ማንኛውንም ነገር በነማገር የድምፅ መልዕክት ይላኩ</b>.

<i>~<b>End conversation</b> ቁልፍን በመጫን ውይይቱን ማቋረጥ ይችላሉ።</i>""".format(vip, profile["nickname"], profile["horoscope"], profile["conversations"], profile["rate"], profile["location"]),
    }
    return text

def text_conversation_ended(profile: dict) -> dict:
    text = {
        "eng": """<b>The conversation with partner: <i>{}</i> is closed</b>.
Join our channel for updates @{}.

<i>~Please press <b>Start conversation</b> button to start a new conversation with another random user.</i>

<b>-Rate {} out of 10 base on the conversation you had, from the options bellow.</b>""".format(profile["nickname"], channel_username, profile["nickname"]),

        "amh": """<b>ከባልደረባ <i>{}</i> ጋር የነበረው ውይይት ተዘግቷል።</b>
አዳዲስ መረጃዎችን ቀድሞ ለማወቅ ፣ ቻናላችንን ይቀላቀሉ @{}.

<i>~ከሌላ ተጠቃሚ ጋር አዲስ ውይይት ለመጀመር እባክዎ <b>Start conversation</b> የሚለውን ቁልፍን ይጫኑ።</i>

<b>-ከዚህ በታች ካሉት አማራጮች ውስጥ ለ{} በነበረው ውይይት ላይ ተመስርታቹ ከ 10 ደረጃ ይስጡ።</b>""".format(profile["nickname"], channel_username, profile["nickname"]),
    }
    return text

def text_cant_change_nickname(days: int) -> dict:
    text = {
        "eng": """You can NOT change your nickname at this time.
Please try again after <b>{} days</b>.

<i>~Remember you can change your nickname once in a week.</i>""".format(days),

        "amh": """ቅጽል ስምዎን በዚህ ጊዜ መለወጥ አይችሉም።
እባክዎ ከ <b>{} ቀናት</b> በኋላ እንደገና ይሞክሩ።

<i>~ያስታውሱ ቅጽል ስምዎን በሳምንት አንድ ጊዜ ብቻ ነው መለወጥ የሚችሉት፡፡</i>""".format(days),
    }
    return text

def text_nickname_updated(nickname: str) -> dict:
    text = {
        "eng": """You changed your nickname to <b>{}</b>.
        
<i>~You can change your nickname again after a week.</i>""".format(nickname),

        "amh": """ቅጽል ስምዎን ወደ <b>{}</b> አዘምነዋል.
        
<i>~ከሳምንት በኋላ ቅጽል ስምዎን እንደገና መለወጥ ይችላሉ፡፡</i>""".format(nickname),
    }
    return text

def text_nickname_length_error() -> dict:
    text = {
        "eng": """You can NOT have a nickname less than <b>{}</b> and more than <b>{}</b> characters.
Please try again.""".format(nickname_length_min, nickname_length_max),

        "amh": """ከ <b>{}</b> ያነሰ እና ከ <b>{}</b> የበለጠ ሆሄ ያለው ቅጽል ስም ሊኖርዎት አይችልም።
እባክዎ እንደገና ይሞክሩ.""".format(nickname_length_min, nickname_length_max),
    }
    return text

def text_rate_success(profile: dict, rate: int) -> dict:
    text = {
        "eng": """<b>The conversation with partner: <i>{}</i> is closed</b>.
Join our channel for updates @{}.

<i>~Please press <b>Start conversation</b> button to start a new conversation with another random user.</i>

You rated <b>{}</b>, {}/10.""".format(profile["nickname"], channel_username, profile["nickname"], rate),

        "amh": """<b>ከባልደረባ <i>{}</i> ጋር የነበረው ውይይት ተዘግቷል።</b>
አዳዲስ መረጃዎችን ቀድሞ ለማወቅ ፣ ቻናላችንን ይቀላቀሉ @{}.

<i>~ከሌላ ተጠቃሚ ጋር አዲስ ውይይት ለመጀመር እባክዎ <b>Start conversation</b> የሚለውን ቁልፍን ይጫኑ።</i>

ለ <b>{}</b> ፣ {}/10 ደረጃ ሰጥተዋል ፡፡""".format(profile["nickname"], channel_username, profile["nickname"], rate),
    }
    return text

def text_invite(link: str) -> dict:
    text = {
        "eng": """<b>This is your invitation link...</b>
{}

<i>~Earn invitation points by sharing the link for friends, family and groups.</i>
<i>~{} Invite points will upgrade your membership to standard for 1 day and help you to unlock extra features like: filtering voice chat partners with gender.</i>""".format(link, invite_upgrade),
        "amh": """<b>ይህ የእርስዎ የግብዣ አገናኝ ነው ...</b>
{}

<i>~ለጓደኞች ፣ ለቤተሰብ እና ለቡድን ሊንኩን በማጋራት የግብዣ ነጥቦችን ያግኙ፡፡</i>
<i>~{} የግብዣ ነጥቦችን ማግኘት ወደ standard አባልነት ለ 1 ቀን የሚያሸጋግሮ ሲሆን በተጨማሪም በርከት ያሉ ጥቅማጥቅሞችን እንድታገኙ ይረዳዎታል።-የውይይት አጋሮችን በፆታ መምረጥ ይችላሉ፡፡</i>""".format(link, invite_upgrade),
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
🔔 <b>NOTOFICATION</b>

Dear {}, You have upgraded your membership type to <b>{}</b>.
You can use all the {} membership features until <b>{}</b>.

<i>Thank you for using our platform.</i>
""".format(profile["nickname"], membership, membership, expire_date),

        "amh": """
🔔 <b>NOTOFICATION</b>

ውድ {} ፣ የአባልነትዎን አይነት ወደ <b>{}</b> አሻሽለዋል።
እስከ <b>{}</b> ድረስ ሁሉንም {} የአባልነት ባህሪያትን መጠቀም ይችላሉ።

<i>የእኛን ስለመረጡ እናመሰግናለን፡፡</i>
""".format(profile["nickname"], membership, membership, expire_date),
    }
    return text


# Promotion texts

text_promo_none = {
    "amh": """
<b>አዲስ ዜና</b>🤭🤭🤭

እስካሁን ምንም አይነት ውይይት አላደረጉም። ዛሬ አሪፍ እና ብዙ ተጠቃሚዎች ስለገቡ /start_conversation የሚለውን በመንካት ከአዲስ ሰው ጋር ይተዋወቁ። 😜

<i>"Your Network is your Networth"</i>
"""
}


text_promo_once = {
    "amh": """
<b>አዲስ ዜና</b>🤭🤭🤭

እስካሁን ምንም አይነት ውይይት አላደረጉም። ዛሬ አሪፍ እና ብዙ ተጠቃሚዎች ስለገቡ /start_conversation የሚለውን በመንካት ከአዲስ ሰው ጋር ይተዋወቁ። 😜 

<i>"Your Network is your Networth"</i>
"""
}

text_promo_twice = {
    "amh": """
<b>አዲስ ዜና</b>🤭🤭🤭

ሰሞኑን ቀዝቀዝ ብለዋል ፣ ምነው? ዛሬ ብዙ እና አሪፍ ተጠቃሚዎች ስለገቡ እስቲ <b>Start conversation</b> የሚለውን ቁልፍን በመጫን ፉታ በሉ።

አወያይ ሰው ቶሎ ለማግኘት ከፈለጉ ወይም ፆታቸው ወንድ ይሁን ሴት መምረጥ ካሰኞ ፣ ከስር <b>Upgrade membership</b> የሚለውን ይጫኑ።

<i>"Your Network is your Networth"</i>
"""
}
