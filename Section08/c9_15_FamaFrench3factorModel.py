
"""
  Name     : c9_15_FamaFrench3factorModel.py
  Book     : Hands-on Data Science with Anaconda )
  Publisher: Packt Publishing Ltd. 
  Author   : Yuxing Yan and James Yan
  Date     : 4/6/2018
  email    : yany@canisius.edu
             paulyxy@hotmail.com
"""

import scipy as sp
import numpy as np
import pandas as pd
import statsmodels.api as sm
from matplotlib.finance import quotes_historical_yahoo_ochl as getData
ticker='IBM'
begdate=(2012,1,1)
enddate=(2016,12,31)
p= getData(ticker, begdate, enddate,asobject=True, adjusted=True)
logret = sp.log(p.aclose[1:]/p.aclose[:-1])
ddate=[]
d0=p.date
for i in range(0,sp.size(logret)):
    x=''.join([d0[i].strftime("%Y"),d0[i].strftime("%m"),"01"])
    ddate.append(pd.to_datetime(x, format='%Y%m%d').date())
#    
t=pd.DataFrame(logret,np.array(ddate),columns=['RET'])
ret=sp.exp(t.groupby(t.index).sum())-1
#
ff=pd.read_pickle('c:/temp/ffMonthly.pkl')
final=pd.merge(ret,ff,left_index=True,right_index=True)
y=final['RET']
x=final[['MKT_RF','SMB','HML']]
x=sm.add_constant(x)
results=sm.OLS(y,x).fit()
print(results.summary())
