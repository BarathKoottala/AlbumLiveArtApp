// NOTE: this standalone script is not currently loaded by index.html (the page
// uses an inline <script>). Kept in sync with that fix for reference.

function refreshArtwork(){
    // Reuse the SAME <img> element. Replacing/recreating it restarts the CSS
    // spin animation from 0deg, which made the vinyl snap back mid-rotation.
    const img = document.getElementById('dynamicImage');

    img.onload = function() {
        const colorThief = new ColorThief();
        let colorArray = colorThief.getColor(img);
        let rgbString = "rgb(" + colorArray[0] + "," + colorArray[1] + "," + colorArray[2] + ")";
        document.body.style.backgroundColor = rgbString;
        changeHeaderBasedOnLuminance(colorArray);
    };

    // Cache-bust so an updated image is re-fetched.
    img.src = "/static/album_art.jpg" + '?' + Math.random();
}

function getLuminance(r,g,b){
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function changeHeaderBasedOnLuminance(colorArray){
    luminance = getLuminance(colorArray[0], colorArray[1], colorArray[2]);
    if(luminance > 128) { // Halfway point on 255 scale
        textColor = "black";
    } else {
        textColor = "white";
    }
    document.getElementById("currentlyPlaying").style.color = textColor;
}
function startLogic(){
    document.addEventListener('DOMContentLoaded', function() {
        try {
            setInterval(refreshArtwork, 1000); // Change image every 5 seconds
        } catch (error) {
            console.log(error);
        }
    });
}

startLogic(); 