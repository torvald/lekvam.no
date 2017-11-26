
function addListListeners() {
    $('.note-modal-click-area').off().click(function(e) {
        if (e.target !== this)
            // prevent sub elements to be clickable
            return;
        var text = $(this).data('text');
        var formatedDue = $(this).data('formated-due');
        var formatedText = $(this).data('formated-text');
        var listid = $(this).data('listid');
        var noteid = $(this).data('noteid');

        $("#modal-edit-text").val(text);
        $("#modal-show-text").html(formatedText);
        $("#modal-due-input").val(formatedDue);
        $("#modal-listid-input").val(listid);
        $("#modal-noteid-input").val(noteid);

        $("#note-modal").modal();
        addModalListeners();
    });

    sortable('.sortable', {
        connectWith: '.connected'
    })[0].addEventListener('sortupdate', onNoteDragnDrop);

    $('.mark-as-done').off().click(function() {
        var id = $(this).parents(".note").attr('data-id');
        var listDiv = $(this).parents(".todo-list");
        ajax(listDiv, "PUT", "notes/" + id + "/done", null, addListListeners);
    });
}

function onNoteDragnDrop(e) {
    var noteid = $(e.detail.item).attr('data-id');
    var toListid = $(e.detail.endparent).attr('id');
    var fromListid = $(e.detail.startparent).attr('id');
    var toIndex = e.detail.elementIndex;

    payload = new FormData();
    payload.append('toListid', toListid);
    payload.append('fromListid', fromListid);
    payload.append('toIndex', toIndex);

    if (toListid === 'waiting-for') {
        confirm("Add date");
    }

    ajax(null, "POST", "notes/" + noteid + "/move", payload, null).done(function() {
        resetAddNoteForm();
    });
}

function addTodoListeners() {
    $('#search-input').click(function() {
        $('#most-active-tags').show();
    });
    $('#archive-search-button').click(function() {
        $('#hidden-archive-input').val("1");
        $('#search-form').submit();
    });
    $('.add-note-button').click(function() {
        var listid = $(this).data("listid");
        payload = new FormData();
        payload.append("image", document.getElementById("note-image").files[0]);
        payload.append("text", $('#note-text').val());
        payload.append("listid", listid);

        ajax($('#list-' + listid), "POST", "notes", payload, addListListeners).done(function() {
            resetAddNoteForm();
            $('#note-text').focus().click();
        });
    });
    addUploadButtonNameListerer();
    addListListeners();
}


function addUploadButtonNameListerer() {
    $(document).on('change', ':file', function() {
        var input = $(this),
        label = input.val().replace(/\\/g, '/').replace(/.*\//, '').slice(0,15) + "...";
        $('#note-image-upload-text').html(label);
    });
}

function resetAddNoteForm() {
    $('#add-note-form').trigger("reset");
    $('#note-image-upload-text').html("Last opp bilde");
}

function addModalListeners() {
    $('.datepicker').datepicker({
         format: 'yyyy-mm-dd',
         todayBtn: true,
         autoclose: true,
         startDate: '-1d',
    });
    $('#modal-show-text').show();
    $('#modal-edit-text').hide();
    $('#modal-show-text').off().click(function() {
        $(this).hide();
        var editText = $('#modal-edit-text');
        editText.show();
        editText.focus();
    });
    $('#modal-change-note').off().click(function() {
        var noteid = $("#modal-noteid-input").val();

        due = $("#modal-due-input").val();
        text = $("#modal-edit-text").val();
        listid = $("#modal-listid-input").val();

        payload = new FormData();
        payload.append('due', due);
        payload.append('text', text);
        payload.append('listid', listid);

        var listDiv = $("#list-" + listid);
        searchQuery = searchQueryURLEnding();
        ajax(listDiv, "POST", "notes/" + noteid + searchQuery, payload, addListListeners);

        $("#note-modal").modal('hide');
    });
}

function searchQueryURLEnding() {
    var query = $('#search-input').val();
    if (query !== "") {
        return "?query=" + encodeURIComponent(query);
    }
    return "";
}

function autoGrowTextarea() {
    $("textarea").on('keyup focus', function(e) {
        while($(this).outerHeight() < this.scrollHeight + parseFloat($(this).css("borderTopWidth")) + parseFloat($(this).css("borderBottomWidth"))) {
            $(this).height($(this).height()+1);
        };
    });
}

$( document ).ready(function() {
    $('#show-help-text').click(function(e) {
        e.preventDefault();
        $('#help-text').toggle("slow");
    });
    addTodoListeners();
    resetAddNoteForm();
    $('#note-text').focus().click();
    autoGrowTextarea();
});
