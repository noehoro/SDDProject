function func1(){
    location.replace("managerLogin.html")
}

// This header will be used throughout the pages
let header = 
'<div id="header"> Laundry Management Tool</div><div id = "nav">' +
    '<div id = "option">' +
        '<div id = "" onclick=func() style="cursor: pointer;">MACHINES</div>' +
        '<div id = "about" onclick= func1() style="cursor: pointer;">LOG IN</div>' +
    '</div>'+
'</div>'+
'<div id="mai_logo_container">'+
    '<img src="Resource/imgs/logo.PNG" id="mai_logo" ></div>'

// This footer will be used throughout the pages
let footer =  
'<footer id = "footer">' +
    '<div class="footer-content">'+
        '<h3>Laundry Management Tool</h3>' +
        '<div id ="term" onclick = "func()">Terms and Privacy</div>' +
        '<ul class="socials">' +
            '<li><a href="https://github.com/noehoro/SDDProject"><i class="fa fa-github"></i></a></li>' +
        '</ul>' +
    '</div>'+
    '<div class="footer-bottom">' +
    '    <p>copyright &copy;2022. designed by <span>Laundry master</span></p>' +
    '</div>'+
'</footer>';


// This bg-model will be used throughout the pages
let bgModel =         
'<div id ="model-content" class = "PT">'+
'<h1 class = "PT">Privacy Policy</h1>'+
'    <h2 class = "PT">Personal Data Collection</h2>'+
'        <h4 class = "PT">The site does not read or collect file content, metadata, or other data from your uploaded files.</h4>'+
'    <h2 class = "PT">Use of Your Personal Data</h2>'+
'        <h4 class = "PT">The site does not collect any personal data.</h4>'+
'    <h2 class = "PT">Handling of Your Files</h2>'+
'        <h4 class = "PT">The files will exist momentarily in the server to retrieve the power information. As soon as that is finished, all files will be <b>DELETED</b>.</h4>'+
'    <h2 class = "PT">Cookies</h2>'+
'        <h4 class = "PT">The site does not collect any cookie</h4>'+
'<h1 class = "PT">Term of Service</h1>'+
'    <h2 class = "PT">Allowed Usage</h2>'+
'        <h4 class = "PT">This service offers functionality to analyze power data from multiple .fit files. This service is provided through web interface. You agree to comply with the policies and limitations concerning the use of the Mai\'s Power Meter Comparison Tool. </h4>'+
'        <h4 class = "PT">You agree to not reverse-compile or decompile, analyze, reverse-engineer, reverse-assemble or disassemble, unlock or otherwise attempt to discover the source code '+
'            or underlying algorithms of Mai\'s Power Meter Comparison Tool or attempt to do any of the foregoing in relation to the Mai\'s Power Meter Comparison Tool service.</h4>'+
'    <h2 class = "PT">Copyright Policy</h2>'+
'        <h4 class = "PT">You are responsible only for the data (e.g., files, URLs) that you send to the Mai\'s Power Meter Comparison Tool service. Mai\'s Power Meter Comparison Tool does not monitor customer content. Please remember that illicit exchanges of recordings and protected works and hacking harm artistic creation. And please respect the laws in force, especially those concerning intellectual and artistic property.</h4>'+
'</div>'+

$('#header_container').append(header);
console.log("here");
$('#footer_container').append(footer);
$('#bg-model').append(bgModel);

// ---------------------------------------------------------------------------------------------
// Animation for status bar
function increase(perc) {
    //change status bar fill percentage
    let bars = document.getElementsByClassName("bar");
    for(let i = 0; i < bars.length; i++){
        bars[i].style.setProperty('--m',perc[i].toString()+"%");
    }
    
    // Change the variable to modify the speed of the number increasing from 0 to (ms)
    let SPEED = 30;
    // Retrieve the percentage value
    let limitList = [];
    let barList = document.getElementsByClassName("value1");
    for(let i = 0; i < barList.length; i++){
        barList[i].innerHTML = perc[i];
        parseInt(limitList.push(barList[i].innerHTML),10);
    }

    for(let j = 0; j < limitList.length; j++){
        for(let i = 0; i <= limitList[j]; i++) {
            setTimeout(function () {
                document.getElementsByClassName("value1")[j].innerHTML = i + "%";
            }, SPEED * i);
        }
    }
}

increase([7,78,8]);