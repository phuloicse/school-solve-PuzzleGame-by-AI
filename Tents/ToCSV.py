import pandas as pd
df = pd.read_json (r'.\data.json')
df.to_csv (r'.\New.csv', index = None)