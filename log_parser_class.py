import re
from typing import Dict
from typing import List

path_to_file: str = 'log_files/anp_user.txt'
# path_to_file: str = 'log_files/anp_user.txt'

with open(file=path_to_file, mode='r') as f:
    lines = f.readlines()
f.close()


class Operation:
    START: str = './AnaplanClient.sh'
    SUCCESS: str = 'The operation was successful.'
    DUMPFILE_NOT_AVAILABLE: str = 'No dump file is available.'
    FAILED: str = 'The operation has failed.'
    UNREACHABLE: str = 'Anaplan Unreachable'


class Colors:
    WHITE = '\033[0m'  # white (normal)
    RED = '\033[31m'  # red
    GREEN = '\033[32m'  # green
    ORANGE = '\033[33m'  # orange
    BLUE = '\033[34m'  # blue
    PURPLE = '\033[35m'  # purple


class ANP:
    parmeters: Dict = {
        '8a81b00f706eee3a0170ab3c020773b8^E928BFB6DCA645168E02C5A4AD410D60': 'ATFY21',
        '8a81b0136d31d24f016d3c604cb236fa^0CED7723541D486C94B6C453F23923D9': 'USERACCESS',
        '8a81b0116ee24a64016ffc2292aa7896^B0D764EEA7644995A161A6A7B4F65DF6': 'BKGHUB',
        '8a81b00f7522c5c10175468b101b04a3^E96CB3D54EDB431EB055182029D566A9': 'FY21NLG_2H',
        '8a81b010721f3bec01722c4420f878e0^5486F999A91246CF9D710D228864764F': 'FY22_NLG_HUB',
        '8a868cd87a25f4cf017a54dbb22c16e3^2FA3B2DE0B544E139FD6BB012D2DA513': 'FY22_NLG',
        '8a868cd87a25f4cf017a54d776c515d7^463B0A00F8FD4FE5839943BCC68D074E': 'FY22_NLG_SNAPSHOT',
        '8a81b00f6d31dc75016d4f837db81106^8B5B1716E92943B2967B603BAB7A9A8A':
            'FY22_NLG_RPT',
        '8a81b09c599f3d1a0159ff60f5e12b6d^456E2DFF385942B8BF45B1D465CEBE51': 'MERAKI',
        '8a81b09c599f3d1a0159ff60f5e12b6d^87CA052790A14BCBA9018E8F42ECFC57': 'MERAKI_SFDC_DATA',
        '8a81b0136cc586ba016ce3a8e40f1e1f^7F4DD0136E5A4319B8F64648ACD58D07': 'SCLASS_CUST_EXP',
        '8a81b0136cc586ba016d06f9a39d0fb5^CA5F8107B9D14589BE0689ACEB450878': 'SCLASS_FY22',
        '8a81b0126d31d3a2016d3c5b7b566143^0840DBA3081F498B99DBE083F006DDB6': 'SCLASS_UAT',
        '8a81b00e6ee246a8016f584e8a576ad8^50007A7C50B6462DA430D3D96C2AC584': 'TPX_SCLASS',
        '8a81b0116d31d5a8016d4186055f03ac^0E2C08013002467AADAAEC797AD62275': 'CENT',
        '8a81b00e6d31d425016d3c5e3375097b^FD58CFEA0AA24B8EA96253936B822BB4': 'BKGHUB_ATBE',
        '8a81b00e6ee246a8016f584e8a576ad8^21AFB617F1574F26BED27B2CC80E5534': 'TPX_FY22'
    }


class Regex:
    regex_workspace = r'-workspace (.+) -model'
    regex_model = r'-model (.+) -debug'
    regex_process = r'-process (.+)-execute'
    # print(f'{regex_model}   {regex_process}'
    #       )


class Log_Parse:

    def __int__(self):
        #  api_status_list: List):
        # self.curr_api_name = ''
        # self.curr_api_index: int = 1
        # self.status_api_index: int = 0
        # self.api_status_list: List = api_status_list
        # self.is_execution_start: bool = false
        # self.is_operation_success: bool = false
        # self.is_operation_fail: bool = false
        # self.is_operation_unavail: bool = false
        pass

    # api_status_list: List = []
    log_parse_dict: Dict = {}
    model_names: Dict = {}

    def constr_model_names_dict(self):

        api_status_list: List = []
        curr_api_index: int = 1
        status_api_index: int = 0
        curr_api_name: str = ''
        model_name_counter: int = 0
        for index, line in enumerate(lines):

            is_execution_start: bool = Operation.START in line
            is_operation_success: bool = Operation.SUCCESS in line
            is_operation_fail: bool = Operation.FAILED in line
            is_operation_unavail: bool = Operation.DUMPFILE_NOT_AVAILABLE in line

            if is_execution_start:
                model_name_counter += 1
                model_name_key: str = self.gen_model_name_key(
                    line=line,
                    model_name_counter=model_name_counter)
                # print(c_log_parse.model_names[model_name_key])
                # print(f' Print curr_api_name {curr_api_name}')
                # print(curr_api_name[-3])
                if curr_api_name[-3] == '*':
                    curr_api_name = self.model_names[
                        model_name_key]
                    curr_api_name += '    Anaplan Unreachable'
                    # api_status_list.append(curr_api_name)

                    self.model_names[
                        model_name_key] = curr_api_name

                curr_api_index = index
                status_api_index = 0

            # print(f' Length of key name {model_name_key}')
            if (is_operation_fail or is_operation_unavail or \
                    is_operation_success):
                if len(model_name_key) > 1:
                    status_api_index = 1
                    curr_api_name = self.model_names[
                        model_name_key]

            if is_operation_success:
                curr_api_name += f'    {Operation.SUCCESS}'

            if is_operation_fail:
                curr_api_name += f'    {Operation.FAILED}'
            if is_operation_unavail:
                curr_api_name += f'    {Operation.DUMPFILE_NOT_AVAILABLE}'

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
                self.model_names[
                    model_name_key] = curr_api_name

        # print((c_log_parse.model_names))

    def xtract_with_regex(self, line: str, regex: str):
        rg = re.compile(regex, re.IGNORECASE | re.DOTALL)
        match = rg.search(line)
        return match.group(1)

    def gen_model_name_key(self, line: str, model_name_counter: int) -> str:
        # print(line)
        # if re.search("./AnaplanClient.sh", line):
        workspace_token_new = self.xtract_with_regex(line,
                                                     Regex.regex_workspace)

        model_token_new = self.xtract_with_regex(line, Regex.regex_model)
        process_token_new = self.xtract_with_regex(line, Regex.regex_process)

        # print(process_token)
        # workspace = self.xtract_with_regex(line, Regex.regex_workspace)
        # workspace = re.search("-workspace ", line)
        # s_workspace = workspace.start()
        # e_workspace = workspace.end()
        #
        # model = re.search("-model ", line)
        # debug = re.search("-debug ", line)
        # process = re.search("-process ", line)
        # execute = re.search("-execute ", line)
        # s_model = model.start()
        # e_model = model.end()
        # s_debug = debug.start()
        # s_process = process.start()
        # e_process = process.end()
        # s_execute = execute.start()
        #
        # workspace_token = line[e_workspace:s_model - 1]
        # model_token = line[e_model:s_debug - 1]
        # process_token = line[e_process:s_execute - 1]
        # # print(workspace_token, model_token,process_token)
        # index_constructed = f'{model_name_counter}:{workspace_token}^{model_token}'
        # print(f'Old way    {index_constructed}')
        index_constructed_new = f'{model_name_counter}:{workspace_token_new}' \
                                f'^{model_token_new}'
        # print(f'New way    {index_constructed_new}')
        self.model_names[index_constructed_new] = process_token_new

        return index_constructed_new  # self.model_names

    def color_the_dict_output(self, log_parse_dict):
        # print(self.anp_parm)
        for key, value in log_parse_dict.items():
            # print(key, value)
            is_anaplan_unreachable: bool = Operation.UNREACHABLE in value
            DUMPFILE_NOT_AVAILABLE: bool = Operation.DUMPFILE_NOT_AVAILABLE in value
            OPERATION_FAILED: bool = Operation.FAILED in value
            OPERATION_SUCCESS: bool = Operation.SUCCESS in value

            key_extract: str = key.split(':')[1]
            # print(f' Second field of key : {key_extract}')

            if key_extract in ANP.parmeters:
                display_model_operation_status: str = f'{ANP.parmeters[key_extract]}   {value}'

                if OPERATION_SUCCESS:
                    print(f'{Colors.BLUE}'
                          f'{display_model_operation_status}'
                          f'{Colors.WHITE}')
                if is_anaplan_unreachable:
                    print(f'{Colors.GREEN}'
                          f'{display_model_operation_status}'
                          f'{Colors.WHITE}')
                elif DUMPFILE_NOT_AVAILABLE:
                    print(f'{Colors.PURPLE}'
                          f'{display_model_operation_status}'
                          f'{Colors.WHITE}')
                elif OPERATION_FAILED:
                    print(f'{Colors.WHITE}'
                          f'{display_model_operation_status}'
                          f'{Colors.WHITE}')
                else:
                    pass


c_log_parse = Log_Parse(
)
c_get_status = c_log_parse.constr_model_names_dict()
c_get_status_colour = c_log_parse.color_the_dict_output(
    c_log_parse.model_names)
