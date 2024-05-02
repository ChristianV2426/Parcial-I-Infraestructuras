"""
    Infraestructuras Paralelas y Distribuidas - 750023C 01
    Parcial I - Parte práctica

    Autores:
    Samuel Galindo Cuevas - 2177491
    Nicolás Herrera Marulanda - 2182551
    Christian David Vargas Gutiérrez - 2179172

    Profesor:
    John Sanabria PhD

    Archivo: single_thread_module.py
"""
import timeit
from datetime import datetime
from modules.reader import Reader
from modules.script import script

class SingleThreadModule:
    def __init__(self, videos_to_download, output_dir_path):
        self.videos_to_download = videos_to_download
        self.total_videos = len(videos_to_download)

        self.output_dir_path = output_dir_path
        self.video_info = [_ for _ in range(self.total_videos)]

    def start(self):
        """
        Inicia la ejecución del script. En este caso, la ejecución es secuencial.
        Al final, imprime la información de los vídeos en un archivo JSON.
        """
        self.output_dir_path += f"/audio_extraction_at_{datetime.now().strftime('%d-%m-%Y__%H_%M_%S')}"

        initial_time = timeit.default_timer()

        for i in range(self.total_videos):
            script(i, self.videos_to_download,
                               self.output_dir_path, self.video_info)

        total_time = timeit.default_timer() - initial_time

        Reader.fix_and_save_json(self.output_dir_path, self.video_info)

        print(
            f"Audio extraction with a single thread, "
            f"completed in {format(total_time, '.2f')} seconds / "
            f"{format(total_time/60, '.2f')} minutes")