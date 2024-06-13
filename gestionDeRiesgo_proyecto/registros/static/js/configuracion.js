const ValidarDatos = async (event) => {
    event.preventDefault();
    const formData = new FormData(id_form_config_inicial);
    try {
        const response = await fetch('/validar_datos_login/', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        let contenido = `<p>${data.data.html_content_1}</p>`;
        id_estado_contraseñas.innerHTML = contenido;
        let estado = data.data.estado_confirmar;

        let form_flotante = ``;
        if (estado === '1') {
            form_flotante += `<p>Contraseñas guardadas con éxito</p>
                    <input id="id_continuar" type="button" value="Continuar">`;
            id_boton_enviar_form.innerHTML = ``;
        }
        id_continuar.innerHTML = form_flotante;

    } catch (error) {
        console.log(error);
    }
}

const cargaInicial = async () => {
    // Asignación de variables para los elementos HTML
    const id_form_config_inicial = document.getElementById('id_form_config_inicial');
    const id_estado_contraseñas = document.getElementById('id_estado_contraseñas');
    const id_boton_enviar_form = document.getElementById('id_boton_enviar_form');
    const id_continuar = document.getElementById('id_continuar');

    // Eventos
    id_form_config_inicial.addEventListener('submit', function (event) {
        ValidarDatos(event);
    });

    id_continuar.addEventListener('click', function () {
        window.location.href = '/confirmar_admin'; // Cambia '/confirmar_admin' por la URL correcta
    });
}

window.addEventListener('load', async () => {
    await cargaInicial();
});
