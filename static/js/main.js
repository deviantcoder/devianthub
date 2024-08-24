document.addEventListener('DOMContentLoaded', () => {
    // Navbar
    const burgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    if (burgers.length > 0) {
        burgers.forEach(burger => {
            burger.addEventListener('click', () => {
                const target = document.getElementById(burger.dataset.target);
                burger.classList.toggle('is-active');
                target.classList.toggle('is-active');
            });
        });
    }

    // Single image post modal
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

    // Close modal
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

    // Carousels
    document.querySelectorAll('.carousel').forEach(carousel => {
        const prevButton = carousel.querySelector('.carousel-control.prev');
        const nextButton = carousel.querySelector('.carousel-control.next');
        const carouselWrapper = carousel.querySelector('.carousel-wrapper');
        const carouselSlides = carousel.querySelectorAll('.carousel-slide');
        const indicatorsContainer = carousel.querySelector('.carousel-indicators');
        const modalTriggers = carousel.querySelectorAll('.js-modal-trigger');
        const modal = carousel.querySelector('.modal');
        const modalImage = modal.querySelector('img');
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

        // Open modal with clicked image
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', (event) => {
                event.preventDefault();
                const imageUrl = trigger.dataset.image;
                modalImage.src = imageUrl;
                modal.classList.add('is-active');
            });
        });

        // Close modal on background or close button click
        modal.querySelector('.modal-background').addEventListener('click', () => {
            modal.classList.remove('is-active');
        });

        modal.querySelector('.modal-close').addEventListener('click', () => {
            modal.classList.remove('is-active');
        });

        createIndicators();
        updateCarousel();
    });

    // Tabs
    const tabButtons = document.querySelectorAll('#tab-buttons li');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(btn => btn.classList.remove('is-active'));
            tabContents.forEach(content => content.classList.remove('active'));

            button.classList.add('is-active');
            document.getElementById(button.dataset.tab).classList.add('active');
        });
    });
});

// Toggle description function
function toggleDescription(ruleId) {
    const description = document.getElementById(ruleId);
    const icon = description.previousElementSibling.querySelector('.toggle-icon');
    
    if (description.style.display === "none" || description.style.display === "") {
        description.style.display = "block";
        icon.textContent = "−";
    } else {
        description.style.display = "none";
        icon.textContent = "+";
    }
}
