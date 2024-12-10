document.addEventListener('DOMContentLoaded', () => {

    // Comments Loading
    const postId = document.getElementById('post-id').value;
    const commentsBox = document.getElementById('comments-box');
    const spinnerBox = document.getElementById('comments-spinner-box');
    const loadingBox = document.getElementById('comments-loading-box');

    let visible = 3;
    let isLoading = false;

    function handleGetComments() {
        if (isLoading) return;
        isLoading = true;

        spinnerBox.classList.remove('not-visible');

        $.ajax({
            type: 'GET',
            url: `/comments-json/${postId}/${visible}`,
            success: function (response) {
                const maxSize = response.max;
                const commentsHtml = response.data;

                setTimeout(() => {
                    spinnerBox.classList.add('not-visible');

                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = commentsHtml;

                    Array.from(tempDiv.children).forEach(child => {
                        commentsBox.appendChild(child);
                    });

                    if (maxSize) {
                        observer.disconnect();
                        const endMessage = document.createElement('div');
                        endMessage.className = 'has-text-centered mt-3';
                        endMessage.innerHTML = "<strong>No more comments to load</strong>";
                        commentsBox.appendChild(endMessage);
                    } else {
                        visible += 3;
                    }

                    isLoading = false;
                }, 1000); // 1000
            },
            error: function (error) {
                console.error(error);
                isLoading = false;
                spinnerBox.classList.add('not-visible');
            }
        });
    }

    const observer = new IntersectionObserver((entries) => {
        const entry = entries[0];
        if (entry.isIntersecting) {
            handleGetComments();
        }
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 1
    });

    if (loadingBox) {
        observer.observe(loadingBox);
    }

});
