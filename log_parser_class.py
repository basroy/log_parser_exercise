import re
from typing import Dict, List, Union

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

    EXPORT_model: str = ' -export '
    IMPORT_model: str = ' -import '
    DEBUG_model: str = ' -debug -process '
    FILE_cp: str = ' -file '
    ACTION_model: str = ' -action '
    CERT_model: str = ' -certificate '


class Colors:
    WHITE = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'


class ANP:
    parmeters: Dict = {
        '8a81b00f706eee3a0170ab3c020773b8^E928BFB6DCA645168E02C5A4AD410D60': 'ATFY21',
        '8a81b0136d31d24f016d3c604cb236fa^0CED7723541D486C94B6C453F23923D9': 'USERACCESS',
        '8a81b0116ee24a64016ffc2292aa7896^B0D764EEA7644995A161A6A7B4F65DF6': 'BKGHUB',
        '8a81b00f7522c5c10175468b101b04a3^E96CB3D54EDB431EB055182029D566A9': 'FY21NLG_2H',
        '8a81b010721f3bec01722c4420f878e0^5486F999A91246CF9D710D228864764F': 'FY22_NLG_HUB',
        '8a868cd87a25f4cf017a54dbb22c16e3^2FA3B2DE0B544E139FD6BB012D2DA513': 'FY22_NLG',
        '8a868cd87a25f4cf017a54d776c515d7^463B0A00F8FD4FE5839943BCC68D074E': 'FY22_NLG_SNAPSHOT',
        '8a81b00f6d31dc75016d4f837db81106^8B5B1716E92943B2967B603BAB7A9A8A': 'FY22_NLG_RPT',
        '8a81b011706ef07f0170aa26df7a23b5^CFEA3491AD6B4ED5B5E1CC1703633D4E': 'FY21NLG_UAT',
        '8a81b011720f725f017212c5c23678d8^914CFB646A074B5886762EDB3BFBC122': 'NLG_HUB',
        '8a81b011720f725f017212c44cdf788d^EABF24B166F0404DA34A2E00D5E43FE3': 'NLG_HUB_2H',
        '8a81b09c599f3d1a0159ff60f5e12b6d^456E2DFF385942B8BF45B1D465CEBE51': 'MERAKI',
        '8a81b09c599f3d1a0159ff60f5e12b6d^87CA052790A14BCBA9018E8F42ECFC57': 'MERAKI_SFDC_DATA',
        '8a81b0136cc586ba016ce3a8e40f1e1f^7F4DD0136E5A4319B8F64648ACD58D07': 'SCLASS_CUST_EXP',
        '8a81b0136cc586ba016d06f9a39d0fb5^CA5F8107B9D14589BE0689ACEB450878': 'SCLASS_FY22',
        '8a81b0126d31d3a2016d3c5b7b566143^0840DBA3081F498B99DBE083F006DDB6': 'SCLASS_UAT',
        '8a81b00e6ee246a8016f584e8a576ad8^50007A7C50B6462DA430D3D96C2AC584': 'TPX_SCLASS',
        '8a81b0116d31d5a8016d4186055f03ac^0E2C08013002467AADAAEC797AD62275': 'CENT',
        '8a81b00e6d31d425016d3c5e3375097b^FD58CFEA0AA24B8EA96253936B822BB4': 'BKGHUB_ATBE',
        '8a81b00e6ee246a8016f584e8a576ad8^21AFB617F1574F26BED27B2CC80E5534': 'TPX_FY22',
        '8a81b0106d31d556016d3c59c99941a9^6918C7ACD5A44F24B1D37C8F457EBDFE': 'SAVHUB',
        '8a81b0106d31d556016d3c59c99941a9^1DF1AF61970242EFAF7E7A2951C4140C': 'HUB'

    }


class Regex:
    regex_workspace = r'-workspace (.+) -model'
    regex_model_1 = r'-model (.+) -debug -process'
    regex_model_2 = r'-model (.+) -action'
    regex_model_3 = r'-model (.+) -certificate'
    regex_model_4 = r'-model (.+) -file'
    # regex_model_5 = r'-model (.+) -import'
    regex_model_6 = r'-model (.+) -export'

    regex_process = r'-process (.+)-execute'
    regex_export = r'-export (.+)-execute'
    regex_file = r'-file (.+)-put'
    regex_action = r'-action (.+)-execute'
    regex_import = r'-import (.+)-execute'

    def xtract_with_regex(self, line: str, regex: str) -> Union[str, None]:
        rg = re.compile(regex, re.IGNORECASE | re.DOTALL)

        match = rg.search(line)
        # print(f' {line}\n {match}')
        try:
            return match.group(1)
        except AttributeError or IndexError:
            # breakpoint()
            return

    # print(f'{regex_model}   {regex_process}'
    #       )


class Log_Parse(Regex):
    # class Log_Parse(Regex):

    def __int__(
            self,
            path_to_log_files: str = 'anaplan_logs',
            path_to_result_files: str = 'log_review'
    ):
        # self.regex = Regex()
        self.path_to_log_files = path_to_log_files
        self.path_to_return_files = path_to_return_files

    # api_status_list: List = []
    log_parse_dict: Dict = {}
    model_names: Dict = {}

    def constr_model_names_dict(self, lines: List):

        api_status_list: List = []
        curr_api_index: int = 1
        status_api_index: int = 0
        curr_api_name: str = ''
        model_name_counter: int = 0
        model_name_key: str = 'Unknown Model Name'
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

                # breakpoint()
                curr_api_index = index
                status_api_index = 0
                # if curr_api_name[-2:] == ' ' or curr_api_name[-2:] == '**':
                if curr_api_name[-3:] == "**":

                    # curr_api_name = self.model_names[model_name_key]
                    curr_api_name: Union[str, None] = self.model_names.get(
                        model_name_key)
                    if curr_api_name == None:
                        curr_api_name = 'Model or Workspace not mapped '
                    curr_api_name += '    Anaplan Unreachable'
                    print(f'Bashobi curr_api_name {curr_api_name[-3:]}')
                    # print(f'Bashobi curr_api_name {curr_api_name}')
                    # api_status_list.append(curr_api_name)

                    self.model_names[model_name_key] = curr_api_name

            # print(f' Length of key name {model_name_key}')
            if (is_operation_fail or is_operation_unavail or
                    is_operation_success):
                if len(model_name_key) > 1 and (model_name_key != 'Unknown '
                                                                  'Model Name'):
                    status_api_index = 1
                    curr_api_name = self.model_names[
                        model_name_key]

            if is_operation_success:
                curr_api_name += f'    {Operation.SUCCESS}'
            elif is_operation_fail:
                curr_api_name += f'    {Operation.FAILED}'
            elif is_operation_unavail:
                curr_api_name += f'    {Operation.DUMPFILE_NOT_AVAILABLE}'
            else:
                curr_api_name += f'   Anaplan Unreachable'

            # The API Line has no follow-up lines which have Operation Status. So,
            # only append ** at the end.
            if curr_api_index > 0 and status_api_index == 0:
                curr_api_name += '**'

            # The api Line has a Operation Status. Add it to the list.
            if curr_api_index > 0 and status_api_index == 1:
                curr_api_index = 0
                status_api_index = 0
                self.model_names[
                    model_name_key] = curr_api_name

        # print((c_log_parse.model_names))

    def construct_model_names_dict(self, lines: List):

        api_status_list: List = []
        curr_api_index: int = 1
        status_api_index: int = 0
        curr_api_name: str = ''
        model_name_counter: int = 0
        model_name_key: str = '9999:Unknown Model Name'
        file_line_number_anaplanclient: int = 0
        for index, line in enumerate(lines):

            is_execution_start: bool = Operation.START in line
            is_operation_success: bool = Operation.SUCCESS in line
            is_operation_fail: bool = Operation.FAILED in line
            is_operation_unavail: bool = Operation.DUMPFILE_NOT_AVAILABLE in line

            if not (is_execution_start or is_operation_unavail or \
                    is_operation_success or is_operation_fail):
                # print(' Do nothing with these file lines ')
                continue

            api_has_execution_status_true_or_false: bool = False

            if is_execution_start:
                model_name_counter += 1
                model_name_key: str = self.gen_model_name_key(
                    line=line,
                    model_name_counter=model_name_counter)
                curr_api_name: Union[str, None] = self.model_names.get(
                    model_name_key)

                file_line_number_anaplanclient: int = index
                api_execution_status: str = Operation.UNREACHABLE
            else:
                api_has_execution_status_true_or_false: bool = (
                        is_operation_fail or
                        is_operation_unavail or
                        is_operation_success
                )
                if is_operation_success:
                    api_execution_status = Operation.SUCCESS
                elif is_operation_fail:
                    api_execution_status = Operation.FAILED
                elif is_operation_unavail:
                    api_execution_status = Operation.DUMPFILE_NOT_AVAILABLE
                else:
                    api_execution_status = "Model Unknown"

            # print(f' Line--> {line[1:100]}')
            # print(f'file_line_number --> {file_line_number_anaplanclient}   '
            #       f'Index here is {index}')
            # breakpoint()
            self.model_names[model_name_key] = (
                    curr_api_name + f'  {api_execution_status}')

    def gen_model_name_key(self, line: str, model_name_counter: int) -> str:
        # print(line)
        # if re.search("./AnaplanClient.sh", line):
        workspace_token_new: Union[str, None] = self.xtract_with_regex(
            line,
            self.regex_workspace)

        model_token_new: str = self.regex_model_1
        token = None

        if Operation.EXPORT_model in line:
            model_token_new: Union[str, None] = (
                self.xtract_with_regex(line,
                                       self.regex_model_6
                                       )
            )
            token: str = (
                self.xtract_with_regex(
                    line,
                    self.regex_export
                )
            )
            # print(' Came here for EXPORT')

        # elif Operation.IMPORT_model in line:
        #     model_token_new: Union[str, None] = (
        #         self.xtract_with_regex(line,
        #                                self.regex_model_5
        #                                )
        #     )
        #     token: Union[str, None] = (
        #         self.xtract_with_regex(
        #             line,
        #             self.regex_import
        #         )
        #     )
        #
        #     print(' Came here for IMPORT')
        #     pass
        elif Operation.FILE_cp in line:
            model_token_new: Union[str, None] = (
                self.xtract_with_regex(line,
                                       self.regex_model_4
                                       )
            )
            if Operation.IMPORT_model in line:
                token: Union[str, None] = (
                    self.xtract_with_regex(
                        line,
                        self.regex_import
                    )
                )
            else:
                token: Union[str, None] = (
                    self.xtract_with_regex(
                        line,
                        self.regex_file
                    )
                )

            # print(' Came here for FILE')

        elif Operation.CERT_model in line:
            model_token_new: Union[str, None] = (
                self.xtract_with_regex(line,
                                       self.regex_model_3
                                       )
            )

            # print(' Came here for CERT')
        elif Operation.ACTION_model in line:
            model_token_new: Union[str, None] = (
                self.xtract_with_regex(line,
                                       self.regex_model_2
                                       )
            )
            token: Union[str, None] = (
                self.xtract_with_regex(
                    line,
                    self.regex_action
                )
            )

            # print(' Came here for ACTION')

        elif Operation.DEBUG_model in line:
            model_token_new: Union[str, None] = (
                self.xtract_with_regex(line,
                                       self.regex_model_1
                                       )
            )
            token: Union[str, None] = (
                self.xtract_with_regex(
                    line,
                    self.regex_process
                )
            )

            # print(' Came here for DEBUG')
        index_constructed_new = f'{model_name_counter}:{workspace_token_new}' \
                                f'^{model_token_new}'

        if token:
            self.model_names[index_constructed_new] = token

        else:
            self.model_names[index_constructed_new] = 'Incorrect connector ' \
                                                      'string to api'

        # print(f' ModelNames Dictionary is ready {self.model_names}')
        # print(
        #     f' Index for Dictionary is {index_constructed_new}')  # self.model_names
        return index_constructed_new  # self.model_names

    def color_the_dict_output(self, log_parse_dict):
        # print(self.anp_parm)
        for key, value in log_parse_dict.items():
            # print(key, value)

            if value == None:
                continue

            is_anaplan_unreachable: bool = Operation.UNREACHABLE in value
            DUMPFILE_NOT_AVAILABLE: bool = Operation.DUMPFILE_NOT_AVAILABLE in value
            OPERATION_FAILED: bool = Operation.FAILED in value
            OPERATION_SUCCESS: bool = Operation.SUCCESS in value

            key_extract: str = key.split(':')[1]
            # print(f' Second field of key : {key_extract}')

            if key_extract not in ANP.parmeters:
                continue

            display_model_operation_status: str = (
                f'{ANP.parmeters[key_extract]}   {value}'
            )

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

    def file_write_dict_output(self, log_parse_dict):
        path_to_out_file: str = 'anaplan_logs/api_status_log.txt'
        with open(file=path_to_out_file, mode='a') as f:
            for key, value in log_parse_dict.items():
                key_extract: str = key.split(':')[1]
                # print(f' Second field of key : {key_extract}')

                if key_extract in ANP.parmeters:
                    value += '\n'
                    display_model_operation_status: str = f'{ANP.parmeters[key_extract]}   {value}'

                # print(key, value)
                f.write(display_model_operation_status)
        f.close()


c_log_parse = Log_Parse(
)
# # Execute One File at a time
# path_to_file: str = 'anaplan_logs/Sclass_sav_refresh.log'
#
# with open(file=path_to_file, mode='r') as f:
#     lines = f.readlines()
# f.close()
# # c_get_status_1 = c_log_parse.constr_model_names_dict(lines)
# c_get_status_1 = c_log_parse.construct_model_names_dict(lines)
# c_get_status_colour_1 = c_log_parse.color_the_dict_output(
#     c_log_parse.model_names)
# # Execute One File at a time end

path_to_file: str = 'anaplan_logs'
# path_to_file: str = 'log_files/anp_user.txt'

import os

subfiles = []
for dirpath, subdirs, files in os.walk(path_to_file):
    for x in files:
        if x.endswith(".log"):
            subfiles.append(os.path.join(dirpath, x))

for file in subfiles:
    with open(file=file, mode='r') as f:
        lines = f.readlines()
    f.close()
    print(f'{Colors.RED}'
          f' LOG FILE BEING PROCESRED IS {file}'
          f'{Colors.GREEN}')

    #
    c_get_status = c_log_parse.construct_model_names_dict(lines)
    c_get_status_colour = c_log_parse.color_the_dict_output(
        c_log_parse.model_names)
    c_write_status = c_log_parse.file_write_dict_output(
        c_log_parse.model_names)
