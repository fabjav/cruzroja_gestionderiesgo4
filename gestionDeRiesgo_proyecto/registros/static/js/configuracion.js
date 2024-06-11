const llenadoDinamico = async () => {
    try{
        const response = await fetch("./configuracion_inicial");
        const data = await response.json();
        console.log(data);
    }catch(error){
        console.log (error);
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
}

window.addEventListener('load', async () => {
    await cargaInicial();
});