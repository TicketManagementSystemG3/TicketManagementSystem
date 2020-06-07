import random
import string
import re


def generate_password(len=6):
    string_char = string.ascii_letters+string.digits+"@#$"
    res = "".join(random.choice(string_char) for i in range(len)) + random.choice(string.ascii_letters) + random.choice(string.digits)+random.choice("@#$")
    res_list = list(res)
    random.shuffle(res_list)
    return "".join(res_list)

def extract_username(email): 
    email4 = re.compile(r'[\w.]+')
    match = email4.match(email)
    return match.group()   