/* ---JSON EXAMPLE OF SENDING MORE THAN ONE VARIABLE------------ */
function findhypotenuse()
{
    var sideA = document.getElementById('sideA').value;
    var sideB = document.getElementById('sideB').value;
    var paramobject = {};
    paramobject.sideA = sideA;
    paramobject.sideB = sideB;
    JSONrequest('/trighandler', 'POST', receivehypotenuse, paramobject);
}
//callback function that receives the JSON, the dictionary keys become variables
function receivehypotenuse(result) 
{
    document.getElementById('sideC').value = result.hypotenuse;
}

/*---JSON RECURRING PING OF THE SERVER DEMO---------------------*/
var recurringhandle = null; //A handle to the recurring function
recurringhandle = setInterval(getactiveusers, 5000); //start pinging the server
function getactiveusers()
{
    JSONrequest('/getactiveusers', 'POST', receiveactiveusers);
}
//callback function
function receiveactiveusers(result)
{
    document.getElementById("activeuserlist").innerHTML = "";
    result.activeusers.forEach(displayuser);
}
function displayuser(user) {
  document.getElementById("activeuserlist").innerHTML += "<li>" + user + "</li>";
}

//---JSON EXAMPLF OF AN EXTERNAL API-----------------------------------
//read hero names from superhero api
function gethero()
{
    apikey = "10158457047547165"
    heroname = document.getElementById("heroname").value;
    proxy = "https://cors-anywhere.herokuapp.com/"; //annoying way of bypassing cross domain scripting errors
    url = proxy + "https://superheroapi.com/api/" + apikey + "/search/" + heroname;
    JSONrequest(url, 'GET', superheroapi, null, "json", true);
}
//callback function to receive results
function superheroapi(result)
{
    document.getElementById("hero").innerHTML = "";
    console.log(result.results);
    if (result.results)
    {
        result.results.forEach(displayhero);
    }
}
function displayhero(hero)
{
    document.getElementById("hero").innerHTML += `<p>,<h3>${hero.name}</h3><br/><image src=${hero.image.url} /></p>`;
    document.getElementById("jsonmessage").innerHTML = `<h3>Result Object</h3><p>${JSON.stringify(hero)}</p>`;
    document.getElementById("jsonmessage").style.visibility = "visible";
}
