document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('toggle-password');
    const password = document.getElementById('password');
    const form = document.getElementById('login-form');

    togglePassword.addEventListener('click', function() {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.setAttribute('aria-label', type === 'password' ? 'Mostrar contraseña' : 'Ocultar contraseña');
    });

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        // Aquí iría la lógica de autenticación
        console.log('Iniciando sesión con:', email.value, password.value);
    });
});