alert("brickpiloadedhandler loaded");

function hideelement(element)
{
    mblock= document.getElementById(element);
    mblock.style.visibility = "hidden";
}

function showelement(element)
{
    mblock= document.getElementById(element);
    mblock.style.visibility = "visible";
}

function setelement(element, message)
{
    mblock = document.getElementById(element);
    mblock.innerHTML = message;
}

//loaded handler
function brickpiloadedhandler(results)
{
    //load button is hidden prior
    console.log(results.message);
    setelement("jsonmessage", results.message);
    showelement("jsonmessage");
    showelement("dashboard");
}

//shutdown handler
function brickpishutdownhandler(results)
{
    //dashboard is hidden prior
    console.log(results.message);
    setelement("jsonmessage", results.message);
    showelement("loadbutton");
}

//hide or show dashboard
if (robotenabled) {
    hideelement("loadbutton");
    showelement("dashboard");
} else {
    hideelement("dashboard");
    showelement("loadbutton"); 
}


