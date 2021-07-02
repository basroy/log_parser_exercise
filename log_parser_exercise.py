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
    "API_LINE": 1,
    "API_LINE": "",
    "EXEC_STATUS": ""
}

curr_api_index: int = 1
curr_api_name: str = ''
for index, line in enumerate(lines):
    is_execution_start: bool = EXECUTION_START in line
    is_operation_success: bool = OPERATION_SUCCESS in line
    is_operation_fail: bool = OPERATION_FAILED in line
    is_operation_unavail: bool = DUMPFILE_NOT_AVAILABLE in line
    if is_execution_start:
        print(line, f'    {index}')
        curr_api_index = index
        curr_api_name = line
        # api_status['API_NAME'] = line
    else:
        curr_api_index = 0
    if is_operation_success:
        print(f'      {DUMPFILE_NOT_AVAILABLE}')
    if is_operation_fail:
        print(f'      {OPERATION_FAILED}')
    if is_operation_unavail:
        print(f'      {OPERATION_SUCCESS}')
    if not is_operation_fail and not is_operation_success and \
            not is_operation_unavail:
        print('Anaplan Unreachable')

    if  is_operation_fail or is_operation_success or  is_operation_unavail:
            api_status = dict(API_LINE=curr_api_index, API_NAME=curr_api_name,
                              EXEC_STATUS=OPERATION_FAILED or OPERATION_SUCCESS
                                          or DUMPFILE_NOT_AVAILABLE)

    print(api_status)

