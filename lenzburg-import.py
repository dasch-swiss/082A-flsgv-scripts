
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
def make_list_prop(list_name, prop_name, values, permissions="prop-default"):
    prop_ = etree.Element("list-prop", list=list_name, name=prop_name)

    for val in values:
        value_ = etree.Element("list", permissions=permissions)
        value_.text = val
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

    root = make_root("082A", "flsgv")
    root = append_permissions(root)

    # loop start
    # fill in loop

    for index, row in lenzburg.iterrows():
        song = make_resource(row['Signatur'], ":Song", "song_obj_"+str(index), "res-default")
        if pd.notna(row['Signatur']):
            song.append(make_text_prop(":hasIdentifier", row['Signatur']))

        if pd.notna(row['Incipit']):
            song.append(make_text_prop(":hasIncipit", row['Incipit']))

        if pd.notna(row['Titel']):
            song.append(make_text_prop(":hasTitle", row['Titel']))

        if pd.notna(row['KomponistIn']):
            song.append(make_text_prop(":hasComposer", row['KomponistIn']))

        if pd.notna(row['TexterIn']):
            song.append(make_text_prop(":hasSongwriter", row['TexterIn']))

        if pd.notna(row['InterpretIn']):
            song.append(make_text_prop(":hasInterpreter", row['InterpretIn']))

        if pd.notna(row['Dauer [min:sec]']):
            song.append(make_text_prop(":hasDuration", row['Dauer [min:sec]']))

        if pd.notna(row['Liedarchiv-Nummer']):
            song.append(make_text_prop(":hasSongArchiveNum", str(row['Liedarchiv-Nummer'])))

        if pd.notna(row['Alte Signatur Tonband']):
            song.append(make_text_prop(":hasOldIdentifierTape", row['Alte Signatur Tonband']))

        if pd.notna(row['Seite']):
            song.append(make_text_prop(":hasPage", row['Seite']))

        if pd.notna(row['Liednr.']):
            song.append(make_text_prop(":hasSongNum", str(row['Liednr.'])))

        if pd.notna(row['Alte Signatur Track']):
            song.append(make_text_prop(":hasOldSignatureTrack", row['Alte Signatur Track']))

        if pd.notna(row['1. Aufnahmeort']):
            song.append(make_text_prop(":hasFirstRecordingLocation", row['1. Aufnahmeort']))

        if pd.notna(row['2. Herkunftort Komposition']):
            song.append(make_text_prop(":hasPointOfOriginComposition", row['2. Herkunftort Komposition']))

        if pd.notna(row['Aufnahmedatum: Anzeige']):
            song.append(make_text_prop(":hasRecordDateDisplay", row['Aufnahmedatum: Anzeige']))

        if pd.notna(row['Kompositionsdatum: Anzeige']):
            song.append(make_text_prop(":hasCompositionDateDisplay", str(row['Kompositionsdatum: Anzeige'])))

        if pd.notna(row['Instrumente']):
            song.append(make_list_prop("instruments", ":hasInstruments", row['Instrumente'].split(";")))

        if pd.notna(row['Personen/Institutionen']):
            song.append(make_text_prop(":hasPersons", row['Personen/Institutionen']))

        if pd.notna(row['Schlagworte']):
            song.append(make_text_prop(":hasKeywords", row['Schlagworte']))

        if pd.notna(row['Kommentar']):
            song.append(make_text_prop(":hasComment", row['Kommentar']))

        if pd.notna(row['Objektart']):
            song.append(make_list_prop("musicgenre", ":hasMusicGenre", [row['Objektart']]))

        if pd.notna(row['Originalträger']):
            song.append(make_list_prop("carriertype", ":hasCarrierType", [row['Originalträger']]))

        if pd.notna(row['Ist ein Teil von']):
            song.append(make_text_prop(":isPartOf", row['Ist ein Teil von']))

        if pd.notna(row['Sammlung']):
            song.append(make_text_prop(":hasCollection", row['Sammlung']))

        if pd.notna(row['Copyright']):
            song.append(make_text_prop(":hasCopyright", row['Copyright']))

        if pd.notna(row['Ähnliche Lieder/Stücke']):
            song.append(make_text_prop(":hasSimilarTracks", row['Ähnliche Lieder/Stücke']))

        if pd.notna(row['Erfassungsdatum']):
            song.append(make_text_prop(":hasEntryDate", row['Erfassungsdatum']))

        root.append(song)

        if pd.notna(row['Herkunftsort KomponistIn']):
            composer = make_resource(row['Herkunftsort KomponistIn'], ":KomponistIn", "comp_obj_" + str(index), "res-default")
            composer.append(make_text_prop(":hasPointOfOrigin", row['Herkunftsort KomponistIn']))
            root.append(composer)

        if pd.notna(row['Herkunftsort TexterIn']):
            songwriter = make_resource(row['Herkunftsort TexterIn'], ":TexterIn", "txt_obj_" + str(index), "res-default")
            songwriter.append(make_text_prop(":hasPointOfOrigin", row['Herkunftsort TexterIn']))
            root.append(songwriter)

        if pd.notna(row['Herkunftsort InterpretIn']):
            interpreter = make_resource(row['Herkunftsort InterpretIn'], ":InterpretIn", "int_obj_" + str(index), "res-default")
            interpreter.append(make_text_prop(":hasPointOfOrigin", row['Herkunftsort InterpretIn']))
            root.append(interpreter)

    # loop end

    document = root

    et = etree.ElementTree(document)
    with open('lenzburg.xml', 'wb') as f:
        et.write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)


if __name__ == "__main__":
    main()
