$(document).ready(function() {

  function disablrSettings(a) {
    var passFirst = $('input[name=firstpass]').val();
    var passSecnd = $('input[name=secndpass]').val();

    if(passFirst.length < 6 && passSecnd.length < 6) {
      $('#settings input[type=submit]').attr('disabled', 'disabled');
      if(a) {
        a.html('Het wachtwoord is <strong>te kort</strong>.').removeClass('okay');
      }

    } else if(passFirst !== passSecnd) {
      $('#settings input[type=submit]').attr('disabled', 'disabled');
      if(a) {
        a.html('De wachtwoorden zijn <strong>niet gelijk</strong>.').removeClass('okay');
      }

    } else {
      $('#settings input[type=submit]').removeAttr('disabled');
      if(a) {
        a.html('De wachtwoorden zijn gelijk!').addClass('okay');
      }
    }

  }

  disablrSettings();

  $('#settings input').keyup(function() {
    disablrSettings($('#samechecker'));
  });

});
