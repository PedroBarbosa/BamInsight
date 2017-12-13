from setuptools import setup

setup(
    name = "BamInsight",        # what you want to call the archive/egg
    version = "0.1",
    packages=["Main", "Configs"],    # top-level python modules you can import like
                                #   'import foo'
    dependency_links = [],      # custom links to a specific project
    install_requires=[],
    extras_require={},      # optional features that other packages can require
                            #   like 'helloworld[foo]'
    package_data = {},
    author="Rui Luis",
    author_email = "ruisergioluis@gmail.com",
    description = "A Useful bioinformatic tool to quickly vizualize stranded BAM file of RNA-seq in Genome Browser UCSC",
    license = "BSD",
    keywords= "RNA-seq, STRANDED, Genome Bowser UCSC tool",
    url = "https://github.com/rluis/BamInsight",
    entry_points = {
        "console_scripts": [        # command-line executables to expose
            "baminsight = Main.system:system",
        ],
        "gui_scripts": []       # GUI executables (creates pyw on Windows)
    }
)
