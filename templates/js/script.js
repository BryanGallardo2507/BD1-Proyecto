const files = [
    { name: "Documento1.docx", type: "Documento", lastModified: "10 nov 2023", size: "15 KB" },
    { name: "Imagen.jpg", type: "Imagen", lastModified: "5 nov 2023", size: "2.5 MB" },
    { name: "Presentación.pptx", type: "Presentación", lastModified: "28 oct 2023", size: "5.2 MB" }
];

const fileList = document.getElementById('fileList');
const gridViewContent = document.getElementById('gridViewContent');
const listViewContent = document.getElementById('listViewContent');
const gridViewButton = document.getElementById('gridView');
const listViewButton = document.getElementById('listView');
const newButton = document.getElementById('newButton');


function renderListView() {
    fileList.innerHTML = '';
    archivos.archivos.forEach(file => {
        const row = document.createElement('tr');
        row.innerHTML = `            
            <td>
                <svg class="file-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M13 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V9L13 2Z" stroke="#5f6368" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M13 2V9H20" stroke="#5f6368" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                ${file.nombre_archivo}
            </td>
            <td>${file.id_usuario__nombre}</td>
            <td>${file.fecha_guardado}</td>
            <td>${file.tamanio}MB</td>
            <td class="dropdown">
                <svg style="height:24px; width=24px;" class="dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false"
                    xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                    <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>
                </svg>
                <ul class="dropdown-menu">
                    <li><a onclick="eliminarArchivo(${file.id})" class="dropdown-item" href="#">Eliminar mwejkwej</a></li>                    
                </ul>
            <td>                 
        `;
        fileList.appendChild(row);
    });
}

function renderGridView() {
    gridViewContent.innerHTML = '';
    archivos.archivos.forEach(file => {
        const item = document.createElement('div');
        item.className = 'grid-item';
        item.style.position = "relative";
        item.innerHTML = `
            <div class="dropdown">
                <svg style="position: absolute; right: 0; height:24px; width=24px;" class="dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false"
                    xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-three-dots-vertical" viewBox="0 0 16 16">
                    <path d="M9.5 13a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m0-5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>
                </svg>    
                <ul class="dropdown-menu">
                    <li><a onclick="eliminarArchivo(${file.id})" class="dropdown-item" href="#">Eliminar mwejkwej</a></li>                    
                </ul>
            </div>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V9L13 2Z" stroke="#5f6368" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M13 2V9H20" stroke="#5f6368" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p>${file.nombre_archivo}</p>
        `;
        gridViewContent.appendChild(item);
    });
}

function switchToGridView() {
    gridViewContent.classList.remove('hidden');
    listViewContent.classList.add('hidden');
    gridViewButton.classList.add('active');
    listViewButton.classList.remove('active');
}

function switchToListView() {
    gridViewContent.classList.add('hidden');
    listViewContent.classList.remove('hidden');
    gridViewButton.classList.remove('active');
    listViewButton.classList.add('active');
}

gridViewButton.addEventListener('click', switchToGridView);
listViewButton.addEventListener('click', switchToListView);

// Inicializar la vista
switchToListView(); // Comenzar con la vista de lista por defecto


const crearArchivosFetch = async (archivo) => {
    try {
        const respuesta = await fetch("http://127.0.0.1:8000/projects/archivos/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(archivo),
        });

        // Verificar si la respuesta es exitosa
        if (!respuesta.ok) {
            console.log('Problema en la solicitud');
            return;
        }

        // Convertir la respuesta a JSON una sola vez
        const archivoCreado = await respuesta.json();
        console.log(archivoCreado);

    } catch (error) {
        console.log("Error al enviar el archivo:", error);
    }
};

document.getElementById("formArchivo").addEventListener("submit", subirArchivo);

async function subirArchivo(event) {
    event.preventDefault();

    const xd = document.getElementById("formArchivo");
    const datos = new FormData(xd);
    datos.append("id_usuario", "1");
    datos.append("id_carpeta", "1");
    const repollitoLindo = Object.fromEntries(datos.entries());

    const hoy = new Date();
    const año = hoy.getFullYear();
    const mes = String(hoy.getMonth() + 1).padStart(2, '0');
    const dia = String(hoy.getDate()).padStart(2, '0');
    const formatoPersonalizado = `${año}-${mes}-${dia}`;

    repollitoLindo.archivo = null;
    repollitoLindo.fecha_guardado = formatoPersonalizado;

    console.log(repollitoLindo);
    console.log(JSON.stringify(repollitoLindo));
    await crearArchivosFetch(repollitoLindo);
}

const ObtenerArchivosFetch = async () => {

    const respuesta = await fetch("http://127.0.0.1:8000/projects/archivos/", {
        method: 'GET',
        headers: {
            'Content-type': 'application/json'
        }
    });

    archivos = await respuesta.json();
    console.log("archivos obtenidos", archivos)
    renderListView();
    renderGridView();

};

ObtenerArchivosFetch();

const EliminarArchivosFetch = async (id) => {

    const respuesta = await fetch(`http://127.0.0.1:8000/projects/archivos/${id}/`, {
        method: 'DELETE',
        headers: {
            'Content-type': 'application/json'
        }
    });

    archivos = await respuesta.json();
    console.log("archivo eliminado", archivos)
    ObtenerArchivosFetch();
};

function eliminarArchivo(id) {
    EliminarArchivosFetch(id);
}