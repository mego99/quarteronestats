"use strict";
const jf = require('jsonfile');
const h = require('https');

const file = 'data.json';
const url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=3hZTlIbHmdMRcRWJ3NxdG8AvQPoW4Mdbilkm13At&"
  + "school.operating=1&"
  + "_sort=2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings:desc&"
  + "_per_page=100&"
  + "_page=0&"
  + "2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings__range=0..&"
  + "2013.cost.attendance.academic_year__range=0..&"
  + "fields=school.name,2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings,2013.cost.attendance.academic_year,2013.admissions.admission_rate.overall,2013.admissions.sat_scores.average.overall,2013.aid.median_debt.number.overall";

h.get(url, res => {
  res.setEncoding('utf8');
  let body = "";
  res.on("data", data => {
    body += data;
  });
  res.on('end',(key,val) => {
    body = JSON.parse(body);
    body = body.results;

    jf.writeFile(file, body,
      function(err) {
        if (err) console.error(err);
      }
    );

    jf.readFile('data.json',function(err,data) {
      for (let i = 0; i<100; i++) {
        data[i]['school'] = data[i]['school.name'];
        delete data[i]['school.name'];
        data[i]['cost'] = data[i]['2013.cost.attendance.academic_year'];
        delete data[i]['2013.cost.attendance.academic_year'];
        data[i]['earnings'] = data[i]['2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings'];
        delete data[i]['2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings'];
        data[i]['admit'] = data[i]['2013.admissions.admission_rate.overall'];
        delete data[i]['2013.admissions.admission_rate.overall'];
        data[i]['act'] = data[i]['2013.admissions.sat_scores.average.overall'];
        delete data[i]['2013.admissions.sat_scores.average.overall'];
        data[i]['debt'] = data[i]['2013.aid.median_debt.number.overall'];
        delete data[i]['2013.aid.median_debt.number.overall']

      };
      for (let i=0;i<100;i++) {
        if(!data[i]) {
          data.splice(i,1);

          if (!(data[i]['cost']&&data[i]['earnings']&&data[i]['admit']&&data[i]['act']&&data[i]['debt'])) {
            console.log(data[i]);
            data.splice(i,1);
          }
        };
      }
      jf.writeFile(file, data,
        function(err) {
          if (err) console.error(err);
        }
      );
    })
  })
});
