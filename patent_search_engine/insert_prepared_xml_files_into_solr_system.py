import os
import subprocess
import pandas as pd

################################################################################

import config_details as config_details

################################################################################

solr_host = config_details.solr_host
solr_port = config_details.solr_port
solr_collection = config_details.solr_collection

################################################################################


def insert_folder_xml_into_solr_system(solr_xml_folder,
                                solr_host,
                                solr_port,
                                solr_collection):
    """
    Inserts all xml files within a folder into solr system
    
           
    Parameters
    ----------
    solr_xml_folder : String
        directory location for xml files
    
    solr_host : String
        Host name defined in config file
    
    solr_port : String
        Port name defined in config file
        
    solr_collection : String
        Collection name defined in config file. Can be assumed similar as a table within database
    
    Returns
    -------
    xml_insert_status_df : DataFrame
        Contains insertion success or failure status for each xml file
    
    """
    
    ## Creating variable string to be used later
    solr_host_and_port = 'http://' + str(solr_host) + ':' + str(solr_port)
    solr_system = 'solr'
    
    ## Finf all sml files within solr_xml_folder
    solr_xml_list = list(filter(lambda x: x.endswith('.xml'), 
                                            os.listdir('Data/solr/' + solr_xml_folder)))
    
    xml_insert_status_dict = {}
    counter = 0
    
    ## Iterating over each xml file. It will be loaded onto solr as a curl command
    for xml_file in solr_xml_list:
        
        counter += 1
        if(counter % 50 == 0):
            print(str(counter))
        
        ## Getting curl command ready    
        CurlUrl = 'curl ' \
                 + str(solr_host_and_port) + '/' + str(solr_system) + '/' + str(solr_collection) + '/update' \
                 + ' -H \"Content-Type: text/xml\"' \
                 + ' --data-binary @' + 'Data/solr/' + str(solr_xml_folder) + '/' + str(xml_file)
    
        
        ## Insertion happens at this step
        status, output = subprocess.getstatusoutput(CurlUrl)
        
        xml_file_status_dict = {}
        xml_file_status_dict[status] = output
        
        ## Writing insertion status of current xml file
        xml_insert_status_dict[xml_file] = xml_file_status_dict
        
    ## Converting dictionary to Dataframe for easy manipulations later
    xml_insert_status_df = pd.DataFrame(xml_insert_status_dict).T      
    
    return xml_insert_status_df



def insert_all_folders_of_xml_into_solr_system():
    """
    Inserts all folders in directory 'Data/solr/' into solr system
    
    Returns
    -------
    xml_insert_status_dict : Dictonary of dictionary
        Contains insertion success or failure status for each xml file
    
    """
    
    solr_xml_folder = 'Data/solr/'
    
    folders_of_xml_to_insert_in_solr = os.listdir(solr_xml_folder)
    
    xml_insert_status_dict = {}
    
    for solr_xml_folder in folders_of_xml_to_insert_in_solr:
        print(solr_xml_folder)
    
        xml_insert_status_df = insert_folder_xml_into_solr_system(solr_xml_folder,
                                                                  solr_host,
                                                                  solr_port,
                                                                  solr_collection)
        
        xml_insert_status_dict[solr_xml_folder] = xml_insert_status_df
    
    return xml_insert_status_dict

