createMap('/nnetTraining', "#nnet", 400, 400);


function createMap(urlData, eleDiv, w, h) {
    var margin = { top: 20, right: 20, bottom: 30, left: 40 },
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

    getPositions();
    // load data
    function getPositions() {
        d3.interval(function () {
            d3.json(urlData, function (error, posData) {
               // if (posData.isTraining) {                    
                    updateMap(posData);                    
              //  }            
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
        rcost = data.rcost;
        rsecure = data.rsecure;     
        changeData(rcost, rsecure);    
        // don't want dots overlapping axis, so add in buffer to data domain
        xScale.domain([0,data.maxiter]);
        yScale.domain([
            d3.min(jdata, function (c) { return d3.min(c.val, function (d) { return d.y; }); }),
            d3.max(jdata, function (c) { return d3.max(c.val, function (d) { return d.y; }); })
        ]);

        lineChartNnet.select('.x.axis').transition().duration(500).call(xAxis);
        lineChartNnet.select(".y.axis").transition().duration(500).call(yAxis)

    
        // draw dots
        var linesC = lineChartNnet.selectAll(".nnetg")
            .data(jdata)  
            .enter().append("g")
            .attr("class", "nnetg")         

        linesC.exit()
            .transition()
            .duration(500)            
            .remove()       

        linesC.append("path")
            .attr("class", "line")
            .attr("d", function (d) {
                return line(d.val);
            })         
            .style("stroke", function (d) {
                return 2;
            })

        linesC.append("text")
            .datum(function (d) { return { id: d.id, val: [d.val[d.val.length - 1]] }; })
            .attr("class", "lineText")
            .attr("transform", function (d) {
                return "translate(" + xScale(d.val[0].x) + "," + yScale(d.val[0].y) + ")";
            })
            .attr("x", 3)
            .attr("dy", "0.35em")
            .style("font", "10px sans-serif")
            .text(function (d) { return d.id; });

        linesC.selectAll(".line").transition().duration(700)           
            .attr("d", function (d) {
                return line(d.val);
            })           
            .style("stroke", function (d) {
                return 2;
            })
        linesC.selectAll(".lineText")
            .datum(function (d) {
                return { id: d.id, val: [d.val[d.val.length - 1]]};
            })
            .attr("transform", function (d) {
                return "translate(" + xScale(d.val[0].x) + "," + yScale(d.val[0].y) + ")";
            })
            .text(function (d) { return d.id; });

    }   

    function changeData(rcost, resecure) {
        if (rcost != undefined) {
            // change string (from CSV) into number format              
            jdata = [{
                id: "secure",
                val: rsecure.map(function (d, i) {
                    i=i+1
                    return { x: i, y: d };
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