$(document).ready(function() {

  function hideOrShowCygnus(toTop) {
    if(toTop > 180) {
      $('header h1').addClass('yepshow');
    } else {
      $('header h1').removeClass('yepshow');
    }
  }

  if($(window).width() > 1000) {
    $(window).scroll(function() {
      hideOrShowCygnus($(window).scrollTop());
    });
  }

});
