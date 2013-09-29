var focusstatus = false;

$(document).ready(function() {

  function isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
  }

  function disablrLogin() {
    var lengthUname = $('#login input[type=text]').val().length;
    var lengthPwd = $('#login input[type=password]').val().length;
    if(lengthUname > 0 && lengthPwd > 0) {
      $('#login input[type=submit]').removeAttr('disabled');
    } else {
      $('#login input[type=submit]').attr('disabled', 'disabled');
    }
  }

  function disablrLost() {
    var emailVal = $('#lost input[type=email]').val();
    if(emailVal.length > 0 && isEmail(emailVal)) {
      $('#lost input[type=submit]').removeAttr('disabled');
    } else {
      $('#lost input[type=submit]').attr('disabled', 'disabled');
    }
  }

  function isLoginForm() {
    if($('div#login').css('-webkit-transform') == 'matrix(0, 0, 0, 0, 0, 0)') {
      return false;
    } else {
      return true;
    }
  }

  function toggleLoginForm() {
    $('div#login').toggleClass('dialog');
    if(!isLoginForm()) {
      $('div#login input:first').focus();
    }
  }

  $('input').focusin(function() {
    focusstatus = true;
  }).focusout(function() {
    focusstatus = false;
  });

  $('#menuopener').click(function() {
    $(this).toggleClass('opened');
    $('header ul').toggleClass('opened');
  });

  $('#searchopener').click(function() {
    $(this).toggleClass('opened');
    $('header form').toggleClass('opened');
  });

  $('input[type=search]').focusin(function() {
    $(this).addClass('opened');
  }).focusout(function() {
    if($(this).val().length == 0) {
      $(this).removeClass('opened');
    }
  });

  if($(window).width() > 1000) {
    $('header .button, div#login .close').click(function(e) {
      e.preventDefault();
      toggleLoginForm();
    });
  }

  $('#login input').keyup(function() {
    disablrLogin();
  });

  $('#lost input').keyup(function() {
    disablrLost();
  });

  $(document.documentElement).keyup(function(e) {
    if(e.keyCode == 27) {//Esc
      $('input').blur();
      if(isLoginForm()) {
        toggleLoginForm();
      }
    }

    if(e.keyCode == 76 && !focusstatus) {//L
      if(!isLoginForm()) {
        toggleLoginForm();
      }
    }

    if(e.keyCode == 83 && !focusstatus || e.keyCode == 191 && !focusstatus) {//S
      $('input[type=search]').focus();
    }
  });
});
