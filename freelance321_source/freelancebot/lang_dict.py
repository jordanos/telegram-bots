from config import *
from backend import Db
import random
from telegram.utils.helpers import mention_html


# Buttons

button_lang = {
    "eng": "🇺🇸English",
    "amh": "🇪🇹አማርኛ",
}


button_register = {
    "eng": "🗒Register",
    "amh": "🗒ልመዝገብ",
}

button_login_freelancer = {
    "eng": "Freelancer",
    "amh": "ባለሙያ",
}

button_login_employer = {
    "eng": "Employer",
    "amh": "ቀጣሪ",
}

button_share_number = {
    "eng": "📞Share my number",
    "amh": "📞ስልክ ቁጥሬን አጋራ",
}

button_profile = {
    "eng": "👦Profile",
    "amh": "👦መገለጫ",
}

button_help = {
    "eng": "🤷‍♂️Help",
    "amh": "🤷‍♂️እርዳታ ላግኝ",
}

button_lang_setting = {
    "eng": "Language/ቋንቋ",
    "amh": "Language/ቋንቋ",
}

button_deposit = {
    "eng": "💵Deposit",
    "amh": "💵ገንዘብ ገቢ ላርግ",
}

button_cashout = {
    "eng": "💵Cash out",
    "amh": "💵ገንዘብ ወጪ ላርግ",
}

button_post_job = {
    "eng": "📝 Post Job",
    "amh": "📝 ስራ ልለጥፍ",
}

button_jobs = {
    "eng": "🛠Jobs",
    "amh": "🛠ስራዎቼን ልይ",
}

button_logout = {
    "eng": "🔙Log out",
    "amh": "🔙ውጣ",
}

button_main = {
    "eng": "🔙 Main Menu",
    "amh": "🔙 ወደ ዋናው መምረጫ ሂድ",
}

button_submit = {
    "eng": "Submit",
    "amh": "አስገባ",
}

button_edit = {
    "eng": "Edit",
    "amh": "ላስተካክል",
}

button_skip = {
    "eng": "Skip",
     "amh": "እለፍ",
}

button_permanent = {
    "eng": "Permanent",
     "amh": "ቋሚ",
}

button_hour = {
    "eng": "Hourly",
     "amh": "በሰአት",
}

button_part = {
    "eng": "Part Time",
     "amh": "በትርፍ ሰአት",
}

button_contract = {
    "eng": "Contractual",
     "amh": "የውል",
}

button_remote = {
    "eng": "Remote",
     "amh": "በርቀት",
}

button_software = {
    "eng": "Software",
     "amh": "ሶፍትዌር",
}

button_tutor = {
    "eng": "Tutor",
     "amh": "አስጠኚ",
}

button_graphics = {
    "eng": "Graphics",
     "amh": "ግራፊክስ",
}

button_video = {
    "eng": "Video Editing",
     "amh": "ቪዲዮ ኤዲቲንግ",
}

button_music = {
    "eng": "Music&Art",
     "amh": "የጥበብ ስራዎች",
}

button_web = {
    "eng": "Website Design",
     "amh": "የዌብሳይት ዲዛይን",
}

button_business = {
    "eng": "Business",
     "amh": "ንግድ",
}

button_other = {
    "eng": "Other",
     "amh": "እዚህ ውስጥ አልተጠቀሰም",
}

button_entery = {
    "eng": "Entery Level",
     "amh": "ጀማሪ",
}

button_intermidiate = {
    "eng": "Intermideate Level",
     "amh": "መካከለኛ",
}

button_expert = {
    "eng": "Expert Level",
     "amh": "የላቀ",
}

button_10 = {
    "eng": "1 - 10",
     "amh": "1 - 10",
}

button_20 = {
    "eng": "10 - 20",
     "amh": "10 - 20",
}

button_30 = {
    "eng": "20 - 30",
     "amh": "20 - 30",
}

button_opened = {
    "eng": "Opened",
     "amh": "የተከፈቱ",
}

button_closed = {
    "eng": "Closed",
     "amh": "የተዘጉ",
}

button_pending = {
    "eng": "Pending",
     "amh": "በመጠባበቅ ላይ ያሉ",
}

button_declined = {
    "eng": "Declined",
     "amh": "ውድቅ የተደረጉ",
}

button_yes = {
    "eng": "Yes",
     "amh": "አዎ",
}

button_no = {
    "eng": "No",
     "amh": "አይ",
}

button_continue = {
    "eng": "Continue",
     "amh": "ቀጥል",
}

button_cancel = {
    "eng": "Cancel",
     "amh": "አቋርጥ",
}

button_buy_coins = {
    "eng": "Buy coins",
     "amh": "Coin ልግዛ",
}

button_days_1 = {
    "eng": "1 day",
     "amh": "1 ቀን",
}

button_days_3 = {
    "eng": "3 days",
     "amh": "3 ቀን",
}

button_days_7 = {
    "eng": "7 days",
    "amh": "7 ቀን",
}

button_days_15 = {
    "eng": "15 days",
    "amh": "15 ቀን",
}

button_days_30 = {
    "eng": "30 days",
    "amh": "30 ቀን",
}

button_assign = {
    "eng": "Assign",
    "amh": "መድብ",
}

button_deassign = {
    "eng": "DeAssign",
    "amh": "ከምድብ አውጣ",
}

button_delete = {
    "eng": "Delete",
    "amh": "ሰርዝልኝ",
}

button_close = {
    "eng": "Close",
    "amh": "ዝጋልኝ",
}

button_verify = {
    "eng": "Verify",
    "amh": "ማንነቴን ላረጋግጥ",
}

button_admin = {
    "eng": "Admins",
    "amh": "አስተዳዳሪዎች",
}

button_mark = {
    "eng": "Mark As Read",
    "amh": "አንብቤዋለው",
}

button_rate = {
    "eng": "Rate",
    "amh": "ነጥብ ልስጥ",
}

button_update_level = {
    "eng": "Update Level",
    "amh": "ደረጃዬን ከፍ ላርግ",
}













# Text informations

text_change_lang= {
    "eng": "Please, choose your language preference.\n*(Currently the bot only supports english language), Other languages will be added soon.",
    "amh": "እባክዎ ቋንቋ ይምረጡ።",
}

text_error = {
    "eng": "❌Something went wrong while processing your request...",
    "amh": "❌ጥያቄዎትን በማስተናገድ ላይ እያለን ያልታወቀ ችግር ተፈጥሯል።",
}

text_success = {
    "eng": "Your request has been executed successfully.",
    "amh": "ጥያቄዎ ብበተሳካ ሁኔታ ተፈጵሟል።",
}

text_welcome = {
    "eng": "Welcome!",
    "amh": "እንኳን በደና መጡ።",
}

text_register_req = {
    "eng": "You must register to use this bot.",
    "amh": "ይህንን ቦት ለመጠቀም መመዝገብ ግዴታ ነው።",
}

text_already_registered = {
    "eng": "You have already registered.",
    "amh": "አስቀድመው ተመዝግበዋል።",
}

text_login = {
    "eng": "Login as a freelancer or employer?",
    "amh": "እንደ ባለሙያ ወይስ ቀጣሪ ፣ መግባት የሚፈልጉት?",
}

text_share_number_req = {
    "eng": "Please press the [Share_my_number] button to continiue.",
    "amh": "ለመቀጠል ስልክ ቁጥሬን አጋራ የሚለውን ቁልፍ ይጫኑ።",
}

text_job_title_req = {
    "eng": "Please, tell me the title of the job?",
    "amh": "እባክዎን የስራውን ርዕስ ይንገሩኝ።",
}

text_job_discription_req = {
    "eng": "Please, tell me the discription of the job?",
    "amh": "እባክዎን የስራውን ዝርዝር ይንገሩኝ።",
}

text_job_company_req = {
    "eng": "Please, tell me your Company Name?",
    "amh": "እባክዎን የድርጅታችሁን ስም ይንገሩኝ።",
}

text_job_limit_req = {
    "eng": "The maximium number of proposals you wish to receive.",
    "amh": "ምን ያህል ፕሮፖዛል መቀበል ይፈልጋሉ።",
}

text_job_type_req = {
    "eng": "Please, choose JobType.",
    "amh": "ምን አይነት ስራ እንደሆነ ከምርጫዎቹ ውስጥ ይምረጡ ።",
}

text_job_cat_req = {
    "eng": "Please, choose Category.",
    "amh": "እባክዎን የስራውን አይነት ይምረጡ።",
}

text_job_level_req = {
    "eng": "What kind of freelancers are you looking for this job?",
    "amh": "ምን አይነት ሰራተኛ ይፈልጋሉ?",
}

text_job_deposit_req = {
    "eng": "You can make a deposit for contractual jobs and issue the paymnet when the job gets done.\n*Remember making a deposit increases the chance of attracting great freelancers. and we assure you that they are only paid when the job is completed.\nIf not, We guarantee that every penny will be returned to your account.\nDo you want to make a deposit for this job?",
    "amh": "ለ የውል ስራ አይነቶች እከፍላለው ያሉትን ገንዘብ አስይዘው ስራውን ማስጀመር ይችላሉ። ገንዘቡ ለተቀጣሪው ገቢ የሚደረገው ስራውን በአግባቡ ሲጨርስና እርሶ ሲፈቅዱ ብቻ ነው ።\n~እንዲ ማድረግ ያስፈለገው, በውል ስራዎች ላይ በቀጣሪና ተቀጣሪ መካከል የመጨረሻ ክፍያ ላይ ያለውን አለመተማመን ለመቀነስ ነው ።\nለዚህ ስራ እከፍላለው ያሉትን ገንዘብ ማስያዝ ይፈልጋሉ ?",
}

text_job_deposit_made = {
    "eng": "✅You have made a deposit for this job.\nPreparing job...",
    "amh": "✅ለዚህ ስራ ገንዘብ ገቢ አርገዋል።\nስራውን እያዘጋጀው ነው...",
}

text_permanent_price = {
    "eng": "Price for the freelancers should be above 50 birr!\n~It could be one time payment or monthly.\nPlease, input price again.",
    "amh": "የሰራተኞች ክፍያ ከ 50 ብር በላይ መሆን አለበት!\n~የአንድ ጊዜ ክፍያ ወይም ወርሃዊ ሊሆን ይችላል።\n እባክዎን ክፍያውን እንደገና ያስገቡ ።",
}

text_hourly_price = {
    "eng": "Price for the freelancers should be above 10 birr per hour!\nPlease, input price again.",
    "amh": "የሰራተኞች ክፍያ በሰአት ከ 10 ብር በላይ መሆን አለበት!\nእባክዎን ክፍያውን እንደገና ያስገቡ ።",
}

text_title_length = {
    "eng": "❌Job title length must be over 3 and less than 50 characters!\nPlease try again.",
    "amh": "❌የሥራ ርዕስ ርዝመት ከ 3 በላይ እና ከ 50 በታች ሆሄዎች መሆን አለበት!\nእባክዎን እንደገና ይሞክሩ ።",
}

text_company_length = {
    "eng": "❌Company name length must be over 1 and less than 50 characters!\nPlease try again.",
    "amh": "❌የኩባንያ ስም ርዝመት ከ 1 በላይ እና ከ 50 ያልበለጠ ሆሄዎች መሆን አለበት!\nእባክዎን እንደገና ይሞክሩ ።",
}

text_discription_length = {
    "eng": "❌Discription length must be over 5 characters!\nPlease try again.",
    "amh": "❌የዝርዝር ርዝመት ከ 5 ሆሄዎች በላይ መሆን አለበት!\nእባክዎን እንደገና ይሞክሩ ።",
}

text_numbers_only = {
    "eng": "❌Only numbers are accepted!\nPlease try again.",
    "amh": "❌ቁጥሮች ብቻ ተቀባይነት አላቸው!\nእባክዎን እንደገና ይሞክሩ ።",
}

text_option_below = {
    "eng": "❌Please, Choose from the options below!",
    "amh": "❌እባክዎን ከታች ካሉት አማራጮች ውስጥ ይምረጡ!",
}

text_edit_job_req = {
    "eng": "okay, lets edit the job...",
    "amh": "እሺ ፣ ስራውን እናስተካክል ...",
}

text_under_development = {
    "eng": "We are currently working on this feature.",
    "amh": "በዚህ አገልግሎት ላይ እየሰራን ነው፡፡",
}

text_not_enough_balance = {
    "eng": "❌You don't have enough balance to perform your request.\n~Please use the deposit option from the main_menu to recharge your account.",
    "amh": "❌ጥያቄዎን ለማከናወን በቂ ገንዘብ የለዎትም ፡፡\n~ሂሳብዎን ለመሙላት እባክዎ ከዋናው መምረጫ የተቀመጠውን ገንዘብ ገቢ ላርግ የሚለውን አማራጭ ይጠቀሙ።",
}

text_not_enough_coins = {
    "eng": "❌You don't have enough coins to perform your request.\n~Please use the buy coins option from the profile menu, to buy coins.",
    "amh": "❌ጥያቄዎን ለማከናወን በቂ coin የለዎትም ፡፡\n~coin ለመሙላት እባክዎ መግለጫ ውስጥ የተቀመጠውን coin ገቢ ላርግ የሚለውን አማራጭ ይጠቀሙ።",
}

text_canceled = {
    "eng": "Your request has been canceled.",
    "amh": "ጥያቄዎ ተሰርዟል።",
}

text_welcome_admin = {
    "eng": "Welcome back dear admin.",
    "amh": "እንኳን ደህና መጡ ውድ አስተዳዳሪ፡፡",
}

text_not_admin = {
    "eng": "❌You are not eligiable to access this feature!",
    "amh": "❌ይህንን መስተንግዶ ለማግኘት ፈቃድ የሎትም!",
}

text_cant_sub_job = {
    "eng": "❌An error has occured while submitting your job.\n~Please, check if you have the required amount of coins.\n~Contact the admins for more.",
    "amh": "❌ሥራዎን በሚያስገቡበት ጊዜ አንድ ስህተት ተከስቷል።\n~እባክዎን የሚያስፈልገው coin ካሉዎት ያረጋግጡ፡፡\n~ለተጨማሪ መረጃ አስተዳዳሪዎቹን ያነጋግሩ።",
}

text_job_sent = {
    "eng": "✅Your request has been sent.\nPlease, wait a while until the admin approves your request.",
    "amh": "✅ጥያቄዎ ተልኳል ፡፡\nእባክዎን አስተዳዳሪው ጥያቄዎን እስኪያፀድቅ ድረስ ትንሽ ይጠብቁ፡፡",
}

text_buy_coins_req = {
    "eng": "How much coins do you want?\n~Remember 1 coin = 1 birr.\n~You should have enough balance to get the ammount of coins of your choice.\n~Please tell me the ammount of coins you need?",
    "amh": "ምን ያህል ሳንቲሞች ይፈልጋሉ?\n~ያስታውሱ 1 coin = 1 ብር ፡፡\n~የመረጡትን coin ብዛት ለማግኘት በቂ ገንዘብ ሊኖርዎት ይገባል፡፡\n~እባክዎን የሚፈልጉትን coin ብዛት ይንገሩኝ?",
}

text_cant_apply = {
    "eng": "❌You can't apply for this job right now.\n~Check if you are on the required level.\n~Check if the job is still open.",
    "amh": "❌ለዚህ ሥራ በአሁኑ ጊዜ ማመልከት አይችሉም፡፡\n~ሥራው በሚፈለገው ደረጃ ላይ እንዳሉ ያረጋግጡ፡፡\n~ሥራው አስካሁን ክፍት መሆኑን ያረጋግጡ፡፡",
}

text_cant_apply_for_own_job = {
    "eng": "❌You cant apply for your own job.",
    "amh": "❌ለራስዎ ሥራ ማመልከት አይችሉም፡፡",
}

text_proposal_discription_req = {
    "eng": "Please tell me your proposal for this job.\n~It should be more than 15 and less than 250 characters.\n~The proposal should talk about what you are willing to do for the job, what are your qualifications, and why should the employer choose you.",
    "amh": "እባክዎን ለዚህ ሥራ ያቀረቡትን ሀሳብ ይንገሩኝ፡፡\n~ሃሳብዎ ከ 15 በላይ እና ከ 250 በታች ሆሄ መያዝ አለበት፡፡\n~የሀሳቡ ዝርዝር ላይ ለሥራው ምን ለማድረግ ፈቃደኛ እንደሆኑ ፣ ብቃቶችዎ ምንድን እንደሆኑ እና ለምን ሥራውን እንደመረጡ መናገር አለቦት፡፡",
}

text_proposal_discription_length = {
    "eng": "❌Discription length can NOT be less than 15 and more than 250 characters!\nPlease try again.",
    "amh": "❌የሃሳቦ ርዝመት ከ 15 በታች እና ከ 250 በላይ ሆሄዎች ሊሆን አይችልም!\n እባክዎ እንደገና ይሞክሩ።",
}

text_proposal_days_req = {
    "eng": "How many days at maximum will it take you, for completing this job?",
    "amh": "ይህንን ሥራ ለማጠናቀቅ ቢበዛ ስንት ቀናት ይፈጅብዎታል?",
}

text_proposal_price_req = {
    "eng": "What is the maximum price you are asking for this job?\n~Please input only numbers and currency should be in birr.",
    "amh": "ለዚህ ሥራ የጠየቁት ከፍተኛው ዋጋ ስንት ነው?\n~ እባክዎን ቁጥሮችን ብቻ ያስገቡ እና ምንዛሬ በብር መሆን አለበት፡፡",
}

text_job_is_closed = {
    "eng": "The job has been closed by the employer and does NOT exist anymore.",
    "amh": "ስራው በአሰሪው ተዘግቷል እና ከእንግዲህ አይኖርም።",
}

text_proposal_sent = {
    "eng": "Your proposal has been sent to the employer. good luck!",
    "amh": "ያቀረቡት ሀሳብ ለአሠሪው ተልኳል፡፡ መልካም አድል!",
}

text_proposal_not_sent = {
    "eng": "❌Your proposal can NOT be submited. Either the job is closed or you have already sent a proposal to this job before.",
    "amh": "❌ፕሮፖዛል መላክ አይችሉም፡፡ ወይ ሥራው ተዘግቷል ወይም ደግሞ ከዚህ በፊት ፕሮፖዛል ወደዚህ ሥራ ልከዋል፡፡",
}

text_proposal_full = {
    "eng": "❌Maximum ammount of proposals have been submited to this job.\nThe employer does NOT accept proposals anymore.",
    "amh": "❌ለእዚህ ሥራ ከፍተኛው የፕሮፖዛል መጠን ቀርቧል፡፡\nአሠሪው ከዚህ በኋላ ምንም አይነት ፕሮፖዛል አይቀበልም፡፡",
}

text_proposal_exists = {
    "eng": "❌You have already sent a proposal to the employer.",
    "amh": "❌ቀደም ሲል ለአሰሪው ፕሮፖዛል ልከዋል፡፡",
}

text_press_asign = {
    "eng": "Please, press Assign to assign the job to this freelancer.",
    "amh": "እባክዎን ሥራውን ለዚህ ሰራተኛ ለመመደብ ይመድቡ የሚለውን ይጫኑ፡፡",
}

text_cant_assign = {
    "eng": "❌You can't assign this job to anyone at this time.\n~Check if the job is still opened by using opened jobs section and check if it's already assigned to another freelancer.\n~If that is the case deassign it from that particular freelancer.\n~You can NOT assign a job more than {} times.".format(assign_count),
    "amh": "❌ይህንን ሥራ ለማንም በዚህ ጊዜ መመደብ አይችሉም፡፡\n~የተከፈቱ የሥራ ክፍሎችን በመጠቀም ሥራው አሁንም የተከፈተ መሆኑን ያረጋግጡ ፣ ቀድሞ ለሌላ ሰራተኛ የተመደበ መሆኑን ያረጋግጡ፡፡\n~ያ ከሆነ ሰራተኛውን ከተመደበበት ያውጡት።\n~ አንድ ሥራ ላይ ከ {} ጊዜ በላይ መመደብ አይችሉም።".format(assign_count),
}

text_cant_deassign = {
    "eng": "❌You can't deassign this job from this freelancer.\n~Check if the job is still opened by using opened jobs section and check if it's assigned to this freelancer.",
    "amh": "❌ይህንን ሥራ ከዚህ ባለሙያ ማፈናቀል አይችሉም፡፡\n~የተከፈቱ የሥራ ክፍሎችን በመጠቀም ሥራው አሁንም የተከፈተ መሆኑን ያረጋግጡ እና ለዚህ ሥራ ዪሄ ባለሙያ የተመደበ መሆኑን ያረጋግጡ፡፡",
}

text_escrow_added_freelancer = {
    "eng": "The job has been added to our escrow service and you are protected.\n~You(the freelancer) must keep your word as you have stated on your proposal.\n~You will be paid when the job gets done.\n~For any kind of question please contact one of our admins.",
    "amh": "ስራው የሰራተኛ እና አሰሪ መብት የምንጠብቅበት አገልግሎት ዉስጥ ገብቷል፡፡\n~እርስዎ (ባለሙያው) በፕሮፖዛሎ ላይ እንዳመለከቱት ቃልዎን መጠበቅ አለብዎት፡፡\n~ስራው ሲጠናቀቅ የጠየቁት ክፍያ ይከፈለዎታል፡፡\n~ለማንኛውም ዓይነት ጥያቄ እባክዎ ከአስተዳዳሪዎቹ ውስጥ አንዱን ያነጋግሩ፡፡",
}

text_no_escrow = {
    "eng": "There is no escrow service for this job because you have NOT made any deposit.\n~You can assign and deassign freelancers anytime.\n~Look at opened jobs section for more information on this job.",
    "amh": "ምንም አይነት ገንዘብ ተቀማጭ አላደረጉም፡፡\n~ባለሙያዎችን በማንኛውም ጊዜ መመደብ እና አለመመደብ ይችላሉ፡፡\n~በዚህ ሥራ ላይ የበለጠ መረጃ ለማግኘት የተከፈቱ ሥራዎችን ይመልከቱ፡፡",
}

text_is_in_escrow = {
    "eng": "The job is already in escrow and the freelancer is protected unless he/she hasn't finished the job properly or there exists some disagreement between you and the freelancer.\n~If that is the case please contact the admin.",
    "amh": "ሥራው ቀድሞውኑ escrow ዉስጥ የተቀመጠ ሲሆን ባለሙያው ሥራውን በትክክል ካላጠናቀቁ ወይም በቀጣሪውና እና በባለሙያው መካከል የተወሰነ አለመግባባት ካልተፈጠረ በስተቀር ለባለሙያው ጥበቃ ይደረጋል፡፡\n~ጉዳዩ ቀደም ብሎ የጠቀሰውን ከሆነ ገን እባክዎ አስተዳዳሪውን ያነጋግሩ፡፡",
}

text_must_pay = {
    "eng": "The job is still in escrow and if you continue, You'll make a payment to the freelancer working on this job.\nAre you sure you want to continue?\n~If you are having quarals with the freelancer and want your money back, please press admin, and talk to one of the admins from the admin list.",
    "amh": "ስራው አሁንም escrow ውስጥ የሚገኝ ሲሆን ፣ ከቀጠሉ በዚህ ስራ ላይ ለሚሰራው ባለሙያ ክፍያ ይከፍላሉ፡፡\nለመቀጠል መፈለግዎን እርግጠኛ ነዎት?\n~ከባለሙያው ጋር አለመግባባት ካለዎት እና ገንዘብዎን እንዲመልሱ ከፈለጉ እባክዎን admin ይጫኑ እና ከadmin ዝርዝር ውስጥ አንዱን ያነጋግሩ።",
}

text_job_closed = {
    "eng": "The job has been closed.",
    "amh": "ሥራው ተዘግቷል፡፡",
}

text_job_already_closed = {
    "eng": "❌The job has already been closed.",
    "amh": "❌ሥራው አስቀድሞ ተዘግቷል።",
}

text_nothing_found = {
    "eng": "I can't find anything concerning your request.",
    "amh": "ጥያቄዎን በተመለከተ ምንም ነገር አላገኘሁም፡፡",
}

text_no_jobs_approved = {
    "eng": "There are no jobs to be approved.",
    "amh": "የሚፀድቁ ሥራዎች የሉም፡፡",
}

text_no_admins_found = {
    "eng": "There are no admins found at current time.",
    "amh": "በአሁኑ ሰዓት የተገኙ አስተዳዳሪዎች የሉም፡፡",
}

text_verify_image_req = {
    "eng": "You can edit an already verified company name or verify a new one.\n~Please, send me a photo of your company License.",
    "amh": "ቀድሞውኑ የተረጋገጠ የድርጅት ስም መቀየር ወይም አዲስ ማስገባት ይችላሉ፡፡\n~በመጀመሪያ ፣ እባክዎን የንግድ ፈቃድ ፎቶ ይላኩልኝ፡፡",
}

text_verify_name_req = {
    "eng": "Please, send me the name of your company.",
    "amh": "እባክዎን የድርጅትዎን ስም ይላኩልኝ፡፡",
}

text_verify_submit = {
    "eng": "In order to verify your company profile the admin has to approve your request.\n\nPlease press <i>Edit</i> to edit, or press <i>Submit</i> to submit it.",
    "amh": "የድርጅቶን ስም ለመቀየር አስተዳዳሪው ጥያቄዎን ማፅደቅ አለበት፡፡\n\nእባክዎን ለማስተካከል <i> አስተካክል </i> ን ይጫኑ ወይም ለማስገባት ከፈለጉ <i> አስገባ </i> ን ይጫኑ ፡፡",
}

text_verify_sent = {
    "eng": "Your request has been sent to the admin. good luck!",
    "amh": "ጥያቄዎ ለአስተዳዳሪው ተልኳል፡፡ መልካም አድል!",
}

text_doesnt_exist = {
    "eng": "The data you are looking for does NOT exist on the database anymore.",
    "amh": "የሚፈልጉት መረጃ በመረጃ ቋቱ ላይ አይገኝም።",
}

text_rate_req = {
    "eng": "Please press the Rate button and rate the freelancer out of 10.\n~The freelancer will be rated 5/10 by default.",
    "amh": "እባክዎን ነጥብ ልስጥ የሚለውን ምርጫ ይምረጡና ለባለሙያው ከ 10 ዉጤት ይስጡ።\n~ባለሙያው አሁን 5/10 ተሰቶታል።",
}

text_rate_freelancer = {
    "eng": "Please rate the freelancer out of 10.\n~The freelancer is rated 5 by default and it will be like that if you return to the main menu without giving your rate.",
    "amh": "እባክዎን ለባለሙያው ከ 10 ዉጤት ይስጡ።\n~ባለሙያው አሁን 5/10 ፣ ተሰቶታል ነጥብ ሳይሰጡ ከወጡ እንደዛው ይቀጥላል።",
}

text_rate_between = {
    "eng": "❌Your rate must be between 1 upto 10.\n~Please try again.",
    "amh": "❌ነጥቦ ከ 1 እስከ 10 መሆን አለበት！ እባክዎን እንደገና ይሞክሩ፡፡",
}

text_processing = {
    "eng": "Processing your request...",
    "amh": "ጥያቄዎን በማስኬድ ላይ ነኝ...",
}

text_cashout_sent = {
    "eng": "Your cashout request has been sent to the admin.\nPlease hold on a while until it gets approved.",
    "amh": "የገንዘብ ወጪ ማድረጊያ ጥያቄዎ ለአስተዳዳሪው ተልኳል።\nእስኪፀድቅ ድረስ እባክዎ ትንሽ ይጠብቁ።",
}

text_update_approved = {
    "eng": "Dear freelancer, your level update request has been approved by the admin.",
    "amh": "ውድ ባለሙያ ፣ የደረጃ ማሻሻያ ጥያቄዎ በአስተዳዳሪው ጸድቋል። ",
}

text_update_declined = {
    "eng": "❌Dear freelancer, your level update request has been declined by the admin.\n~Try completing more jobs and increasing your rate.",
    "amh": "❌ውድ ባለሙያ ፣ የደረጃ ማሻሻያ ጥያቄዎ በአስተዳዳሪው ውድቅ ተደርጓል።\n~ብዙ ስራዎችን ለማጠናቀቅ እና ነጥቦን ለመጨመር ይሞክሩ።",
}

text_must_complete_jobs = {
    "eng": "❌You must complete at least one job to ask for level update.",
    "amh": "❌የደረጃ ማሻሻያ ለመጠየቅ ቢያንስ አንድ ሥራ ማጠናቀቅ አለብዎት።",
}

text_update_exists = {
    "eng": "❌You have aleardy sent an update level request.\nPlease wait a while, until the admin to approves that.",
    "amh": "❌አስቀድመው የደረጃ ማሻሻያ ጥያቄ ልከዋል።\nአስተዳዳሪው ያንን እስኪያፀድቅ ድረስ ትንሽ ጊዜ ይጠብቁ።",
}

text_max_update = {
    "eng": "❌You can NOT update your level more than expert.",
    "amh": "❌ደረጃዎን ከዚህ በላይ ማሳደግ አይችሉም።",
}

text_update_sent = {
    "eng": "Your update level request has been sent to the admin. good luck!",
    "amh": "የደረጃ ማሻሻያ ጥያቄዎ ለአስተዳዳሪው ተልኳል። መልካም አድል!",
}

text_max_jobs_opened = {
    "eng": "Dear employer you have opened more than {} jobs and closed none. Please atleast close one to post a new job".format(opened_jobs_count),
    "eng": "ውድ አሠሪ ከ {} በላይ ሥራዎች ከፍተዋል። እባክዎን አዲስ ሥራ ለመለጠፍ አንዱን ይዝጉ".format(opened_jobs_count),
}



# Bot commands text

text_other_commands = {
    "eng": """
<b>verify</b> - to verify company names.
<i>example</i> - verify
<b>ulevel</b> - to approve update level requests.
<i>example</i> - vlevel
<b>show users minimum_jobs</b> - to show users based on how many jobs they posted.
<i>example</i> - show users 1
<b>sid id</b> - to search a user by user id.
<i>example</i> - sid 123456
<b>suser username</b> - to search a user by username.
<i>example</i> - suser abebe123
<b>ban id</b> - to ban a user by user id.
<i>example</i> - ban 123456
<b>unban id</b> - to unban a user by user id.
<i>example</i> - unban 123456
<b>show admins</b> - to show admins.
<i>example</i> - show admins
<b>sjob id</b> - to search a job by job id.
<i>example</i> - sjob 123456

<u>Super admin commands</u>
<b>acash</b> - to approve pending cashouts.
<i>example</i> - acash
<b>dtdec</b> - to change delete [declined jobs] value which deletes a job when it gets declined to true/false.
<i>example</i> - dtdec
<b>chlvl</b> - to change [check level] value which asks the user level at proposal submitting to true/false.
<i>example</i> - chlvl
<b>clesc job_id true/false</b> - to close jobs that are in escrow. the last parameter true or false is to define if the freelancer will be paid(true) or not(false).
<i>example</i> - clesc job_id true
<i>example</i> - clesc job_id false
<b>aadmin id</b> - to add an admin by user id.
<i>example</i> - aadmin 123456
<b>aadmin id true</b> - to add an admin by user id and make it super.
<i>example</i> - aadmin 123456 true
<b>radmin id</b> - to remove an admin from the admin list.
<i>example</i> - radmin 123456
<b>jcoin amount</b> - to update minimum coins needed for posting a job.
<i>example</i> - jcoin 5
<b>pcoin amount</b> - to update minimum coins needed for submitting a proposal.
<i>example</i> - pcoin 4
<b>apfee amount</b> - to update job application fee.
<i>example</i> - apfee 7
<b>mdepo amount</b> - to update minimum deposit amount.
<i>example</i> - mdepo 10
<b>xdepo amount</b> - to update maximum deposit amount.
<i>example</i> - xdepo 4000
<b>mcash amount</b> - to update minimum cashout amount.
<i>example</i> - mcash 20
<b>xcash amount</b> - to update maximum cashout amount.
<i>example</i> - xcash 50
<b>yenec amount</b> - to update yenepay cut if yenepay starts making cuts.
<i>example</i> - yenec 5
<b>merch id</b> - to update merchant id.
<i>example</i> - merch 1234
"""
}



# formatted text

def text_enough_balance(price: int) -> dict:
    text = {
    "eng": "You have enough balance to perform your request and {} birr will be deducted from your account if you wish to continue.\nDo you want to continue?".format(price),
    "amh": "ጥያቄዎን ለመፈፀም በቂ ሂሳብ አለዎት እና ለመቀጠል ከፈለጉ {} ብር ከሂሳብዎ ተቀናሽ ይሆናል።\nመቀጠል ይፈልጋሉ?".format(price),
    }

    return text

def text_help(bot: dict) -> dict:
    text_help = {
        "eng": """You can read the documentations <a href='https://t.me/{}'>here</a>
Ask any questions <a href='https://t.me/{}'>here</a>""".format(bot["s_channel"], bot["s_group"]),
        "amh": """ሰነዶቹን（documentations） <a href='https://t.me/{}'>እዚህ</a> ማንበብ ይችላሉ
ማንኛውንም ጥያቄ ካለዎት <a href='https://t.me/{}'>እዚህ</a> ይጠይቁ""".format(bot["s_channel"], bot["s_group"]),
    }

    return text_help

def text_jobs(status: str) -> dict:
    text = {
        "eng": "You have no {} jobs right now.".format(status),
        "amh": "አሁን ምንም {} ስራዎች የሎትም።".format(status),
    }

    return text

def text_assigned(chat_id: int) -> dict:
    mention_user = mention_html(chat_id, "Freeelancer")
    text = {
        "eng": "The job has been assigned to this {}.\nPress <b>DeAssign</b> to deassign it from this freelancer.\n~Remember you can't assign a job more than {} times.".format(mention_user, assign_count),
        "amh": "ሥራው ለዚህ {} ባለሙያ ተመድቧል።\nሥራውን ከዚህ ባለሙያ ለመንፈግ <b>ከምድብ አውጣ</b> ን ተጫን።\n~ከ {} ጊዜ በላይ ሥራ መመደብ አይችሉም።".format(mention_user, assign_count),
    }

    return text

def text_assigned_deposit(chat_id: int) -> dict:
    mention_user = mention_html(chat_id, "Freeelancer")
    text = {
        "eng": "The job has been assigned to this {}.\n~You can still deassign it from the freelancer before he/she accepts the job.\nPress <b>DeAssign</b> to deassign it from the freelancer.\n~Remember you can't assign a job more than 3 times.".format(mention_user),
        "amh": "ስራው ለዚህ {} ባለሙያ ተመድቧል፡፡\n~ባለሙያው ስራውን ከመቀበሉ በፊት ከምደባው ማውጣት ይችላሉ፡፡\n~ያስታውሱ አንድ ሥራን ከ 3 ጊዜ በላይ መመደብ አይችሉም፡፡".format(mention_user),
    }

    return text

def text_deassigned(chat_id: int) -> dict:
    mention_user = mention_html(chat_id, "Freeelancer")
    text = {
        "eng": "The job has been DeAssigned from this {}.\nPress <b>Assign</b> to assign it to this freelancer again.\n~Remember you can't assign a job more than {} times.".format(mention_user, assign_count),
        "amh": "ስራው ከዚህ {} ባለሙያ ተነፍጓል።\nእንደገና ለዚህ ባለሙያ መመደብ ከፈለጉ <b>መድብ</b> የሚለውን ይጫኑ፡፡\n~ያስታውሱ አንድ ሥራን ከ {} ጊዜ በላይ መመደብ አይችሉም።".format(mention_user, assign_count),
    }

    return text

def text_proposal_assigned(job: dict) -> dict:
    text = {
        "eng": "Your proposal for job title: <b>{}</b>, has been approved.\nPlease press <i>Continue</i> to start working on this job.".format(job["title"]),
        "amh": "ለሥራ ርዕስ <b>{}</b> ያቀረቡት ሀሳብ  ተቀባይነት አግኝቷል።\nእባክዎ በዚህ ሥራ ላይ መሥራት ለመጀመር<i>ቀጥል</i> የሚለውን ቁልፍ ይጫኑ።".format(job["title"]),
    }

    return text

def text_proposal_assigned_no_deposit(job: dict) -> dict:
    text = {
        "eng": "Your proposal for job title: <b>{}</b>, has been approved.\n~There is no esrow service because no deposit was made for the job.".format(job["title"]),
        "amh": "ለሥራ ርዕስ <b>{}</b> ያቀረቡት ሃሳብ ተቀባይነት አግኝቷል።\n~ለሥራው ምንም ተቀማጭ ስላልተደረገ የ escrow አገልግሎት አይኖረውም።".format(job["title"]),
    }

    return text

def text_proposal_deassigned(job: dict) -> dict:
    text = {
        "eng": "Your proposal for job title: <b>{}</b>, has been disapproved.\nPlease stop working on that job.".format(job["title"]),
        "amh": "ለሥራ ርዕስ <b>{}</b> ያቀረቡት ሀሳብ ተቀባይነቱ ውድቅ ተደርጓል።\nእባክዎ በዚያ ሥራ ላይ መሥራትዎን ያቁሙ።".format(job["title"]),
    }

    return text

def text_job_price_req(job: dict) -> dict:
    if job["type"] == "Contractual":
        text = {
        "eng": "How much are you willing to pay, when the job gets done?\n~You can only input numbers!",
        "amh": "ስራው ሲጠናቀቅ ስንት ለመክፈል ፈቃደኛ ነዎት?\n~እባክዎን ቁጥር ብቻ ያስገቡ!",
        }
    elif job["type"] == "Hourly":
        text = {
        "eng": "How much are you willing to pay per hour?\n~You can only input numbers!",
        "amh": "በሰአት ስንት ለመክፈል ፈቃደኛ ነዎት?\n~እባክዎን ቁጥር ብቻ ያስገቡ!",
        }
    else:
        text = {
        "eng": "How much are you willing to pay per month?\n~You can only input numbers!",
        "amh": "በወር ስንት ለመክፈል ፈቃደኛ ነዎት?\n~እባክዎን ቁጥር ብቻ ያስገቡ!",
        }

    return text

def text_money_back_job(data: dict) -> dict:
    text = {
        "eng": "Dear employer, your deposit {} birr for job title: {} has been returned to your account.".format(data["price"], data["title"]),
        "amh": "ውድ አሠሪ ፣ ተቀማጭ ያረጉት ገንዘብ መጠን {} ብር ለሥራ ርዕስ: {} ወደ ተቀማጭ ሂሳብዎ ተመልሷል።".format(data["price"], data["title"]),
    }

    return text

def text_price_above_job(data: dict) -> dict:
    text = {
        "eng": "Dear freelancer, Your fee can not be greater than the job price, which is {} birr.\n~Please try a lower ammount.".format(data["price"]),
        "amh": "ውድ ባለሙያ ፣ እንዲከፈሎ የጠየቁት ብር ከስራ ዋጋ ሊበልጥ አይችልም ፣ ይህም {} ብር ነው።\n~እባክዎ በታችኛው ጥይት ይሞክሩ።".format(data["price"]),
    }

    return text

def text_job_accepted(data: dict) -> dict:
    user_mention = mention_html(data["freelancer"], "freelancer")
    text = {
        "eng": "Dear employer the {} has accepted your job title: {}.\nThe job has been added to the escrow service, and both of you(employer and freelancer) are protected by our escrow service".format(user_mention, data["title"]),
        "amh": "ውድ አሠሪ {} የሥራ ርዕስ {} ተቀብሏል።\nሥራው በ escrow አገልግሎት ላይ ተጨምሯል እናም ሁለታችሁም (አሠሪና ባለሙያ) በ escrow አገልግሎት መብታቹ ይጠበቃል።".format(user_mention, data["title"]),
    }

    return text

def text_payment_freelancer(data: dict) -> dict:
    user_mention = mention_html(data["chat_id"], "Employer")
    text = {
        "eng": "Congradualations dear freelancer, you have got a payment from {}.\n~For job title: {}.\nYour balance have been updated.".format(user_mention, data["title"]),
        "amh": "እንኳን ደስ አሎት ውድ ባለሙያ ፣ ከ {} ክፍያ አግኝተዋል።\nክፍያው የተፈፀመው ለስራ ርዕስ {} ነው።\nተቀማጭ ሂሳቦ ታድሷል።".format(user_mention, data["title"]),
    }

    return text

def text_payment_employer(data: dict) -> dict:
    user_mention = mention_html(data["chat_id"], "Freelancer")
    text = {
        "eng": "You have made a payment of {} birr to this {}.\n~Thank you for using our platform.".format(data["price"], user_mention),
        "amh": "{} ብር ለዚህ {} ባለሙያ ከፍለዋል።\n~እኛን ስለመረጡ እናመሰግናለን።".format(data["price"], user_mention),
    }

    return text

def text_job_coin(data: dict) -> dict:
    text = {
        "eng": "You need {} coin to post a job.\n~If you continue [{}] coin will be deducted from your account as a job posting fee.".format(data["job_coin"], data["job_coin"]),
        "amh": "ሥራ ለመለጠፍ {} coin ያስፈልግዎታል።\n~ከቀጠሉ [{}] coin እንደ ስራ መለጠፊያ ክፍያ ከተቀማጭ ላይ ይቀነሳል።".format(data["job_coin"], data["job_coin"])
    }

    return text

def text_proposal_coin(data: dict) -> dict:
    text = {
        "eng": "You need {} coin to submit a proposal.\n~If you continue [{}] coin will be deducted from your account as an application fee.".format(data["proposal_coin"], data["proposal_coin"]),
        "amh": "ፕሮፖዛል ለማስገባት {} coin ያስፈልግዎታል።\n~ከቀጠሉ [{}] coins እንደ ማመልከቻ ክፍያ ከተቀማጭ ላይ ይቀነሳል።".format(data["proposal_coin"], data["proposal_coin"]),
    }

    return text

def text_deposit_req(data: dict) -> dict:
    text = {
        "eng": "How much money do you wish to deposit?\n~Remember we don't accept a deposit less than {} and more than {} birr.".format(data["minimum_deposit"], data["maximum_deposit"]),
        "amh": "ምን ያህል ገንዘብ ለማስቀመጥ ይፈልጋሉ?\n~ያስታውሱ ከ {} በታች እና ከ {} ብር በላይ አንቀበልም።".format(data["minimum_deposit"], data["maximum_deposit"])
    }

    return text

def text_min_max_deposit(data: dict) -> dict:
    text = {
        "eng": "We do NOT accept deposits less than {} and more than {} birr.".format(data["minimum_deposit"], data["maximum_deposit"]),
        "amh": "ከ {} በታች እና ከ {} ብር በላይ አንቀበልም። እባክዎን  እንደገና ይሞክሩ።".format(data["minimum_deposit"], data["maximum_deposit"]),
    }

    return text

def text_min_max_cashout(data: dict) -> dict:
    text = {
        "eng": "We do NOT accept cashouts less than {} and more than {} birr.".format(data["minimum_cashout"], data["maximum_cashout"]),
        "amh": "ከ {} በታች እና ከ {} ብር በላይ አንቀበልም፡፡ እባክዎን  እንደገና ይሞክሩ።".format(data["minimum_cashout"], data["maximum_cashout"]),
    }

    return text


def text_deposit_link(link: str) -> dict:
    text = {
        "eng": "<b>You need a YenePay account to make a deposit</b>.\nYou can make a deposit by going <a href='{}'>here</a> and completing the payment.\n~As soon as you complete the payment you will recieve a notification and your balance will be updated.".format(link),
        "amh": "<b>ገንዘብ ተቀማጭ ለማድረግ የ YenePay account ያስፈልግዎታል</b>።\n<a href='{}'> እዚህ </a> በመሄድ እና ክፍያውን በማጠናቀቅ ተቀማጭ ማድረግ ይችላሉ።\n~ክፍያውን ካጠናቀቁ ወዲያውኑ ማሳወቂያ ይደርሰዎታል እንዲሁም ሂሳብዎ ይታደሳል።".format(link),
    }

    return text

def text_balance_updated_plus(user: dict, price: int) -> dict:
    text = {
        "eng": "Dear {}, You have made a deposit of {} birr.\n~Your current balance is {} birr.\nThank you for using our platform.".format(user["first_name"], price, user["balance"]),
        "amh": "ውድ {} ፣ {} ብር ተቀማጭ አድርገዋል።\n~አሁን ያሎት ሂሳብ {} ብር ነው።\n እኛን ስለመረጡ እናመሰግናለን።".format(user["first_name"], price, user["balance"]),
    }

    return text

def text_balance_updated_minus(user: dict, price: int) -> dict:
    text = {
        "eng": "Dear {}, You have made a cashout of {} birr.\n~Your current balance is {} birr.\nThank you for using our platform.".format(user["first_name"], price, user["balance"]),
        "amh": "ውድ {} ፣ {} ብር ወጪ አድርገዋል፡፡\n~አሁን ያሎት ሂሳብ {} ብር ነው፡፡\nእኛን ስለመረጡ እናመሰግናለን፡፡".format(user["first_name"], price, user["balance"]),
    }

    return text

def text_cashout_req(data: dict) -> dict:
    text = {
        "eng": "How much money do you wish to cashout?\n~Remember we don't accept a cashout less than {} and more than {} birr.".format(data["minimum_cashout"], data["maximum_cashout"]),
        "amh": "ምን ያህል ገንዘብ ለማውጣት ይፈልጋሉ?\n~ያስታውሱ ወጪ የሚያረጉት ገንዘብ ከ {} በላይ እና ከ {} ብር በታች መሆን አለበት።".format(data["minimum_cashout"], data["maximum_cashout"]),
    }

    return text

def text_cashout(user: dict, price: int) -> dict:
    text = {
        "eng": "Are you sure you want to cashout {} birr from your account?\n<b>Remember the admin will use your phone number <i>+{}</i> to send the payment via yenepay</b>, If your yenepay account is not connected with this phone number please cancel the cashout request and contact the admins.\n~The admin will process the payment and notify you shortly.\n~Please press the Submit button if you want to continue.".format(price, user["phone_number"]),
        "amh": "እርግጠኛ ነዎት ከተቀማጭ ሂሳቦ ውስጥ {} ብር ማውጣት ይፈልጋሉ?\n<b>አስተዳዳሪው ክፍያውን በ yenepay በኩል ለመላክ የስልክ ቁጥርዎን <i>+{}</i> እንደሚጠቀም ያስታውሱ </b>, የ yenepay አካውንት ከዚህ የስልክ ቁጥር ጋር ካልተያያዘ እባክዎን የገንዘብ ወጪ ጥያቄውን ይሰርዙ እና አስተዳዳሪዎቹን ያነጋግሩ።\n~አስተዳዳሪው ክፍያውን ያካሂድና በቅርቡ ያሳውቅዎታል።\n~ለመቀጠል ከፈለጉ እባክዎን አስገባ የሚለውን ቁልፍ ይጫኑ።".format(price, user["phone_number"]),
    }

    return text

def text_cashout_approved(cashout: dict) -> dict:
    text = {
        "eng": "✅Your cashout request with ID: {} and birr {} has been approved.\nThe admin made a payment to your yenepay account linked with your phone number.\n~Please contact one of our admins if you are having troubles.\n~Thank you for using our platform".format(cashout["cashout_id"], cashout["price"]),
        "amh": "✅የገንዘብ ወጪ ጥያቄዎ በ ID: {} እና ብር {} ፀድቋል።\nአስተዳዳሪው ከስልክ ቁጥርዎ ጋር ለተያያዘው yenepay የክፍያ ሂሳብዎ ክፍያ ፈፅሟል። እኛን ስለመረጡ እናመሰግናለን".format(cashout["cashout_id"], cashout["price"]),
    }

    return text

def text_cashout_declined(cashout: dict) -> dict:
    text = {
        "eng": "❌Your cashout request with ID: {} and birr {} has been declined.\nThe admin returned your money to your deposit.\n~Please contact one of our admins if you are having troubles.\n~Thank you for using our platform".format(cashout["cashout_id"], cashout["price"]),
        "amh": "❌የገንዘብ ወጪ ጥያቄዎ  በ ID: {} እና ብር {} ውድቅ ተደርጓል፡፡\nአስተዳዳሪው ወጪ ያረጉትን ገንዘብ ወደ ተቀማጭ ሂሳቦ መልሶታል፡፡".format(cashout["cashout_id"], cashout["price"]),
}

    return text

def text_rate_notification(employer_id: int, rate: int) -> dict:
    user_mention = mention_html(employer_id, "employer")
    text = {
        "eng": "Dear freelancer you have been rated {} by this {}.\nThank you for using our platform.".format(rate, user_mention),
        "amh": "ውድ ባለሙያ {} ውጤት በዚህ {} ተሰጥቶዎታል ፡፡ \ n የእኛን መድረክ ስለተጠቀሙ እናመሰግናለን፡፡".format(rate, user_mention),
}

    return text

def text_job_closed_no_deposit(job: dict) -> dict:
    text = {
        "eng": "Dear freelancer the job ID: <b>{}</b>, and title: <b>{}</b> has been closed by the employer.\nPlease stop working on it if you are still working.".format(job["job_id"], job["title"]),
        "amh": "ውድ ባለሙያ የሥራ መታወቂያ: <b>{}</b> እና አርእስት <b>{}</b> በአሠሪው ተዘግቷል፡፡\nአሁንም በእሱ ላይ እየሠሩ ከሆነ እባክዎን መስራቱን ያቁሙ፡፡".format(job["job_id"], job["title"]),
 }

    return text

def text_job_declined(job: dict) -> dict:
    text = {
        "eng": "❌Dear employer, the job ID: <b>{}</b>, and title: <b>{}</b> has been declined by the admin.".format(job["job_id"], job["title"]),
        "amh": "❌ውድ አሠሪ ፣ የሥራ መታወቂያ: <b> {} </b> እና አርእስት <b>{}</b> ፣ በአስተዳዳሪው ውድቅ ተደርጓል፡፡".format(job["job_id"], job["title"]),
}

    return text

def text_job_approved(job: dict) -> dict:
    text = {
        "eng": "✅Dear employer, the job ID: <b>{}</b>, and title: <b>{}</b> has been approved by the admin.".format(job["job_id"], job["title"]),
        "amh": "✅ውድ አሠሪ የሥራ መታወቂያ: <b>{}</b> እና አርእስት <b>{}</b> በአስተዳዳሪው ጸድቋል፡፡".format(job["job_id"], job["title"]),
 }

    return text

def text_verify_declined(verify: dict) -> dict:
    text = {
        "eng": "❌Dear employer, your company verification request with company name: <b>{}</b> has been declined by the admin.".format(verify["company"]),
        "amh": "❌ውድ አሠሪ ፣ የኩባንያዎ የማረጋገጫ ጥያቄ በኩባንያው ስም <b>{}</b> ፣ በአስተዳዳሪው ውድቅ ተደርጓል፡፡".format(verify["company"]),
   }

    return text

def text_verify_approved(verify: dict) -> dict:
    text = {
        "eng": "✅Dear employer, your company verification request with company name: <b>{}</b> has been approved by the admin.".format(verify["company"]),
        "amh": "✅ውድ አሠሪ ፣ የኩባንያዎ ማረጋገጫ ጥያቄ በኩባንያው ስም <b>{}</b> ፣ በአስተዳዳሪው ፀድቋል፡፡".format(verify["company"]),
    }

    return text