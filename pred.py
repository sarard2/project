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
#pio.templates.default = "simple_white"


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
    with st.expander("Have a look at the dataset format!"):
        df_sample=df.sample(frac=0.25)
        AgGrid(df_sample)


#RFM page
if selected=="RFM":
    col1,col2=st.columns(2)
    with col1:
        st.write("Intro")
    with col2:
        st.image("home.jpg")

    #In order to perform customer segmentation, the Invoice Types which are sales are only of interest
    #Thus, only sales dataframe is considered.
    
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Recency</h5>
          <h6 class="card-subtitle mb-2 text-muted">Customer Visits</h6>
          <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          <a href="#" class="card-link">Card link</a>
          <a href="#" class="card-link">Another link</a>
         </div>
        </div>  """,unsafe_allow_html=True)
    with col2:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Recency</h5>
          <h6 class="card-subtitle mb-2 text-muted">Customer Visits</h6>
          <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          <a href="#" class="card-link">Card link</a>
          <a href="#" class="card-link">Another link</a>
         </div>
        </div>  """,unsafe_allow_html=True)
    with col3:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Recency</h5>
          <h6 class="card-subtitle mb-2 text-muted">Customer Visits</h6>
          <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          <a href="#" class="card-link">Card link</a>
          <a href="#" class="card-link">Another link</a>
         </div>
        </div>  """,unsafe_allow_html=True)
    with col4:
        st.markdown(""" 
        <div class="card" style="width: 18rem;">
          <div class="card-body">
          <h5 class="card-title">Recency</h5>
          <h6 class="card-subtitle mb-2 text-muted">Customer Visits</h6>
          <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
          <a href="#" class="card-link">Card link</a>
          <a href="#" class="card-link">Another link</a>
         </div>
        </div>  """,unsafe_allow_html=True)
    st.write("")
    st.markdown("""
    <div class="alert alert-secondary" role="alert">
    </div>
    """,unsafe_allow_html=True)
    
    
    rfm=pd.read_csv("rfm.csv")
    
    col1,col2,col3,col4,col5,col6=st.columns(6)
    
    with col2:
        client1=df["Client"].unique().tolist()
        client_select=st.multiselect("Which customer are you interested in reviewing?",client1,"Tyrone Wright")
        selectedclient=rfm[rfm["Client"].isin(client_select)]
        
    with col5:
        #Second customer
        client2=df["Client"].unique().tolist()
        client_select2=st.multiselect("Which customer are ?",client2,"Peter Smith")
        selectedclient2=rfm[rfm["Client"].isin(client_select2)]
        
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
    with col4:
        overall_value=selectedclient["OverallScore"]
        st.metric(label="Overall Score", value=overall_value)
    with col5:
        recency_value2=selectedclient2["Recency"]
        st.metric(label="Recency", value=recency_value2)
    with col6:
        freq_value2=selectedclient2["Frequency"]
        st.metric(label="Frequency", value=freq_value2)
    with col7:
        monetary_value2=selectedclient2["Revenue"]
        st.metric(label="Revenue", value=monetary_value2)
    with col8:
        overall_value2=selectedclient2["OverallScore"]
        st.metric(label="Overall Score", value=overall_value2)
        
        segments=selectedclient["Segment"].values[0]
        st.write("The client you have selected is",segments)
        segments2=selectedclient2["Segment"].values[0]
        st.write("The client you have selected is",segments2, "as the client has an overall value", overall_value2)
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
   rules=pd.read_csv("rules.csv")
   AgGrid(rules)
   st.markdown("""
   <ul class="list-group list-group-flush">
     <li class="list-group-item">An item</li>
     <li class="list-group-item">A second item</li>
     <li class="list-group-item">A third item</li>
     <li class="list-group-item">A fourth item</li>
     <li class="list-group-item">And a fifth one</li>
     </ul>""",unsafe_allow_html=True)
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
