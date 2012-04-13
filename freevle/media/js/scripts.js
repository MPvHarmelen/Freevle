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
    $('#id_username').focus();
  });
  $('#closelogin').click(function() {
    $('#darken').fadeOut('fast');
    $('#id_username, #id_password, #id_email').blur();
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

  if($('#focus')) {
    $('#focus').focus();
    focusstatus = true;
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

//Settings-tabs
  $('#tabs').width($('.tab').length * 850);
  var url = $(location).attr('href');
  var aLink = 'a.tabnav[href="#' + url.split('#')[1] + '"]';
  var tabIdUrl = '#tab' + url.split('#')[1];
  var marginMove = '-' + $(tabIdUrl).prevAll('.tab').length * 850 + 'px';
  if (/#/i.test(url)) {
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
    var tabId = '#tab' + $(this).attr('href').split('#')[1];
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

//Focusstatus
  $('input, textarea').focus(function() {
    focusstatus = true;
  }).focusout(function() {
    focusstatus = false;
  });

//Live passwordchecker
  $('#confirm-password').keyup(function() {
    if($('#new-password').val() != $('#confirm-password').val()) { 
      if($('#checkifsame').is(":hidden")) {
        $('#checkifsame').animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
        $('#triangleleft').animate({ left: '441px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
      }
      $('#checkifsame').text('The passwords don\'t match.');
      $('#confirm-password').css('background-image', 'url(/media/img/redcross.png)');
    } else {
      $('#confirm-password').css('background-image', 'url(/media/img/check.png)');
      $('#checkifsame').animate({ left: '457px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
      $('#triangleleft').animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
    }
  }).focus(function() {
    if($('#confirm-password').val()) {
      $('#checkifsame').animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
      $('#triangleleft').animate({ left: '441px' }, {queue: false, duration: 'fast'}).fadeIn('fast');
    }
  }).focusout(function() {
    $('#checkifsame').animate({ left: '457px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
    $('#triangleleft').animate({ left: '449px' }, {queue: false, duration: 'fast'}).fadeOut('fast');
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
  if (e.keyCode == 27) {//Esc
    $('#closelogin').click();
  }
  if (e.keyCode == 76 && !focusstatus) {//L
    $('#loginhome').click();
  }
  if (e.keyCode == 83 && !focusstatus) {//S
    $('#search-box').focus();
  }
});

document.createElement('header');
document.createElement('footer');
