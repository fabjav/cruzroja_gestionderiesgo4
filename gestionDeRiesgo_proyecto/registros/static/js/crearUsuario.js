
const envioDatosCrearUsuario = async (event) => {
    event.preventDefault();

    const formData = new FormData(id_form_crear_usuario);
    try{
        const response = await fetch(id_form_crear_usuario.action, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.message){
            messages.innerHTML = `<p style="color: green;" id="successMessage">${data.message}</p>`;
            id_form_crear_usuario.reset();
        }
        if (data.error_message){
            messages.innerHTML = `<p style="color: red;" id="errorMessage">${data.error_message}</p>`;
        }

    }catch(error){
        console.log(error);
    }

}

const cargaInicial = async()=>{
    id_DNI_form.addEventListener('input', function(){
        id_usuario_form.value = 'CR'+id_DNI_form.value;
        id_contraseña_form.value = id_DNI_form.value;
    });
    id_form_crear_usuario.addEventListener('submit', function(event){
        envioDatosCrearUsuario(event);
    });

};


window.addEventListener('load', async() => {
    await cargaInicial();
});
