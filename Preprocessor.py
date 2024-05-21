import pandas as pd


def preprocess(olympic_df,region_df):
    olympic_df[olympic_df['Season']=='Summer']
    olympic_df=olympic_df.merge(region_df,on='NOC',how='left')
    olympic_df.drop_duplicates(inplace=True)
    olympic_df=pd.concat([olympic_df,pd.get_dummies(olympic_df['Medal'])],axis=1)
    return olympic_df


