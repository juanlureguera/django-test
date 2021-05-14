function PuntuationDriver(){

    var puntuation = document.getElementById("punt").value;
    var idMessage = document.getElementById("idMessage").textContent;


    $.ajax({
            url: '/puntuation-driver/',
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                id: idMessage,
                puntuation: puntuation,
            },
            dataType: 'text',
            type: 'POST',
            success: function (data) {
            }
        });
}