function prediction() {
    canvasImage = $('#preview').get(0);
    var base64 = canvasImage.toDataURL('image/png');
    console.log(base64);

    var fData = new FormData();
    fData.append('img', base64);

    $.ajax({
        url: '/return',
        type: 'post',
        data: fData,
        success: function (data, dataType) {
            console.log('success', data);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log('error: ' + errorThrown);
        }
    });
}

function reset() {
    let elements = document.querySelectorAll(".accuracy");
        elements.forEach(el => {
            el.innerText = '-';
            el.parentNode.classList.remove('is-selected');
            canvas.clearRect(0,0,250,250);
        })
}