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
