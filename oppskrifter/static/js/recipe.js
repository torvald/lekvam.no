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
            div.html(response)
            callback();
        },
        error: function(xhr, textStatus, errorThrown) {
            alert("Please report this error: "+errorThrown+xhr.status+xhr.responseText);
        }
    });
}

function addIngredientsListeners() {
    $('#add-ingredient-button').click(function() {
        payload = {'amount': $('#ingredient-amount').val(),
                   'title': $('#ingredient-title').val()}
        ajax($('#recipe-ingredients'), "POST", "ingredients", payload, addIngredientsListeners).done(function() {
            $("#ingredient-amount").focus();
        });
    });
    $('.remove-ingredient-button').click(function() {
        var id = $(this).attr('data-id');
        ajax($('#recipe-ingredients'), "DELETE", "ingredient/" + id + "/delete", null, addIngredientsListeners);
    });
    $('#recipe-ingredients ul li').click(function() {
        var $checkbox = $(this).find('input')
        $checkbox.attr('checked', !$checkbox.attr('checked'));
    });
    $('#show-ingredients-plain-text').click(function() {
        $('#ingredients-plain-text-modal').modal('show');
        $('#ingredients-plain-text-modal').on('shown.bs.modal', function () {
            $('#ingredients-plain-text-textarea').select();
        });
    });
}

function addStepsListeners() {
    $('#add-step-button').click(function() {

        payload = new FormData();
        //payload.append("image", ($('#step-image')[0].files[0])); // stupid html
        payload.append("image", document.getElementById("step-image").files[0]);
        payload.append("desc", $('#step-desc').val());
        payload.append("weight", 0);

        ajax($('#recipe-steps'), "POST", "steps", payload, addStepsListeners).done(function() {
            $("#step-desc").focus();
        });
    });
    $('.remove-step-button').click(function() {
        var id = $(this).attr('data-id');
        ajax($('#recipe-steps'), "DELETE", "step/" + id + "/delete", null, addStepsListeners);
    });
    $('.move-step-up').click(function() {
        var id = $(this).attr('data-id');
        ajax($('#recipe-steps'), "PUT", "step/" + id + "/move/up", null, addStepsListeners);
    });
    $('.move-step-down').click(function() {
        var id = $(this).attr('data-id');
        ajax($('#recipe-steps'), "PUT", "step/" + id + "/move/down", null, addStepsListeners);
    });
    addUploadButtonNameListerer();
}

function addUploadButtonNameListerer() {
    $(document).on('change', ':file', function() {
        var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '').slice(0,15) + "...";
        $('#step-image-upload-text').html(label);
    });
}

function addImagePopupListeners() {
    $(".img-thumbnail").click(function() {
        // here asign the image to the modal when the user click the enlarge link
        $('#imagepreview').attr('src', $(this).attr('src'));
        $('#imagemodal').modal('show');
    });
}

function addPeopleAdjustmentListener() {
    $('#people').change(function() {
        var people = $(this).val();
        ajax($('#recipe-ingredients'), "GET", "ingredients?people=" + people, null, addIngredientsListeners)
    });
}

$( document ).ready(function() {
    addIngredientsListeners();
    addStepsListeners();
    addImagePopupListeners();
    addPeopleAdjustmentListener();

});
