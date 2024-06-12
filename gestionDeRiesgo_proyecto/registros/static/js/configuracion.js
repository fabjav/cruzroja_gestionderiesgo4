const ValidarDatos = async (event) => {
    event.preventDefault();
    const formData = new FormData(id_form_config_inicial);
    try{   
        const response = await fetch('/validar_datos_login/', {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        let contenido = `<p>${data.data.contraseña}</p>`;
        let contenido_p = `<p>${data.data.contraseña_p}</p>`
        id_estado_contraseñas.innerHTML = contenido;
        id_estado_contraseñas_p.innerHTML = contenido_p;
        


    }catch(error){
        console.log(error)
    }

}
/**
 * 
 * <script type="text/javascript">
        var tipo = "{{ tipo }}";
        console.log("Tipo:", tipo);
        // Aquí puedes usar el valor de 'tipo' en tu script
    </script>

    const llenadoDinamico = async () => {
    try {
        const response = await fetch('/ruta/a/tu/vista/actualizar_contraseña'); // Reemplaza con la URL correcta
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        console.log(data);
        // Aquí puedes usar 'data.tipo' para lo que necesites
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}
 */

const cargaInicial = async () => {
    //aca van las funciones y los controles de evento
    id_form_config_inicial.addEventListener('submit', function(event){
        ValidarDatos(event);
    });
}

window.addEventListener('load', async () => {
    await cargaInicial();
});