const INPUT_WIDTH = 28;
const INPUT_HEIGHT = 28;

$('#input_img').change(function() {
  canvas.clearRect(0,0,28,28);
  canvas_.clearRect(0, 0, 250, 250);

  if (this.files.length > 0){
    var file = this.files[0];

    var image = new Image();
    var reader = new FileReader();

    reader.onload = function(evt) {
      image.onload = function() {
        canvas.drawImage(image, 0, 0, 28, 28);
        canvas_.drawImage(image, 0, 0, 250, 250);
      };
      image.src = evt.target.result;
    };
    reader.readAsDataURL(file);
  }
});