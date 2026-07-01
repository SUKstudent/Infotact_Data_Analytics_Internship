import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df=pd.read_csv("/content/multi_touch_attribution_dataset_cleaned.csv")

total_spend = df['ad_spend'].sum()
total_revenue = df['conversion_value'].sum()

print("Total Spend:", round(total_spend))
print("Total Revenue:", round(total_revenue))

roas = total_revenue / total_spend
print("ROAS:", round(roas))

attributed_revenue = df["conversion_value"].sum()
print(round(attributed_revenue))

total_customers = df[df['is_conversion'] == 1]['user_id'].nunique()

cac = total_spend / total_customers#Customer Acquisition Cost
print("CAC:",round(cac,2))
total_regions = df['region'].nunique()
print(total_regions)

total_count = df['total_touchpoints_in_journey'].count()
print("Total Count:", total_count)
print("Average Touch Points :",round(total_touchpoints/total_count,1))

first_touch = df[df['touchpoint_number'] == 1]
print("First Touch Records:", len(first_touch))
print(first_touch['channel'].value_counts())

last_touch = df[df['touchpoint_number'] == df['total_touchpoints_in_journey']]
print("Last Touch Records:", len(last_touch))
print(last_touch['channel'].value_counts())

df['linear_credit'] = df['conversion_value'] / df['total_touchpoints_in_journey']
print(df[['journey_id', 'channel', 'linear_credit']].head())
