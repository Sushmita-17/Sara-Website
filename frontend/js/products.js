var allProducts = [];
var activeFilter = 'all';

var FALLBACK = [
    {name:'Chia seed',cat:'Seeds',catLetter:'A',price:350,img:'prod_moringa.png'},
    {name:'Moringa powder',cat:'Powder',catLetter:'A',price:450,img:'prod_moringa.png'},
    {name:'Ashwagandha powder',cat:'Powder',catLetter:'A',price:550,img:'prod_moringa.png'},
    {name:'Wild Honey',cat:'Himali Products',catLetter:'A',price:1200,img:'prod_moringa.png'},
    {name:'Shilajit',cat:'Himali Products',catLetter:'A',price:2500,img:'prod_moringa.png'},
    {name:'Turmeric powder',cat:'Powder',catLetter:'A',price:200,img:'prod_moringa.png'},
    {name:'Black seed oil',cat:'Oil',catLetter:'A',price:650,img:'prod_moringa.png'},
    {name:'Lavender oil',cat:'Essential Oil',catLetter:'A',price:850,img:'prod_moringa.png'},
    {name:'Aloe vera fresh juice',cat:'Juices',catLetter:'A',price:300,img:'prod_moringa.png'},
    {name:'Rose water',cat:'Floral Waters',catLetter:'B',price:350,img:'prod_moringa.png'},
    {name:'Henna Powder',cat:'Hair Colours',catLetter:'B',price:250,img:'prod_moringa.png'},
    {name:'Moringa Neem soap',cat:'Soaps',catLetter:'B',price:180,img:'prod_moringa.png'},
    {name:'Rudraksha',cat:'Spiritual Items',catLetter:'C',price:500,img:'prod_moringa.png'},
    {name:'Moringa Plant',cat:'Herbal Plants',catLetter:'D',price:300,img:'prod_moringa.png'},
    {name:'Dragon Fruit',cat:'Fruit Plants',catLetter:'D',price:450,img:'prod_moringa.png'},
];

function catLetterToLabel(letter) {
    var map = {A:'Organic Food',B:'Natural Cosmetics',C:'Spiritual Wellness',D:'Sara Nursery'};
    return map[letter] || letter;
}

function renderGrid(products) {
    var grid = document.getElementById('product-grid');
    if (!grid) return;
    if (!products.length) {
        grid.innerHTML = '<div style="text-align:center; color:var(--text-muted); padding:100px 0; grid-column:1/-1;">' +
                         '<h2 style="font-size:3rem; margin-bottom:16px;">🔍</h2>' +
                         '<h3>No products found in this category</h3>' +
                         '<p>Try searching for something else or browse all products.</p>' +
                         '</div>';
        return;
    }
    grid.innerHTML = products.map(function(p) {
        var imgSrc = p.img
            ? (p.img.startsWith('http') ? p.img : p.img)
            : 'prod_moringa.png';
        return `
            <div class="product-card">
                <div class="p-img">
                    <img src="${imgSrc}" alt="${p.name}" loading="lazy"
                         onerror="this.src='prod_moringa.png'">
                    <span class="p-badge">${catLetterToLabel(p.catLetter)}</span>
                </div>
                <div class="p-info">
                    <h3>${p.name}</h3>
                    <p class="p-cat">${p.cat}</p>
                    <div class="p-bottom">
                        <span class="price">Rs. ${p.price || 450}</span>
                        <button class="add-to-cart" onclick="addToCart('${p.name.replace(/'/g,"\\'")}', ${p.price || 450})">Add to Cart</button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
}

function filterProducts(letter) {
    activeFilter = letter;
    var filtered = letter === 'all' ? allProducts : allProducts.filter(function(p){ return p.catLetter === letter; });
    renderGrid(filtered);
}
window.filterProducts = filterProducts;

function searchProducts(query) {
    var q = query.toLowerCase();
    var filtered = allProducts.filter(function(p){
        return p.name.toLowerCase().includes(q) || p.cat.toLowerCase().includes(q);
    });
    renderGrid(filtered);
}

document.addEventListener('DOMContentLoaded', function() {
    fetch(API + '/products')
        .then(function(r) { if (!r.ok) throw new Error(); return r.json(); })
        .then(function(categories) {
            allProducts = [];
            var letters = {
                'Category A: Food': 'A',
                'Category B: Natural Cosmetics': 'B',
                'Category C: Spirituals': 'C',
                'Category D: Sara Nursery': 'D'
            };
            categories.forEach(function(cat) {
                var letter = letters[cat.name] || 'A';
                cat.children.forEach(function(sub) {
                    sub.products.forEach(function(p) {
                        allProducts.push({
                            name: p.name, cat: sub.name,
                            catLetter: letter, price: p.price || 450,
                            img: p.image_url || 'prod_moringa.png'
                        });
                    });
                });
            });
            renderGrid(allProducts);
        })
        .catch(function() {
            allProducts = FALLBACK;
            renderGrid(FALLBACK);
        });

    // Global Search override for products page
    const globalSearch = document.getElementById('global-search');
    if (globalSearch) {
        globalSearch.addEventListener('input', function(e) {
            const query = e.target.value.trim();
            if (query) {
                searchProducts(query);
            } else {
                filterProducts(activeFilter);
            }
        });
    }
});
