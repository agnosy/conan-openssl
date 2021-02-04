from conans import ConanFile, CMake, tools


class OpensslConan(ConanFile):
    name = "openssl"
    version = "1.0.2t.fips"
    license = "OpenSSL"
    author = "agnosy"
    url = "https://github.com/agnosy/conan-openssl"
    description = "A toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL) protocols"
    topics = ("conan", "openssl", "ssl", "tls", "encryption", "security")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    generators = "cmake"

    def source(self):
        tools.get("https://www.openssl.org/source/openssl-1.0.2t.tar.gz")

    def build(self):
        with tools.chdir(os.path.join(self.source_folder, 'openssl-1.0.2t')):
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                self.run(
                    "./config fips --with-fipsdir=%s" %
                    os.path.join(self.source_folder, 'openssl-fips-2.0.16')
                )
                self.run("make depend")
                self.run("make")

    def package(self):
        self.copy("*.h", dst="include", src="hello")
        self.copy("*hello.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["hello"]

