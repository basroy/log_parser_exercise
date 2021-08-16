import os
import re


class Colors:
    WHITE = '\033[0m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    ORANGE = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'


class Regex:
    initialization = "Initializing session "
    session_load = "SESSION LOAD SUMMARY"
    source_load = "Source Load Summary"
    target_load = "Target Load Summary"
    table_name = "Instance Name:"
    p_id = "Process id"
    shell_failed = "The shell command failed"
    standard_error = "Standard output and error:"
    error = "denied"


class Source_Target_match:
    tot_sr_out = 0;
    tot_sr_aff = 0;
    tot_sr_app = 0;
    tot_sr_rej = 0
    tot_tar_out = 0;
    tot_tar_aff = 0;
    tot_tar_app = 0;
    tot_tar_rej = 0
    all_matching = tot_sr_out == tot_tar_out and tot_sr_aff == tot_tar_aff and tot_sr_app == tot_tar_app
    out_mismatch = tot_sr_out != tot_tar_out and tot_sr_aff == tot_tar_aff and tot_sr_app == tot_tar_app
    aff_mismatch = tot_sr_out == tot_tar_out and tot_sr_aff != tot_tar_aff and tot_sr_app == tot_tar_app
    app_mismatch = tot_sr_out == tot_tar_out and tot_sr_aff == tot_tar_aff and tot_sr_app != tot_tar_app


path_to_informat_log: str = 'anp_informat_logs'
subfiles = []
for dirpath, subdirs, files in os.walk(path_to_informat_log):
    for x in files:
        if x.endswith(".bin"):
            subfiles.append(os.path.join(dirpath, x))

# for file in subfiles:
#     with open(file=file, mode='r', encoding='utf-8', errors='ignore') as f:
#         lines = f.readlines()
#     f.close()
#     print(f'{Colors.RED} LOG FILE BEING PROCESRED IS {file}{Colors.GREEN}')
#
# path_to_file: str = 'anp_informat_logs\s_m_P_FF_TO_ANAPLAN_SAV_SITE_GEO_ACCT.log.4.bin'
#
# file = open(
#     file=path_to_file,
#     encoding='utf-8', errors='ignore')

for list_file in subfiles:
    file = open(
        file=list_file,
        encoding='utf-8', errors='ignore')

    infile = file.read()
    for initialization_session_expr in \
            re.finditer(Regex.initialization, infile):
        # print(p)
        session = infile[initialization_session_expr.end() +
                         1:].split(']')[0]  # .split('[')[1]
        print(Colors.GREEN + 'session name: ', list_file, '   -->', session
              + Colors.WHITE)
        break

    # file.close()
    initialization_flag: bool = Regex.initialization in infile

    print(initialization_flag)
    # for p in re.finditer(initialization, lines):
    #     print(p)
    #     session = lines[p.end() + 1:].split(']')[0]  # .split('[')[1]
    #     print(G + 'session name: ', session)
    #     break
    for n in re.finditer(Regex.session_load, infile):
        f = infile[n.end() + 1:]
        #     # picking only source data set
        for m in re.finditer(Regex.source_load, f):
            x = f[m.end() + 1:].split(Regex.target_load)[0]
            for o in re.finditer(Regex.table_name, x):
                out_count = \
                    x[o.end() + 1:].split('Output Rows [')[1].split(']')[0]
                Source_Target_match.tot_sr_out += int(out_count)
                Source_Target_match.aff_count = \
                    x[o.end() + 1:].split('Affected Rows [')[1].split(']')[
                        0]
                Source_Target_match.tot_sr_aff += int(
                    Source_Target_match.aff_count
                )
                Source_Target_match.app_count = \
                    x[o.end() + 1:].split('Applied Rows [')[1].split(']')[
                        0]
                Source_Target_match.tot_sr_app += int(
                    Source_Target_match.app_count)
                Source_Target_match.rej_count = \
                    x[o.end() + 1:].split('Rejected Rows [')[1].split(']')[
                        0]
                Source_Target_match.tot_sr_rej += int(
                    Source_Target_match.rej_count)
        #     # picking only target data set
        for m in re.finditer(Regex.target_load, f):
            x = f[m.end() + 1:].split('QSession ')[0]
            for o in re.finditer(Regex.table_name, x):
                Source_Target_match.out_count = \
                    x[o.end() + 1:].split('Output Rows [')[1].split(']')[0]
                Source_Target_match.tot_tar_out += int(
                    Source_Target_match.out_count)
                Source_Target_match.aff_count = \
                    x[o.end() + 1:].split('Affected Rows [')[1].split(']')[
                        0]
                Source_Target_match.tot_tar_aff += int(
                    Source_Target_match.aff_count)
                Source_Target_match.app_count = \
                    x[o.end() + 1:].split('Applied Rows [')[1].split(']')[
                        0]
                Source_Target_match.tot_tar_app += int(
                    Source_Target_match.app_count)
                Source_Target_match.rej_count = \
                    x[o.end() + 1:].split('Rejected Rows [')[1].split(']')[
                        0]
                Source_Target_match.tot_tar_rej += int(
                    Source_Target_match.rej_count)
        if (Source_Target_match.tot_tar_rej != 0):
            print(Source_Target_match.tot_tar_rej,
                  ' : These are the rejected rows at the targte side')
        a: bool = Source_Target_match.all_matching
        b: bool = Source_Target_match.out_mismatch
        c: bool = Source_Target_match.aff_mismatch
        d: bool = Source_Target_match.app_mismatch
        e: bool = Source_Target_match.tot_tar_rej == 0

        if a and e:
            print(Colors.GREEN + 'Source and Target counts are matching')
        if b and e:
            print(Colors.RED + 'Source and Target Output counts are not '
                               'matching')
        if c and e:
            print(Colors.RED + 'Source and Target Affected counts are not '
                               'matching')
        if d and e:
            print(Colors.RED + 'Source and Target Applied counts are not '
                               'matching')
    # # getting faulty process id status and errors
    # print(B + "Faulty", p_id)
    # for m in re.finditer(p_id, infile):
    #     process = infile[m.end() + 1:].split('.')
    #     a: bool = shell_failed in process[1]
    #     if a:
    #         for n in re.finditer(standard_error, infile):
    #             z = infile[m.end() + 1:].split('bin/')
    #             err = z[1].split('PRE-SESS')
    #             b: bool = error in err[0]  # Can be removed
    #         if b:
    #             print(B + process[0], process[1], R + err[0])
