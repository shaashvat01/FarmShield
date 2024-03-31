$(document).ready(function() {
    // Smooth scrolling for navigation links
    $('a[href*="#"]').on('click', function(e) {
        e.preventDefault();
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top,
        }, 500, 'linear');
    });

    // Handle form submission
    $('#uploadForm').on('submit', function(e) {
        e.preventDefault();

        // Display a loading message or graphic
        $('#predictionResult').html(`<div>Loading...</div>`);

        $.ajax({
            url: '/predict',
            type: 'POST',
            data: new FormData(this),
            contentType: false,
            cache: false,
            processData: false,
            success: function(data) {
                $('#predictionResult').html(`<p>Predicted class: ${data.predictedClass}, Probability: ${data.probability}</p>`);
            },
            error: function() {
                $('#predictionResult').html(`<p>An error occurred. Please try again.</p>`);
            }
        });
    });
});
