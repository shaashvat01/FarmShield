const express = require('express');
const fileUpload = require('express-fileupload');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const tf = require('@tensorflow/tfjs-node'); // Import TensorFlow.js for Node.js
const fs = require('fs');

const app = express();

// Middleware setup
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(fileUpload({
    createParentPath: true
}));
app.use(express.static('public')); // Serve static files from the 'public' directory

// Load your TensorFlow model globally to avoid reloading it on each request
let globalModel;
async function loadGlobalModel() {
    if (!globalModel) {
        console.log("Loading model...");
        globalModel = await tf.loadLayersModel('file:///Users/shaashvatmittal/Desktop/Hackprinceton/Wheat_Health_Model/model.json');
        console.log("Model loaded successfully.");
    }
}

// Immediately invoke the model loading to ensure it's done before any request comes in
loadGlobalModel().catch(console.error);

// Function to process image and make a prediction
async function predictImage(imagePath) {
    const imageBuffer = fs.readFileSync(imagePath);
    let tfimage = tf.node.decodeImage(imageBuffer, 3);
    tfimage = tf.image.resizeBilinear(tfimage, [224, 224]);
    const imageTensor = tfimage.expandDims(0);
    const prediction = globalModel.predict(imageTensor);
    
    const predictionArray = await prediction.array();
    const scores = predictionArray[0];
    const predictedClass = scores.indexOf(Math.max(...scores));
    return { predictedClass, probability: scores[predictedClass] };
}

// Endpoint to upload images and get predictions
app.post('/predict', async (req, res) => {
    try {
        if (!req.files || Object.keys(req.files).length === 0) {
            return res.status(400).send('No files were uploaded.');
        }

        let image = req.files.image;
        const imagePath = path.join(__dirname, 'uploads', image.name);
        await image.mv(imagePath);

        const { predictedClass, probability } = await predictImage(imagePath);
        
        // Optionally, delete the image after prediction to save space
        fs.unlinkSync(imagePath);

        res.send({
            message: 'Prediction completed',
            predictedClass,
            probability
        });
    } catch (err) {
        console.error("Error during prediction:", err);
        res.status(500).send('Server error');
    }
});

// Start the server
const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Server is listening on port ${port}.`));
