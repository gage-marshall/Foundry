// Foundry Engine - Core JavaScript
// Minimal utilities and enhancements

(function() {
    'use strict';

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Lazy load images
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // Simple parallax effect for hero sections
    const parallaxSections = document.querySelectorAll('.section-parallax');
    if (parallaxSections.length > 0) {
        window.addEventListener('scroll', () => {
            parallaxSections.forEach(section => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * 0.5;
                section.style.transform = `translate3d(0, ${rate}px, 0)`;
            });
        });
    }

    // CSRF token helper for forms
    window.getCSRFToken = function() {
        const cookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrf_token='));
        return cookie ? cookie.split('=')[1] : null;
    };

    // Contact form success handler
    document.body.addEventListener('htmx:afterRequest', function(event) {
        if (event.detail.target.id === 'contact-message') {
            const xhr = event.detail.xhr;
            if (xhr.status === 200) {
                const form = event.detail.elt;
                if (form && form.tagName === 'FORM') {
                    form.reset();
                }
            }
        }
    });

    console.log('Foundry Engine initialized');
})();
