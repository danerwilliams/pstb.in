
// Lambda API Endpoint
const api = 'https://ez02ob0o22.execute-api.us-west-1.amazonaws.com/api/'

/* Submit handler */
function submitHandler() {
    const url = document.getElementById('target_url').value;
    const file = document.getElementById('target_file').files[0];

    if (file['size'] > 5000000) { //maximum 5 mb allowed
        displayUrl('5 mb maximum upload size');
        return
    }

    if (!url && file)
        getPresignedUrl(file);
    else if (url && !file)
        shortenUrl(url);
    else
        displayUrl('enter either a file or url');
}

/* Get shortened url */
function shortenUrl(target_url) {
    fetch(api + 'shorten', {method: 'POST', mode: 'cors', body: target_url})
        .then(response => response.json())
        .then(response => displayUrl(response['body']['url']));
}

/* Get presigned url for file upload */
function getPresignedUrl(file) {
    fetch(api + 'upload', {method: 'POST', 
                           mode: 'cors', 
                           headers: {
                                'Accept': 'application/json',
                                'Content-Type': 'application/json'
                           },
                           body: JSON.stringify({
                                'type': file['type'],
                                'name': file['name']
                           })
                           })
        .then(response => response.json())
        .then(response => uploadFile(response));
}

/* Upload file */
function uploadFile(response) {

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