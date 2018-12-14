var canvas = $('#preview').get(0).getContext('2d');

$(function(){
    var result = function(data){
        $('#result').text("this image is :" + data.result);
        $('#acuracy').text("acuracy :" + data.acuracy);
    };

    var fileChange = function(evt){

        canvas.clearRect(0,0,250,250);

        if (this.files.length > 0){
            var file = this.files[0];

            var image = new Image();
            var reader = new FileReader();

            reader.onload = function(evt) {
                image.onload = function() {
                canvas.drawImage(image, 0, 0, 250, 250);
                };
                image.src = evt.target.result;
            };
            reader.readAsDataURL(file);
        }
        canvasImage = $('#preview').get(0);
        var base64Img = canvasImage.toDataURL('image/png');
        console.log(base64Img);

        // var fData = new FormData();
        // fData.append('img', base64);

        var req = {
            url: '/predict',
            type: 'post',
            data: {
                "img": base64Img
            },
            success: function (data, dataType) {
                console.log('success', data);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log('error: ' + errorThrown);
            }
        };

        var promise = $.ajax(req);
        promise.then(result);
    };

    $('#inputImg').change(fileChange);
});