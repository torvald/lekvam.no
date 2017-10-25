function ajax(div, method, url, payload, callback) {
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
            }
        },
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

function addListeners() {
    $('#add-ingredient-button').click(function() {
        payload = {'amount': $('#ingredient-amount').val(),
                   'title': $('#ingredient-title').val()}
        ajax($('#recipe-ingredients'), "POST", "ingredients", payload, addListeners);
    });
    $('.remove-ingredient-button').click(function() {
        //payload = {'id': $(this).attr('data-id')};
        var id = $(this).attr('data-id');
        ajax($('#recipe-ingredients'), "DELETE", "ingredient/" + id + "/delete", null, addListeners);
    });
}

$( document ).ready(function() {
    addListeners();
});
