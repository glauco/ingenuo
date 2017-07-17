import sys
import os

from src import RosettaExerciseWebCrawler
from src import RosettaCodeWebCrawler

def run_analysis(args):
    print('running analysis…')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'download-data':
            download_data(sys.argv)
    else:
        run_analysis(sys.argv)
