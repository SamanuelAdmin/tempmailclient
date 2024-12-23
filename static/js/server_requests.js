
function sendPOSTRequest(url) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Type", "application/json; charset=UTF-8");
    xhr.send();
}


function deleteMailFromList(mail) {
    sendPOSTRequest('/mail/delete?mail=' + mail);
}

function deleteAllMails() {
    sendPOSTRequest('/mail/delete?mail=all');
}

function addMailToList(mail) {
    sendPOSTRequest('/mail/add');
}

function deleteEmail(emailId) {
    sendPOSTRequest('/email/delete?id=' + emailId);
}