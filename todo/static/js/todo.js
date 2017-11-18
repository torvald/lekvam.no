
function notify(data) {
    console.log(data);
}

$( document ).ready(function() {
    $('#show-help-text').click(function(e) {
        e.preventDefault();
        $('#help-text').toggle("slow");
    });
    sortable('.sortable', {
        connectWith: '.connected'
    });
});

