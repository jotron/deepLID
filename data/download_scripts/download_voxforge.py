# HTTP
import requests
# Regular expressions
import re
# Command-line arguments
import argparse
# File operations
import os
# unzip
import tarfile

# https://docs.python.org/2/howto/regex.html
# https://www.codementor.io/aviaryan/downloading-files-from-urls-in-python-77q3bs0un
# https://docs.python.org/2/library/argparse.html#module-argparse
# https://stackoverflow.com/questions/273192/how-can-i-create-a-directory-if-it-does-not-exist
# https://stackoverflow.com/questions/5598181/python-multiple-prints-on-the-same-line
# https://docs.python.org/3/library/tarfile.html
# https://stackoverflow.com/questions/2632205/how-to-count-the-number-of-files-in-a-directory-using-python

# argument parser
parser = argparse.ArgumentParser(description='Download raw files from Voxforge')
parser.add_argument('language', type=str, choices=['french', 'english', 'german'],
                    help='The language of of the files to download')
args = parser.parse_args()


# urls on Voxforge
language_urls = {'french': 'http://www.repository.voxforge1.org/downloads/fr/Trunk/Audio/Main/16kHz_16bit/',
                 'english': 'http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit/',
                 'german': 'http://www.repository.voxforge1.org/downloads/de/Trunk/Audio/Main/16kHz_16bit/'}

# filename scraping with regex
    # (?<=<a href=") :lookbehind assertion
    # .+tgz :any string with ending tgz
    # (?=">) :lookahead assertion
regex = '(?<=<a href=").+tgz(?=">)'


# helper function to unpack only .wav files
def wav_files(members, source_name):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".wav":
            tarinfo.name = source_name + '-' + os.path.basename(tarinfo.name)
            yield tarinfo


# unpack tgz archives
def process(archive, lang):
    source_name = 'n' + os.path.splitext(os.path.basename(archive))[0]
    tar = tarfile.open(archive, 'r:gz')
    tar.extractall(lang, members=wav_files(tar, source_name))
    tar.close()
    os.remove(archive)


# download with requests
def download(lang):

    # folder for languange if not existent
    if not os.path.exists(lang):
        os.makedirs(lang)
    # Temporary folder if not existent
    if not os.path.exists('tmp'):
        os.makedirs('tmp')

    # get filenames
    site_url = language_urls[lang]
    site = requests.get(site_url).text  # returns html string
    file_names = re.findall(regex, site)  # returns array
    num_files = len(file_names)  # returns number of files

    for i, filename in enumerate(file_names):

        # print progress
        print(f"Processing Archive: {i} / {num_files}", end="", flush=True)
        print('\r', end='')

        # download file
        file_url = site_url + filename
        file_r = requests.get(file_url)

        # save file
        file_path = 'tmp/' + filename
        open(file_path, 'wb').write(file_r.content)

        # Unpack file
        process(file_path, lang)

    # clean tmp folder
    os.rmdir('tmp')

    # print summary
    num_wavs = len([name for name in os.listdir(lang) if os.path.isfile(name)])
    print(f"Processed indivual audio files: {num_wavs}")


# execute function with argument
download(args.language)
