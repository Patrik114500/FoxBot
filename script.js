const canvas = document.getElementById('canvas1')
const ctx = canvas.getContext('2d');
var w = window.innerWidth;
var h = window.innerHeight;
const CANVAS_WIDTH = canvas.width = 1500;
const CANVAS_HIGHT = canvas.height = 600;
const playerImage = new Image();
playerImage.src = 'Main/Fox Sprite Sheet.png'
const backgroundImage = new Image();
backgroundImage.src = 'Main/Background.png'
const speechbubble = new Image();
speechbubble.src = 'Main/SpeechBubble.png'

const spriteWidth = 32;
const spriteHeight = 32;
const floor = CANVAS_HIGHT-spriteHeight-130
let frameX = 0;
let frameY = 0;
let posX = 200;
let heading = 1
let animationFrame = 0;
const staggerFrames = 16;


function printAt( context , text, x, y, lineHeight, fitWidth)
{
    fitWidth = fitWidth || 0;

    if (fitWidth <= 0)
    {
        context.fillText( text, x, y );
        return;
    }
    
    for (var idx = 1; idx <= text.length; idx++)
    {
        var str = text.substr(0, idx);
        console.log(str, context.measureText(str).width, fitWidth);
        
        if (context.measureText(str).width > fitWidth)
        {
            context.fillText( text.substr(0, idx-1), x, y );
            printAt(context, text.substr(idx-1), x, y + lineHeight, lineHeight,  fitWidth);
            
            return;
        }
        if (text.length==idx)
        {

        }
    }
    context.fillText( text, x, y );
   
}

function run(){
    frameY = 2
    let position = (Math.floor(animationFrame/staggerFrames) % 7)
    frameX = spriteHeight*position;
    if(posX>900)
    {
        heading=-1
    }
    else if ( posX<1)
    {
        heading=1
    }
    else{
        if (heading==1) {
            ctx.scale(1,1)
            ctx.drawImage(playerImage,frameX ,spriteHeight*frameY, spriteWidth, spriteHeight , posX, floor,100 ,100);
        }
        else{
            ctx.scale(-1,1)
            ctx.drawImage(playerImage,frameX ,spriteHeight*frameY, spriteWidth, spriteHeight , -posX-100, floor,100 ,100);
        }
    }
    posX+=heading
    
}
function look(){
    frameY = 1
    let position = (Math.floor(animationFrame/staggerFrames+5) % 13)
    frameX = spriteHeight*position;
    if (heading==1) {
        ctx.scale(1,1)
        ctx.drawImage(playerImage,frameX ,spriteHeight*frameY, spriteWidth, spriteHeight , posX, floor,100 ,100);
    }
    else{
        ctx.scale(-1,1)
        ctx.drawImage(playerImage,frameX ,spriteHeight*frameY, spriteWidth, spriteHeight , -posX-100, floor,100 ,100);
    }
}
function stand(){
    frameY = 0
    let position = (Math.floor(animationFrame/staggerFrames+3) % 4)
    frameX = spriteHeight*position;
    if (heading==1) {
        ctx.scale(1,1)
        ctx.drawImage(playerImage,frameX ,spriteHeight*frameY, spriteWidth, spriteHeight , posX, floor,100 ,100);
    }
    else{
        ctx.scale(-1,1)
        ctx.drawImage(playerImage,frameX ,spriteHeight*frameY, spriteWidth, spriteHeight , -posX-100, floor,100 ,100);
    }
}

function animate(){

    let chat = document.getElementById("chat").innerHTML;
    ctx.clearRect(0, 0, CANVAS_WIDTH,CANVAS_HIGHT);
    ctx.fillStyle = "#000000";
    ctx.drawImage(backgroundImage,0,-190)
    ctx.drawImage(speechbubble, posX+80, 0,  600, 600);
    ctx.font = '130% bold Courier';
    
    printAt(ctx, chat, posX+150, 100, 40, 430, 600, 600, 0);
    

    if (Math.floor(animationFrame)%1000<400) {
        run()
    }
    else if (Math.floor(animationFrame)%1000<700){
        stand()
    }
    else{
        look()
    }
    //ctx.drawImage(playerImage,frameX ,spriteHeight*frameY, spriteWidth, spriteHeight , 0, floor,100 ,100);
    animationFrame++;
    requestAnimationFrame(animate);
};
animate();