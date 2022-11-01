import os
import csv
import asyncio
import re

import requests
from datetime import datetime
import xml.etree.ElementTree as ET


def column(data: list | tuple, index: int) -> list:
    """
    Возвращает колонку из таблицы списков
    """
    if not data:
        return []
    assert index < len(data[0])
    return [x[index] for x in data]


def read_csv(path: str, csv_kwargs: dict, delimiter=';') -> list:
    with open(path, 'r', **csv_kwargs) as f:
        reader = csv.reader(f, delimiter=delimiter)
        for row in reader:
            yield row


def write_csv(path: str, data: list, csv_kwargs: dict, delimiter=';', mode='w', many=True):
    with open(path, mode, **csv_kwargs) as f:
        writer = csv.writer(f, delimiter=delimiter)
        if many:
            writer.writerows(data)
        else:
            for row in data:
                writer.writerow(row)


def create_elem(element_data: list, parent: ET.Element | None = None) -> ET.SubElement:
    name = element_data[1]
    text = element_data[2]
    if text and text[-1] == '\n':
        text = text[:-1]
    if parent is not None:
        element = ET.SubElement(parent, name)
    else:
        element = ET.Element(name)
    element.text = text
    if len(element_data) == 4 and element_data[3]:
        for k, v in element_data[3].items():
            element.set(k, v)
    return element


def create_xml_tree(data: list, root: ET.Element | None = None):
    if not root:
        root = create_elem(data[0])
        data.pop(0)
    parents = {root.tag: root}
    for item in data:
        node = create_node(item, parents)
        parents[node.tag] = node
    return root


def create_node(data: list, parents: dict) -> ET.SubElement | ET.Element:
    parent = ''
    if data[0] in parents.keys():
        parent = parents[data[0]]
    node = create_elem(data, parent if parent else None)
    return node


def write_xml(data: ET.Element, path: str, encoding: str, prefix: str | None = None):
    with open(path, 'w', encoding=encoding) as f:
        if prefix:
            f.write(prefix)
            tree = ET.tostring(data, encoding='unicode')
            f.write(tree)

 
def get_field(data: dict, path: list[str | int, ]) -> dict | str:
    if not data:
        return ''
    for key in path:
        if type(data) is list and len(data) >= key + 1:
            data = data[key]
        elif key in data.keys():
            data = data[key]
        else:
            return ''
    return data
     
