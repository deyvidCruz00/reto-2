// Configuración de producción
export const environment = {
  production: true,
  apiUrl: 'http://localhost:8080',  // Cambiar por URL de producción
  endpoints: {
    login: '/login',
    employee: '/employee',
    access: '/access',
    alert: '/alert'
  }
};
