/**
 * Portfolio Website JavaScript
 * Handles animations, interactions, and dynamic functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Navigation menu toggle for mobile
    const menuToggle = document.getElementById('menu-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (menuToggle && navMenu) {
        menuToggle.addEventListener('click', function() {
            menuToggle.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking anywhere else
        document.addEventListener('click', function(event) {
            if (!navMenu.contains(event.target) && !menuToggle.contains(event.target) && navMenu.classList.contains('active')) {
                navMenu.classList.remove('active');
                menuToggle.classList.remove('active');
            }
        });
    }
    
    // Navbar scroll behavior
    const navbar = document.querySelector('.navbar');
    let scrolled = false;
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            if (!scrolled) {
                navbar.style.padding = '0.7rem 0';
                scrolled = true;
            }
        } else {
            if (scrolled) {
                navbar.style.padding = '1rem 0';
                scrolled = false;
            }
        }
    });
    
    // Animate stats counting
    const stats = document.querySelectorAll('.stat-number');
    
    if (stats.length > 0) {
        const statsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateStats();
                    statsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        stats.forEach(stat => {
            statsObserver.observe(stat);
        });
    }
    
    function animateStats() {
        stats.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-count'));
            let count = 0;
            const duration = 2000; // ms
            const increment = target / (duration / 30);
            
            const counter = setInterval(() => {
                count += increment;
                if (count >= target) {
                    stat.textContent = target;
                    clearInterval(counter);
                } else {
                    stat.textContent = Math.floor(count);
                }
            }, 30);
        });
    }
    
    // Skill bars animation
    const skillBars = document.querySelectorAll('.skill-progress');
    
    if (skillBars.length > 0) {
        const skillsObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.width = entry.target.style.width || '0%';
                    skillsObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        skillBars.forEach(bar => {
            skillsObserver.observe(bar);
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            if (this.getAttribute('href') !== '#') {
                e.preventDefault();
                
                const target = document.querySelector(this.getAttribute('href'));
                
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth'
                    });
                    
                    // Close mobile menu if open
                    if (navMenu && navMenu.classList.contains('active')) {
                        navMenu.classList.remove('active');
                        if (menuToggle) {
                            menuToggle.classList.remove('active');
                        }
                    }
                }
            }
        });
    });
    
    // Fade-in animations for sections
    const fadeElements = document.querySelectorAll('.section-header, .service-card, .project-card, .testimonial-content, .about-image, .about-content, .timeline-item, .pricing-card, .faq-item');
    
    if (fadeElements.length > 0) {
        const fadeObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in');
                    fadeObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        fadeElements.forEach(el => {
            fadeObserver.observe(el);
        });
    }
    
    // Form validation enhancement
    const contactForm = document.querySelector('.contact-form');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            let valid = true;
            const requiredFields = contactForm.querySelectorAll('input[required], textarea[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('invalid');
                    
                    // Remove invalid class when field is focused
                    field.addEventListener('focus', function() {
                        field.classList.remove('invalid');
                    }, { once: true });
                }
            });
            
            // Email validation
            const emailField = contactForm.querySelector('input[type="email"]');
            if (emailField && emailField.value) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailField.value)) {
                    valid = false;
                    emailField.classList.add('invalid');
                    
                    emailField.addEventListener('focus', function() {
                        emailField.classList.remove('invalid');
                    }, { once: true });
                }
            }
            
            if (!valid) {
                e.preventDefault();
            }
        });
    }
    
    // Add CSS class for animations
    document.body.classList.add('loaded');
    
    // Turn off preloader if it exists
    const preloader = document.querySelector('.preloader');
    if (preloader) {
        preloader.classList.add('preloader-hidden');
    }
    
    // Active navigation indicator enhancement
    function enhanceActiveNavItem() {
        const activeNavItem = document.querySelector('.nav-menu li a.active');
        if (activeNavItem) {
            // Add subtle animations when hovering neighboring items
            const navItems = document.querySelectorAll('.nav-menu li a');
            const navParent = activeNavItem.closest('.nav-menu');
            
            navItems.forEach(item => {
                if (!item.classList.contains('active')) {
                    item.addEventListener('mouseenter', () => {
                        activeNavItem.style.transition = 'all 0.3s ease';
                        activeNavItem.style.opacity = '0.7';
                    });
                    
                    item.addEventListener('mouseleave', () => {
                        activeNavItem.style.transition = 'all 0.3s ease';
                        activeNavItem.style.opacity = '1';
                    });
                }
            });
            
            // Create an entrance effect on page load
            activeNavItem.style.opacity = '0';
            activeNavItem.style.transform = 'translateY(5px)';
            
            setTimeout(() => {
                activeNavItem.style.transition = 'all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
                activeNavItem.style.opacity = '1';
                activeNavItem.style.transform = 'translateY(-2px)';
                
                // Add shimmer effect after entrance animation
                setTimeout(() => {
                    activeNavItem.classList.add('shimmer-once');
                    setTimeout(() => {
                        activeNavItem.classList.remove('shimmer-once');
                    }, 1500);
                }, 500);
            }, 100);
            
            // Create a subtle indicator animation
            const createPulseEffect = () => {
                const pulseEl = document.createElement('span');
                pulseEl.className = 'nav-pulse-effect';
                pulseEl.style.position = 'absolute';
                pulseEl.style.bottom = '-2px';
                pulseEl.style.left = '0';
                pulseEl.style.width = '100%';
                pulseEl.style.height = '3px';
                pulseEl.style.backgroundColor = 'rgba(162, 193, 28, 0.7)';
                pulseEl.style.opacity = '0';
                pulseEl.style.borderRadius = '2px';
                
                activeNavItem.appendChild(pulseEl);
                
                setTimeout(() => {
                    pulseEl.style.transition = 'opacity 1s ease';
                    pulseEl.style.opacity = '0.5';
                    
                    setTimeout(() => {
                        pulseEl.style.opacity = '0';
                        setTimeout(() => {
                            if (pulseEl.parentNode) {
                                pulseEl.parentNode.removeChild(pulseEl);
                            }
                        }, 1000);
                    }, 1000);
                }, 10);
            };
            
            // Run pulse effect on load
            createPulseEffect();
            
            // Set up interval for subtle pulse every 3 seconds
            setInterval(createPulseEffect, 3000);
        }
    }
    
    enhanceActiveNavItem();
});
