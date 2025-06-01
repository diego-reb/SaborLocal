
function cambiarEstado(btn) {
    const idCliente = btn.getAttribute('data-id'); // Obtiene el id del cliente
    console.log("Cambiar estado del cliente con id:", idCliente);
    // Aquí puedes agregar la lógica para cambiar el estado en el backend.
}

function eliminarFila(btn) {
    let id_cliente = btn.getAttribute('data-id');
    console.log("ID cliente:", id_cliente);

    console.log("ID a eliminar:", idCliente);  // Verifica si llega el ID

    if (confirm('¿Estás seguro de que quieres eliminar este cliente?')) {
        fetch(`/eliminar_cliente/${idCliente}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Eliminar la fila del DOM
                btn.closest('tr').remove();
                alert(data.message);
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar el cliente');
        });
    }
}


