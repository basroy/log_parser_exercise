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

api_status: Dict = {
    "API_LINE_NUM": 1,
    "API_LINE": "",
    "EXEC_1": "",
    "EXEC_2": "",
    "EXEC_3": "",
    "EXEC_4": ""
}

curr_api_index: int = 1
curr_api_name: str = ''
for index, line in enumerate(lines):
    is_execution_start: bool = EXECUTION_START in line
    is_operation_success: bool = OPERATION_SUCCESS in line
    is_operation_fail: bool = OPERATION_FAILED in line
    is_operation_unavail: bool = DUMPFILE_NOT_AVAILABLE in line
    if is_execution_start:
        # print(line, f'    {index}')
        curr_api_index = index
        curr_api_name = line
        # api_status['API_NAME'] = line
    else:
        curr_api_index = 0
    if is_operation_success:
        api_status = dict(API_LINE_NUM=curr_api_index,
                          API_NAME=curr_api_name,
                          EXEC_1=OPERATION_SUCCESS)
    if is_operation_fail:
        api_status = dict(API_LINE_NUM=curr_api_index,
                          API_NAME=curr_api_name,
                          EXEC_3=OPERATION_FAILED)
        # print(f'      {OPERATION_SUCCESS}')
        # print(f'      {OPERATION_FAILED}')
    if is_operation_unavail:
        # print(f'      {DUMPFILE_NOT_AVAILABLE}')
        api_status = dict(API_LINE_NUM=curr_api_index,
                          API_NAME=curr_api_name,
                          EXEC_3=DUMPFILE_NOT_AVAILABLE)
    #     print('Anaplan Unreachable')

    if  is_operation_fail or is_operation_success or  is_operation_unavail:
        pass

    print(api_status)

