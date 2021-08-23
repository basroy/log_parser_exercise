import getopt
import glob
import os
import sys
from typing import List

from core import LogParser
from support import Colors


def main(argv):
    inputfile: str = ''
    inputtype: str = ''
    outputfile: str = ''
    try:
        # opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        opts, args = getopt.getopt(argv, "hi:o:t:")
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile> -t <inputfiletype')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--type"):
            inputtype = arg

    print('Input file location is ', inputfile)

    print('Output file location is ', outputfile)
    if inputtype == 'log':
        print('Input file type is to be processed is text log files')

    elif inputtype == 'informat':
        print('Input file type is to be processed is informatica log files')

    return inputfile, outputfile


if __name__ == "__main__":
    inputfile, outputfile = main(sys.argv[1:])

parser = LogParser()
current_directory: str = os.getcwd()
log_file_path: str = os.path.join(current_directory, '..', inputfile, '*')
results_dir_path: str = os.path.join(current_directory, '..', outputfile)
# log_file_path: str = os.path.join(current_directory, '..', 'anp_logs', '*')
# results_dir_path: str = os.path.join(current_directory, '..', 'results')
print(results_dir_path)
log_files: List[str] = glob.glob(log_file_path)

for log_file in log_files:
    with open(file=log_file, mode='r') as f:
        lines = f.readlines()
    f.close()
    print(f'{Colors.RED}'
          f' LOG FILE BEING PROCESRED IS {log_file}'
          f'{Colors.GREEN}')
    parser.construct_model_names(lines)

parser.dump_results()

parser.write_results(
    log_file_name='anplog',
    # log_file_name=os.path.basename(log_file).split('.')[0],
    results_dir_path=results_dir_path
)
# if content:
#     with open(results_file_path, 'w')as f:
#         f.write(content)
#     f.close()
