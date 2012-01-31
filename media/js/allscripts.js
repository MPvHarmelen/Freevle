$(document).ready(function(){

//Dropdowns
  $('ul.dropdown').hide();

  $("li.menu, #settingicon").hover(function() {
      $(this).children("ul.dropdown").stop(true, true).slideDown('fast');
    }, function() {
      $(this).children("ul.dropdown").stop(true, true).slideUp('fast');
    });


//Menu backgrounds
  var menuLi = $('li.menu, div.header');

  menuLi.hover(function() {
      $(this).children('a.header').css('background-color', '#eee');
  }, function() {
      $(this).children('a.header').css('background-color', '#fff');
  });


//Height
  var height = $('.dag').css('height');
  $('.divider').css('height', height);
  $('#weekend').css('height', height);


//Weekend
  var vrijdag = /*HIER MOET EEN true OF false KOMEN*/true;
  if(vrijdag === true) {
    $('.dag').css('width', '226px');
    $('#weekend').css('height', height);
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


//Inlogform
  $('#darken').hide();
  $('#loginhome').click(function() {
      $("#inlogform").animate({marginTop: '200px'}, {queue: false, duration: 'fast'});
      $('#darken').fadeIn('fast');
    });
  $('#closelogin').click(function() {
      $("#inlogform").animate({marginTop: '100px'}, {queue: false, duration: 'fast'});
      $('#darken').fadeOut('fast');
    });
  
//Menu backgrounds
  var menuLi = $('li.menu, div.header');

  menuLi.hover(function() {
      $(this).children('a.header').css('background-color', '#eee');
  }, function() {
      $(this).children('a.header').css('background-color', '#fff');
  });


  $('ul.dropdown').hide();
  $("li.menu").hover(function() {
      $(this).children("ul.dropdown").stop(true, true).slideDown('fast');
    }, function() {
      $(this).children("ul.dropdown").stop(true, true).slideUp('fast');
    });
});

document.createElement('header');
document.createElement('footer');

