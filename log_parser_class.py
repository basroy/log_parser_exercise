import re
from typing import Dict

path_to_file: str = 'log_files/anp_user.txt'
# path_to_file: str = 'log_files/anp_user.txt'

with open(file=path_to_file, mode='r') as f:
    lines = f.readlines()
f.close()


class Log_Parse:
    EXECUTION_START: str = './AnaplanClient.sh'
    # TODO: Search for "The operation was successful."
    OPERATION_SUCCESS: str = 'The operation was successful.'
    # TODO: Search for "No dump file is available."
    DUMPFILE_NOT_AVAILABLE: str = 'No dump file is available.'
    # TODO: Search for "The operation has failed."
    OPERATION_FAILED: str = 'The operation has failed.'
    # TODO: If none of the 3 above are found, log error "Couldn't find operation log message"

    # api_status_list: List = []
    curr_api_index: int = 1
    status_api_index: int = 0
    curr_api_name: str = ''

    model_names: Dict = {}
    anp_parm: Dict = {
        '8a81b0116ee24a64016ffc2292aa7896^B0D764EEA7644995A161A6A7B4F65DF6':
            'BKGHUB',
        '8a81b00f7522c5c10175468b101b04a3^E96CB3D54EDB431EB055182029D566A9':
            'FY21NLG_2H',
        '8a81b010721f3bec01722c4420f878e0^5486F999A91246CF9D710D228864764F': 'FY22_NLG_HUB',
        '8a868cd87a25f4cf017a54dbb22c16e3^2FA3B2DE0B544E139FD6BB012D2DA513':
            'FY22_NLG',
        '8a868cd87a25f4cf017a54d776c515d7^463B0A00F8FD4FE5839943BCC68D074E':
            'FY22_NLG_SNAPSHOT',
        '8a81b00f6d31dc75016d4f837db81106^8B5B1716E92943B2967B603BAB7A9A8A':
            'FY22_NLG_RPT',
        '8a81b09c599f3d1a0159ff60f5e12b6d^456E2DFF385942B8BF45B1D465CEBE51': \
            'MERAKI',
        '8a81b09c599f3d1a0159ff60f5e12b6d^87CA052790A14BCBA9018E8F42ECFC57': \
            'MERAKI_SFDC_DATA',
        '8a81b0136cc586ba016ce3a8e40f1e1f^7F4DD0136E5A4319B8F64648ACD58D07': \
            'SCLASS_CUST_EXP',
        '8a81b0136cc586ba016d06f9a39d0fb5^CA5F8107B9D14589BE0689ACEB450878':
            'SCLASS_FY22',
        '8a81b0126d31d3a2016d3c5b7b566143^0840DBA3081F498B99DBE083F006DDB6': 'SCLASS_UAT',
        '8a81b00e6ee246a8016f584e8a576ad8^50007A7C50B6462DA430D3D96C2AC584':
            'TPX_SCLASS',
        '8a81b0116d31d5a8016d4186055f03ac^0E2C08013002467AADAAEC797AD62275':
            'CENT',
        '8a81b00e6d31d425016d3c5e3375097b^FD58CFEA0AA24B8EA96253936B822BB4':
            'BKGHUB_ATBE',
        '8a81b00e6ee246a8016f584e8a576ad8^21AFB617F1574F26BED27B2CC80E5534': 'TPX_FY22'
    }

    def construct_model_names_dict(self, log_line: str) -> Dict:
        if re.search("./AnaplanClient.sh", log_line):
            workspace = re.search("-workspace ", log_line)
            s_workspace = workspace.start()
            e_workspace = workspace.end()

            # print(workspace.re.pattern, workspace.string, s_workspace, e_workspace,
            #       line[s_workspace:e_workspace])
            model = re.search("-model ", log_line)
            debug = re.search("-debug ", log_line)
            process = re.search("-process ", log_line)
            execute = re.search("-execute ", log_line)
            s_model = model.start()
            e_model = model.end()
            s_debug = debug.start()
            s_process = process.start()
            e_process = process.end()
            s_execute = execute.start()

            workspace_token = line[e_workspace:s_model - 1]
            model_token = line[e_model:s_debug - 1]
            process_token = line[e_process:s_execute - 1]
            # print(workspace_token, model_token,process_token)
            c_log_parse.model_names[workspace_token + '^' + model_token] = \
                process_token
            return ''


c_log_parse = Log_Parse(

)
# regex = '(<property name="(.*?)">(.*?)<\/property>)'
# for line in lines:
for index, line in enumerate(lines):
    # print(line)
    # x = re.search("./AnaplanClient.sh", line)
    # print(type(x))

    # is_execution_start: bool = EXECUTION_START in line
    # is_operation_success: bool = OPERATION_SUCCESS in line
    # is_operation_fail: bool = OPERATION_FAILED in line
    # is_operation_unavail: bool = DUMPFILE_NOT_AVAILABLE in line

    if re.search("./AnaplanClient.sh", line):
        print(f'File Line -----> {line}')
        workspace = re.search("-workspace ", line)
        s_workspace = workspace.start()
        e_workspace = workspace.end()

        # print(workspace.re.pattern, workspace.string, s_workspace, e_workspace,
        #       line[s_workspace:e_workspace])
        model = re.search("-model ", line)
        debug = re.search("-debug ", line)
        process = re.search("-process ", line)
        execute = re.search("-execute ", line)
        s_model = model.start()
        e_model = model.end()
        s_debug = debug.start()
        s_process = process.start()
        e_process = process.end()
        s_execute = execute.start()

        workspace_token = line[e_workspace:s_model - 1]
        model_token = line[e_model:s_debug - 1]
        process_token = line[e_process:s_execute - 1]
        # print(workspace_token, model_token,process_token)
        c_log_parse.model_names[workspace_token + '^' + model_token] = \
            process_token

# print(c_log_parse.model_names)
# print(c_log_parse.model_names)
for key, value in c_log_parse.model_names.items():
    print(key, value)
    if key in c_log_parse.anp_parm:
        print(c_log_parse.anp_parm[key], value)
