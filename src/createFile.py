#Se importan las librerías que se van a utilizar 
#https://docs.python.org/2/library/os.html
import os
#https://docs.python.org/3/library/shutil.html
import shutil

data_folder = "DATABASES/"


class createFile():

    # crea el folder / los folders en la direccion que se especifica 
    def create_folder(self, path):
        try:
            if not os.path.exists(path):
                os.makedirs(data_folder + path)
        except OSError:
            print('ERROR: NO SE HA PODIDO CREAR EL DIRECTORIO. ' + path)

    # Crea archivos de texto que almacenaran los datos que se están 
    # especificando
    def createWrite_file(self, path, content):
        file = open(data_folder + path, "w")
        file.write(content)
        file.close()
        return True

    # crea una lista de los objetos que se encuentran dentro de la direccion especificiada 
    def list_files(self, path=""):
        files = []
        for name in os.listdir(data_folder + path):
            files.append(name)

        return (files)

    # Agrega datos en el archivo que se esta especificando (direccion)
    def append_file(self, path, content):
        file = open(data_folder + path, "a+")
        file.write(content)
        file.close()

    # Lee los datos que se le estan especificando en el path 
    def read_file(self, path):
        file = open(data_folder + path, "r")
        return file.read()

    # Eliminar archivos 
    def remove_folder(self, path):

        if os.path.exists(data_folder + path):
            shutil.rmtree(data_folder + path)
            return True
        return False

    #Re nombra a los folders que se le han seleccionado
    def rename_file(self, path, newPath):
        if os.path.exists(data_folder + path):
            os.rename(data_folder + path, data_folder + newPath)
            return True
        return False

    #Re nombra a los folders que se le han especificado
    def rename_files(self, folder_path, path, old_name, new_name):
        for name in  os.listdir(data_folder + path):
           indexType = name.index('.')
           os.rename(data_folder + path + name, data_folder + path + new_name+name[indexType:])
        for folder in os.listdir(data_folder + folder_path):
            print (new_name)
            if (folder == old_name):
                os.rename(data_folder + folder_path + folder, data_folder + folder_path + new_name)