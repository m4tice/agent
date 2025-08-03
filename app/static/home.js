document.addEventListener('DOMContentLoaded', function() {
    const lights = document.querySelectorAll('.light');
    lights.forEach(light => {
        light.addEventListener('click', function() {
            changeState(light);
        });
    });
});

function changeState(light) {
    const currentState = light.dataset.state;
    light.dataset.state = currentState === "1" ? "0" : "1";
}
