# UrbaTiler

[![Docker Cloud Automated build](https://img.shields.io/docker/cloud/automated/olivierdalang/marblecutter-virtual.svg)](https://hub.docker.com/r/olivierdalang/marblecutter-virtual) [![test_docker](https://github.com/olivierdalang/marblecutter-virtual/workflows/test_docker/badge.svg)](https://github.com/olivierdalang/marblecutter-virtual/actions)

Forké de marblecutter-virtual (voir readme ci-dessous).

## Déploiement

Le déploiement se fait via `git push` [à la heroku](https://tridnguyen.com/articles/simple-heroku-like-workflow-with-git-and-docker-compose/).

Il faut que la branche poussée corresponde à la branche courante sur le remote.

### Configuration

Sur le VPS :

```
# installer les dépendances
sudo apt-get update
sudo apt-get install docker.io docker-compose git

# initialiser un repo
git init marblecutter
cd marblecutter
git checkout -b prod

# configurer le repo
git config receive.denyCurrentBranch updateInstead
ln -s ../../git-deploy.sh ./.git/hooks/post-update
```

Sur votre machine :
```
# ajouter le remote (voir settings sur jelastics)
git remote add prod ssh://40948-1164@gate.jpe.infomaniak.com:3022/root/marblecutter

# créer la branche
git checkout -b prod
```

### Déploiement

Pusher la branche vers "prod" :
```
git push MY_REMOTE prod
```

## Test urls

- OpenAerialMaps
  - http://tiles.rdnt.io/bounds?url=https%3A%2F%2Foin-hotosm.s3.amazonaws.com%2F5f382b5cdf88ab000761cb10%2F0%2F5f382b5cdf88ab000761cb11.tif
  - http://127.0.0.1:8000/bounds?url=https%3A%2F%2Foin-hotosm.s3.amazonaws.com%2F5f382b5cdf88ab000761cb10%2F0%2F5f382b5cdf88ab000761cb11.tif
  - http://marblecutter.jcloud.ik-server.com:11543/bounds?url=https%3A%2F%2Foin-hotosm.s3.amazonaws.com%2F5f382b5cdf88ab000761cb10%2F0%2F5f382b5cdf88ab000761cb11.tif

- Inondations-Dakar (DTK-extract)
  - https://tiles.rdnt.io/bounds?url=https%3A%2F%2Finondations-dakar.org%2Fdataset%2F7e075bf5-7481-4253-8127-0ff1068938e4%2Fresource%2F3b8ef7ab-5d9e-49f7-93b9-e2b30e2ad733%2Fdownload%2Fdtk-extract-cog.tif
  - http://127.0.0.1:8000/bounds?url=https%3A%2F%2Finondations-dakar.org%2Fdataset%2F7e075bf5-7481-4253-8127-0ff1068938e4%2Fresource%2F3b8ef7ab-5d9e-49f7-93b9-e2b30e2ad733%2Fdownload%2Fdtk-extract-cog.tif
  - http://marblecutter.jcloud.ik-server.com:11543/bounds?url=https%3A%2F%2Finondations-dakar.org%2Fdataset%2F7e075bf5-7481-4253-8127-0ff1068938e4%2Fresource%2F3b8ef7ab-5d9e-49f7-93b9-e2b30e2ad733%2Fdownload%2Fdtk-extract-cog.tif

- Inondations-Dakar (Ndiareme-complet, on a souvent des erreurs avec celle là ?)
  - http://tiles.rdnt.io/bounds?url=https%3A%2F%2Finondations-dakar.org%2Fdataset%2Fe5717b4f-8590-4ed1-96ea-44a546b1411a%2Fresource%2F1dd744a3-3290-4589-94cd-da0e43337c12%2Fdownload%2Fndiareme-cog.tif
  - http://127.0.0.1:8000/bounds?url=https%3A%2F%2Finondations-dakar.org%2Fdataset%2Fe5717b4f-8590-4ed1-96ea-44a546b1411a%2Fresource%2F1dd744a3-3290-4589-94cd-da0e43337c12%2Fdownload%2Fndiareme-cog.tif
  - http://marblecutter.jcloud.ik-server.com:11543/bounds?url=https%3A%2F%2Finondations-dakar.org%2Fdataset%2Fe5717b4f-8590-4ed1-96ea-44a546b1411a%2Fresource%2F1dd744a3-3290-4589-94cd-da0e43337c12%2Fdownload%2Fndiareme-cog.tif

------

# marblecutter-virtual

I am a tile server for HTTP(S)-accessible [Cloud Optimized GeoTIFFs
(COGs)](http://www.cogeo.org/).

I can also be seen as an example of a virtual `Catalog` implementation, drawing
necessary metadata from URL parameters. For more information, check out [`VirtualCatalog`](virtual/catalogs.py) and [`web.py`](virtual/web.py).

## Running Locally

The easiest way to get a working instance running locally is to use [Docker
Compose](https://docs.docker.com/compose/):

```bash
docker-compose up
```

A tile server will then be accessible on `localhost:8000`. To browse a map
preview, visit
`http://localhost:8000/preview?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif`.

URLs (`url` in the query string) must be URL-encoded. From a browser's
JavaScript console (or Node.js REPL), run:

```javascript
encodeURIComponent("https://s3-us-west-2.amazonaws.com/planet-disaster-data/hurricane-harvey/SkySat_Freeport_s03_20170831T162740Z3.tif")
```

If you need to access non-public files on S3, set your environment accordingly
(see `sample.env`), either by creating `.env` and uncommenting `env_file` in
`docker-compose.yml` or by adding appropriate `environment` entries.

## Endpoints

### `/bounds` - Source image bounds (in geographic coordinates)

#### Parameters

* `url` - a URL to a valid COG. Required.

#### Example

```bash
$ curl "http://localhost:8000/bounds?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif"
{
  "bounds": [
    -95.46993599071261,
    28.86905396361014,
    -95.2386152334213,
    29.068190805522605
  ],
  "url": "https://s3-us-west-2.amazonaws.com/planet-disaster-data/hurricane-harvey/SkySat_Freeport_s03_20170831T162740Z3.tif"
}
```

### `/tiles/{z}/{x}/{y}` - Tiles

#### Parameters

* `url` - a URL to a valid COG. Required.
* `rgb` - Source bands to map to RGB channels. Defaults to `1,2,3`.
* `nodata` - a custom NODATA value.
* `linearStretch` - whether to stretch output to match min/max values present in
  the source. Useful for raw sensor output, e.g. earth observation (EO) data.
* `resample` - Specify a custom resampling method (e.g. for discrete values).
  Valid values (from `rasterio.enums.Resampling`): `nearest`, `bilinear`,
  `cubic`, `cubic_spline`, `lanczos`, `average`, `mode`, `gauss`, `max`, `min`,
  `med`, `q1`, `q3`. Defaults to `bilinear`.

`@2x` can be added to the filename (after the `{y}` coordinate) to request
retina tiles. The map preview will detect support for retina displays and
request tiles accordingly.

PNGs or JPEGs will be rendered depending on the presence of NODATA values in the
source image (surfaced as transparency in the output).

#### Examples

```bash
$ curl "http://localhost:8000/tiles/14/3851/6812@2x?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif" | imgcat
```

![RGB](docs/rgb.png)

```bash
$ curl "http://localhost:8000/tiles/14/3851/6812@2x?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif&rgb=1,1,1" | imgcat
```

![greyscale](docs/greyscale.png)

```bash
$ curl "http://localhost:8000/tiles/14/3851/6812@2x?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif&rgb=1,1,1&linearStretch=true" | imgcat
```

![greyscale stretched](docs/greyscale_stretched.png)

### `/tiles` - TileJSON

#### Parameters

See tile parameters.

#### Example

```bash
$ curl "http://localhost:8000/tiles?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif"
{
  "bounds": [
    -95.46993599071261,
    28.86905396361014,
    -95.2386152334213,
    29.068190805522605
  ],
  "center": [
    -95.35427561206696,
    28.968622384566373,
    15
  ],
  "maxzoom": 21,
  "minzoom": 8,
  "name": "Untitled",
  "tilejson": "2.1.0",
  "tiles": [
    "//localhost:8000/tiles/{z}/{x}/{y}?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif"
  ]
}
```

### `/preview` - Preview

#### Parameters

See tile parameters.

#### Example

`http://localhost:8000/preview?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif`

### `/debug` - Debug

Returns validation information from cog validator (see https://github.com/rouault/cog_validator).

#### Parameters

* `url` - a URL to a COG. Required.

#### Example

`http://localhost:8000/debug?url=https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fplanet-disaster-data%2Fhurricane-harvey%2FSkySat_Freeport_s03_20170831T162740Z3.tif`

## Deploying to AWS

marblecutter-virtual is deployed using the [AWS Serverless Application Model
(SAM)](https://github.com/awslabs/serverless-application-model).

Once you have the [SAM CLI](https://github.com/awslabs/aws-sam-cli) installed, you can build with:

```bash
sam build --use-container
```

You can then test it locally as though it's running on Lambda + API Gateway
(it will be _really_ slow, as function invocations are not re-used in the
same way as on Lambda proper):

```bash
sam local start-api
```

To deploy, first package the application:

```bash
sam package --s3-bucket <staging-bucket> --output-template-file packaged.yaml
```

Once staged, it can be deployed:

```bash
sam deploy \
  --template-file packaged.yaml \
  --stack-name marblecutter-virtual \
  --capabilities CAPABILITY_IAM \
  --parameter-overrides DomainName=<hostname>
```

These commands are wrapped as a `deploy` target, so this can be done more
simply with:

```bash
S3_BUCKET=<staging-bucket> DOMAIN_NAME=<hostname> make deploy
```

`<staging-bucket>` must be in the target AWS region (`AWS_DEFAULT_REGION`).

NOTE: when setting up a Cloudfront distribution in front of a regional API
Gateway endpoint (which is what this process does), an `Origin Custom Header`
will be added: `X-Forwarded-Host` should be the hostname used for your
Cloudfront distribution (otherwise auto-generated tile URLs will use the API
Gateway domain; CF sends a `Host` header corresponding to the origin, not the
CDN endpoint).