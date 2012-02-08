$(document).ready(function(){

//Slider
  var totWidth = 0;
  var positions = new Array();
  var currentPosition = 0;

  var bodyWidth = $('body').width();
  $('.slide').width(bodyWidth);

  $('#slides .slide').each(function(i){
      positions[i]= totWidth;
      totWidth += bodyWidth;
  });

  $('#slides').width(totWidth);
        $(‘#next-button’).click(function(e,keepScroll) {
          if (currentPosition < positions.length-1) {
            var pos = currentPosition+1;
            currentPosition = pos;
            var menuPosition = pos+2;
            /* Need max click handling */
            $('li.menuItem').removeClass('act').addClass('inact');
            $("#menu ul li:nth-child("+menuPosition+")").addClass('act');
            $('#slides').stop().animate({marginLeft:-positions[pos]+'px'},450);
            /* Start the sliding animation */
            e.preventDefault();
            /* Prevent the default action of the link */
            // Stopping the auto-advance if an icon has been clicked:
            if(!keepScroll) {
              clearInterval(itvl);
            }
          }
        });
        $('#prev-button').click(function(e,keepScroll) {
          if (currentPosition != 0) {
            var pos = currentPosition-1;
            currentPosition = pos;
            var menuPosition = pos+2;
            /* Need min click handling */
            $('li.menuItem').removeClass('act').addClass('inact');
            $("#menu ul li:nth-child("+menuPosition+")").addClass('act');
            $('#slides').stop().animate({marginLeft:-positions[pos]+'px'},450);
            /* Start the sliding animation */
            e.preventDefault();
            /* Prevent the default action of the link */
            // Stopping the auto-advance if an icon has been clicked:
            if(!keepScroll) {
              clearInterval(itvl);
            }
          }
        });
  $('a.li').click(function(e, keepScroll){
      $('a.li').removeClass('act').addClass('inact');
      $(this).removeClass('inact').addClass('act');

      var pos = $(this).parent().prevAll('.slidernav').length;
      var currentPosition = pos;
      $('#slides').stop().animate({marginLeft:-positions[pos]+'px'},450);
      e.preventDefault();
  });

  $('a.li').addClass('inact')
  $('a.li:first').removeClass('inact').addClass('act');

  var current=1;
  function autoAdvance()
  {
      if(current==-1) return false;
      $('a.li').eq(current%$('a.li').length).trigger('click',[true]);
      current++;
  }
  var changeEvery = 3;
  var interval = setInterval(function(){autoAdvance()},changeEvery*1000);


//Height
  var height = $('.dag').css('height');
  $('.divider').css('height', height);
  $('#weekend').css('height', height);


//Weekend
  var vrijdag = /*HIER MOET EEN true OF false KOMEN*/true;
  if(vrijdag === true) {
    $('div.dag').addClass('weekendday');
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
      var topMargin = (($(window).height / 2) - ($('#inlogform') / 2));
      $("#inlogform").animate({marginTop: topMargin}, {queue: false, duration: 'fast'});
      $('#darken').fadeIn('fast');
    });
  $('#closelogin').click(function() {
      $('#inlogform').animate({marginTop: '100px'}, {queue: false, duration: 'fast'});
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

