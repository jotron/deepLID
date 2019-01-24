# Used for HTTP requests
import requests
# Used for Regular expressions
import re
# Used to parse Command-line arguments
import argparse
# Used to execute file system operations
import os
# Used to unzip files
import tarfile

# Important sources:
# https://docs.python.org/2/howto/regex.html
# https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
# https://docs.python.org/2/library/argparse.html#module-argparse
# https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
# https://stackoverflow.com/questions/5598181/python-multiple-prints-on-the-same-line
# https://docs.python.org/3/library/tarfile.html
# https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python

# Parse Arguments
parser = argparse.ArgumentParser(description='Download raw files from Voxforge')
# Argument = language to download
parser.add_argument('language', type=str, choices=['french', 'english', 'german'],
                    help='The language of of the files to download')
args = parser.parse_args()


# Urls to the Voxforge API
language_urls = {'french': 'http://www.repository.voxforge1.org/downloads/fr/Trunk/Audio/Main/16kHz_16bit/',
                 'english': 'http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/',
                 'german': 'http://www.repository.voxforge1.org/downloads/de/Trunk/Audio/Main/16kHz_16bit/'}

# Filename scraping with regex
    # (?<=<a href=") = The string appears after the start of a link
    # .+tgz = The string ends with tgz
    # (?=">) = The string appears before the closure of the link
regex = '(?<=<a href=").+tgz(?=">)'


# Helper function to unpack only .wav files
def wav_files(members, source_name):
    # For all files in archive
    for tarinfo in members:
        # If ending is .wav
        if os.path.splitext(tarinfo.name)[1] == ".wav":
            # unpack to SOURCEX-FILENAMEX
            tarinfo.name = source_name + '-' + os.path.basename(tarinfo.name)
            yield tarinfo


# Unpack tgz archives
def process(archive, lang):
    # Remember Source of Files (needed for name to save as later)
    source_name = 'n' + os.path.splitext(os.path.basename(archive))[0]
    # Open for reading with gzip compression
    tar = tarfile.open(archive, 'r:gz')
    # extract to directory=lang
    tar.extractall(lang, members=wav_files(tar, source_name))
    # close and delte archive
    tar.close()
    os.remove(archive)


# Download Data from Voxforge with requests
def download(lang):

    # Create folder for languange if not existent
    if not os.path.exists(lang):
        os.makedirs(lang)
    # Create Temporary folder to save archives if not existent
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # Voxforge API URL for lang
    site_url = language_urls[lang]
    # Get HTML string of URL Website
    site = requests.get(site_url).text
    # Get Array with filenames found in String
    file_names = re.findall(regex, site)
    # Count number of files found
    num_files = len(file_names)

    # Process all archives
    for i, filename in enumerate(file_names):

        # Print progress
        print(f"Processing Archive: {i} / {num_files}", end="", flush=True)
        print('\r', end='')

        # Download specific file (url is combination of site with file)
        file_url = site_url + filename
        file_r = requests.get(file_url)

        # Save File in TMP
        file_path = 'tmp/' + filename
        open(file_path, 'wb').write(file_r.content)

        # Unpack Archive
        process(file_path, lang)

    # Clean tmp folder
    os.rmdir('tmp')

    # Print summary = number of total wav files extracted
    num_wavs = len([name for name in os.listdir(lang) if os.path.isfile(name)])
    print(f"Processed indivual audio files: {num_wavs}")


# Execute function with parsed argument
download(args.language)
