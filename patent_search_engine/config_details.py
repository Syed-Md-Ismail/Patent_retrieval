
data_tar_location = "source_data_folder"

##########################################################

"""
Solr system configuration
"""
solr_host       = "localhost"          ## Solr host address
solr_port       = "8983"               ## Solr port
solr_collection = "patent_repo"        ## Solr collection containing dataset. Can be assumed similar as a table within database

solr_fl         = "id, abstract, description, claims"    ## Fields to retrieve from query results
solr_rows       = "5"                                   ## Number of matching rows that should come out from solr

##########################################################

