import setuptools

setuptools.setup(
    name = "PDF tool",
    version="1.0",
    author="Sameer",
    author_email="sam.parvez116@gmail.com",

    py_modules=['new-img-to-pdf'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8'
)

#shiv --site-packages dist --compressed -r requirements.txt -o pdftool.pyz -e new-img-to-pdf:main .