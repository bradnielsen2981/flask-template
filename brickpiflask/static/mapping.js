
//Initialise Turtle
var brd = JXG.JSXGraph.initBoard('box',{boundingbox: [-250, 250, 250, -250]});
var turtle = brd.create('turtle',[0, 0], {strokeOpacity:0.5});
turtle.setPenSize(3);

function rotateturtle(results)
{
    console.log(results);
    turtle.rt(results.rotated);
    //set the heading degrees
    //turtle.lookTo()
}

//function recieves the JSON back from AJAZ request
function forwardturtle(results)
{
    console.log(results);
    turtle.forward(results.elapsed*20);
}


