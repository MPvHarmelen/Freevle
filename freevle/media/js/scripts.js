var focusstatus = false;
$(document).ready(function(){

//Slider
  $('a.li').addClass('inact')
  $('a.li:first').removeClass('inact').addClass('act');

  var amountPictures = 9;

  var totWidth = amountPictures * $('.slide').width();
  $('#slides').width(totWidth);
  var currentPos = 0;

  function advance() {
    $('#slides').stop(true, true).animate({marginLeft: '-' + currentPos * 799 + 'px'});
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


//Speech bubbles
  $("div.uure,div.uuru").hover(function(event) {
      if(event.target != $(this).children("ul.huiswerk")[0]) {
        $(this).children("ul.huiswerk").stop(true, true).animate({top: '33px'}, {queue: false, duration: 'fast'}).fadeIn('fast');
        $(this).children("div.triangle").stop(true, true).animate({top: '2px'}, {queue: false, duration: 'fast'}).fadeIn('fast');
      }
    }, function(event) {
      $(this).children("ul.huiswerk").stop(true, true).animate({top: '55px'}, {queue: false, duration: 'fast'}).fadeOut('fast');
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
    $('#id_username').focus();
  });
  $('#closelogin').click(function() {
    $('#darken').fadeOut('fast');
    $('#id_username, #id_password, #id_email').blur();
  });
  if($(window).width() > 900) {
    centerInlogForm();
  }

  $(window).resize(function() {
    if($(window).width() > 900) {
      centerInlogForm();
    }
  });

//Menu backgrounds

  if($(window).width() > 900) {
    $('ul.dropdown').hover(function() {
        $(this).prev('a.menuitem').addClass('menuhover');
    }, function() {
        $(this).prev('a.menuitem').removeClass('menuhover');
    });

    $('ul.dropdown').hide();
    $('li.navmenu').hover(function() {
      $(this).children('ul.dropdown').stop(true, true).slideDown('fast');
    }, function() {
      $(this).children('ul.dropdown').stop(true, true).slideUp('fast');
    });
  }

  if($('#focus').length != 0) {
    $('#focus').focus();
    focusstatus = true;
  }


//Login and password functionality
  $('#password').hide();
  $('#focusonpassword').click(function() {
    $('#password').fadeIn('fast');
    $('#focuslogin').fadeOut('fast');
    if($(window).width() > 900) {
      $('#inlogform').animate({'height': '371px'}, 'fast');
      $('#loginandpassword').animate({'margin-left': '-280px'}, 'fast');
    } else {
      $('#loginandpassword').animate({'margin-left': -$(window).width() + 'px'}, 'fast');
    }
  });
  $('#focusonlogin').click(function() {
    $('#password').fadeOut('fast');
    $('#focuslogin').fadeIn('fast');
    $('#loginandpassword').animate({'margin-left': '0'}, 'fast');
    if($(window).width() > 900) {
      $('#inlogform').animate({'height': '337px'}, 'fast');
    }
  });

/*Settings-tabs
  $('#tabs').width($('.tab').length * 850);
  var url = $(location).attr('href');
  var urlParts = url.split('/')
  var aLink = 'a.tabnav[href="/settings/' + urlParts[urlParts.length-2] + '/"]';
  var tabIdUrl = '#tab' + urlParts[urlParts.length-2];
  var marginMove = '-' + $(tabIdUrl).prevAll('.tab').length * 850 + 'px';
  if (/settings\/(\w*)\//i.test(url)) {
    $(aLink).css('border-color', '#007');
    $('#tabs').animate({ 'margin-left': marginMove }, 'fast');
    if($(tabIdUrl).height() > 365) {
      $('#tabbrowser').height($(tabIdUrl).height());
    } else {
      $('#tabbrowser').height(365);
    }
  } else {
    $('#tabbrowser').height(365);
    $('a.tabnav:first').css('border-color', '#007');
  }
  $(this).css('border-color', '#007');
  $('a.tabnav').click(function() {
    $('a.tabnav').css('border-color', '#fff');
    $(this).css('border-color', '#007');
    var href = $(this).attr('href')
    var tabId = '#tab' + href.split('/')[href.split('/').length-2];
    var amountTabs = $(tabId).prevAll('.tab').length
    var marginMove = '-' + amountTabs * 850 + 'px';
    if($(tabId).height() > 365) {
      var changeHeight = $(tabId).height() + 'px';
    } else {
      var changeHeight = '365px';
    }
    $('#tabs').animate({ 'margin-left': marginMove }, 'fast');
    $('#tabbrowser').animate({ 'height': changeHeight }, 'fast');
  });

//Prettier history
  var History = window.History;
  $('.settingsmenu a').click(function(e) {
    History.replaceState(null, null, $(this).attr('href'));
    e.preventDefault();
  });*/

//Focusstatus
  $('input, textarea').focus(function() {
    focusstatus = true;
  }).focusout(function() {
    focusstatus = false;
  });

//Live passwordchecker
  var confirmPasswd = $('#confirm-password');
  var newPasswd = $('#new-password');
  var checkIfSame = $('#checkifsame');
  var triangleLeft = $('#triangleleft');

  confirmPasswd.keyup(function() {
    if(newPasswd.val() != confirmPasswd.val()) { 
      if(checkIfSame.is(":hidden")) {
        checkIfSame.animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
        triangleLeft.animate({ left: '441px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
      }
      checkIfSame.text('The passwords don\'t match.');
      confirmPasswd.css('background-image', 'url(/media/img/redcross.png)');
    } else {
      confirmPasswd.css('background-image', 'url(/media/img/check.png)');
      checkIfSame.animate({ left: '457px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
      triangleLeft.animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
    }
  }).focus(function() {
    if(confirmPasswd.val()) {
      checkIfSame.animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
      triangleLeft.animate({ left: '441px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
    }
  }).focusout(function() {
    checkIfSame.animate({ left: '457px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
    triangleLeft.animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
  });



  if($(window).width() < 900) {
    $('#menutoggle').click(function() {
      if($('nav').css('left') === '-100%') {
        $('nav').animate({ 'left': '-54px' }, 'fast');
      } else {
        $('nav').animate({ 'left': '-100%' }, 'fast');
      }
    });
  }

/*----------------EASTEREGG, YEEEY :D :D :D :D----------------*/
konami = new Konami()
  konami.code = function() {
    $('body').attr('id', 'konami').append('<div id="rainbow"></div><div id="flyingbird"></div><audio src="/media/Nyan_cat.ogg" loop controls autoplay>');
  }
  konami.load()
});

//Ctrl+
//$.ctrl = function(key, callback, args) {
//    $(document).keydown(function(e) {
//        if(!args) args=[];
//        if(e.keyCode == key.charCodeAt(0) && e.ctrlKey) {
//            callback.apply(this, args);
//            return false;
//        }
//    });
//};
//$.ctrl('S', function() {
//  $('.course').click();
//});

//Other keyboardfunctions
$(document.documentElement).keyup(function(e) {
  if(e.keyCode == 27) {//Esc
    $('#closelogin').click();
    $('input[type="text"], input[type="password"]').blur();
  }
  if(e.keyCode == 76 && !focusstatus) {//L
    $('#loginhome').click();
  }
  if(e.keyCode == 83 && !focusstatus) {//S
    $('#search-box').focus();
  }
  if(e.keyCode == 75 && !focusstatus && $('.conversation').length > 1) {
    if($('.conversation:first').hasClass('selected') !== true) {
      $('.selected').removeClass('selected').prev('li').addClass('selected');
    }
  }
  if(e.keyCode == 74 && !focusstatus && $('.conversation').length > 1) {
    if($('.conversation:last').hasClass('selected') !== true) {
      $('.selected').removeClass('selected').next('li').addClass('selected');
    }
  }
});

document.createElement('header');
document.createElement('footer');
