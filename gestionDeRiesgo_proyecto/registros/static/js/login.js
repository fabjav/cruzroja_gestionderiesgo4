const enviarDatosLogin = async (event) => {
    event.preventDefault();

    const formData = new FormData(id_login_form);
    
    try{
        const response = await fetch(id_login_form.action, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        if (data.data.es_admin && data.data.primer_login){
            console.log('si es admin y es primer login');
            const tipo = '1';
            /*
            const userId = data.data.user_id;
            window.location.href = `/configuracion_inicial/?user_id=${userID}`; */
            window.location.href = `/configuracion_inicial/?tipo=${tipo}`;
        }else if(data.data.primer_login){
            console.log('no es admin y es primer login');
            const tipo = '2';
            /*
            const userId = data.data.user_id;
            window.location.href = `/configuracion_inicial/?user_id=${userID}`; */
            window.location.href = `/configuracion_inicial/?tipo=${tipo}`;

            //window.location.href = '/index/';
        }

        
          
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