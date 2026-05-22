const API_BASE = window.SARA_API || ((window.location.origin || 'http://localhost:8000') + '/api');
var I = window.SaraImages || { productImg: function(u,n){ return u; }, DEFAULT: 'https://saraworldwide.com.np/wp-content/uploads/2024/08/moringa.jpg' };

// Cart drawer toggle
window.addEventListener('DOMContentLoaded', function() {
    var cartBtn = document.getElementById('cart-btn');
    if (cartBtn) {
        cartBtn.addEventListener('click', function() {
            var drawer = document.getElementById('cart-drawer');
            if (drawer) drawer.classList.toggle('hidden');
        });
    }
});

// Category filter (UI only — toggles active tab)
window.filterCategory = function(cat) {
    document.querySelectorAll('.cat-tab').forEach(function(btn) {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    // TODO: filter product cards by category
};

function saraImg(url, name) {
    return I.productImg(url || I.DEFAULT, name || '');
}

// Hardcoded fallback (saraworldwide.com.np images only)
const FALLBACK_PRODUCTS = [
    { name: "Chia seed", category: "Seeds", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2017/04/unnamed-1-scaled.jpg'), price: 350 },
    { name: "Moringa powder", category: "Powder", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2024/08/moringa.jpg'), price: 450 },
    { name: "Ashwagandha powder", category: "Powder", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2017/11/ashawagandha-powder.jpg'), price: 550 },
    { name: "Black seed oil", category: "Oil", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2017/09/black-scaled-e1745215640698.jpg'), price: 650 },
    { name: "Coconut oil", category: "Oil", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2017/11/coconut-oil-latest.jpg'), price: 400 },
    { name: "Lavender oil", category: "Essential Oil", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2021/07/Lavender-Oil_front.png'), price: 800 },
    { name: "Wild Honey", category: "Himali Products", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2025/02/wh.jpg'), price: 1200 },
    { name: "Shilajit", category: "Himali Products", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2024/06/shw.jpg'), price: 2500 },
    { name: "Aloevera fresh juice", category: "Juices & Detox Water", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2022/06/287329122_4928240767282481_4667855119876077382_n-1.jpg'), price: 300 },
    { name: "Spirulina powder", category: "Powder", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2017/04/index.jpg'), price: 700 },
    { name: "Turmeric powder", category: "Powder", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2020/08/wild-turmeric-new...............jpg'), price: 200 },
    { name: "Brahmi Powder", category: "Powder", img: saraImg('https://saraworldwide.com.np/wp-content/uploads/2019/09/brahami-powder.png'), price: 300 }
];

var allFeaturedItems = [];
var featuredShown = 0;
var featuredCatFilter = 'all';
var FEATURED_PAGE = 24;
var Catalog = window.SaraCatalog;

function escHtml(s) {
    return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function getFeaturedFiltered() {
    if (featuredCatFilter === 'all') return allFeaturedItems;
    return allFeaturedItems.filter(function (item) {
        return item.catLetter === featuredCatFilter;
    });
}

function renderFeaturedBatch(grid, append) {
    var pool = getFeaturedFiltered();
    if (!append) {
        grid.innerHTML = '';
        featuredShown = 0;
    }
    var next = pool.slice(featuredShown, featuredShown + FEATURED_PAGE);

    next.forEach(function(item) {
        var card = document.createElement('div');
        card.className = 'product-card';
        var imgRaw = item.original_image || item.img;
        var imgUrl = saraImg(imgRaw, item.name);
        var detailUrl = Catalog ? Catalog.productPageUrl(item.name) : ('product.html?name=' + encodeURIComponent(item.name));
        var storeLink = item.link || 'https://saraworldwide.com.np/';
        var badge = item.badge || (Catalog ? Catalog.catLabel(item.catLetter) : '');

        card.innerHTML =
            '<a href="' + escHtml(detailUrl) + '" class="product-card-link" title="' + escHtml(item.name) + '">' +
            '<div class="p-img"><img src="' + imgUrl + '" alt="' + escHtml(item.name) + '" decoding="async" referrerpolicy="no-referrer">' +
            (badge ? '<span class="p-badge">' + escHtml(badge) + '</span>' : '') +
            '</div>' +
            '<div class="p-info"><h3>' + escHtml(item.name) + '</h3>' +
            (badge ? '<p class="p-cat">' + escHtml(badge) + '</p>' : '') +
            '<span class="price">Rs. ' + (item.price || 450) + '</span>' +
            '<span class="catalog-card-link">View product photo →</span>' +
            '</div></a>' +
            '<div class="p-card-actions featured-card-actions">' +
            '<button type="button" class="add-to-cart" data-name="' + escHtml(item.name) + '" data-price="' + (item.price || 450) + '">Add to Cart</button>' +
            '</div>';
        grid.appendChild(card);
        var btn = card.querySelector('.add-to-cart');
        if (btn && window.addToCart) {
            btn.addEventListener('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                window.addToCart(item.name, item.price || 450);
            });
        }
        var imgEl = card.querySelector('img');
        if (imgEl && I.attachImgFallback) I.attachImgFallback(imgEl, item.name, imgRaw);
    });

    featuredShown += next.length;

    // Update or create load-more button
    var loadMoreBtn = document.getElementById('featured-load-more');
    if (!loadMoreBtn) {
        var ctaDiv = document.querySelector('.index-featured-cta');
        if (ctaDiv) {
            loadMoreBtn = document.createElement('button');
            loadMoreBtn.type = 'button';
            loadMoreBtn.className = 'cta-btn';
            loadMoreBtn.id = 'featured-load-more';
            loadMoreBtn.textContent = 'Load more products';
            loadMoreBtn.style.marginRight = '12px';
            loadMoreBtn.addEventListener('click', function() { renderFeaturedBatch(grid, true); });
            ctaDiv.insertBefore(loadMoreBtn, ctaDiv.firstChild);
        }
    }
    var pool = getFeaturedFiltered();
    if (loadMoreBtn) {
        loadMoreBtn.style.display = featuredShown >= pool.length ? 'none' : 'inline-flex';
    }

    var countEl = document.getElementById('featured-count');
    if (!countEl) {
        var header = document.querySelector('#featured .section-header');
        if (header) {
            countEl = document.createElement('p');
            countEl.id = 'featured-count';
            countEl.className = 'section-sub';
            countEl.style.fontSize = '13px';
            countEl.style.opacity = '0.7';
            header.appendChild(countEl);
        }
    }
    if (countEl) {
        countEl.textContent = 'Showing ' + featuredShown + ' of ' + pool.length + ' in this collection';
    }
}

function initFeaturedCategoryTabs() {
    var tabs = document.getElementById('featured-cat-tabs');
    if (!tabs) return;
    tabs.addEventListener('click', function (e) {
        var btn = e.target.closest('.featured-cat');
        if (!btn) return;
        featuredCatFilter = btn.getAttribute('data-cat') || 'all';
        featuredShown = 0;
        tabs.querySelectorAll('.featured-cat').forEach(function (b) {
            b.classList.remove('active');
        });
        btn.classList.add('active');
        var grid = document.getElementById('main-product-grid');
        if (grid) renderFeaturedBatch(grid, false);
    });
}

function loadEcomProducts() {
    var grid = document.getElementById('main-product-grid');
    if (!grid) return;

    initFeaturedCategoryTabs();

    var load = Catalog && Catalog.loadCatalog
        ? Catalog.loadCatalog()
        : fetch(API_BASE + '/catalog').then(function (r) { return r.ok ? r.json() : null; });

    load.then(function (data) {
        if (!data || !data.products) {
            FALLBACK_PRODUCTS.forEach(function (p) {
                allFeaturedItems.push({
                    name: p.name,
                    img: p.img,
                    original_image: p.img,
                    badge: p.category,
                    catLetter: 'A',
                    link: 'https://saraworldwide.com.np/',
                    price: p.price || 450
                });
            });
        } else {
            data.products.forEach(function (p) {
                allFeaturedItems.push({
                    name: p.name,
                    img: p.original_image || p.image_url,
                    original_image: p.original_image || p.image_url,
                    badge: Catalog ? Catalog.catLabel(p.cat_letter) : p.cat,
                    catLetter: p.cat_letter || 'A',
                    link: p.store_link || 'https://saraworldwide.com.np/',
                    price: p.price || 450
                });
            });
        }
        renderFeaturedBatch(grid, false);
    }).catch(function () {
        renderFeaturedBatch(grid, false);
    });
}

// Cart
var cart = [];
window.addToCart = function(name, price) {
    cart.push({ name: name, price: price });
    updateCartBadge();
    showCartNotification(name);
};

function updateCartBadge() {
    var badge = document.getElementById('cart-badge');
    if (badge) badge.textContent = cart.length;
}

function showCartNotification(name) {
    var notif = document.createElement('div');
    notif.style.cssText = 'position:fixed;top:80px;right:20px;background:#2e7d32;color:white;padding:12px 20px;border-radius:12px;z-index:999999;font-weight:600;animation:slideIn 0.3s ease';
    notif.textContent = name + ' added to cart!';
    document.body.appendChild(notif);
    setTimeout(function() { notif.remove(); }, 2500);
}

// Initialize homepage catalog (chatbot: js/chatbot-widget.js)
window.addEventListener('DOMContentLoaded', function() {
    loadEcomProducts();
});
