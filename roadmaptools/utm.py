import utm
import numpy as np

from roadmaptools.init import config


class TransposedUTM:
	def __init__(self, origin_lat, origin_lon):
		self.origin_lat = origin_lat
		self.origin_lon = origin_lon

		res = utm.from_latlon(origin_lat, origin_lon)

		self.origin_easting = res[0]
		self.origin_northing = res[1]
		self.origin_zone_number = res[2]
		self.origin_zone_letter = res[3]

	def from_latlon(self, lat, lon):
		easting, northing, _, _ = utm.from_latlon(lat, lon, force_zone_number=self.origin_zone_number)
		easting -= self.origin_easting
		northing -= self.origin_northing
		return (easting, northing)

	def to_latlon(self, easting, northing):
		easting += self.origin_easting
		northing += self.origin_northing
		return utm.to_latlon(easting, northing, self.origin_zone_number, self.origin_zone_letter)


# Project to Euclidean plane such that the units are meters.
projection = TransposedUTM(config.utm_center_lon, config.utm_center_lat)


def latlon2tutm(latlon):
	easting, northing = np.vectorize(projection.from_latlon)(latlon[:,0],latlon[:,1])
	return np.column_stack([easting,northing])


def tutm2latlon(latlon):
	lat, lon = np.vectorize(projection.to_latlon)(latlon[:,0],latlon[:,1])
	return np.column_stack([lat, lon])