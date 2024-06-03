document.addEventListener("DOMContentLoaded", function() {
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

    window.confirmMitre = function() {
        var confirmation = confirm("Do you want to continue to MITRE ATT&CK Reconnaissance?");
        if (confirmation) {
            window.open('https://attack.mitre.org/tactics/TA0043/', '_blank');
        }
    };
});
