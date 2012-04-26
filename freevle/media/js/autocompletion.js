$(document).ready(function() {
  var rearea = $('#searchresults');
  var searchfield = $('#search-box');

  $('.resul').live('click', function(){
      $('.activeres').removeClass('activeres');
      $(this).addClass('activeres');
      searchfield.focus();
  });

  rearea.hide();

  searchfield.focus(function() {
      var chars = $(this).val();
      if(chars.length >= 2) {
          rearea.stop(true, true).slideDown('fast');
      }
  });
  searchfield.blur(function() {
      rearea.stop(true, true).slideUp('fast');
  });
  searchfield.keydown(function(e) {
      if (e.keyCode == 38 || e.keyCode == 40) {
          var pos = this.selectionStart;
          this.selectionStart = pos; this.selectionEnd = pos;
          e.preventDefault();
      }
  });


  searchfield.keyup(function(e) {
      if(e.keyCode == 40) {
          if($('.resul:last').hasClass('activeres')) {
              $('.activeres').removeClass('activeres');
              rearea.children('li:first').addClass('activeres');
          } else {
              $('.activeres').removeClass('activeres').next('li').addClass('activeres');
          }
      } else if(e.keyCode == 38) {
          if(rearea.children('li:first').hasClass('activeres')) {
              $('.activeres').removeClass('activeres');
              rearea.children('li:last').addClass('activeres');
          } else {
              $('.activeres').removeClass('activeres').prev('li').addClass('activeres');
          }
      } else if(e.keyCode == 16 || e.keyCode == 17 || e.keyCode == 18 || e.keyCode == 19 || e.keyCode == 20 || e.keyCode == 35 || e.keyCode == 36 || e.keyCode == 37 || e.keyCode == 39 || e.keyCode == 91 || e.keyCode == 92) {

      } else if(e.keyCode == 13) {
          //Select this one
          
      } else {
          var chars = $(this).val();
          if(chars.length >= 2) {
              rearea.html('');
              rearea.append('<li id="hiddenres" class="activeres"></li>');
//              $.post('/search', { 'query': $(this).val() },
//                function(data) {
//                  var results = data;
//                }
//              )
              var results = ['aaaaa', 'aaaab', 'bbbbb'];
              for(var i = 0; i < results.length; i++) {
                  result = results[i];
                  result = result.replace(chars, '<strong>' + chars + '</strong>');
                  rearea.append('<li class="resul">' + result + '</li>');
              }
              rearea.slideDown('fast');
          } else {
              rearea.slideUp('fast');        
          }
      }
  });


  $('form#search').submit(function(e) {
    if (!$('li.activeres#hiddenres')[0]) {
      e.preventDefault();
      window.location.href = '/courses/wiskunde' /*$('.activeres').data*/;
    } else {
      e.preventDefault();
      alert('baa');
    }
  });

});
