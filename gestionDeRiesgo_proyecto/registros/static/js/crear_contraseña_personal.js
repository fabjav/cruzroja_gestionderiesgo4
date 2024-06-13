const ValidarDatos = async (event) => {
    event.preventDefault();
    const formData = new FormData(form_contraseña_personal);
    try{
        const response = await fetch ('/validar_contraseña_personal/', {
            method : 'POST',
            body: formData

        });
        const data = await response.json();
        let contenido = `<p>${data.data.contraseña_p}</p>`;
        id_estado_contraseñas.innerHTML = contenido;
        let estado = data.data.estado;
        let form_flotante = ``;
        if(estado == '1'){
            form_flotante +=` <p>Contraseñas guardadas con exito</p>
                    <input id="id_continuar" type="button" value="Continuar">`;
            id_boton_enviar_form.innerHTML = ``;
        }
        id_continuar.innerHTML = form_flotante;

    }catch(error){
        console.log(error);
    }
}

const cargaInicial = async () => {
    //aca van las funciones y los controles de evento
    form_contraseña_personal.addEventListener('submit', function(event){
        ValidarDatos(event);
    });
    id_continuar.addEventListener('click', function() {
        window.location.href = '/'; // Cambia '/nueva-vista' por la URL de la vista a la que quieres redirigir
    });
}

window.addEventListener('load', async () => {
    await cargaInicial();
});