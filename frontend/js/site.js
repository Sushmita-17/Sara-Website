/** Shared site config — load before other scripts */

window.SARA_API = (window.location.origin || 'http://localhost:8000') + '/api';



window.SARA_SITE = {

    businessName: 'Sara Worldwide Business Pvt. Ltd.',

    brandName: 'Sara Foods',

    address: 'Kalanki-14, Kathmandu, Nepal',

    phone: '+977 1 5225181',

    mobile: '+977 9851105234',

    email: 'info@saraworldwide.com.np',

    website: 'https://saraworldwide.com.np/',

    facebook: 'https://www.facebook.com/saraworldwide.com.np/',

    hours: 'Sunday – Friday 9am–6pm · Saturday closed',

    mapLink: 'https://www.google.com/maps/search/?api=1&query=Sara+Worldwide+Business+Kalanki-14+Kathmandu+Nepal',

    mapEmbed: 'https://www.google.com/maps?q=Sara+Worldwide+Business+Pvt+Ltd,+Kalanki-14,+Kathmandu,+Nepal&output=embed'

};



/** Marquee: main product highlights only */

window.SARA_MARQUEE = [
    { name: 'Moringa Powder', url: 'https://saraworldwide.com.np/wp-content/uploads/2017/04/fina.jpg', tag: 'Superfood' },
    { name: 'Shilajit', url: 'https://saraworldwide.com.np/wp-content/uploads/2024/06/shw.jpg', tag: 'Himalayan' },
    { name: 'Ginseng', url: 'https://saraworldwide.com.np/wp-content/uploads/2026/01/WhatsApp-Image-2026-01-02-at-5.09.07-PM.jpeg', tag: 'Energy' },
    { name: 'Wild Honey', url: 'https://saraworldwide.com.np/wp-content/uploads/2025/02/wh.jpg', tag: 'Organic' }
];