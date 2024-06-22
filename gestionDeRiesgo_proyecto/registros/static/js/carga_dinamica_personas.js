function calculateAge(dateString) {
    const birthDate = new Date(dateString);
    const now = new Date();
    const age = now.getFullYear() - birthDate.getFullYear();
    const monthDiff = now.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birthDate.getDate())) {
        return age - 1;
    }
    return age;
}

const llenarTabla = async (idCasa) => {
    try {
        const response = await fetch(`./get_persona/${idCasa}`);
        const data = await response.json();

        if (data.message === 'Success') {
            const personas = data.personas;
            console.log(personas);
            let contenido_tabla = '';

            personas.forEach((persona) => {
                contenido_tabla += `<tr>
                    <td>${persona.nombre}</td>
                    <td>${persona.apellido}</td>
                    <td>${calculateAge(persona.fecha_nac)} años</td>
                    <td>${persona.rol ? persona.rol : ''}</td>
                    <td>${persona.rol ? 'Sí' : 'No'}</td>
                    <td>${persona.casa.calle}, ${persona.casa.numero}</td>
                    <td>${persona.telefono_emergencia}</td>
                    <td>${persona.padecimientos.join(', ')}</td>
                    <td>${persona.medicamento ? persona.medicamento : ''}</td>
                    <td>${persona.dosis ? persona.dosis : ''}</td>
                </tr>`;
            });

            // Seleccionamos el cuerpo de la tabla
            const tbody = document.getElementById('id_tbody_personas');
            // Asignamos el contenido a la tabla
            tbody.innerHTML = contenido_tabla;
        } else {
            console.error('Error al obtener las personas:', data.message);
        }
    } catch (error) {
        console.error('Error en la solicitud:', error);
    }
};


const listarCasas = async (idBarrio) => {
    try{
        const response = await fetch(`./get_casa/${idBarrio}`);
        const data = await response.json();
        if (data.message === 'Success'){
            let opciones_p = ``;
            casas = data.casas;
            casas.forEach((casa) =>{
                opciones_p += `<option value="${casa.id}">${casa.nombre}</option>`;
            });
            id_opc_casas.innerHTML = opciones_p;
            llenarTabla(data.casas[0].id);
        }else{
            console.log('no hay casas');
            id_opc_casas.innerHTML = `<option value="">No hay casas registradas</option>`;
        }


    }catch(error){
        console.log(error);
    }
}


const listarBarrios = async (idDistrito) => {
    try{
        
        const response = await fetch(`./get_barrio/${idDistrito}`);
        const data = await response.json();
        if (data.message === 'Success'){
            let opciones_p = ``;
            console.log(data.barrios);
            barrios = data.barrios;
            barrios.forEach((barrio) =>{
                opciones_p += `<option value="${barrio.id}">${barrio.nombre}</option>`;
            });
            id_opc_barrios.innerHTML = opciones_p;
            if (id_opc_barrios.value === 'todos') {
                id_opc_casas.disabled = true;
                id_opc_casas.style.backgroundColor = 'gray';
            } else {
                listarCasas(data.barrios[0].id);
            }
        }else{
            console.log('no hay distritos');
        }


    }catch(error){
        console.log(error);
    }
}

const listarDistritos = async (idDepartamento) => {
    try{
        const response = await fetch(`./get_distrito/${idDepartamento}`);
        const data = await response.json();

        if (data.message === 'Success'){
            id_main_barrios.style.display = 'block';
            id_main_casas.style.display = 'block';
            let opciones_p = ``;
            distritos = data.distritos;
            distritos.forEach((distrito) =>{
                opciones_p += `<option value="${distrito.id}">${distrito.nombre}</option>`;
            });
            id_opc_distritos.innerHTML = opciones_p;
            if (id_opc_distritos.value === 'todos') {
                id_opc_barrios.disabled = true;
                id_opc_barrios.style.backgroundColor = 'gray';
                id_opc_casas.disabled = true;
                id_opc_casas.style.backgroundColor = 'gray';
                listarBarrios(data.distritos[0].id);
            } else {
                listarBarrios(data.distritos[0].id);
            }
        }else{
            console.log('no hay distritos');
            id_opc_distritos.innerHTML = `<option value="">No hay distritos cargados.</option>`;
            id_main_barrios.style.display = 'none';
            id_main_casas.style.display = 'none';
        }
    }catch(error){
        console.log(error);
    }
}

const listarDepartamentos = async (idProvincia) => {
    try{
        const response = await fetch(`./get_departamento/${idProvincia}`);
        const data = await response.json();

        if (data.message === 'Success'){
            let opciones_p = ``;
            departamentos = data.departamentos;
            departamentos.forEach((departamento) =>{
                opciones_p += `<option value="${departamento.id}">${departamento.nombre}</option>`;
            });
            id_opc_departamentos.innerHTML = opciones_p;
            listarDistritos(data.departamentos[0].id);
        }else{
            console.log('no hay provincias xd');
        }
    }catch(error){
        console.log(error);
    }
}

const listarProvincias = async (idPais) => {
    try{
        const response = await fetch(`./get_provincia/${idPais}`);
        const data = await response.json();

        if (data.message === 'Success'){
            let opciones_p = ``;
            provincias = data.provincias;
            provincias.forEach((provincia) =>{
                opciones_p += `<option value="${provincia.id}">${provincia.nombre}</option>`;
            });
            id_opc_provincias.innerHTML = opciones_p;
            listarDepartamentos(data.provincias[0].id);
        }else{
            console.log('no hay provincias xd');
        }
    }catch(error){
        console.log(error);
    }
}

const listarPaises = async () => {
    try{
        const response = await fetch ('./get_pais');
        const data = await response.json();

        if(data.message === 'Success'){
            let opciones = ``;
            data.paises.forEach((pais)  => {
                opciones += `<option value='${pais.id}'>${pais.nombre}</option>`
            });
            id_opc_pais.innerHTML = opciones;
            listarProvincias(data.paises[0].id);

        }else {
            console.log('no hay paises xdxd');
        }
    }catch(error){
        console.log(error);
    }
}

const cargaInicial = async()=>{
    await listarPaises();

    id_opc_pais.addEventListener('change', (event)=>{
        listarProvincias(event.target.value);
    });
    id_opc_provincias.addEventListener('change', (event) => {
        listarDepartamentos(event.target.value);
    });
    id_opc_departamentos.addEventListener('change', (event) => {
        listarDistritos(event.target.value);
    });
    id_opc_distritos.addEventListener('change', (event) => {
       listarBarrios(event.target.value);
           
    });
    id_opc_barrios.addEventListener('change', (event) => {
        listarCasas(event.target.value);
        
    });
    id_opc_casas.addEventListener('change', (event) => {
        llenarTabla(event.target.value);
    });

};


window.addEventListener('load', async() => {
    await cargaInicial();
});
