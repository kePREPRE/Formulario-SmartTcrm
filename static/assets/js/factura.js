document.addEventListener("DOMContentLoaded", () => {
    // Elementos del DOM
    const selectProd = document.getElementById("producto");
    const inputCant = document.getElementById("cantidad");
    const btnAgregar = document.getElementById("btnAgregar");
    const btnEliminarTodo = document.getElementById("btnEliminarTodo");
    const contenedorLista = document.getElementById("listaProductosAgregados");
    const subtotalEl = document.getElementById("subtotal");
    const totalImpEl = document.getElementById("totalImpuesto");
    const totalGenEl = document.getElementById("totalGeneral");
    const totalesDiv = document.getElementById("totalesLista");

    // Datos iniciales
    const detalleInicial = JSON.parse(document.getElementById("detalle-json").textContent || "[]");
    let detalleFactura = [];
    const impuestoPorc = 13;

    // Si hay datos iniciales (modo edición), los cargamos
    if (detalleInicial.length > 0) {
        detalleFactura = detalleInicial.map(d => ({
            id: d[0],
            nombre: d[1],
            cantidad: d[2],
            precio: parseFloat(d[3])
        }));
        renderLista();
    }

    // Agregar producto
    btnAgregar.addEventListener("click", e => {
        e.preventDefault();
        let id = selectProd.value;
        let nombre = selectProd.options[selectProd.selectedIndex].text;
        let precio = parseFloat(selectProd.options[selectProd.selectedIndex].dataset.precio || 0);
        let cantidad = parseInt(inputCant.value);

        if (!id) {
            Swal.fire("Producto requerido", "Seleccione un producto.", "warning");
            return;
        }
        if (cantidad <= 0) {
            Swal.fire("Cantidad inválida", "Ingrese una cantidad mayor que 0.", "warning");
            return;
        }

        detalleFactura.push({ id, nombre, precio, cantidad });
        renderLista();
    });

    // Eliminar todos los productos
    btnEliminarTodo.addEventListener("click", e => {
        e.preventDefault();
        detalleFactura = [];
        renderLista();
    });

    // Función para renderizar la lista
    function renderLista() {
        contenedorLista.innerHTML = "";
        let subtotal = 0;
        let totalImpuesto = 0;

        detalleFactura.forEach((item) => {
            let sub = item.cantidad * item.precio;
            let imp = sub * (impuestoPorc / 100);

            subtotal += sub;
            totalImpuesto += imp;

            let card = document.createElement("div");
            card.className = "producto-card";
            card.innerHTML = `
                <strong>${item.nombre}</strong>
                <small>Cantidad: ${item.cantidad}</small>
            `;
            contenedorLista.appendChild(card);
        });

        if (detalleFactura.length > 0) {
            subtotalEl.textContent = subtotal.toFixed(2);
            totalImpEl.textContent = totalImpuesto.toFixed(2);
            totalGenEl.textContent = (subtotal + totalImpuesto).toFixed(2);
            totalesDiv.style.display = "block";
            contenedorLista.appendChild(totalesDiv);
        } else {
            totalesDiv.style.display = "none";
        }
    }

    // Guardar factura
    document.getElementById("btnGuardarFactura").addEventListener("click", () => {
        const cliente_id = document.getElementById("cliente").value;
        const fecha = document.getElementById("fecha").value;

        if (!cliente_id) {
            Swal.fire("Cliente requerido", "Seleccione un cliente.", "warning");
            return;
        }
        if (!fecha) {
            Swal.fire("Fecha requerida", "Seleccione una fecha.", "warning");
            return;
        }
        if (detalleFactura.length === 0) {
            Swal.fire("Productos requeridos", "Agregue al menos un producto.", "warning");
            return;
        }

        fetch("/guardarFactura", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                cliente_id: cliente_id,
                fecha: fecha,
                total: parseFloat(totalGenEl.textContent) || 0,
                impuestos: parseFloat(totalImpEl.textContent) || 0
            })
        })
        .then(res => res.json())
        .then(data => {
            Swal.fire("Éxito", data.msg || "Factura guardada correctamente.", "success")
                .then(() => window.location.href = "listaF");
        })
        .catch(() => {
            Swal.fire("Error", "No se pudo guardar la factura.", "error");
        });
    });
});
