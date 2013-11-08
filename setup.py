from setuptools import setup

setup(
    name='hockeystreams',
    version='0.1',
    description='Python wrapper for the hockeystreams.com REST API',
    author='Charlie Meyer',
    author_email='charlie@charliemeyer.net',
    url='http://charliemeyer.net',
    packages=['hockeystreams'],
    long_description="""\
      hockeystreams is a wrapper around the hockeystreams.com REST API
      """,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet",
    ],
    keywords='hockey hockeystreams REST API',
    license='GPL',
    install_requires=[
        'setuptools',
    ],
)