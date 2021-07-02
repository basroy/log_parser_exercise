import os
import re

basedir = os.path.abspath(os.path.dirname(__file__))
print('path returned is ' + basedir)
remote = os.getcwd() == '/home/basroy/scripts/python'
local_path = 'C:\\Users\\basroy\\projects\\mentoring'
remote_path = '/home/basroy/data'
path = remote_path if remote else local_path

logfile = 'anp_user.txt'
regex = '(<property name="(.*?)">(.*?)<\/property>)'
match_list = []
read_line = True

api_name: str = ''
oper_succ_line: str = ''
oper_action_line: str = ''
oper_fail_line: str = ''

with open(os.path.join(local_path, logfile), "r") as file:
    # with open(r'''C:\Users\basroy\projects\mentoring\anp_user.txt''') as file:
    match_list = []
    if read_line == True:
        for line in file:
            for match in re.finditer(regex, line, re.S):
                match_text = match.group()
                match_list.append(match_text)
                # print(match_text)

            x = re.search("./AnaplanClient.sh", line)
            y = "0" if x is None else x
            # print(line)
            # https://www.dataquest.io/blog/regular-expressions-data-scientists/
            #
            # https://github.com/glenjarvis/talk-yaml-json-xml-oh-my
            #
            # https://pythonicways.wordpress.com/2016/12/20/log-file-parsing-in-python/
            #
            # https://opensource.com/article/19/5/log-data-apache-spark
            # https://blog.red-badger.com/2013/11/08/getting-started-with-elasticsearch
            #
            if y == x:
                # print(line)
                api_name = line
                print(api_name)
            model_name = r'('
            oper = re.search("The operation was successful", line)
            oper_succ = "0" if oper is None else oper
            oper_succ_line = line

            oper = re.search("No dump file is available", line)
            oper_action = "0" if oper is None else oper
            oper_action_line = line

            oper = re.search("The operation has failed", line)
            oper_fail = "0" if oper is None else oper
            oper_fail_line = line

            if oper_succ or oper_fail or oper_action:
                # print('VALIDATE' + line)
                x: str = 'VALIDATED' + oper_succ_line or oper_action_line or \
                         oper_fail_line

                oper_fail = None
                oper_action = None
                oper_succ = None


    else:
        print('Anaplan unreachable for ' + api_name)

data = f.read()
for match in re.finditer(regex, data, re.S):
    match_text = match.group()
    match_list.append(match_text)
file.close()
