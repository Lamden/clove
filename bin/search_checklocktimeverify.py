#!/usr/bin/env python3

import glob
import logging
import os
import subprocess
import time
from urllib.error import HTTPError, URLError
import urllib.request

import requests

from clove.utils.logging import logger

logger.setLevel(logging.INFO)


def get_github_api_token():
    return os.getenv('GITHUB_API_TOKEN')


def search_checklocktime(lines, index, filename):
    api_token = get_github_api_token()
    github_line_offset = next((i for i, line in enumerate(lines[index:]) if 'github.com' in line), None)
    github_line = lines[index + github_line_offset]

    search_link, repo_info_link, repo_zip_file = create_github_links(github_line)

    authorization_header = {'Authorization': f'token {api_token}'}
    repo_info = requests.get(repo_info_link, headers=authorization_header)
    repo_info_json = repo_info.json()
    if repo_info_json['fork']:
        zip_name = filename.replace('.py', '.zip')
        zip_path = f'repos_zip/{zip_name}'
        urllib.request.urlretrieve(repo_zip_file, zip_path)
        zipgrep_process = subprocess.Popen(
            ['zipgrep', '-i', 'op_checklocktimeverify', zip_path], stdout=subprocess.PIPE
        )
        wc_process = subprocess.Popen(["wc", '-l'], stdin=zipgrep_process.stdout, stdout=subprocess.PIPE)
        zipgrep_process.stdout.close()
        count = wc_process.communicate()[0]
        return int(count.strip())
    response = requests.get(search_link, headers=authorization_header)
    response_json = response.json()
    return response_json.get('total_count', 0)


def create_github_links(line):
    search_base = 'https://api.github.com/search/code?q=op_checklocktimeverify+in:file+repo:'
    repo_info_base = 'https://api.github.com/repos/'

    repo_name = line.strip().split('github.com/')[1]
    repo_name = repo_name.split('/blob/')[0]

    repo_zip_file = f'https://github.com/{repo_name}/archive/master.zip'

    return search_base + repo_name, repo_info_base + repo_name, repo_zip_file


if __name__ == '__main__':
    if get_github_api_token() is None:
        logger.error('GITHUB_API_TOKEN environment variable is required to run this script.')
        exit(1)

    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    network_dir = os.path.join(base_dir, 'clove/network/bitcoin_based/')
    files = sorted(glob.glob(network_dir+'*'))

    found = []
    fork = []
    failed = []

    os.makedirs('repos_zip', exist_ok=True)

    for file_path in files:
        if not os.path.isfile(file_path):
            continue

        filename = os.path.basename(file_path)
        if filename == '__init__.py':
            continue

        time.sleep(.1)
        with open(file_path, 'r') as f:
            file_lines = f.readlines()
            file_length = len(file_lines)

            indices = [i for i, line in enumerate(file_lines) if 'Class with all the necessary' in line]
            if not indices:
                logger.error("Couldn't find network class in %s", filename)
                continue
            try:
                count = search_checklocktime(file_lines, indices[0], filename)
                if count is None:
                    fork.append(filename)
                    logger.info("%s network is forked and cannot be searched", filename)
                    continue
                elif count == 0:
                    failed.append(filename)
                    logger.error("Couldn't find OP_CHECKLOCKTIMEVERIFY in %s network", filename)
                    continue
                found.append(filename)
                logger.info("Found %s in %s network", count, filename)

            except(HTTPError, URLError):
                failed.append(filename)
                logger.error("HTTP error in %s network", filename)
                continue

    logger.info('Found: %s', found)
    logger.info('Failed: %s', failed)
    logger.info('Fork: %s', fork)
    logger.info('Found: %s, Failed: %s, Fork: %s', len(found), len(failed), len(fork))
