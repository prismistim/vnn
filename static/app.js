$(function(){
    var successResult = function (data) {
        $('#result').text(data.result);
        $('#acuracy').text(data.acuracy);
    }

    var failedResult = function (data) {
        alert("HA?YABAI");
    }

    var fileChange = function(evt){
        var fileOb = $("#input_img")[0].files[0];

        var formData = new FormData();
        formData.append("imageFile", fileOb);

        var req = {
            url: "/result",
            method: "post",
            processData: false,
            contentType: false,
            data: formData
        };

        var promise = $.ajax(req);
        promise.then(successResult, failedResult);

    };

    $('#input_img').change(fileChange);
});

function reset() {
    let elements = document.querySelectorAll(".accuracy");
        elements.forEach(el => {
            el.innerText = '-';
            el.parentNode.classList.remove('is-selected');
            canvas.clearRect(0,0,250,250);
        })
}

