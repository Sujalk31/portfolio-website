document.addEventListener('DOMContentLoaded', function () {

    /* ---------- Background decoration layers ---------- */
    function injectBackgroundLayers() {
        const frag = document.createDocumentFragment();
        ['blob blob-1', 'blob blob-2', 'blob blob-3', 'noise-layer'].forEach(cls => {
            const div = document.createElement('div');
            div.className = cls;
            frag.appendChild(div);
        });
        document.body.appendChild(frag);
    }

    /* ---------- Scroll progress bar ---------- */
    function initScrollProgress() {
        const bar = document.createElement('div');
        bar.className = 'scroll-progress';
        document.body.appendChild(bar);
        window.addEventListener('scroll', () => {
            const h = document.documentElement;
            const scrolled = (h.scrollTop) / (h.scrollHeight - h.clientHeight) * 100;
            bar.style.width = scrolled + '%';
        }, { passive: true });
    }

    /* ---------- Navbar scrolled state ---------- */
    function initNavbarScroll() {
        const nav = document.querySelector('nav');
        if (!nav) return;
        let ticking = false;
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(() => {
                    nav.classList.toggle('scrolled', window.scrollY > 24);
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }

    /* ---------- Hero letter-by-letter split ---------- */
    function initHeroLetters() {
        const heading = document.querySelector('.hero h1, .profile-hero h1');
        if (!heading || heading.dataset.split) return;
        heading.dataset.split = 'true';

        function walk(node) {
            node.childNodes.forEach(child => {
                if (child.nodeType === Node.TEXT_NODE) {
                    const frag = document.createDocumentFragment();
                    [...child.textContent].forEach((ch, i) => {
                        const span = document.createElement('span');
                        span.textContent = ch === ' ' ? '\u00A0' : ch;
                        span.className = 'hero-letter';
                        span.style.animationDelay = `${i * 0.02}s`;
                        frag.appendChild(span);
                    });
                    child.replaceWith(frag);
                } else if (child.nodeType === Node.ELEMENT_NODE) {
                    walk(child);
                }
            });
        }
        walk(heading);
    }

    /* ---------- Scroll reveal, per-section variants ---------- */
    function initScrollReveal() {
        const fadeTargets = document.querySelectorAll('.skill-category, #about, .profile-hero .bio');
        const staggerTargets = document.querySelectorAll('.project-card');
        const timelineItems = document.querySelectorAll('.timeline-item');
        const scaleTargets = document.querySelectorAll('.section-title, .skills-wrap');
        const timeline = document.querySelector('.timeline');

        fadeTargets.forEach(el => el.classList.add('reveal-fade'));
        scaleTargets.forEach(el => el.classList.add('reveal-scale'));

        staggerTargets.forEach((el, i) => {
            el.classList.add('reveal-fade');
            el.style.transitionDelay = `${(i % 3) * 0.12}s`;
        });

        timelineItems.forEach((el, i) => {
            el.classList.add(i % 2 === 0 ? 'reveal-left' : 'reveal-right');
            el.style.transitionDelay = `${i * 0.1}s`;
        });

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        [...fadeTargets, ...staggerTargets, ...timelineItems, ...scaleTargets]
            .forEach(el => observer.observe(el));

        // Timeline vertical line grows once timeline enters view
        if (timeline) {
            const lineObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        timeline.classList.add('line-grown');
                        lineObserver.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15 });
            lineObserver.observe(timeline);
        }
    }

    /* ---------- Mouse-position glow on project cards (throttled via rAF) ---------- */
    function initCardGlow() {
        let scheduled = false;
        let lastCard = null, lastX = 0, lastY = 0;

        document.querySelectorAll('.project-card').forEach(card => {
            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                lastCard = card;
                lastX = ((e.clientX - rect.left) / rect.width) * 100;
                lastY = ((e.clientY - rect.top) / rect.height) * 100;
                if (!scheduled) {
                    scheduled = true;
                    requestAnimationFrame(() => {
                        if (lastCard) {
                            lastCard.style.setProperty('--x', `${lastX}%`);
                            lastCard.style.setProperty('--y', `${lastY}%`);
                        }
                        scheduled = false;
                    });
                }
            });
        });
    }

    /* ---------- Magnetic pull on primary buttons ---------- */
    function initMagneticButtons() {
        document.querySelectorAll('.btn.primary').forEach(btn => {
            btn.addEventListener('mousemove', (e) => {
                const rect = btn.getBoundingClientRect();
                const x = (e.clientX - rect.left - rect.width / 2) * 0.12;
                const y = (e.clientY - rect.top - rect.height / 2) * 0.25;
                btn.style.transform = `translate(${x}px, ${y}px) translateY(-2px)`;
            });
            btn.addEventListener('mouseleave', () => { btn.style.transform = ''; });
        });
    }

    /* ---------- Custom cursor (desktop only) ---------- */
    function initCustomCursor() {
        if (window.matchMedia('(hover: none)').matches || window.innerWidth <= 850) return;

        document.body.classList.add('cursor-active');
        const dot = document.createElement('div');
        dot.className = 'cursor-dot';
        const ring = document.createElement('div');
        ring.className = 'cursor-ring';
        document.body.appendChild(dot);
        document.body.appendChild(ring);

        let mouseX = 0, mouseY = 0, ringX = 0, ringY = 0;

        window.addEventListener('mousemove', (e) => {
            mouseX = e.clientX; mouseY = e.clientY;
            dot.style.transform = `translate(${mouseX}px, ${mouseY}px) translate(-50%, -50%)`;
        });

        function animateRing() {
            ringX += (mouseX - ringX) * 0.18;
            ringY += (mouseY - ringY) * 0.18;
            ring.style.transform = `translate(${ringX}px, ${ringY}px) translate(-50%, -50%)`;
            requestAnimationFrame(animateRing);
        }
        animateRing();

        document.querySelectorAll('.btn, a').forEach(el => {
            el.addEventListener('mouseenter', () => {
                ring.classList.add('hover-btn');
                dot.classList.add('hover-btn');
            });
            el.addEventListener('mouseleave', () => {
                ring.classList.remove('hover-btn');
                dot.classList.remove('hover-btn');
            });
        });

        document.querySelectorAll('.project-card').forEach(el => {
            el.addEventListener('mouseenter', () => {
                ring.classList.add('hover-card');
                dot.classList.add('hover-card');
            });
            el.addEventListener('mouseleave', () => {
                ring.classList.remove('hover-card');
                dot.classList.remove('hover-card');
            });
        });
    }

    /* ---------- Init everything ---------- */
    injectBackgroundLayers();
    initScrollProgress();
    initNavbarScroll();
    initHeroLetters();
    initScrollReveal();
    initCardGlow();
    initMagneticButtons();
    initCustomCursor();
});