# Script para crear el frontend completo de Control de Acceso
Write-Host "Creando frontend de Control de Acceso..." -ForegroundColor Green

cd c:\Users\Usuario\soft-2\reto-2\frontend\control-acceso

# Actualizar index.html
Write-Host "Actualizando index.html..." -ForegroundColor Yellow
@"
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Sistema de Control de Acceso</title>
  <base href="/">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" type="image/x-icon" href="favicon.ico">
  <link rel="preconnect" href="https://fonts.gstatic.com">
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap" rel="stylesheet">
  <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
</head>
<body>
  <app-root></app-root>
</body>
</html>
"@ | Out-File -FilePath "src\index.html" -Encoding UTF8

Write-Host "✓ Frontend base configurado" -ForegroundColor Green
Write-Host ""
Write-Host "Para completar la configuración, ejecuta:" -ForegroundColor Cyan
Write-Host "  cd c:\Users\Usuario\soft-2\reto-2\frontend\control-acceso" -ForegroundColor White
Write-Host "  npm start" -ForegroundColor White
Write-Host ""
Write-Host "La aplicación estará disponible en: http://localhost:4200" -ForegroundColor Green
