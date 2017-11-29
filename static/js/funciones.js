/**
 * 
 */


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getProvincias(pais_id, url){
  	$.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
  	$.ajax({
	  method: "POST",
	  url: url,
	  data: { pais_id: pais_id}
	}).done(function( respuesta ) {
        $("#id_provincia").empty()

        $.each( respuesta, function( index, value )
        {
            $('#id_provincia').append('<option value="'+value.id+'">'+value.nombre+'</option>')
        });
	});
  }
  
function getCiudades(provincia_id, url){
  	$.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
  	$.ajax({
	  method: "POST",
	  url: url,
	  data: { provincia_id: provincia_id}
	}).done(function( respuesta ) {
        $("#id_ciudad").empty()

        $.each( respuesta, function( index, value )
        {
            $('#id_ciudad').append('<option value="'+value.id+'">'+value.nombre+'</option>')
        });
	});
  }