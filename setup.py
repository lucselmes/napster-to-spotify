from setuptools import setup, find_packages

requires = [
    'flask==2.1.3',
    'spotipy',
    'requests',
    'numpy',
    'pandas',
    'redis',
    'urllib3',
    'urllib',
    'json',
    'os'
]

setup(
    name='toSpotifyPlaylistConverter',
    version='1.0',
    description='Application allowing you to convert playlists from other streaming services to Spotify',
    author='Luc Selmes',
    author_email='lselmes@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)