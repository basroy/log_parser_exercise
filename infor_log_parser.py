import re,os
from typing import Dict
source_table_load: Dict = {}
target_table_load: Dict={}
source_row_count: Dict = {
    "Output Rows": 0,
    "Affected Rows": 0,
    "Rejected Rows": 0,
}
target_row_count: Dict = {
    "Output Rows": 0,
    "Affected Rows": 0,
    "Rejected Rows": 0,
}
source_output_count = []
source_affected_count = []
source_rejected_count = []
target_output_count = []
target_affected_count = []
target_rejected_count = []
counts = []
file = open('C:\\Users\\risraj2\\OneDrive - Enquero\\Desktop\\Session log files\\m_P_XXANP_ARCH_GOAL_REPORT_ACV.log.bin', encoding='utf-8', errors='ignore')
infile = file.read()

#picking the session name
for p in re.finditer("Initializing session",infile):
        session = infile[p.end() + 1:].split(']')[0].split('[')[1]
        print('session name: ',session)
        break
for n in re.finditer('SESSION LOAD SUMMARY',infile):
    f = infile[n.end() + 1:]
    # picking only source data set
    for m in re.finditer('Source Load Summary',f):
        x = f[m.end() + 1:].split('Target Load Summary')[0]
        for o in re.finditer("Instance Name:", x):
            #table_name = x[o.end()+1:].split(']')[0]
            #output_rows = x[o.end()+1:].split('Output Rows [')[1].split(']')[0]
            #affected_rows = x[o.end()+1:].split('Affected Rows [')[1].split(']')[0]
            #rejected_rows = x[o.end()+1:].split('Rejected Rows [')[1].split(']')[0]
            #source_row_count["Output Rows"] = output_rows
            output_count = x[o.end()+1:].split('Output Rows [')[1].split(']')[0]
            source_output_count.append(output_count)
            affected_count =x[o.end()+1:].split('Affected Rows [')[1].split(']')[0]
            source_affected_count.append(affected_count)
            rejected_count =x[o.end()+1:].split('Rejected Rows [')[1].split(']')[0]
            source_rejected_count.append(rejected_count)
            #source_row_count["Affected Rows"] = affected_rows
            #source_row_count["Rejected Rows"] = rejected_rows
            #source_table_load[table_name] = source_row_count
            #print(source_row_count)
    #print(source_rejected_count,source_affected_count, source_output_count)
    #print(source_row_count)
    #print(source_table_load)
    #picking only target data set
    for m in re.finditer('Target Load Summary',f):
        x = f[m.end() + 1:].split('QSession ')[0]
        for o in re.finditer("Instance Name:", x):
            #table_name = x[o.end()+1:].split(']')[0]
            #output_rows = x[o.end()+1:].split('Output Rows [')[1].split(']')[0]
            #affected_rows = x[o.end()+1:].split('Affected Rows [')[1].split(']')[0]
            #target_row_count["Output Rows"] = output_rows
            #target_row_count["Affected Rows"] = affected_rows
            #target_row_count["Rejected Rows"] = rejected_rows
            #target_table_load[table_name] = target_row_count
            output_count = x[o.end()+1:].split('Output Rows [')[1].split(']')[0]
            target_output_count.append(output_count)
            affected_count =x[o.end()+1:].split('Affected Rows [')[1].split(']')[0]
            target_affected_count.append(affected_count)
            rejected_count =x[o.end()+1:].split('Rejected Rows [')[1].split(']')[0]
            target_rejected_count.append(rejected_count)
    #print(target_rejected_count, target_affected_count, target_output_count)
    #print(target_table_load)

    #for merging the two dictionaries
    #source_table_load.update(target_table_load)
    #print(source_table_load)
    #print(target_row_count)
    #print(source_row_count)
    if source_output_count == target_output_count and source_affected_count == target_affected_count and source_rejected_count == target_rejected_count:
        print('Source and Target counts Matching')
    else :
        if source_output_count != target_output_count:
            print('Source output counts and Target output counts are not matching')
        if source_affected_count != target_affected_count:
            print('Source affected counts and Target affected counts are not matching')
        if source_rejected_count != target_rejected_count:
            print('Source rejected counts and Target rejected counts are not matching')
