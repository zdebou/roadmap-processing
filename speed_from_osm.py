from __future__ import print_function
import geojson
import codecs
from curvature import get_length
from utils import err_print
import sys
import argparse


def execute(input_stream, output_stream):
    json_dict = load_file(input_stream)
    get_speed(json_dict)
    save_geojson(output_stream, json_dict)


def load_file(in_stream):
    err_print("loading file...")
    json_dict = geojson.load(in_stream)
    return json_dict


def get_speed(json_dict):
    err_print("getting speed from map...")
    for item in json_dict['features']:
        if 'maxspeed' not in item['properties']:
            if item['properties']['highway'] == 'motorway' or item['properties']['highway'] == 'motorway_link':  # for czechia
                item['properties']['speed'] = 130
            else:
                item['properties']['speed'] = 50
        else:
            item['properties']['speed'] = int(item['properties']['maxspeed'])
        item['properties']['length'] = get_length(item['geometry']['coordinates'])


def save_geojson(out_stream, json_dict):
    err_print("saving file...")
    geojson.dump(json_dict, out_stream)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest="input", type=str, action='store', help='input file')
    parser.add_argument('-o', dest="output", type=str, action='store', help='output file')
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    input_stream = sys.stdin
    output_stream = sys.stdout

    if args.input is not None:
        input_stream = codecs.open(args.input, encoding='utf8')
    if args.output is not None:
        output_stream = codecs.open(args.output, 'w')

    execute(input_stream, output_stream)
    input_stream.close()
    output_stream.close()
