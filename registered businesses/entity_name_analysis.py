import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string

data = pd.read_csv('EntitiesRegisteredwithACRA.csv')

#extract the first letter of each entity name and convert to uppercase
data['first_letter'] = data['entity_name'].apply(lambda x: x[0].upper() if isinstance(x, str) and len(x) > 0 else None)
letter_counts = data['first_letter'].value_counts().sort_index()
alphabet_counts = letter_counts[letter_counts.index.isin(list(string.ascii_uppercase))]

plt.figure(figsize=(14, 8))
bars = plt.bar(alphabet_counts.index, alphabet_counts.values, color=plt.cm.viridis(alphabet_counts.values/max(alphabet_counts.values)))

#labels above each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height}', ha='center', va='bottom')

plt.title('Distribution of First Letters in Business Entity Names', fontsize=16)
plt.xlabel('First Letter', fontsize=12)
plt.ylabel('Number of Entities', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

#horizontal line for the average count
avg_count = alphabet_counts.mean()
plt.axhline(y=avg_count, color='r', linestyle='--', alpha=0.7)
plt.text(0, avg_count + 0.5, f'Average: {avg_count:.1f}', color='r')
plt.tight_layout()
plt.savefig('entity_name_analysis.png')

#pie chart with top 13 most frequent letters and "Others"
alphabet_letters = letter_counts[letter_counts.index.isin(list(string.ascii_uppercase))]
top_13_letters = alphabet_letters.sort_values(ascending=False).head(13)
other_count = alphabet_letters.sum() - top_13_letters.sum()
#combine top letters and "Others" category
pie_data = top_13_letters.copy()
pie_data['Others'] = other_count

plt.figure(figsize=(10, 10))
plt.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%', 
        startangle=90, shadow=True, 
        explode=[0.05] * 13 + [0.1],  #slightly more explode for "Others"
        colors=plt.cm.Set3(range(len(pie_data))))
plt.axis('equal')
plt.title('Top 13 First Letters in Business Entity Names', fontsize=16)
plt.savefig('entity_name_top_letters.png')

plt.show()

print("Analysis complete. Visualizations saved as 'entity_name_analysis.png' and 'entity_name_top_letters.png'") 