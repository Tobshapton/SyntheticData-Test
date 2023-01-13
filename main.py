# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from sdv.tabular import CTGAN
from sdv.tabular import CopulaGAN
from sdv import Metadata
import sys
import getopt
# import json
# import requests
import pandas as pd
from sqlalchemy import create_engine
import warnings
import datetime
import sys

def load_testgenerator_libs():
    vip_path = r"C:\Program Files\Curiosity\Visual Integration Processor"
    lib_path = r"C:\ProgramData\VIP\lib"
    addon_path = r"C:\ProgramData\VIP\addons"
    sys.path.append(vip_path)
    sys.path.append(lib_path)
    sys.path.append(addon_path)
    import clr
    clr.addReference("Task.Automation.Common")
    clr.AddReference("TestGeneratorLib")
    clr.AddReference("VIP.Extension.SyntheticDataAI")


def get_connection_profile(host_url, api_key):
    from TestGeneratorLib.Services import ConnectionProfile
    conn_prof = ConnectionProfile()
    conn_prof.APIUrl = host_url
    conn_prof.APIKey = api_key
    return conn_prof

def check_modeller_connection(host_url, api_key):
    conn_prof = get_connection_profile(host_url, api_key)
    from TestGeneratorLib.Services.Admin import BuildInfoService
    build_info_service = BuildInfoService(conn_prof)
    build_info = build_info_service.GetAPIBuildInfo()
    print(build_info.name)
    print(build_info.version)
    print(build_info.group)
    print(build_info.artifact)
    print(str(build_info.time))

def generate_modeller_model(input_file, output_file, epochs, batch_size):
    # conn_prof = get_connection_profile(host_url, api_key)
    from VIP.Extension.SyntheticDataAI import APIHelper
    api_helper = APIHelper()
    data = api_helper.GetInfo(input_file)
    metadata = Metadata()
    print("Load CSV data to pandas.DataFrames and add tables to metadata")
    print("https://sdv.dev/SDV/user_guides/relational/relational_metadata.html")

    print("https://github.com/sdv-dev/SDV/blob/master/tests/integration/relational/test_hma.py")
    for tableDef in data:
        print("-----------------------------------------")
        print("Load data for tableDef " + tableDef.name)
        # dfTable = pd.read_sql_table(tableDef.name,
        for colDef in tableDef.columns:
            print(colDef.name)
        print("-----------------------------------------")


def generate_model(input_file, output_file, epochs, batch_size):
    warnings.filterwarnings('ignore')
    # input_file = "D:/Curiosity/Git/VIP.AI.SyntheticData/data/prod_for_model_1000.csv"
    data = pd.read_csv(input_file)
    data = data.fillna(0)
    # print("Model using CopulaGAN")
    model = CopulaGAN(epochs=epochs, batch_size=batch_size, enforce_min_max_values=True)
    # CTGAN()
    print("fit model data")
    fit_start_time = datetime.datetime.today()
    model.fit(data)
    model.save(output_file)
    difference = (datetime.datetime.today() - fit_start_time).total_seconds()
    print("Fit completed in " + str(difference) + " secs")

def generate_data(input_file, output_file, epochs, batch_size, no_of_rows):
    warnings.filterwarnings('ignore')
    print("Generate using CopulaGAN")
    # model = CopulaGAN()
    model = CopulaGAN.load(input_file)
    print(str(model.get_metadata()))
    print("generating samples")
    new_data = model.sample(no_of_rows)
    new_data.to_csv(output_file, index=False)

def main(argv):
    #get_connection_profile("https://partner.testinsights.io", "lfK7tFyOp9rlimULrsw4CJjtD")
    # check_modeller_connection("https://partner.testinsights.io", "lfK7tFyOp9rlimULrsw4CJjtD")
    #return
    debug = True
    epochs = 300
    batch_size = 500
    no_of_rows = 1000
    mode = "generate_csv"
    if len(argv) > 1:
        try:
            #opts, args = getopt.getopt(argv, "hm:i:o:e:b:n:", ["mode=", "ifile=", "ofile=", "epochs=", "batch_size=", "no_of_rows="])
            opts, args = getopt.getopt(argv, "hm:i:",
                                       ["mode=", "ifile=", "ofile=", "epochs=", "batch_size=", "no_of_rows="])
        except getopt.GetoptError:
            print('main.py -i <inputfile> -o <outputfile> -e <epochs> -b <batch_size>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('main.py -i <inputfile> -o <outputfile> -e <epochs> -b <batch_size>')
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
            elif opt in ("-m", "--mode"):
                mode = arg
            elif opt in ("-o", "--ofile"):
                outputfile = arg
            elif opt in ("-e", "--epochs"):
                epochs = int(arg)
            elif opt in ("-b", "--batch_size"):
                batch_size = int(arg)
            elif opt in ("-n", "--no_of_rows"):
                no_of_rows = int(arg)

        print('Input file is ', inputfile)
        print('Output file is ', outputfile)

    print("https://github.com/sdv-dev/SDV/blob/master/tests/integration/relational/test_hma.py")

    if mode == "model_csv":
        if debug:
            inputfile = 'C:/Github/VIP.AI.SyntheticData/data/prod_for_model_1000.csv'
            outputfile = 'C:/Github/VIP.AI.SyntheticData/model/CopulaGAN_prod_for_model_1000_2.pkl'
        generate_model(inputfile, outputfile, epochs, batch_size)
    elif mode == "model":
        load_testgenerator_libs()
        if debug:
            inputfile = r"C:\Github\VIP.AI.SyntheticData\request.xml"
            outputfile = ""
        generate_modeller_model(inputfile, outputfile, epochs, batch_size)
    else:
        if debug:
            inputfile = 'C:/Github/VIP.AI.SyntheticData/model/CopulaGAN_prod_for_model_1000_2.pkl'
            outputfile = 'C:/Github/VIP.AI.SyntheticData/generated/generated_for_model_1000.csv'
        generate_data(inputfile, outputfile, epochs, batch_size, no_of_rows)

if __name__ == "__main__":
    if len(sys.argv) > 0:
        main(sys.argv[1:])
    else:
        main(sys.argv)
