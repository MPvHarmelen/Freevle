var focusstatus = false;

$(document).ready(function() {

  function disablr() {
    var lengthUname = $('#login input[type=text]').val().length;
    var lengthPwd = $('#login input[type=password]').val().length;
    if(lengthUname > 0 && lengthPwd > 0) {
      $('#login input[type=submit]').removeAttr('disabled');
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

  $('#login input').focusout(function() {
    disablr();
  });
  $('#login input').keyup(function() {
    disablr();
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
