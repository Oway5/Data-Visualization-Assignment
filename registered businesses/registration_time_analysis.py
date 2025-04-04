import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('EntitiesRegisteredwithACRA.csv')

#date and year
data['uen_issue_date'] = pd.to_datetime(data['uen_issue_date'])
data['issue_year'] = data['uen_issue_date'].dt.year

#group by year and count registrations
yearly_counts = data.groupby(['issue_year', 'uen_status_desc']).size().unstack(fill_value=0)

#line chart
plt.figure(figsize=(14, 8))
ax = yearly_counts.plot(kind='line', marker='o', linewidth=2, ax=plt.gca())

#data labels to the end points
for column in yearly_counts.columns:
    last_valid_idx = yearly_counts[column].last_valid_index()
    if last_valid_idx:
        plt.annotate(f'{yearly_counts[column].loc[last_valid_idx]}',
                    xy=(last_valid_idx, yearly_counts[column].loc[last_valid_idx]),
                    xytext=(5, 0), textcoords='offset points')

plt.title('Business Registrations Over Time', fontsize=16)
plt.xlabel('Year', fontsize=12)
plt.ylabel('Number of Businesses', fontsize=12)
plt.legend(title='Registration Status')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig('registration_time_line.png')
plt.show()

print("Analysis complete. Visualization saved as 'registration_time_line.png'") 