const IMAGE_SIZE = 28;
var canvas = document.querySelector("#preview").getContext('2d');
var canvas_ = document.querySelector("#preview_").getContext('2d');

function prediction() {
    $.ajax({
        url: $(this).parent('form').attr('action'),
        type: 'post',
        data: $(this).parent('form').serialize()
    });
}

function reset() {
    let elements = document.querySelectorAll(".accuracy");
        elements.forEach(el => {
            el.innerText = '-';
            el.parentNode.classList.remove('is-selected');
            canvas.clearRect(0,0,28,28);
            canvas_.clearRect(0, 0, 250, 250);
        })
}