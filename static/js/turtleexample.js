/* ------------------------------------------------------------------------
- A Custom JS File - can use other libraries pre-imported in this template e.g
- Bootstrap, JQuery, AJAX, JSXGraph - https://jsxgraph.uni-bayreuth.de/wp/about/index.html
- Google Charts
- the jsonrequesthandler file in this folder can also be used to make simple requests
--------------------------------------------------------------------------*/
// TURTLE EXAMPLE
var brd = JXG.JSXGraph.initBoard('box',{boundingbox: [-250, 250, 250, -250]});
var t = brd.create('turtle',[0, 0], {strokeOpacity:0.5});
t.setPenSize(3);
t.right(90);
var alpha = 0;
 
function run() {
   t.forward(2);
   if (Math.floor(alpha / 360) % 2 === 0) {
      t.left(1);        // turn left by 1 degree
   } else {
      t.right(1);       // turn right by 1 degree
   }

   alpha += 1;
   
   if (alpha < 1440) {  // stop after two rounds
       setTimeout(run, 20); 
   }
}

run();
