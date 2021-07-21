from django.contrib.auth.models import User
from django.http import HttpRequest
from arches.app.models.models import GraphModel, Node, ResourceInstance, TileModel
from arches.app.models.concept import Concept, get_preflabel_from_valueid, get_valueids_from_concept_label
from arches.app.views import search
from django.core.management.base import BaseCommand
from eamena.bulk_uploader import HeritagePlaceBulkUploadSheet, GridSquareBulkUploadSheet
from geomet import wkt
import json, os, sys, logging, re, uuid, hashlib, datetime, warnings

logger = logging.getLogger(__name__)

class Command(BaseCommand):
	"""
	Command for finding invalid GeoJSON in the EAMENA database.

	"""

	def __test_geojson(self, gj):
		if isinstance(gj, (dict)):
			ret = True
			for keyo in gj.keys():
				key = str(keyo)
				ret = ret & (self.__test_geojson(gj[key]))
			return ret
		elif isinstance(gj, (list)):
			floats = 0
			for item in gj:
				if isinstance(item, (float)):
					floats = floats + 1
			if len(gj) == floats:
				if floats == 2:
					return True
				else:
					return False
			ret = True
			for item in gj:
				ret = ret & (self.__test_geojson(item))
			return ret
		else:
			return True

	def handle(self, *args, **options):

		node_id = '3080eebe-c2c5-11ea-9026-02e7594ce0a0'
		field_id = '5348cf67-c2c5-11ea-9026-02e7594ce0a0'
		tiles = TileModel.objects.filter(nodegroup_id=node_id).filter(data__icontains=field_id)

		sys.stderr.write('Searching for invalid geometries...\n')
		ct = 0

		for tile in tiles:
			if not(field_id in tile.data):
				continue
			geom = tile.data[field_id]
			if not(self.__test_geojson(geom)):
				rid = str(tile.resourceinstance_id)
				sys.stderr.write(self.style.ERROR("Arches ID " + rid + ' contains an invalid geometry!\n'))
				ct = ct + 1

		if ct == 0:
			sys.stderr.write('No invalid geometries found.\n')
		elif ct == 1:
			sys.stderr.write('1 invalid geometry found.\n')
		else:
			sys.stderr.write(str(ct) + ' invalid geometries found.\n')

# Choices are: data, file, geojsongeometry, nodegroup, nodegroup_id, parenttile, parenttile_id,
# provisionaledits, resourceinstance, resourceinstance_id, resxres_tile_id, sortorder,
# tileid, tilemodel, vwannotation
