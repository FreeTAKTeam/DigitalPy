from setuptools import setup, find_packages

setup(name='digitalpy',
      version='0.3.6',
      description="A python implementation of the aphrodite's specification, heavily based on WCMF",
      author='Natha Paquette',
      author_email='natha.paquette@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      install_requires=[
            "rule-engine",
            "pyzmq",
      ],
      extras_require={
            "DEV": ["pytest"],
      },
      package_data={'': ['*.ini', "*.conf", "*.json"]},
      packages=find_packages(include=["digitalpy", "digitalpy.*", "*.json", "*.ini", "*.conf"])
     )
