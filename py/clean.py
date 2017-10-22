import pandas as pd
import matplotlib.pyplot as plt
from pandas.core import datetools
import statsmodels.api as sm
import math


sc = pd.read_pickle('data.pkl')
sc.columns = ['index','admitrate','satscores','mediandebt','cost','earnings','retention','schoolname']

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
sx = sc['cost'].std()
sy = sc['earnings'].std()
xbar = sc['cost'].mean()
ybar = sc['earnings'].mean()
b1 = r * (sy / sx)
b0 = ybar - (b1 * xbar)


def regressionLine(x):
    return b0 + (b1 * x)

plt.scatter(sc.cost,sc.earnings,1,c='#4148e8')
plt.plot(sc.cost, regressionLine(sc.cost), c='#00243d', aa=True)
plt.xlabel('Cost of Attendance ($)', size='smaller')
plt.ylabel('Earnings, 10 Years After Entry into Institution ($)', size='smaller')
plt.title('Cost vs Earnings in US Higher Ed Institutions', size='smaller')
plt.savefig('original-line.png', dpi=150, bbox_inches='tight')
