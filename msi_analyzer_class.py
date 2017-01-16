from subprocess import run, PIPE

class MSI_File(object):

    """
    This is a helper class which represents msi files as an object.
    Relies on msitool.
    https://packages.debian.org/sid/utils/msitools
    """

    def __init__(self, name):

        self.name = name


    def get_table_data(self, table):

        """
        Extracts data from table. format: get_table_data('tablename')
        Returns a set of files in a form of dictionary for msi file.
        {'Header': 'Value'}
        """

        output = run(["msiinfo export '{0}' '{1}'".format(self.name, table)], shell=True, stdout=PIPE).stdout.decode('utf-8',errors='backslashreplace').splitlines()
        files = [line.split('\t') for line in output]
        res = [dict(zip(files[0], file)) for file in files[1:]]

        return res

    def get_tables(self):
        """
        Returns a list of tables in MSI file
        """

        output = run(["msiinfo tables '{0}'".format(self.name)], shell=True, stdout=PIPE).stdout.decode('utf-8',errors='backslashreplace').splitlines()
        output = [line for line in output if line]
        return output


    def get_prod_id(self):
 
        """
        Returns a dictionary {'ProductName' : 'Name', 'Manufacturer' : 'Creator'}
        Sets 'NAN' for field if absent in MSI file
 
        """

        res = {}
        keys = ['Manufacturer','ProductName']

        for data in self.get_table_data('Property'):
             if data['Property'] in keys:
                 res[data['Property']] = data['Value']

        for key in keys:
             if not key in res:
                 res[key] = 'NAN'

        return res #if res else {'ProductName': 'NAN', 'Manufacturer': 'NAN'}

    def get_version(self):
        """
        Returns string with product version
        """
        keys = ['ProductVersion']
        res = ''

        for data in self.get_table_data('Property'):
            if data['Property'] in keys:
                res = data['Value']
        return res if res else 'NAN'
        
    def get_path_and_version(self):
        return (self.name, self.get_version())
             
