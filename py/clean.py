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



darkblue='#4148e8'
lightblue='#6f63f2'
red='#ec5237'
green='#43d1cd'
colors = {1:red,2:lightblue,3:green}

def makeScatterPlot(x,y,lineBool,xTitle,yTitle,groupBool): #explanatory and response must be column names
    model = sm.OLS(x,y,missing='drop')
    model = model.fit()
    print(model.summary())

    r = math.sqrt(model.rsquared)
    sx = x.std()
    sy = y.std()
    xbar = x.mean()
    ybar = y.mean()
    b1 = r * (sy / sx)
    b0 = ybar - (b1 * xbar)
    print(r, sx, sy, xbar, ybar, b1, b0)

    def regressionLine(x):
        return b0 + (b1 * x)

    if (groupBool):
        plt.scatter(x,y,1,c=sc['ownership'].apply(lambda x: colors[x]))
    else:
        plt.scatter(x,y,1,green)
    if (lineBool):
        plt.plot(x, regressionLine(x), c='#079799', aa=True)
    plt.xlabel(xTitle, size='smaller')
    plt.ylabel(yTitle, size='smaller')

# makeScatterPlot(sc[sc["ownership"] == 3]["costlog"],sc[sc["ownership"] == 3]["earningslog"],True,'Log of Cost of Attendance ($)','Log of Earnings, 10 Years After Entry into Institution ($)',False)
makeScatterPlot(sc['cost'],sc['earnings'],True,'Log of Cost of Attendance ($)','Log of Earnings, 10 Years After Entry into Institution ($)',False)

plt.title('Cost vs Earnings in US Higher Ed Institutions (Private For-profit)', size='smaller')
# plt.savefig('privatefp-line.png', dpi=150, bbox_inches='tight')
