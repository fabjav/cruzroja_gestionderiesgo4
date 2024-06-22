const Formulario_barrio = async () =>{
    //alert ('tood ok');
    try{
        const response = await fetch('./crear_barrio/');
        const data = await response.json();
        console.log(data.html_content);
        id_content_crear_barrio.innerHTML = data.html_content;

    }catch(error){
        console.log(error);
    }
    cerrarVentana_1.addEventListener('click', function(){
        id_form_crear_barrio.style.display = 'none';
    });
};

const Formulario_casa = async () =>{
    try{
        const idBarrio = id_opc_barrios.value;
        console.log(idBarrio);
        const response = await fetch(`./crear_casa/${idBarrio}`);
        const data = await response.json();
        console.log(data.html_content);
        id_content_crear_casa.innerHTML = data.html_content;

    }catch(error){
        console.log(error);
    }
    cerrarVentana_2.addEventListener('click', function(){
        id_form_crear_casa.style.display = 'none';
    });
}
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
            id_form_crear_barrio.style.display = 'none';
        } else if (data.message == 'Error') {
            mensaje = '<p>Faltan Datos</p>';
        } else if (data.message == 'Exist') {
            mensaje = '<p>El barrio ya existe</p>';
        } else {
            mensaje = '<p>No se encontró el distrito</p>';
        }

        const id_mensaje = document.getElementById('id_mensaje');
        id_mensaje.innerHTML = mensaje;
        id_mensaje.classList.add('show');

        // Deslizar el mensaje hacia adentro
        setTimeout(() => {
            id_mensaje.classList.remove('show');
        }, 2000); // Esperar 2 segundos antes de desaparecer

    } catch (error) {
        console.log(error);
    }
}
const CrearCasa = async(event) =>{
    event.preventDefault();
    const barrio = id_opc_barrios.value;
    const formData = new FormData(id_formulario_crear_casa);
    formData.append('barrio', barrio);
    try{
        const response = await fetch(`./crear_casa/${0}`,{
            method : 'POST',
            body: formData,

        });

        const data = await response.json();
        let mensaje = '';
        if (data.message == 'Success') {
            mensaje = '<p>Casa creado con exito</p>';
            id_formulario_crear_casa.reset();
            id_form_crear_casa.style.display = 'none';

            listarCasas(barrio);
        } else if (data.message == 'Error') {
            mensaje = '<p>Faltan Datos</p>';
        } else if (data.message == 'Exist') {
            mensaje = '<p>La casa ya existe</p>';
        } else {
            mensaje = '<p>No se encontró el barrio</p>';
        }

        const id_mensaje = document.getElementById('id_mensaje');
        id_mensaje.innerHTML = mensaje;
        id_mensaje.classList.add('show');

        // Deslizar el mensaje hacia adentro
        setTimeout(() => {
            id_mensaje.classList.remove('show');
        }, 2000); // Esperar 2 segundos antes de desaparecer

    }catch(error){
        console.log(error);
    }

}


const CargaInicial = async() => {
    id_btn_crear_barrio.addEventListener('click', function(){
        id_form_crear_barrio.style.display = 'block';
        Formulario_barrio();
    });
    id_btn_crear_casa.addEventListener('click', function(){
        id_form_crear_casa.style.display = 'block';
        Formulario_casa();
    })

    id_formulario_crear_barrio.addEventListener('submit', function(event){
       CrearBarrio(event);
        
    });
    id_formulario_crear_casa.addEventListener('submit', function(event){
        CrearCasa(event);
    });


};

window.addEventListener('load', async () =>{
    await CargaInicial();
});