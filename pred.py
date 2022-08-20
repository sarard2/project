import pandas as pd
import streamlit as st
import matplotlib as plt
import numpy
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid
import plotly
import plotly.graph_objects as go
import plotly.express as px
from prophet import Prophet
import plotly.io as pio
import pickle

#Setting page width to wide
st.set_page_config(layout="wide")

#Loading Data
 
df=pd.read_csv(r"transactions.csv")
sales=df[df["InvoiceType"]=="Sales"]
sales['TransDate'] = pd.to_datetime(sales['TransDate'])
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
    selected = option_menu(None, ["Overview","Customers","Transactions","Sales Prediction"],
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
 col1,col2=st.columns(2)
 with col1:
  st.markdown("""<h3>Retail Analysis<span class="badge bg-secondary"></span></h3>""", unsafe_allow_html=True) 
  st.write("This application includes a set of machine learning tools that would allow the company to know more abouts its customers and its transactions.")
  st.write("The examination of a business’s data aids the management in taking strategic decisions and provides the business with indisputable evidence on the effectiveness of its strategies. ")
 with col2:
  st.image("dashboard.jpeg")
  
 with st.expander("View the Dataset"):
  df_sample=df.sample(frac=0.25)
  AgGrid(df_sample)


#Customers page
if selected=="Customers":
    col1,col2=st.columns(2)
    with col1:
        st.markdown("""<h3>Customer RFM Analysis<span class="badge bg-secondary"></span></h3>""", unsafe_allow_html=True)
        st.write("The latter is a marketing approach that is used to statistically evaluate and classify clients based on the frequency, total dollar amount, and recency of their most recent transactions.")
        st.write("It aims at pinpointing the best customers and consequently executing focused marketing campaigns.")
    with col2:   
     st.image("client.jpeg")
     
    #In order to perform customer segmentation, the Invoice Types which are sales are only of interest
    #Thus, only sales dataframe is considered.
    
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Recency</h5>
          <h6 class="card-subtitle mb-2 text-muted">How recent was the customer's last purchase?</h6>
          <p class="card-text">Customers who recently made a purchase will still have the product on their mind and are more likely to purchase or use the product again. Businesses often measure recency in days.</p>
         
         </div>
        </div>  """,unsafe_allow_html=True)
    with col2:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Frequency</h5>
          <h6 class="card-subtitle mb-2 text-muted">How often did this customer make a purchase?</h6>
          <p class="card-text">Customers who purchased once are often are more likely to purchase again. Additionally, first time customers may be good targets for follow-up advertising to convert them into more frequent customers.</p>
         
         </div>
        </div>  """,unsafe_allow_html=True)
    with col3:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Monetary</h5>
          <h6 class="card-subtitle mb-2 text-muted">How much money did the customer spend?</h6>
          <p class="card-text">Customers who spend a lot of money are more likely to spend money in the future and have a high value to a business. The total revenue of each client is calculated during a given period.</p>
         
         </div>
        </div>  """,unsafe_allow_html=True)
    with col4:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Customer Segment</h5>
          <h6 class="card-subtitle mb-2 text-muted">How are customers different?</h6>
          <p class="card-text">According to the recency, frequency and monetary value, customers are given scores and are then segmented into groups. Each group will be targeted differently. A customer is either "High Value", "Mid Value" or "Low Value".</p>
        
         </div>
        </div>  """,unsafe_allow_html=True)
    
    st.write("")
    st.markdown("""
    <div class="alert alert-secondary" role="alert">
    </div>
    """,unsafe_allow_html=True)
    
    #Model of rfm From Pickle File
    rfm=pickle.load(open("rfm.pkl",'rb'))
    
    client1=df["Client"].unique().tolist()
    client2=df["Client"].unique().tolist()
    
    col1,col2,col3,col4=st.columns(4)
    with col1:
        client_select=st.multiselect("Choose first customer:",client1,"Terry Klein")
        selectedclient=rfm[rfm["Client"].isin(client_select)]
        segments=selectedclient["Segment"].values[0]
        st.write("The client you have selected is",segments)  
    
    with col3:
        client_select2=st.multiselect("Choose another customer:",client2,"Raymond Walters")
        selectedclient2=rfm[rfm["Client"].isin(client_select2)]
        segments2=selectedclient2["Segment"].values[0]
        st.write("The client you have selected is",segments2)
    
    col1,col2,col3,col4,col5,col6,col7,col8=st.columns(8)  
    with col1:
        recency_value=selectedclient["Recency"]
        st.metric(label="Recency", value=recency_value)
    with col2:
        freq_value=selectedclient["Frequency"]
        st.metric(label="Frequency", value=freq_value)
    with col3:
        monetary_value=selectedclient["Revenue"]
        st.metric(label="Revenue", value=monetary_value)
    #with col4:
        #overall_value=selectedclient["OverallScore"]
        #st.metric(label="Overall Score", value=overall_value)
    with col5: 
        recency_value2=selectedclient2["Recency"]
        st.metric(label="Recency", value=recency_value2)
    with col6:
        freq_value2=selectedclient2["Frequency"]
        st.metric(label="Frequency", value=freq_value2)
    with col7:
        monetary_value2=selectedclient2["Revenue"]
        st.metric(label="Revenue", value=monetary_value2)
    #with col8:
        #overall_value2=selectedclient2["OverallScore"]
        #st.metric(label="Overall Score", value=overall_value2)  
        
        
    clientsales=sales[sales["Client"].isin(client_select)]
    clientsales2=sales[sales["Client"].isin(client_select2)]
    grouped_sales= clientsales.groupby('TransDate').Revenue.sum().reset_index()
    grouped_sales2= clientsales2.groupby('TransDate').Revenue.sum().reset_index()  
    
    col1,col2=st.columns(2)
    
    with col1:
        figure=px.line(grouped_sales,x="TransDate",y="Revenue")
        figure.update_layout(xaxis_title="",yaxis_title="Revenue")
        figure.update_xaxes(showgrid=False,zeroline=False)
        figure.update_yaxes(showgrid=False,showticklabels = True)
        st.plotly_chart(figure)
    
    with col2:
        figure1=px.line(grouped_sales2,x="TransDate",y="Revenue")
        figure1.update_layout(xaxis_title="",yaxis_title="Revenue")
        figure1.update_xaxes(showgrid=False,zeroline=False)
        figure1.update_yaxes(showgrid=False,showticklabels = True)
        st.plotly_chart(figure1)
        

#ARM page
if selected=="Transactions": 
    #Model of rules From Pickle File
    rules=pickle.load(open("arm.pkl",'rb'))
    
    col1,col2=st.columns(2)
    with col1:
     st.markdown("""<h3>Market Basket Analysis<span class="badge bg-secondary"></span></h3>""", unsafe_allow_html=True)
     st.write("Market Basket Analysis is one of the key techniques used by large retailers to uncover associations between items. It works by looking for combinations of items that occur together frequently in transactions. It allows retailers to identify relationships between the items that people buy.")
     st.write("The growing application of market basket analysis would allow retailers to better anticipate the purchasing habits of customers and to forecast the likelihood of products being purchased together.")
    with col2:
        st.image("money.png")
    unique=sales.groupby('InvoiceID')["Quantity"].count().reset_index()
    unique2=unique[unique["Quantity"]<30]
    figure3=px.histogram(unique2,x="Quantity")
    figure3.update_layout(xaxis_title="Number of Unique Items",yaxis_title="",title="Number of Unique Products per Transaction")
    figure3.update_xaxes(showgrid=False,zeroline=False)
    figure3.update_yaxes(showgrid=False,showticklabels = True)
    st.plotly_chart(figure3)
   
    with st.expander("Have a look at the dataset format!"):  
        AgGrid(rules)
    col1,col2,col3=st.columns(3)
    with col1:
     st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Customer Segment</h5>
          <h6 class="card-subtitle mb-2 text-muted">How are customers different?</h6>
          <p class="card-text">According to the recency, frequency and monetary value, customers are given scores and are then segmented into groups. Each group will be targeted differently. A customer is either "High Value", "Mid Value" or "Low Value".</p>
        
         </div>
        </div>  """,unsafe_allow_html=True)
     with col2:
     st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Customer Segment</h5>
          <h6 class="card-subtitle mb-2 text-muted">How are customers different?</h6>
          <p class="card-text">According to the recency, frequency and monetary value, customers are given scores and are then segmented into groups. Each group will be targeted differently. A customer is either "High Value", "Mid Value" or "Low Value".</p>
        
         </div>
        </div>  """,unsafe_allow_html=True)
     with col3:
     st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Customer Segment</h5>
          <h6 class="card-subtitle mb-2 text-muted">How are customers different?</h6>
          <p class="card-text">According to the recency, frequency and monetary value, customers are given scores and are then segmented into groups. Each group will be targeted differently. A customer is either "High Value", "Mid Value" or "Low Value".</p>
        
         </div>
        </div>  """,unsafe_allow_html=True)
    
    st.markdown("""
    <ul class="list-group list-group-flush">
     <li class="list-group-item">item</li>
     <li class="list-group-item">A second item</li>
     <li class="list-group-item">A third item</li>
     <li class="list-group-item">A fourth item</li>
     <li class="list-group-item">And a fifth one</li>
     </ul>""",unsafe_allow_html=True)


#Prediction page
if selected=="Sales Prediction":
    
    from datetime import datetime
    from prophet.plot import plot_plotly, plot_components_plotly
    col1,col2=st.columns(2)
    with col1:
        st.markdown("""<h3>Forecast Sales Analysis<span class="badge bg-secondary"></span></h3>""", unsafe_allow_html=True)
        st.write("Forecasting is a procedure for estimating the future sales trend based on past sales behavior. ")
        st.write("This is of great importance for a business as it allows it to allocate resources in an efficient and timely manner and enhance future growth.")
        st.write("The library Prophet is used for the forecasting. ")
    with col2:
     st.image("forecast.jpeg")
    st.markdown("""<hr style="height:5px;border:none;color:#00ced1;background-color:#1F628E;" /> """, unsafe_allow_html=True)
    col1,col2,col3,col4=st.columns(4)
    with col1:
        itemkinds=sales["ItemKind"].unique().tolist()
        kind_select=st.multiselect("Choose an Item Family",itemkinds,"Shoes")
    with col2:
        grouped_df= sales.groupby(['TransDate',"ItemKind"]).Revenue.sum().reset_index()
        grouped_df.columns=["ds","kind","y"]
        prediction=grouped_df[grouped_df["kind"].isin(kind_select)]
        model = Prophet()
        model.fit(prediction)
        forecastime=st.slider("Choose the Number of Forecast Days",7,45,30)
        data=pd.date_range(start = prediction['ds'].max(), periods = forecastime).tolist()
        future = pd.DataFrame(data, columns=['ds'])
        forecast = model.predict(future)
        forecast['ds'] = pd.to_datetime(forecast['ds'])
    
    col1,col2=st.columns([2,1])
    with col1:
        fig2=plot_plotly(model, forecast)
        fig2.update_layout(xaxis_title="",yaxis_title="Revenue",title="Revenue Forecasts")
        fig2.update_xaxes(showgrid=False,zeroline=False)
        fig2.update_yaxes(showgrid=False,showticklabels = True)
        st.plotly_chart(fig2)
    with col2:
     st.write("The blue line represents the sales forecast to the future")
     st.write("The blue area represents the sales prediction with upper and lowers limits")
     values=forecast[["ds","yhat"]]
     values.columns=["Date","Expected Revenue"]
     with st.expander("Have a look at the predicted revenue values!"):
      AgGrid(values)
    
    col1,col2=st.columns([2,1])
    with col1:
     fig1=plot_components_plotly(model, forecast)
     fig1.update_layout(title="Forecast Trends")
     fig1.update_xaxes(showgrid=False,zeroline=False)
     fig1.update_yaxes(showgrid=False,showticklabels = True)
     st.plotly_chart(fig1)
  
