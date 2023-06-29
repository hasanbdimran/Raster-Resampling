

in_raster_address = "/Users/ihasan/Downloads/TAMU/Network Theory/mspa/data/GFPlain/Raster/gfplain.tif"
upscale_factor = 1/2

with rasterio.open(in_raster_address) as dataset:

    # resample data to target shape
    data = dataset.read(
        out_shape=(
            dataset.count,
            int(dataset.height * upscale_factor),
            int(dataset.width * upscale_factor)
        ),
        resampling=Resampling.bilinear
    )

    # scale image transform
    transform = dataset.transform * dataset.transform.scale(
        (dataset.width / data.shape[-1]),
        (dataset.height / data.shape[-2])

  dst_kwargs = dataset.meta.copy()
dst_kwargs.update(
    {
        "crs": dataset.crs,
        "transform": transform,
        "width": data.shape[-1],
        "height": data.shape[-2],
        "nodata": 0,
        'compress': 'lzw'
    }
)

with rasterio.open("/Users/ihasan/Downloads/TAMU/Network Theory/mspa/data/GFPlain/Raster/gfplain30.tif", "w", **dst_kwargs) as dst:
    # iterate through bands
    for i in range(data.shape[0]):
          dst.write(data[i].astype(rasterio.uint32), i+1)
