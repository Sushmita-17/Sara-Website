(function () {
    var I = window.SaraImages;
    var C = window.SaraCatalog;
    var API = C.API;

    function qs(name) {
        return new URLSearchParams(window.location.search).get(name);
    }

    function render(p) {
        var root = document.getElementById('product-detail');
        if (!root || !p) return;

        var img = p.original_image || p.image_url || I.DEFAULT;
        var imgSrc = I.productImg(img, p.name);
        var store = I.productLink(p.name, p.store_link);
        var benefits = p.benefits ? '<div class="pd-block"><h3>Benefits</h3><p>' + C.esc(p.benefits) + '</p></div>' : '';
        var effects = p.effects ? '<div class="pd-block"><h3>Effects</h3><p>' + C.esc(p.effects) + '</p></div>' : '';

        document.title = p.name + ' | Sara Foods';
        root.innerHTML =
            '<nav class="pd-breadcrumb"><a href="/">Home</a> / <a href="products.html">Shop</a> / <span>' + C.esc(p.name) + '</span></nav>' +
            '<div class="pd-layout">' +
            '<div class="pd-gallery">' +
            '<img id="pd-main-img" src="' + imgSrc + '" alt="' + C.esc(p.name) + '" decoding="async" referrerpolicy="no-referrer">' +
            '<p class="pd-img-caption">Official photo from saraworldwide.com.np</p></div>' +
            '<div class="pd-info">' +
            '<span class="pd-cat">' + C.esc(p.category || '') + '</span>' +
            '<h1>' + C.esc(p.name) + '</h1>' +
            '<p class="pd-price">Rs. ' + (p.price || 450) + '</p>' +
            '<div class="pd-actions">' +
            '<button type="button" class="cta-btn" id="pd-add-cart">Add to Cart — Rs. ' + (p.price || 450) + '</button>' +
            '<a href="' + C.esc(store) + '" class="secondary-btn pd-store-link" target="_blank" rel="noopener">View on saraworldwide.com.np →</a>' +
            '</div>' + benefits + effects +
            '</div></div>';

        var mainImg = document.getElementById('pd-main-img');
        if (mainImg) I.attachImgFallback(mainImg, p.name, img);

        var addBtn = document.getElementById('pd-add-cart');
        if (addBtn && window.addToCart) {
            addBtn.addEventListener('click', function () {
                window.addToCart(p.name, p.price || 450);
            });
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var name = qs('name');
        var root = document.getElementById('product-detail');
        if (!name) {
            if (root) root.innerHTML = '<p class="grid-empty">No product selected. <a href="products.html">Browse shop</a></p>';
            return;
        }

        fetch(API + '/product/' + encodeURIComponent(name))
            .then(function (r) {
                if (!r.ok) throw new Error();
                return r.json();
            })
            .then(render)
            .catch(function () {
                return C.loadCatalog().then(function (data) {
                    var key = name.trim().toLowerCase();
                    var found = (data.products || []).find(function (p) {
                        return p.name.trim().toLowerCase() === key;
                    });
                    if (found) {
                        render({
                            name: found.name,
                            category: found.cat,
                            price: found.price,
                            image_url: found.original_image,
                            original_image: found.original_image,
                            store_link: found.store_link,
                            benefits: found.benefits,
                            effects: found.effects
                        });
                    } else if (root) {
                        root.innerHTML = '<p class="grid-empty">Product not found. <a href="products.html">Back to shop</a></p>';
                    }
                });
            });
    });
})();
