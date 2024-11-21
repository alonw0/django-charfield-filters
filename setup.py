from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="django-charfield-filters",
    version="0.1.0",
    author="Alon Wolenitz",
    author_email="alonsukasa@gmail.com",
    description="Django admin filters for CharFields with select and autocomplete functionality",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alonw0/django-charfield-filters",
    project_urls={
        "Bug Tracker": "https://github.com/alonw0/django-charfield-filters/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 5.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    package_dir={"": "."},
    packages=find_packages(where="."),
    python_requires=">=3.8",
    install_requires=[
        "Django>=4.2.0",
    ],
    include_package_data=True,
    zip_safe=False,
)
