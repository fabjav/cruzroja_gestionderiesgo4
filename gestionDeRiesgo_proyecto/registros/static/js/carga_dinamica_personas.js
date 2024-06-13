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
            console.log('no hay distritos');
        }


    }catch(error){
        console.log(error)
    }
}


const listarBarrios = async (idDistrito) => {
    try{
        const response = await fetch(`./get_barrio/${idDistrito}`);
        const data = await response.json();
        if (data.message === 'Success'){
            let opciones_p = ``;
            barrios = data.barrios;
            barrios.forEach((barrio) =>{
                opciones_p += `<option value="${barrio.id}">${barrio.nombre}</option>`;
            });
            id_opc_barrios.innerHTML = opciones_p;
            listarCasas(data.barrios[0].id);
        }else{
            console.log('no hay distritos');
        }


    }catch(error){
        console.log(error)
    }
}

const listarDistritos = async (idDepartamento) => {
    try{
        const response = await fetch(`./get_distrito/${idDepartamento}`);
        const data = await response.json();

        if (data.message === 'Success'){
            let opciones_p = ``;
            distritos = data.distritos;
            distritos.forEach((distrito) =>{
                opciones_p += `<option value="${distrito.id}">${distrito.nombre}</option>`;
            });
            id_opc_distritos.innerHTML = opciones_p;
            listarBarrios(data.distritos[0].id);
        }else{
            console.log('no hay distritos');
        }
    }catch(error){
        console.log(error)
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
        console.log(error)
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
        console.log(error)
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
