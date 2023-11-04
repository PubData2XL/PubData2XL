var CACHE_VERSION = 'PubMed2XL-cache-v1';
var CACHE_URLS = [
    '',
    '/xlsx',
    '/xml',
    '/faq',
    '/offline',
    '/static/css/bootstrap.min.css',
    '/static/js/bootstrap.min.js',
    '/static/js/jquery.slim.min.js',    
    '/static/pubmed2xl/css/style.css',
    '/static/pubmed2xl/js/rows_counter.js',
    '/static/img/favicons/apple-touch-icon.png',
    '/static/img/favicons/apple-touch-icon-precomposed.png',
    '/static/img/favicons/apple-touch-icon-57x57.png',
    '/static/img/favicons/apple-touch-icon-57x57-precomposed.png',
    '/static/img/favicons/apple-touch-icon-72x72.png',
    '/static/img/favicons/apple-touch-icon-72x72-precomposed.png',
    '/static/img/favicons/apple-touch-icon-114x114.png',
    '/static/img/favicons/apple-touch-icon-114x114-precomposed.png',
    '/static/img/favicons/apple-touch-icon-120x120.png',
    '/static/img/favicons/apple-touch-icon-120x120-precomposed.png',
    '/static/img/favicons/apple-touch-icon-144x144.png',
    '/static/img/favicons/apple-touch-icon-144x144-precomposed.png',
    '/static/img/favicons/apple-touch-icon-152x152.png',
    '/static/img/favicons/apple-touch-icon-152x152-precomposed.png',
    '/static/img/favicons/favicon.ico',
    '/static/img/favicons/favicon-16x16.png',
    '/static/img/favicons/favicon-32x32.png',
    '/static/img/favicons/android-chrome-48x48.png',
    '/static/img/favicons/android-chrome-72x72.png',
    '/static/img/favicons/android-chrome-144x144.png',
    '/static/img/favicons/android-chrome-256x256.png',
    '/static/img/favicons/android-chrome-512x512.png',
    '/static/img/favicons/safari-pinned-tab.svg',
    '/static/img/favicons/browserconfig.xml',  
    '/static/img/favicons/mstile-144x144.png',
    '/static/img/favicons/maskable_icon.png',
    '/static/img/favicons/maskable_icon_36x36.png',
    '/static/img/favicons/maskable_icon_48x48.png',
    '/static/img/favicons/maskable_icon_72x72.png',
    '/static/img/favicons/maskable_icon_96x96.png',
    '/static/img/favicons/maskable_icon_144x144.png',
    '/static/img/favicons/maskable_icon_192x192.png',
    '/static/img/favicons/maskable_icon_384x384.png',
    '/static/img/favicons/maskable_icon_512x512.png',
]

// Cache on install
self.addEventListener("install", event => {
    this.skipWaiting();
    event.waitUntil(
        caches.open(CACHE_VERSION)
            .then(cache => {
                return cache.addAll(CACHE_URLS);
            })
    )
});

// Clear cache on activate
self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(cacheURLS => {
            return Promise.all(
                cacheURLS
                    .filter(cacheURLS => (cacheURLS.startsWith("PubMed2XL-cache-")))
                    .filter(cacheURLS => (cacheURLS !== CACHE_URLS))
                    .map(cacheURLS => caches.delete(cacheURLS))
            );
        })
    );
});

// Serve from Cache
self.addEventListener("fetch", event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => {
                return response || fetch(event.request);
            })
            .catch(() => {
                return caches.match('/offline');
            })
    )
});
