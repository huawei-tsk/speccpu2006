#!/usr/bin/env python
import re
import string
import operator
import json
import yaml
from caliper.server.parser_process import parser_log
#                 Base     Base       Base        Peak     Peak       Peak
# Benchmarks      Ref.   Run Time     Ratio       Ref.   Run Time     Ratio
# -------------- ------  ---------  ---------    ------  ---------  ---------
# 400.perlbench    9770     285          34.3 *    9770     259          37.7 S
# 400.perlbench    9770     285          34.2 S    9770     259          37.7 *
# 400.perlbench    9770     285          34.3 S    9770     260          37.6 S
# 401.bzip2        9650     458          21.1 *    9650     449          21.5 S
# 401.bzip2        9650     456          21.2 S    9650     449          21.5 *
# 401.bzip2        9650     459          21.0 S    9650     449          21.5 S
# 403.gcc          8050     241          33.4 S    8050     240          33.5 S
# 403.gcc          8050     241          33.4 *    8050     243          33.2 S
# 403.gcc          8050     240          33.5 S    8050     241          33.4 *
# 429.mcf          9120     162          56.4 *    9120     160          56.9 S
# 429.mcf          9120     163          56.0 S    9120     161          56.8 *
# 429.mcf          9120     161          56.5 S    9120     161          56.5 S
# 445.gobmk       10490     412          25.5 S   10490     425          24.7 S
# 445.gobmk       10490     412          25.5 *   10490     425          24.7 S
# 445.gobmk       10490     412          25.4 S   10490     425          24.7 *
# 456.hmmer        9330     131          71.1 S    9330     135          69.3 *
# 456.hmmer        9330     131          71.2 *    9330     135          69.1 S
# 456.hmmer        9330     131          71.3 S    9330     135          69.3 S
# 458.sjeng       12100     422          28.7 S   12100     410          29.5 *
# 458.sjeng       12100     422          28.6 S   12100     410          29.5 S
# 458.sjeng       12100     422          28.6 *   12100     410          29.5 S
# 462.libquantum  20720       3.47     5980   S   20720       3.47     5980   S
# 462.libquantum  20720       3.46     5990   S   20720       3.46     5990   S
# 462.libquantum  20720       3.46     5980   *   20720       3.46     5980   *
# 464.h264ref     22130     455          48.6 S   22130     455          48.6 S
# 464.h264ref     22130     453          48.8 *   22130     453          48.8 *
# 464.h264ref     22130     453          48.9 S   22130     453          48.9 S
# 471.omnetpp      6250     170          36.8 S    6250     129          48.5 *
# 471.omnetpp      6250     172          36.3 S    6250     129          48.6 S
# 471.omnetpp      6250     172          36.4 *    6250     129          48.4 S
# 473.astar        7020     235          29.8 S    7020     237          29.6 S
# 473.astar        7020     237          29.7 S    7020     237          29.6 *
# 473.astar        7020     236          29.7 *    7020     237          29.6 S
# 483.xalancbmk    6900     109          63.6 S    6900      99.9        69.1 *
# 483.xalancbmk    6900     109          63.0 S    6900     100          69.0 S
# 483.xalancbmk    6900     109          63.4 *    6900      99.5        69.3 S
# ==============================================================================
# 400.perlbench    9770     285          34.3 *    9770     259          37.7 *
# 401.bzip2        9650     458          21.1 *    9650     449          21.5 *
# 403.gcc          8050     241          33.4 *    8050     241          33.4 *
# 429.mcf          9120     162          56.4 *    9120     161          56.8 *
# 445.gobmk       10490     412          25.5 *   10490     425          24.7 *
# 456.hmmer        9330     131          71.2 *    9330     135          69.3 *
# 458.sjeng       12100     422          28.6 *   12100     410          29.5 *
# 462.libquantum  20720       3.46     5980   *   20720       3.46     5980   *
# 464.h264ref     22130     453          48.8 *   22130     453          48.8 *
# 471.omnetpp      6250     172          36.4 *    6250     129          48.5 *
# 473.astar        7020     236          29.7 *    7020     237          29.6 *
# 483.xalancbmk    6900     109          63.4 *    6900      99.9        69.1 *
#  SPECint(R)_base2006                   57.9
#  SPECint2006                                                           60.1

def speccpu_parser(content, outfp):
    seperators = ['base_ref', 'base_run_time', 'base_ratio', 'peak_ref', 'peak_run_time', 'peak_ratio']
    contents = content.split("==============================================================================")

    dic = {}
    dic['400.perlbench'] = {}
    dic['401.bzip2'] = {}
    dic['403.gcc'] = {}
    dic['429.mcf'] = {}
    dic['445.gobmk'] = {}
    dic['456.hmmer'] = {}
    dic['458.sjeng'] = {}
    dic['462.libquantum'] = {}
    dic['464.h264ref'] = {}
    dic['471.omnetpp'] = {}
    dic['473.astar'] = {}
    dic['483.xalancbmk'] = {}

    for key in dic.keys():
        for i in range(len(seperators)):
            value_list = re.findall(key + r'(.*)', contents[1])[0].split(' ')
            value_list2 = []
            for value in value_list:
                if value != '' and value != '*':
                    value_list2.append(value)
            dic[key][seperators[i]] = value_list2[i]
    outfp.write(yaml.dump(dic, default_flow_style=False))
    outfp.close()
    return dic

def speccpu(filePath, outfp):
    cases = parser_log.parseData(filePath)
    result = []
    for case in cases:
        caseDict = {}
        caseDict[parser_log.BOTTOM] = parser_log.getBottom(case)
        titleGroup = re.search('(\s+Base\s+Base\s+Base\s+Peak\s+Peak\s+Peak\nBenchmarks\s+Ref\.\s+Run Time\s+Ratio\s+Ref\.\s+Run Time\s+Ratio)', case)
        if titleGroup != None:
            caseDict[parser_log.TOP] = titleGroup.group(0)
            caseDict[parser_log.BOTTOM] = parser_log.getBottom(case)
        tables = []
        tableContent = {}
        tableContent[parser_log.CENTER_TOP] = ''
        # tableGroup = re.search("(.*)SPECint\(", case)
        tableGroup = re.search(r'=======([\s\S]+)SPECint\(R\)_base2006', case)
        if tableGroup is not None:
            tableGroupContent_temp = tableGroup.groups()[0]
            table = parser_log.parseTable(tableGroupContent_temp, ":{1,}")
            tableContent[parser_log.I_TABLE] = table
        tables.append(tableContent)
        caseDict[parser_log.TABLES] = tables
        result.append(caseDict)
    outfp.write(json.dumps(result))
    return result

if __name__ == "__main__":
    infp = open("cpu2006-20160725-42998.txt", "r")
    content = infp.read()
    outfp = open("2.txt", "a+")
    # for data in content:
    #     print data
    a = speccpu_parser(content, outfp)
        #print a

    outfp.close()
    infp.close()
    infile = "cpu2006-20160725-42998.txt"
    outfile = "cpu2006.json"
    outfp = open(outfile, "a+")
    speccpu(infile, outfp)
    outfp.close()
