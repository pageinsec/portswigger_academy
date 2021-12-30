# Intersperse passwords to avoid lockouts
import pandas as pd

new_passwords = []
passwords = pd.read_csv('./burp_pass.csv')
count = 1
for pw in passwords:
    # Set % number to 1 less than where IP block kicks in
    if count % 2 != 0:
        new_passwords.append(pw)
    else:
        new_passwords.append(pw)
        new_passwords.append('peter')
    count += 1

f = pd.DataFrame(new_passwords,columns=["column"])
f.to_csv('./combined_password.csv', index=False)
# Remove "column" from csv (or 0 if leave columns blank)