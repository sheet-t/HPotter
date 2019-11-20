from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='hpotter',
      version='0.0.4',
      author='Steve Beaty',
      author_email='drjsb80@gmail.com',
      url='https://github.com/sheet-t/HPotter',
      py_modules=["hpotter"],
      packages=find_packages(),
      data_files=[
        ('hpotter',
            ['hpotter/env.py',
             'hpotter/logging.conf',
             'hpotter/requirements.txt',
             'README.md'])],
      description='An easy to install, configure, and run honeypot',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
      ],
    python_requires='>=3.6',
    install_requires=['SQLAlchemy', 'SQLAlchemy-Utils', 'paramiko'],
    )
