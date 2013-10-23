function coverBottom() {
  var liHeight = 0;
  $('ul#quicknav > li').each(function() {
    if($(this).outerHeight() > liHeight) {
      liHeight = Math.round($(this).outerHeight());
    }
  });
  if(window.innerWidth > 999) {
    $('#indexcover').css('margin-bottom', -1 * (liHeight + 24));
    $('ul#quicknav li.more a').css('height', liHeight);
    $('ul#quicknav > li').css('min-height', liHeight);
  } else {
    $('#indexcover').css('margin-bottom', 0);
    $('ul#quicknav li.more a').css('height', '100%');
    $('ul#quicknav > li').css('min-height', 0);
  }
}

$(document).ready(function() {

  $(window).load(function() {
    coverBottom();
  });

  $(window).resize(function() {
    coverBottom();
  });

});
