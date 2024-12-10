document.addEventListener('DOMContentLoaded', () => {
    const postsBox = document.getElementById('posts-box');
    const spinnerBox = document.getElementById('spinner-box');
    const loadBox = document.getElementById('loading-box');

    let visible = 3;
    let isLoading = false;

    function initializeModals() {
        const newImages = postsBox.querySelectorAll('img[data-bs-toggle="modal"]');
        newImages.forEach((img) => {
            img.addEventListener('click', function () {
                const modalImage = document.getElementById('modalImage');
                modalImage.src = this.src;
            });
        });
    }

    function handleGetData() {
        if (isLoading) return;
        isLoading = true;

        spinnerBox.classList.remove('not-visible');

        $.ajax({
            type: 'GET',
            url: `/posts-json/${visible}/`,
            success: function (response) {
                const maxSize = response.max;
                const postsHtml = response.data;

                setTimeout(() => {
                    spinnerBox.classList.add('not-visible');

                    const tempDiv = document.createElement('div');
                    tempDiv.innerHTML = postsHtml;

                    Array.from(tempDiv.children).forEach(child => {
                        postsBox.appendChild(child);
                    });

                    initializeCarousels();
                    initializeModals();

                    if (maxSize) {
                        observer.disconnect();
                        const endMessage = document.createElement('div');
                        endMessage.className = 'has-text-centered mt-3';
                        endMessage.innerHTML = "<strong>No more posts to load</strong>";
                        postsBox.appendChild(endMessage);
                    } else {
                        visible += 3;
                    }

                    isLoading = false;
                }, 0); // 1000
            },
            error: function (error) {
                console.error(error);
                isLoading = false;
                spinnerBox.classList.add('not-visible');
            }
        });
    }

    function initializeCarousels() {
        const carousels = document.querySelectorAll('.carousel');
        carousels.forEach(carousel => {
            if (!carousel.dataset.bsInitialized) {
                new bootstrap.Carousel(carousel, {
                    interval: 4000, // Интервал смены слайдов
                    ride: false     // Автозапуск карусели
                });
                carousel.dataset.bsInitialized = true;
            }
        });
    }    

    const observer = new IntersectionObserver((entries) => {
        const entry = entries[0];
        if (entry.isIntersecting) {
            handleGetData();
        }
    }, {
        root: null,
        rootMargin: '0px',
        threshold: 0.5
    });

    if (loadBox) {
        observer.observe(loadBox);
        handleGetData();
    }
});
