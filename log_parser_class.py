import os
import re
from typing import Dict, List, Union


class Operation:
    START: str = './AnaplanClient.sh'
    SUCCESS: str = 'The operation was successful.'
    DUMPFILE_NOT_AVAILABLE: str = 'No dump file is available.'
    FAILED: str = 'The operation has failed.'
    UNREACHABLE: str = 'Anaplan Unreachable'

    EXPORT_model: str = ' -export '
    IMPORT_model: str = ' -import '
    DEBUG_model: str = ' -debug -process '
    PROCESS_model: str = ' -process '
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
    regex_model_debug_process = r'-model (.+) -debug -process'
    regex_model_process = r'-model (.+) -process'
    regex_model_action = r'-model (.+) -action'
    regex_model_certificate = r'-model (.+) -certificate'
    regex_model_file = r'-model (.+) -file'
    regex_model_import = r'-model (.+) -import'
    regex_model_export = r'-model (.+) -export'

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
            return


class LogParser(Regex):

    def __init__(
            self,
            path_to_log_files: str = 'anaplan_logs',
            path_to_result_files: str = 'log_review'
    ):
        # self.regex = Regex()
        self.path_to_log_files = path_to_log_files
        self.path_to_return_files = path_to_result_files

    log_parse_dict: Dict = {}
    model_names: Dict = {}

    def construct_model_names_dict(self, lines: List):

        curr_api_name: str = ''
        model_name_counter: int = 0
        model_name_key: str = '9999:Unknown Model Name'

        for index, line in enumerate(lines):

            is_execution_start: bool = Operation.START in line
            is_operation_success: bool = Operation.SUCCESS in line
            is_operation_fail: bool = Operation.FAILED in line
            is_operation_unavail: bool = Operation.DUMPFILE_NOT_AVAILABLE in line

            construct_names: bool = any([
                is_execution_start,
                is_operation_unavail,
                is_operation_success,
                is_operation_fail
            ])
            if not construct_names:
                # print(' Do nothing with these file lines ')
                continue

            if is_execution_start:
                model_name_counter += 1
                model_name_key: str = self.gen_model_name_key(
                    line=line,
                    model_name_counter=model_name_counter)
                curr_api_name: Union[str, None] = self.model_names.get(
                    model_name_key)

                api_execution_status: str = Operation.UNREACHABLE
            else:
                if is_operation_success:
                    api_execution_status = Operation.SUCCESS
                elif is_operation_fail:
                    api_execution_status = Operation.FAILED
                elif is_operation_unavail:
                    api_execution_status = Operation.DUMPFILE_NOT_AVAILABLE
                else:
                    api_execution_status = "Model Unknown"

            self.model_names[model_name_key] = (
                    curr_api_name + f'  {api_execution_status}'
            )

    def gen_model_name_key(self, line: str, model_name_counter: int) -> str:

        workspace_token: Union[str, None] = self.xtract_with_regex(
            line=line,
            regex=self.regex_workspace)

        model_token_regex: str = self.regex_model_debug_process
        api_type_token_value: str = ''

        if Operation.EXPORT_model in line:
            model_token_regex: str = self.regex_model_export
            api_type_token_value: str = self.regex_export

        elif Operation.IMPORT_model in line and Operation.FILE_cp not in line:
            model_token_regex: str = self.regex_model_import
            api_type_token_value: str = self.regex_import
        elif Operation.FILE_cp in line:
            model_token_regex: str = self.regex_model_file
            if Operation.IMPORT_model in line:
                api_type_token_value: str = self.regex_import
            else:
                api_type_token_value: str = self.regex_file

        elif Operation.CERT_model in line:
            model_token_regex: str = self.regex_model_certificate
        elif Operation.ACTION_model in line:
            model_token_regex: str = self.regex_model_action
            api_type_token_value: str = self.regex_action

        elif Operation.DEBUG_model in line:
            model_token_regex: str = self.regex_model_debug_process
            api_type_token_value: str = self.regex_process
        elif (Operation.PROCESS_model in line and
              Operation.DEBUG_model not in line
        ):
            model_token_regex: str = self.regex_model_process
            api_type_token_value: str = self.regex_process

        model_token: Union[str, None] = (
            self.xtract_with_regex(
                line=line,
                regex=model_token_regex
            )
        )
        token: Union[str, None] = (
            self.xtract_with_regex(
                line=line,
                regex=api_type_token_value
            )
        )

        index_constructed = (
            f'{model_name_counter}:{workspace_token}^{model_token}'
        )

        if token:
            self.model_names[index_constructed] = token
        else:
            self.model_names[index_constructed] = (
                'Incorrect connector string to api'
            )

        return index_constructed

    def dump_results(self):

        for key, execution_status in self.model_names.items():

            if execution_status is None:
                continue

            is_anaplan_unreachable: bool = (
                    Operation.UNREACHABLE in execution_status
            )
            DUMPFILE_NOT_AVAILABLE: bool = (
                    Operation.DUMPFILE_NOT_AVAILABLE in execution_status
            )
            OPERATION_FAILED: bool = Operation.FAILED in execution_status
            OPERATION_SUCCESS: bool = Operation.SUCCESS in execution_status

            key_extract: str = key.split(':')[1]

            if key_extract not in ANP.parmeters:
                continue

            display_model_operation_status: str = (
                f'{ANP.parmeters[key_extract]}   {execution_status}'
            )

            if OPERATION_SUCCESS:
                print(f'{Colors.BLUE}'
                      f'{display_model_operation_status}'
                      f'{Colors.WHITE}')
            elif is_anaplan_unreachable:
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

    def write_results(self):
        # def write_results(self, dict_of_api_execution_status: Dict):
        path_to_out_file: str = 'anaplan_logs/api_status_log.txt'
        with open(file=path_to_out_file, mode='a') as f:
            # for key, execution_status in dict_of_api_execution_status.items():
            for key, execution_status in self.model_names.items():
                key_extract: str = key.split(':')[1]
                is_anaplan_unreachable: bool = Operation.UNREACHABLE in execution_status

                if key_extract in ANP.parmeters:

                    if is_anaplan_unreachable:
                        execution_status += '\n'

                        f.write(
                            f'{ANP.parmeters[key_extract]} {execution_status}')
                    else:
                        continue
        f.close()


c_log_parse = LogParser(
)
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
path_to_file: str = 'anp_logs'

subfiles = []
for dirpath, subdirs, files in os.walk(path_to_file):
    for x in files:
        print(f' LOG FILE IS --> {x}')
        if x.endswith(".log"):
            subfiles.append(os.path.join(dirpath, x))
print(subfiles)
for file in subfiles:
    with open(file=file, mode='r') as f:
        lines = f.readlines()
    f.close()
    print(f'{Colors.RED}'
          f' LOG FILE BEING PROCESRED IS {file}'
          f'{Colors.GREEN}')
    c_get_status = c_log_parse.construct_model_names_dict(lines)

c_get_status_colour = c_log_parse.dump_results()
#
# c_write_status = c_log_parse.write_results(
#     dict_of_api_execution_status=c_log_parse.model_names)

c_write_status = c_log_parse.write_results()
