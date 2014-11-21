import zipfile
import glob, os

class DDZip:
    """Handles all zip operations"""
    
    def write_zip(self, filepath, path, remove_source=False):
        # open the zip file for writing, and write stuff to it
        file = zipfile.ZipFile(path, "w")
        
        for name in glob.glob(filepath):
            file.write(name, os.path.basename(name), zipfile.ZIP_DEFLATED)

        file.close()
        if remove_source:
            print 'Removing sources.'
            self.remove_sources(filepath)
            
    def print_zip(self, filepath):
        
        file = zipfile.ZipFile(filepath, "r")
        for info in file.infolist():
            print info.filename, info.date_time, info.file_size, info.compress_size
            
    def remove_sources(self, path):
        i = path.find("/*")
        if i > -1:
            path = path[:i]
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception, e:
                print e    
            
    
