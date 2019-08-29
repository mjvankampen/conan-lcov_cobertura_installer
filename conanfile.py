from conans import ConanFile
from conans import tools
import subprocess
import os
import codecs

class LcovCoberturaConan(ConanFile):
    name = "lcov_cobertura_installer"
    version = "1.6"
    url = "https://github.com/mjvk/conan-lcov_cobertura_installer"
    homepage = "https://github.com/eriwen/lcov-to-cobertura-xml"
    topics = ("coverage", "documentation", "doxygen")
    author = "mjvk <>"
    description = ("Lcov_cobertura can be used to generate cobertura files from lcov files")
    license = "MIT"
    settings = "os_build", "arch_build"
    _source_subfolder = "sourcefolder"
    
    def _makeAbsoluteImport(self,input_name):
        tmp_name = input_name + ".bak"
        with codecs.open(input_name, 'r', encoding='utf8') as fi, \
            codecs.open(tmp_name, 'w', encoding='utf8') as fo:

            for line in fi:
                fo.write(line.replace("from .", "from lcov_cobertura."))

        os.remove(input_name) # remove original
        os.rename(tmp_name, input_name) # rename temp to original name
                
    def source(self):
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version))
        os.rename("lcov-to-cobertura-xml-%s" % self.version, self._source_subfolder)
        
    def build(self):
        subprocess.call("pip install pyinstaller", shell=True)
        mainfilename = os.path.join(self._source_subfolder,"lcov_cobertura","lcov_cobertura.py")
        self._makeAbsoluteImport(mainfilename)
        self._makeAbsoluteImport(mainfilename)
        subprocess.call('pyinstaller %s --name lcov_cobertura --onefile --workpath %s --distpath %s --specpath %s' % (mainfilename, os.path.join(self.build_folder,"build"), os.path.join(self.build_folder,"bin"), self.build_folder), shell=True)

    def package(self):
        self.copy("*lcov_cobertura", dst="bin", src="bin", keep_path=False)
        self.copy("*lcov_cobertura.exe", dst="bin", src="bin", keep_path=False)

    def deploy(self):
        self.copy("*", src="bin", dst="bin")
        
    def package_id(self):
        self.info.include_build_settings()
    
    def package_info(self):
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        