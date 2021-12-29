# Interspese known users to avoid lockouts
import pandas as pd
import csv

users_known = []
count = 1
for user in range(1,200):
    if count % 2 != 0:
        users_known.append('carlos')
    else:
        users_known.append('carlos')
        users_known.append('wiener')
    count += 1

f = pd.DataFrame(users_known, columns=["column"])
f.to_csv('./split_users.csv', index=False)
# Remove "column" from csv (or 0 if leave columns blank)