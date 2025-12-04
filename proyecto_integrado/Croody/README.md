# Croody.app

Landing y tienda Buddy diseñadas con la biblia de geometría sagrada (negro + verde) e implementadas en Django.

## Requisitos previos

- Python 3.11+ (probado con 3.12)
  - **Linux**: disponible en la mayoría de distribuciones; en Debian/Ubuntu instala `python3` y `python3-venv`.
  - **macOS**: instala desde [python.org](https://www.python.org/downloads/mac-osx/) o con Homebrew (`brew install python@3.11`).
  - **Windows**: instala el launcher desde [python.org](https://www.python.org/downloads/windows/) y selecciona “Add python.exe to PATH”.

## Puesta en marcha

### Linux / macOS

```bash
# 1. Crear y activar entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar dependencias
pip install django

# 3. Aplicar migraciones (incluye productos Buddy semilla)
python manage.py migrate

# 4. Ejecutar el servidor de desarrollo
python manage.py runserver
```

### Windows (PowerShell)

```powershell
# 1. Crear y activar entorno virtual
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install django

# 3. Aplicar migraciones (incluye productos Buddy semilla)
python manage.py migrate

# 4. Ejecutar el servidor de desarrollo
python manage.py runserver
```

### Probar en el navegador

Visita `http://127.0.0.1:8000/` para revisar la landing (tema claro/oscuro, tienda Buddy y búsqueda).

### HTTPS local opcional

1. Instala la dependencia una vez: `pip install django-sslserver`.
2. Ejecuta `python manage.py runhttps` (si estás dentro de la carpeta `Croody`) o `python Croody/manage.py runhttps` (si estás en la raíz del repo).
3. Abre `https://127.0.0.1:8443/` y acepta el certificado autofirmado cuando el navegador lo pida. La primera vez se copiará el certificado de ejemplo de django-sslserver en `ssl/`.
- Compatibilidad: el comando parchea automáticamente `django-sslserver` para Python 3.13+, donde la librería sigue usando la API obsoleta `ssl.wrap_socket`.

## Notas

- Si `python3 -m venv` falla por ausencia de `ensurepip`, instala `python3-venv` y repite el paso 1.
- En Windows, si la activación del entorno virtual está bloqueada, ejecuta `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` y vuelve a lanzar `.\.venv\Scripts\Activate.ps1`.
- Los assets estáticos (tokens, CSS, JS) ya están en `static/` y se sirven con `runserver`. Para producción, usa `collectstatic`.
- Los productos Buddy iniciales se crean vía migración (`shop.0002_seed_products`). Edita/añade desde `/admin/` si lo necesitas.
- El comando `python manage.py runhttps --address 0.0.0.0:8443` permite exponer el servidor seguro en otro host/puerto si lo requieres.
- Si aparece el error “Falta django-sslserver”, instala la dependencia y vuelve a intentar.
