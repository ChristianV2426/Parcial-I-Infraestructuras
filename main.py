"""
    Infraestructuras Paralelas y Distribuidas - 750023C 01
    Parcial I - Parte práctica

    Autores: 
    Samuel Galindo Cuevas - 2177491
    Nicolás Herrera Marulanda - 2182551
    Christian David Vargas Gutiérrez - 2179172

    Profesor:
    John Sanabria PhD

    Archivo: main.py
"""

import sys
import os
from modules.reader import Reader
from modules.single_thread_module import SingleThreadModule
from modules.multithreading_module import MultithreadingModule
from modules.multiprocessing_module import MultiprocessingModule


def main():
    """
    Define el controlador principal del programa.
    Verifica que los argumentos de entrada sean correctos, llama a la clase Reader para leer el archivo de entrada y
    ejecuta el módulo correspondiente al modo de ejecución seleccionado.
    """
    reader = Reader()

    if len(sys.argv) != 3 and len(sys.argv) != 5:
        print(
            "Correct usage: "
            "python main.py "
            "<input_file_path> "
            "<output_dir_path> "
            "optional: "
            "<execution_mode> "
            "<number_of_threads or number_of_processes>)")
        return

    input_file_path = sys.argv[1]
    output_dir_path = sys.argv[2]

    if not input_file_path.endswith(".txt"):
        print("Input file must be a .txt file")
        return

    if not os.path.exists(output_dir_path):
        print("Output directory does not exist")
        return

    videos_to_download = reader.read_input(input_file_path)

    # Ejecución de un solo hilo
    if len(sys.argv) == 3:
        single_thread_module = SingleThreadModule(
            videos_to_download, output_dir_path)
        return single_thread_module.start()

    # Ejecución con múltiples hilos o múltiples procesos
    execution_mode = sys.argv[3]
    execution_mode.lower()
    n = sys.argv[4]

    if (
            execution_mode != "-threads"
            and execution_mode != "-t"
            and execution_mode != "-processes"
            and execution_mode != "-p"):
        print("Invalid execution mode. Choose between '-threads' or '-t' or '-processes' or '-p'")
        return

    if not n.isdigit():
        print("Last argument must be a number that indicates the number of threads or processes")
        return

    n = int(n)

    if execution_mode == "-threads" or execution_mode == "-t":
        multithreading_module = MultithreadingModule(
            videos_to_download, n, output_dir_path)
        return multithreading_module.start()

    elif execution_mode == "-processes" or execution_mode == "-p":
        multiprocessing_module = MultiprocessingModule(
            videos_to_download, n, output_dir_path)
        return multiprocessing_module.start()


if __name__ == "__main__":
    main()
