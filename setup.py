import setuptools

setuptools.setup(
    name = "cltemwf",
    author = "Arkadiy Davydov",
    version = '0.0.3',
    author_email="arkadiy.davydov@warwick.ac.uk",
    description = "A wrapper for creating templated workflows for clTEM code",
    # Dependencies/Other modules required for your package to work
    install_requires=['deepdiff', 'argparse', 'pillow','numpy'],
    package_data={'': ['STEM_config.json', 'CTEM_config.json', 'CBED_config.json']},
    include_package_data=True,
    packages=setuptools.find_packages(),
    entry_points={
        'console_scripts': [
            'cltemwf_batch = cltemwf.batch:run_batch',
            'cltemwf_showtif = cltemwf.showtif:showtif',
            'cltemwf_converttif = cltemwf.converttif:converttif',
        ],
    },
    classifiers = [
        "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
    ],
)
