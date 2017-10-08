const jf = require('jsonfile');
const h = require('https');

const file = 'data.json';
const url = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=3hZTlIbHmdMRcRWJ3NxdG8AvQPoW4Mdbilkm13At&"
  + "school.operating=1&"
  + "_sort=2013.cost.attendance.academic_year:desc&"
  + "_per_page=100&"
  + "fields=school.name,2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings,2013.cost.attendance.academic_year";

h.get(url, res => {
  res.setEncoding('utf8');
  let body = "";
  res.on("data", data => {
    body += data;
  });
  res.on('end',(key,val) => {
    body = JSON.parse(body);
    jf.writeFile(file, body,
      {replacer: ['results','school.name','2013.cost.attendance.academic_year','2013.earnings.10_yrs_after_entry.working_not_enrolled.mean_earnings']},
      function(err) {
        if (err) console.error(err);
      }
    )
  })
});
