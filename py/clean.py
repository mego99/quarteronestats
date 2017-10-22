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

def regressionLine(x):
    return b0 + (b1 * x)

def makeScatterPlot(explanatory,response,lineBool,xTitle,yTitle,groupBool): #explanatory and response must be Pandas Series
    model = sm.OLS(sc[explanatory],sc[response],missing='drop')
    model = model.fit()
    print(model.summary())

    r = math.sqrt(model.rsquared)
    sx = sc[explanatory].std()
    sy = sc[response].std()
    xbar = sc[explanatory].mean()
    ybar = sc[response].mean()
    b1 = r * (sy / sx)
    b0 = ybar - (b1 * xbar)
    if (groupBool):
        plt.scatter(sc[explanatory],sc[response],1,c=sc['ownership'].apply(lambda x: colors[x]))
    else:
        plt.scatter(sc[explanatory],sc[response],1,'#4148e8')
    if (lineBool):
        plt.plot(sc[explanatory], regressionLine(sc[explanatory]), c='#079799', aa=True)
    plt.xlabel(xTitle, size='smaller')
    plt.ylabel(yTitle, size='smaller')

makeScatterPlot('cost','earnings',False,'Cost of Attendance ($)','Earnings, 10 Years After Entry into Institution ($)',False)

plt.title('Cost vs Earnings in US Higher Ed Institutions', size='smaller')
plt.savefig('test.png', dpi=150, bbox_inches='tight')
