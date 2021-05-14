var listRegister = [ 'usrnameR','dniR','nameR', 'emailR', 'pswR', 'pswcR', 'bancR' ];

function registerUser(){
    var usrnameR = "", dniR = "", nameR = "", borndateR = "", emailR = "",  pswcR = "", pswR = "";
    var ok = true;
    borndateR = document.getElementById("year").value + "-" + document.getElementById("month").value + "-" + document.getElementById("day").value;

    for (var idx = 0; idx < listRegister.length; idx++) {
        if ($('#' + listRegister[idx]).val() == "") {
            ok = false;
        }
        else {
            if ($('#' + listRegister[idx])[0].id == "usrnameR") {
                usrnameR = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "dniR") {
                dniR = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "nameR") {
                nameR = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "emailR") {
                emailR = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "pswR") {
                pswR = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "pswcR") {
                pswcR = $('#' + listRegister[idx]).val();
            }
             else if ($('#' + listRegister[idx])[0].id == "bancR") {
                bancR = $('#' + listRegister[idx]).val();
            }
            else {
                ok = false;
            }
        }
    }
    if(usrnameR.length <= 0 || usrnameR == ""){
        alert('Tamaño de nombre incorrecto.');
        ok = false;
    }
    else if(pswR.length <= 0 || pswR == ""){
        alert('Tamaño de contraseña incorrecto.');
        ok = false;
    }
    else if(pswR != pswcR){
        alert('Contraseñas no coinciden.');
        ok = false;
    }
    if (ok) {
        $.ajax({
            url: '/register/',
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                usrnameR: $('#usrnameR').val(),
                dniR: $('#dniR').val(),
                nameR: $('#nameR').val(),
                emailR: $('#emailR').val(),
                borndateR: borndateR,
                pswR: $('#pswR').val(),
                bancR: $('#bancR').val(),
            },
            dataType: 'text',
            type: 'POST',
            success: function (data) {
                if ( data == "Error al crear el registro"){
                    alert('Error al crear el registro');
                }
                else if ( data == "Nombre de usuario ya existente"){
                    alert('Nombre de usuario ya existente');
                }
                else if ( data == "Datos del Registro Errores"){
                    alert('Datos del Registro Errores');
                }
                else if ( data == "No hubo errores"){
                    alert('Registro realizado correctamente.');
                    $('#modal-register').modal('hide');
                    $("#modal-login").modal('show');
                    $("#usrname").val(usrnameR);
                }
            },
            failure: function (data) {
                alert('Ha ocurrido un error');
            }
        });
    }
}
$(document).ready(function(){
    $("#href-register").click(function(){
        $("#modal-register").modal();
        //BornDate function
        getDate(true);
    });
});
