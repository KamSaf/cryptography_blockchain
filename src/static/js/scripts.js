function message(msg, status) {
    return `\
        <div id="reminder_message" class="mt-3 alert alert-${status}" role="alert" style="display: block;">\
            ${msg}\
            <button type="button" class="btn-close float-end" data-bs-dismiss="alert" aria-label="Close"></button>\
        </div>`
}

function lastRowIndex() {
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

// Node register event
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname != '/nodes') {
        return;
    }
    const address = window.location.origin;
    const btn = document.getElementById('registerNode');
    const modal = new bootstrap.Modal(document.getElementById('newNodeModal'));
    btn.addEventListener('click', async () => {
        const input = document.getElementById('input');
        const url = address + btn.getAttribute('data-url');
        const msgBox = document.getElementById('msgBox');
        const errorBox = document.getElementById('errorBox');
        const nodesTable = document.getElementById('nodesTableBody');
        msgBox.innerHTML = '';
        errorBox.innerHTML = '';
        input.classList.remove('is-invalid');

        let inputUrl = null;
        try {
            inputUrl = new URL(input.value);
        } catch (err) {
            errorBox.innerHTML += message('Invalid URL address given.', 'danger');
            input.classList.add('is-invalid');
            return;
        }
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
                nodesTable.innerHTML += `\
                    <tr><th scope="row">${lastRowIndex()}</th>\
                    <td>${inputUrl.host}</td></tr>`;
            } else if (data.status_code === 409) {
                responseStatus = 'warning';
            }
            if (responseStatus != 'danger') {
                modal.hide();
                msgBox.innerHTML += message(data.detail, responseStatus);
                input.value = '';
                return;
            }
            errorBox.innerHTML += message(data.detail, responseStatus);
        });
    });
});

// Transaction creation event
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname != '/transactions') {
        return;
    }
    const address = window.location.origin;
    const btn = document.getElementById('createTransaction');
    const modal = new bootstrap.Modal(document.getElementById('newTransactionModal'));
    btn.addEventListener('click', async (e) => {
        e.preventDefault();
        const formData = new FormData(document.getElementById('form'), btn);
        const jsonData = JSON.stringify(Object.fromEntries(formData));
        const url = address + btn.getAttribute('data-url');
        const msgBox = document.getElementById('msgBox');
        const errorBox = document.getElementById('errorBox');
        const transactionsTable = document.getElementById('transactionsTableBody');
        msgBox.innerHTML = '';
        errorBox.innerHTML = '';
        const inputElements = document.getElementsByTagName('input');

        let error = false;
        for (let i=0; i<inputElements.length; i++) {
            const el = inputElements[i]; 
            if (!el.value) {
                error = true;
                errorBox.innerHTML += message(`Field value missing or invalid (${el.getAttribute('name')})`, 'danger');
                el.classList.add('is-invalid');
            } else {
                el.classList.remove('is-invalid');
            }
        }

        if (error) {
            return;
        }
        const response = await fetch(
            url, 
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: jsonData
            },
        );
        await response.json().then((data) => {
            let responseStatus = 'danger';
            if (data.status_code === 201) {
                responseStatus = 'success';
                const date = new Date();
                const datetime = `${date.getDate()}-${date.getMonth()}-${date.getFullYear()}\
                                    ${date.getHours()}:${date.getMinutes()}`;
                transactionsTable.innerHTML += `\
                    <tr><th scope="row">${lastRowIndex()}</th>\
                    <td>${formData.get('sender')}</td>\
                    <td>${formData.get('recipient')}</td>\
                    <td>${formData.get('amount')}</td>\
                    <td>${datetime}</td></tr>\
                    `;
                modal.hide();
                msgBox.innerHTML += message(data.detail, responseStatus);
                document.getElementsByTagName('input').forEach(element => {
                    element.value = '';
                });
                return;
            }
            errorBox.innerHTML += message(data.detail, responseStatus);
        });
    });
});

// Mining
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname != '/') {
        return;
    }

    const address = window.location.origin;
    const btn = document.querySelector('.mine');
    const url = address + btn.getAttribute('data-url');
    const msgBox = document.getElementById('msgBox');
    btn.addEventListener('click', async () => {
        if (btn.getAttribute('data-mining') === 'false') {
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"\
             aria-hidden="true"></span> <span role="status">Mining...</span>';
            btn.setAttribute('data-mining', true);
            btn.setAttribute('disabled', true);

            const response = await fetch(url, { method: "GET" });
            await response.json().then((data) => {
                if (data.status_code === 204) {
                    responseStatus = 'warning';
                } else if (data.status_code === 201) {
                    responseStatus = 'success';
                    playYoink();
                } else {
                    responseStatus = 'danger';
                }
                setTimeout(() => {
                    msgBox.innerHTML += message(data.detail, responseStatus);
                    btn.innerHTML = '<span role="status">Mine!</span>';
                    btn.setAttribute('data-mining', false);
                    btn.removeAttribute('disabled');    
                }, 800) // mining the YoinkCoin hehe
            });            
        }
    });
});

// Syncing blockchain
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname != '/') {
        return;
    }

    const btn = document.querySelector('.sync-blockchain');
    const address = window.location.origin;
    const url = address + btn.getAttribute('data-url');
    btn.addEventListener('click', async () => {
        if (btn.getAttribute('data-syncing') === 'false') {
            btn.innerHTML = '<span class="spinner-border spinner-border-sm"\
            aria-hidden="true"></span> Syncing...';
            btn.setAttribute('data-syncing', true);
            btn.setAttribute('disabled', true);
        
            const response = await fetch(url, { method: "GET" });
            await response.json().then((data) => {
                let responseStatus = 'danger';
                if (data.status_code === 200) {
                    responseStatus = 'success';
                }
                setTimeout(() => {
                    msgBox.innerHTML += message(data.detail, responseStatus);
                    btn.innerHTML = 'Sync blockchain';
                    btn.setAttribute('data-syncing', false);
                    btn.removeAttribute('disabled');
                }, 800)
            });            
        }
    });
});
