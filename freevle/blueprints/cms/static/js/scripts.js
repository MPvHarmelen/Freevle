var focusstatus = false;

$(document).ready(function() {
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



  $('#menuopener').click(function(e) {
    e.preventDefault();
    $(this).toggleClass('opened');
    $('header ul').toggleClass('opened');
  });

  $('#searchopener').click(function(e) {
    e.preventDefault();
    $(this).toggleClass('opened');
    $('header form').toggleClass('opened');
  });


  $('input[type=search]').focusin(function() {
    $(this).addClass('opened');
  }).focusout(function() {
    if($(this).val().length == 0) {
      $(this).removeClass('opened');
    }
  });


  if($(window).width() > 1000) {
    $('header .button, div#login .close').click(function(e) {
      e.preventDefault();
      toggleLoginForm();
    });
  }


  disablrLogin();

  $('#login input').keyup(function() {
    disablrLogin();
  });


  $('#jumpto a').click(function() {
    var headerId = $(this).attr('href');
    var offsetHeading = $(headerId).offset().top - 70;
    scrollTo(offsetHeading);
  });

  if(window.location.hash) {
    var offsetHeading = $(window.location.hash).offset().top - 70;
    scrollTo(offsetHeading);
  }


  $('input').focusin(function() {
    focusstatus = true;
  }).focusout(function() {
    focusstatus = false;
  });


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


  if($('#subjectoverview')) {
    var minHeightLi = 0;
    $('#subjectoverview > ul > li').each(function() {
      if($(this).height() > minHeightLi) {
        minHeightLi = $(this).outerHeight();
      }
    }).css('min-height', minHeightLi);
  }


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

    if(e.keyCode == 83 && !focusstatus || e.keyCode == 191 && !focusstatus) {//S
      $('input[type=search]').focus();
    }
  });
});
