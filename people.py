# ALS Hiring Exercise

#%% import packages
import os
import pandas as pd
import datetime as dt

#%% parent directory
parentdir = os.path.abspath(os.path.dirname(__file__))

#%% set data inputs
# cons_info for constituent information, cons_email for constituent emails 
# and cons_subscr for constituent subscription status
cons_info_file = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons.csv'
cons_email_file = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email.csv'
cons_subscr_file = 'https://als-hiring.s3.amazonaws.com/fake_data/2020-07-01_17%3A11%3A00/cons_email_chapter_subscription.csv'

#%% read and format data
# per specifications analysis is limited to chapter_id = 1 for cons_subscr
print(f'Reading and formatting constituent data')
cons_subscr_dtypes = {'cons_email_id': object, 'isunsub': bool}
cons_subscr = pd.read_csv(cons_subscr_file, dtype=cons_subscr_dtypes)
cons_subscr = cons_subscr.loc[cons_subscr['chapter_id'] == 1]
cons_subscr['isunsub'] = cons_subscr['isunsub'].fillna(False)

cons_info_dtypes = {'cons_id': str, 'source': str}
cons_info = pd.read_csv(cons_info_file, dtype=cons_info_dtypes)

cons_email_parse_dates = ['create_dt', 'modified_dt']
cons_email_dtypes = {'cons_email_id': str, 'cons_id': str, 'email': str}
cons_email = pd.read_csv(cons_email_file, dtype=cons_email_dtypes, parse_dates=cons_email_parse_dates)

#%% combine data sources to create people directory
# use create_dt and modified_dt from cons_email as these are unique to the email address
# create_dt and modified_dt in cons_info are mapped to the primary account holder
print(f'Analyzing constituent data')
cons_email_subscr = pd.merge(cons_email, cons_subscr[['cons_email_id', 'isunsub']], on='cons_email_id', how='left')
cons_email_subscr_columns = ['cons_id', 'email', 'isunsub', 'create_dt', 'modified_dt']
cons_email_subscr = cons_email_subscr[cons_email_subscr_columns]
people = pd.merge(cons_email_subscr, cons_info[['cons_id', 'source']], on='cons_id', how='left').reset_index()
people = people.drop(columns=['cons_id'])
# rename columns to align with specified schema
people = people.rename(columns={'source': 'code', 'isunsub': 'is_unsub', 'create_dt': 'created_dt', 'modified_dt': 'updated_dt'})

#%% aggregate date based on created_dt
acquisition_facts = people.groupby(people['created_dt'].dt.date).size().reset_index(name='acquisitions')

#%% save people and acquisition_facts dataframes as csv, using parentdir
save_folder = 'als_hiring_exercise'
save_file_path = f'{parentdir}/{save_folder}'
# create folder if it does not exist
if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)
print(f'Saving files to {save_file_path}')
people.to_csv(f'{save_file_path}/people.csv', index=False)
acquisition_facts.to_csv(f'{save_file_path}/acquisition_facts.csv', index=False)