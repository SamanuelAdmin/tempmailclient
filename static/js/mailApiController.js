function sendRequest(url) {
    return new Promise((resolve, reject) => {
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.send();

        xhr.onreadystatechange = function () {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    resolve(true);
                } else {
                    console.error(xhr.statusText);
                    reject(false);
                }
            }
        };
    });
}

function addMail() {
    loadingMessage();
    sendRequest('/addmail')
        .then(() => {
            location.reload();
        });
}

function deleteMail(mail) {
    loadingMessage();
    sendRequest('/deletemail?mail=' + mail)
        .then(() => {
            location.reload();
        });
}