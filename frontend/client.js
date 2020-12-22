
// Lambda API Endpoint
const api = 'https://ez02ob0o22.execute-api.us-west-1.amazonaws.com/api/'


/* Get shortened url */
function shortenUrl() {
    const target_url = document.getElementById('target_url').value;
    fetch(api + 'shorten', {method: 'POST', mode: 'cors', body: target_url})
        .then(response => response.json())
        .then(response => displayUrl(response['body']['url']));
}


/* Displays shortened url */
function displayUrl(url){
    const code_html = document.getElementById('short_url');
    code_html.innerHTML = url;
}


/* Copies shortened url */
function copyUrl() {
    var range = document.createRange();
    range.selectNode(document.getElementById("short_url"));
    window.getSelection().removeAllRanges(); // clear current selection
    window.getSelection().addRange(range); // to select text
    document.execCommand("copy");
    window.getSelection().removeAllRanges();// to deselect
}