"""# Market Basket Analysis Using Apriori

## Apriori
"""
import pandas as pd
import pickle
import matplotlib as plt
df=pd.read_csv("transactions.csv")
sales=df[(df['InvoiceType']=="Sales")]
#Loading needed libraries for this section
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
#saless=sales.sample(frac=0.10)

#Need to create my basket dataframe which shows products in the following format, it will return 0 if product is not in the Invoice, and a number representing quantity if included
mybasket = (sales.groupby(['InvoiceID', 'Item'])['Quantity']
          .sum().unstack().reset_index().fillna(0)
          .set_index('InvoiceID'))

#Need to convert all positive values to 1 and all other to 0 as the quantity is not important over here
#What is important is the presence/absence of product in the Invoice
def my_encode_units(x):
    if x <= 0:
        return 0
    if x >= 1:
        return 1

my_basket_sets = mybasket.applymap(my_encode_units)

#As apriori doesn't accept any missing values, need to double check through dropping any missing values
my_basket_sets.dropna(0,inplace=True)
#Inspect the basket dataframe
my_basket_sets

#Need to generate frequent itemsets
my_frequent_itemsets = apriori(my_basket_sets, min_support=0.005, use_colnames=True).sort_values('support',ascending=False).reset_index(drop=True)
my_frequent_itemsets['length']=my_frequent_itemsets['itemsets'].apply(lambda x: len(x))
my_frequent_itemsets

"""## Association Rules"""

#Need to apply association rules
assoc_rules = association_rules(my_frequent_itemsets, metric="lift", min_threshold=1).sort_values("lift",ascending=False).reset_index(drop=True)
assoc_rules["consequent_length"]=assoc_rules['consequents'].apply(lambda x: len(x))

#Only rules were the consequent is of length are accepted
assoc_rules_new=assoc_rules[assoc_rules["consequent_length"]<=1]
assoc_rules_new.reset_index(inplace=True)

rules=assoc_rules_new[["antecedents","consequents","support","confidence","lift"]]
rules

#Moving it into pickle file to be used in streamlit
import pickle
file = open(r"C:\Users\Sara\Desktop\arm.pkl", "wb")
pickle.dump(rules , file)
file.close()
model = open("arm.pkl", "rb")
forest = pickle.load(model)
