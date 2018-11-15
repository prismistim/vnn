const IMAGE_SIZE = 28;
var canvas = document.querySelector("#preview").getContext('2d');
var canvas_ = document.querySelector("#preview_").getContext('2d');
// load pre-trained model
let model;
tf.loadModel('../model/model.json')
  .then(pretrainedModel => {
    model = pretrainedModel;
    document.querySelector('#prediction-btn').classList.remove('disabled');
  });
  
function getImageData() {
  const inputWidth = inputHeight = 28;

  // convert grayscale
  let imageData = canvas.getImageData(0, 0, inputWidth, inputHeight);
  console.log(imageData);
  for (let i = 0; i < imageData.data.length; i+=4) {
    const avg = (imageData.data[i] + imageData.data[i+1] + imageData.data[i+2]) / 3;
    imageData.data[i] = imageData.data[i+1] = imageData.data[i+2] = avg;
  }
  return imageData;
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