function ajax(div, method, url, payload, callback) {
//    csrfmiddlewaretoken = $(div).find('[name="csrfmiddlewaretoken"]').val();
    csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    payload['csrfmiddlewaretoken'] = csrfmiddlewaretoken
    $.ajax({
        type: method,
        url: url,
        data: payload,
        success: function(response) {
            div.html(response)
            callback();
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}

$( document ).ready(function() {
    function addListeners() {
        $('#add-ingredient-button').click(function() {
            payload = {'amount': $('#ingredient-amount').val(),
                       'title': $('#ingredient-title').val()}
            ajax($('#recipe-ingredients'), "POST", "ingredients", payload, addListeners);
        });
    }
    addListeners();
});
