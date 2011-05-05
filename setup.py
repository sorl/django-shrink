from setuptools import setup, find_packages


setup(
    name='django-shrink',
    version='0.0.2.1',
    description='js compiler & css minifier with sass compatibility',
    long_description=open('README.rst').read(),
    author='Mikko Hellsing',
    author_email='mikko@aino.se',
    license='BSD',
    url='https://github.com/aino/django-shrink',
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = [ 'pyScss==1.0.6' ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Framework :: Django',
    ],
)

