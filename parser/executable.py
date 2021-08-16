import glob
import os
from typing import List

from core import LogParser
from support import Colors

parser = LogParser()
current_directory: str = os.getcwd()
log_file_path: str = os.path.join(current_directory, '..', 'anp_logs', '*')
results_dir_path: str = os.path.join(current_directory, '..', 'results')

log_files: List[str] = glob.glob(log_file_path)
# # Execute One File at a time
# path_to_file: str = 'anaplan_logs/SFDC_GTM_PIPELINE.log'
# path_to_file: str = 'log_files/anp_user.txt'
#
# with open(file=path_to_file, mode='r') as f:
#     lines = f.readlines()
# f.close()
# c_get_status_1 = c_log_parse.construct_model_names_dict(lines)
# c_get_status_colour_1 = c_log_parse.dump_results(
#     c_log_parse.model_names)
# # Execute One File at a time end

# path_to_file: str = 'anaplan_logs'
# path_to_file: str = 'anp_logs'

for log_file in log_files
    with open(file=log_file, mode='r') as f:
        lines = f.readlines()
    f.close()
    print(f'{Colors.RED}'
          f' LOG FILE BEING PROCESRED IS {file}'
          f'{Colors.GREEN}')
    c_get_status = parser.construct_model_names(lines)

    parser.dump_results()
    parser.write_results(
        log_file_name=os.path.basename(log_file).split('.')[0],
        results_dir_path=results_dir_path
    )
