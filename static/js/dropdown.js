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