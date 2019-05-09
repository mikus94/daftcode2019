from setuptools import setup
setup(
    name='notifiai',
    version='1.0',
    description='These are solutions for Daftcode/NotifyAI recruitment task.',
    author='Mikolaj Gagatek',
    author_email='mikolaj.gagatek@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'certifi==2019.3.9',
        'chardet==3.0.4',
        'Click==7.0',
        'Flask==1.0.2',
        'idna==2.8',
        'itsdangerous==1.1.0',
        'Jinja2==2.10.1',
        'MarkupSafe==1.1.1',
        'requests==2.21.0',
        'urllib3==1.24.3',
        'Werkzeug==0.15.2'
    ]
)
