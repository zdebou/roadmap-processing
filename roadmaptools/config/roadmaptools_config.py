
from fconfig.config import Config


class RoadmaptoolsConfig(Config):

    def __init__(self):
        self.geojson_file = None
        self.simplified_file = None
        self.cleaned_geojson_file = None
        self.simplified_file_with_speed_and_curvature = None
        self.osm_map_filename = None
        self.osm_source_url = None
        self.simplified_file_with_speed = None
        self.filtered_osm_filename = None



        pass

    def fill(self, properties: dict=None):
        self.geojson_file = properties.get("geojson_file")
        self.simplified_file = properties.get("simplified_file")
        self.cleaned_geojson_file = properties.get("cleaned_geojson_file")
        self.simplified_file_with_speed_and_curvature = properties.get("simplified_file_with_speed_and_curvature")
        self.osm_map_filename = properties.get("osm_map_filename")
        self.osm_source_url = properties.get("osm_source_url")
        self.simplified_file_with_speed = properties.get("simplified_file_with_speed")
        self.filtered_osm_filename = properties.get("filtered_osm_filename")



        pass
