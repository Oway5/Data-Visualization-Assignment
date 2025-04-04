import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('EntitiesRegisteredwithACRA.csv')

#group by street name and count registrations by status
street_status = data.groupby(['reg_street_name', 'uen_status_desc']).size().unstack(fill_value=0)

#top 15 streets with the most businesses
if len(street_status) > 15:
    total_businesses = street_status.sum(axis=1)
    top_streets = total_businesses.sort_values(ascending=False).head(15).index
    street_status = street_status.loc[top_streets]

plt.figure(figsize=(14, 10))
street_status.plot(kind='barh', stacked=True, color=['#ff9999', '#66b3ff'], ax=plt.gca())

plt.title('Registered vs Deregistered Businesses by Street Name', fontsize=16)
plt.xlabel('Number of Businesses', fontsize=12)
plt.ylabel('Street Name', fontsize=12)
plt.legend(title='Registration Status')
plt.tight_layout()

plt.savefig('street_name_analysis.png')
plt.close()

print("Analysis complete. Visualization saved as 'street_name_analysis.png'") 