import pandas as pd
import matplotlib.pyplot as plt
from pandas.core import datetools
import statsmodels.api as sm
import math


sc = pd.read_pickle('data.pkl')
# print(sc.columns)
sc.columns = ['index','admitrate','satscores','mediandebt','cost','earnings','retention','schoolname']

sc.dropna()

sc['earningslog'] = sc['earnings'].apply(lambda x:
    math.log(x,10)
)
print(sc.head(1))

# print(sc.info)
print(sc.columns)
plt.scatter(sc.cost,sc.earningslog,1)
# plt.show()
plt.savefig('foo.png', bbox_inches='tight')

model = sm.OLS(sc.cost,sc.earnings,missing = 'drop')
model = model.fit()
print(model.summary())
