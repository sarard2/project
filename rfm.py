import pandas as pd
import matplotlib as plt
df=pd.read_csv("transactions.csv")
sales=df[(df['InvoiceType']=="Sales")]
"""# RFM Clustering Using Kmeans"""
#In order to perform customer segmentation, the Invoice Types which are sales are only of interest
#Thus, only sales dataframe is considered.
#A new dataframe which highlight the unique clients is created
rfm_df = pd.DataFrame(sales['Client'].unique())
rfm_df.columns = ['Client']

"""## Recency"""

#Need to find out most recent purchase date of each customer and see how many days they are inactive for (When did they last have a transaction?)
date_df = sales.groupby('Client').TransDate.max().reset_index()
date_df.columns = ['Client','MaxDate']
date_df['MaxDate'] = pd.to_datetime(date_df['MaxDate'])

#The observation point is the max invoice date in the dataset in order to correspond to most recent date
date_df['Recency'] = (date_df['MaxDate'].max() - date_df['MaxDate']).dt.days

#The date dataframe is then merged with the unique clients dataframe through clients.
rfm_df1 = pd.merge(rfm_df,date_df[["Client","Recency"]],on='Client',how="inner")

"""## Frequency"""

#The frequency per customer depends on the number of times the customer purchased from us
freq_df = sales.groupby('Client').TransDate.count().reset_index()
freq_df.columns = ['Client','Frequency']

#The frequency dataframe is then merged with the unique clients dataframe through clients.
rfm_df2= pd.merge(rfm_df1, freq_df, on='Client',how="inner")

"""## Monetary"""

#Need to calculate revenue for each customer in order to know the monetary score of each customer
rev_df = sales.groupby('Client').Revenue.sum().reset_index()

#The revenue dataframe is then merged with the unique clients dataframe through clients.
rfm_df3= pd.merge(rfm_df2, rev_df, on='Client',how="inner")

#As the three previous merges caused reoccuring columns, only columns of importance are selected to create the final rfm dataframe which shows each client with corresponding scores
rfm=rfm_df3[["Client","Recency","Frequency","Revenue"]]
rfm

"""## Analysis"""

#As each client now has score based on recency, frequency and monetary, Clients are grouped based on similarities in these scores

#Importing needed libary for this sections
from sklearn.cluster import KMeans

#As line chart above becomes stable on k=3, should build 3 clusters for recency and add it to dataframe
kmeans = KMeans(n_clusters=3)
kmeans.fit(rfm[['Recency']])
rfm['RecencyCluster'] = kmeans.predict(rfm[['Recency']])

#The following function is used to order the cluster numbers
def ordering(cluster_field_name, target_field_name,df,ascending):
    new_cluster_field_name = 'new_' + cluster_field_name
    df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
    df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
    df_new['index'] = df_new.index
    df_final = pd.merge(df,df_new[[cluster_field_name,'index']], on=cluster_field_name)
    df_final = df_final.drop([cluster_field_name],axis=1)
    df_final = df_final.rename(columns={"index":cluster_field_name})
    return df_final

rfm = ordering('RecencyCluster','Recency',rfm,False)

#Doing Kmeans for Frequency
kmeans = KMeans(n_clusters=3)
kmeans.fit(rfm[['Frequency']])
rfm['FrequencyCluster'] = kmeans.predict(rfm[['Frequency']])

#Need to order the frequency cluster numbers
rfm = ordering('FrequencyCluster', 'Frequency',rfm,True)

#Doing Kmeans for Revenue
kmeans = KMeans(n_clusters=3)
kmeans.fit(rfm[['Revenue']])
rfm['RevenueCluster'] = kmeans.predict(rfm[['Revenue']])

#Need to order the revenue cluster numbers
rfm = ordering('RevenueCluster', 'Revenue',rfm,True)

#Need to calculate overall RFM score and see the mean to know the details
rfm['OverallScore'] = rfm['RecencyCluster'] + rfm['FrequencyCluster'] + rfm['RevenueCluster']
rfm.groupby('OverallScore')['Recency','Frequency','Revenue'].mean()

#According to the RFM score, each customer is placed in a certain category and should be treated accordingly
rfm['Segment'] = 'Low-Value'
rfm.loc[rfm['OverallScore']>2,'Segment'] = 'Mid-Value'
rfm.loc[rfm['OverallScore']>4,'Segment'] = 'High-Value'

#Moving it into pickle file to be used in streamlit
import pickle
file = open(r"C:\Users\Sara\Desktop\rfm.pkl", "wb")
pickle.dump(rfm , file)
file.close()
model = open("rfm.pkl", "rb")
forest = pickle.load(model)
