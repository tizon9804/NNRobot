var margin = { top: 20, right: 20, bottom: 30, left: 40 },
    width = 500 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

/* 
 * value accessor - returns the value to encode for a given data object.
 * scale - maps value to a visual display encoding, such as a pixel position.
 * map function - maps from data value to display value
 * axis - sets up axis
 */

// setup x 
var xValue = function (d) {
    return d.x;
}, // data -> value
    xScale = d3.scaleLinear().range([0, width]), // value -> display
    xMap = function (d) { return xScale(xValue(d)); }, // data -> display
    xAxis = d3.axisBottom(xScale);

// setup y
var yValue = function (d) {
    return d.y;
}, // data -> value
    yScale = d3.scaleLinear().range([height, 0]), // value -> display
    yMap = function (d) { return yScale(yValue(d)); }, // data -> display
    yAxis = d3.axisLeft(yScale);

// setup fill color
var cValue = function (d) { return "("+d.x+","+d.y+")"; }
var color = d3.scale.linear()
    .domain([0, width / 4, width / 4 * 2, width / 4 * 3, width])
    .range(["#fb000f", "#6e00fb", "#00fbec", "#8dfb00", "#fb3c00"])
    .interpolate(d3.interpolateHsl); 

// add the graph canvas to the body of the webpage
var map = d3.select("#map").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// add the tooltip area to the webpage
var tooltip = d3.select("#map").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// x-axis
map.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .append("text")
    .attr("class", "label")
    .attr("x", width)
    .attr("y", -6)
    .style("text-anchor", "end")
    .text("X");

// y-axis
map.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("class", "label")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("Y");

getPositions();
// load data
function getPositions() {   
    d3.interval(function () {
        d3.json("/positionStream", function (error, posData) {
            if (posData.buffer.length > 0) {
                updateMap(posData);
            }
            //getPositions();
        });
    }, 500);
}
var jdata = []
var isadd = 0
function updateMap(data) {

    // change string (from CSV) into number format   
    data.buffer.forEach(function (d) {
        var json = JSON.stringify(eval("(" + d + ")"));
        var object = JSON.parse(json)   
        if (jdata.length > 5000) {
            jdata.splice(0, 500);;
        }
        if (object.range < 4900 && isadd==0) {
            jdata.push(object)
        }
        if (isadd>40) {
            isadd = 0
        }
        else {
            isadd++
        }

    });

    // don't want dots overlapping axis, so add in buffer to data domain
    xScale.domain([d3.min(jdata, xValue) - 1, d3.max(jdata, xValue) + 1]);
    yScale.domain([d3.min(jdata, yValue) - 1, d3.max(jdata, yValue) + 1]);

    map.select('.x.axis').transition().duration(200).call(xAxis);
    map.select(".y.axis").transition().duration(200).call(yAxis)


    // draw dots
    var dots = map.selectAll(".dot")
        .data(jdata)
        .on("mouseover", function (d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            tooltip.html( "Positions  <br/> (" + xValue(d)
                + ", " + yValue(d) + ")")
                .style("left", (d3v3.event.pageX + 5) + "px")
                .style("top", (d3v3.event.pageY - 28) + "px");
        })
        .on("mouseout", function (d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        });  

    dots.exit()
        .transition()
        .duration(100)
        .style("opacity","0.1")
        .remove()

    dots.enter().append("circle")
        .attr("class", "dot")
        .attr("r", 2.5)
        .attr("cx", xMap)        
        .attr("cy", yMap)
        .style("fill", function (d) { return d3.rgb(color((((d.range / 4000) % 20) * 38) + 10)).darker(Math.floor((d.range / 4000) / 20) * (1 / 4)).toString();})
        .transition()
        .duration(500)
        .style("opacity", function (d, i) { return (i / 2000) })

    dots.transition().duration(100)
        .attr("cx", xMap)
        .attr("cy", yMap)
        .style("opacity", function (d,i) { return (i/ 2000) })
        .style("fill", function (d) { return d3.rgb(color((((d.range) % 20) * 38) + 10)).darker(Math.floor((d.range) / 20) * (1 / 4)).toString();})
        

}