#!usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: Jon Zhang
@contact: zj.fly100@gmail.com
@site:
@version: 1.0
@license:
@file: edit_config.py
@time: 2017/3/14 21:12
Edit Config
    1.show the config
    2.add the configuration information to the SPfile
    3.del the configuration information from the SPfile
"""
import json
import os

def toShowConfig(oneTitle,oneConfigFile):
    showConfigAsList = []
    oneFlag = 0
    with open(oneConfigFile) as readHaConfigFile:
        for i in readHaConfigFile:
            if oneTitle == "backend \n":
                showConfigAsList.append(i)
            if i == oneTitle:
                oneFlag += 1
                continue
            if oneFlag and i.startswith("backend"):
                break
            if oneFlag and i:
                showConfigAsList.append(i)
        return showConfigAsList

def addConf(input_dict,haconfig_path,haconfig_path_tmp,haconfig_path_bak,backend_title,result_list, record_conf):
    writeOldConfigFlag = 1
    writeNewConfigFlag = 1
    # backend = input_dict["backend"]
    # backend_title = "backend %s\n" % backend
    # result_list = toShowConfig(backend_title,haconfig_path)
    # record_conf = "        server %s %s weight %s maxconn %s\n" % (input_dict['record']['server'], input_dict['record']['server'], input_dict['record']['weight'],input_dict['record']['maxconn'])
    if not result_list:                                 # add new title and configuration information
        with open(haconfig_path) as readConfigFile ,open(haconfig_path_tmp,'w') as writeConfigFileTmp:
            for i in readConfigFile:
                writeConfigFileTmp.write(i)
            writeConfigFileTmp.write('\n')
            writeConfigFileTmp.write(backend_title)
            writeConfigFileTmp.write(record_conf)
    elif record_conf in result_list:                      # title and configuration information are in old config-file
        # with open(haconfig_path) as readConfigFile, open(haconfig_path_tmp, 'w') as writeConfigFileTmp:
        #     for i in readConfigFile:
        #         writeConfigFileTmp.write(i)                # only backup the file
        print("No update")
        return "No update"
    else:
        with open(haconfig_path) as readConfigFile, open(haconfig_path_tmp, 'w') as writeConfigFileTmp:
            for i in readConfigFile:
                if writeOldConfigFlag:
                    writeConfigFileTmp.write(i)
                if i == backend_title:
                    writeOldConfigFlag -= 1
                    continue
                if not writeOldConfigFlag:
                    if len(i.strip()) != 0:
                        writeConfigFileTmp.write(i)
                    else:
                        writeConfigFileTmp.write(record_conf) # only title ,add the first configuration information
                        writeNewConfigFlag -= 1
                        writeConfigFileTmp.write(i)
                if not writeOldConfigFlag and i.startswith("backend"):
                    writeOldConfigFlag += 1
            if writeNewConfigFlag:      # the configuration information will been added at the end of the file
                writeConfigFileTmp.write(record_conf)
    if os.path.isfile(haconfig_path_bak):
        os.remove(haconfig_path_bak)
        os.renames(haconfig_path, haconfig_path_bak)
    else:
        os.renames(haconfig_path,haconfig_path_bak)
    os.renames(haconfig_path_tmp, haconfig_path)

def del_conf(input_dict,haconfig_path,haconfig_path_tmp,haconfig_path_bak,backend_title,result_list, record_conf):
    writeOldConfigFlag = 1
    # backend = input_dict['backend']
    # backend_title = "backend %s\n"%backend
    # result_list = toShowConfig(backend_list,haconfig_path)
    # restord_conf = "        server %s %s weight %s maxconn %s\n" % (input_dict['record']['server'], input_dict['record']['server'], input_dict['record']['weight'],input_dict['record']['maxconn'])
    if not result_list:
        print("There is not title match!")
        return "Not match title"
    elif record_conf in result_list:
        result_list.remove(record_conf)
        with open(haconfig_path) as readConfigFile,open(haconfig_path_tmp,'w') as writeConfigFileTmp:
            for i in readConfigFile:
                if writeOldConfigFlag:
                    writeConfigFileTmp.write(i)
                if writeOldConfigFlag and i == backend_title:
                    writeOldConfigFlag -= 1
                    for j in result_list:
                        writeConfigFileTmp.write(j)
                        writeConfigFileTmp.write('\n')
                    continue
                if not writeOldConfigFlag and i.startswith("backend"):
                    writeConfigFileTmp.write(i)
                    writeOldConfigFlag += 1
    else:
        print("There is not record match!")
        return "Not match record"
    if os.path.isfile(haconfig_path_bak):
        os.remove(haconfig_path_bak)
        os.renames(haconfig_path, haconfig_path_bak)
    else:
        os.renames(haconfig_path,haconfig_path_bak)
    os.renames(haconfig_path_tmp, haconfig_path)

def getConf(input_dict,haconfig_path):
    backend = input_dict['backend']
    backend_title = "backend %s\n" % backend
    result_list = toShowConfig(backend_title, haconfig_path)
    restord_conf = "        server %s %s weight %s maxconn %s\n" % (input_dict['record']['server'], input_dict['record']['server'], input_dict['record']['weight'],input_dict['record']['maxconn'])
    return (backend_title,result_list,restord_conf)

def main(haconfig_path,haconfig_path_tmp,haconfig_path_bak):
    while True:
        print("""
            1.Show the config
            2.Add the config
            3.Del the config
        """)
        input_id = input("Please choose one id :")
        if input_id == '1':
            inputBackendTitle = input("Please input backend-title:")
            backendTitle = "backend %s\n" % inputBackendTitle
            showConfig = toShowConfig(backendTitle, haConfigFile)
            if backendTitle != "backend \n":
                showConfig.insert(0,backendTitle)
            for i in showConfig:
                print(i,end='')
        elif input_id == '2':
            inputBackendTitleAndRecordToAdd = input("Please input backend-dict:")
            input_dict = json.loads(inputBackendTitleAndRecordToAdd)
            backend_title,result_list, restord_conf = getConf(input_dict,haconfig_path)
            addConf(input_dict,haConfigFile,haconfig_path_tmp,haconfig_path_bak,backend_title,result_list, restord_conf)
        elif input_id == '3':
            input_str = input("Please input backend-dict:")
            input_dict = json.loads(input_str)
            backend_title,result_list, restord_conf = getConf(input_dict, haconfig_path)
            del_conf(input_dict,haConfigFile,haconfig_path_tmp,haconfig_path_bak,backend_title,result_list, restord_conf)

if __name__ =="__main__":
    haConfigFile = "haconfig.txt"
    haConfigFileBak = "haconfig_bak.txt"
    haConfigFileTmp = "haconfig_tmp.txt"
    main(haConfigFile,haConfigFileTmp,haConfigFileBak)