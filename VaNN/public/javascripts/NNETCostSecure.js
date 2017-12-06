createMap('/nnetTraining', "#nnet", 500, 400);


function createMap(urlData, eleDiv, w, h) {
    var margin = { top: 20, right: 100, bottom: 30, left: 40 },
        width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

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
        xAxis = d3.axisBottom(xScale);

    // setup y
    var yValue = function (d) {
        return d.y;
    }, // data -> value
        yScale = d3.scaleLinear().range([height, 0]), // value -> display      
        yAxis = d3.axisLeft(yScale);

    var line = d3.line()
        .curve(d3.curveBasis)
        .x(function (d) {
            return xScale(d.x);
        })
        .y(function (d) {
            return yScale(d.y);
        });

    // A area generator, for the dark stroke.
    var area = d3.svg.area()
        .interpolate("basis")
        .x(function (d) { return xScale(d.x); })
        .y1(function (d) { return yScale(d.y); });

    // add the graph canvas to the body of the webpage
    var lineChartNnet = d3.select(eleDiv).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");   

    // x-axis
    lineChartNnet.append("g")
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
    lineChartNnet.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("class", "label")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Y");

    var lineChartPath = lineChartNnet.append("g")
        .attr("class", "nnetg")

    getPositions();
    // load data
    function getPositions() {
        d3.interval(function () {
            d3.json(urlData, function (error, posData) {
                if ( posData.rcost!= undefined) {                    
                    updateMap(posData);                    
                }            
            });
        }, 1000);
    }

    var jdata = []

    function updateMap(data) {

        //update statistics
        d3.select(".statistics_nnet #maxIter").attr("value", data.maxiter)
        d3.select(".statistics_nnet #lambda").attr("value", data.lambdann)
        d3.select(".statistics_nnet #accExp").attr("value", data.accurExp)
        d3.select(".statistics_nnet #iterP").attr("value", data.iterp)
        d3.select(".statistics_nnet #iterS").attr("value", data.iters)
        d3.select(".trainingNN").html("")
        if (data.isTraining == "True") {
            d3.select(".trainingNN").html("Training Navigation...");
            $(".trainingNN").fadeOut(600);
            $(".trainingNN").fadeIn(600);
        }
        
        
        rcost = data.rcost;
        rsecure = data.rsecure;
        changeData(rcost, rsecure);
        // don't want dots overlapping axis, so add in buffer to data domain
        xScale.domain([0, jdata[0].val.length+100]);
        //yScale.domain([0, 1.0]);     
        minYScale = d3.min(jdata, function (c) { return d3.min(c.val, function (d) { return d.y; }); });
        maxYScale = d3.max(jdata, function (c) { return d3.max(c.val, function (d) { return d.y; }); });
        minYScale = parseFloat(minYScale)
        maxYScale = parseFloat(maxYScale)
        minYScale -= 0.01
        maxYScale += 0.01
        yScale.domain([minYScale,maxYScale]);

        lineChartNnet.select('.x.axis').transition().duration(500).call(xAxis);
        lineChartNnet.select(".y.axis").transition().duration(500).call(yAxis);       
              
            
        var linesC = lineChartPath.selectAll(".line")
            .data(jdata)
           
        var textline = lineChartPath.selectAll(".lineText")
            .data(jdata) 

        var areaC = lineChartPath.selectAll(".area")
            .data(jdata)

        area.y0(height)
            .y1(function (d) { return yScale(d.y); });

        linesC.exit()
            .transition()
            .duration(500)
            .remove()  
        textline.exit()
            .transition()
            .duration(500)
            .remove()   

        areaC.exit()
            .transition()
            .duration(500)
            .remove()    

        linesC.enter().append("path")
            .attr("class", "line")
            .attr("d", function (d) {
                return line(d.val);
            })
            .style("stroke", function (d) {
                return 2;
            })
        textline.enter().append("text")
            .datum(function (d) { return { id: d.id, val: [d.val[d.val.length - 1]] }; })
            .attr("class", "lineText")
            .attr("transform", function (d) {
                return "translate(" + xScale(d.val[0].x) + "," + yScale(d.val[0].y) + ")";
            })
            .attr("x", 3)
            .attr("dy", "0.35em")
            .style("font", "10px sans-serif")
            .text(function (d) { return d.id; });

        areaC.enter().insert("path", ".line").transition().duration(500)
            .attr("class", "area")
            .attr("transform", function (d) { return "translate(0," + (d.val[0].y * (h / 4 - 20)) + ")"; })
            .attr("d", function (d) { return area(d.val); })
            .style("fill", function (d, i) { return colores_google(4); })
            .style("fill-opacity", 1e-6);

        linesC.transition().duration(500)
            .attr("d", function (d) {
                return line(d.val);
            })
            .style("stroke", function (d) {
                return 3;
            })

        textline.datum(function (d) {
            return { id: d.id, val: [d.val[d.val.length - 1]] };
        })
        .attr("transform", function (d) {
            return "translate(" + xScale(d.val[0].x) + "," + yScale(d.val[0].y) + ")";
        })
            .text(function (d) {
                return d.id + ": " + (d.val[0].y)+ "%";
            });

        areaC.style("fill-opacity", .9)
            .attr("d", function (d) { return area(d.val); });  
    }   

    function changeData(rcost, resecure) {
        if (rcost != undefined) {
            // change string (from CSV) into number format              
            jdata = [{
                id: "secure",
                val: rsecure.map(function (d, i) {                    
                    return { x: i, y: (d*100).toFixed(3) };
                })
            }];
           // rcost.forEach(function (d, i) {
          //      jdata.push({ id: "cost", x: i, y: d });
          //  });
        } 
    }
   
    function colores_google(n) {
        var colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
        return colores_g[n % colores_g.length];
    }
}
