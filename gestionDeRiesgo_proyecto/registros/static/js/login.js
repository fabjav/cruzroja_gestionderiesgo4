const enviarDatosLogin = async (event) => {
    event.preventDefault();

    const formData = new FormData(id_login_form);
    
    try{
        const response = await fetch(id_login_form.action, {
            method: 'POST',
            body: formData
        });
         
    }catch(error){
        console.log(error);
    }
}



const cargaInicial = async () => {
    id_login_form.addEventListener('submit', function(event){
        enviarDatosLogin(event);
    });
   
}

window.addEventListener('load', async () => {
    await cargaInicial();
});