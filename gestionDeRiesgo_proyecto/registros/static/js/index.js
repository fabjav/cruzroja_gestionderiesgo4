const Formulario_barrio = async () =>{
    //alert ('tood ok');
    try{
        const response = await fetch('./crear_barrio/');
        const data = await response.json();
        console.log(data.html_content);
        id_form_crear_barrio.innerHTML = data.html_content;

    }catch(error){
        console.log(error);
    }
    cerrarVentana.addEventListener('click', function(){
        id_form_crear.style.display = 'none';
    });
};
const CrearBarrio = async (event) => {
    event.preventDefault();
    //alert('form enviado');
    const formData = new FormData(id_formulario_crear_barrio);
    try{   
        const response = await fetch('./crear_barrio/',{
            method: 'POST',
            body: formData
        });
        const data = await response.json();
        //console.log(data.message)
        let mensaje = ``;
        if (data.message == 'Success'){
            mensaje = `<p>Barrio creado con exito</p>`;
            id_formulario_crear_barrio.reset();
            id_form_crear.style.display = 'none';
        } else if (data.message == 'Error'){
            mensaje = `<p>Faltan Datos</p>`;
        }else if (data.message == 'Exist'){
            mensaje = `<p>El barrio ya existe</p>`;
        }else{
            mensaje = `<p>No se encontró el distrito</p>`;
        }
        id_mensaje.innerHTML = mensaje;

    }catch(error){
        console.log(error);
    }
}

const CargaInicial = async() => {
    id_btn_crear_barrio.addEventListener('click', function(){
        id_form_crear.style.display = 'block';
        Formulario_barrio()
    } );

    
    id_formulario_crear_barrio.addEventListener('submit', function(event){
        
        CrearBarrio(event);
        
    } );

};

window.addEventListener('load', async () =>{
    await CargaInicial();
});