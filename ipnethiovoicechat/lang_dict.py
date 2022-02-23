from config import *

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