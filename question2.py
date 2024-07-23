import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('CPIdata.csv')
df = df[df['Date'] >= '2019-01-01']

# Year-over-year percentage variation
df['All Items'] = df['All Items'].pct_change() * 100
df['All Items Less Food and Energy'] = df['All Items Less Food and Energy'].pct_change() * 100
df['Gasoline'] = df['Gasoline'].pct_change() * 100


fig = go.Figure()


fig.add_trace(go.Scatter(x=df['Date'], y=df['All Items'],
                         mode='lines+markers', name='All Items'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['All Items Less Food and Energy'],
                            mode='lines+markers', name='All Items Less Food and Energy'))
fig.add_trace(go.Scatter(x=df['Date'], y=df['Gasoline'],
                            mode='lines+markers', name='Gasoline'))

fig.update_layout(
    title='CPI - Year-over-Year Percentage Change',
    xaxis_title='Date',
    yaxis_title='Year-over-Year Percentage Change (%)',
    template='ggplot2'
)

fig.write_html('question2.html', auto_open=True)
