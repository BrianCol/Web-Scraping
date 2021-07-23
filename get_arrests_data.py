import sqlalchemy as sa
import getpass 
import pandas as pd
import requests
from datetime import datetime, date, timedelta  

user = input('What is your username?')
pwd = getpass.getpass(prompt = 'What is your password?')
host = '10.18.54.68'
database = 'bcolgrov'

cnx_string = 'mysql+pymysql://'+user + ':'+pwd + '@' + host + '/' + database

cnxn = sa.create_engine(cnx_string)

yesterday = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
today = datetime.today()

SoQL = "https://data.montgomerycountymd.gov/resource/xhwt-7h2h.json?$query=SELECT *"
results = requests.get(SoQL)

dictr = results.json()

results_df = pd.json_normalize(dictr)

results_df['insert_dt'] = today
     
# Push to mySQL database
results_df.to_sql(name = 'arrests',con = cnxn, if_exists = 'append', index = False)

