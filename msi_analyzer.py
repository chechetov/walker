import os
from msi_analyzer_class import MSI_File
from jinja2 import Environment, FileSystemLoader

_reg_counter  = 0
_file_counter = 0
_msi_counter  = 0


def create_files_from_cfg():

    msi_files = []
    def get_lines(input_file):
        with open(input_file,'r') as f:
            for line in f:
                yield line
    msi_files = [MSI_File(line.rstrip()) for line in get_lines('filtered.txt') if line != '\n']
    return msi_files


def get_uniq_files(msi_list, how_much='ALL', debug = False):

    i = 0
    result = {}

    for msi_file in msi_list:

        global _msi_counter
        global _file_counter
        _msi_counter += 1

        if how_much != 'ALL':
            i += 1
            if i > how_much:
                break
        resp = msi_file.get_prod_id()
        seq  = (resp['ProductName'], resp['Manufacturer'])
        key = "-".join(seq)
        
        filelist = msi_file.get_table_data('File')

        try:
            result[key]
        except KeyError:
            result[key] = []


        for file in filelist:
            _file_counter += 1
            try:

                if (file['FileName'], file['FileSize'], file['Version']) not in result[key] and file['File'] not in ['s72','File']:
                    file = (file['FileName'], file['FileSize'], file['Version'])
                    result[key].append(file)
            except KeyError:
                continue

    return result

def get_uniq_paths(msi_list, how_much='ALL', debug = False):
    
     i = 0
     result = {}

     for msi_file in msi_list:

        if how_much != 'ALL':
            i += 1
            if i > how_much:
                break
        resp = msi_file.get_prod_id()
        seq  = (resp['ProductName'], resp['Manufacturer'])
        key = "-".join(seq)

        paths_and_versions = msi_file.get_path_and_version()
        
        try:
            result[key]
        except KeyError:
            result[key] = [paths_and_versions]

        if paths_and_versions not in result[key]:
            result[key].append(paths_and_versions)

     return result

def get_uniq_registry_keys(msi_list, how_much = 'ALL', debug = False):
     i = 0
     result = {}

     for msi_file in msi_list:

        if how_much != 'ALL':
            i += 1
            if i > how_much:
                break
        resp = msi_file.get_prod_id()
        seq  = (resp['ProductName'], resp['Manufacturer'])
        key = "-".join(seq)
        result[key] = []

        registry_keys = msi_file.get_table_data('Registry')
        global _reg_counter
        _reg_counter += len(registry_keys)

        for registry_key in registry_keys: 
            
            try:
                if registry_key['Root'] != '0' and 'CLASSES' not in registry_key['Key'] and (registry_key['Key'],registry_key['Value']) not in result[key] and registry_key['Name'] != 'L255':
                    registry_key = (registry_key['Key'],registry_key['Value'])
                    result[key].append(registry_key)
            except KeyError:
                continue

     return result


def create_html_report(input_data):
     env = Environment(
           loader = FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')))
     template = env.get_template('uniq_msi_files.tmpl')
     rendered = template.render(data = input_data[0], stats = input_data[1])
     
     with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'report.html'), 'w') as output_file:
         output_file.write(str(rendered))

     

if __name__ == '__main__':
    final_result = {}


    msi_files = create_files_from_cfg()
    how_many = 10

    uniq_files = get_uniq_files(msi_files, how_much=how_many)
    uniq_paths = get_uniq_paths(msi_files, how_much=how_many)
    uniq_regkeys = get_uniq_registry_keys(msi_files, how_much=how_many)


for key in uniq_paths:
    final_result[key] = {'Paths':[],
                         'Files':[],
                         'Registry':[]
                        }



    final_result[key]['Paths'] = uniq_paths[key]
    final_result[key]['Files'] = uniq_files[key]
    final_result[key]['Registry'] = uniq_regkeys[key]

stats = (_msi_counter,_reg_counter,_file_counter)


create_html_report((final_result, stats))



