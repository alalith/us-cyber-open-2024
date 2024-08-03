document.getElementById("image_form").addEventListener("submit",function(e) {
    
    e.preventDefault();

    const input = document.getElementById('image_input');

    $("#submit_button").val("Please wait...").attr("disabled","disabled");

    const file = input.files[0];
    if (!file) {
        alert('Please select a file.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    var fr = new FileReader();
    fr.onload = function () {
        document.getElementById("img").src = fr.result;
    }
    
    fr.readAsDataURL(file);

    fetch('/api/image/classify', {
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
        $('#cat').css('width', data["cat"]+'%').attr('aria-valuenow', data["cat"]).html(data["cat"]+'% Cat');
        $('#dog').css('width', data["dog"]+'%').attr('aria-valuenow', data["dog"]).html(data["dog"]+'% Dog');
        $("#submit_button").val("Submit").removeAttr("disabled");
    })
    .catch((error) => {
        console.error('Error:', error);
        $("#submit_button").val("Submit").removeAttr("disabled");
    });
});
