createNavPred('/predNav', "#predNav", 700, 200);

function createNavPred(urlData, eleDiv, w, h) {
     var margin = { top: 5, right: 100, bottom: 10, left: 40 },
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
        .x(function (d,i) {
            return xScale(i);
        })
        .y(function (d) {
            return yScale(d.y);
        });

    // A area generator, for the dark stroke.
    var area = d3.svg.area()
        .interpolate("basis")
        .x(function(d,i) { return xScale(i); })
        .y1(function(d) { return yScale(d.y); });

    // add the graph canvas to the body of the webpage
    var lineChartNnet = d3.select(eleDiv).append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");    

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
        .attr("class", "navpredvis")

    getPositions();
    // load data
    function getPositions() {
        d3.interval(function () {
            d3.json(urlData, function (error, posData) {
               // if (posData.isTraining) {                    
                    overlappingArea(posData);                    
              //  }            
            });
        }, 200);
    }

    var jdata = []

    function overlappingArea(posdata) {  
        d3.select(".predNavH2").html(posdata.predNav);
        $(".predNavH2").fadeOut(600);
        $(".predNavH2").fadeIn(600);     
        changeData(posdata);
        xScale.domain([0, 1000]);        
        yScale.domain([0,100]);   
        lineChartNnet.select(".y.axis").transition().duration(500).call(yAxis);               
            
        var linesC = lineChartPath.selectAll(".line")
            .data(jdata)
        var areaC = lineChartPath.selectAll(".area")
            .data(jdata)

      area.y0(height)
      .y1(function(d) { return yScale(d.y); });
           
        var textline = lineChartPath.selectAll(".lineText")
            .data(jdata)       

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

        linesC.enter().append("path").transition().duration(500)
            .attr("class", "line")
            .attr("d", function (d) {
                return line(d.val);
            })
            .style("stroke", function (d) {
                return 2;
            })

        textline.enter().append("text")
            .datum(function (d) { return { id: posdata.predNav,x: d.val.length, val: [d.val[d.val.length - 1]] }; })
            .attr("class", "lineText")
            .attr("transform", function (d,i) {
                return "translate(" + xScale(d.x) + "," + yScale(d.val[0].y) + ")";
            })
            .attr("x", 3)
            .attr("dy", "0.35em")
            .style("font", "10px sans-serif")
            .text(function (d) { return posdata.predNav; });

         areaC.enter().insert("path", ".line").transition().duration(500)
                .attr("class", "area")
                .attr("transform", function(d) { return "translate(0," + (d.val[0].y * (h / 4 - 20)) + ")"; })
                .attr("d", function(d){return area(d.val);})
                .style("fill", function(d,i) { return colores_google(d.c); })
                .style("fill-opacity", 1e-6);

        linesC.transition().duration(500)
            .attr("d", function (d) {
                return line(d.val);
            })
            .style("stroke", function (d) {
                return 3;
            })

        textline.datum(function (d) {
                return { id: posdata.predNav,x: d.val.length, val: [d.val[d.val.length - 1]] };
            })
            .attr("transform", function (d,i) {
                return "translate(" + xScale(d.x) + "," + yScale(d.val[0].y) + ")";
            })
            .text(function (d) {
                if (d.val[0].y > 0) {
                    return (d.val[0].y) + "%";
                }
                return "";
            });       

        areaC.style("fill-opacity", .9)
            .attr("d", function(d) { return area(d.val); });   
    
    }
   var valu=[]
   valu.push({ x: 0, y: 0 })
   var valuB = []
   valuB.push({ x: 0, y: 0 })
   function changeData(data) {
        if (data != undefined) {
            // change string (from CSV) into number format    
            if (data.predNav == "Is a good Direction") {
                valu.push({ x: 1, y: (data.probNav * 100).toFixed(3) })
                valuB.push({ x: 2, y: 0 })
            }
            else {
                valu.push({ x: 1, y: 0 })
                valuB.push({ x: 2, y: (data.probNav * 100).toFixed(3) })
            }
           if (valu.length>1000){
               valu.splice(0, 1);
               valuB.splice(0, 1);
            }            
           jdata = [{
               id: "nav",
               c:3,
               val: valu               
           }, {
                id: "navB",
                c:1,
                val: valuB   
               }];         
        } 
    }
   
    function colores_google(n) {
        var colores_g = ["#3366cc", "#dc3912", "#ff9900", "#109618", "#990099", "#0099c6", "#dd4477", "#66aa00", "#b82e2e", "#316395", "#994499", "#22aa99", "#aaaa11", "#6633cc", "#e67300", "#8b0707", "#651067", "#329262", "#5574a6", "#3b3eac"];
        return colores_g[n % colores_g.length];
    }
}