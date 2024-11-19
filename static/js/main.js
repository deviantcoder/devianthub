document.addEventListener('DOMContentLoaded', () => {

    // Comments Loading

    const postId = document.getElementById('post-id').value
    
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

    commentsLoading()
    
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
                }, 1000);
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




    // USERNAME CHECKER и PREVIEW
    const usernameInput = document.querySelector('input[name="username"]');
    const feedbackSpan = document.getElementById('username-feedback');
    const usernamePreview = document.getElementById('username-preview');
    const saveButton = document.querySelector('button[type="submit"]');

    if (usernameInput && feedbackSpan) {
        usernameInput.addEventListener('input', function () {
            const username = usernameInput.value.trim();

            if (usernamePreview) {
                usernamePreview.textContent = 'u/' + username;

                if (username.length <= 9) {
                    usernamePreview.style.fontSize = "35px";
                } else if (username.length <= 12) {
                    usernamePreview.style.fontSize = "30px";
                } else if (username.length <= 20) {
                    usernamePreview.style.fontSize = "25px";
                }
            }

            const isValidUsername = /^[a-zA-Z0-9]+$/.test(username);

            if (!isValidUsername || username === '') {
                feedbackSpan.innerHTML = '<span class="icon is-small has-text-danger"><i class="fas fa-times"></i></span>';
                if (saveButton) {
                    saveButton.disabled = true;
                }
                return;
            }

            fetch(`/users/check-username/?username=${encodeURIComponent(username)}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    feedbackSpan.innerHTML = '';
                    if (data.available) {
                        feedbackSpan.innerHTML = '<span class="icon is-small has-text-success"><i class="fas fa-check"></i></span>';
                        if (saveButton) {
                            saveButton.disabled = false;
                        }
                    } else {
                        feedbackSpan.innerHTML = '<span class="icon is-small has-text-danger"><i class="fas fa-times"></i></span>';
                        if (saveButton) {
                            saveButton.disabled = true;
                        }
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    feedbackSpan.innerHTML = '<span class="icon is-small has-text-danger"><i class="fas fa-times"></i> Error fetching data</span>';
                    if (saveButton) {
                        saveButton.disabled = true;
                    }
                });
        });
    }

    // PROFILE IMAGE AND BANNER PREVIEW
    const profileImageInput = document.querySelector('input[name="image"]');
    const bannerImageInput = document.querySelector('input[name="banner"]');
    const profileImagePreview = document.getElementById('profile-image-preview');
    const profileBannerPreview = document.getElementById('profile-banner-preview');
    const profileImageError = document.getElementById('profile-image-error');
    const profileBannerError = document.getElementById('profile-banner-error');

    function updateIcon(element, isValid) {
        element.innerHTML = isValid
            ? '<span class="icon is-small has-text-success"><i class="fas fa-check"></i></span>'
            : '<span class="icon is-small has-text-danger"><i class="fas fa-times"></i></span>';
    }

    function isImage(file) {
        return file && file.type.startsWith('image/') && file.type !== 'image/gif';
    }

    if (profileImageInput && profileImagePreview) {
        profileImageInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            profileImageError.innerHTML = ''; // Очистить предыдущее сообщение

            if (isImage(file)) {
                updateIcon(profileImageError, true);

                const reader = new FileReader();
                reader.onload = function () {
                    profileImagePreview.src = reader.result;
                };
                reader.readAsDataURL(file);
            } else {
                updateIcon(profileImageError, false);
                profileImageInput.value = ''; // Сбросить выбранный файл
            }
        });
    }

    if (bannerImageInput && profileBannerPreview) {
        bannerImageInput.addEventListener('change', function (event) {
            const file = event.target.files[0];
            profileBannerError.innerHTML = ''; // Очистить предыдущее сообщение

            if (isImage(file)) {
                updateIcon(profileBannerError, true);

                const reader = new FileReader();
                reader.onload = function () {
                    profileBannerPreview.style.backgroundImage = `url(${reader.result})`;
                };
                reader.readAsDataURL(file);
            } else {
                updateIcon(profileBannerError, false);
                bannerImageInput.value = ''; // Сбросить выбранный файл
            }
        });
    }


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

            console.log('>>>>> ERROR <<<<<')

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
    const textTab = document.getElementById('text-tab');
    const imagesTab = document.getElementById('media-tab');
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

    if (textForm){
        textForm.addEventListener('input', function() {
            if (textForm.querySelector('textarea').value.trim() !== "") {
                disableTabs(textTab);
            } else {
                enableTabs();
            }
        });
    }
    

    if (linkForm) {
        linkForm.addEventListener('input', function() {
            if (linkForm.querySelector('input').value.trim() !== "") {
                disableTabs(linkTab);
            } else {
                enableTabs();
            }
        });
    }

    if (imagesForm) {
        imagesForm.addEventListener('input', checkMediaForms);
    }

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

function toggleDropdown(button) {
    const dropdown = button.closest('.dropdown');
    dropdown.classList.toggle('is-active');
}

document.addEventListener('click', function(event) {
document.querySelectorAll('.dropdown.is-active').forEach(dropdown => {
    if (!dropdown.contains(event.target)) {
        dropdown.classList.remove('is-active');
    }
});
});