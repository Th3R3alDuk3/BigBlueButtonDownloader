window.onload = () => {

    /* SYNCHRONIZE VIDEO1 CONTROL WITH VIDEO2 */

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

    /* SPLIT.JS */

    if (window.Split) {

        Split([".split1", ".split2"], {
            sizes: [75, 25],
            minSize: [450, 150]
        });

    } else {
        console.log("split.js not found");
    }

    /* VANTA.JS */

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