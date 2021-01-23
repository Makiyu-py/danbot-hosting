import setuptools

with open("README.md", "r", encoding="UTF-8") as f:
    long_description = f.read()

setuptools.setup(
    name='danbot-hosting-py',
    version='0.1a',
    description='A Python Wrapper for the DanBotHosting API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    url='https://github.com/Makiyu-py/danbot-hosting',
    license='MIT License',
    author='Makiyu',
    author_email='dankerdanker11@gmail.com',
    python_requires='>=3.6',
)
