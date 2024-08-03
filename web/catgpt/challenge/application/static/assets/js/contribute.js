document.getElementById("model_form").addEventListener("submit",function(e) {
    
    e.preventDefault();

    $("#submit_button").val("Please wait...").attr("disabled","disabled");

    const input = document.getElementById('model_input');
    const file = input.files[0];
    if (!file) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('model', file);

    fetch('/api/model/validate', {
        method: 'POST',
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            throw new Error('Something went wrong');
        }
    })
    .then(data => {
        $('#accuracy').css('width', data["accuracy"]+'%').attr('aria-valuenow', data["accuracy"]).html(data["accuracy"]+'% Accuracy');
        $("#submit_button").val("Submit").removeAttr("disabled");
    })
    .catch((error) => {
        console.error('Error:', error);
        $("#submit_button").val("Submit").removeAttr("disabled");
    });
});