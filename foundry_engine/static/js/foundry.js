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

    // Smooth parallax effect for hero sections
    const parallaxSections = document.querySelectorAll('.section-parallax');

    if (parallaxSections.length > 0) {
        let ticking = false;

        function updateParallax() {
            const scrolled = window.pageYOffset;

            parallaxSections.forEach(section => {
                const background = section.querySelector('.hero-background');
                if (background) {
                    const sectionTop = section.offsetTop;
                    const sectionHeight = section.offsetHeight;

                    // Only apply parallax when section is in or near viewport
                    if (scrolled + window.innerHeight > sectionTop && scrolled < sectionTop + sectionHeight) {
                        // Background moves up slower than scroll (0.3x speed)
                        // Creates depth illusion - background "stays behind" as you scroll
                        const parallaxOffset = (scrolled - sectionTop) * -0.3;
                        background.style.transform = `translate3d(0, ${parallaxOffset}px, 0)`;
                    }
                }
            });
            ticking = false;
        }

        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }, { passive: true });

        // Initial call
        updateParallax();
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
