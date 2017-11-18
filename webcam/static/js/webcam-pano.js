$( document ).ready(function() {
    $('#datepicker').datepicker({
         format: 'yyyy-mm-dd',
         todayBtn: true,
         autoclose: true,
         endDate: '-1d',
    });
    $('#datepicker input').change(function () {
       // TODO change
      window.location.href = "https://lekvam.no/webcam/pano/" + $(this).val();
    });
});
