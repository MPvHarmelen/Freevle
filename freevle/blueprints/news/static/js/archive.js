$(document).ready(function() {
  $('#archivepicker .button').hide();

  $('select').change(function() {
    $('#archivepicker').submit();
  });
});
