alert("brickpiloadedhandler loaded")

function showdashboard()
{
    mblock = document.getElementById('dashboard');
    mblock.style.visibility = "visible";
    mbutton= document.getElementById('loadbrickpibutton');
    mbutton.style.visibility = "hidden";
}

function hidedashboard()
{
    mblock = document.getElementById('dashboard');
    mblock.style.visibility = "hidden"; 
    mbutton= document.getElementById('loadbrickpibutton');
    mbutton.style.visibility = "visible";
}

function brickpiloadedhandler(results)
{
    console.log(results.message);
    mblock = document.getElementById('jsonmessage');
    mblock.style.visibility = "visible";
    mblock.innerHTML = results.message;

    //need to test the robot loaded properly before the following
    showdashboard();
}

//hide or show dashboard
if (robotenabled) {
    showdashboard();
} else {
    hidedashboard();
}

//need a good loading bar as well
