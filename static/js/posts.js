document.addEventListener('DOMContentLoaded', () => {

    // Posts Loading

    const postsBox = document.getElementById('posts-box');
    const spinnerBox = document.getElementById('spinner-box');
    const loadBox = document.getElementById('loading-box');

    let visible = 3;
    let isLoading = false;

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
                    initializeDynamicComponents();
                }, ); // 1000
            },
            error: function (error) {
                console.error(error);
                isLoading = false;
                spinnerBox.classList.add('not-visible');
            }
        });
    }

    function initializeDynamicComponents() {
        document.querySelectorAll('.carousel').forEach(carousel => {
            const prevButton = carousel.querySelector('.carousel-control.prev');
            const nextButton = carousel.querySelector('.carousel-control.next');
            const carouselWrapper = carousel.querySelector('.carousel-wrapper');
            const carouselSlides = carousel.querySelectorAll('.carousel-slide');
            const indicatorsContainer = carousel.querySelector('.carousel-indicators');
            let index = 0;

            function updateCarousel() {
                const totalSlides = carouselSlides.length;
                carouselWrapper.style.transform = `translateX(-${index * 100}%)`;

                prevButton.disabled = index === 0;
                nextButton.disabled = index === totalSlides - 1;

                indicatorsContainer.querySelectorAll('.carousel-indicator').forEach((indicator, i) => {
                    indicator.classList.toggle('active', i === index);
                });
            }

            function createIndicators() {
                indicatorsContainer.innerHTML = '';
                carouselSlides.forEach((_, i) => {
                    const indicator = document.createElement('div');
                    indicator.className = 'carousel-indicator';
                    indicator.addEventListener('click', () => {
                        index = i;
                        updateCarousel();
                    });
                    indicatorsContainer.appendChild(indicator);
                });
            }

            prevButton.addEventListener('click', () => {
                if (index > 0) {
                    index--;
                    updateCarousel();
                }
            });

            nextButton.addEventListener('click', () => {
                if (index < carouselSlides.length - 1) {
                    index++;
                    updateCarousel();
                }
            });

            createIndicators();
            updateCarousel();
        });

        document.querySelectorAll('.js-modal-trigger').forEach(trigger => {
            trigger.addEventListener('click', (event) => {
                event.preventDefault();
                const target = document.getElementById(trigger.dataset.target);
                const imageUrl = trigger.dataset.image;
                const modalImage = target.querySelector('img');
                modalImage.src = imageUrl;
                target.classList.add('is-active');
            });
        });

        document.querySelectorAll('.modal').forEach(modal => {
            const closeButton = modal.querySelector('.modal-close');
            const background = modal.querySelector('.modal-background');

            closeButton.addEventListener('click', () => {
                modal.classList.remove('is-active');
            });

            background.addEventListener('click', () => {
                modal.classList.remove('is-active');
            });
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
        threshold: 1
    });

    if (loadBox) {
        observer.observe(loadBox);
        handleGetData();
    }

})