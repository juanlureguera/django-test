var listLogin = ['usrname', 'psw'];

function loginUser(){
    var usrname = "", psw = "";
    var ok = true;
    for (var idx = 0; idx < listLogin.length; idx++) {
        if ($('#' + listLogin[idx]).val() == "") {
            ok = false;
        } else {
            if ($('#' + listLogin[idx])[0].id == "usrname") {
                loginUserName = $('#' + listLogin[idx]).val();
            } else if ($('#' + listLogin[idx])[0].id == "psw") {
                loginPassword = $('#' + listLogin[idx]).val();
            } else {
                ok = false;
            }
        }
    }
    if( ok ){
        $.ajax({
            url: '/loginS/',
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                usrname: $('#usrname').val(),
                psw: $('#psw').val(),
            },
            dataType: 'text',
            type: 'POST',
            success: function (data) {
                if (data == "not") {
                    alert("Usuario o contraseña invalidos");
                    for (var idx = 0; idx < listLogin.length; idx++) {
                        $('#' + listLogin[idx]).val("");
                    }
                    $('#' + listLogin[0])[0].focus();
                }
                else if ( data == "Error al crear la sesion"){
                    alert('Error al crear la sesion');
                }
                else if ( data == "Credenciales no validas"){
                    alert('Credenciales no validas');
                }
                else if ( data == "No hubo errores"){
                    window.location.reload();
                }
            },
            failure: function (data) {
                alert('Ha ocurrido un error');
            }
        });
    }
}

$(document).ready(function(){
    $("#href-login").click(function(){
        $("#modal-login").modal();
    });
});