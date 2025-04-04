import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('EntitiesRegisteredwithACRA.csv')

# Convert postal_code to string and group by postal code and registration status
data['reg_postal_code'] = data['reg_postal_code'].astype(str)
postal_status = data.groupby(['reg_postal_code', 'uen_status_desc']).size().unstack(fill_value=0)

#top 15 postal codes with the most businesses
if len(postal_status) > 15:
    total_businesses = postal_status.sum(axis=1)
    top_postal_codes = total_businesses.sort_values(ascending=False).head(15).index
    postal_status = postal_status.loc[top_postal_codes]

plt.figure(figsize=(12, 8))
postal_status.plot(kind='bar', stacked=True, color=['#ff9999', '#66b3ff'], ax=plt.gca())

plt.title('Registered vs Deregistered Businesses by Postal Code', fontsize=16)
plt.xlabel('Postal Code', fontsize=12)
plt.ylabel('Number of Businesses', fontsize=12)
plt.legend(title='Registration Status')
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('postal_code_analysis.png')
plt.close()

print("Analysis complete. Visualization saved as 'postal_code_analysis.png'") 