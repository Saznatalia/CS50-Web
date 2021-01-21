document.addEventListener('DOMContentLoaded', function() {
    load_posts();
});

function load_posts() {
    fetch('/posts', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(() => {
        console.log(response);
        console.log("Hello World")
    })
} 