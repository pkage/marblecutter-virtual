# coding=utf-8

import logging
import math

from marblecutter import Bounds, get_resolution_in_meters, get_source, get_zoom
from marblecutter.catalogs import WGS84_CRS, Catalog
from marblecutter.utils import Source
from rasterio import warp
from rasterio.enums import Resampling

LOG = logging.getLogger(__name__)


class VirtualCatalog(Catalog):
    _rgb = None
    _nodata = None
    _linear_stretch = None
    _resample = None

    override_global_min = None
    override_global_max = None

    def __init__(self, uri, rgb=None, nodata=None, linear_stretch=None, resample=None, global_min=None, global_max=None):
        self._uri = uri

        if rgb:
            self._rgb = rgb

        if nodata:
            self._nodata = nodata

        if linear_stretch:
            self._linear_stretch = linear_stretch


        try:
            # test whether provided resampling method is valid
            Resampling[resample]
            self._resample = resample
        except KeyError:
            self._resample = None

        self._meta = {}

        if global_min is not None:
            self._meta['override_global_min'] = float(global_min)

        if global_max is not None:
            self._meta['override_global_max'] = float(global_max)

        with get_source(self._uri) as src:
            self._bounds = warp.transform_bounds(src.crs, WGS84_CRS, *src.bounds)
            self._resolution = get_resolution_in_meters(
                Bounds(src.bounds, src.crs), (src.height, src.width)
            )
            approximate_zoom = get_zoom(max(self._resolution), op=math.ceil)

            if global_min is not None:
                global_min = src.get_tag_item("TIFFTAG_MINSAMPLEVALUE")
            if global_max is not None:
                global_max = src.get_tag_item("TIFFTAG_MAXSAMPLEVALUE")

            for band in range(0, src.count):
                self._meta["values"] = self._meta.get("values", {})
                self._meta["values"][band] = {}
                min_val = src.get_tag_item("STATISTICS_MINIMUM", bidx=band + 1)
                max_val = src.get_tag_item("STATISTICS_MAXIMUM", bidx=band + 1)
                mean_val = src.get_tag_item("STATISTICS_MEAN", bidx=band + 1)

                if min_val is not None:
                    self._meta["values"][band]["min"] = float(min_val)
                elif global_min is not None:
                    self._meta["values"][band]["min"] = float(global_min)

                if max_val is not None:
                    self._meta["values"][band]["max"] = float(max_val)
                elif global_max is not None:
                    self._meta["values"][band]["max"] = float(global_max)

                if mean_val is not None:
                    self._meta["values"][band]["mean"] = float(mean_val)

        self._center = [
            (self._bounds[0] + self.bounds[2]) / 2,
            (self._bounds[1] + self.bounds[3]) / 2,
            approximate_zoom - 3,
        ]
        self._maxzoom = approximate_zoom + 3
        self._minzoom = approximate_zoom - 10

    @property
    def uri(self):
        return self._uri

    def get_sources(self, bounds, resolution):
        recipes = {"imagery": True}

        if self._rgb is not None:
            recipes["rgb_bands"] = map(int, self._rgb.split(","))

        if self._nodata is not None:
            recipes["nodata"] = self._nodata

        if self._linear_stretch is not None:
            recipes["linear_stretch"] = "per_band"

        if self._resample is not None:
            recipes["resample"] = self._resample

        if 'override_global_min' in self._meta and 'override_global_max' in self._meta:
            recipes["global_min"] = self._meta['override_global_min']
            recipes["global_max"] = self._meta['override_global_max']

        yield Source(
            url=self._uri,
            name=self._name,
            resolution=self._resolution,
            band_info={},
            meta=self._meta,
            recipes=recipes,
        )
