
var width = 300,
    height = 300,
    radius = Math.min(width, height) / 2 - 30;

var r = d3.scaleLinear()
    .domain([0, 5000.1])
    .range([0, radius]);

var line = d3.radialLine()
    .curve(d3.curveLinearClosed)
    .radius(function (d) {
        return r(d);
    })
    .angle(function (d, i) {

        return (i * Math.PI) / 180;
    });

var svg = d3.select("#Laser").append("svg")
    .attr("width", width)
    .attr("height", height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var gr = svg.append("g")
    .attr("class", "r axis")
    .selectAll("g")
    .data(r.ticks(5).slice(1))
    .enter().append("g");

gr.append("circle")
    .attr("r", r);

gr.append("text")
    .attr("y", function (d) { return -r(d) - 4; })
    .attr("transform", "rotate(15)")
    .style("text-anchor", "middle")
    .text(function (d) { return d; });

var ga = svg.append("g")
    .attr("class", "a axis")
    .selectAll("g")
    .data(d3.range(-90,270, 30))
    .enter().append("g")
    .attr("transform", function (d) { return "rotate(" + -(d+90) + ")"; });

ga.append("line")
    .attr("x2", radius);

ga.append("text")
    .attr("x", radius + 6)
    .attr("dy", ".35em")
    .style("text-anchor", function (d) { return d < 180 && d > 0 ? "end" : null; })
    .attr("transform", function (d) { return d < 180 && d > 0 ? "rotate(180 " + (radius + 6) + ",0)" : null; })
    .text(function (d) { return d + "°"; });

var laser = svg.append("path")

getLaser();

function getLaser() {    
    d3.interval(function () {
        d3.json("/laserstream", function (error, laserData) {    
            if (laserData.buffer != undefined) {
                if (laserData.buffer.length > 0) {
                    update(laserData);
                }
            }
        });
    }, 500);
}

function update(data) {     

    var laserchange = svg.selectAll("path")        
        .datum(data.buffer)
        .attr("class", "line")       
        .attr("d", line); 
}