$(document).ready(function() {
  function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
  }

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
