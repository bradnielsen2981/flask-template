//GAUGE CODE-----------------------------------------------------------
//Google Charts - Gauge
//The following code creates a 5 second recurring function once google charts has loaded

var recurringhandle = null;
google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(
    function()
    { 
        recurringhandle = setInterval(get_gauge_data, 2000); 
    } );

//The draw gauge code is called on the reture of the JSON function
function draw_gauge(result) {
    console.log(result);
    var options = {
        width: '100%', height: '100%',
        redFrom: 800, redTo: 1000,
        yellowFrom:500, yellowTo: 800,
        minorTicks: 5, max:1000
    };
    var data = google.visualization.arrayToDataTable([
        ['Label', 'Value'],
        ['Light', 300]
    ]);
    data.setValue(0, 1, result.light);

    var chart = new google.visualization.Gauge(document.getElementById('light_gauge_chart'));
    chart.draw(data, options);
}

//THis function is called every 5 seconds setInterval()
function get_gauge_data() {
    JSONrequest('/getlight','POST', draw_gauge); //Once data is received, send to draw
}

//----------------------------------------------------------