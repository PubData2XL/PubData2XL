// Initialize the service worker
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register("/serviceworker.js", {
      scope: '/'
  }).then(function (registration) {
      // Registration was successful
      //console.log('PubMed2XL-PWA: ServiceWorker registration successful with scope: ', registration.scope);
  }, function (err) {
      // registration failed :(
      //console.log('PubMed2XL-PWA: ServiceWorker registration failed: ', err);
  });
}
