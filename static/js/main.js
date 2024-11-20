document.addEventListener('DOMContentLoaded', () => {

    // Navbar
    // const burgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    // if (burgers.length > 0) {
    //     burgers.forEach(burger => {
    //         burger.addEventListener('click', () => {
    //             const target = document.getElementById(burger.dataset.target);
    //             burger.classList.toggle('is-active');
    //             target.classList.toggle('is-active');
    //         });
    //     });
    // }
    const burger = document.querySelector('.navbar-burger');
    const menu = document.querySelector('.navbar-menu');

    if (burger && menu) {
        burger.addEventListener('click', () => {
            burger.classList.toggle('is-active');
            menu.classList.toggle('is-active');
        });
    }
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

