window.onload = () => {

    var video1 = document.getElementById("video1");
    var video2 = document.getElementById("video2");

    /* SYNCHRONIZE VIDEO1 CONTROL WITH VIDEO2 */

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

    /* JQUERY AND JQUERY.UI */

    if (window.jQuery) {
        if (window.jQuery.ui) {

            $(".resizable").resizable({
                handles: "e",
                start: (event, ui) => {
                    $("video").css({
                        "maxHeight": ui.size.height - 100
                    });
                }
            });

            $("video").draggable();

            // focused video set foreground
            $("video").mousedown((event) => {
                $("video").each((index, target) => {
                    target.style.zIndex = 1;
                    if (target == event.target)
                        target.style.zIndex = 9999;
                });
            });

        } else {
            alert("Not possible to load 'jQuery.ui' which was used for certain element effect!");
        }
    } else {
        alert("Not possible to load 'jQuery', which is required for 'jQuery.ui'!");
    }

    if (window.VANTA) {
        VANTA.WAVES({
            el: "#vanta",
            mouseControls: false,
            touchControls: false,
            gyroControls: false,
            scale: 1.0,
            scaleMobile: 1.0,
            color: 0x111111,
            waveSpeed: 0.5
        })
    }

}