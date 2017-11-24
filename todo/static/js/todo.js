
function addListListeners() {
    $('.note-modal-click-area').off().click(function(e) {
        if (e.target !== this)
            // prevent sub elements to be clickable
            return;
        $(this).next().modal("show");
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
    $('.add-note-button').click(function() {

        payload = new FormData();
        payload.append("image", document.getElementById("note-image").files[0]);
        payload.append("text", $('#note-text').val());
        payload.append("listid", $(this).data("listid"));
        var list = $(this).data("list");

        ajax($('.todo-list#' + list), "POST", "notes", payload, addListListeners).done(function() {
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
}

function addModalListeners() {
    $('.datepicker').datepicker({
         format: 'yyyy-mm-dd',
         todayBtn: true,
         autoclose: true,
         startDate: '-1d',
    });
    $('.modal .edit-text').hide();
    $('.modal .show-text').click(function() {
        var id = $(this).data('id');
        modalNoteId = "#modal-note-" + id
        var editText = $(modalNoteId + ' .edit-text');

        $(this).hide();
        editText.show();
        editText.focus();
    });
    $('.modal .change-note').click(function() {
        var noteid = $(this).data('id');
        modalNoteId = "#modal-note-" + noteid

        // list to update
        var listDiv = $(this).parents('.todo-list');

        due = $(modalNoteId + " .due-input").val();
        text = $(modalNoteId + " .edit-text").val();
        listid = $(modalNoteId + " .listid-input").val();

        payload = new FormData();
        payload.append('due', due);
        payload.append('text', text);
        payload.append('listid', listid);

        ajax(listDiv, "POST", "notes/" + noteid, payload, addListListeners);

        $(modalNoteId).modal('toggle');
    });
}

$( document ).ready(function() {
    $('#show-help-text').click(function(e) {
        e.preventDefault();
        $('#help-text').toggle("slow");
    });
    addTodoListeners();
    addModalListeners();
    resetAddNoteForm();
    $('#note-text').focus().click();
});
