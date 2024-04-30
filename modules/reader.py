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


class Reader:
    def __init__(self):
        pass

    def read_input(self, file_path):
        """
        Documentación
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
