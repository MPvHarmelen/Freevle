$(document).ready(function() {
  function disablrLost() {
    var emailVal = $('#lost input[type=email]').val();
    if(emailVal.length > 0 && isEmail(emailVal)) {
      $('#lost input[type=submit]').removeAttr('disabled');
    } else {
      $('#lost input[type=submit]').attr('disabled', 'disabled');
    }
  }

  disablrLost();

  $('#lost input').keyup(function() {
    disablrLost();
  });

  $('input[type=email]').focus();
});
