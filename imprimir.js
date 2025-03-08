
    function cargarNoticias() {
        fetch('/imprimir')
            .then(response => response.json())
            .then(data => {
                // Obtener el contenedor donde se mostrarán las noticias
                const contenedorNoticias = document.querySelector('.row.align-items-lg-stretch.bg-secondary');

                // Limpiar el contenedor antes de añadir las nuevas noticias
                contenedorNoticias.innerHTML = '';

                // Iterar sobre los datos de las noticias y crear elementos HTML para cada una
                data.forEach(noticia => {
                    const divCol = document.createElement('div');
                    divCol.classList.add('col-lg-12', 'mb-5', 'mt-5');

                    const divCardBody = document.createElement('div');
                    divCardBody.classList.add('card-body', 'p-3', 'text-white', 'bg-dark');

                    divCardBody.innerHTML = `
                        <div class="embed-responsive embed-responsive-16by9">
                            <img src="${noticia.imagen}" class="card-img-top p-3 rounded-5" alt="aswdasdasd">
                        </div>
                        <h2 class="card-title mt-2 p-2">${noticia.titulo}</h2>
                        <p class="card-text mt-3 p-3" style="height: 10rem; overflow: hidden; text-overflow: ellipsis;">
                            ${noticia.parrafo}
                        </p>
                        <button type="button" class="btn btn-outline-light mt-5 mx-auto d-block w-100" data-bs-toggle="modal"
                            data-bs-target="#articuloModal${noticia.id}">Leer Más</button>
                    `;

                    divCol.appendChild(divCardBody);
                    contenedorNoticias.appendChild(divCol);

                    // Crear el modal para cada noticia
                    const divModal = document.createElement('div');
                    divModal.classList.add('modal', 'fade');
                    divModal.id = `articuloModal${noticia.id}`;
                    divModal.tabIndex = -1;
                    divModal.setAttribute('aria-labelledby', `articuloModalLabel${noticia.id}`);
                    divModal.setAttribute('aria-hidden', 'true');

                    divModal.innerHTML = `
                        <div class="modal-dialog modal-lg">
                            <div class="modal-content bg-secondary text-white">
                                <div class="modal-header">
                                    <h5 class="modal-title" id="articuloModalLabel${noticia.id}">${noticia.titulo}</h5>
                                    <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
                                </div>
                                <div class="modal-body">
                                    <img src="${noticia.imagen}" class="img-fluid mb-3" alt="Imagen del artículo">
                                    <p style="text-align: justify;">${noticia.parrafo}</p>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-outline-light" data-bs-dismiss="modal">Cerrar</button>
                                </div>
                            </div>
                        </div>
                    `;

                    contenedorNoticias.appendChild(divModal);
                });
            })
            .catch(error => console.error('Error al cargar las noticias:', error));
    }

    // Cargar las noticias al cargar la página
    cargarNoticias();
