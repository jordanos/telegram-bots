

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

