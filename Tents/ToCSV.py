import pandas as pd
df = pd.read_json (r'.\a_star_tents_data.json')
df.to_csv (r'.\a_star.csv', index = None)
df = pd.read_json (r'.\dfs_tents_data.json')
df.to_csv (r'.\dfs.csv', index = None)