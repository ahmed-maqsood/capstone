import pandas as pd

array = {'Name': ['oof'], 'age': [5]}
df = pd.DataFrame(array)

with open('test.csv', 'a') as log:
    df.to_csv(log, index=False)