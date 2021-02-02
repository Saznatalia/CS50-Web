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
        var ListedItems = data.response;
        console.log(ListedItems);
        const postsElement = document.getElementById("posts");
        var posts = "";
        var LikeBtn = "<button class='btn btn-primary'>Like</button>";
        for (var i = 0; i < ListedItems.length; i++) {
            console.log(ListedItems[i]);
            posts += "<p>" + ListedItems[i].content + "<br/>" + LikeBtn + "</p>";
        }
        postsElement.innerHTML = posts;
    })
} 