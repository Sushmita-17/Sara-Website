/**
 * Shared product images: saraworldwide direct URLs, proxy fallback, unique placeholders.
 */
(function (global) {
    var API = global.SARA_API || ((global.location.origin || 'http://localhost:8000') + '/api');
    var DEFAULT = 'https://saraworldwide.com.np/wp-content/uploads/2024/08/moringa.jpg';
    var STORE = 'https://saraworldwide.com.np/';

    function isSaraUrl(url) {
        return url && url.indexOf('saraworldwide.com.np') !== -1;
    }

    function isAllowed(url) {
        if (!url) return false;
        if (isSaraUrl(url)) return true;
        if (url.indexOf('placehold.co') !== -1) return true;
        if (url.indexOf('fbcdn.net') !== -1) return true;
        return /^https:\/\/scontent[a-z0-9.-]*\.fbcdn\.net\//i.test(url);
    }

    function placeholderUrl(productName) {
        var label = encodeURIComponent((productName || 'Product').substring(0, 40));
        return 'https://placehold.co/400x400/043d2e/ffffff?text=' + label;
    }

    /** Prefer direct saraworldwide URL (fewer 404s); proxy only when needed. */
    function productImg(url, productName) {
        var u = url || DEFAULT;
        if (!isAllowed(u)) u = DEFAULT;
        if (isSaraUrl(u)) return u;
        return API + '/image-proxy?url=' + encodeURIComponent(u);
    }

    function proxy(url) {
        return productImg(url, '');
    }

    function productLink(title, link) {
        if (link) return link;
        return STORE;
    }

    function attachImgFallback(img, productName, originalUrl) {
        if (!img) return;
        var tried = 0;
        img.addEventListener('error', function onErr() {
            tried += 1;
            if (tried === 1 && originalUrl && !isSaraUrl(originalUrl)) {
                img.src = productImg(DEFAULT, productName);
                return;
            }
            if (tried === 2 && isSaraUrl(originalUrl || '')) {
                img.src = API + '/image-proxy?url=' + encodeURIComponent(originalUrl || DEFAULT);
                return;
            }
            img.removeEventListener('error', onErr);
            img.src = placeholderUrl(productName);
        });
    }

    global.SaraImages = {
        API: API,
        DEFAULT: DEFAULT,
        STORE: STORE,
        isSaraUrl: isSaraUrl,
        isAllowed: isAllowed,
        placeholderUrl: placeholderUrl,
        productImg: productImg,
        proxy: proxy,
        productLink: productLink,
        attachImgFallback: attachImgFallback
    };
})(window);
