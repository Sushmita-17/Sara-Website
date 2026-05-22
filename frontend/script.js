const API_BASE = "http://localhost:8000/api";

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

// Hardcoded product fallback (works without MySQL)
const FALLBACK_PRODUCTS = [
    { name: "Chia Seed", category: "Seeds", img: "bg.png", price: 350 },
    { name: "Moringa Powder", category: "Powder", img: "prod_moringa.png", price: 450 },
    { name: "Ashwagandha Powder", category: "Powder", img: "bg.png", price: 550 },
    { name: "Black Seed Oil", category: "Oil", img: "bg.png", price: 650 },
    { name: "Coconut Oil", category: "Oil", img: "bg.png", price: 400 },
    { name: "Lavender Oil", category: "Essential Oil", img: "bg.png", price: 800 },
    { name: "Wild Honey", category: "Himali Products", img: "bg.png", price: 1200 },
    { name: "Shilajit", category: "Himali Products", img: "bg.png", price: 2500 },
    { name: "Aloevera Fresh Juice", category: "Juices & Detox Water", img: "bg.png", price: 300 },
    { name: "Spirulina Powder", category: "Powder", img: "bg.png", price: 700 },
    { name: "Turmeric Powder", category: "Powder", img: "bg.png", price: 200 },
    { name: "Brahmi Powder", category: "Powder", img: "bg.png", price: 300 }
];

function loadEcomProducts() {
    var grid = document.getElementById('main-product-grid');
    if (!grid) return;

    // Try API first
    fetch(API_BASE + '/products')
        .then(function(res) {
            if (!res.ok) throw new Error('API error');
            return res.json();
        })
        .then(function(categories) {
            if (!Array.isArray(categories)) throw new Error('Not an array');
            grid.innerHTML = '';
            var count = 0;
            categories.forEach(function(cat) {
                cat.children.forEach(function(sub) {
                    sub.products.slice(0, 3).forEach(function(p) {
                        if (count >= 12) return;
                        count++;
                        var card = document.createElement('div');
                        card.className = 'product-card';
                        card.innerHTML = '<div class="p-img"><img src="bg.png" alt="' + p.name + '"></div>' +
                            '<div class="p-info"><h3>' + p.name + '</h3><p>' + sub.name + '</p>' +
                            '<div class="p-bottom"><span class="price">Rs. 450</span>' +
                            '<button class="add-to-cart">Add to Cart</button></div></div>';
                        grid.appendChild(card);
                    });
                });
            });
        })
        .catch(function() {
            // Fallback: show hardcoded products
            grid.innerHTML = '';
            FALLBACK_PRODUCTS.forEach(function(p) {
                var card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = '<div class="p-img"><img src="' + p.img + '" alt="' + p.name + '"></div>' +
                    '<div class="p-info"><h3>' + p.name + '</h3><p>' + p.category + '</p>' +
                    '<div class="p-bottom"><span class="price">Rs. ' + p.price + '</span>' +
                    '<button class="add-to-cart" onclick="addToCart(\'' + p.name + '\', ' + p.price + ')">Add to Cart</button></div></div>';
                grid.appendChild(card);
            });
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

// Chatbot
function initChatbot() {
    var chatToggle = document.getElementById('chat-toggle');
    var chatWidget = document.getElementById('chat-widget');
    var closeChat = document.getElementById('close-chat');
    var userInput = document.getElementById('user-input');
    var sendBtn = document.getElementById('send-btn');
    var typingIndicator = document.getElementById('typing-indicator');
    var chatMessages = document.getElementById('chat-messages');

    if (!chatToggle || !chatWidget) {
        console.error('Chat elements not found!');
        return;
    }

    chatToggle.addEventListener('click', function() {
        chatWidget.style.display = 'flex';
        chatWidget.classList.remove('hidden');
        chatToggle.style.display = 'none';
    });

    closeChat.addEventListener('click', function() {
        chatWidget.style.display = 'none';
        chatWidget.classList.add('hidden');
        chatToggle.style.display = 'flex';
    });

    function addMessage(text, isBot) {
        var msgDiv = document.createElement('div');
        msgDiv.className = 'message ' + (isBot !== false ? 'bot-message' : 'user-message');
        msgDiv.innerHTML = text;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function showTyping(show) {
        if (typingIndicator) typingIndicator.style.display = show ? 'block' : 'none';
    }

    function handleSearch(query) {
        var q = query.toLowerCase().trim();
        showTyping(true);

        // Small talk
        if (q === 'hi' || q === 'hello' || q === 'hey') {
            setTimeout(function() {
                addMessage("Hi there! I'm doing great, thank you! 😊 How can I help you with Sara World Business products today?");
                showTyping(false);
            }, 800);
            return;
        }

        if (q.includes('how are you')) {
            setTimeout(function() {
                addMessage("I'm perfectly fine and ready to help! Feel free to ask me about our organic products, location, or anything else! 🌿");
                showTyping(false);
            }, 800);
            return;
        }

        // Location with Map
        if (q.includes('location') || q.includes('where') || q.includes('contact') || q.includes('info')) {
            setTimeout(function() {
                addMessage('<strong>Sara World Business Pvt. Ltd.</strong><br>' +
                    '📍 Kalanki-14, Kathmandu, Nepal<br>' +
                    '📞 +977 1 5225181 | +977 9851105234<br>' +
                    '📧 info@saraworldwide.com.np<br>' +
                    '🌐 <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">Website</a> | ' +
                    '<a href="https://www.facebook.com/saraworldwide.com.np/" target="_blank">Facebook</a>' +
                    '<div style="margin-top:10px;border-radius:10px;overflow:hidden;">' +
                    '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.8344158226!2d85.2818!3d27.6932!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb18635848c087%3A0x67399426f4370597!2sKalanki%2C%20Kathmandu!5e0!3m2!1sen!2snp" ' +
                    'width="100%" height="150" style="border:0;" allowfullscreen="" loading="lazy"></iframe></div>');
                showTyping(false);
            }, 800);
            return;
        }

        // Stats
        if (q.includes('total') || q.includes('how many') || q.includes('stats')) {
            fetch(API_BASE + '/products/stats')
                .then(function(r) { return r.json(); })
                .then(function(stats) {
                    addMessage('We have <strong>' + stats.total_products + ' products</strong> across ' + stats.total_categories + ' categories!<br>' +
                        'See them all on our <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">website</a>!');
                })
                .catch(function() {
                    addMessage('We have over <strong>300+ products</strong> across 4 main categories — Food, Cosmetics, Spirituals & Nursery.<br>' +
                        'See them all on our <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">website</a> & <a href="https://www.facebook.com/saraworldwide.com.np/" target="_blank">Facebook</a>!');
                })
                .finally(function() { showTyping(false); });
            return;
        }

        // Product list
        if (q.includes('list') || q.includes('show all') || q.includes('all products') || q.includes('products')) {
            setTimeout(function() {
                var html = 'We have products in these categories:<br>';
                html += '<div class="category-title">🌿 Category A - Food</div>';
                html += 'Seeds, Powders, Oils, Essential Oils, Medicinal Herbs, Himali Products, Juices, Microgreens, Dehydrated Fruits & Vegs, Millets & More!<br><br>';
                html += '<div class="category-title">💄 Category B - Natural Cosmetics</div>';
                html += 'Oils, Soaps, Perfumes, Hair & Skin Care Products<br><br>';
                html += '<div class="category-title">🙏 Category C - Spirituals</div>';
                html += 'Rudraksha, Gems, Stones, Idols & More<br><br>';
                html += '<div class="category-title">🌱 Category D - Sara Nursery</div>';
                html += 'Herbal Plants & Fruit Plants<br><br>';
                html += '<em>Explore all products at our <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">website</a> or <a href="https://www.facebook.com/saraworldwide.com.np/" target="_blank">Facebook</a>!</em>';
                addMessage(html);
                showTyping(false);
            }, 800);
            return;
        }

        // Specific product
        fetch(API_BASE + '/product/' + encodeURIComponent(query))
            .then(function(r) {
                if (!r.ok) throw new Error('Not found');
                return r.json();
            })
            .then(function(detail) {
                addMessage('<strong>' + detail.name + '</strong> (' + detail.category + ')<br><br>' +
                    '<strong>Benefits:</strong> ' + detail.benefits + '<br>' +
                    '<strong>Effects:</strong> ' + detail.effects + '<br><br>' +
                    '<em>Find more at our <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">website</a>.</em>');
            })
            .catch(function() {
                // Fallback: check hardcoded products
                var found = FALLBACK_PRODUCTS.find(function(p) {
                    return p.name.toLowerCase().includes(q) || q.includes(p.name.toLowerCase());
                });
                if (found) {
                    addMessage('<strong>' + found.name + '</strong> (' + found.category + ')<br><br>' +
                        'This is a premium organic product from Sara World Business. ' +
                        'Rich in natural nutrients and ideal for everyday wellness!<br><br>' +
                        '<em>Find more at our <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">website</a>.</em>');
                } else {
                    addMessage("I'm not sure about that one. Try clicking <strong>Products List</strong> or visit our <a href='https://www.facebook.com/saraworldwide.com.np/' target='_blank'>Facebook Page</a>!");
                }
            })
            .finally(function() { showTyping(false); });
    }

    sendBtn.addEventListener('click', function() {
        var text = userInput.value.trim();
        if (!text) return;
        addMessage(text, false);
        userInput.value = '';
        handleSearch(text);
    });

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') sendBtn.click();
    });

    window.quickReply = function(text) {
        addMessage(text, false);
        handleSearch(text);
    };

    window.askProduct = function(name) {
        addMessage(name, false);
        handleSearch(name);
    };
}

// Initialize everything
window.addEventListener('DOMContentLoaded', function() {
    loadEcomProducts();
    initChatbot();
});
