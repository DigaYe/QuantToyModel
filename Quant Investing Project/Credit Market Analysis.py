# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 10:17:22 2023

@author: yej
"""

import numpy as np
#from util import st_charts as myChart

import streamlit
import bbgapi as bbgapi

import PyDSWS

bbg = bbgapi.BloombergAPI()

streamlit.set_page_config(layout="wide")
streamlit.title('Credit')
streamlit.subheader('US Investment Grade')

myChart.change_defaults(fontsize=14)

### Styles/Size/Regions ###
ds = PyDSWS.Datastream("ZONT033","MOTOR506")
df_IG = ds.get_data(tickers=['MLCORML(MV)', 'MLCORML(DM)', 'MLCORML(CX)','MLCORML(NOIS)', 'MLCORML(YTW)', 'MLCORML(OAS)'],
                    start='19860101', end='')
df_IG.columns = ['Market Value', 'Modified Duration', 'Convexity (RHS)', 'Number of Issuers', 'Yield', 'Spread']

df_basis = bbg.bdh(['.TFMIGSPR F Index'],
                 fields='PX_LAST', startdate='2000-01-01').resample('B').last().fillna(method='ffill')
df_basis.columns = ['Basis']

myChart.change_defaults(fontsize=14)
fig, ax = myChart.create_fig('JY-1200', rows=3, cols=2,figsize=(17,17))
df_IG_MV = np.log(df_IG['Market Value'].to_frame())
ax1 = myChart.ax_line_plot(ax[0,0],df_IG_MV , title="US IG Market Value (log)",grid=True,title_fontsize=14,
                          x_label='',legend=False, y_label=' ',excel_write=False, legend_loc='upper left',rec_bars=False,extend_date=True,
                           dot=True)
ax1.tick_params(axis='x', labelrotation=0)

ax2 = myChart.ax_line_plot(ax[0, 1], df_IG['Number of Issuers'].loc['1986-06-30':].to_frame(), title="US IG Number of Issuers",grid=True,title_fontsize=14,
                          x_label='',legend=False, y_label=' ',excel_write=False, legend_loc='upper left',rec_bars=False,extend_date=True,
                           dot=True)
ax2.tick_params(axis='x', labelrotation=0)

ax3 = myChart.ax_line_plot(ax[1, 0], df_IG['Modified Duration'], title="US IG Modified Duration",grid=True,title_fontsize=14,
                          x_label='',legend=False, y_label=' ', excel_write=False, legend_loc='upper left',rec_bars=False,extend_date=True,
                           dot=True)
ax3.tick_params(axis='x', labelrotation=0)

ax4 = myChart.ax_line_plot(ax[1,1], df_IG['Yield'].to_frame(), title="US IG Yield (%)",grid=True,title_fontsize=14,
                          x_label='',legend=False, y_label=' ',excel_write=False, legend_loc='upper left',rec_bars=False,extend_date=True,
                           dot=True)
ax4.axhline(df_IG['Yield'].mean() , color='red', linestyle='--')
ax4.tick_params(axis='x', labelrotation=0)

ax5 = myChart.ax_line_plot(ax[2,0], df_IG['Spread'].to_frame(), title="US IG Spread (bps)",grid=True,title_fontsize=14,
                          x_label='',legend=False, y_label=' ',excel_write=False, legend_loc='upper left',rec_bars=False,extend_date=True,
                           dot=True)
ax5.axhline(df_IG['Spread'].mean() , color='red', linestyle='--')
ax5.tick_params(axis='x', labelrotation=0)

ax6 = myChart.ax_line_plot(ax[2,1], df_basis, title="US IG Basis (Cash minus Synthetic Spread)",grid=True,title_fontsize=14,
                          x_label='',legend=False, y_label=' ',excel_write=False, legend_loc='upper left',rec_bars=False,extend_date=True,
                           dot=True)
ax6.axhline(df_basis['Basis'].mean(), color='red', linestyle='--')
ax6.tick_params(axis='x', labelrotation=0)

fig.tight_layout()
streamlit.pyplot(fig)
