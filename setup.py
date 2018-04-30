from setuptools import setup
from Configs import configs
setup(
    name = "BamInsight",        # what you want to call the archive/egg
    version = configs.Configs.ARG_BAMINSIGHT_VERSION,
    packages=["Main", "Configs"],    # top-level python modules you can import like
    dependency_links = [],      # custom links to a specific project

    install_requires=['pandas','pybedtools','pyBigWig', 'pysam', 'setuptools'],

    extras_require={},      # optional features that other packages can require
    package_data = {},
    author="Rui Luis",
    author_email = "ruisergioluis@gmail.com",
    description = "A Useful bioinformatic tool to quickly vizualize stranded BAM files in Genome Browser UCSC",
    license = "BSD",
    keywords= "NGSs, STRANDED, Genome Bowser UCSC",
    url = "https://github.com/rluis/BamInsight",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "baminsight = Main.system:system",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
