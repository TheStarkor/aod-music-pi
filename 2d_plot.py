import plotly.express as px
import pandas as pd
import numpy as np

# my_dict = {"direction": ["N", "N", "N"], "frequency": [np.random.rand(1), np.random.rand(1), np.random.rand(1)]}
# my_dict = {"direction": ["N"], "frequency": [np.random.rand(1)]}
# my_dict = {"direction": ["N"], "frequency": [np.random.rand(1)]}
# df = pd.DataFrame(my_dict)
# print(df)
df1 = pd.DataFrame(np.random.randint(0, 100, (100, 1)), columns=['d'])

df = px.data.wind()
fig = px.scatter_polar(df, r="frequency", theta="direction")
fig.show()