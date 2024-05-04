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

import threading
import timeit
from datetime import datetime
from modules.reader import Reader
from modules.script import script


class MultithreadingModule:
    def __init__(self, videos_to_download, number_of_threads, output_dir_path):
        self.videos_to_download = videos_to_download
        self.total_videos = len(videos_to_download)

        self.number_of_threads = number_of_threads
        self.threads = []

        self.output_dir_path = output_dir_path
        self.video_info = [_ for _ in range(self.total_videos)]

    def thread_loop(self, thread_id):
        """
        Le asigna a cada hilo un rango de vídeos a procesar.
        Utiliza la función script que define el bloque de tareas a realizar por cada hilo
        (descargar el vídeo, extraer el audio y eliminar el archivo mp4).
        """
        for i in range(thread_id, self.total_videos, self.number_of_threads):
            script(i, self.videos_to_download,
                   self.output_dir_path, self.video_info)

    def start(self):
        """
        Inicializa cada hilo, lo guarda en una lista de hilos y espera a que todos los hilos terminen su ejecución.
        Finalmente imprime la información de los vídeos en un archivo JSON.
        """
        self.output_dir_path += f"/audio_extraction_at_{datetime.now().strftime('%d-%m-%Y__%H_%M_%S')}"

        initial_time = timeit.default_timer()

        for i in range(self.number_of_threads):
            thread = threading.Thread(target=self.thread_loop, args=(i,))
            thread.start()
            self.threads.append(thread)

        for thread in self.threads:
            thread.join()

        total_time = timeit.default_timer() - initial_time

        Reader.fix_and_save_json(self.output_dir_path, self.video_info)

        print(
            f"Audio extraction with {self.number_of_threads} threads "
            f"completed in {format(total_time, '.2f')} seconds / "
            f"{format(total_time/60, '.2f')} minutes")
