function ajax(div, method, url, payload, callback) {
    var processData = true;
    var contentType = "application/x-www-form-urlencoded; charset=UTF-8";
    if (payload && payload.constructor.name === "FormData") {
        processData = false;
        contentType = false; // lol, this is the "correct" way to remove the header
    }
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    csrfmiddlewaretoken = $('[name="csrfmiddlewaretoken"]').val();
    return $.ajax({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfmiddlewaretoken);
            }
        },
        type: method,
        url: url,
        data: payload,
        processData: processData,
        contentType: contentType,
        success: function(response) {
            if (div) {
                div.html(response)
            }
            if(callback) {
                callback();
            }
        },
        error: function(xhr, textStatus, errorThrown) {
            if(xhr.status==403) {
                alert("Du må logge på for bruke denne funksjonen.");
                return
            }
            alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}
