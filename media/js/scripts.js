$(document).ready(function(){

//Slider
  $('a.li').addClass('inact')
  $('a.li:first').removeClass('inact').addClass('act');

  var amountPictures = 9;

  var totWidth = amountPictures * $('.slide').width();
  $('#slides').width(totWidth);
  var currentPos = 0;

  function advance() {
    $('#slides').stop(true, true).animate({marginLeft: '-' + currentPos * 798 + 'px'});
  }

  function autoAdvance() {
    if(currentPos < 2) {
      currentPos++;
      advance();
      $('a.act:first').removeClass('act').addClass('inact')
                      .parent().next().children().removeClass('inact').addClass('act');
    } else if(currentPos === 2) {
      currentPos = 0;
      advance();
      $('a.act').removeClass('act').addClass('inact');
      $('a.li:first').removeClass('inact').addClass('act');
    }
  }

  var interval = setInterval(function(){autoAdvance()},3000);

  $('a.li').click(function(event) {
    event.preventDefault();
    $('a.act').removeClass('act').addClass('inact');
    $(this).removeClass('inact').addClass('act');
    currentPos = $(this).parent().prevAll('.slidernav').length;
    advance();
    window.clearInterval(interval);
  });


//Height
  var height = $('.dag').css('height');
  $('.divider').css('height', height);
  $('#weekend').css('height', height);


//Weekend
  if($('#rooster').length) {
    if(vrijdag === true) {
      $('div.dag').addClass('weekendday');
      $('#weekend').css('height', height);
    }
  }


//Speech bubbles
  $("div.uure,div.uuru").hover(function(event) {
			if(event.target != $(this).children("ul.huiswerk")[0]) {
				$(this).children("ul.huiswerk").stop(true, true).animate({top: '2px'}, {queue: false, duration: 'fast'}).fadeIn('fast');
				$(this).children("div.triangle").stop(true, true).animate({top: '2px'}, {queue: false, duration: 'fast'}).fadeIn('fast');
			}
    }, function(event) {
			$(this).children("ul.huiswerk").stop(true, true).animate({top: '20px'}, {queue: false, duration: 'fast'}).fadeOut('fast');
			$(this).children("div.triangle").stop(true, true).animate({top: '20px'}, {queue: false, duration: 'fast'}).fadeOut('fast');
    });

  $('div.uure, div.uuru, div.uuri').each(function() {
    var divClass = $(this).attr('class');
    if($('ul',this).length) {
      var huiswerk = $(this).children('ul.huiswerk').children('li:first').css('border-left-color');
      $(this).css('border-left-color', huiswerk);
    }
  });


  function centerInlogForm() {
    var windowHeight = $(window).height();
    var halfWindowHeight = (windowHeight / 2);
    var loginFormHeight = $('#inlogform').height();
    var halfLoginFormHeight = (loginFormHeight / 2);
    var topMargin = (halfWindowHeight - halfLoginFormHeight) - 40;
    $('#inlogform').css('margin-top', topMargin + 'px');
  }


//Inlogform
  $('#darken').hide();
  $('#loginhome').click(function() {
      $('#darken').fadeIn('fast');
      document.getElementById('id_username').focus();
    });
  $('#closelogin').click(function() {
      $('#darken').fadeOut('fast');
    });
  centerInlogForm();

  $(window).resize(centerInlogForm);

//Menu backgrounds

  $('ul.dropdown').hover(function() {
      $(this).prev('a.menuitem').css('background-color', '#008').css('color', '#fff');
  }, function() {
      $(this).prev('a.menuitem').css('background-color', 'transparent').css('color', '#333');
  });

  $('a.menuitem').hover(function(){
    $(this).css('background-color', '#008').css('color', '#fff');
  }, function() {
    $(this).css('background-color', 'transparent').css('color', '#333');
  });

  $('ul.dropdown').hide();
  $('li.navmenu').hover(function() {
      $(this).children('ul.dropdown').stop(true, true).slideDown('fast');
    }, function() {
      $(this).children('ul.dropdown').stop(true, true).slideUp('fast');
    });

  if(document.getElementById('focus')) {
    document.getElementById('focus').focus();
  }


  //Login and password functionality
  $('#password').hide();
  $('#focusonpassword').click(function() {
    $('#password').fadeIn('fast');
    $('#loginandpassword').animate({'margin-left': '-280px'}, 'fast');
    $('#focuslogin').fadeOut('fast');
    $('#inlogform').animate({'height': '357px'}, 'fast');
  });
  $('#focusonlogin').click(function() {
    $('#password').fadeOut('fast');
    $('#loginandpassword').animate({'margin-left': '0'}, 'fast');
    $('#focuslogin').fadeIn('fast');
    $('#inlogform').animate({'height': '337px'}, 'fast');
  });

});

//Ctrl+
$.ctrl = function(key, callback, args) {
    $(document).keydown(function(e) {
        if(!args) args=[];
        if(e.keyCode == key.charCodeAt(0) && e.ctrlKey) {
            callback.apply(this, args);
            return false;
        }
    });
};
$.ctrl('S', function() {
  $('.course').click();
});

//Other keyboardfunctions
$(document.documentElement).keyup(function(e) {
  if (e.keyCode == 27) {
    $('#closelogin').click();
  }
  if (e.keyCode == 145) {
    $('#loginhome').click();
  }
});

document.createElement('header');
document.createElement('footer');
