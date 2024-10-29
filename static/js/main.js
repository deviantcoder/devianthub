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

document.addEventListener('DOMContentLoaded', function() {
    // Получаем элементы вкладок и формы
    const textTab = document.getElementById('text-tab');
    const imagesTab = document.getElementById('images-tab');
    const linkTab = document.getElementById('link-tab');

    const textForm = document.getElementById('text-form');
    const imagesForm = document.getElementById('images-form');
    const linkForm = document.getElementById('link-form');

    const postTypeField = document.getElementById('post-type');
    const tabs = [textTab, imagesTab, linkTab];

    function setActiveTab(activeTab, activeForm, postType) {
        textTab.classList.remove('is-active');
        imagesTab.classList.remove('is-active');
        linkTab.classList.remove('is-active');

        textForm.classList.add('hidden');
        imagesForm.classList.add('hidden');
        linkForm.classList.add('hidden');

        activeTab.classList.add('is-active');
        activeForm.classList.remove('hidden');

        postTypeField.value = postType;
    }

    function disableTabs(activeTab) {
        tabs.forEach(tab => {
            if (tab !== activeTab) {
                tab.classList.add('disabled');
                tab.style.pointerEvents = 'none';
                tab.style.opacity = '0.5';
            }
        });
    }

    function enableTabs() {
        tabs.forEach(tab => {
            tab.classList.remove('disabled');
            tab.style.pointerEvents = 'auto';
            tab.style.opacity = '1';
        });
    }

    function checkMediaForms() {
        const files = imagesForm.querySelectorAll('input[type="file"]');
        if ([...files].some(fileInput => fileInput.value.trim() !== "")) {
            disableTabs(imagesTab);
        } else {
            enableTabs();
        }
    }

    textForm.addEventListener('input', function() {
        if (textForm.querySelector('textarea').value.trim() !== "") {
            disableTabs(textTab);
        } else {
            enableTabs();
        }
    });

    linkForm.addEventListener('input', function() {
        if (linkForm.querySelector('input').value.trim() !== "") {
            disableTabs(linkTab);
        } else {
            enableTabs();
        }
    });

    imagesForm.addEventListener('input', checkMediaForms);

    document.getElementById('add-media').addEventListener('click', function() {
        const formsetDiv = document.getElementById('media-formset');
        const totalForms = document.getElementById('id_postmedia_set-TOTAL_FORMS');
        const formNum = parseInt(totalForms.value);

        const newForm = document.getElementById('empty-form').innerHTML.replace(/__prefix__/g, formNum);
        formsetDiv.insertAdjacentHTML('beforeend', newForm);

        totalForms.value = formNum + 1;
        checkMediaForms();
    });

    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('delete-media')) {
            const form = event.target.closest('.media-form');
            const deleteField = form.querySelector('input[name$="-DELETE"]');

            if (deleteField) {
                deleteField.value = 'on';
            }

            form.remove();

            const totalForms = document.getElementById('id_postmedia_set-TOTAL_FORMS');
            totalForms.value = document.querySelectorAll('.media-form').length;

            checkMediaForms();
        }
    });

    textTab.addEventListener('click', function() {
        setActiveTab(textTab, textForm, 'text');
    });

    imagesTab.addEventListener('click', function() {
        setActiveTab(imagesTab, imagesForm, 'media');
    });

    linkTab.addEventListener('click', function() {
        setActiveTab(linkTab, linkForm, 'link');
    });
});