#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests as r
import pandas as pd

import sys
sys.path.append("../helper_functions")
import duneapi_utils as d
import metabaseapi_utils as mb
sys.path.pop()

import os
import dotenv

dotenv.load_dotenv()
mb_name = os.environ["MS_METABASE_NAME"]
mb_pw = os.environ["MS_METABASE_PW"]

mb_url_base = "https://dash.goldsky.com"

# https://goldsky.notion.site/SHARED-Lightweight-API-Documentation-for-Goldsky-Dashboarding-5cde15ba222844f485c31a4426f6ed53


# In[ ]:


# Map Chain Names
chain_mappings = {
    'zora': 'Zora Network',
    'pgn': 'Public Goods Network',
    # Add more mappings as needed
}


# In[ ]:


try: #do you already have a session
        session_id = os.environ["MS_METABASE_SESSION_ID"]
except: #if not, make one
        print('creating new session')
        session_id = mb.get_mb_session_key(mb_url_base,mb_name,mb_pw)
# print(session_id)



# In[ ]:


# Run Query

#21-op-chains-activity-by-day
resp = mb.get_mb_query_response(mb_url_base, session_id, 21, num_retries = 3)
# print(resp)


# In[ ]:


data_df = pd.DataFrame(resp)

data_df['chain'] = data_df['chain'].replace(chain_mappings)

print(data_df.columns)
# print(data_df.dtypes)

print(data_df.sample(5))


# In[ ]:


# Post to Dune API
d.write_dune_api_from_pandas(data_df, 'opchain_activity_by_day_gs',\
                             'Basic Daily Activity for OP Chains - Zora & PGN (from Goldsky)')

