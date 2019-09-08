import pandas as pd
import plotly.express as px

data = pd.read_csv('./Data/EconModel/results_summary_bycrop.csv')
dp = data['p'].unique()
dc1 = data['c1'].unique()
dc2 = data['c2'].unique()
dfs = data['fertilizer subsidy (%)'].unique()


df = data[(data["p"]==0)&(data["c1"]==0)&(data["c2"]==0)&(data["c2"]==0)]
dc = data[(data["c1"]==0)]
fig = px.bar(data, y="yield (kg/ha)", x="production (kg)", color="crop", barmode='group',height=400)

#fig = px.scatter(dc, x="fertilizer subsidy (%)", y="yield (kg/ha)", color="crop")

fig.show()

