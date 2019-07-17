let use_vgg = 0

window.onload = () => {

}

$(function () {
    const successResult = (data) => {
        $('#cam_img').attr("src", data.gene_image_data);

        $('#result').html(data.class_name);
        $('#accuracy').html(data.score);

        $('.prediction').css("background-color", "#d10d3f")
    };

    const failedResult = (data, result) => {
        alert("Error");
    };

    const fileChange = (evt) => {
        let model_select = $("input[name='model_select']:checked").val();

        use_vgg = 0

        if (model_select === 'orginal') {
            use_vgg = 0;
        }

        var fileOb = $("#input_img")[0].files[0];

        var formData = new FormData();
        formData.append("imageFile", fileOb);
        formData.append("use_model", use_vgg.toString());

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

    $('#prediction-btn').click(fileChange);
});

$('#use_vgg16').click(function () {
    console.log("in")
    use_vgg = 1;
});

function reset() {
    let elements = document.querySelectorAll("#accuracy");
    elements.forEach(el => {
        el.innerText = '-';
        canvas.clearRect(0, 0, 224, 224);
    });

    let elements2 = document.querySelectorAll("#result");
    elements2.forEach(el => {
        el.innerText = '-';
    });
    $('#cam_img').attr("src", "");
    $('.prediction').css("background-color", "#696969")
}

