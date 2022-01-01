import base64
import hashlib
import pandas as pd

password_list = []
data = pd.read_csv('./burp_pass.csv')
for passw in data:
    password_list.append(passw)

md5_list = []
for pw in password_list:
    string = pw
    result = hashlib.md5(string.encode())
    #print(result.hexdigest())
    md5_list.append(result.hexdigest())

for i in md5_list:
    message = 'carlos:'+i
    print(message)
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')
    print(base64_message)
