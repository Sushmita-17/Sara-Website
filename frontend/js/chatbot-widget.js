/**
 * Sara AI chatbot — Gemini API + local quick replies
 */
(function (global) {
    var API = global.SARA_API || ((global.location.origin || 'http://localhost:8000') + '/api');
    var SITE = global.SARA_SITE || {};

    function initChatbot() {
        var chatToggle = document.getElementById('chat-toggle');
        var chatWidget = document.getElementById('chat-widget');
        var closeChat = document.getElementById('close-chat');
        var userInput = document.getElementById('user-input');
        var sendBtn = document.getElementById('send-btn');
        var typingIndicator = document.getElementById('typing-indicator');
        var chatMessages = document.getElementById('chat-messages');

        if (!chatToggle || !chatWidget) return;

        chatToggle.addEventListener('click', function () {
            chatWidget.style.display = 'flex';
            chatWidget.classList.remove('hidden');
            chatToggle.style.display = 'none';
        });

        if (closeChat) {
            closeChat.addEventListener('click', function () {
                chatWidget.style.display = 'none';
                chatWidget.classList.add('hidden');
                chatToggle.style.display = 'flex';
            });
        }

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

        function locationReply() {
            var embed = SITE.mapEmbed || 'https://www.google.com/maps?q=Sara+Worldwide+Business+Kalanki-14+Kathmandu&output=embed';
            var link = SITE.mapLink || embed;
            return '<strong>' + (SITE.businessName || 'Sara Worldwide Business') + '</strong><br>' +
                '📍 ' + (SITE.address || 'Kalanki-14, Kathmandu, Nepal') + '<br>' +
                '📞 ' + (SITE.phone || '+977 1 5225181') + ' · ' + (SITE.mobile || '+977 9851105234') + '<br>' +
                '📧 ' + (SITE.email || 'info@saraworldwide.com.np') + '<br>' +
                '🕐 ' + (SITE.hours || 'Sun–Fri 9am–6pm') + '<br>' +
                '<a href="' + link + '" target="_blank" rel="noopener">Open in Google Maps →</a>' +
                '<div style="margin-top:10px;border-radius:10px;overflow:hidden;">' +
                '<iframe src="' + embed + '" width="100%" height="160" style="border:0;" allowfullscreen loading="lazy" title="Sara Worldwide Business location"></iframe></div>';
        }

        function productsReply() {
            return 'Browse our full catalog on <a href="products.html">Shop All Products</a> or ' +
                '<a href="' + (SITE.website || 'https://saraworldwide.com.np/') + '" target="_blank" rel="noopener">saraworldwide.com.np</a>.<br><br>' +
                '<strong>Highlights:</strong> Moringa Powder, Shilajit, Ginseng, Wild Honey 🌿';
        }

        function askAI(query) {
            fetch(API + '/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: query })
            })
                .then(function (r) { return r.json(); })
                .then(function (data) {
                    addMessage(data.response || 'No response.');
                })
                .catch(function () {
                    fetch(API + '/product/' + encodeURIComponent(query))
                        .then(function (r) {
                            if (!r.ok) throw new Error();
                            return r.json();
                        })
                        .then(function (detail) {
                            addMessage('<strong>' + detail.name + '</strong> (' + (detail.category || '') + ')<br><br>' +
                                (detail.benefits ? '<strong>Benefits:</strong> ' + detail.benefits + '<br>' : '') +
                                (detail.effects ? '<strong>Effects:</strong> ' + detail.effects + '<br>' : '') +
                                '<a href="product.html?name=' + encodeURIComponent(detail.name) + '">View product →</a>');
                        })
                        .catch(function () {
                            addMessage("I couldn't reach Sara AI right now. Call <strong>+977 9851105234</strong> or try " +
                                '<a href="products.html">Shop All Products</a>.');
                        });
                })
                .finally(function () { showTyping(false); });
        }

        function handleSearch(query) {
            var q = query.toLowerCase().trim();
            showTyping(true);

            if (q === 'hi' || q === 'hello' || q === 'hey' || q === 'namaste') {
                setTimeout(function () {
                    addMessage("Namaste! 🙏 I'm <strong>Sara AI</strong>. Ask me about Moringa, Shilajit, Ginseng, Honey, or any product from our catalog!");
                    showTyping(false);
                }, 400);
                return;
            }

            if (q.includes('location') || q.includes('where') || q.includes('map') || q.includes('address') || q === 'store location') {
                setTimeout(function () {
                    addMessage(locationReply());
                    showTyping(false);
                }, 400);
                return;
            }

            if (q.includes('contact') || q.includes('phone') || q.includes('email') || q === 'info') {
                setTimeout(function () {
                    addMessage(locationReply());
                    showTyping(false);
                }, 400);
                return;
            }

            if (q.includes('list') || q.includes('show all') || q.includes('all products') || q.includes('catalog') || q.includes('products')) {
                setTimeout(function () {
                    addMessage(productsReply());
                    showTyping(false);
                }, 400);
                return;
            }

            askAI(query);
        }

        sendBtn.addEventListener('click', function () {
            var text = userInput.value.trim();
            if (!text) return;
            addMessage(text, false);
            userInput.value = '';
            handleSearch(text);
        });

        userInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendBtn.click();
        });

        global.quickReply = function (text) {
            addMessage(text, false);
            handleSearch(text);
        };

        global.askProduct = function (name) {
            addMessage(name, false);
            handleSearch(name);
        };
    }

    global.SaraChat = { init: initChatbot };

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initChatbot);
    } else {
        initChatbot();
    }
})(window);
