// ── Constants ─────────────────────────────────────────────────────────────────
const API = window.SARA_API || ((window.location.origin || 'http://localhost:8000') + '/api');

// ── Auth helpers ──────────────────────────────────────────────────────────────
function getToken() { return localStorage.getItem('sara_token'); }
function getUser()  { return JSON.parse(localStorage.getItem('sara_user') || 'null'); }
function setAuth(token, name, role) {
    localStorage.setItem('sara_token', token);
    localStorage.setItem('sara_user', JSON.stringify({ name, role: role || 'customer' }));
    updateNavAuth();
}
function clearAuth() {
    localStorage.removeItem('sara_token');
    localStorage.removeItem('sara_user');
    updateNavAuth();
}

function updateNavAuth() {
    const user = getUser();
    const loginBtn  = document.getElementById('nav-login');
    const regBtn    = document.getElementById('nav-register');
    const userWrap  = document.getElementById('nav-user');
    const userName  = document.getElementById('nav-username');
    const adminLink = document.getElementById('nav-admin');

    if (user) {
        if (loginBtn)  loginBtn.style.display  = 'none';
        if (regBtn)    regBtn.style.display    = 'none';
        if (userWrap)  userWrap.style.display  = 'flex';
        if (userName)  userName.textContent    = user.name.split(' ')[0];
        
        // Show admin link if role is admin or staff
        if (adminLink) {
            if (user.role === 'admin' || user.role === 'staff') {
                adminLink.style.display = 'block';
            } else {
                adminLink.style.display = 'none';
            }
        }
    } else {
        if (loginBtn)  loginBtn.style.display  = '';
        if (regBtn)    regBtn.style.display    = '';
        if (userWrap)  userWrap.style.display  = 'none';
        if (adminLink) adminLink.style.display = 'none';
    }
}

// ── Global Search ─────────────────────────────────────────────────────────────
function initSearch() {
    const searchInput = document.getElementById('global-search');
    if (!searchInput) return;

    searchInput.addEventListener('input', function(e) {
        const query = e.target.value.toLowerCase().trim();
        const cards = document.querySelectorAll('.product-card');
        
        cards.forEach(card => {
            const name = card.querySelector('h3').textContent.toLowerCase();
            const cat  = card.querySelector('.p-cat').textContent.toLowerCase();
            if (name.includes(query) || cat.includes(query)) {
                card.style.display = '';
            } else {
                card.style.display = 'none';
            }
        });
    });
}
// ── Cart ──────────────────────────────────────────────────────────────────────
var cart = JSON.parse(localStorage.getItem('sara_cart') || '[]');

function saveCart() { localStorage.setItem('sara_cart', JSON.stringify(cart)); }

function addToCart(name, price) {
    var existing = cart.find(function(i){ return i.name === name; });
    if (existing) {
        existing.qty = (existing.qty || 1) + 1;
    } else {
        cart.push({ name: name, price: price, qty: 1 });
    }
    saveCart();
    updateCartBadge();
    showToast(name + ' added to cart!');
}
window.addToCart = addToCart;

function updateCartBadge() {
    var total = cart.reduce(function(s, i){ return s + (i.qty || 1); }, 0);
    document.querySelectorAll('.cart-badge').forEach(function(el){ el.textContent = total; });
}

function renderCartDrawer() {
    var itemsEl = document.getElementById('cart-items');
    var totalEl = document.getElementById('cart-total');
    if (!itemsEl) return;
    if (cart.length === 0) {
        itemsEl.innerHTML = '<p style="padding:20px;color:#aaa;text-align:center;">Your cart is empty 🛒</p>';
        if (totalEl) totalEl.textContent = 'Total: Rs. 0';
        return;
    }
    var total = 0;
    itemsEl.innerHTML = cart.map(function(item, idx) {
        var sub = item.price * (item.qty || 1);
        total += sub;
        return '<div class="cart-item">' +
            '<div><div class="cart-item-name">' + item.name + '</div>' +
            '<small style="color:#aaa">Rs. ' + item.price + ' × ' + (item.qty || 1) + '</small></div>' +
            '<div style="display:flex;align-items:center;gap:8px;">' +
            '<span class="cart-item-price">Rs. ' + sub + '</span>' +
            '<button class="cart-remove" onclick="removeFromCart(' + idx + ')">✕</button>' +
            '</div></div>';
    }).join('');
    if (totalEl) totalEl.textContent = 'Total: Rs. ' + total;
}
window.removeFromCart = function(idx) {
    cart.splice(idx, 1);
    saveCart();
    updateCartBadge();
    renderCartDrawer();
};

function showToast(msg) {
    var t = document.createElement('div');
    t.style.cssText = 'position:fixed;top:80px;right:20px;background:var(--brand-primary);color:white;padding:12px 24px;border-radius:50px;z-index:999999;font-weight:600;box-shadow:var(--shadow-lg);animation:popIn .3s ease';
    t.textContent = msg;
    document.body.appendChild(t);
    setTimeout(function(){ t.remove(); }, 2500);
}

async function handlePayment() {
    const method = document.querySelector('input[name="payment"]:checked').value;
    const total = cart.reduce((s, i) => s + (i.price * (i.qty || 1)), 0);
    const token = getToken();

    if (method === 'qr') {
        alert('Thank you! Our team will verify your payment and process the order shortly.');
        localStorage.removeItem('sara_cart');
        window.location.href = '/';
        return;
    }

    try {
        const res = await fetch(API + '/payment/initiate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + token
            },
            body: JSON.stringify({ amount: total, payment_method: method })
        });

        const data = await res.json();
        if (data.method === 'esewa') {
            const form = document.createElement('form');
            form.setAttribute('method', 'POST');
            form.setAttribute('action', data.url);

            for (const key in data.fields) {
                const hiddenField = document.createElement('input');
                hiddenField.setAttribute('type', 'hidden');
                hiddenField.setAttribute('name', key);
                hiddenField.setAttribute('value', data.fields[key]);
                form.appendChild(hiddenField);
            }

            document.body.appendChild(form);
            form.submit();
        }
    } catch (err) {
        alert('Payment initiation failed. Please try again.');
        console.error(err);
    }
}

// ── On load ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', function() {
    updateNavAuth();
    updateCartBadge();
    initSearch();

    // Cart drawer toggle
    var cartBtn    = document.getElementById('cart-btn');
    var cartDrawer = document.getElementById('cart-drawer');
    var cartClose  = document.getElementById('cart-close');
    if (cartBtn && cartDrawer) {
        cartBtn.addEventListener('click', function() {
            cartDrawer.classList.toggle('hidden');
            renderCartDrawer();
        });
    }
    if (cartClose && cartDrawer) {
        cartClose.addEventListener('click', function(){ cartDrawer.classList.add('hidden'); });
    }

    // Checkout Modal
    const checkoutBtn = document.querySelector('.checkout-btn');
    const checkoutModal = document.getElementById('checkout-modal');
    const checkoutClose = document.getElementById('checkout-close');
    const payNowBtn = document.getElementById('pay-now-btn');
    const qrDisplay = document.getElementById('qr-display');

    if (checkoutBtn && checkoutModal) {
        checkoutBtn.addEventListener('click', function() {
            if (!getUser()) {
                window.location.href = 'login.html?next=index.html';
                return;
            }
            if (cart.length === 0) return alert('Your cart is empty!');
            
            const total = cart.reduce((s, i) => s + (i.price * (i.qty || 1)), 0);
            document.getElementById('checkout-total-val').textContent = 'Rs. ' + total;
            checkoutModal.classList.remove('hidden');
        });
    }

    if (checkoutClose) {
        checkoutClose.addEventListener('click', () => checkoutModal.classList.add('hidden'));
    }

    // Toggle QR display
    document.querySelectorAll('input[name="payment"]').forEach(radio => {
        radio.addEventListener('change', (e) => {
            qrDisplay.style.display = e.target.value === 'qr' ? 'block' : 'none';
            payNowBtn.textContent = e.target.value === 'qr' ? 'I Have Paid (Verify)' : 'Confirm & Pay';
        });
    });

    if (payNowBtn) {
        payNowBtn.addEventListener('click', handlePayment);
    }

    // Logout
    var logoutBtn = document.getElementById('nav-logout');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            clearAuth();
            window.location.href = '/';
        });
    }
});
