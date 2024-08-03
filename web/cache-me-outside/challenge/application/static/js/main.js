function activeTab(tab){
    $('.nav-tabs a[href="#' + tab + '"]').tab('show');
  };

document.getElementById('loginForm').addEventListener('submit', function(event) {

    event.preventDefault();

    const username = document.getElementById('loginUser').value;
    const password = document.getElementById('loginPassword').value;

    fetch('/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location = "/dashboard";
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('registerForm').addEventListener('submit', function(event) {

    event.preventDefault();

    const username = document.getElementById('registerUser').value;
    const password = document.getElementById('registerPassword').value;

    fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            activeTab("login");
        } else {
            alert(data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});