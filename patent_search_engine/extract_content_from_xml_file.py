import os
import xmltodict
from ftfy import fix_text
import glob

################################################################################
## Section to extract different fields from source xml files
################################################################################

def find_abstract_section_text(index_dict): 
    """
    Extracts abstract_section_text from source xml file
    
           
    Parameters
    ----------
    index_dict : OrderedDict
        Contains various fields available in xml file in dictonary
    
    Returns
    -------
    abstract_section_text : string
        If there is a key 'abstract', its content is returned as text
    
    """
    abstract_section_text = ''
    section = 'abstract'
    if section in index_dict:
        abstract_dict = index_dict[section]
        
        if 'p' in abstract_dict:
            p_dict = abstract_dict['p']
            
            if '#text' in p_dict:
                abstract_section_text = p_dict['#text']    
            
    return abstract_section_text


            
def find_description_section_text(index_dict):
    """
    Extracts description_section_text from source xml file
    
           
    Parameters
    ----------
    index_dict : OrderedDict
        Contains various fields available in xml file in dictonary
    
    Returns
    -------
    description_section_text : string
        If there is a key 'description', its content is returned as text
    
    """
    description_section_text = ''
    section = 'description'
    
    if section in index_dict:
        description_dict = index_dict[section]
        
        
        if 'p' in description_dict:
            p_dict = description_dict['p']
            
            if type(p_dict) == list:
                
                for list_item in p_dict:
                    if '#text' in list_item:
                        description_section_text = description_section_text + ' ' + list_item['#text']
                
            
    return description_section_text
        


def find_claims_section_text(index_dict):
    """
    Extracts claims_section_text from source xml file
    
           
    Parameters
    ----------
    index_dict : OrderedDict
        Contains various fields available in xml file in dictonary
    
    Returns
    -------
    claims_section_text : string
        If there is a key 'claims', its content is returned as text
    
    """
    claims_section_text = ''
    section = 'claims'
    
    if section in index_dict:
        claims_dict = index_dict[section]
        
        
        if 'claim' in claims_dict:
            claim_dict_level_2 = claims_dict['claim']
            
            if type(claim_dict_level_2) == list:
                
                try:
                    for list_item in claim_dict_level_2:
                        if '#text' in list_item:
                            claims_section_text = claims_section_text + ' ' + list_item['#text']
                        
                        if 'claim-text' in list_item:
                            claim_dict_level_3 = list_item['claim-text']
                            
                            if type(claim_dict_level_3) == list:
                                for str_item in claim_dict_level_3:
                                    claims_section_text = claims_section_text + ' ' + str_item
                            else:
                                claims_section_text = claims_section_text + ' ' + claim_dict_level_3
                except:
                    pass
            
    return claims_section_text


################################################################################

def function_fix_text(string_input):
    return fix_text(string_input, 
                    remove_control_chars=True,
                    
                    fix_entities=True,
                    remove_terminal_escapes=False,
                    fix_encoding=False,
                    #fix_entities=False,
                    uncurl_quotes=False,
                    fix_latin_ligatures=False,
                    fix_character_width=False,
                    fix_line_breaks=False,
                    fix_surrogates=False,
                    remove_bom=False,
                    normalization=None,)


def create_data_string_to_write_in_xml_file(file_name,
                                            abstract_section_text,
                                            description_section_text,
                                            claims_section_text):    
    """
    Joins different portions of text as different fields of xml file
    The structure of xml file is governed by format defined by solr 
    
           
    Parameters
    ----------
    file_name : string
        Patent name
    
    abstract_section_text : string
        Text related to abstract field
    
    description_section_text : string
        Text related to description field
        
    claims_section_text : string
        Text related to claims field
    
    Returns
    -------
    xml_string : string
        Appears to carry the structure of an xml file
    
    """
    write_xml_file = ['<add>']
    write_xml_file.append('  <doc>')
    
    write_xml_file.append('    <field name="id">' + file_name  + '</field>')
    write_xml_file.append('    <field name="abstract">' + abstract_section_text  + '</field>')
    write_xml_file.append('    <field name="description">' + description_section_text  + '</field>')
    write_xml_file.append('    <field name="claims">' + claims_section_text  + '</field>')
    
    write_xml_file.append('  </doc>')
    write_xml_file.append('</add>')
    
    
    xml_string = str('\n\n'.join(write_xml_file))
    
    return xml_string
    



def write_data_string_to_xml_file(file_name,
                                  xml_string,
                                  data_folder):
    """
    Writes xml structured xml_string within directory 'Data/solr/'
    
           
    Parameters
    ----------
    file_name : string
        Name of the patent file
    
    xml_string : string
        Content to be written in xml file
    
    data_folder : string
        Folder within which xml file is to be stored
    
    """
    
    if not os.path.exists('Data/solr/' + str(data_folder)):
        os.makedirs('Data/solr/' + str(data_folder))
        
    write_file_name = 'Data/solr/' + str(data_folder) + '/' + str(file_name) + '.xml'
    with open(write_file_name, 'w', encoding='utf-8') as f:
        f.write(xml_string)
        f.close()

    return 0


def tackle_regex_pattern(to_be_cleaned_text):
    """
    Removes character from text which could break parsing, hence insertion into solr system
    
           
    Parameters
    ----------
    to_be_cleaned_text : string
        Generally one of the three sections of xml file [abstract, description, claims]
    
    Returns
    -------
    to_be_cleaned_text : string
        Generally one of the three sections of xml file [abstract, description, claims]
    
    """
    to_be_cleaned_text = to_be_cleaned_text.replace('&', '&#038;')
    to_be_cleaned_text = to_be_cleaned_text.replace('<', ' ')
    to_be_cleaned_text = to_be_cleaned_text.replace('>', ' ')
    return to_be_cleaned_text



################################################################################


def create_xml_files_ready_to_be_inserted_into_solr():
    """
    This function acts as transformation step to source data.
    It iterates through folders in 'Data' directory, 
    converts xml files in format acceptable to solr system 
    and stores them with directory 'Data/solr'.
    
    """

    ## List all fodlers to be processed
    data_folders_to_process = os.listdir('Data')
    
    if 'solr' in data_folders_to_process:
        data_folders_to_process.remove('solr')
        
    
    ## Iterate through each folder
    for data_folder in data_folders_to_process:
        print("\n\n\n" + str(data_folder))
        
        ## Find all xml files in current folder
        list_of_xml_files = glob.glob('Data/' + data_folder + "/**/*.xml", recursive = True)
        
        ## Processing each file iteratively
        for xml_file in list_of_xml_files:
            
            xml_data = open(xml_file, 'r', encoding="utf-8").read()
            xmlDict = xmltodict.parse(xml_data)
            
            
            for main_key in xmlDict:
                index_dict = xmlDict[main_key]
                
                file_name = index_dict['@file']
                file_name = file_name.split('.xml')[0]
                
                
                #######################################################################
                ''' Section extracts text for each section of xml file 
                and removes character which could break parsing, hence insertion into solr system'''
                #######################################################################
                
                abstract_section_text = find_abstract_section_text(index_dict)
                abstract_section_text = function_fix_text(abstract_section_text)
                abstract_section_text = tackle_regex_pattern(abstract_section_text)
                
                description_section_text = find_description_section_text(index_dict)
                description_section_text = function_fix_text(description_section_text)
                description_section_text = tackle_regex_pattern(description_section_text)
                
                claims_section_text = find_claims_section_text(index_dict)
                claims_section_text = function_fix_text(claims_section_text)
                claims_section_text = tackle_regex_pattern(claims_section_text)
                
                #######################################################################
                
                '''Joins different portions of text as different fields of xml file
                The structure of xml file is governed by format defined by solr '''
                xml_string = create_data_string_to_write_in_xml_file(file_name,
                                                        abstract_section_text,
                                                        description_section_text,
                                                        claims_section_text)
                
                ## Saves xml string within 'Data/solr/data_folder'
                write_data_string_to_xml_file(file_name,
                                              xml_string,
                                              data_folder)

    return 0
