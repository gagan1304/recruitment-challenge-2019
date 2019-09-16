"""
Load  data from a BOM grid file in to a 2D array that uses
LAT/LON as the index.

For example to get the total daily irradiance for location  -27.45, 153.05:

>>> data_by_location, start_date, end_date = get_solar_exposure_data_from_grid_file(grid_file_name)
>>> data_by_location['-27.45']['153.05'] # note that the index is a string NOT float

See also http://www.bom.gov.au/climate/austmaps/about-solar-maps.shtml

"""
import sys
import datetime


def round_to(n, precission):
    correction = 0.5 if n >= 0 else -0.5
    return int(n/precission+correction)*precission

def round_to_05(n):
    return round_to(n, 0.05)

def get_solar_exposure_data_from_grid_file(grid_file_name, tzinfo=None):

    grid_file = open(grid_file_name, mode='r')
    
    params = {}
    data_by_location = {}
    ln_no = 0
    nrows = -1
    data_row_no = 0
    data_col_no = 0
    no_value_replacement = ''

    for ln in grid_file.readlines():
        ln = ln.strip('\n')
        if ln_no < 6:
            p,v = ln.split(' ')
            params[p] = v
            
            if 'ncols' in params: params['ncols'] = int(params['ncols'])
            if 'nrows' in params:
                params['nrows'] = int(params['nrows'])
                nrows = params['nrows']
            if 'xllcenter' in params:  params['xllcenter'] = float(params['xllcenter'])
            if 'yllcenter' in params:  params['yllcenter'] = float(params['yllcenter'])
            if 'cellsize' in params:  params['cellsize'] = float(params['cellsize'])
    
        if ln_no > 5 and ln_no <= (nrows+5):
            data_row_no +=1
            data_col_no = 0
            # y coord
            yll = params['yllcenter'] + (params['nrows'] * params['cellsize']) - (data_row_no * params['cellsize'])
            yll = str(yll)
            row_data = ln.split(' ')
            for i in range(params['ncols']):
                xll = params['xllcenter'] + (data_col_no * params['cellsize'])
                xll = str(xll)
                value = row_data[i+1]
                if value == params['nodata_value']:
                    value = no_value_replacement
                else:
                    value=float(value)
                data_col_no +=1
                
                if yll not in data_by_location:
                    data_by_location[yll] = {}
                data_by_location[yll][xll]= value    
            
        if ln_no > nrows+5:
            pos = ln.find('ANALYSIS')
            if pos > -1:
                analysis_date_range_str = ln[pos:].strip()[-16:]
                start_date_str = analysis_date_range_str[:8]
                end_date_str = analysis_date_range_str[8:]
                start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
                end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
                if tzinfo is not None:
                    start_date = start_date.replace(tzinfo=tzinfo)
                    end_date = end_date.replace(tzinfo=tzinfo)
    
        ln_no +=1
    
    return data_by_location, start_date, end_date


if __name__ == '__main__':
    grid_file_name = sys.argv[1]
    data_by_location, start_date, end_date = get_solar_exposure_data_from_grid_file(grid_file_name)
    print(data_by_location['-27.45']['153.05'], start_date, end_date)
