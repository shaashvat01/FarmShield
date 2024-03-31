const tf = require('@tensorflow/tfjs-node'); // Use '@tensorflow/tfjs' for browser
const fs = require('fs');

async function loadModel() {
    // Correct path to the model.json
    const model = await tf.loadLayersModel('file:///Users/shaashvatmittal/Desktop/Hackprinceton/Wheat_Health_Model/model.json');
    return model;
}

async function loadImageAsTensor(path) {
    const imageBuffer = fs.readFileSync(path);
    let tfimage = tf.node.decodeImage(imageBuffer, 3); // for a 3-channel (RGB) image
    
    // Resize the image to 224x224 to match the model's expected input
    tfimage = tf.image.resizeBilinear(tfimage, [224, 224]);
    
    return tfimage.expandDims(0); // Add batch dimension
}

async function predict(imageTensor) {
    const model = await loadModel();
    const prediction = model.predict(imageTensor);
    prediction.print(); // Prints the raw prediction tensor

    // Convert prediction to array and process
    const predictionArray = await prediction.array();
    const scores = predictionArray[0];
    const predictedClass = scores.indexOf(Math.max(...scores));
    console.log(`Predicted class: ${predictedClass} with probability ${scores[predictedClass]}`);
}

async function main() {
    // Correct path to the image
    const imagePath = '/Volumes/Mannan\'s D/Dataset/BrownRust/Brown_rust001.jpg'; // Make sure this is the correct path to your image
    const imageTensor = await loadImageAsTensor(imagePath);
    await predict(imageTensor);
}

main();
