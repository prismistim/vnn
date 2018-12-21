// $(function() {
//     canvasImage = $('#preview').get(0);
//     var base64Img = canvasImage.toDataURL('image/png');
//     console.log(base64Img);
//
//     // var fData = new FormData();
//     // fData.append('img', base64);
//
//     var req = {
//         url: '/predict',
//         type: 'post',
//         data: {
//             "img": base64Img
//         },
//         success: function (data, dataType) {
//             console.log('success', data);
//         },
//         error: function (XMLHttpRequest, textStatus, errorThrown) {
//             console.log('error: ' + errorThrown);
//         }
//     };
//
//     var promise = $.ajax(req);
//     promise.then(result);
//
//     var result = function(data){
//         $('#result').text("this image is :" + data.result);
//         $('#acuracy').text("acuracy :" + data.acuracy);
//     };
// });

function reset() {
    let elements = document.querySelectorAll(".accuracy");
        elements.forEach(el => {
            el.innerText = '-';
            el.parentNode.classList.remove('is-selected');
            canvas.clearRect(0,0,250,250);
        })
}