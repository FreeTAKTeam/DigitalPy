from setuptools import setup, find_packages

setup(name='digitalpy',
      version='0.2.1.5',
      description="A python implementation of the aphrodite's framework",
      author='Natha Paquette',
      author_email='natha.paquette@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      install_requires=[
            "rule-engine"
            ],
      packages=find_packages(include=["digitalpy", "digitalpy.*"])
      #packages=["digitalpy"]
     )