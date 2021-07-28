import re
from typing import Dict
from typing import List

path_to_file: str = 'log_files/anp_user.txt'
# path_to_file: str = 'log_files/anp_user.txt'

with open(file=path_to_file, mode='r') as f:
    lines = f.readlines()
f.close()


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

    key_model_names_dict: str = ''

    EXECUTION_START: str = './AnaplanClient.sh'
    # TODO: Search for "The operation was successful."
    OPERATION_SUCCESS: str = 'The operation was successful.'
    # TODO: Search for "No dump file is available."
    DUMPFILE_NOT_AVAILABLE: str = 'No dump file is available.'
    # TODO: Search for "The operation has failed."
    OPERATION_FAILED: str = 'The operation has failed.'
    # TODO: If none of the 3 above are found, log error "Couldn't find operation log message"

    # api_status_list: List = []
    log_parse_dict: Dict = {}
    model_names: Dict = {}
    anp_parm: Dict = {
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

    W = '\033[0m'  # white (normal)
    R = '\033[31m'  # red
    G = '\033[32m'  # green
    O = '\033[33m'  # orange
    B = '\033[34m'  # blue
    P = '\033[35m'  # purple

    def constr_model_names_dict(self):

        api_status_list: List = []
        curr_api_index: int = 1
        status_api_index: int = 0
        curr_api_name: str = ''
        model_name_counter: int = 0
        for index, line in enumerate(lines):
            is_execution_start: bool = self.EXECUTION_START in line
            is_operation_success: bool = self.OPERATION_SUCCESS in line
            is_operation_fail: bool = self.OPERATION_FAILED in line
            is_operation_unavail: bool = self.DUMPFILE_NOT_AVAILABLE in line

            if is_execution_start:
                model_name_counter += 1
                self.key_model_names_dict: str = c_log_parse.parse_api_line(
                    line=line,
                    model_name_counter=model_name_counter)
                # print(c_log_parse.model_names[key_model_names_dict])
                # print(f' Print curr_api_name {curr_api_name}')
                # print(curr_api_name[-3])
                if curr_api_name[-3] == '*':
                    curr_api_name = c_log_parse.model_names[
                        self.key_model_names_dict]
                    curr_api_name += '    Anaplan Unreachable'
                    # api_status_list.append(curr_api_name)
                    c_log_parse.model_names[
                        self.key_model_names_dict] = curr_api_name

                curr_api_index = index
                status_api_index = 0

            # print(f' Length of key name {self.key_model_names_dict}')
            if (is_operation_fail or is_operation_unavail or \
                    is_operation_success):
                if len(self.key_model_names_dict) > 1:
                    status_api_index = 1
                    curr_api_name = c_log_parse.model_names[
                        self.key_model_names_dict]

            if is_operation_success:
                curr_api_name += f'    {self.OPERATION_SUCCESS}'

            if is_operation_fail:
                curr_api_name += f'    {self.OPERATION_FAILED}'
            if is_operation_unavail:
                curr_api_name += f'    {self.DUMPFILE_NOT_AVAILABLE}'

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
                c_log_parse.model_names[
                    self.key_model_names_dict] = curr_api_name

        # print((c_log_parse.model_names))

    def parse_api_line(self, line: str, model_name_counter: int) -> str:
        # print(line)
        if re.search("./AnaplanClient.sh", line):
            workspace = re.search("-workspace ", line)
            s_workspace = workspace.start()
            e_workspace = workspace.end()

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
            index_constructed = str(model_name_counter) + ':' + \
                                workspace_token + '^' + model_token
            # print(f'{index_constructed}  {process_token}')
            c_log_parse.model_names[index_constructed] = process_token
            # print(c_log_parse.model_names[index_constructed])
        return index_constructed  # c_log_parse.model_names

    def color_the_dict_output(self, log_parse_dict):
        W = '\033[0m'  # white (normal)
        R = '\033[31m'  # red
        G = '\033[32m'  # green
        O = '\033[33m'  # orange
        B = '\033[34m'  # blue
        P = '\033[35m'  # purple
        print(c_log_parse.anp_parm)
        for key, value in log_parse_dict.items():
            # print(key, value)
            is_anaplan_unreachable: bool = "Anaplan Unreachable" in value

            DUMPFILE_NOT_AVAILABLE: bool = 'No dump file is available.' in value
            # TODO: Search for "The operation has failed." in x
            OPERATION_FAILED: bool = 'The operation has failed.' in value
            OPERATION_SUCCESS: bool = 'The operation was successful.' in value

            key_extract: str = key.split(':')[1]
            # print(f' Second field of key : {key_extract}')

            if key_extract in c_log_parse.anp_parm:
                # print(c_log_parse.anp_parm[key_extract], value)
                display_model_operation_status: str = f'' \
                                                      f'{c_log_parse.anp_parm[key_extract]}   {value}'
                # print(display_model_operation_status, OPERATION_SUCCESS)
                if OPERATION_SUCCESS:
                    print(B + display_model_operation_status + W)
                if is_anaplan_unreachable:
                    #
                    print(G + display_model_operation_status + W)
                elif DUMPFILE_NOT_AVAILABLE:
                    print(P + display_model_operation_status + W)
                elif OPERATION_FAILED:
                    print(W + display_model_operation_status + W)
                else:
                    pass

    #
    # for x in api_status_list:
    #     is_anaplan_unreachable: bool = "Anaplan Unreachable" in x
    #     DUMPFILE_NOT_AVAILABLE: bool = 'No dump file is available.' in x
    #     # TODO: Search for "The operation has failed." in x
    #     OPERATION_FAILED: bool = 'The operation has failed.' in x
    #     if is_anaplan_unreachable:
    #         print(R + x + W)
    #     elif DUMPFILE_NOT_AVAILABLE:
    #         print(P + x + W)
    #     elif OPERATION_FAILED:
    #         print(B + x + W)
    #     else:
    #         # pass


def construct_model_names_dict(self) -> Dict:
    model_name_counter: int = 0
    api_status_list: List = []
    curr_api_index: int = 1
    status_api_index: int = 0
    curr_api_name: str = ''
    iterate_model_named_again: int = 0
    index_constructed: str = ''
    for index, line in enumerate(lines):
        if re.search("./AnaplanClient.sh", line):
            model_name_counter += 1
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
            index_constructed = str(model_name_counter) + '^' + \
                                workspace_token + '^' + model_token
            # print(index_constructed)
            c_log_parse.model_names[index_constructed] = process_token
            # c_log_parse.model_names[str(
            #     model_name_counter) + '^' + workspace_token + '^' +
            #                         model_token] = \
            #     process_token

        is_execution_start: bool = self.EXECUTION_START in line
        is_operation_success: bool = self.OPERATION_SUCCESS in line
        is_operation_fail: bool = self.OPERATION_FAILED in line
        is_operation_unavail: bool = self.DUMPFILE_NOT_AVAILABLE in \
                                     line
        # print(is_execution_start)

        if is_execution_start:
            # api_status_list.append('1:')
            # print(curr_api_name[-3])
            if curr_api_name[-1] == '*':
                # print('bashobi')
                curr_api_name += 'Anaplan Unreachable'
                api_status_list.append(curr_api_name)
                status_api_index = 0
                # print(line, f'    {index}')
                curr_api_index = index
                curr_api_name = process_token
                # curr_api_name = line[109:195]
        if is_operation_success:
            status_api_index = 1
            curr_api_name += f'{self.OPERATION_SUCCESS}'
        if is_operation_fail:
            status_api_index = 1
            curr_api_name += f'{self.OPERATION_FAILED}'
        if is_operation_unavail:
            status_api_index = 1
            curr_api_name += f'{self.DUMPFILE_NOT_AVAILABLE}'
        # # The API Line has no follow-up lines which have Operation Status. So,
        # only append ** at the end.
        if curr_api_index > 0 and status_api_index == 0:
            curr_api_name += '**'
            # api_status_list.append(curr_api_name)
            c_log_parse.model_names[index_constructed] = curr_api_name
            print(curr_api_name)
        # The api Line has a Operation Status. Add it to the list.
        if curr_api_index > 0 and status_api_index == 1:
            api_status_list.append(curr_api_name)
            curr_api_index = 0
            status_api_index = 0
            print(line, curr_api_name)

        W = '\033[0m'  # white (normal)
        R = '\033[31m'  # red
        G = '\033[32m'  # green
        O = '\033[33m'  # orange
        B = '\033[34m'  # blue
        P = '\033[35m'  # purple
        for x in api_status_list:
            is_anaplan_unreachable: bool = "Anaplan Unreachable" in x
            DUMPFILE_NOT_AVAILABLE: bool = 'No dump file is available.' in x
            # TODO: Search for "The operation has failed." in x
            OPERATION_FAILED: bool = 'The operation has failed.' in x
            if is_anaplan_unreachable:
                print(R + x + W)
            elif DUMPFILE_NOT_AVAILABLE:
                print(P + x + W)
            elif OPERATION_FAILED:
                print(B + x + W)
            else:
                # pass
                print(G + x + W)
    return c_log_parse.model_names


# # self.api_status_list = ['bashobi']
# def get_status_api_execution(self, line_index: int, model_counter: int) -> \
#         List:
#     return api_status_list


c_log_parse = Log_Parse(
)
# c_get_status = c_log_parse.get_status_api_execution()
c_get_status = c_log_parse.constr_model_names_dict()
c_get_status_colour = c_log_parse.color_the_dict_output(
    c_log_parse.model_names)
# c_get_status = c_log_parse.construct_model_names_dict()
# print(c_get_status)

# for key, value in c_log_parse.model_names.items():
#     print(key, value)
# key_extract: str = key.split('^')[1]
# if key_extract in c_log_parse.anp_parm:
#     print(c_log_parse.anp_parm[key_extract], value)
