document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('loginForm');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const usuario = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
           body: JSON.stringify({ usuario: usuario, contra: password })

        })
        .then(function (respuesta) {
            return respuesta.json();
        })
        .then(function (datos) {
            if (datos.success) {
                 Swal.fire({
                    icon: 'success',
                    title: 'Bienvenido ' + datos.usuario,
                    showConfirmButton: true,
                    timer: 2000
                }).then(() => {
                window.location.href = '/index';
                });

            } else {
                Swal.fire({
                icon: 'error',
                title: 'Error de inicio de sesión',
                text: datos.message,
                confirmButtonText: 'Intentar de nuevo'
        });
            }
        })
        .catch(function (error) {
           Swal.fire({
            icon: 'error',
            title: 'Error de conexión',
            text: 'Ocurrió un error al intentar iniciar sesión.',
            confirmButtonText: 'Cerrar'
        });
    });
});
});

/*
        Swal.fire({
          icon: 'success',
          title: 'Bienvenido ' + datos.usuario,
          showConfirmButton: false,
          timer: 2000
        }).then(() => {
          window.location.href = '/index';
        });
      } else {
        Swal.fire({
          icon: 'error',
          title: 'Error de inicio de sesión',
          text: datos.message,
          confirmButtonText: 'Intentar de nuevo'
        });
      }
    } catch (error) {
      console.error('Error en la solicitud:', error);
      Swal.fire({
        icon: 'error',
        title: 'Error de conexión',
        text: 'Ocurrió un error al intentar iniciar sesión.',
        confirmButtonText: 'Cerrar'

        */

        