import glob
import os
from typing import List

from core import LogParser
from support import Colors

parser = LogParser()
current_directory: str = os.getcwd()
log_file_path: str = os.path.join(current_directory, '..', 'anp_logs', '*')
results_dir_path: str = os.path.join(current_directory, '..', 'results')
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
