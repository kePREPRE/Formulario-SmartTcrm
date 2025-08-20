document.addEventListener("DOMContentLoaded", function () {
    const btnActualizar = document.getElementById("btnActualizarCliente");

    if (btnActualizar) {
        btnActualizar.addEventListener("click", async function (e) {
            e.preventDefault(); // evita que el form recargue la página

            // ⚡ capturar datos del formulario
            const datos = new FormData();
            datos.append("idCliente", document.getElementById("idCliente").value); // ✅ Lee del hidden
            datos.append("txtNombreCli", document.getElementById("txtNombreCli").value.trim());
            datos.append("txtCorreoCli", document.getElementById("txtCorreoCli").value.trim());
            datos.append("txtTelefonoCli", document.getElementById("txtTelefonoCli").value.trim());
            datos.append("txtDireccionCli", document.getElementById("txtDireccionCli").value.trim());
            datos.append("slcProvincias", document.getElementById("slcProvincias").value.trim());
            datos.append("fecha", document.getElementById("fecha").value.trim());

            try {
                let resp = await fetch("/actualizarCliente", {
                    method: "POST",
                    body: datos
                });

                if (resp.redirected) {
                    // ✅ si Flask redirige -> éxito
                    Swal.fire({
                        icon: "success",
                        title: "Cliente actualizado",
                        text: "El cliente se actualizó correctamente.",
                        confirmButtonText: "OK"
                    }).then(() => {
                        window.location.href = '/listaCliente';
                    });
                } else {
                    // ⚠️ si Flask devolvió errores de validación
                    let htmlError = await resp.text();
                    Swal.fire({
                        icon: "warning",
                        title: "Validación",
                        html: htmlError
                    });
                }
            } catch (error) {
                console.error("Error:", error);
                Swal.fire({
                    icon: "error",
                    title: "Error",
                    text: "No se pudo actualizar el cliente. Intente de nuevo."
                });
            }
        });
    }
});

