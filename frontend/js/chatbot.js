document.addEventListener('DOMContentLoaded', function() {
    var toggle = document.getElementById('chat-toggle');
    var widget = document.getElementById('chat-widget');
    var closeBtn = document.getElementById('chat-close');
    var msgs = document.getElementById('chat-msgs');
    var input = document.getElementById('chat-input');
    var sendBtn = document.getElementById('chat-send');
    var typing = document.getElementById('chat-typing');

    if (!toggle || !widget) return;

    toggle.addEventListener('click', function() {
        widget.classList.remove('hidden');
        toggle.style.display = 'none';
    });
    closeBtn.addEventListener('click', function() {
        widget.classList.add('hidden');
        toggle.style.display = 'flex';
    });

    function addMsg(text, isBot) {
        var d = document.createElement('div');
        d.className = 'msg ' + (isBot !== false ? 'bot' : 'user');
        d.innerHTML = text;
        msgs.appendChild(d);
        msgs.scrollTop = msgs.scrollHeight;
    }

    function setTyping(show) { if (typing) typing.style.display = show ? 'block' : 'none'; }

    function respond(query) {
        var q = query.toLowerCase().trim();
        setTyping(true);

        // Fast Local Rules (optional, for common stuff)
        if (['hi','hello','hey','namaste'].includes(q)) {
            delay(function() { addMsg("Hi there! 👋 I'm Sara AI, your organic health guide. How can I help you today?"); });
            return;
        }

        if (q.includes('location') || q.includes('address') || q.includes('where')) {
             delay(function() {
                addMsg('<strong>Sara World Business Pvt. Ltd.</strong><br>' +
                    '📍 Kalanki-14, Kathmandu, Nepal<br>' +
                    '📞 +977 1 5225181 | 9851105234<br>' +
                    '<div style="margin-top:10px;border-radius:10px;overflow:hidden;">' +
                    '<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.8344158226!2d85.2818!3d27.6932!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb18635848c087%3A0x67399426f4370597!2sKalanki%2C%20Kathmandu' +
                    '!5e0!3m2!1sen!2snp" width="100%" height="140" style="border:0;" allowfullscreen="" loading="lazy"></iframe></div>');
            });
            return;
        }

        // Call AI Backend
        fetch(API + '/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: query })
        })
        .then(function(r) { return r.json(); })
        .then(function(data) {
            addMsg(data.response || "I'm not sure how to respond to that. Can you try rephrasing?");
        })
        .catch(function() {
            addMsg("I'm having trouble connecting to my AI brain. Please try again later or contact us directly!");
        })
        .finally(function() {
            setTyping(false);
        });
    }

    function delay(fn) {
        setTimeout(function() { fn(); setTyping(false); }, 700);
    }

    sendBtn.addEventListener('click', function() {
        var text = input.value.trim();
        if (!text) return;
        addMsg(text, false);
        input.value = '';
        respond(text);
    });
    input.addEventListener('keypress', function(e){ if(e.key === 'Enter') sendBtn.click(); });

    window.quickChat = function(text) {
        addMsg(text, false);
        respond(text);
    };
});
