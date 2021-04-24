////////////////
//    P5JS    //
////////////////

var posX;
var posY;
var progress = 0;
var progressDeg = 0;
var COMP = 0;
var INCOMP = 1;
var mouseState = INCOMP;
var inRad = 5;
function setup() {
    canvas = createCanvas(50,50);
    strokeWeight(2);
    document.addEventListener('mousemove', (ev) => {
        posX = ev.clientX;
        posY = ev.clientY;
        canvas.position(window.scrollX + posX-width/2, window.scrollY + posY-width/2);
    });
    document.body.addEventListener('touchmove', (ev) => {
        posX = ev.touches[0].clientX;
        posY = ev.touches[0].clientY;
        canvas.position(window.scrollX + posX-width/2, window.scrollY + posY-width/2);
    });
    window.addEventListener('scroll', (ev) => {
        progress = Math.round(window.scrollY / (document.body.offsetHeight - window.innerHeight) * 100);
        progressDeg = progress * 360/100;
        canvas.position(window.scrollX + posX-width/2, window.scrollY + posY-width/2);
        //progress = (window.scrollY / window.innerHeight)*100;
        //Smoothprogress = (window.scrollY * progress/100) + progress
        //progressDeg = Smoothprogress * 360/100;
        //console.log(progress)
        //console.log(progressDeg)
    });
}

function draw() {
    clear();
    background(color(0,0,0,0));
    if(mouseState === INCOMP && progress < 100){
        noFill();

        stroke(color(255,155,155));
        circle(25, 25, 46);

        stroke(color(255,55,55));
        arc(25, 25, 46, 46, 0, rads(progressDeg));

        fill(color(255,155,155));
        stroke(color(255,155,155));
        circle(25, 25, inRad);
    }
    
    if(mouseState === COMP && progress > 99){
        noFill();
        stroke(color(255,155,155));
        circle(25, 25, 46);
        stroke(color(255,55,55));
        arc(25, 25, 48, 48, 0, rads(360));
        fill(color(255,155,155));
        stroke(color(255,155,155));
        circle(25, 25, 48);
    }

    if(mouseState === INCOMP && progress > 99){
        for(r = inRad; r <= 48; r+=0.05){
            setTimeout(function() {
                noFill();
                stroke(color(255,155,155));
                circle(25, 25, 46);
                stroke(color(255,55,55));
                arc(25, 25, 46, 46, 0, rads(360));
                fill(color(255,155,155));
                stroke(color(255,155,155));
                circle(25, 25, r);
            }, 100);
        }
        mouseState = COMP;
    }
    
    if(mouseState === COMP && progress < 100){
        for(r = 48; r >= inRad; r-=0.05){
            setTimeout(function() {            
                noFill();
                stroke(color(255,155,155));
                circle(25, 25, 46);
                stroke(color(255,55,55));
                arc(25, 25, 46, 46, 0, rads(360));
                fill(color(255,155,155));
                stroke(color(255,155,155));
                circle(25, 25, r);
            }, 100);
        }
        mouseState = INCOMP;
    }
}

function rads(d) {
    return d * PI / 180;
}

////////////////
//  DOCUMENT  //
////////////////
function landing(){
    window.scroll(0,0);
}
function blogs(){
    window.scroll(0,window.innerHeight);
}

document.addEventListener('mouseleave', (_ev) => {
    for(o = 1; o >= 0; o -= 0.01){
        setTimeout(function() {
            document.getElementsByTagName("canvas")[0].style.opacity = o;
        }, 100);
    }
});

document.addEventListener('mouseenter', (_ev) => {
    for(o = 0; o <= 1; o += 0.1){
        setTimeout(function() {
            document.getElementsByTagName("canvas")[0].style.opacity = o;
        }, 100);
    }
});