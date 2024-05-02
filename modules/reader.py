"""
    Infraestructuras Paralelas y Distribuidas - 750023C 01
    Parcial I - Parte práctica

    Autores: 
    Samuel Galindo Cuevas - 2177491
    Nicolás Herrera Marulanda - 2182551
    Christian David Vargas Gutiérrez - 2179172

    Profesor:
    John Sanabria PhD

    Archivo: reader.py
"""


import json
from datetime import datetime


class Reader:
    def __init__(self):
        pass

    def read_input(self, file_path):
        """
       Lee el archivo de entrada y retorna una lista de tuplas, donde cada tupla contiene la URL de un canal de YouTube
       y un número ordinal que indica la posición del vídeo (de más reciente a más antiguo) que se desea descargar de ese canal.
        """
        try:
            with open(file_path, 'r') as file:
                data = file.readlines()
                videos_to_download = []

                for line in data:
                    video_url = line.strip()
                    for ordinal in range(1, 6):
                        videos_to_download.append((video_url, ordinal))

                return videos_to_download

        except Exception as exception:
            print("Error reading input file.\n", exception)
            raise exception

    @staticmethod
    def sanitize_filename(filename):
        """
        Elimina caracteres potencialmente problemáticos en los nombres de archivo.
        """
        return "".join([c if c.isalnum() else "_" for c in filename])

    @staticmethod
    def fix_and_save_json(file_path, list_of_json):
        """
        Arregla el formato de la fecha de descarga epoch guardada en los objetos JSON (Originalmente en formato UNIX timestamp)
        y guarda la información de los vídeos en un archivo .json.
        """
        for json_info in list_of_json:
            json_info['upload_date'] = datetime.strptime(
                json_info['upload_date'], '%Y%m%d').strftime('%d-%m-%Y')

            json_info['epoch'] = datetime.fromtimestamp(
                json_info['epoch']).strftime('%d-%m-%Y %H:%M:%S')

        try:
            with open(f"{file_path}/info.json", 'w') as file:
                json.dump(list_of_json, file, indent=4)

        except Exception as exception:
            print("Error saving JSON file.\n", exception)
            raise exception
