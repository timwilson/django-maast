// Toggle the mobile menu open and closed
$(document).ready(function () {
    const menuButton = $('[aria-controls="mobile-menu"]');
    const mobileMenu = $('#mobile-menu');
    const openIcon = menuButton.find('.block'); // Hamburger icon
    const closeIcon = menuButton.find('.hidden'); // X icon

    // Hide the mobile menu initially
    mobileMenu.hide();

    menuButton.click(function () {
        // Toggle the mobile menu
        mobileMenu.toggle();

        // Swap the visibility of the hamburger and X icons
        openIcon.toggleClass('hidden');
        closeIcon.toggleClass('hidden');
    });
});

// Highlight the current navbar link if the browser is on that page.
$(document).ready(function() {
    const currentClasses = "bg-gray-900 text-white";
    const defaultClasses = "text-gray-300 hover:bg-gray-700 hover:text-white";

    // Iterate over each link in both the desktop and mobile navbars
    $('#desktop-nav a, #mobile-nav a').each(function() {
        const link = $(this); // Current link
        const href = link.attr('href'); // href of the link

        // Check if the link's href matches the current URL
        if (window.location.pathname === href) {
            // Apply the "current" classes and remove the "default" classes
            link.addClass(currentClasses).removeClass(defaultClasses);
        } else {
            // Ensure the link has the "default" classes
            link.removeClass(currentClasses).addClass(defaultClasses);
        }
    });
});
