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

function getAccuracyScores(imageData) {
  console.log("入った");
  const score = tf.tidy(() => {
    // convert to tensor (shape: [width, height, channels])  
    const channels = 1; // grayscale              
    let input = tf.fromPixels(imageData, channels);
    // normalized
    input = tf.cast(input, 'float32').div(tf.scalar(255));
    // reshape input format (shape: [batch_size, width, height, channels])
    input = input.expandDims();
    // predict
    return model.predict(input).dataSync();
  });
  console.log(score);
  return score;
}

function prediction() {
  const imageData = getImageData();
  const accuracyScores = getAccuracyScores(imageData);
  const maxAccuracy = accuracyScores.indexOf(Math.max.apply(null, accuracyScores));
  const elements = document.querySelectorAll(".accuracy");
  elements.forEach(el => {
    const rowIndex = Number(el.dataset.rowIndex);
    if (maxAccuracy === rowIndex) {
      el.parentNode.classList.add('is-selected');
    }
    el.innerText = accuracyScores[rowIndex];
  })
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