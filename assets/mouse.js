document.addEventListener('click', function(event) {
    var mousePos = { x: event.clientX, y: event.clientY };
    var dashStore = document.querySelector('#mouse-position');
    if (dashStore) {
        dashStore.setAttribute('data', JSON.stringify(mousePos));
    }
});

