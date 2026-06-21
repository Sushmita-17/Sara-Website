/** Mobile navigation drawer */
(function () {
    document.addEventListener('DOMContentLoaded', function () {
        var toggle = document.getElementById('nav-toggle');
        var drawer = document.getElementById('nav-drawer');
        var overlay = document.getElementById('nav-overlay');
        var closeBtn = document.getElementById('nav-drawer-close');

        if (!toggle || !drawer) return;

        function openNav() {
            drawer.classList.add('open');
            if (overlay) overlay.classList.add('open');
            document.body.classList.add('nav-open');
            toggle.setAttribute('aria-expanded', 'true');
        }

        function closeNav() {
            drawer.classList.remove('open');
            if (overlay) overlay.classList.remove('open');
            document.body.classList.remove('nav-open');
            toggle.setAttribute('aria-expanded', 'false');
        }

        toggle.addEventListener('click', function () {
            if (drawer.classList.contains('open')) closeNav();
            else openNav();
        });
        if (closeBtn) closeBtn.addEventListener('click', closeNav);
        if (overlay) overlay.addEventListener('click', closeNav);
        drawer.querySelectorAll('a').forEach(function (a) {
            a.addEventListener('click', closeNav);
        });

        var navbar = document.querySelector('.navbar');
        if (navbar) {
            window.addEventListener('scroll', function () {
                navbar.classList.toggle('scrolled', window.scrollY > 24);
            }, { passive: true });
        }
    });
})();
