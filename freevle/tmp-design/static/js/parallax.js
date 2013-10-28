$(document).ready(function() {
  function resizeParBegin() {
    if(window.innerWidth > 999) {
      $('#parbegin').height($(window).height());
      $('body').css('padding-top', $(window).height());
    } else {
      $('#parbegin').height('auto');
      $('body').css('padding-top', '3.8em');
    }
  }

  $('div#pointdown').click(function() {
    scrollTo($(window).height());
  });

  $('[data-type="background"]').each(function(){
    var bgobj = $(this);

    $(window).scroll(function() {
      if(window.innerWidth > 999) {
        var yPos = -(($(window).scrollTop() - bgobj.offset().top) / bgobj.data('speed'));
        var coords = '50% '+ yPos + 'px';
        bgobj.css({ backgroundPosition: coords });
      } else {
        bgobj.css({ backgroundPosition: '50% 0%' });
      }
    });
  });

  resizeParBegin();

  $(window).resize(function() {
    resizeParBegin();
  });
});
