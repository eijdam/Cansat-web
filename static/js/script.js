// Mobile menu functionality
document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");
    
    const menuToggle = document.getElementById('mobile-menu-toggle');
    const mobileDropdown = document.getElementById('mobile-dropdown');
    
    if (menuToggle && mobileDropdown) {
        console.log("Menu elements found");
        
        // Stop event propagation to prevent immediate closing
        menuToggle.addEventListener('click', function(event) {
            console.log("Button clicked");
            event.stopPropagation();
            mobileDropdown.classList.toggle('show');
        });
        
        mobileDropdown.addEventListener('click', function(event) {
            event.stopPropagation();
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (mobileDropdown.classList.contains('show')) {
                if (!event.target.closest('.mobile-menu-button') && 
                    !event.target.closest('.mobile-dropdown')) {
                    console.log("Closing dropdown");
                    mobileDropdown.classList.remove('show');
                }
            }
        });
    } else {
        console.log("Menu elements not found", {
            menuToggle: menuToggle,
            mobileDropdown: mobileDropdown
        });
    }
});

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.backgroundPositionY = scrolled * 0.5 + 'px';
    }
});

