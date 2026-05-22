/**
 * Shared catalog loader — DB + gallery with name-matched original images.
 */
(function (global) {
    var API = global.SARA_API || ((global.location.origin || 'http://localhost:8000') + '/api');
    var cache = null;
    var loadPromise = null;

    var CAT_LABELS = {
        A: 'Organic Food',
        B: 'Natural Beauty',
        C: 'Spiritual Wellness',
        D: 'Sara Nursery'
    };

    function esc(s) {
        return String(s)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function productPageUrl(name) {
        return 'product.html?name=' + encodeURIComponent(name || '');
    }

    function loadCatalog(force) {
        if (cache && !force) return Promise.resolve(cache);
        if (loadPromise && !force) return loadPromise;
        loadPromise = fetch(API + '/catalog')
            .then(function (r) {
                if (!r.ok) throw new Error('catalog');
                return r.json();
            })
            .then(function (data) {
                cache = data;
                return data;
            })
            .catch(function () {
                return fetch(API + '/products')
                    .then(function (r) { return r.ok ? r.json() : []; })
                    .then(function (categories) {
                        var products = [];
                        var letters = {
                            'Category A: Food': 'A',
                            'Category B: Natural Cosmetics': 'B',
                            'Category C: Spirituals': 'C',
                            'Category D: Sara Nursery': 'D'
                        };
                        (categories || []).forEach(function (cat) {
                            var letter = letters[cat.name] || 'A';
                            (cat.children || []).forEach(function (sub) {
                                (sub.products || []).forEach(function (p) {
                                    products.push({
                                        name: p.name,
                                        cat: sub.name,
                                        cat_letter: letter,
                                        price: p.price || 450,
                                        image_url: p.original_image || p.image_url,
                                        original_image: p.original_image || p.image_url,
                                        store_link: p.store_link
                                    });
                                });
                            });
                        });
                        cache = { products: products, total: products.length };
                        return cache;
                    });
            });
        return loadPromise;
    }

    function catLabel(letter) {
        return CAT_LABELS[letter] || letter;
    }

    global.SaraCatalog = {
        API: API,
        loadCatalog: loadCatalog,
        getCache: function () { return cache; },
        productPageUrl: productPageUrl,
        catLabel: catLabel,
        esc: esc
    };
})(window);
