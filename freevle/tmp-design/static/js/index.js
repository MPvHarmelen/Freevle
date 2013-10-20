$(document).ready(function() {

  function hideOrShowCygnus(toTop,when) {
    if(toTop > when) {
      $('header h1').addClass('yepshow');
    } else {
      $('header h1').removeClass('yepshow');
    }
  }

  function coverBottom() {
    var liHeight = 0;
    $('ul#quicknav > li').each(function() {
      if($(this).outerHeight() > liHeight) {
        liHeight = $(this).outerHeight();
      }
    });
    if($('body').innerWidth() > 999) {
      $('#indexcover').css('margin-bottom', -liHeight-24);
      $('ul#quicknav > li').css('height', liHeight);
    } else {
      $('#indexcover').css('margin-bottom', 0);
      $('ul#quicknav > li').css('height', 'auto');
    }
  }

  coverBottom();

  if($(window).width() > 1000) {
    $(window).scroll(function() {
      hideOrShowCygnus($(window).scrollTop(), 180);
    });
  } else {
    $(window).scroll(function() {
      hideOrShowCygnus($(window).scrollTop(), 120);
    });
  }

  $(window).resize(function() {
    coverBottom();
  });

});
