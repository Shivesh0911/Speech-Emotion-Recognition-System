$('#uploadForm').submit(function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    $.ajax({
        type: 'POST',
        url: '',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            console.log(response); // Log the response object to the console
            $('#result').text('Predicted emotion: ' + response.predicted_emotion); // Update based on response format
        },
        error: function() {
            alert('Failed to predict emotion.');
        }
    });
});
