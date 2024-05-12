function message(msg, status) {
    return `\
        <div id="reminder_message" class="mt-3 alert alert-${status}" role="alert" style="display: block;">\
            ${msg}\
            <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>\
    `
}

function lastNodeIndex() {
    const rows = document.getElementsByName('rowIndex');
    let lastIndex = 0;
    rows.forEach(function(value) {
        lastIndex = value.innerHTML;
    });
    return parseInt(lastIndex) + 1;
}

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

document.addEventListener('DOMContentLoaded', function() {
    const address = window.location.origin;
    const btn = document.getElementById('registerNode');
    btn.addEventListener('click', async () => {
        const input = document.getElementById('input');
        const url = address + input.getAttribute('data-url');
        const msgBox = document.getElementById('msgBox');
        const nodesTable = document.getElementById('nodesTableBody');
        const response = await fetch(
            url, 
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ "nodes": input.value })
            },
        );
        await response.json().then((data) => {
            let responseStatus = 'danger';
            if (data.status_code === 201) {
                responseStatus = 'success';
                const inputUrl = new URL(input.value);
                nodesTable.innerHTML += `\
                    <tr><th scope="row">${lastNodeIndex()}</th>\
                    <td>${inputUrl.host}</td></tr>`
            } else if (data.status_code === 409) {
                responseStatus = 'warning';
            }
            msgBox.innerHTML += message(data.detail, responseStatus);
        });
    });
});
