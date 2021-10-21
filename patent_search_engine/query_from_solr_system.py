import pysolr

################################################################################

import config_details as config_details

################################################################################

solr_host = config_details.solr_host
solr_port = config_details.solr_port
solr_collection = config_details.solr_collection

solr_fl = config_details.solr_fl
solr_rows = config_details.solr_rows

################################################################################

## Building query to be processed in solr
solr_qt         = "select"
solr_fq         = ""
solr_url        = 'http://' + solr_host + ':' + solr_port + '/solr/' + solr_collection 




def query_string(q):
    """
    When provided with text, it finds the best matches among all the other patents
    
           
    Parameters
    ----------
    q : string
        Text that could be connected to a patent
    
    Returns
    -------
    score_list : list of dictionary
        Contains different patent description ("id, abstract, description, claims") in dictionary format 
        in each indices of the list 
    
    """
    
    ## Initialise to capture failure of any function of the pipeline
    message = "No error"
    
    solr       = pysolr.Solr(solr_url,
                             search_handler="/"+solr_qt,
                             timeout=5)
    
    
    ## Retrieves top matches for th input string 'q'
    try:
        results    = solr.search(q, **{
            'fl': solr_fl,
            'fq': solr_fq,
            'rows': solr_rows
        })
    except:
        try:
            ''' 
            Patent has odd number of backslash '/'. 
            It gives the text the appearance that the tags are opening but not closing,
            which is making solr system to give error. Adding an extra '/' will clsoe it/
            for eg: "cat sits / on a / bed / ." -> "cat sits / on a / bed / . /"
            '''
            q = str(q) + ' / '
            
            results    = solr.search(q, **{
                'fl': solr_fl,
                'fq': solr_fq,
                'rows': solr_rows
            })
        except:
            ## Below message is imporatnt and can suggest to a developer during production that solr server is down
            message = "SolrError: Patent either not available in Solr system or cannot be retrieved"
            message = q
            return 0, message
        
    
    score_list = results.docs
    return score_list, message

