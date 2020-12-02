
# with open('./data/testdata.csv', 'r') as read_obj:
import csv
import numpy as np
import pandas as pd
import sys
import os

from pprint import pprint

from lxml import etree
from lxml import builder

def main():
    lenzburg = pd.read_csv('./data/testdata.csv')
    print(lenzburg.loc[0, :])
    print(lenzburg.at[0, 'Signatur'])

    E = builder.ElementMaker(
        nsmap={'xsi' : "http://www.w3.org/2001/XMLSchema-instance"}
    )
    ROOT = E.knora
    PERMISSIONS = E.permissions
    ALLOW = E.allow
    RESOURCE = E.resource
    LIST_PROP = E('list-prop')
    LIST = E.list

    document = ROOT(
        PERMISSIONS(
            ALLOW("RV", group='UnknownUser'),
            ALLOW("V", group='KnownUser'),
            id="prop-default"
        ),
        RESOURCE(
            E("list-prop",
                LIST("Tree list node 02", permissions="prop-default"),
                list="treelistroot", name=":hasListItem"
            ),
            label="obj_inst1", restype=":BlueThing", id="obj_0001", permissions="res-default"
        )   
    )   

    et = etree.ElementTree(document)
    with open('lenzburg.xml', 'wb') as f:
        et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)
    
if __name__ == "__main__":
    main()