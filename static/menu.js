document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const floatingMenu = document.querySelector('.floating-menu');
    
    menuToggle.addEventListener('click', function(e) {
        e.stopPropagation();
        floatingMenu.classList.toggle('active');
        
        // Add vibration feedback for mobile devices
        if (navigator.vibrate) {
            navigator.vibrate(50);
        }
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!floatingMenu.contains(event.target)) {
            floatingMenu.classList.remove('active');
        }
    });

    // Close menu when scrolling (optional, remove if not wanted)
    let lastScroll = 0;
    window.addEventListener('scroll', function() {
        const currentScroll = window.pageYOffset;
        if (Math.abs(currentScroll - lastScroll) > 50) {
            floatingMenu.classList.remove('active');
            lastScroll = currentScroll;
        }
    });
}); 