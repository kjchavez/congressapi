from setuptools import setup

setup(name='congressapi',
      version='0.1',
      description='Wrapper for ProPublica Congress API',
      url='http://github.com/kjchavez/congressapi',
      author='Kevin Chavez',
      author_email='kevin.j.chavez@gmail.com',
      license='MIT',
      install_requirements = [
          "enum",
          "requests"
      ],
      packages=['congressapi'],
      zip_safe=False)
