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
	Command for finding duplicate IDs in the EAMENA database.

	"""

	def handle(self, *args, **options):

		used = {}
		dates = {}
		highest = 0
		highest_id = ''

		eamena_id_uuid='34cfe992-c2c0-11ea-9026-02e7594ce0a0'
		date_uuid='34cfea81-c2c0-11ea-9026-02e7594ce0a0'
		ass_uuid='34cfea2e-c2c0-11ea-9026-02e7594ce0a0'
		for tile in TileModel.objects.filter(nodegroup_id=ass_uuid):
			data = tile.data
			if not(date_uuid in data):
				continue
			date = str(data[date_uuid])
			uuid = ''
			if not(tile is None):
				if not(tile.resourceinstance_id is None):
					uuid = str(tile.resourceinstance_id)
			if date == '':
				continue
			if uuid == '':
				continue
			dates[uuid] = date

		for tile in TileModel.objects.filter(nodegroup_id=eamena_id_uuid):
			data = tile.data
			if not(eamena_id_uuid in data):
				continue
			id = data[eamena_id_uuid]
			if id is None:
				id = ''
			uuid = ''
			if not(tile is None):
				if not(tile.resourceinstance_id is None):
					uuid = str(tile.resourceinstance_id)

			if id == '':
				num = 0
			else:
				num = int(id.replace('EAMENA-', ''))
			if num > highest:
				highest = num
				highest_id = id
			if id in used:
				used[id].append(uuid)
			else:
				used[id] = [uuid]

		print("Highest EAMENA ID: " + highest_id)
		print("Duplicates:")
		for idk in used.keys():
			id = str(idk)
			uuids = used[id]
			if len(uuids) <= 1:
				continue
			print(" * " + id)
			for uuid in uuids:
				date = ''
				if uuid in dates:
					date = ' (' + dates[uuid] + ')'
				print("   " + uuid + date)
