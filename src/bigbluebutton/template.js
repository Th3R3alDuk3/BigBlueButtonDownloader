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

    video1.onkeypress = (event) => {
        switch(event.keyCode) {
            case 49: // key 1
                video1.currentTime -= 10;
                break;
            case 50: // key 2
                video1.currentTime -= 30;
                break;
            case 51: // key 3
                video1.currentTime -= 60;
                break;
            case 52: // key 4
                video1.currentTime += 10;
                break;
            case 53: // key 5
                video1.currentTime += 30;
                break;
            case 54: // key 6
                video1.currentTime += 60;
                break;
            case 55: // key 7
                video1.playbackRate = 0.8;
                video2.playbackRate = 0.8;
                break;
            case 56: // key 8
                video1.playbackRate = 1;
                video2.playbackRate = 1;
                break;
            case 57: // key 9
                video1.playbackRate = 1.2;
                video2.playbackRate = 1.2;
                break;
        }
    }

    // TODO: audio

    /**/

    var messages = document.getElementsByClassName("message");

    setInterval(() => {

        [...messages].forEach(message => {

            let seconds = message.getAttribute("seconds");

            if (video1.currentTime > Number(seconds))
                message.classList.add("marked");
            else
                message.classList.remove("marked");

        });

    }, 5000);

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
        console.log("split not found");
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
        console.log("vanta not found");
    }

}