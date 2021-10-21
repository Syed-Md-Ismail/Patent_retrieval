import os, tarfile

################################################################################

import config_details as config_details

################################################################################

data_tar_location = config_details.data_tar_location

###############################################################################

## Create "Data" folder if it doesn't exist. Target location of all zip folder
if not os.path.exists('Data'):
    os.makedirs('Data')



def create_list_of_tar_files_available(data_tar_location):
    """
    Finds list of all tar files available within a folder
       
    Parameters
    ----------
    data_tar_location : string
        Location of main tar file extracted. Defined in config file 
    
    Returns
    -------
    tar_file_list : list 
        list of all tar files
    
    """
    tar_file_list = []
    
    for root, dirs, files in os.walk(data_tar_location):
        for file in files:
            if file.endswith('.tgz'):
                tar_file_list.append(file)
    
    return tar_file_list




def extract_tar_file_in_list(tar_file_list, 
                             data_tar_location):
    """
    Extracts all tar file given in a list
       
    Parameters
    ----------
    tar_file_list : list
        List of tar files to be extracted
        
    data_tar_location : string
        Location of main tar file extracted. Defined in config file 

    """
    
    for file_name in tar_file_list:
        print(file_name)
        file_location = data_tar_location + '/' + file_name
        
        # open file
        file = tarfile.open(file_location)
    
        # extracting file
        folder_name = file_name.split('.tgz')[0]
        write_folder_location = 'Data/' + folder_name
        file.extractall(write_folder_location)
        
        file.close()

    return 0


def extract_all_tar_files_in_source_data_location(data_tar_location):
    """
    This function consist of two steps:
    1) Find list of all available tar folders
    2) Extract each of those tar folder
    
    Parameters
    ----------
        
    data_tar_location : string
        Location of main tar file extracted. Defined in config file 

    """

    tar_file_list = create_list_of_tar_files_available(data_tar_location)
    extract_tar_file_in_list(tar_file_list, data_tar_location)
    
    return 0
