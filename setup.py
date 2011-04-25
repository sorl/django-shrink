from setuptools import setup, find_packages


setup(
    name='django-shrink',
    version='0.0.1',
    description='js compiler & css minifier with scss compatibility',
    long_description=open('README.rst').read(),
    author='Mikko Hellsing',
    author_email='mikko@aino.se',
    license='BSD',
    url='https://github.com/aino/django-shrink',
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires = [ 'pyScss' ],
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

