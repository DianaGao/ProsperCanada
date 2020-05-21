
# import sqlite3
# conn = sqlite3.connect('Prosper_Canada.db')
# cursor = conn.cursor()

import pandas as pd
import numpy as np


df = pd.read_excel('/Users/chengshuliu/Documents/Prosper Canada/redcap_data.xlsx')
df_t = df.pivot_table(index=['project_id', 'event_id'], columns='field_name', values='value', aggfunc=np.sum)
df_t_new = df_t.reset_index()
df_t_new['UniqueID'] = df_t_new['project_id'].map(str) + '-' + df_t_new['event_id'].map(str)
df_t_new['Year'] = pd.DatetimeIndex(df_t_new['startdate']).year
df_t_new['Federal_Tax_Benefits'] = df_t_new['fed_taxcbc'] + df_t_new['fed_taxhstgst']
df_t_new['Provincial_Tax_Benefits'] = df_t_new['prov_taxotb'] + df_t_new['prov_taxcai']
df_t_new['Data_Source'] = 'OFEC'
df_t_new.rename(columns={'quarter':'Quarter', 'clients_coaching':'Number_of_people_receiving_financial_coaching',
                  'fl_tttworkshops':'Number_of_financial_literacy_trainings_conducted',
                  'ben_claimed_total':'Other_Benefits_Secured'}, inplace=True)

# KPI = pd.DataFrame(df_t_new[['UniqueID', 'Year', 'Quarter', 'Data_Source', 'Number_of_people_receiving_financial_coaching',
#                              'Number_of_financial_literacy_trainings_conducted', 'Federal_Tax_Benefits',
#                              'Provincial_Tax_Benefits', 'Other_Benefits_Secured']],
#                             columns=['UniqueID', 'Year', 'Quarter', 'Data_Source', 'Number_of_people_receiving_financial_coaching',
#                                        'Number_of_financial_literacy_trainings_conducted', 'Federal_Tax_Benefits',
#                                        'Provincial_Tax_Benefits', 'Other_Benefits_Secured'])
######## INSERT DATA INTO A NEW DF NAMED KPI ##########
KPI = pd.DataFrame(df_t_new, columns=['UniqueID', 'Year', 'Quarter', 'Data_Source', 'Number_of_people_receiving_financial_coaching',
                                       'Number_of_financial_literacy_trainings_conducted', 'Federal_Tax_Benefits',
                                       'Provincial_Tax_Benefits', 'Other_Benefits_Secured'])

# print(df_t_new[['UniqueID', 'Year', 'Quarter', 'Data_Source', 'Number_of_people_receiving_financial_coaching',
#                              'Number_of_financial_literacy_trainings_conducted', 'Federal_Tax_Benefits',
#                              'Provincial_Tax_Benefits', 'Other_Benefits_Secured']].head(10))
print(KPI.head(10))
# print(df_t.head(20))
# print(df_t_new.head(5))
#print(df_t.reset_index())

# df_t.to_sql('redcap_data', conn, if_exists='replace', index=True)
#
# cursor.execute('CREATE TABLE IF NOT EXISTS KPI (Year TIMESTAMP, Quarter INTEGER, Data_Source TEXT,'
#              'Unique_Key TEXT, '
#              'Number_of_people_receiving_financial_coaching INTEGER,'
#               'Number_of_financial_literacy_trainings_conducted INTEGER,'
#               'Federal_Tax_Benefits INTEGER, '
#               'Provincial_Tax_Benefits INTEGER,'
#               'Other_Benefits_Secured INTEGER)')
# cursor.execute('DELETE FROM KPI')
#
# cursor.execute('INSERT INTO KPI '
#                'SELECT Year, quarter, Data_Source, (project_id||"-"||event_id), clients_coaching,'
#                'fl_tttworkshops, Federal_Tax_Benefits, Provincial_Tax_Benefits,'
#                'ben_claimed_total FROM redcap_data')
# conn.commit()


