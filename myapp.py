import streamlit as st
import requests
import json
import pandas as pd
import sqlalchemy as db
import uuid
from datetime import date
from sqlalchemy import create_engine, text
# create a SQLite database using SQLAlchemy
engine = db.create_engine('sqlite:///nytimes.db', echo=True)
conn = engine.connect()

meta = db.MetaData()
fait_artic2 = db.Table(
   'fait_artic2', meta,
   db.Column('id', db.Integer, primary_key=True, autoincrement=True),
   db.Column('abstract', db.String),
   db.Column('snippet', db.String),
   db.Column('lead_paragraph', db.String)
)
meta.create_all(engine)

# create a streamlit app
st.title("New York Times API App")

# get user input for start and end years for the NYT Archive API
sub1 = st.sidebar.subheader("Enter the start and end years for the New York Times Archive API:")
start_year = st.sidebar.number_input("Start Year", value=2010, step=1)
end_year = st.sidebar.number_input("End Year", value=2023, step=1)

# get user input for start and end months for the NYT Archive API
sub2 = st.sidebar.subheader("Enter the start and end months for the New York Times Archive API:")
start_month = st.sidebar.number_input("Start Month", value=1, min_value=1, max_value=12, step=1)
end_month = st.sidebar.number_input("End Month", value=12, min_value=1, max_value=12, step=1)

# define a function to retrieve data from the NYT Archive API
def get_nyt_archive_data(start_year, end_year, start_month, end_month):
    # create an empty dataframe to hold the data
    df_archive = pd.DataFrame()

    # loop through the years and months and retrieve the data
    for year in range(start_year, end_year):
        for month in range(start_month, end_month):
            # create the API endpoint url for each year and month
            url = 'https://api.nytimes.com/svc/archive/v1/' +str(year)+ '/' +str(month) + '.json?api-key=NhNaE50yWYQnrI3nAiNjgjcV8sAC5sR7'
            url_archive = requests.get(url)
            data_archive = json.loads(url_archive.text)
            results_archive = data_archive['response']
            # append the data to the dataframe
            df_archive = df_archive.append(results_archive["docs"])

    # return the dataframe
    return df_archive
data = None
side = st.sidebar.button("submit")
if side :
    data = get_nyt_archive_data(start_year, end_year, start_month, end_month)

# display the data
    st.write("NYT Archive API Results:")
    st.write(data.head())
#data = get_nyt_archive_data(start_year, end_year, start_month, end_month)
# insert the data into the database
    #for x in range(len(data)):
   # uuids = [uuid.uuid4() for i in range(len(data))]
   # uuids2 = [uuid.uuid4() for i in range(len(data))]
     #   data["id_date"].iloc[x] = x
     #   data["id_articles"].iloc[x] = x + 10000
sub2 = st.button("Enregistrer les données")
if sub2:
    data = get_nyt_archive_data(start_year, end_year, start_month, end_month)
    data.fillna(value="none", inplace=True)
    data['word_count'].replace("none",0, inplace=True)
    data = data.drop(["pub_date", "word_count", "headline","web_url" , "source", "multimedia", "keywords", "document_type", "news_desk", "section_name", "subsection_name", "byline", "type_of_material", "_id", "uri", "print_section", "print_page"], axis=1)
    data.to_sql(name='fait_artic2',
         con=engine,
         if_exists='append',
         index=False,
         dtype={
                'abstract': db.String(),
                'snippet': db.String(),
                'lead_paragraph': db.String()})
    st.write("Data saved successfully")

#with st.form('my_form'):
options = ["fait_artic2"]
selected_table = st.selectbox("Select a table", options)
sub0 = st.button('Voir cette table')
if sub0:
    query = f"SELECT * FROM {selected_table}"
    df = pd.read_sql_query(sql=text(query), con=engine.connect())
    st.write(df)
