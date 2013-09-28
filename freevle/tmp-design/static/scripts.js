$(document).ready(function() {
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
    $('header .button, form#login .close').click(function(e) {
      e.preventDefault();
      $('header .button').toggleClass('dialog');
      $('form#login').toggleClass('dialog');
    });
  }
});
