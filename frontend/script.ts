interface CompanyInfo {
    name: string;
    location: string;
    phone: string;
    email: string;
    website: string;
    facebook: string;
}

interface ProductStats {
    total_products: number;
    total_categories: number;
}

interface Product {
    id: number;
    name: string;
}

interface Category {
    id: number;
    name: string;
    children: Category[];
    products: Product[];
}

interface ProductDetail {
    name: string;
    benefits: string;
    effects: string;
    category: string;
}

const API_BASE = "http://localhost:8000/api";

// DOM Elements
const chatToggle = document.getElementById('chat-toggle') as HTMLDivElement;
const chatWidget = document.getElementById('chat-widget') as HTMLDivElement;
const closeChat = document.getElementById('close-chat') as HTMLButtonElement;
const chatMessages = document.getElementById('chat-messages') as HTMLDivElement;
const userInput = document.getElementById('user-input') as HTMLInputElement;
const sendBtn = document.getElementById('send-btn') as HTMLButtonElement;
const typingIndicator = document.getElementById('typing-indicator') as HTMLDivElement;

// Toggle Chat Window
chatToggle.addEventListener('click', () => {
    chatWidget.classList.remove('hidden');
    chatToggle.style.display = 'none';
});

closeChat.addEventListener('click', () => {
    chatWidget.classList.add('hidden');
    chatToggle.style.display = 'flex';
});

function addMessage(text: string, isBot: boolean = true) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${isBot ? 'bot-message' : 'user-message'}`;
    msgDiv.innerHTML = text;
    chatMessages.appendChild(msgDiv);
    
    setTimeout(() => {
        chatMessages.scrollTo({
            top: chatMessages.scrollHeight,
            behavior: 'smooth'
        });
    }, 100);
}

function showTyping(show: boolean) {
    typingIndicator.style.display = show ? 'block' : 'none';
}

async function handleSearch(query: string) {
    const q = query.toLowerCase().trim();
    showTyping(true);
    
    try {
        // 1. General Greetings
        if (q === 'hi' || q === 'hello' || q === 'hey') {
            addMessage("Hi there! I'm doing great, thank you for asking. How are you doing today? I'm here to help you explore everything about <strong>Sara World Business</strong>! 🌿");
        }
        else if (q.includes('how are you')) {
            addMessage("I'm functioning perfectly and feeling energized to help you! How can I assist you with our organic products or company info?");
        }
        // 2. Info / Contact / Location
        else if (q.includes('info') || q.includes('contact') || q.includes('location') || q.includes('where')) {
            const res = await fetch(`${API_BASE}/info`);
            const info: CompanyInfo = await res.json();
            const mapHtml = `
                <div style="margin-top:10px; border-radius:12px; overflow:hidden; border:1px solid #ddd;">
                    <iframe 
                        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3532.8344158226!2d85.2818!3d27.6932!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39eb18635848c087%3A0x67399426f4370597!2sKalanki%2C%20Kathmandu%2044600!5e0!3m2!1sen!2snp!4v1715443200000!5m2!1sen!2snp" 
                        width="100%" height="150" style="border:0;" allowfullscreen="" loading="lazy">
                    </iframe>
                </div>
            `;
            addMessage(`
                <strong>${info.name}</strong><br>
                📍 ${info.location}<br>
                📞 ${info.phone}<br>
                📧 ${info.email}<br>
                🌐 <a href="${info.website}" target="_blank">Website</a><br>
                FB: <a href="${info.facebook}" target="_blank">Facebook Page</a>
                ${mapHtml}
            `);
        } 
        else if (q.includes('total') || q.includes('how many')) {
            const res = await fetch(`${API_BASE}/products/stats`);
            const stats: ProductStats = await res.json();
            addMessage(`We have a total of <strong>${stats.total_products} products</strong> across <strong>${stats.total_categories} categories</strong>. You can view all of them on our <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">website</a>!`);
        }
        else if (q.includes('list') || q.includes('all products') || q.includes('show all')) {
            const res = await fetch(`${API_BASE}/products`);
            const categories: Category[] = await res.json();
            let html = "Here are our featured products. You can find our full range on our <strong>Website</strong> and <strong>Facebook page</strong>!<br>";
            categories.forEach(cat => {
                html += `<div class="category-title">${cat.name}</div>`;
                cat.children.forEach(sub => {
                    html += `<div style="margin: 5px 0;"><strong>${sub.name}:</strong><br>`;
                    html += sub.products.map(p => `<span class="product-item" onclick="askProduct('${p.name}')">${p.name}</span>`).join(' ');
                    html += "</div>";
                });
            });
            addMessage(html);
        }
        else {
            const res = await fetch(`${API_BASE}/product/${encodeURIComponent(query)}`);
            if (res.ok) {
                const detail: ProductDetail = await res.json();
                addMessage(`
                    <strong>${detail.name}</strong> (${detail.category})<br><br>
                    <strong>Benefits:</strong> ${detail.benefits}<br>
                    <strong>Effects:</strong> ${detail.effects}<br><br>
                    <em>Find more details on our <a href="https://saraworldwide.com.np/saraworldwide" target="_blank">website</a>.</em>
                `);
            } else {
                addMessage("I'm not quite sure about that. Try asking for 'Products List' or check our <a href='https://www.facebook.com/saraworldwide.com.np/' target='_blank'>Facebook Page</a> for the latest updates!");
            }
        }
    } catch (error) {
        addMessage("Oops! My connection to the database is down. Please ensure the backend server is running.");
    } finally {
        showTyping(false);
    }
}

// Global functions
(window as any).askProduct = (name: string) => {
    addMessage(name, false);
    handleSearch(name);
};

(window as any).quickReply = (text: string) => {
    addMessage(text, false);
    handleSearch(text);
};

sendBtn.addEventListener('click', () => {
    const text = userInput.value.trim();
    if (!text) return;
    addMessage(text, false);
    userInput.value = '';
    handleSearch(text);
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendBtn.click();
});
