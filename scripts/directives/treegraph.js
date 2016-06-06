'use strict';

/**
 * @ngdoc directive
 * @name websiteApp.directive:treeGraph
 * @description
 * # treeGraph
 http://cloudspace.com/blog/2014/03/25/creating-d3.js-charts-using-angularjs-directives/#.VzLMnRUrLOQ
 */
 var call_once = true;
angular.module('websiteApp')
  .directive('treeGraph', [
  function () {
    return {
      restrict: 'E',
      scope: false,
      // scope: {
      //   data: '='
      // },
      link: function (scope, element) {
        // var margin = {top: 20, right: 20, bottom: 30, left: 40},
        //   width = 480 - margin.left - margin.right,
        //   height = 360 - margin.top - margin.bottom;

        // var x = d3.scale.ordinal().rangeRoundBands([0, width], .1);
        // var y = d3.scale.linear().range([height, 0]);

        // var xAxis = d3.svg.axis()
        //     .scale(x)
        //     .orient("bottom");

        // var yAxis = d3.svg.axis()
        //     .scale(y)
        //     .orient("left")
        //     .ticks(10);




      var margin = {top: 0, right: 0, bottom: 20, left: 80};

      // var width = 960 - margin.right - margin.left,
      //     height = 800 - margin.top - margin.bottom;

      var width = window.innerWidth,// - margin.right - margin.left,
          height = window.innerHeight// - margin.top - margin.bottom;

      var i = 0,
          duration = 750,
          root;

      var tree = d3.layout.tree()
          .size([height, width]);

      var diagonal = d3.svg.diagonal()
          .projection(function(d) { return [d.y, d.x]; });

      // var svg = d3.select(element[0]).append("svg")
      //     .attr("width",  '100%')//width + margin.right + margin.left)
      //     .attr("height", height + margin.top + margin.bottom)
      //   .append("g")
      //     .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      var svg = d3.select(element[0]).append("svg")
         .attr("width", width)//'100%')
        .attr("height", height)//'100%')
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        // .attr('viewBox','0 0 '+Math.min(width,height)+' '+Math.min(width,height))
        // .attr('preserveAspectRatio','xMinYMin')
        // .append("g")
        // .attr("transform", "translate(" + Math.min(width,height) / 2 + "," + Math.min(width,height) / 2 + ")");

        // Toggle children on click.
        function click(d) {
          if (d.children) {
            d._children = d.children;
            d.children = null;
          } else {
            d.children = d._children;
            d._children = null;
          }
          scope.update(d);
        }


        //Render graph based on 'data'
        scope.update = function(source) {
          console.log("called update")

          // Compute the new tree layout.
          var nodes = tree.nodes(root).reverse(),
              links = tree.links(nodes);

          // Normalize for fixed-depth.
          nodes.forEach(function(d) { d.y = d.depth * 180; });

          // Update the nodes…
          var node = svg.selectAll("g.node")
              .data(nodes, function(d) { return d.id || (d.id = ++i); });

          // Enter any new nodes at the parent's previous position.
          var nodeEnter = node.enter().append("g")
              .attr("class", "node")
              .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
              .on("click", click);

          nodeEnter.append("circle")
              .attr("r", 1e-6)
              .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

          nodeEnter.append("text")
              .attr("x", function(d) { return d.children || d._children ? -10 : 10; })
              .attr("dy", ".35em")
              .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
              .text(function(d) { return d.name; })
              .style("fill-opacity", 1e-6);

          // Transition nodes to their new position.
          var nodeUpdate = node.transition()
              .duration(duration)
              .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

          nodeUpdate.select("circle")
              .attr("r", 4.5)
              .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

          nodeUpdate.select("text")
              .style("fill-opacity", 1);

          // Transition exiting nodes to the parent's new position.
          var nodeExit = node.exit().transition()
              .duration(duration)
              .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
              .remove();

          nodeExit.select("circle")
              .attr("r", 1e-6);

          nodeExit.select("text")
              .style("fill-opacity", 1e-6);

          // Update the links…
          var link = svg.selectAll("path.link")
              .data(links, function(d) { return d.target.id; });

          // Enter any new links at the parent's previous position.
          link.enter().insert("path", "g")
              .attr("class", "link")
              .attr("d", function(d) {
                var o = {x: source.x0, y: source.y0};
                return diagonal({source: o, target: o});
              });

          // Transition links to their new position.
          link.transition()
              .duration(duration)
              .attr("d", diagonal);

          // Transition exiting nodes to the parent's new position.
          link.exit().transition()
              .duration(duration)
              .attr("d", function(d) {
                var o = {x: source.x, y: source.y};
                return diagonal({source: o, target: o});
              })
              .remove();

          // Stash the old positions for transition.
          nodes.forEach(function(d) {
            d.x0 = d.x;
            d.y0 = d.y;
          });
        }

         //Watch 'data' and run scope.render(newVal) whenever it changes
         //Use true for 'objectEquality' property so comparisons are done on equality and not reference
          scope.$watch('scope.tab', function(){


              root = scope.tab.content
              console.log("treegraph: " + root)
              if (root == undefined || !root.hasOwnProperty("name")) {
                console.log("treegraph: Error rendering tree root")
                return;
              }

              root['x0'] = height / 2;
              root.y0 = 0;

              function collapse(d) {
                if (d.children) {
                  d._children = d.children;
                  d._children.forEach(collapse);
                  d.children = null;
                }
              }

              root.children.forEach(collapse);
              scope.update(root);
              // scope.render(scope.data);
              call_once = false;
            
          }, false);  
        }
    };
  }
]);
