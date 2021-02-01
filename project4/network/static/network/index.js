document.addEventListener('DOMContentLoaded', function() {
    load_posts();
});

function load_posts() {
    fetch('/api/posts', {
        method: 'GET'
    })
    .then(response => response.json())
    .then((data) => {
        console.log(data);
        // var ListedItems = data.response;
        // console.log(ListedItems);
        // const postsElement = document.getElementById("posts");
        // console.log(postsElement);
        // postsElement.innerHTML = "Loading..."
    })
} 