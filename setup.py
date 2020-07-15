from setuptools import setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        README = f.read()
    return README


setup(
      name='uma',
      version='1.0',
      description='A python package to collect pyomo results as pandas dataframe for easier access.',
      long_description=readme(),
      long_description_content_type="text/markdown",
      url='https://github.com/dgusain1/uma',
      author='Digvijay Gusain',
      author_email='digvijay.gusain29@gmail.com',
      license='MIT',
      classifiers=[
              'License :: OSI Approved :: MIT License',
              'Programming Language :: Python :: 3.6',
              'Programming Language :: Python :: 3.7',
              'Programming Language :: Python :: 3.8'],
      packages=['uma'],
      include_package_data=True,
      install_requires=['numpy', 'pandas', 'pyomo']     
      )
