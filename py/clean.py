import pandas as pd
import matplotlib.pyplot as plt
from pandas.core import datetools
import statsmodels.api as sm


sc = pd.read_pickle('data.pkl')
print(sc.columns)
sc.columns = ['index','admitrate','satscores','mediandebt','cost','earnings','retention','schoolname']
print(sc.head(1))
# print(sc.info)
print(sc.columns)
plt.scatter(sc.retention,sc.earnings,1)
# plt.show()
plt.savefig('foo.png', bbox_inches='tight')

model = sm.OLS(sc.retention,sc.earnings)
model = model.fit()
print(model.summary())
