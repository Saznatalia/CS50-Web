document.addEventListener("DOMContentLoaded", function() {
    hideFooter();
    document.querySelectorAll('#heart').forEach(heart => {
        heart.onclick = function() {
            let postId = this.getAttribute("data-post-id");
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
        body: JSON.stringify({'btn_value': btn.value, 
                              'user_id': id})
    })
    .then(response => {
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

function edit_post(btn, postId) {
    const editPostDiv = btn.parentNode;
    postDiv = editPostDiv.parentNode;
    oldContent = document.getElementById("content" + postId).innerText;
    const newContentTextArea = document.createElement('textarea');
    newContentTextArea.className = "post";
    newContentTextArea.value = oldContent;

    const savePostBtn = document.createElement('button');
    savePostBtn.className = "btn btn-primary btn-sm";
    savePostBtn.innerHTML = "Save";
    savePostBtn.addEventListener('click', () => {
        if (newContentTextArea.value == "") {
            alert("Your entry is empty!");
        }
        else {
            fetch(`/edit/${postId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    'post_id': postId, 
                    'new_content': newContentTextArea.value
                }) 
            })
            .then(response => {
                if (response.status == 204) {
                    location.reload();
                }
            })
        }
    })

    const cancelBtn = document.createElement('button');
    cancelBtn.className = "btn btn-secondary btn-sm";
    cancelBtn.style = "margin-left: 20px;";
    cancelBtn.innerHTML = "Cancel";
    cancelBtn.addEventListener('click', () => {
        newContentTextArea.style.display = 'none';
        savePostBtn.style.display = 'none';
        cancelBtn.style.display = 'none';
        btn.style.display = '';
        document.getElementById("content" + postId).style.display = '';
        postDiv.getElementsByClassName("post_date")[0].style.display = '';
        postDiv.getElementsByClassName("fa fa-heart")[0].style.display = '';
        document.getElementById("post" + postId).style.display = '';
    })
    editPostDiv.append(newContentTextArea);
    editPostDiv.append(savePostBtn);
    editPostDiv.append(cancelBtn);
    
    // Hide old content of div
    btn.style.display = 'none';
    document.getElementById("content" + postId).style.display = 'none';
    postDiv.getElementsByClassName("post_date")[0].style.display = 'none';
    postDiv.getElementsByClassName("fa fa-heart")[0].style.display = 'none';
    document.getElementById("post" + postId).style.display = 'none';

}