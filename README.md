# Servicio de envíos automáticos de correo

Proyecto minimalista para enviar correos automáticamente cada cierto intervalo.

Requisitos
- Python 3.7+

Dependencias opcionales
- Si quieres cargar variables desde un archivo `.env`, instala las dependencias:

```powershell
pip install -r requirements.txt
```

Nota: el proyecto funciona sin `python-dotenv` si exportas las variables en el shell.

Configuración
1. Copia `.env.example` a `.env` o exporta las variables en PowerShell:

```powershell
# ejemplo: establecer variables temporales en PowerShell
$env:SMTP_HOST = "smtp.gmail.com"
$env:SMTP_PORT = "587"
$env:SMTP_USER = "tu_usuario@gmail.com"
$env:SMTP_PASSWORD = "tu_app_password"
$env:FROM_EMAIL = "tu_usuario@gmail.com"
$env:TO_EMAIL = "destino@example.com"
$env:INTERVAL_SECONDS = "3600"
```

Nota sobre Gmail: requiere usar App Passwords si tienes verificación en dos pasos.

Uso
1. Ejecuta en PowerShell (desde la carpeta del proyecto):

```powershell
python hola.py
```

El script se mantendrá en ejecución y enviará un correo cada INTERVAL_SECONDS.

Ejecución de tests
Se incluye un test unitario mínimo. Ejecutar:

```powershell
python -m unittest discover -v
```

Seguridad
- No subas credenciales a repositorios públicos.
- Considera usar un vault o variables de entorno administradas en producción.

Mejoras sugeridas
- Añadir reintentos exponenciales en fallos de red.
- Persistir logs (archivo) y añadir rotación de logs.
- Integrar notificaciones de fallo (Slack, etc.)
# test_script