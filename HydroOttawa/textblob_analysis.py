import pandas as pd 

df = pd.read_csv("HydroOttawaAnnotatedData.csv") 
df['PatternAnalyzerSentiment'] = 0
print(df)

