"""
YAML Configuration Loader
Utilidad para cargar y parsear archivos YAML de configuración
"""

import yaml
import os
from pathlib import Path
from django.conf import settings


class YAMLConfigLoader:
    """
    Clase para cargar configuraciones desde archivos YAML
    """

    def __init__(self, config_file_name):
        """
        Inicializa el loader con el nombre del archivo de configuración

        Args:
            config_file_name (str): Nombre del archivo YAML (ej: 'reglas_negocio.yaml')
        """
        self.config_file_name = config_file_name
        self.config_path = self._get_config_path()
        self._config_data = None

    def _get_config_path(self):
        """
        Obtiene la ruta completa del archivo de configuración

        Returns:
            Path: Ruta completa al archivo YAML
        """
        # Primero intenta encontrar el archivo en quotations/config/
        app_config_path = Path(__file__).resolve(
        ).parent.parent / 'config' / self.config_file_name

        if app_config_path.exists():
            return app_config_path

        # Si no existe, intenta en la raíz del proyecto
        base_dir = Path(settings.BASE_DIR)
        root_config_path = base_dir / self.config_file_name

        if root_config_path.exists():
            return root_config_path

        raise FileNotFoundError(
            f"No se encontró el archivo de configuración '{self.config_file_name}' "
            f"en {app_config_path} ni en {root_config_path}"
        )

    def load(self):
        """
        Carga el archivo YAML y retorna su contenido

        Returns:
            dict: Contenido del archivo YAML parseado
        """
        if self._config_data is None:
            try:
                with open(self.config_path, 'r', encoding='utf-8') as file:
                    self._config_data = yaml.safe_load(file)
            except yaml.YAMLError as e:
                raise ValueError(f"Error al parsear el archivo YAML: {e}")
            except Exception as e:
                raise Exception(
                    f"Error al cargar el archivo de configuración: {e}")

        return self._config_data

    def get(self, key, default=None):
        """
        Obtiene un valor específico de la configuración

        Args:
            key (str): Clave a buscar (soporta notación de punto para nested keys)
            default: Valor por defecto si no se encuentra la clave

        Returns:
            El valor encontrado o el default
        """
        config = self.load()

        # Soportar claves anidadas con notación de punto
        keys = key.split('.')
        value = config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def reload(self):
        """
        Recarga el archivo de configuración (útil si se modificó)
        """
        self._config_data = None
        return self.load()


def load_yaml_config(config_file_name):
    """
    Función de conveniencia para cargar un archivo YAML

    Args:
        config_file_name (str): Nombre del archivo YAML

    Returns:
        dict: Contenido del archivo YAML
    """
    loader = YAMLConfigLoader(config_file_name)
    return loader.load()
