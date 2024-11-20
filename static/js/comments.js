document.addEventListener('DOMContentLoaded', () => {
    // Comments Loading
        
    const postId = document.getElementById('post-id').value
    const commentsBox = document.getElementById('commentsBox')

    function commentsLoading() {
        $.ajax({
        type: 'GET',
        url: `/comments-json/${postId}/`,
        success: function (response) {
            console.log(postId)
            console.log(response.data)
        },
        error: function (error) {
            console.error(error);
        }
    });
    }

    if (commentsBox) {
        commentsLoading()
    }
})