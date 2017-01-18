#! /usr/bin/python3.5

import os
from ast import literal_eval
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, create_engine
from sqlalchemy.orm import mapper

db = create_engine('sqlite:///output.db/', echo=False)
metadata = MetaData(db)

package_table = Table('Package', metadata,
                Column('id',Integer,primary_key=True),
                Column('ProductName',String),
                Column('Manufacturer',String)
                )

package_version_table = Table('PackageVersion', metadata,
                        Column('id',Integer,primary_key=True),
                        Column('pid', ForeignKey("Package.id")),
                        Column('version', String))

package_version_path_table = Table('PackageVersionPath',metadata,
                             Column('id',Integer,primary_key=True),
                             Column('pvid',Integer,ForeignKey("PackageVersion.id")),
                             Column('path',String))

package_version_file_table = Table('PackageVersionFile', metadata,
                             Column('id',Integer,primary_key=True),
                             Column('pvid',Integer,ForeignKey("PackageVersion.id")),
                             Column('name',String))

package_version_registry_entry = Table('PackageRegistryEntry',metadata,
                             Column('id',Integer,primary_key=True),
                             Column('pvid',Integer,ForeignKey("PackageVersion.id")),
                             Column('root',String),
                             Column('key', String),
                             Column('value',String),
                             Column('data',String))

metadata.create_all(db)


with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'output-test.txt'),'r') as input_file:
    global res
    res = input_file.read()

res = literal_eval(res)

for key in res:
    package_table.insert().execute({'ProductName':  key.split("-")[0],
               'Manufacturer': key.split("-")[1]
              })
    package_version_table.insert().execute({
                                          'pid': 'Package.id',
                                          'version' : "111"
                                          })    
     

s = package_table.select()
rs = s.execute()
row = rs.fetchone()

print(row)



