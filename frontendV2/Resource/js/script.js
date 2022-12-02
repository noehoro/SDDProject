function func(){
    document.getElementById("bg-model").style.display = "flex";
    // document.getElementsByTagName("body")[0].style.overflow = "hidden";
}

var cont = document.getElementById("bg-model");
cont.addEventListener("click",function(event){
    // console.log([...event.target.classList].indexOf('PT'));
    if([...event.target.classList].indexOf('PT') === -1){
        document.getElementById("bg-model").style.display = "none";
        // document.getElementsByTagName("body")[0].style.overflow = "visible";
    };
})


function redirectLogIn(){
    location.replace("managerLogin.html")
}

function redirectManager(){
    location.replace("management.html")
}

// This header will be used throughout the pages
let header = 
'<div id="header"> Laundry Management Tool</div><div id = "nav">' +
    '<div id = "option">' +
        '<div id = "" onclick=redirectManager() style="cursor: pointer;">MANAGE</div>' +
        '<div id = "about" onclick= redirectLogIn() style="cursor: pointer;">LOG IN</div>' +
    '</div>'+
'</div>'+
'<div id="mai_logo_container">'+
    '\<a href= \"/frontendV2\"> <img src="Resource/imgs/logo.PNG" id="mai_logo" ></a></div>'

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
$('#footer_container').append(footer);
$('#bg-model').append(bgModel);

