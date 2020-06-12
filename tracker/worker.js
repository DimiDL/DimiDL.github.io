onmessage = function(e) {
  try {
    indexedDB.open("test", "1");
    postMessage(true);
  } catch (e) {
    postMessage(false);
  }
}
