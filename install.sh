# Activar el entorno virtual
source /home/emiliano/Escritorio/ing_software/ing_software_project/ing_soft_env/bin/activate


# Verificar si el entorno virtual se activó correctamente
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Entorno virtual activado con éxito."
else
    echo "No se pudo activar el entorno virtual."
    exit 1
fi

# Instalar paquetes desde requirements.txt
pip3 install -r requirements.txt

