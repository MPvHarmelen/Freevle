var focusstatus = false;

/*FUNCTIONS*/
$.fn.setCursorPosition = function(pos) {
  if ($(this).get(0).setSelectionRange) {
    $(this).get(0).setSelectionRange(pos, pos);
  } else if ($(this).get(0).createTextRange) {
    var range = $(this).get(0).createTextRange();
    range.collapse(true);
    range.moveEnd('character', pos);
    range.moveStart('character', pos);
    range.select();
  }
}

function fetchSearch(searchInput, callback) {
  var svalue = searchInput.val();

  if(svalue.length > 2) {
    $.ajax({
      type: "POST",
      url: "/zoek/autocompletion/",
      data: {
        value: svalue
      }
    }).done(function(back) {
        response = back;
        if(callback) {
          callback(searchInput);
        }
    });
  }
}

function processSearch(searchInput) {
  if(response['results'] === 'true') {
    var toReplace = searchInput.val();
    var reg = new RegExp(toReplace,"gi");

    $('div#aclist').html('');

    for(var key in response) {
      if(response.hasOwnProperty(key) && key !== 'results') {
        var itemName = response[key]['name'].replace(reg, '<b>' + toReplace + '</b>');
        var itemUrl = response[key]['url'];
        var listItem = '<a href="' + itemUrl + '">' + itemName + '</a>';
        console.log(itemName);
        $('div#aclist').append(listItem);
      }
    }

    $('div#aclist').children(':first').addClass('selected');
  } else {
    $('div#aclist').html('<li class="noresult"><i>Geen resultaten</i></li>');
  }
}


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

function sameHeight(first) {
  if($('#subjectoverview')) {
    if(window.innerWidth > 999) {
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
  if(window.innerWidth > 999) {
    for(var i = 0; i < places.length; i++) {
      if(places[i-1] < $(window).scrollTop() && places[i] > $(window).scrollTop()) {
        $('.youarehere').removeClass('youarehere');
        n = i + 1;
        $('#jumpto li:nth-of-type('+n+') a').addClass('youarehere');
      }
    }
  }
}

function jumpToBottom() {
  var breakpoint = $('footer').offset().top - 164;
  if($(window).scrollTop() + $(window).height() > breakpoint) {
    $('nav#jumpto').css({ 'bottom': $('footer').height() + 66, 'position': 'absolute' });
  } else {
    $('nav#jumpto').css({ 'bottom': '2em', 'position': 'fixed' });
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

  var places = [];
  $(window).load(function() {

    if(window.location.hash) {
      var offsetHeading = $(window.location.hash).offset().top - 70;
      scrollTo(offsetHeading);
    }

    $('#jumpto li a').each(function() {
      var headerId = $(this).attr('href');
      if(headerId === '#top') {
        offsetHeading = 0;
      } else {
        var offsetHeading = $(headerId).offset().top - 71;
      }
      places.push(offsetHeading);
    });

    $('#jumpto a:first').addClass('youarehere');
  });

  $(window).scroll(function() {
    jumptoFeedback(places);
    if(window.innerWidth > 999) {
      jumpToBottom();
    }
  });


  /*FOCUSSTATUS*/
  $('input').focusin(function() {
    focusstatus = true;
  }).focusout(function() {
    focusstatus = false;
  });


  /*AUTOCOMPLETION*/
  $('input[name=search]').keyup(function(e) {
    if(e.keyCode === 38) { //uparrow
      $(this).setCursorPosition($(this).val().length);
      if($('div#aclist a:first').hasClass('selected')) {
        $('div#aclist .selected').removeClass('selected')
        $('div#aclist a:last').addClass('selected');
      } else {
        $('div#aclist .selected').removeClass('selected')
                             .prev().addClass('selected');
      }

    } else if(e.keyCode === 40) { //downarrow
      if($('div#aclist a:last').hasClass('selected')) {
        $('div#aclist .selected').removeClass('selected')
        $('div#aclist a:first').addClass('selected');
      } else {
        $('div#aclist .selected').removeClass('selected')
                             .next().addClass('selected');
      }

    } else {
      if($(this).val().length > 2) {
        fetchSearch($(this), processSearch);
      } else {
        $('div#aclist').html('');
      }
    }
  }).click(function() {
    if($(this).val().length > 2) {
      fetchSearch($(this), processSearch);
    } else {
      $('div#aclist').html('');
    }
  });

  $('form#search').submit(function(e) {
    e.preventDefault();
    var selectedHref = $('div#aclist .selected').attr('href');
    if(selectedHref != undefined && selectedHref != '') {
      window.location = selectedHref;
    }
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


  /*FLASHED MESSAGES*/
  setTimeout(function() {
    $('.messagecont').fadeOut(1000);
  }, 2000);

  $(window).blur(function() {
    $('.messagecont').stop().css('opacity', '1');
  }).focus(function() {
    setTimeout(function() {
      $('.messagecont').fadeOut(2000);
    }, 2000);
  });
});
