document.addEventListener('DOMContentLoaded', function() {
    const textTab = document.getElementById('text-tab');
    const imagesTab = document.getElementById('media-tab');
    const linkTab = document.getElementById('link-tab');

    const textForm = document.getElementById('text');
    const imagesForm = document.getElementById('media');
    const linkForm = document.getElementById('link');

    const postTypeField = document.getElementById('post-type');
    const tabs = [textTab, imagesTab, linkTab];

    function setActiveTab(activeTab, activeForm, postType) {
        textTab.classList.remove('active');
        imagesTab.classList.remove('active');
        linkTab.classList.remove('active');

        textForm.classList.add('d-none');
        imagesForm.classList.add('d-none');
        linkForm.classList.add('d-none');

        activeTab.classList.add('active');
        activeForm.classList.remove('d-none');

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

    if (textForm) {
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
