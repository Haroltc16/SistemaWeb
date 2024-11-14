// Gráfico de Productos por Categoría
fetch('/datos_productos_por_categoria/')
    .then(response => response.json())
    .then(datos => {
        const categorias = datos.map(d => d.categoria__nombre);
        const totales = datos.map(d => d.total);

        // Cambia los colores aquí para el gráfico de pastel
        const coloresCategorias = [
            '#FF6384', // Rojo
            '#36A2EB', // Azul
            '#FFCE56', // Amarillo
            '#4BC0C0', // Verde
            '#9966FF', // Púrpura
            '#FF9F40' // Naranja
        ];

        const ctx = document.getElementById('graficoProductosPorCategoria').getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: categorias,
                datasets: [{
                    label: 'Cantidad de Productos',
                    data: totales,
                    backgroundColor: coloresCategorias,
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Permitir que el gráfico se ajuste al tamaño del contenedor
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return `${tooltipItem.label}: ${tooltipItem.raw} productos`;
                            }
                        }
                    }
                }
            }
        });
    });

// Gráfico de Cantidad de Productos por Almacén
fetch('/datos_inventario_por_almacen/')
    .then(response => response.json())
    .then(datos => {
        const almacenes = datos.map(d => d.almacen__nombre);
        const totales = datos.map(d => d.total);

        // Cambia los colores aquí para el gráfico de barras
        const coloresAlmacenes = [
            '#36A2EB', // Azul
            '#FF6384', // Rojo
            '#FFCE56', // Amarillo
            '#4BC0C0', // Verde
            '#9966FF', // Púrpura
            '#FF9F40' // Naranja
        ];

        const ctx = document.getElementById('graficoInventarioPorAlmacen').getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: almacenes,
                datasets: [{
                    label: 'Cantidad de Productos',
                    data: totales,
                    backgroundColor: coloresAlmacenes,
                    borderColor: 'rgba(255, 255, 255, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false, // Permitir que el gráfico se ajuste al tamaño del contenedor
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: { position: 'top' },
                    tooltip: {
                        callbacks: {
                            label: function(tooltipItem) {
                                return `${tooltipItem.label}: ${tooltipItem.raw} unidades`;
                            }
                        }
                    }
                }
            }
        });
    });


document.addEventListener("DOMContentLoaded", function() {
    fetch('/obtener_ventas/')
        .then(response => response.json())
        .then(data => {
            const fechas = data.map(item => item.fecha_venta);
            const cantidades = data.map(item => item.cantidad);

            // Crear el gráfico de ventas
            const ctxVentas = document.getElementById('graficoVentas').getContext('2d');
            const graficoVentas = new Chart(ctxVentas, {
                type: 'bar', // Tipo de gráfico
                data: {
                    labels: fechas, // Etiquetas del eje X
                    datasets: [{
                        label: 'Cantidad de Ventas',
                        data: cantidades, // Datos del eje Y
                        backgroundColor: 'rgba(75, 192, 192, 0.6)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true // Iniciar el eje Y en cero
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error al obtener los datos:', error));
});