document.addEventListener('DOMContentLoaded', () => {
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
})