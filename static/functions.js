const xml = new XMLHttpRequest();
var lastScrollPos = 0;
var bottomed = false;

function requestMessage(){
    bottomed = false;
    xml.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            const comments = JSON.parse(this.responseText);

            for (var i = 0; i < comments.length; i++){
                var comment = comments[i];
                console.log(comment);
                const parent = document.getElementById("comments");
                const commentDiv = document.createElement("div");
                const commentTime = document.createElement("p");
                const commentText = document.createElement("p");
                const commentLink = document.createElement("a");
                const logo = document.createElement("img");

                commentDiv.className = "comment";
                commentTime.className = "time";
                commentText.className = "text";
                logo.className = "logo";

                console.log(comment);
                commentTime.innerHTML = comment.publishedAt + " ";
                commentLink.href = "https://www.youtube.com/watch?v=" + comment.videoID;
                commentLink.target = "_blank";
                commentText.innerHTML = comment.textDisplay;
                logo.src = "youtubeLogo.png"
                
                commentLink.appendChild(logo);
                commentTime.appendChild(commentLink);
                commentDiv.appendChild(commentTime);
                commentDiv.appendChild(commentText);

                parent.appendChild(commentDiv);
            }
            //document.getElementById("comments").innerHTML = this.responseText;
        }else if(this.status >= 400){
            console.log(this.responseText);
        }
    };

    const value = document.getElementsByClassName("comment").length;
    xml.open("GET", "/update", true);
    xml.setRequestHeader("value", value);
    xml.send();
}

function getOffsetTop(element) {
    let offsetTop = 0;
    while(element) {
        offsetTop += element.offsetTop;
        element = element.offsetParent;
    }
    return offsetTop;
}
window.addEventListener("scrollend", function(){
    const windowHeight = window.innerHeight;
    const scrolledPixels = window.scrollY;
    const offset = document.body.offsetHeight;
    // Check if user has scrolled to the bottom
    console.log(bottomed);
    if (scrolledPixels > lastScrollPos) {
        if (windowHeight + scrolledPixels >= offset) {
            console.log("User has scrolled to the bottom of the page");
            requestMessage();
        }
    }

    lastScrollPos = scrolledPixels;
});