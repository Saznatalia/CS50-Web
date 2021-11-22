document.addEventListener("DOMContentLoaded", function() {
    hideFooter();
    document.querySelectorAll('#heart').forEach(heart => {
        heart.onclick = function() {
            let postId = this.getAttribute("data-post-id");
            console.log(postId);
            fetch('/like', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken':  getCookie('csrftoken')
                },
                body: JSON.stringify({
                    post_id: postId
                })
            })
            .then(async response => {
                const result = await response.json();
                console.log(result)
                if (result['liked'] == false) {
                    heart.style.color = 'red';
                }
                if (result['liked'] == true) {
                    heart.style.color = 'black';
                }
                document.querySelector(`#post${postId}`).innerHTML = result['likes']
            })
        }
    });
})

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function hideFooter() {
    let posts = document.getElementsByName("post");
    if (posts.length == 0) {
        document.querySelector("footer").hidden = true;
    }
}

function follow(btn, id) {
    fetch(`/profile/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken':  getCookie('csrftoken')
        },
        body: JSON.stringify({'btn_value': btn.value, 'user_id': id})
    })
    .then(response => {
        console.log(response);
        return response.json()
    })
    .then(result => {
        if (result['status'] == 200) {
            alert(result.message);
            location.reload();
        }
        if (result['status'] == 404) {
            console.log("User you want to follow doesn't exist");
        }
    })
}