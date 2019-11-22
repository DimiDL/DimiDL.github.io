self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('v1').then((cache) => {
      return cache.addAll([
        './index.html'
      ]);
    })
  );
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    try {
      let url = "https://itisatracker.org/index.html";
      const response = await fetch(url, { mode: 'cors' });
    } catch(e) {
    }
  })());
});

self.addEventListener('fetch', event => {
});

self.addEventListener('message', event => {
});
