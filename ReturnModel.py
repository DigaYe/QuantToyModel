import pandas as pd
import numpy as np
from util import st_charts as myChart
import streamlit
import bbgapi as bbgapi

bbg = bbgapi.BloombergAPI()

x = bbg.bdh(["NFP T Index", "AWH TOTL Index", "AHE TOTL Index"], startdate="2006-03-01", per='M')
x.columns = ["Jobs", "Hours", "Wages"]
x['Total'] = x['Jobs'] * x['Hours'] * x['Wages']
