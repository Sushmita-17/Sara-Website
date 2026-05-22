var allProducts = [];
var activeFilter = 'all';
var currentPage = 1;
var PER_PAGE = 24;

var I = window.SaraImages;
var C = window.SaraCatalog;

function productImageSrc(url, name) {
    return I.productImg(url, name);
}

function getFilteredProducts() {
    if (activeFilter === 'all') return allProducts;
    return allProducts.filter(function (p) { return p.catLetter === activeFilter; });
}

function renderGrid(products) {
    var grid = document.getElementById('product-grid');
    if (!grid) return;

    var total = products.length;
    var totalPages = Math.max(1, Math.ceil(total / PER_PAGE));
    if (currentPage > totalPages) currentPage = totalPages;
    if (currentPage < 1) currentPage = 1;

    var start = (currentPage - 1) * PER_PAGE;
    var pageItems = products.slice(start, start + PER_PAGE);

    if (!total) {
        grid.innerHTML = '<div class="grid-empty"><h3>No products found</h3><p>Try another category or search.</p></div>';
        renderPagination(0, 0);
        return;
    }

    grid.innerHTML = pageItems.map(function (p) {
        var imgUrl = p.original_image || p.img;
        var imgSrc = productImageSrc(imgUrl, p.name);
        var safeName = p.name.replace(/'/g, "\\'").replace(/"/g, '&quot;');
        var detailUrl = C.productPageUrl(p.name);
        var storeLink = I.productLink(p.name, p.storeLink);
        return '<div class="product-card">' +
            '<a class="p-img" href="' + detailUrl + '" title="View ' + C.esc(p.name) + '">' +
            '<img src="' + imgSrc + '" alt="' + C.esc(p.name) + '" decoding="async" referrerpolicy="no-referrer" data-original="' + C.esc(imgUrl) + '">' +
            '<span class="p-badge">' + C.catLabel(p.catLetter) + '</span></a>' +
            '<div class="p-info"><h3><a href="' + detailUrl + '">' + C.esc(p.name) + '</a></h3>' +
            '<p class="p-cat">' + C.esc(p.cat) + '</p>' +
            '<div class="p-bottom"><span class="price">Rs. ' + (p.price || 450) + '</span>' +
            '<div class="p-card-actions">' +
            '<a href="' + detailUrl + '" class="secondary-btn p-view-btn">View</a>' +
            '<button type="button" class="add-to-cart" onclick="addToCart(\'' + safeName + '\', ' + (p.price || 450) + ')">Add to Cart</button>' +
            '</div></div>' +
            '<a class="p-store-mini" href="' + storeLink + '" target="_blank" rel="noopener">On saraworldwide.com.np →</a>' +
            '</div></div>';
    }).join('');

    grid.querySelectorAll('.p-img img').forEach(function (img) {
        I.attachImgFallback(img, img.alt, img.getAttribute('data-original'));
    });

    renderPagination(total, totalPages);
    var countEl = document.getElementById('product-count');
    if (countEl) {
        countEl.textContent = 'Showing ' + (start + 1) + '–' + Math.min(start + PER_PAGE, total) + ' of ' + total + ' products';
    }
}

function renderPagination(total, totalPages) {
    var el = document.getElementById('pagination');
    if (!el) return;
    if (totalPages <= 1) {
        el.innerHTML = '';
        return;
    }
    var html = '<button class="page-btn" ' + (currentPage === 1 ? 'disabled' : '') + ' onclick="goPage(' + (currentPage - 1) + ')">← Prev</button>';
    var startP = Math.max(1, currentPage - 2);
    var endP = Math.min(totalPages, currentPage + 2);
    if (startP > 1) html += '<button class="page-btn" onclick="goPage(1)">1</button><span class="page-dots">…</span>';
    for (var i = startP; i <= endP; i++) {
        html += '<button class="page-btn' + (i === currentPage ? ' active' : '') + '" onclick="goPage(' + i + ')">' + i + '</button>';
    }
    if (endP < totalPages) html += '<span class="page-dots">…</span><button class="page-btn" onclick="goPage(' + totalPages + ')">' + totalPages + '</button>';
    html += '<button class="page-btn" ' + (currentPage === totalPages ? 'disabled' : '') + ' onclick="goPage(' + (currentPage + 1) + ')">Next →</button>';
    el.innerHTML = html;
}

window.goPage = function (n) {
    currentPage = n;
    renderGrid(getFilteredProducts());
    window.scrollTo({ top: 0, behavior: 'smooth' });
};

function filterProducts(letter) {
    activeFilter = letter;
    currentPage = 1;
    renderGrid(getFilteredProducts());
}
window.filterProducts = filterProducts;

function searchProducts(query) {
    var q = query.toLowerCase();
    currentPage = 1;
    var filtered = allProducts.filter(function (p) {
        return p.name.toLowerCase().includes(q) || p.cat.toLowerCase().includes(q);
    });
    renderGrid(filtered);
}

function mapCatalogItem(p) {
    return {
        name: p.name,
        cat: p.cat,
        catLetter: p.cat_letter || 'A',
        price: p.price || 450,
        img: p.image_url,
        original_image: p.original_image || p.image_url,
        storeLink: p.store_link || I.STORE
    };
}

document.addEventListener('DOMContentLoaded', function () {
    C.loadCatalog()
        .then(function (data) {
            allProducts = (data.products || []).map(mapCatalogItem);
            allProducts.sort(function (a, b) {
                return a.name.localeCompare(b.name, undefined, { sensitivity: 'base' });
            });
            renderGrid(getFilteredProducts());
        })
        .catch(function () {
            var grid = document.getElementById('product-grid');
            if (grid) {
                grid.innerHTML = '<p class="grid-empty">Could not load catalog. Start server: python run.py</p>';
            }
        });

    var globalSearch = document.getElementById('global-search');
    if (globalSearch) {
        globalSearch.addEventListener('input', function (e) {
            var query = e.target.value.trim();
            if (query) searchProducts(query);
            else filterProducts(activeFilter);
        });
    }
});
