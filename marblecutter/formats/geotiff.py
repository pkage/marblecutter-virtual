# coding=utf-8
from __future__ import absolute_import

import logging
import numpy as np

from rasterio import transform
from rasterio.io import MemoryFile

from .. import _nodata, get_resolution_in_meters

CONTENT_TYPE = "image/tiff"
LOG = logging.getLogger(__name__)


def GeoTIFF(area_or_point="Area", blocksize=512, colormap=None):

    def _format(pixels, data_format, sources):
        data, (data_bounds, data_crs), _, _colormap = pixels
        if data_format is not "raw":
            raise Exception("raw data is required")

        (count, height, width) = data.shape
        cm = colormap or _colormap

        if np.issubdtype(data.dtype, np.floating):
            predictor = 3

            if count == 1:
                # (np.floating + count == 1) == typically DEMs
                resolution = get_resolution_in_meters(pixels.bounds, (height, width))

                # downsample to int16 if ground resolution is more than 10 meters
                # (at the equator)
                if resolution[0] > 10 and resolution[1] > 10:
                    data = data.astype(np.int16)
                    data.fill_value = _nodata(data.dtype)
        else:
            predictor = 2

        meta = {
            "blockxsize": blocksize if width >= blocksize else width,
            "blockysize": blocksize if height >= blocksize else height,
            "compress": "deflate",
            "count": count,
            "crs": data_crs,
            "dtype": data.dtype,
            "driver": "GTiff",
            "nodata": data.fill_value if data.dtype != np.uint8 else None,
            "predictor": predictor,
            "height": height,
            "width": width,
            "tiled": width >= blocksize and height >= blocksize,
            "transform": transform.from_bounds(
                *data_bounds, width=width, height=height
            ),
        }

        with MemoryFile() as memfile:
            with memfile.open(**meta) as dataset:
                dataset.update_tags(AREA_OR_POINT=area_or_point)
                sources_tag = "\n".join(
                    ["{} - {}".format(name, url) for (name, url) in sources]
                )
                dataset.update_tags(SOURCES=sources_tag)
                dataset.write(data.filled())

                if count == 1 and cm and len(list(cm.values())[0]) == 3:
                    dataset.write_colormap(1, cm)

                # TODO set colorinterp (may not be possible)
                # dataset.colorinterp = [ColorInterp.red, ColorInterp.green, ColorInterp.blue, ColorInterp.alpha]

            return (CONTENT_TYPE, memfile.read())

    return _format
