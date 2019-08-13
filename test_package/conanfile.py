from conans import ConanFile, CMake, tools


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake_paths"

    def test(self):
        if not tools.cross_building(self.settings):
            tools.save("testfile.info", "")
            self.run("lcov_cobertura testfile.info", run_environment=True)