from setuptools import setup, find_packages

setup(name='digitalpy',
      version='0.2.0',
      description="A python implementation of the aphrodite's framework",
      author='Natha Paquette',
      author_email='natha.paquette@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      requires=[
            "rule-engine"
            ],
      package_dir={"": "src"},
      packages=find_packages(exclude=['tests', 'emergency_RI*']),
     )