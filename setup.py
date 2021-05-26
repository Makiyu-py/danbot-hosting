from setuptools import setup


reqs = []
with open("requirements.txt") as f:
    reqs = f.read().splitlines()

with open("README.md", "r", encoding="UTF-8") as f:
    long_description = f.read()

github_url = 'https://github.com/Makiyu-py/danbot-hosting'

setup(
    name='danbot-hosting-py',
    version='0.2',
    description='A Python Wrapper for the DanBotHosting API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['danbot_api'],
    url=github_url,
    project_urls={
        "Issue tracker": github_url + "/issues"
    },
    license='MIT License',
    author='Makiyu',
    author_email='73825066+Makiyu-py@users.noreply.github.com',
    python_requires='>=3.6',
    install_requires=reqs,
    classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Natural Language :: English",
            "License :: OSI Approved :: MIT License",
            "Topic :: Internet",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: Utilities",
    ],
    keywords="DanBotHosting discord dbh"
)
