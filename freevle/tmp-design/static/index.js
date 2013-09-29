$(document).ready(function() {

  function hideOrShowCygnus(toTop,when) {
    if(toTop > when) {
      $('header h1').addClass('yepshow');
    } else {
      $('header h1').removeClass('yepshow');
    }
  }

  if($(window).width() > 1000) {
    $(window).scroll(function() {
      hideOrShowCygnus($(window).scrollTop(), 180);
    });
  } else {
    $(window).scroll(function() {
      hideOrShowCygnus($(window).scrollTop(), 120);
    });
  }

});
