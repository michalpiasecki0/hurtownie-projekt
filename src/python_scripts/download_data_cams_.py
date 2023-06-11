import cdsapi
import xarray as xr
import zipfile
import os

from typing import Optional
from pathlib import Path

def get_month_days_amount(month_number: int) -> int:
    assert 1 <= month_number <= 12, "Invalid month number"
    if month_number in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month_number == 2:
        return 28
    else:
        return 30


def download_data_air_quality_forecasts(
    start_date: str, end_date: str, output_path: str
) -> None:
    """
    Download data from CAMS website in NetCDF format.

    Args:
        start_date (str): start date in format 'yyyy-mm-dd'
        end_date (str): end date in format 'yyyy-mm-dd'
        output_path (str): path to output file
    """

    c = cdsapi.Client()

    c.retrieve(
        'cams-global-atmospheric-composition-forecasts',
        {
            'date': f'{start_date}/{end_date}',
            'type': 'forecast',
            'format': 'netcdf_zip',
            'leadtime_hour': '0',
            'time': '00:00',
            "area": [
                55,
                13.96,
                48.89,
                25.48,
            ],
            'variable': [
                '10m_u_component_of_wind', '10m_v_component_of_wind', 'u_component_of_wind',
                'v_component_of_wind',
            ],
        },
        f'{output_path}')


def convert_single_nc_to_csv(nc_path: str,
                             output_csv_folder: str,
                             month_number: Optional[int] = None) -> None:
    if not month_number:
        month_number = nc_path.split(sep='/')[-1].split(sep='.')[0]
    def _internal_convert_time_column(time_delta):
        return f'{str((time_delta.day + 1)).zfill(2)}-{str(month_number).zfill(2)}-2022'
    dataset = xr.open_dataset(nc_path, engine='netcdf4')
    dataset =dataset.to_dataframe()
    print(dataset)
    # remove level from index columns, everything measured on surface
    #dataset.reset_index(level=["level"], inplace=True)
    #dataset.drop(columns=["level"], inplace=True)
    #
    dataset.index = dataset.index.map(lambda k: (k[0], k[1], _internal_convert_time_column(k[2])))
    dataset.to_csv(f"{output_csv_folder}/{str(month_number).zfill(2)}.csv")    
    

if __name__ == "__main__":

    for path in Path("data/atmospheric_forecasts").iterdir():
        if path.is_file():
            with zipfile.ZipFile(path, 'r') as z:
                z.extractall('data/atmospheric_forecasts/')
            print(path)
            os.remove(path)
            os.rename('data/atmospheric_forecasts/data.nc', path)


    for path in Path("data/atmospheric_forecasts").iterdir():
        if path.is_file():
            print(path.stem)
            convert_single_nc_to_csv(nc_path=f"data/atmospheric_forecasts/{path.name}",
                                     output_csv_folder="data/atmospheric_forecasts/csvki",
                                    )

    ''' for i in range(1, 13, 1):
        days_month = get_month_days_amount(month_number=i)
        download_data_air_quality_forecasts(
            start_date=f"2022-{i:0{2}}-01",
            end_date=f"2022-{i:0{2}}-{days_month}",
            output_path=f"data/atmospheric_forecasts/{i}.nc",
        )
'''
