from typing import List
from typing import Dict


path_to_file: str = 'log_files/anp_user.txt'

with open(file=path_to_file, mode='r') as f:
    lines = f.readlines()
f.close()

#print(lines)

EXECUTION_START: str = './AnaplanClient.sh'
# TODO: Search for "The operation was successful."
OPERATION_SUCCESS: str = 'The operation was successful.'
# TODO: Search for "No dump file is available."
DUMPFILE_NOT_AVAILABLE: str = 'No dump file is available.'
# TODO: Search for "The operation has failed."
OPERATION_FAILED: str = 'The operation has failed.'
# TODO: If none of the 3 above are found, log error "Couldn't find operation log message"

api_status_list: List = []
curr_api_index: int = 1
status_api_index: int = 0
curr_api_name: str = ''
for index, line in enumerate(lines):
    is_execution_start: bool = EXECUTION_START in line
    is_operation_success: bool = OPERATION_SUCCESS in line
    is_operation_fail: bool = OPERATION_FAILED in line
    is_operation_unavail: bool = DUMPFILE_NOT_AVAILABLE in line
    if is_execution_start:
        #print(curr_api_name[-3])
        if curr_api_name[-3] == '*':
            # print('bashobi')
            curr_api_name += 'Anaplan Unreachable'
            api_status_list.append(curr_api_name)
        status_api_index = 0
        # print(line, f'    {index}')
        curr_api_index = index
        curr_api_name = line[109:195]

    if is_operation_success:
        status_api_index = 1
        curr_api_name += f'{OPERATION_SUCCESS}'
    if is_operation_fail:
        status_api_index = 1
        curr_api_name += f'{OPERATION_FAILED}'
    if is_operation_unavail:
        status_api_index = 1
        curr_api_name += f'{DUMPFILE_NOT_AVAILABLE}'

# The API Line has no follow-up lines which have Operation Status. So,
    # only append ** at the end.
    if curr_api_index > 0 and status_api_index == 0:
        curr_api_name += '**'
        # api_status_list.append(curr_api_name)

# The api Line has a Operation Status. Add it to the list.
    if curr_api_index > 0 and status_api_index == 1:
        api_status_list.append(curr_api_name)
        curr_api_index = 0
        status_api_index = 0

# print(api_status_list)
# print(len(api_status_list))
for x in api_status_list:
    is_anaplan_unreachable: bool = "Anaplan Unreachable" in x
    if is_anaplan_unreachable:
        print(x)



