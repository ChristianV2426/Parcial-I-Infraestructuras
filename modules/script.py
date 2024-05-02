"""
    Infraestructuras Paralelas y Distribuidas - 750023C 01
    Parcial I - Parte práctica

    Autores:
    Samuel Galindo Cuevas - 2177491
    Nicolás Herrera Marulanda - 2182551
    Christian David Vargas Gutiérrez - 2179172

    Profesor:
    John Sanabria PhD

    Archivo: script.py
"""

import os
import subprocess
import json
from modules.reader import Reader


def script(i, videos_to_download, output_dir_path, video_info):
    """
    Define el script que se ejecutará en cada hilo.
    Como primer paso, se descarga el vídeo en formato mp4 usando yt-dlp.
    Luego, se extrae el audio del vídeo y se guarda en formato m4a usando ffmpeg.
    Finalmente, se elimina el archivo mp4.
    """
    video_url = videos_to_download[i][0]
    cardinal = videos_to_download[i][1]

    download_command = (
        f"yt-dlp "
        f"--format mp4 "
        f"--playlist-items {cardinal} "
        f"-o \"{output_dir_path}/{i}.%(ext)s\" "
        f"-O \"%(.{{title,upload_date,epoch}})j\" "
        f"--no-simulate "
        f"\"{video_url}\"")

    downloading_result = subprocess.run(
        download_command, shell=True, capture_output=True, text=True)

    info = json.loads(downloading_result.stdout)

    # Limpia el nombre del archivo para evitarle problemas al sistema operativo más adelante al intentar buscar un archivo con un nombre no alcanzable.
    info['title'] = Reader.sanitize_filename(info['title'])
    title = info['title']
    os.rename(f"{output_dir_path}/{i}.mp4",
              f"{output_dir_path}/{title}.mp4")

    video_info[i] = info

    audio_extraction_command = (
        f"ffmpeg "
        f"-loglevel error "
        f"-i \"{output_dir_path}/{title}.mp4\" "
        f"-vn "
        f"-acodec copy "
        f"\"{output_dir_path}/{title}.m4a\"")
    subprocess.run(audio_extraction_command, shell=True)

    os.remove(f"{output_dir_path}/{title}.mp4")
