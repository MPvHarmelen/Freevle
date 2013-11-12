var textSection = '<section class="added">\
                    <label for="subtitle">Kopje:</label> \
                    <input type="text" class="subtitle" name="#" placeholder="Kopje">\
                    <button class="deletesection button">Verwijder deel</button>\
                    <textarea placeholder="Inhoud..." name="#"></textarea>\
                  </section>'

var imageSection = '<section class="added">\
                      <button class="deletesection button">Verwijder deel</button>\
                      <input type="file" id="subtitle" name="#">\
                      <div class="filemask">\
                        <p>Kies een afbeelding</p>\
                        <div></div>\
                      </div>\
                    </section>'


function menuOpener() {
  $('div#menuopener').toggleClass('opened');
  $('nav#sidebar').toggleClass('opened');
  $('body').toggleClass('opened');
}

function readURL(input) {
  if(input.prop('files') && input.prop('files')[0]) {
    var reader = new FileReader();

    reader.onload = function(e) {
      input.next().children('div').html('<img src="' + e.target.result + '">');
    }

    reader.readAsDataURL(input.prop('files')[0]);
  }
}

function slugger(titleInput) {
  var slug = titleInput.val()
      .toLowerCase()
      .replace(/[^\w ]+/g,'')
      .replace(/ +/g,'-')
      .substring(0,255);
  $('#slug').text(slug);
  $('[name=slug]').val(slug);
}

$(document).ready(function() {

/*MENU*/
  $('div#menuopener').click(function() {
    menuOpener();
  });


/*CHECKBOXES PAGELIST*/
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


/*FILTER INPUTS*/
  $('input + label').click(function() {
    $(this).prev().click();
  });


/*CATEGORY COLOR*/
  $('select[name=category]').addClass($('select[name=category]').children('option:selected').val());
  $('select[name=category]').change(function() {
    $(this).removeClass();
    $(this).addClass($(this).children('option:selected').val());
  });


/*FILE-UPLOAD HIDER*/
  $(document).on('click', '.filemask', function() {
    $(this).prev().click();
  });

  $(document).on('change', 'input[type=file]', function() {
    $(this).next().children('p').text($(this).val().replace("C:\\fakepath\\", ""));
    readURL($(this));
  });


/*NEW SECTION*/
  $('#newsection div').click(function() {
    if($(this).attr('id') == 'newtext') {
      $('form#editor').append(textSection);
      $('form#editor').children('.added').slideDown('fast');
    } else {
      $('form#editor').append(imageSection);
      $('form#editor').children('.added').slideDown('fast');
    }
  });


/*SECTION DELETE*/
  $(document).on('click', '.deletesection', function(e) {
    var really = confirm('Weet je zeker dat je dit wil verwijderen?');
    if(really == false) {
      e.preventDefault();
    } else {
      e.preventDefault();
      $(this).parent().slideUp(400);
      setTimeout(function() {
        $(this).parent().remove();
      }, 400);
    }
  });


/*PHOTO SELECT*/
  $('#gallery > div').click(function() {
    $(this).children('input').click();
  });

  $('#gallery > div').click(function() {
    $(this).prev('input').click();
  });

  $(document).on('change', '#gallery input[type=file]', function() {
    if($(this).prop('files').length == 1) {
      $(this).next().html('Je hebt<span>' + $(this).prop('files').length + '</span>foto toegevoegd');
    } else {
      $(this).next().html('Je hebt<span>' + $(this).prop('files').length + '</span>foto\'s toegevoegd');
    }
  });

  $(document).on('click', '.delete', function(e) {
    var really = confirm('Weet je zeker dat je dit wil verwijderen?');
    if(really == false) {
      e.preventDefault();
    }
  });

});
