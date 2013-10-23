var focusstatus = false;

/*FUNCTIONS*/
function scrollTo(place) {
  $('html, body').animate({ scrollTop: place }, 200);
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

function sameHeight(first) {
  if($('#subjectoverview')) {
    if($(window).width() > 1000) {
      $('#subjectoverview > ul > section').each(function() {
        var minHeightLi = 0;
        $(this).children('li').each(function() {
          if($(this).outerHeight() > minHeightLi) {
            if(first) {
              minHeightLi = $(this).outerHeight() + 2;
            } else {
              minHeightLi = $(this).outerHeight();
            }
          }
        }).css('min-height', minHeightLi);
      });
    } else {
      $('#subjectoverview > ul > li, #subjectoverview > ul > section > li').css('min-height', 0)
    }
  }
}

function jumptoFeedback(places) {
  if($(window).width() > 999) {
    for(var i = 0; i < places.length; i++) {
      if(places[i-1] < $(window).scrollTop() && places[i] > $(window).scrollTop()) {
        $('.youarehere').removeClass('youarehere');
        n = i + 1;
        $('#jumpto li:nth-of-type('+n+') a').addClass('youarehere');
      }
    }
  }
}


$(document).ready(function() {

  /*MOBILE MENU AND SEARCH OPENERS*/
  $('#menuopener').click(function(e) {
    e.preventDefault();
    $(this).toggleClass('opened');
    if($(window).width() < 1000) {
      $('body').height($(window).height() - 61).toggleClass('opened');
      $('header nav > ul').toggleClass('opened').height($(window).height());
    }
  });

  $('#searchopener').click(function(e) {
    e.preventDefault();
    $(this).toggleClass('opened');
    $('header form').toggleClass('opened');
  });


  /*OPEN AND CLOSE SEARCH-INPUT*/
  $('input[type=search]').focusin(function() {
    $(this).addClass('opened');
  }).focusout(function() {
    if($(this).val().length == 0) {
      $(this).removeClass('opened');
    }
  });


  /*LOGINFORM SHOWING*/
  $('header .button, div#login .close').click(function(e) {
    if($(window).width() > 1000) {
      e.preventDefault();
      toggleLoginForm();
    }
  });


  /*LOGIN-FORM CHECK EXECUTION*/
  $('#login input').keyup(function() {
    disablrLogin();
  });


  /*INPAGE NAVIGATION*/
  $('#jumpto a').click(function() {
    var headerId = $(this).attr('href');
    var offsetHeading = $(headerId).offset().top - 70;
    scrollTo(offsetHeading);
  });

  if(window.location.hash) {
    var offsetHeading = $(window.location.hash).offset().top - 70;
    scrollTo(offsetHeading);
  }

  var places = [];
  $(window).load(function() {

    $('#jumpto li a').each(function() {
      var headerId = $(this).attr('href');
      if(headerId === '#top') {
        offsetHeading = 0;
      } else {
        var offsetHeading = $(headerId).offset().top - 71;
      }
      places.push(offsetHeading);
      console.log(offsetHeading+headerId);
    });

    $('#jumpto a:first').addClass('youarehere');

    $(window).scroll(function() {
      jumptoFeedback(places);
    });
  });


  /*FOCUSSTATUS*/
  $('input').focusin(function() {
    focusstatus = true;
  }).focusout(function() {
    focusstatus = false;
  });


  /*AUTOCOMPLETION*/
  $('input[name=search]').keyup(function() {
    var svalue = $(this).val();

    $.ajax({
      type: "POST",
      url: "/zoek/autocompletion/",
      data: { value: svalue }
    })
      .done(function(back) {
        $('datalist#search').html(back);
      });
  });


  /*GIVE ITEMS ON OVERVIEW PAGE SAME HEIGHT*/
  sameHeight(true);

  /*MOBILE MENU RESIZE*/
  $(window).resize(function() {
    sameHeight(false);

    if($(window).width() < 1000) {
      $('header nav > ul').height($(window).height());
    }
  });


  /*KEYBOARD NAVIGATION*/
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

    if(e.keyCode == 83 && !focusstatus || e.keyCode == 191 && !focusstatus) {//S and /
      $('input[type=search]').focus();
    }
  });


  /*TOUCHEVENTS FOR MENU-SWIPE*/
  var touchX = 0;
  var touchY = 0

  document.addEventListener('touchstart', function(e) {
    var touch = e.touches[0];
    touchX = touch.pageX;
    touchY = touch.pageY;
  });

  document.addEventListener('touchend', function(e) {
    var touch = e.changedTouches[0];
    deltaTouchX = touch.pageX - touchX;
    deltaTouchY = Math.abs(touch.pageY - touchY);
    if(deltaTouchX > 0.2 * $(window).width() && deltaTouchY < 200) {
      if(!$('#menuopener').hasClass('opened')) {
        $('#menuopener').click();
      }
    } else if(deltaTouchX < -0.2 * $(window).width() && deltaTouchY < 200) {
      if($('#menuopener').hasClass('opened')) {
        $('#menuopener').click();
      }
    }
  });
});
