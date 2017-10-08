"use strict";
const jf = require('jsonfile');
const h = require('https');

const file = 'data.json';
const url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=3hZTlIbHmdMRcRWJ3NxdG8AvQPoW4Mdbilkm13At&"
  + "school.operating=1&"
  + "_sort=2013.cost.attendance.academic_year:desc&"
  + "_per_page=100&"
  + "fields=school.name,2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings,2013.cost.attendance.academic_year,2013.admissions.admission_rate.overall";

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
      }
      jf.writeFile(file, data,
        function(err) {
          if (err) console.error(err);
        }
      );
    })
  })
});
