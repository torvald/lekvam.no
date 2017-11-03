$( document ).ready(function() {
    $('#datepicker').datepicker({
         format: 'yyyy-mm-dd',
         todayBtn: true,
         autoclose: true,
         endDate: '-1d',
    });
    $('#datepicker input').change(function () {
       // TODO change
      window.location.href = "http://193.35.52.75:12333/webcam/pano/" + $(this).val();
    });
});
