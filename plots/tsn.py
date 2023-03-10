"""
Grouped violinplots with split violins
======================================

_thumb: .44, .47
"""
import sys
import seaborn as sns
import pandas as pd 

e=sys.exit
sns.set_theme(style="whitegrid")

# Load the example tips dataset
#tips = sns.load_dataset("tips")
tips = pd.read_csv('tips.csv')

#print(tips)

# Draw a nested violinplot and split the violins for easier comparison
sns.violinplot(data=tips, x="day", y="total_bill", hue="smoker",
               split=True, inner="quart", linewidth=1,
               palette={"Yes": "b", "No": ".85"})
sns.despine(left=True)