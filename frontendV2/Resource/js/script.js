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