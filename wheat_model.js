const tf = require('@tensorflow/tfjs-node'); // Use '@tensorflow/tfjs' for browser
const fs = require('fs');

// Define class names based on your model's training
const classNames = ['HSeptoria', 'Healthy', 'Yellow Rust', 'Brown Rust', 'Loose Smut']; // Update this array based on your model

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
    const predictionArray = await prediction.array();
    const scores = predictionArray[0];
    const predictedClassIndex = scores.indexOf(Math.max(...scores));
    const predictedClassName = classNames[predictedClassIndex]; // Map the predicted index to the class name
    const probabilities = classNames.map((className, index) => ({ class: className, probability: scores[index] }));
    return { predictions: probabilities, predictedClass: predictedClassName, highestProbability: Math.max(...scores) };
}

module.exports = { predict };

async function main() {
    // Correct path to the image
    const imagePath = '/Users/shaashvatmittal/Desktop/HackPrinceton/Septoria193.png'; // Make sure this is the correct path to your image
    const imageTensor = await loadImageAsTensor(imagePath);
    const prediction = await predict(imageTensor);
    
    console.log('Predictions:');
    prediction.predictions.forEach(pred => {
        console.log(`${pred.class}: ${pred.probability}`);
    });

    console.log(`\nPredicted Class with Highest Probability: ${prediction.predictedClass}, Probability: ${prediction.highestProbability}`);
}

main();
