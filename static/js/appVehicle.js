window.onload = function () {
	$('#save').addClass('disabled');
	$('#cancel').addClass('disabled');
}

var list = [ 'matricula', 'marca', 'modelo', 'anio', 'km' ];

function cancel() {
	if( $("#cancel").attr('class') != "disabled" ){
        for (var idx = 0; idx < list.length; idx++)
            document.getElementById(list[idx]).readOnly = true;

        $('#edit').removeClass();
        $('#save').addClass('disabled');
		$('#cancel').addClass('disabled');
	}
}
function edit() {
    for (var idx = 0; idx < list.length; idx++)
        document.getElementById(list[idx]).readOnly = false;

	$('#edit').addClass('disabled');
    $('#save').removeClass();
	$('#cancel').removeClass();
}
function save(){
	if( $("#save").attr('class') != "disabled" ){
        $('#edit').removeClass();
        $('#save').addClass('disabled');
        $('#cancel').addClass('disabled');
    }
    saveVehicle();

}
function saveVehicle(){
    var matricula, modelo, marca, anio, km;
    for (var idx = 0; idx < list.length; idx++){
        if ($('#' + list[idx])[0].id == "matricula" && $('#' + list[idx]).val() != "") {
            matricula = $('#' + list[idx]).val();
        } else if ($('#' + list[idx])[0].id == "marca" && $('#' + list[idx]).val() != "") {
            marca = $('#' + list[idx]).val();
        } else if ($('#' + list[idx])[0].id == "modelo") {
            modelo = $('#' + list[idx]).val();
        } else if ($('#' + list[idx])[0].id == "anio") {
            anio = $('#' + list[idx]).val();
        } else if ($('#' + list[idx])[0].id == "km") {
            km = $('#' + list[idx]).val();
        }
    }
    $.ajax({
			url: '/saveVehicle/',
			data: {
				csrfmiddlewaretoken: '{{ csrf_token }}',
				matricula: $('#matricula').val(),
				marca: $('#marca').val(),
				modelo: $('#modelo').val(),
				anio: $('#anio').val(),
				km: $('#km').val()

			},
			dataType: 'text',
			type: 'POST',
			success: function (data) {
				if ( data == "Error al cambiar los datos del usuario"){
					alert('Error al cambiar los datos del usuario');
				}
				else if ( data == "Error vehiculo no encontrado"){
					alert('Error usuario no encontrado');
				}
				else if ( data == "No hubo errores"){
					alert('¡Actualizado!');
					window.location.reload();
				}
			},
			failure: function (data) {
				alert('Ha ocurrido un error');
			}
		});
}