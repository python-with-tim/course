import streamlit as st

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tiobeindexpy import tiobeindexpy

def percent_to_float(x):
    return float(x.strip('%'))

def get_cleaned_data():

    df = tiobeindexpy.top_20()

    df.dropna(axis='columns', inplace=True)

    df['Change.1'] = df['Change.1'].apply(percent_to_float)
    df['Ratings'] = df['Ratings'].apply(percent_to_float)

    df.rename(inplace=True, columns={
        'Programming Language.1':'Programming Language',
        'Change.1':'Change (%)',
        'Ratings':'Ratings (%)'
    })

    df['Old ratings (%)'] = df['Ratings (%)'] - df['Change (%)']

    return df



def popularity_barplot(df, label, target='Programming Language', sort_by='Ratings (%)', n_top=10):

    sns.barplot(
        x=sort_by, y=target, data=df.head(n_top).sort_values(by=sort_by, ascending=False),
        palette='crest_r',
    )

    plt.title(f'Popularity of Programming Languages ({label})')
    plt.bar_label(plt.gca().containers[0], fmt='%.2f%%')

    sns.despine()
    plt.show()


st.title('Programming Languages Popularity')
df = get_cleaned_data()

st.markdown('### Top languages bar chart')

n_top = st.slider('Number of languages:', 3, 20, 10)

month = st.selectbox('Month:', df.columns[:2])
sort_by = 'Old ratings (%)' if month == 'Dec 2021' else 'Ratings (%)'
label = month

popularity_barplot(df, label, sort_by=sort_by, n_top=n_top)
fig = plt.gcf()
st.pyplot(fig)

st.markdown('### Check your favorite language')
language = st.selectbox('Programming language:', df['Programming Language'].unique())

# filter the dataframe
df_lang = df[df['Programming Language'] == language].drop(columns=['Programming Language'])

# display the dataframe, 2 decimal places
st.dataframe(df_lang.style.format({
    'Change (%)': '{:.2f}',
    'Ratings (%)': '{:.2f}',
    'Old ratings (%)': '{:.2f}',
}))