"""
    Infraestructuras Paralelas y Distribuidas - 750023C 01
    Parcial I - Parte práctica

    Autores:
    Samuel Galindo Cuevas - 2177491
    Nicolás Herrera Marulanda - 2182551
    Christian David Vargas Gutiérrez - 2179172

    Profesor:
    John Sanabria PhD

    Archivo: multithreading_module.py
"""

import multiprocessing
import timeit
from datetime import datetime
from modules.reader import Reader
from modules.script import script


class MultiprocessingModule:
    def __init__(self, videos_to_download, number_of_processes, output_dir_path):
        self.videos_to_download = videos_to_download
        self.total_videos = len(videos_to_download)

        self.number_of_processes = number_of_processes
        self.processes = []

        self.output_dir_path = output_dir_path

    @staticmethod
    def process_loop(process_id, total_videos, number_of_processes, videos_to_download, output_dir_path, video_info):
        """
        Le asigna a cada proceso un rango de vídeos a procesar.
        Utiliza la función script que define el bloque de tareas a realizar por cada proceso
        (descargar el vídeo, extraer el audio y eliminar el archivo mp4).
        A diferencia de la función utilizada en la implementación con hilos, esta función no puede utilizar los atributos
        de la clase (self) ya que multiprocessing.process requiere que los argumentos sean completamente serializables.
        """
        for i in range(process_id, total_videos, number_of_processes):
            script(i, videos_to_download, output_dir_path, video_info)

    def start(self):
        """
        Inicializa cada proceso, lo guarda en una lista de procesos y espera a que todos los procesos terminen su ejecución.
        Finalmente imprime la información de los vídeos en un archivo JSON.
        """
        self.output_dir_path += f"/audio_extraction_at_{datetime.now().strftime('%d-%m-%Y__%H_%M_%S')}"

        initial_time = timeit.default_timer()

        # Como los procesos no comparten memoria, se debe utilizar un objeto de tipo Manager para compartir información.
        with multiprocessing.Manager() as manager:

            # Particularmente los procesos comparten la lista de diccionarios video_info, donde se almacena la información
            # de cada vídeo procesado.
            self.video_info = manager.list(
                [_ for _ in range(self.total_videos)])

            for i in range(self.number_of_processes):
                process = multiprocessing.Process(target=self.process_loop,
                                                  args=(i, self.total_videos, self.number_of_processes,
                                                        self.videos_to_download, self.output_dir_path, self.video_info))
                process.start()
                self.processes.append(process)

            for process in self.processes:
                process.join()

            total_time = timeit.default_timer() - initial_time

            # video_info inicialmente se definió como una lista multiproceso, por lo que se convierte a una lista normal
            # para poder ser serializada a un archivo JSON.
            self.video_info = list(self.video_info)
            Reader.fix_and_save_json(self.output_dir_path, self.video_info)

            print(
                f"Audio extraction with {self.number_of_processes} processes "
                f"completed in {format(total_time, '.2f')} seconds / "
                f"{format(total_time/60, '.2f')} minutes")
