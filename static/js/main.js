(function() {

    var guid = (function() {
        function s4() {
            return Math.floor((1 + Math.random()) * 0x10000)
                .toString(16)
                .substring(1);
        }
        return function() {
            return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
                s4() + '-' + s4() + s4() + s4();
        };
    })();


    var streaming = false,
        video = document.querySelector('#video'),
        cover = document.querySelector('#cover'),
        canvas = document.querySelector('#iframe'),
        photo = document.querySelector('#photo'),
        startbutton = document.querySelector('#startbutton'),
        width = 200,
        height = 0;

    navigator.getMedia = (navigator.getUserMedia ||
        navigator.webkitGetUserMedia ||
        navigator.mozGetUserMedia ||
        navigator.msGetUserMedia);

    navigator.getMedia({
            video: true,
            audio: false
        },
        function(stream) {
            if (navigator.mozGetUserMedia) {
                video.mozSrcObject = stream;
            } else {
                var vendorURL = window.URL || window.webkitURL;
                video.src = vendorURL ? vendorURL.createObjectURL(stream) : stream;
            }
            video.play();
        },
        function(err) {
            console.log("An error occured! " + err);
        }
    );

    video.addEventListener('canplay', function(ev) {
        if (!streaming) {
            height = video.videoHeight / (video.videoWidth / width);
            video.setAttribute('width', width);
            video.setAttribute('height', height);
            canvas.setAttribute('width', width);
            canvas.setAttribute('height', height);
            streaming = true;
        }
    }, false);


    function dataURItoBlob(dataURI) {
        var byteString = atob(dataURI.split(',')[1]);
        var ab = new ArrayBuffer(byteString.length);
        var ia = new Uint8Array(ab);
        for (var i = 0; i < byteString.length; i++) {
            ia[i] = byteString.charCodeAt(i);
        }
        return new Blob([ab], { type: 'image/jpeg' });
    };

    function takepicture() {
        var data,
            postOBj,
            fd;

        console.log("Picture being taken.");
        canvas.width = width;
        canvas.height = height;
        canvas.getContext('2d').drawImage(video, 0, 0, width, height);

        // Converting picture to the little frame
        data = canvas.toDataURL('image/png');
        photo.setAttribute('src', data);

        // Upload the photo

        postObj = dataURItoBlob(data);
        fd = new FormData();

        fd.append("file", postObj);
        debugger

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: fd,
            contentType: false,
            processData: false,
            success: function(data) {

            },
            error: function() {


            }
        });
    };

    var timeoutId;
    startbutton.addEventListener('click', function(ev) {
        $("#count_num").html("3");

        var pictureTime = Math.floor((Math.random() * 3) + 1);

        if (timeoutId) window.clearTimeout(timeoutId);
        var timeoutId = window.setTimeout(takepicture, pictureTime * 1000);

        var timer = setInterval(function() {
            $("#count_num").html(function(i, html) {

                if (parseInt(html) > 0) {
                    return parseInt(html) - 1;
                } else {
                    clearTimeout(timer);
                    return "Enjoy!";

                }
            });
        }, 1000);
        ev.preventDefault();
    }, false);

})();
