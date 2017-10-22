import pandas as pd
import matplotlib.pyplot as plt
from pandas.core import datetools
import statsmodels.api as sm
import math


sc = pd.read_pickle('data.pkl')
print(sc.columns)
sc.columns = ['index','admitrate','satscores','mediandebt','cost','earnings','retention','schoolname','ownership']
sc.dropna()

sc['costsqrt'] = sc['cost'].apply(lambda x:
    math.sqrt(x)
)
sc['costlog'] = sc['cost'].apply(lambda x:
    math.log(x)
)
sc['earningslog'] = sc['earnings'].apply(lambda x:
    math.log(x)
)

model = sm.OLS(sc.costlog,sc.earningslog,missing='drop')
model = model.fit()
print(model.summary())

r = math.sqrt(model.rsquared)
sx = sc['costlog'].std()
sy = sc['earningslog'].std()
xbar = sc['costlog'].mean()
ybar = sc['earningslog'].mean()
b1 = r * (sy / sx)
b0 = ybar - (b1 * xbar)


def regressionLine(x):
    return b0 + (b1 * x)

colors = {1:'#ec5237',2:'#5346e7',3:'#43d1cd'}

plt.scatter(sc.costlog,sc.earningslog,1,c=sc['ownership'].apply(lambda x: colors[x]))
# plt.plot(sc.costlog, regressionLine(sc.costlog), c='#079799', aa=True)
plt.xlabel('Log of Cost of Attendance ($)', size='smaller')
plt.ylabel('Log of Earnings, 10 Years After Entry into Institution ($)', size='smaller')
plt.title('Cost vs Earnings in US Higher Ed Institutions', size='smaller')
plt.savefig('ownership-grouped.png', dpi=150, bbox_inches='tight')
