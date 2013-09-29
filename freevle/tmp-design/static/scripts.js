$(document).ready(function() {

  function disablr() {
    var lengthUname = $('#login input[type=text]').val().length;
    var lengthPwd = $('#login input[type=password]').val().length;
    if(lengthUname > 0 && lengthPwd > 0) {
      $('#login input[type=submit]').removeAttr('disabled');
    }
  }

  function loginForm() {
    $('div#login').toggleClass('dialog');
    if($('div#login').css('-webkit-transform') == 'matrix(0, 0, 0, 0, 0, 0)') {
      $('div#login input:first').focus();
    }
  }

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
      loginForm();
    });
  }

  $('#login input').focusout(function() {
    disablr();
  });
  $('#login input').keyup(function() {
    disablr();
  });
});
