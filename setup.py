from setuptools import setup, find_packages

PLUGIN_ENTRY_POINT = 'google_translate_stt = ovos_stt_plugin_google_cloud_translate:GoogleTranslateSTTPlugin'

setup(
    name='ovos-stt-plugin-google-cloud-translate',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'ovos-core',
        'ovos-plugin-manager',
        'requests',
        'speechrecognition'
    ],
    entry_points={'mycroft.plugin.stt': [PLUGIN_ENTRY_POINT]},
    author='Mosi',
    author_email='zxcvbnm914121@pinklab.art',
    description='A Google Translate STT plugin for OVOS',
    license='Apache License 2.0',
    keywords='OVOS STT Google Translate',
    url='https://github.com/mosiwon/ovos-stt-plugin-google-cloud-translate',   # 프로젝트 URL 또는 GitHub URL
)
