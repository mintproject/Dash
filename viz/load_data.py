# Centralized location for extracting data information from a THREAD_ID
# These functions can be shared between the different visualization apps

# MINT API ingestion
from __future__ import print_function

import logging
import time
import urllib
from gzip import GzipFile
from io import BytesIO
import uuid

import solutioncatalog
import urllib3
from solutioncatalog.rest import ApiException
from pprint import pprint
from solutioncatalog.download import  download_files
from pathlib import Path
from osgeo import gdal
import pandas as pd

# GET Data from MINT API usint scenario_id, subgoal_id and THREAD_ID

http = urllib3.PoolManager()



api_instance = solutioncatalog.ResultsApi(solutioncatalog.ApiClient())
def get_MINT_data(scenario_id, subgoal_id, thread_id):
    try:
    # Get the results of a thread
        api_response = api_instance.results_scenario_id_subgoal_id_thread_id_get(scenario_id, subgoal_id, thread_id)
        resultsdf = pd.DataFrame(columns=['model', 'output','url'])
        results = api_response['thread']['results']
        for model in results.keys():
            for runs in results[model]:
                for output in runs['has_output']:
                    resultsdf = resultsdf.append({'model': model, 'output': output, 'url': runs['has_output'][output]['url']}, ignore_index=True)
        return resultsdf
    # except:
    #     return {'Result':'No data found in Solutions Catalog for this thread'}
    except ApiException as e:
        print("Exception when calling ResultsApi->results_scenario_id_subgoal_id_thread_id_get: %s\n" % e)


def open_http_query(url):
    try:
        response = urllib.request.urlopen(url)
        return response.read()
    except Exception as e:
        raise e




# Geto geospatial extent info from a geotiff
def get_geotiff_details(geotiff):
    details ={
        "center": [0,0],
        "bounds": [(0,0),(0,0)]
    }

    image_data = open_http_query(geotiff)
    mmap_name = "/vsimem/" + uuid.uuid4().hex
    gdal.FileFromMemBuffer(mmap_name, image_data)

    try:
        data = gdal.Open(mmap_name)

    except Exception as e:
        logging.error(e, exc_info=True)
    geoTransform = data.GetGeoTransform()
    if geoTransform is not None:
        minx = geoTransform[0]
        maxy = geoTransform[3]
        maxx = minx + geoTransform[1] * data.RasterXSize
        miny = maxy + geoTransform[5] * data.RasterYSize
        details['center'] = [(miny + maxy)/2, (minx + maxx)/2]
        details['bounds'] = [(miny, minx), (maxy, maxx)]
    data = None
    gdal.Unlink(mmap_name)
    return details
