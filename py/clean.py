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
sc['logcostsq'] = sc['cost'].apply(lambda x:
    math.log(x*x)
)
sc['costlog'] = sc['cost'].apply(lambda x:
    math.log(x)
)
sc['earningslog'] = sc['earnings'].apply(lambda x:
    math.log(x)
)
sc['earningssq'] = sc['earnings'].apply(lambda x:
    x*x
)
sc['earningssqrt'] = sc['earnings'].apply(lambda x:
    math.sqrt(x)
)
sc['sqearningslog'] = sc['earningslog'].apply(lambda x:
    x*x
)
sc['sqcostlog'] = sc['costlog'].apply(lambda x:
    x * x
)
sc['earningslogsq'] = sc['earnings'].apply(lambda x:
    math.log(x*x)
)
sc['costlogsqrt'] = sc['cost'].apply(lambda x:
    math.log(math.sqrt(x))
)
sc['earningsloglog'] = sc['earningslog'].apply(lambda x:
    math.log(x)
)
sc['sqrtcostlog'] = sc['costlog'].apply(lambda x:
    math.sqrt(x)
)
sc['sqrtearningslog'] = sc['earningslog'].apply(lambda x:
    math.sqrt(x)
)

darkblue='#4148e8'
lightblue='#6f63f2'
red='#ec5237'
green='#43d1cd'
colors = {1:red,2:lightblue,3:green}

def makeRegression(x,y):
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
    return [b0,b1]

def getRegression(x,y):
    b = makeRegression(x,y)
    return b[0] + (b[1] * x)

def getResid(x,y):
    return y - getRegression(x,y)

def makeScatterPlot(x,y,lineBool,xTitle,yTitle,groupBool): #explanatory and response must be column names
    if (groupBool):
        plt.scatter(x,y,1,c=sc['ownership'].apply(lambda x: colors[x]))
    else:
        plt.scatter(x,y,1,darkblue)
    if (lineBool):
        plt.plot(x, getRegression(x,y), c='#079799', aa=True)
    plt.xlabel(xTitle, size='smaller')
    plt.ylabel(yTitle, size='smaller')

# makeScatterPlot(sc[sc["ownership"] == 2]["costlog"],sc[sc["ownership"] == 2]["sqearningslog"],True,'Log of Cost of Attendance ($)','Log of Earnings Squared, 10 Years After Entry into Institution ($)',False)
# # makeScatterPlot(sc['costlog'],sc['earningslog'],True,'Log of Cost of Attendance ($)','Log of Earnings, 10 Years After Entry into Institution ($)',False)
#
# plt.title('Cost vs Earnings in US Higher Ed Institutions (Private For-profit)', size='smaller')
# plt.savefig('generated plots/test2.png', dpi=150, bbox_inches='tight')

def plotResid(x,y):
    plt.scatter(x,getResid(x,y),1,c=darkblue)
    plt.ylabel('Residuals')
    plt.savefig('generated plots/residuals.png', dpi=150, bbox_inches='tight')

plotResid(sc[sc["ownership"] == 2]["costlog"],sc[sc["ownership"] == 2]["earningslog"])
