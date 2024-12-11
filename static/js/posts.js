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

    function initializeCarousels() {
        const carousels = postsBox.querySelectorAll('.carousel-container:not(.initialized)');
        carousels.forEach((carousel) => {
            let currentIndex = 0;

            function updateCarousel() {
                const slides = carousel.querySelectorAll('.carousel-slide');
                const indicators = carousel.querySelectorAll('.indicator');

                carousel.querySelector('.carousel').style.transform = `translateX(-${currentIndex * 100}%)`;

                indicators.forEach((indicator, index) => {
                    indicator.classList.toggle('active', index === currentIndex);
                });
            }

            function prevSlide() {
                const slides = carousel.querySelectorAll('.carousel-slide').length;
                currentIndex = (currentIndex - 1 + slides) % slides;
                updateCarousel();
            }

            function nextSlide() {
                const slides = carousel.querySelectorAll('.carousel-slide').length;
                currentIndex = (currentIndex + 1) % slides;
                updateCarousel();
            }

            function goToSlide(index) {
                currentIndex = index;
                updateCarousel();
            }

            const prevButton = carousel.querySelector('.carousel-control.prev');
            const nextButton = carousel.querySelector('.carousel-control.next');
            const indicators = carousel.querySelectorAll('.indicator');

            prevButton?.addEventListener('click', prevSlide);
            nextButton?.addEventListener('click', nextSlide);

            indicators.forEach((indicator, idx) => {
                indicator.addEventListener('click', () => goToSlide(idx));
            });

            updateCarousel();

            carousel.classList.add('initialized');
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

                    initializeModals();
                    initializeCarousels();

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
                }, 0);
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
