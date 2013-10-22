$(document).ready(function() {

  function menuOpener() {
    $('div#menuopener').toggleClass('opened');
    $('nav#sidebar').toggleClass('opened');
    $('body').toggleClass('opened');
  }

  $('div#menuopener').click(function() {
    menuOpener();
  });

  $('ul.pages input').change(function() {
    if($(this).prop('checked')) {
      $(this).prop('checked', false)
             .parent().parent().addClass('selected');
    } else {
      $(this).prop('checked', true)
             .parent().parent().removeClass('selected');
    }
  });

  $('ul.pages .checkboxcont').click(function() {
    var checkbox = $(this).children();
    if(checkbox.prop('checked')) {
      $(this).parent().removeClass('selected');
      checkbox.prop('checked', false);
    } else {
      $(this).parent().addClass('selected');
      checkbox.prop('checked', true);
    }
  });

  $('input + label').click(function() {
    $(this).prev().click();
  });

});
