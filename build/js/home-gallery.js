/**
 * Homepage: hero collage, product slider, category card backgrounds
 */
(function (win) {
    'use strict';

    var I = win.SaraImages || {};
    var API = win.SARA_API || I.API || ((win.location.origin || 'http://localhost:8000') + '/api');

    function productImg(url, name) {
        if (I.productImg) return I.productImg(url, name);
        return url || '';
    }

    function escapeHtml(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    function setCategoryBg(id, url) {
        var el = document.getElementById(id);
        if (!el || !url) return;
        var bg = el.querySelector('.category-card-bg');
        if (bg) bg.style.backgroundImage = 'url("' + productImg(url) + '")';
    }

    function buildHeroCollage(heroItems) {
        var root = document.getElementById('hero-collage');
        if (!root || !heroItems.length) return;

        var main = heroItems[0];
        var side = heroItems.slice(1, 4);
        while (side.length < 3 && heroItems.length) {
            side.push(heroItems[side.length % heroItems.length]);
        }

        root.innerHTML =
            '<div class="hero-collage-main">' +
            '<img src="' + productImg(main.url, main.title) + '" alt="' + escapeHtml(main.title) + '" width="160" height="168" decoding="async">' +
            '<span class="hero-collage-caption">' + escapeHtml(main.title) + '</span></div>' +
            '<div class="hero-collage-side">' +
            side.map(function (item, i) {
                return '<div class="hero-collage-tile tile-' + (i + 1) + '">' +
                    '<img src="' + productImg(item.url, item.title) + '" alt="' + escapeHtml(item.title) + '" width="80" height="52" decoding="async"></div>';
            }).join('') +
            '</div>';
    }

    function marqueeCard(item) {
        var src = productImg(item.url, item.name);
        var detail = 'product.html?name=' + encodeURIComponent(item.name);
        var tag = item.tag ? '<span class="marquee-item-tag">' + escapeHtml(item.tag) + '</span>' : '';
        return '<a class="marquee-item" href="' + detail + '" title="' + escapeHtml(item.name) + '">' +
            '<div class="marquee-item-img-wrap">' + tag +
            '<img src="' + src + '" alt="' + escapeHtml(item.name) + '" decoding="async" referrerpolicy="no-referrer">' +
            '</div><div class="marquee-item-body">' +
            '<span class="marquee-item-label">' + escapeHtml(item.name) + '</span>' +
            '<span class="marquee-item-cta">View product</span></div></a>';
    }

    function buildMarquee() {
        var track = document.getElementById('marquee-track');
        var highlights = win.SARA_MARQUEE || [];
        if (!track || !highlights.length) return;
        try {
            var oneSet = highlights.map(marqueeCard).join('');
            track.innerHTML = oneSet + oneSet + oneSet;
            var sets = track.querySelectorAll('.marquee-item').length / highlights.length;
            if (sets >= 3) {
                track.style.setProperty('--marquee-end', '-' + (100 / sets) + '%');
            }
        } catch (err) {
            console.warn('Marquee build skipped:', err);
        }
    }

    function init() {
        buildMarquee();

        fetch(API + '/gallery')
            .then(function (r) { return r.ok ? r.json() : Promise.reject(new Error('gallery')); })
            .then(function (data) {
                if (data.hero && data.hero.length) buildHeroCollage(data.hero);
                buildMarquee();
                if (data.categories) {
                    setCategoryBg('cat-food', data.categories.food);
                    setCategoryBg('cat-beauty', data.categories.beauty);
                    setCategoryBg('cat-spiritual', data.categories.spiritual);
                    if (data.categories.nursery) setCategoryBg('cat-nursery', data.categories.nursery);
                }
            })
            .catch(function () {
                var fallback = (win.SARA_MARQUEE && win.SARA_MARQUEE[0])
                    ? { title: win.SARA_MARQUEE[0].name, url: win.SARA_MARQUEE[0].url }
                    : { title: 'Moringa Powder', url: 'https://saraworldwide.com.np/wp-content/uploads/2017/04/fina.jpg' };
                buildHeroCollage([fallback]);
            });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window);
