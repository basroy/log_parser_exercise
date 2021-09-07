import getopt
import glob
import os
import sys
from typing import List

from core import LogParser
from support import Colors


def validate_arguments(argv) -> List:
    sourceloc: str = ''
    inputtype: str = ''
    targetloc: str = ''
    try:
        # opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
        opts, args = getopt.getopt(argv, "hi:o:t:")
    except getopt.GetoptError:
        print('test.py -i <source loc> -o <target loc> -t <inputfiletype')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <source loc> -o <target loc>')
            sys.exit()
        elif opt in ('-i', '--ifile'):
            sourceloc = arg
        elif opt in ('-o', '--ofile'):
            targetloc = arg
        elif opt in ('-t', '--type'):
            inputtype = arg
        else:
            print('test.py -i <source loc> -o <target loc>')
            sys.exit()

    if inputtype == 'log':
        print('Input file type is to be processed is text log files')

    elif inputtype == 'informat':
        print('Input file type is to be processed is informatica log files')

    all_locations: List = [sourceloc, targetloc]
    return all_locations


# if __name__ == "__main__":
if len(sys.argv) < 3:
    print('The script needs at least 2 argumants')
    print('executable.py -i <source loc> -o <target loc>')
    exit()
    
sourceloc, targetloc = validate_arguments(sys.argv[1:])

parser = LogParser()
current_directory: str = os.getcwd()
log_file_path: str = os.path.join(current_directory, '..', sourceloc, '*')
results_dir_path: str = os.path.join(current_directory, '..', targetloc)
# log_file_path: str = os.path.join(current_directory, '..', 'anaplan_logs', '*')
# results_dir_path: str = os.path.join(current_directory, '..', 'results')
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
