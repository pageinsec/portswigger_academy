# Put passwords in quotes to paste into Burp
import pandas as pd
import json
new_passwords = []
passwords = pd.read_csv('./burp_pass.csv')
count = 1
for pw in passwords:
    new_passwords.append(pw)

#print(new_passwords)
print(json.dumps(new_passwords))
        


#f = pd.DataFrame(new_passwords,columns=["column"])
#f.to_csv('./quote_password.csv', index=False)
# Remove "column" from csv (or 0 if leave columns blank)