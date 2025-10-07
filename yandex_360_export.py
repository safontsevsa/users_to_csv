from dotenv import load_dotenv
import os
import requests
import csv
import random
import string

load_dotenv()

TOKEN = os.getenv("TOKEN")
ORG_ID = os.getenv("ORG_ID")
OUT_CSV = 'users_migration.csv'

def random_password(length=8):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def y360_req(url, token, params=None):
    headers = {
        'Authorization': f'OAuth {token}',
        'Accept': 'application/json',
    }
    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    return r.json()

def translit_gender(g):
    if g == "male":
        return "male"
    elif g == "female":
        return "female"
    return ""

def main():
    users = []
    next_page_token = None
    base_url = f"https://api360.yandex.net/directory/v1/org/{ORG_ID}/users"
    while True:
        params = {'page_token': next_page_token} if next_page_token else {}
        resp = y360_req(base_url, TOKEN, params)
        users.extend(resp['users'])
        next_page_token = resp.get('next_page_token')
        if not next_page_token:
            break

    fieldnames = [
        'login','password','password_change_required','first_name','last_name','middle_name','position',
        'gender','birthday','language','phone',
    ]
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()

        for user in users:
            login = user['nickname'].lower()
            password = random_password(8)
            password_change_required = 'true'
            first_name = user['name'].get('first', '')
            last_name = user['name'].get('last', '')
            middle_name = user['name'].get('middle', '')
            position = user.get('position', '')
            gender = translit_gender(user.get('gender', ''))

            birthday = user.get('birthday', '')
            if birthday and '-' in birthday:
                parts = birthday.split('-')
                if len(parts) == 3:
                    birthday = f"{parts[2]}.{parts[1]}.{parts[0]}"

            language = user.get('language', 'ru')
            phone = ''
            for c in user.get('contacts', []):
                if c.get('type') == 'phone':
                    phone = c.get('value', '').replace('+','').replace('-','').replace(' ','')
                    break

            row = {
                'login': login,
                'password': password,
                'password_change_required': password_change_required,
                'first_name': first_name,
                'last_name': last_name,
                'middle_name': middle_name,
                'position': position,
                'gender': gender,
                'birthday': birthday,
                'language': language,
                'phone': phone,
            }
            writer.writerow(row)
            print(f"✓ {login}")

if __name__ == '__main__':
    main()