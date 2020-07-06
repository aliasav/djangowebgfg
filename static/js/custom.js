// access to global scope
console.log('custom.js file', word);

initPage();

function fetchWord(){
    // when the page loads, call dict api  
    let word = $('#inputBox').val();
    let url = '/_api/v1/dictionary/' + word;
    console.log('fetching meaning for word', word, url);
    $.ajax({
        type: 'GET',
        url:  url,
        dataType: 'json',
        success: function(data){
            console.log(data);
        },
    })
}
