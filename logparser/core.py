import datetime
import os.path
from typing import List, Dict, Union

from support import ANP, Regex, Operation, Colors


class LogParser(Regex):

    def __init__(
            self,
            path_to_log_files: str = 'anaplan_logs',
            path_to_result_files: str = 'log_review'
    ):
        self.path_to_log_files = path_to_log_files
        self.path_to_return_files = path_to_result_files

    log_parse_dict: Dict = {}
    model_names: Dict = {}

    def construct_model_names(self, lines: List) -> None:

        curr_api_name: str = ''
        model_name_counter: int = 0
        model_name_key: str = '9999:Unknown Model Name'
        for index, line in enumerate(lines):
            is_execution_start: bool = Operation.START in line
            is_operation_success: bool = Operation.SUCCESS in line
            is_operation_fail: bool = Operation.FAILED in line
            is_operation_unavail: bool = (
                    Operation.DUMPFILE_NOT_AVAILABLE in line
            )
            construct_names: bool = any([
                is_execution_start,
                is_operation_unavail,
                is_operation_success,
                is_operation_fail
            ])
            if not construct_names:
                continue
            if is_execution_start:
                model_name_counter += 1
                model_name_key: str = self.gen_model_name_key(
                    line=line,
                    model_name_counter=model_name_counter
                )
                curr_api_name: Union[str, None] = (
                    self.model_names.get(
                        model_name_key
                    )
                )
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

        workspace_token: Union[str, None] = (
            self.xtract_with_regex(
                line=line,
                regex=self.regex_workspace
            )
        )
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
        elif (
                Operation.PROCESS_model in line and
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

        index_constructed: str = (
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

    def write_results(
            self,
            log_file_name: str,
            results_dir_path: str
    ):
        if not os.path.isdir(results_dir_path):
            os.mkdir(results_dir_path)

        time_now: datetime.datetime = datetime.datetime.now()
        # results_file_path: str = os.path.join(
        #     results_dir_path,
        #     f'{log_file_name}_results_{time_now}.txt'
        # )

        content: str = ''

        for key, execution_status in self.model_names.items():
            key_extract: str = key.split(':')[1]
            is_anaplan_unreachable: bool = Operation.UNREACHABLE in execution_status
            OPERATION_FAILED: bool = Operation.FAILED in execution_status

            if key_extract in ANP.parmeters:

                if is_anaplan_unreachable or OPERATION_FAILED:
                    execution_status += '\n'

                    display_model_operation_status: str = (
                        f'{ANP.parmeters[key_extract]} {execution_status}')
                    content += display_model_operation_status
                else:
                    continue

        results_file_path1: str = os.path.join(
            results_dir_path,
            f'{log_file_name}_results.txt'
        )

        if content:
            print(content)
            with open(results_file_path1, 'w') as f:
                # with open('../results/anplog_results.txt', 'w') as f:
                f.write(content)
            f.close()
