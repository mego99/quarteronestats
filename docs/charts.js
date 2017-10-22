let firstScatter = {};

var w = ((Math.max(document.documentElement.clientWidth, window.innerWidth || 0)) * .6);
var h = 500;

firstScatter.svg = d3.select('#first-scatter')
    .attr('width',w+50)
    .attr('height',h+20);

d3.json('node_app/data.json',
(error, data) => {
  if (error) return console.error(error);
  console.log(data);

  firstScatter.x = d3.scaleLinear()
    .domain(d3.extent(data,(d)=>{return d.act}))
    .range([50,w]);

  firstScatter.y = d3.scaleLinear()
    .domain(d3.extent(data,(d)=>{return d.earnings}))
    .range([h,0]);

  firstScatter.xAxis = d3.axisBottom(firstScatter.x);

  firstScatter.yAxis = d3.axisLeft(firstScatter.y);


  gX = firstScatter.svg.append('g')
    .call(firstScatter.xAxis)
    .attr('transform','translate(0,' + h + ')');

  gY = firstScatter.svg.append('g')
    .call(firstScatter.yAxis)
    .attr('transform','translate(50,0)');

  gData = firstScatter.svg.append('g')
    .selectAll('circle')
        .data(data)
      .enter()
        .append('circle')
        .attr('transform',function(d) {
          let x = firstScatter.x(d.act);
          let y = firstScatter.y(d.earnings);
          return "translate(" + x + ',' + y + ")"
        })
        .attr('r',3);
})
