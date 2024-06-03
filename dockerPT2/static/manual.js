document.addEventListener("DOMContentLoaded", function() {
    var sections = document.querySelectorAll('.section');
    sections.forEach(function(section) {
        section.addEventListener('click', function() {
            var content = this.querySelector('.content-hidden');
            var toggle = this.querySelector('.toggle');
            if (content.style.maxHeight) {
                content.style.maxHeight = null;
                toggle.classList.remove('active'); // Ensure this line is correctly managing the active class
            } else {
                content.style.maxHeight = content.scrollHeight + "px";
                toggle.classList.add('active'); // Ensure this line is correctly managing the active class
            }
        });
    });

    var navLinks = document.querySelectorAll('.nav-link'); // Select all nav links
    var currentLocation = window.location.pathname; // Get the current path

    navLinks.forEach(function(link) {
        if (link.getAttribute('href') === currentLocation) {
            link.classList.add('active'); // Add 'active' class to the matching link
        }
    });
    
    window.confirmGithub = function() {
        var confirmation = confirm("Do you want to continue to GitHub?");
        if (confirmation) {
            window.open('https://github.com/Ey06ubjk/osint', '_blank');
        }
    };
});