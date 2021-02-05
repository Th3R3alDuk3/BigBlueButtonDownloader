window.onload = () => {

    var video1 = document.getElementById("video1");
    var video2 = document.getElementById("video2");

    video1.onplay = (event) => {
        video2.play();
    };

    video1.onpause = (event) => {
        video2.pause();
    };

    video1.onseeking = (event) => {
        video2.currentTime = video1.currentTime;
    };

    video1.onseeked = (event) => {
        video2.currentTime = video1.currentTime;
    };

    // TODO: audio

    /**/

    if (window.Split) {

        Split(["#view1", "#splitView2"], {
            sizes: [75, 25],
            minSize: [450, 350],
            direction: "horizontal",
            gutterSize: 5
        });

        Split(["#view2", "#view3"], {
            sizes: [25, 75],
            minSize: [150, 250],
            direction: "vertical",
            gutterSize: 5
        });

    } else {
        console.log("split.js not found");
    }

    /**/

    if (window.VANTA) {

        VANTA.WAVES({
            el: "#vanta",
            mouseControls: false,
            touchControls: false,
            gyroControls: false,
            scale: 1.0,
            scaleMobile: 1.0,
            color: 0x06172a,
            waveSpeed: 0.5
        })

    } else {
        console.log("vanta.js not found");
    }

}