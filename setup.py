from setuptools import setup

setup(name='congressapi',
      version='0.4',
      description='Wrapper for ProPublica Congress API',
      url='http://github.com/kjchavez/congressapi',
      author='Kevin Chavez',
      author_email='kevin.j.chavez@gmail.com',
      license='MIT',
      install_requirements = [
          "requests"
      ],
      packages=['congressapi'],
      zip_safe=False)
