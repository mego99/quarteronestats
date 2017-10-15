import pandas as pd
from pandas.io.json import json_normalize as jn
import requests
import json
import math
import matplotlib.pyplot as plt

# sc = pd.read_csv('Scorecard.csv')
# sc.head(1)
#
# print(sc.info)

url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=3hZTlIbHmdMRcRWJ3NxdG8AvQPoW4Mdbilkm13At&school.operating=1&_sort=2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings:desc&_per_page=1&_page= %s &2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings__range=0..&2013.cost.attendance.academic_year__range=0..&fields=school.name"%(0)
print("retrieving data count...")
j = json.loads(requests.get(url).text)
count = int(math.ceil(j["metadata"]["total"]/100))

sc = []
for x in range(0,count):
    url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=3hZTlIbHmdMRcRWJ3NxdG8AvQPoW4Mdbilkm13At&school.operating=1&_sort=2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings:desc&_per_page=100&_page= %s &2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings__range=0..&2013.cost.attendance.academic_year__range=0..&fields=school.name,2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings,2013.cost.attendance.academic_year,2013.admissions.admission_rate.overall,2013.admissions.sat_scores.average.overall,2013.aid.median_debt.number.overall,2013.student.retention_rate.four_year.full_time"%(x)
    print("retrieving data points %s to %s..."%(x*100,(x*100)+100))
    j = json.loads(requests.get(url).text)
    df = jn(j,"results")
    sc.append(df)

sc = pd.concat(sc, axis=0)
print("reassigning index...")
sc.reset_index(inplace=True)
sc.to_pickle("data.pkl")
print("saved to file!")
