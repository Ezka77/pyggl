from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()

requires = [
        'click',
        ]

setup(name='pyggl',
      version='0.1',
      description='Toggl CSV creator',
      long_description=README,
      author='Théo Vaquer',
      author_email='tvaquer@vegafrance.eu',
      url='',
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Private :: Do Not Upload",
        ],
      keywords='toggle csv useless',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      entry_points="""\
      [console_scripts]
      pyggl = pyggl:main
      """,
      )
