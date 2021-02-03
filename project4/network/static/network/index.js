document.addEventListener('DOMContentLoaded', function() {
    load_posts();
});

function load_posts() {
    fetch('/api/posts', {
        method: 'GET'
    })
    .then(response => response.json())
    .then((data) => {
        var ListedItems = data.response;
        console.log(ListedItems);
        const postsElement = document.getElementById("posts");
        var posts = "";
        for (var i = 0; i < ListedItems.length; i++) {
            var postObj = ListedItems[i];
            var currentPost = FormatUserPost(postObj);
            posts += currentPost;
        }
        postsElement.innerHTML = posts;
    })
} 

function FormatUserPost(post) {
    var LikeBtn = "<button class='btn btn-success btn-sm'>Like</button>";
    var dateStr = JSON.parse(JSON.stringify(post.date));
    var formattedDate = new Date(dateStr);
    // var formattedDate = dateStr.getMonth();
    var formattedPost = "<h5>" + post.username + "</h5>" + post.content + 
    "<br/>" + formattedDate + "<br/>" + LikeBtn;
    return formattedPost
}