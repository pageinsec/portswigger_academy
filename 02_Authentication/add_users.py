# Intersperse user list with known good user to avoid lockouts
import pandas as pd
import csv

new_users = []
users = pd.read_csv('./burp_users.csv')
count = 1
for user in users:
    # Set % number to 1 less than where IP block kicks in
    if count % 2 != 0:
        
        new_users.append(user)
    
    else:
        new_users.append(user)
        new_users.append('wiener')
    count += 1

f = pd.DataFrame(new_users, columns=["column"])
f.to_csv('./combined_users.csv', index=False)
# Remove "column" from csv (or 0 if leave columns blank)
