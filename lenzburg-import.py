
# with open('./data/testdata.csv', 'r') as read_obj:
import csv
import numpy as np
import pandas as pd
import sys
import os

from pprint import pprint

from lxml import etree
from lxml.builder import E


def make_root(shortcode, default_ontology):
    root = etree.Element("knora", nsmap={'xsi': "http://www.w3.org/2001/XMLSchema-instance"})
    root.set("shortcode", shortcode)
    root.set("default-ontology", default_ontology)
    return root


# noinspection PyPep8Naming
def append_permissions(root_element: etree.Element):
    PERMISSIONS = E.permissions
    ALLOW = E.allow

    res_default = PERMISSIONS(id="res-default")
    res_default.append(ALLOW("RV", group='UnknownUser'))
    res_default.append(ALLOW("V", group='KnownUser'))
    res_default.append(ALLOW("CR", group='Creator'))
    res_default.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(res_default)

    res_restricted = PERMISSIONS(id="res-restricted")
    res_restricted.append(ALLOW("V", group='KnownUser'))
    res_restricted.append(ALLOW("CR", group='Creator'))
    res_restricted.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(res_restricted)

    prop_default = PERMISSIONS(id="prop-default")
    prop_default.append(ALLOW("V", group='UnknownUser'))
    prop_default.append(ALLOW("V", group='KnownUser'))
    prop_default.append(ALLOW("CR", group='Creator'))
    prop_default.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(prop_default)

    prop_restricted = PERMISSIONS(id="prop-restricted")
    prop_restricted.append(ALLOW("V", group='KnownUser'))
    prop_restricted.append(ALLOW("CR", group='Creator'))
    prop_restricted.append(ALLOW("CR", group='ProjectAdmin'))
    root_element.append(prop_restricted)

    return root_element


# noinspection PyPep8Naming
def make_boolean_prop(name, value, permissions="prop-default") -> etree.Element:
    prop_ = etree.Element("boolean-prop", name=name)
    value_ = etree.Element("boolean", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_color_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("color-prop", name=name)
    value_ = etree.Element("color", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_date_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("date-prop", name=name)
    value_ = etree.Element("date", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_geometry_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("geometry-prop", name=name)
    value_ = etree.Element("geometry", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_geoname_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("geoname-prop", name=name)
    value_ = etree.Element("geoname", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_resptr_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("resptr-prop", name=name)
    value_ = etree.Element("resptr", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_interval_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("interval-prop", name=name)
    value_ = etree.Element("interval", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_list_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("list-prop", name=name)
    value_ = etree.Element("list", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_text_prop(name, value, permissions="prop-default", encoding="utf8"):
    prop_ = etree.Element("text-prop", name=name)
    value_ = etree.Element("text", permissions=permissions, encoding=encoding)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_uri_prop(name, value, permissions="prop-default"):
    prop_ = etree.Element("uri-prop", name=name)
    value_ = etree.Element("uri", permissions=permissions)
    value_.text = value
    prop_.append(value_)
    return prop_


# noinspection PyPep8Naming
def make_resource(label, restype, id, permissions="res-default") -> etree.Element:
    resource_ = etree.Element("resource", label=label, restype=restype, id=id, permissions=permissions)
    return resource_


def main():
    lenzburg = pd.read_csv('./data/testdata.csv')
    print(lenzburg.loc[0, :])
    print(lenzburg.at[0, 'Signatur'])

    root = make_root("0000", "flsgv")
    root = append_permissions(root)

    # loop start
    # fill in loop

    for index, row in lenzburg.iterrows():
        song = make_resource(row['Signatur'], ":Song", "obj_"+str(index), "res-default")
        song.append(make_text_prop(":hasSignature", row['Signatur']))
        song.append(make_boolean_prop(":hasBoolean", "true"))
        root.append(song)

        composer = make_resource(row['Signatur'], ":Komponist", "obj_" + str(index), "res-default")
        composer.append(make_text_prop(":hasSignature", row['Signatur']))
        composer.append(make_boolean_prop(":hasBoolean", "true"))
        root.append(composer)

        songwriter = make_resource(row['Signatur'], ":Texter", "obj_" + str(index), "res-default")
        songwriter.append(make_text_prop(":hasSignature", row['Signatur']))
        songwriter.append(make_boolean_prop(":hasBoolean", "true"))
        root.append(songwriter)

        interpreter = make_resource(row['Signatur'], ":Interpret", "obj_" + str(index), "res-default")
        interpreter.append(make_text_prop(":hasSignature", row['Signatur']))
        interpreter.append(make_boolean_prop(":hasBoolean", "true"))
        root.append(interpreter)

    # loop end

    document = root

    et = etree.ElementTree(document)
    with open('lenzburg.xml', 'wb') as f:
        et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)


if __name__ == "__main__":
    main()
