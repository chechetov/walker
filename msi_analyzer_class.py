from subprocess import run, PIPE

class MSI_File(object):

    def __init__(self, name):

        self.name = name


    def get_table_data(self, table):

        """
        Returns a set of files in a form of dictionary for msi file.
        """

        output = run(['msiinfo export {0} {1}'.format(self.name, table)], shell=True, stdout=PIPE).stdout.decode('utf-8',errors='backslashreplace').split("\r\n")
        files = [line.split('\t') for line in output]
        res = [dict(zip(files[0], file)) for file in files[1:]]

        return res

    def get_tables(self):
        output = run(['msiinfo tables {0}'.format(self.name)], shell=True, stdout=PIPE).stdout.decode('utf-8',
                                                                                                                 errors='backslashreplace').split("\n")
        output = [line for line in output if line]
