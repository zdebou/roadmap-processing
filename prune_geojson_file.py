import geojson
import codecs
import copy


class Pruning_geojson_file:
    set_of_useful_properties = {'highway', 'id', 'lanes', 'maxspeed', 'oneway', 'bridge', 'width', 'tunnel', 'traffic_calming', 'lanes:forward', 'lanes:backward'}

    def __init__(self, filename):
        self.filename = filename

    def remove_properties(self, item):
        temp_dict_with_props = copy.deepcopy(item['properties'])
        for prop in temp_dict_with_props:
            if prop not in self.set_of_useful_properties:
                del item['properties'][prop]
        return item

    def load_file(self):
        print "loading file..."
        with codecs.open(self.filename, encoding='utf8') as f:
            self.json_dict = geojson.load(f)
        f.close()

        self.fill_new_geojson_with_deleted_items()

    def fill_new_geojson_with_deleted_items(self):
        json_deleted = {}
        json_deleted['type'] = self.json_dict['type']
        json_deleted['features'] = list()

        for item in self.json_dict['features']:
            if item['geometry']['type'] != 'LineString':
                json_deleted['features'].append(item)

        with codecs.open("data/deleted_items.geojson", 'w') as output:
            geojson.dump(json_deleted, output, indent=4, sort_keys=True)
        output.close()

    def get_single_pair_of_coords(self, coord_u, coord_v, new_item, id, is_forward):
        new_item['properties']['id'] = id
        del new_item['geometry']['coordinates']
        new_item['geometry']['coordinates'] = [coord_u, coord_v]
        if ('oneway' in new_item['properties'] and new_item['properties']['oneway'] != 'yes') or ('oneway' not in new_item['properties']):
            if 'lanes:forward' in new_item['properties'] and is_forward:
                new_item['properties']['lanes'] = new_item['properties']['lanes:forward']
            elif 'lanes:backward' in new_item['properties'] and not is_forward:
                new_item['properties']['lanes'] = new_item['properties']['lanes:backward']
            elif is_forward and 'lanes' in new_item['properties']:
                new_item['properties']['lanes'] = int(new_item['properties']['lanes']) - 1
            elif not is_forward and 'lanes' in new_item['properties']:
                new_item['properties']['lanes'] = 1

        if 'lanes' not in new_item['properties'] or new_item['properties']['lanes'] < 1:
            new_item['properties']['lanes'] = 1

        new_item['properties']['oneway'] = 'yes'
        return new_item

    def prune_geojson_file(self):
        print "processing..."
        id_iterator = 0
        length = len(self.json_dict['features'])

        for i in range(0, length):
            item = self.json_dict['features'][i]
            if item['geometry']['type'] == 'LineString':
                item = self.remove_properties(item)
                for i in range(0, len(item['geometry']['coordinates']) - 1):
                    temp = copy.deepcopy(item)
                    u = item['geometry']['coordinates'][i]
                    v = item['geometry']['coordinates'][i + 1]
                    new_item = self.get_single_pair_of_coords(u, v, temp, id_iterator, True)
                    self.json_dict['features'].append(new_item)
                    if 'oneway' in item['properties']:
                        if item['properties']['oneway'] == 'no':
                            id_iterator += 1
                            temp = copy.deepcopy(item)
                            new_item = self.get_single_pair_of_coords(v, u, temp, id_iterator, False)
                            self.json_dict['features'].append(new_item)
                    else:
                        id_iterator += 1
                        temp = copy.deepcopy(item)
                        new_item = self.get_single_pair_of_coords(v, u, temp, id_iterator, False)
                        self.json_dict['features'].append(new_item)

                    id_iterator += 1

            item.clear()

    def save_pruned_geojson(self):
        print "saving file..."
        self.json_dict['features'] = [i for i in self.json_dict["features"] if i]  # remove empty dicts
        with codecs.open("data/pruned_file.geojson", 'w') as out:
            geojson.dump(self.json_dict, out)
        out.close()


# EXAMPLE OF USAGE
# test = Pruning_geojson_file("data/output.geojson")
# test.load_file()
# test.prune_geojson_file()
# test.save_pruned_geojson()