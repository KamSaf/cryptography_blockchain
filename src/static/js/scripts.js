function playYoink(){
    const audio = new Audio('/static/sounds/yoink.mp3');
    audio.play();
}

document.addEventListener('DOMContentLoaded', function() {
    const yoinkCoin = document.getElementById('yoinkCoin');
    yoinkCoin.addEventListener('click', () => {
        playYoink();
    });
});

document.addEventListener('DOMContentLoaded', function(e) {
    e.preventDefault();
    const btn = document.getElementById('registerNode');
    btn.addEventListener('click', async () => {
        const input = document.getElementById('input');
        const url = 'http://127.0.0.1:5000/' + input.getAttribute('data-url');
        const response = await fetch(
            url, 
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "nodes": input.value })
            },
        );
        const data = await response.json();
        console.log(data);
    });
});
