import pandas as pd
import streamlit as st

import numpy
from streamlit_option_menu import option_menu
#from st_aggrid import AgGrid
import plotly
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
import matplotlib as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error

#Setting page width to wide
st.set_page_config(layout="wide")

#Loading Data
df=pd.read_csv(r"transactions.csv")
sales=df[df["InvoiceType"]=="Sales"]
purhases=df[df["InvoiceType"]=="Purchase"]
returnsales=df[df["InvoiceType"]=="Return Sales"]



#This is to hide the above white banner appearing
st.markdown("""
<style>
    #MainMenu, header, footer {visibility: hidden;}
    /* This code gets the first element on the sidebar,
    and overrides its default styling */
    section[data-testid="stSidebar"] div:first-child {
        top: 0;
        height: 100vh;
    }
</style>
""",unsafe_allow_html=True)

#st.markdown("""
#<div class="alert alert-secondary" role="alert">
#</div>
#""",unsafe_allow_html=True)

#This is to show the upper banner with links
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #1F628E;">
  <a class="navbar-brand" href="https://www.aub.edu.lb/osb/MSBA/Pages/default.aspx" target="_blank">Capstone Project</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="https://invis.io/VZ12GD1UDFTG" target="_blank">My Portfolio</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.linkedin.com/in/sara-ramadan/" target="_blank">Contact Me</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

#Setting Default Theme for plotly graphs
pio.templates.default = "simple_white"


#Sidebar Menu
col1,col2,col3=st.columns([1,3,1])
with col1:
    st.markdown("""<hr style="height:3px;border:none;color:#00ced1;background-color:#1F628E;" /> """, unsafe_allow_html=True)
with col2:
    selected = option_menu(None, ["Overview","RFM","ARM","Prediction"],
    icons=['house', 'cloud-upload', "list-task", 'gear'],
    menu_icon="cast", default_index=0,orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#33CCCC"},
        "icon": {"color": "white", "font-size": "15px"},
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#1F628E"},
    })
with col3:
    st.markdown("""<hr style="height:3px;border:none;color:#00ced1;background-color:#1F628E;" /> """, unsafe_allow_html=True)


#Overview page
if selected=="Overview":
    
    #df_sample=df.sample(frac=0.2)
    #st.dataframe(df)
    #AgGrid(df_sample)
    col1,col2=st.columns(2)
    with col1:
        st.write("Project Overview")
    with st.expander("Have a look at the dataset format!"):
         st.dataframe(df)




#RFM page
if selected=="RFM":

    #In order to perform customer segmentation, the Invoice Types which are sales are only of interest
    #Thus, only sales dataframe is considered.

    #A new dataframe which highlight the unique clients is created
    rfm_df = pd.DataFrame(sales['Client'].unique())
    rfm_df.columns = ['Client']
    #Need to find out most recent purchase date of each customer and see how many days they are inactive for (When did they last have a transaction?)
    date_df = sales.groupby('Client').TransDate.max().reset_index()
    date_df.columns = ['Client','MaxDate']
    date_df['MaxDate'] = pd.to_datetime(date_df['MaxDate'])

    #The observation point is the max invoice date in the dataset in order to correspond to most recent date
    date_df['Recency'] = (date_df['MaxDate'].max() - date_df['MaxDate']).dt.days

    #The date dataframe is then merged with the unique clients dataframe through clients.
    rfm_df1 = pd.merge(rfm_df,date_df[["Client","Recency"]],on='Client',how="inner")


    #The frequency per customer depends on the number of times the customer purchased from us
    freq_df = sales.groupby('Client').TransDate.count().reset_index()
    freq_df.columns = ['Client','Frequency']

    #The frequency dataframe is then merged with the unique clients dataframe through clients.
    rfm_df2= pd.merge(rfm_df1, freq_df, on='Client',how="inner")


    #Need to calculate revenue for each customer in order to know the monetary score of each customer
    rev_df = sales.groupby('Client').Revenue.sum().reset_index()

    #The revenue dataframe is then merged with the unique clients dataframe through clients.
    rfm_df3= pd.merge(rfm_df2, rev_df, on='Client',how="inner")

    #As the three previous merges caused reoccuring columns, only columns of importance are selected to create the final rfm dataframe which shows each client with corresponding scores
    rfm=rfm_df3[["Client","Recency","Frequency","Revenue"]]

    #As each client now has score based on recency, frequency and monetary, Clients are grouped based on similarities in these scores

    #Importing needed libary for this sections
    from sklearn.cluster import KMeans

    #K means for recency to find similar clients in this aspect
    sse={}
    recency = rfm[['Recency']]

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


    col1,col2,col3=st.columns(3)
    with col1:
        st.markdown(""" 
        <div class="card text-bg-light mb-3" style="max-width: 18rem;">
          <div class="card-header">Recency</div>
          <div class="card-body">
            <h5 class="card-title">Light card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          </div>
         </div>  """,unsafe_allow_html=True)
    with col2:
        st.markdown(""" 
        <div class="card text-bg-light mb-3" style="max-width: 18rem;">
          <div class="card-header">Frequency</div>
          <div class="card-body">
            <h5 class="card-title">Light card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          </div>
         </div>  """,unsafe_allow_html=True)
    
    with col3:
        st.markdown(""" 
        <div class="card text-bg-light mb-3" style="max-width: 18rem;">
          <div class="card-header">Monetary</div>
          <div class="card-body">
            <h5 class="card-title">Light card title</h5>
            <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          </div>
         </div>  """,unsafe_allow_html=True)
        
    col1,col2=st.columns(2)
    with col1:
        #st.markdown("""<hr style="height:3px;border:none;color:#00ced1;background-color:#1F628E;" /> """, unsafe_allow_html=True)
        #st.dataframe(selectedclient)
        client1=df["Client"].unique().tolist()
        client_select=st.multiselect("Which customer are you interested in reviewing?",client1,"Tyrone Wright")
        selectedclient=rfm[rfm["Client"].isin(client_select)]
        segments=selectedclient["Segment"].values[0]
        st.write("The client you have selected is",segments)

        recency_value=selectedclient["Recency"]
        st.metric(label="Recency", value=recency_value)

        freq_value=selectedclient["Frequency"]
        st.metric(label="Frequency", value=freq_value)

        monetary_value=selectedclient["Revenue"]
        st.metric(label="Revenue", value=monetary_value)

        overall_value=selectedclient["OverallScore"]
        st.metric(label="Overall Score", value=overall_value)
    with col2:
        #Second customer
        client2=df["Client"].unique().tolist()
        client_select2=st.multiselect("Which customer are ?",client2,"Peter Smith")
        selectedclient2=rfm[rfm["Client"].isin(client_select2)]
        segments2=selectedclient2["Segment"].values[0]
        st.write("The client you have selected is",segments2)

        recency_value2=selectedclient2["Recency"]
        st.metric(label="Recency", value=recency_value2)

        freq_value2=selectedclient2["Frequency"]
        st.metric(label="Frequency", value=freq_value2)

        monetary_value2=selectedclient2["Revenue"]
        st.metric(label="Revenue", value=monetary_value2)

        overall_value2=selectedclient2["OverallScore"]
        st.metric(label="Overall Score", value=overall_value2)


    clientsales=sales[sales["Client"].isin(client_select)]
    clientsales2=sales[sales["Client"].isin(client_select2)]
    grouped_sales= clientsales.groupby('TransDate').Revenue.sum().reset_index()
    grouped_sales2= clientsales2.groupby('TransDate').Revenue.sum().reset_index()
    figure=px.line(grouped_sales,x="TransDate",y="Revenue")
    #figure.add_scatter(x=grouped_sales2["TransDate"],y=grouped_sales2["Revenue"])
    st.plotly_chart(figure)
    figure1=px.line(grouped_sales2,x="TransDate",y="Revenue")
    #figure.add_scatter(x=grouped_sales2["TransDate"],y=grouped_sales2["Revenue"])
    st.plotly_chart(figure1)





#ARM page
if selected=="ARM": 
    #Loading needed libraries for this section
    from mlxtend.frequent_patterns import apriori
    from mlxtend.frequent_patterns import association_rules
    #Need to create my basket dataframe which shows products in the following format, it will return 0 if product is not in the Invoice, and a number representing quantity if included
    mybasket = (sales.groupby(['InvoiceID', 'Item'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('InvoiceID'))
    #Need to convert all positive values to 1 and all other to 0 as the quantity is not important over here, what is important is the presence/absence of product in Invoice
    def my_encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1
    my_basket_sets = mybasket.applymap(my_encode_units)
    
    #Only transactions that have more than 1 product in them are included in apriori to find more accurate association relationships
    basket_filter=my_basket_sets[(my_basket_sets>0).sum(axis=1)>=2]
    basket_filter=basket_filter.dropna(inplace=True)
    my_frequent_itemsets = apriori(basket_filter, min_support=0.0007, use_colnames=True).sort_values('support',ascending=False).reset_index(drop=True)
    my_frequent_itemsets['length']=my_frequent_itemsets['itemsets'].apply(lambda x: len(x))
    
    assoc_rules = association_rules(my_frequent_itemsets, metric="lift", min_threshold=1).sort_values("lift",ascending=False).reset_index(drop=True)
    rules=assoc_rules[["antecedents","consequents","support","confidence","lift"]]
#Prediction page
if selected=="Prediction":
    col1,col2=st.columns([1,2])

    with col2:

        st.write("Prediction Page")
        st.write("This page focuses on...")
        st.write("This page focuses on...")
        #"""# Prediction Using Prophet"""
        itemkinds=sales["ItemKind"].unique().tolist()
        kind_select=st.multiselect("Which Item Kind are you interested in?",itemkinds,"Shoes")
        sales['TransDate'] = pd.to_datetime(sales['TransDate'])
        grouped_df= sales.groupby(['TransDate',"ItemKind"]).Revenue.sum().reset_index()
        #prediction= sales.groupby('TransDate').Revenue.sum().reset_index()
        #prediction.columns=["ds","y"]
        grouped_df.columns=["ds","kind","y"]
        prediction=grouped_df[grouped_df["kind"].isin(kind_select)]
        #st.dataframe(prediction)
        # define the model
        model = Prophet()
        # fit the model
        model.fit(prediction)

        # initialize list elements
        #data = ["2021-11-08","2021-11-09","2021-11-10","2021-11-11","2021-11-12","2021-11-13","2021-11-14","2021-11-15","2021-11-16","2021-11-17","2021-11-18","2021-11-19","2021-11-20","2021-11-21","2021-11-22","2021-11-23"]
        from datetime import datetime
        forecastime=st.slider("Choose forecast days",5,35,20)
        data=pd.date_range(start = prediction['ds'].max(), periods = forecastime).tolist()
        # Create the pandas DataFrame with column name is provided explicitly
        future = pd.DataFrame(data, columns=['ds'])


        # use the model to make a forecast
        forecast = model.predict(future)
    st.markdown("""<hr style="height:3px;border:none;color:#00ced1;background-color:#1F628E;" /> """, unsafe_allow_html=True)

    from prophet.plot import plot_plotly, plot_components_plotly
    fig2=plot_plotly(model, forecast)
    st.plotly_chart(fig2)


    fig1=plot_components_plotly(model, forecast)
    st.plotly_chart(fig1)
