        
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



        // ---------------------------------------------------------------------------------------------
        function show_create_option(){
            document.querySelectorAll(".createMachineType").forEach(div => {
                let currentDisplay = getComputedStyle(div).getPropertyValue('display');
                if(currentDisplay == "flex"){div.style.display = "none";}
                if(currentDisplay == "none"){div.style.display = "flex";}
            })

            document.querySelectorAll(".createWashMachineTimeContainer").forEach(div => {
                let currentDisplay = getComputedStyle(div).getPropertyValue('display');
                if(currentDisplay == "flex"){div.style.display = "none";}
            })

        }

        // ---------------------------------------------------------------------------------------------
        function has_logged_in(){
            $.ajax({
                type: "GET",
                url:"http://127.0.0.1:5000/loggedin",
                success:function(msg){
                    console.log(msg);
                }
            })
        }
        
        // ---------------------------------------------------------------------------------------------
        function show_time(ele){
            
            //reset all color to white
            document.querySelectorAll(".createButton").forEach(div => {
                div.style.color = "white";
            })
            
            //set selected color to different color
            ele.style.color = "#b7e1cc";

            //reset all time button
            document.querySelectorAll(".createWashMachineTimeContainer").forEach(div => {
                div.style.display = "none";
            })

            //display selected time options
            document.getElementById(ele.id + "Time").style.display = "flex";
        }
        
        // ---------------------------------------------------------------------------------------------
        document.querySelectorAll(".createWashMachineTimeContainer").forEach(div => {
            div.addEventListener("click",function(event){
                let typeOfMachine = event.target.parentNode.getAttribute("data-type"); //e.g. wash dry other
                let time = event.target.innerHTML.slice(0,-3); //e.g. 15 30 45... 

                new_machine_helper(typeOfMachine,time);
            })
        })

        // ---------------------------------------------------------------------------------------------
        function new_machine_helper(type,time){
            $.ajax({
                type: "GET",
                url:"http://127.0.0.1:5000/getsite",
                success:function(msg){
                    var site = msg["site"]; 

                    new_machine(site,type,time)
                }
            })
        }

        // ---------------------------------------------------------------------------------------------
        function get_machine_helper(){
            $.ajax({
                type: "GET",
                url:"http://127.0.0.1:5000/getsite",
                success:function(msg){
                    var site = msg["site"]; 
                    console.log(site);
                    get_machines(site);

                }
            })
        }

        // ---------------------------------------------------------------------------------------------
        function addmachineToHtml(type, status){



            console.log(status);
            if (type == 1) {type = "wash"};
            if (type == 2) {type = "dry"};
            if (type == 3) {type = "other"};

            if (status == "0") {status = "Ava"}
            else if (status == "-1") {status = "Broken"}
            else{
                status = "UnAva";
            }
            // if (status != "0") {status = "UnAva"};

            let domId = type + status +"Sec";

            console.log(domId);
            
            if(status === "Broken"){
                domId = type + "UnAvaSec";
                console.log(domId);
                $("#"+ domId).append('<div class="imgContainer hoverAva">' +
                                '<img src="Resource/imgs/LM.svg" class="lm">'+
                                '<div class="middle">' +
                                    '<div class="text">broken</div>' +
                                '</div>' +
                            '</div>');
            }
            else{
                $("#"+ domId).append('<div class="imgContainer hoverAva">' +
                                    '<img src="Resource/imgs/LM.svg" class="lm">'+
                                    '<div class="middle">' +
                                        '<div class="text">avalible</div>' +
                                    '</div>' +
                                '</div>');
            }

            



        }

        // ---------------------------------------------------------------------------------------------
        // when hover over machine, show how much time is left
        // list = [w,d,o],  each represents an array of machine, 0 is ava, any number above 0 means time left in seconds 

        function add_hover(list){
            // let washUnava = list[0].filter(e => e!==0);
            // let dryUnava = list[1].filter(e => e!==0);
            // let otherUnava = list[2].filter(e => e!==0);
            console.log(list);
            for(let i = 0; i < list.length; i++){
                let Unava = list[i].filter(e => e!==0);

                for(let j = 0; j < Unava.length; j++){
                    if(Unava[j] == -1){continue;}
                    document.getElementsByClassName("unavaSection")[i].children[j].children[1].innerHTML = Unava[j];
                }
            }
            
        }

        // ---------------------------------------------------------------------------------------------
        function get_machines(site){
            let washStatus = [];
            let dryStatus = [];
            let otherStatus = [];

            let url = "http://127.0.0.1:5000/dashboard?site=" + site;
            $.ajax({
                type: "POST",
                url:"http://127.0.0.1:5000/dashboard?site=" + site,
                success:function(msg){
                    for( i in msg){
                        if(i == "site"){continue;}
                        let machineId = i;
                        let status = msg[i];
                        let machineType = String(machineId)[0]; //if the first digit is a 1, it is a washer, if it is a 2, it is a drier, if it is a 3
                        
                        if(machineType == "1" && status == 0){washStatus.push(0)};
                        if(machineType == "1" && status >= 0){washStatus.push(parseInt(status))};
                        if(machineType == "1" && status == -1){washStatus.push(-1)}
                        if(machineType == "2" && status == 0){dryStatus.push(0)};
                        if(machineType == "2" && status >= 0){dryStatus.push(parseInt(status))};
                        if(machineType == "2" && status == -1){dryStatus.push(-1)}
                        if(machineType == "3" && status == 0){otherStatus.push(0)};
                        if(machineType == "3" && status >= 0){otherStatus.push(parseInt(status))};
                        if(machineType == "3" && status == -1){otherStatus.push(-1)}

                        addmachineToHtml(machineType,status);
                    }
                    
                    //add hover effect
                    add_hover([washStatus,dryStatus,otherStatus]);

                    // render status bar
                    let washPerc = washStatus.filter(x => x === 0).length/washStatus.length*100;
                    let dryPerc = dryStatus.filter(x => x === 0).length/dryStatus.length*100;
                    let otherPerc = otherStatus.filter(x => x === 0).length/otherStatus.length*100;
                    
                    // if there is no machine in the system, washPerc/dryPerc/otherPerc would return NaN, if so set the number to 0
                    if(isNaN(washPerc)){washPerc = 0;}
                    if(isNaN(dryPerc)){dryPerc = 0;}
                    if(isNaN(otherPerc)){otherPerc = 0;}

                    increase([washPerc,dryPerc,otherPerc]);
                }
            })
        }

        // ---------------------------------------------------------------------------------------------
        function new_machine(site,type,time){
            console.log("http://127.0.0.1:5000/new-machine?time=" + time*60 + "&site="+ site+"&type=" + type);
            
            $.ajax({
                type: "POST",
                url:"http://127.0.0.1:5000/new-machine?time=" + time*60 + "&site="+ site+"&type=" + type,
                success:function(msg){
                    window.open("http://127.0.0.1:5500/backend/" + msg, '_blank').focus();
                }
            })
        }

        get_machine_helper();

        //honest attemp to convert to more readable time format
        // // ---------------------------------------------------------------------------------------------
        // // second to actual time
        // function fancyTimeFormat(duration)
        // {   
        //     // Hours, minutes and seconds
        //     var hrs = ~~(duration / 3600);
        //     var mins = ~~((duration % 3600) / 60);
        //     var secs = ~~duration % 60;

        //     // Output like "1:01" or "4:03:59" or "123:03:59"
        //     var ret = "";

        //     if (hrs > 0) {
        //         ret += "" + hrs + ":" + (mins < 10 ? "0" : "");
        //     }

        //     ret += "" + mins + ":" + (secs < 10 ? "0" : "");
        //     ret += "" + secs;
        //     return ret;
        // }

        // // ---------------------------------------------------------------------------------------------
        // // reduce timer
        // let unAvaArray = [];
        // $(".middle").each(function() {
        //     // console.log($(this).text());
        //     if($(this).text() === "avalible"){;}
        //     else{
        //         var newValue = parseInt($(this).text(), 10);
        //         unAvaArray.push(newValue);
        //     }
        // });


        // setInterval(function(){
        //     document.getElementsByClassName("middle");
        //     for
        // })

        var timer = setInterval(function () {
            $(".middle").each(function() {
                // console.log($(this).text());
                if($(this).text() === "avalible" || $(this).text() === "broken"){;}
                else{
                    var newValue = parseInt($(this).text(), 10) - 1;
                    $(this).text(newValue + "s");
                    if(newValue == 0) {
                        location.reload();
                    }
                }
            });
        }, 1000);