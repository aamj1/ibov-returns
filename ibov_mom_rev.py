# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 21:31:38 2021

@author: Ahmad
"""

import yfinance
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# auxiliary function;
def dataFrame(ibov, window):
    df = pd.DataFrame(index=ibov.index)
    df['Gross Return'] = ibov['Adj Close']/ibov['Adj Close'].shift(1)
    df['Return'] = df['Gross Return'] - 1

    # 5 and 20 days;
    df['CumRet'] = df['Gross Return'].rolling(window).agg(lambda x: x.prod()) - 1

    return df    

# function to cumulate returns over a horizon based on previous returns;
def cumReturns(k, n_ahead, ibov, window):
    df = dataFrame(ibov, window)
    cumRetUp = pd.DataFrame(index=df[df['CumRet'] >= k].index)
    cumRetDown = pd.DataFrame(index=df[df['CumRet'] <= -k].index)
    
    for idx in cumRetUp.index:
        t = df.index.get_loc(idx)
        cumRetUp.loc[idx,'ret'] = 100*(df.iloc[(t + 1):(t + n_ahead),:]['Gross Return'].prod()-1)

    for idx in cumRetDown.index:
        t = df.index.get_loc(idx)
        cumRetDown.loc[idx,'ret'] = 100*(df.iloc[(t + 1):(t + n_ahead),:]['Gross Return'].prod()-1)

    return dict({'Up': cumRetUp, 'Down': cumRetDown})
    
# download data from yahoo;
ibov =  yfinance.download("^BVSP", start="2001-01-01", end="2021-09-20")

# plot figures (lazy way);
f, axes = plt.subplots(2, 2, figsize=(12, 10))
sns.distplot(cumReturns(0.05, 20, ibov, 5)['Up'],
             hist=False,
             ax=axes[0,0],
             label='k = 5%, n = 20 days')
sns.distplot(cumReturns(0.05, 20, ibov, 5)['Down'],
             hist=False,
             ax=axes[0,0],
             label='k = -5%, n = 20 days')
axes[0,0].legend()
sns.distplot(cumReturns(0.1, 20, ibov, 5)['Up'],
             hist=False,
             ax=axes[0,1],
             label='k = 10%, n = 20 days')
sns.distplot(cumReturns(0.1, 20, ibov, 5)['Down'],
             hist=False,
             ax=axes[0,1],
             label='k = -10%, n = 20 days')
axes[0,1].legend()
sns.distplot(cumReturns(0.05, 60, ibov, 5)['Up'],
             hist=False,
             ax=axes[1,0],
             label='k = 5%, n = 60 days')
sns.distplot(cumReturns(0.05, 60, ibov, 5)['Down'],
             hist=False,
             ax=axes[1,0],
             label='k = -5%, n = 60 days')
axes[1,0].legend()
sns.distplot(cumReturns(0.1, 60, ibov, 5)['Up'],
             hist=False,
             ax=axes[1,1],
             label='k = 10%, n = 60 days')
sns.distplot(cumReturns(0.1, 60, ibov, 5)['Down'],
             hist=False,
             ax=axes[1,1],
             label='k = -10%, n = 60 days')
axes[1,1].legend()