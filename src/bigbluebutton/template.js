window.onload = () => {

    var video1 = document.getElementById("video1");
    var video2 = document.getElementById("video2");

    /**/

    // TODO: bundle if cases

    if (video1.readyState != 4) {
        if (video2.readyState == 4) {
            video2.controls = true;
        }
    }

    /**/

    if (video1.readyState == 4) {
        if (video2.readyState == 4) {

            video1.onplay = () => {
                video2.play();
            };

            video1.onpause = () => {
                video2.pause();
            };

            video1.onseeked = () => {
                video2.currentTime = video1.currentTime;
            };
        }
    }

    /**/

    var videos = [video1, video2];

    videos.forEach(video => {
        if (video.readyState == 4) {

            video.onkeypress = (event) => {
                switch(event.keyCode) {

                    case 49: // key 1
                        video.currentTime -= 10;
                        break;
                    case 50: // key 2
                        video.currentTime -= 30;
                        break;
                    case 51: // key 3
                        video.currentTime -= 60;
                        break;

                    case 52: // key 4
                        video.currentTime += 10;
                        break;
                    case 53: // key 5
                        video.currentTime += 30;
                        break;
                    case 54: // key 6
                        video.currentTime += 60;
                        break;

                    case 55: // key 7
                        videos.forEach(video => video.playbackRate = 1.0);
                        break;
                    case 56: // key 8
                        videos.forEach(video => video.playbackRate = 1.5);
                        break;
                    case 57: // key 9
                        videos.forEach(video => video.playbackRate = 2.0);
                        break;

                }
            }

        }
    });

    // TODO: audio

    /**/

    var video = null;

    videos.forEach(_video => {
        if (_video.readyState == 4)
            video = _video;
    });

    /**/

    var messages = document.getElementsByClassName("message");

    setInterval(() => {

        [...messages].forEach(message => {

            let seconds = message.getAttribute("seconds");

            message.classList.toggle(
                "marked",
                video.currentTime > Number(seconds)
            );

        });

    }, 3000);

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