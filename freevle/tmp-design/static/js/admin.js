$(document).ready(function() {

  function menuOpener() {
    $('div#menuopener').toggleClass('opened');
    $('nav#sidebar').toggleClass('opened');
    $('body').toggleClass('opened');
  }

  $('div#menuopener').click(function() {
    menuOpener();
  });

});
