import geojson
import codecs
from roadmaptools.calculate_curvature import get_length
import sys
import argparse
import time

from roadmaptools.printer import print_info
from roadmaptools.init import config

SPEED_CODE_DICT = {'CZ:urban': 50}


# length is computed here too!!!
def estimate_posted_speed(input_filename: str, output_filename: str):
    print_info('Estimating travel speed')
    start_time = time.time()

    input_stream = codecs.open(input_filename, encoding='utf8')
    output_stream = open(output_filename, 'w')

    print_info("Loading file from: {}".format(input_filename))
    geojson_file = load_geojson(input_stream)

    print_info("Computing speed")
    geojson_out = get_geojson_with_speeds(geojson_file)

    print_info("Saving file to: {}".format(output_filename))
    save_geojson(geojson_out, output_stream)
    input_stream.close()
    output_stream.close()

    print_info('Speed estimation completed. (%.2f secs)' % (time.time() - start_time))



def estimate_speeds(input_stream, output_stream):
    json_dict = load_geojson(input_stream)
    get_speeds(json_dict)
    save_geojson(json_dict, output_stream)


def get_geojson_with_speeds(json_dict):
    get_speeds(json_dict)
    return json_dict


def load_geojson(in_stream):
    json_dict = geojson.load(in_stream)
    return json_dict


def get_speeds(json_dict):
    for item in json_dict['features']:
        if 'maxspeed' not in item['properties']:
            if item['properties']['highway'] == 'motorway' or item['properties']['highway'] == 'motorway_link':  # for czechia
                item['properties']['maxspeed'] = 130
            elif item['properties']['highway'] == 'living_street':  # for czechia
                item['properties']['maxspeed'] = 20
            else:
                item['properties']['maxspeed'] = 50
        else:
            try:
                item['properties']['maxspeed'] = int(item['properties']['maxspeed'])
            except:
                item['properties']['maxspeed'] = SPEED_CODE_DICT[item['properties']['maxspeed']]

        item['properties']['length'] = get_length(item['geometry']['coordinates'])


def save_geojson(json_dict, out_stream):
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

    estimate_speeds(input_stream, output_stream)
    input_stream.close()
    output_stream.close()
