
import sqlite3
conn = sqlite3.connect('Prosper_Canada.db')
cursor = conn.cursor()

import pandas as pd
import numpy as np


df = pd.read_excel('redcap_data.xlsx')
df_t = df.pivot_table(index=['project_id', 'event_id'], columns='field_name', values='value', aggfunc=np.sum)
df_t['Year'] = pd.DatetimeIndex(df_t['startdate']).year
df_t['Federal_Tax_Benefits'] = df_t['fed_taxcbc'] + df_t['fed_taxhstgst']
df_t['Provincial_Tax_Benefits'] = df_t['prov_taxotb'] + df_t['prov_taxcai']
df_t['Data_Source'] = 'OFEC'


#print(df_t.head(20))
df_t.to_sql('redcap_data', conn, if_exists='replace', index=True)

cursor.execute('CREATE TABLE IF NOT EXISTS KPI (Year TIMESTAMP, Quarter INTEGER, Data_Source TEXT,'
             'Unique_Key TEXT, '
             'Number_of_people_receiving_financial_coaching INTEGER,'
              'Number_of_financial_literacy_trainings_conducted INTEGER,'
              'Federal_Tax_Benefits INTEGER, '
              'Provincial_Tax_Benefits INTEGER,'
              'Other_Benefits_Secured INTEGER)')
cursor.execute('DELETE FROM KPI')

cursor.execute('INSERT INTO KPI '
               'SELECT Year, quarter, Data_Source, (project_id||"-"||event_id), clients_coaching,'
               'fl_tttworkshops, Federal_Tax_Benefits, Provincial_Tax_Benefits,'
               'ben_claimed_total FROM redcap_data')
conn.commit()


