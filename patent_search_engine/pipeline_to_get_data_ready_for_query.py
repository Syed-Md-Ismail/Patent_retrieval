
"""
After running this script, we will be ready to search for matching patents.
It achieves it over three steps

1) Extract data from all tar files and saves xml files in a directory called 'Data'
2) Transform xml files in a format defined in solr schema
3) Load transformed xml files into solr system

"""
# =============================================================================
# Importing all functions. 
# They are available in files under same folder structure as this file.
# =============================================================================

from unzip_tar_file import extract_all_tar_files_in_source_data_location 
from extract_content_from_xml_file import create_xml_files_ready_to_be_inserted_into_solr
from insert_prepared_xml_files_into_solr_system import insert_all_folders_of_xml_into_solr_system

import config_details as config_details

################################################################################

data_tar_location = config_details.data_tar_location

################################################################################

print("extract_all_tar_files_in_source_data_location")
extract_all_tar_files_in_source_data_location(data_tar_location)

print("create_xml_files_ready_to_be_inserted_into_solr")
create_xml_files_ready_to_be_inserted_into_solr()

print("insert_all_folders_of_xml_into_solr_system")
insert_all_folders_of_xml_into_solr_system()
