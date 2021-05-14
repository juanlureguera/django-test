function createRoute(){
	var origin = "", destinity = "", distance = "", duration = "", price = "", startdate = "";
    origin = getRouteOrigin();
    destinity = getRouteDestinity();
    distance = getDistancia();
    duration = getTiempo();
    price = getPrecio();
    startdate = document.getElementById("year").value + "-" + document.getElementById("month").value + "-" + document.getElementById("day").value;

    $.ajax({
        url: '/createRoute/',
        data: {
            csrfmiddlewaretoken: '{{ csrf_token }}',
            start: origin,
            end: destinity,
            distance: distance,
            duration: duration,
            price: price,
            startdate: startdate,
            hour: $('#hour').val(),
            minutes: $('#minutes').val()
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
                window.location.reload();
            }
        },
        failure: function (data) {
            alert('Ha ocurrido un error');
        }
    });
}
function getList(){
    $('#modal-routes').modal('show');
}
function viewProfile(){
    window.location.href = "http://127.0.0.1:8000/profile/";
}

function modalregisterdriver(){
    $("#modal-driver-register").modal()
}

var listRegister = [ 'bancR', 'matricula', 'marca', 'modelo', 'anios' , 'km' ];

function registerUserDriver(){
    var bancR = "", matricula = "", marca = "", modelo = "", anios = "", km = "";
    var ok = true;

    for (var idx = 0; idx < listRegister.length; idx++) {
        if ($('#' + listRegister[idx]).val() == "") {
            ok = false;
        }
        else {
            if ($('#' + listRegister[idx])[0].id == "bancR") {
                bancR = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "matricula") {
                matricula = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "marca") {
                marca = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "modelo") {
                modelo = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "anios") {
                anios = $('#' + listRegister[idx]).val();
            }
            else if ($('#' + listRegister[idx])[0].id == "km") {
                km = $('#' + listRegister[idx]).val();
            }
        }
    }
    if (ok) {
        $.ajax({
            url: '/register-driver/',
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                bancR: $('#bancR').val(),
                matricula: $('#matricula').val(),
                marca: $('#marca').val(),
                modelo: $('#modelo').val(),
                anios: $('#anios').val(),
                km: $('#km').val(),
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
                    window.location = "http://127.0.0.1:8000/driver-home";
                }
            },
            failure: function (data) {
                alert('Ha ocurrido un error');
            }
        });
    }
}
function modallogindriver(){
    $("#modal-login-confirmed").modal()
}

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
          url: '/login-driver/',
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
                    alert('Autentificado!');
                    window.location = "http://127.0.0.1:8000/driver-home";
              }
          },
          failure: function (data) {
              alert('Ha ocurrido un error');
          }
      });
  }
}

