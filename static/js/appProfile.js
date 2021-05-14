window.onload = function () {
	$('#save').addClass('disabled');
	$('#cancel').addClass('disabled');
	$('a#passchange').text('Ver datos personales');
}
var list = [ 'txtname', 'txtEmail', 'dni', 'txtCuentaB' ];
function edit() {
    for (var idx = 0; idx < list.length; idx++)
        document.getElementById(list[idx]).readOnly = false;

	$('#edit').addClass('disabled');
    $('#save').removeClass();
	$('#cancel').removeClass();
}
function cancel() {
	if( $("#cancel").attr('class') != "disabled" ){
        for (var idx = 0; idx < list.length; idx++)
            document.getElementById(list[idx]).readOnly = true;

        $('#edit').removeClass();
        $('#save').addClass('disabled');
		$('#cancel').addClass('disabled');
	}
}
function save(){
	if( $("#save").attr('class') != "disabled" ){
		if( validateProfile( ) ){
			$('#modal-save').modal('show');

	    	$('#edit').removeClass();	
	    	$('#save').addClass('disabled');
			$('#cancel').addClass('disabled');

			for (var idx = 0; idx < list.length; idx++) {
	            document.getElementById(list[idx]).readOnly = true;
			}
		}
		else{
			alert("Existen campos necesarios vacios.");
		}
	}
}
function changebornDateConfirmation(){
	getDate(true);
	$('#modal-bornDateChange').modal('show');
}
function changePassConfirmation(){
	$('#modal-passChange').modal('show');
}
function returnFunction(){
	if( $("#edit").attr('class') == "disabled" ) {
		$('#modal-confirmation').modal('show');
			$(document).ready(function(){
      			$("#yesConfirm").click(function(e){
	        		window.location.href = "http://127.0.0.1:8000";
      			});
	    	});
	}
	else{
		window.location.href = "http://127.0.0.1:8000";
	}
}

var txtname = "", txtpassword = "", dni = "", txtEmail = "", txtCuentaB = "", txtPasswordConfirm = "", txtBornDate = "", nPass = "no", newBorn = "";
var passNew, bordDateNew;

function validateProfile() {
    // grabar
    var nameCOK = false, emailOk = false, dniOk = false, cuentaOk = false;
    for (var idx = 0; idx < list.length; idx++){
        if ($('#' + list[idx])[0].id == "txtname" && $('#' + list[idx]).val() != "") {
            txtname = $('#' + list[idx]).val();
            nameCOK = true;
        } else if ($('#' + list[idx])[0].id == "txtEmail" && $('#' + list[idx]).val() != "") {
            txtEmail = $('#' + list[idx]).val();
            emailOk = true
        } else if ($('#' + list[idx])[0].id == "dni") {
            dni = $('#' + list[idx]).val();
            dniOk = true;
        } else if ($('#' + list[idx])[0].id == "txtCuentaB") {
            txtCuentaB = $('#' + list[idx]).val();
            cuentaOk = true;
        } else if ($('#' + list[idx])[0].id == "txtBornDate") {
            txtBornDate = $('#' + list[idx]).val();
        }
    }
    if( nameCOK && dniOk && cuentaOk && emailOk ) {
    	passNew = false;
    	return true;
    }
    else{
    	return false;
    }
}
function validateChangeBornDate(){
	var day = $('#day').val();
	var month = $('#month').val();
	var year = $('#year').val();

	newBorn = year+"-"+month+"-"+day;
	bordDateNew = true;
	validatePass();

}
function validateChangePass(){
	var rePassNew = "";
	nPass = $('#passNew').val();
	rePassNew = $('#rePassNew').val();

	if( nPass == rePassNew ) {
		passNew = true;
		validatePass();
	}
	else{
		alert("No coinciden las contraseñas.");
	}
}
function validatePass() {
	var p = "";
	if( passNew ) {
		p = $('#passActual').val();
	}
	else if( bordDateNew ) {
		p = $('#txtPasswordView').val();
	}
	else{
		p = $('#txtPasswordConfirm').val();
	}

    if( !passNew ) {
        txtPasswordConfirm = $('#txtPasswordView').val();
        nPass = txtPasswordConfirm;
    }
    if( !bordDateNew ) {
        newBorn =  $('#txtBornDate').val();
    }

    $.ajax({
        url: '/saveProfile/',
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            txtname: $('#txtname').val(),
            dni: $('#dni').val(),
            txtEmail: $('#txtEmail').val(),
            txtBornDate: newBorn,
            txtCuentaB: $('#txtCuentaB').val(),
            nPass: nPass,
            txtPasswordView: $('#txtPasswordView').val()

        },
        dataType: 'text',
        type: 'POST',
        success: function (data) {
            if ( data == "Error al cambiar los datos del usuario"){
                alert('Error al cambiar los datos del usuario');
            }
            else if ( data == "Error usuario no encontrado"){
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
    passNew = false;
    newBorn = false;

	
}
var caset = true;
function changeTypePass(){
	if(caset){
		$('a#passchange').text('Ocultar datos personales');
		$('#txtPasswordView').attr('type', 'text');
		$('#dni').attr('type', 'text');
		caset = false;
	}
	else{
		$('a#passchange').text('Ver datos personales');	
		$('#txtPasswordView').attr('type', 'password');
		$('#dni').attr('type', 'password');
		caset = true;
	}
}