#!/usr/bin/env python
# Copyright 2021
# author: Luis Ackermann <ackermann.luis@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from collections import defaultdict
import pickle
import os
import sys
import ctypes
import shutil
import glob
from datetime import datetime
import time
import calendar
import email
import imaplib
import smtplib
import platform
import ftplib
from io import BytesIO
import zipfile
import subprocess
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from math import e as e_constant
import math
from tkinter import filedialog
from pathlib import Path as Path_pathlib
import re
import tempfile
from pathlib import Path as Path_lib

from PIL import Image as PIL_Image
from PIL.PngImagePlugin import PngInfo
import numpy as np
import matplotlib
from scipy.stats import ttest_ind, mode
import netCDF4 as nc
import requests
from xlrd import open_workbook
from xlrd.xldate import xldate_as_datetime
from scp import SCPClient
import imageio
import pyproj as proj
import pygrib

from numpy import genfromtxt
from scipy.optimize import curve_fit
from scipy.cluster.vq import kmeans,vq
from scipy.interpolate import interpn, interp1d
import matplotlib.dates as mdates
import dateutil.tz
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
from matplotlib.ticker import (MultipleLocator, NullFormatter, ScalarFormatter, FormatStrFormatter)
from matplotlib.colors import ListedColormap, BoundaryNorm, LinearSegmentedColormap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import LassoSelector
from matplotlib.path import Path

import IMProToo_mod
import SkewT_V2 as SkewT
import cdsapi

# <editor-fold desc="conditional imports that are troublesome">
try:
    from mpl_toolkits.basemap import Basemap
    basemap_available = True
except:
    basemap_available = False
try:
    import cartopy.crs as ccrs
    cartopy_available = True
except:
    cartopy_available = False
try:
    import wrf
    wrf_available = True
except:
    wrf_available = False
try:
    import pdf2image
    pdf_available = True
except:
    pdf_available = False

try:
    from paramiko import SSHClient, AutoAddPolicy
    paramiko_available = True
except:
    paramiko_available = False
# </editor-fold>



import warnings
warnings.filterwarnings("ignore")


AtmSciTools_path = str(Path_pathlib(__file__).parent)
sys.path.append(AtmSciTools_path)

tz_UTC = dateutil.tz.gettz('UTC')

try:
    matplotlib.use('qtagg')
except:
    try:
        matplotlib.use('TkAgg')
    except:
        pass
# plt.style.use('classic')
# matplotlib.use('QT4Agg')

# font size
# font_size = 14
# matplotlib.rc('font', **{'family': 'serif', 'serif': ['Arial'], 'size': font_size})
# matplotlib.rc('font', weight='bold')
p_progress_writing = False

SMALL_SIZE = 8
MEDIUM_SIZE = 10
BIGGER_SIZE = 12
plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title



time_format = '%d-%m-%Y_%H:%M'
time_format_iso = '%Y-%m-%dT%H:%M:%SZ'
time_format_khan = '%Y%m%d.0%H'
time_format_mod = '%Y-%m-%d_%H:%M:%S'
time_format_easy = '%Y-%m-%d %H:%M'
time_format_wrf_filename = '%Y-%m-%d_%H_%M_%S'
time_format_twolines = '%H:%M\n%d-%m-%Y'
time_format_twolines_noYear_noMin_intMonth = '%H\n%d-%m'
time_format_twolines_noYear = '%H:%M\n%d-%b'
time_format_twolines_noYear_noMin = '%H\n%d-%b'
time_format_date = '%Y-%m-%d'
time_format_date_inverse = '%d-%m-%Y'
time_format_time = '%H:%M:%S'
time_format_parsivel = '%Y%m%d%H%M'
time_format_YMDHM = time_format_parsivel
time_format_YMD = '%Y%m%d'
time_format_parsivel_ = '%Y%m%d_%H%M'
time_format_parsivel_seconds = '%Y%m%d%H%M%S'
time_format_YMDHMS = time_format_parsivel_seconds
time_str_formats = [
    time_format,
    time_format_iso,
    time_format_khan,
    time_format_mod,
    time_format_easy,
    time_format_wrf_filename,
    time_format_twolines,
    time_format_twolines_noYear_noMin_intMonth,
    time_format_twolines_noYear,
    time_format_twolines_noYear_noMin,
    time_format_date,
    time_format_date_inverse,
    time_format_time,
    time_format_parsivel,
    time_format_YMDHM,
    time_format_YMD,
    time_format_parsivel_,
    time_format_parsivel_seconds,
    time_format_YMDHMS
]


path_program = os.path.dirname(os.path.realpath(sys.argv[0])) + '/'
if platform.platform()[0] == "W":
    path_input = "C:/_input/"
    path_output = "C:/_output/"
    path_temp = "C:/_temp/"
    path_data = 'D:/Data/'
    path_log = '/g/data/k10/la6753/job_logs/'
else:
    path_input = '/home/lackerma/_input/'
    path_output = '/home/lackerma/_output/'
    path_temp = "/home/lackerma/_temp/"
    path_data = '/home/lackerma/data/'
    path_log = '/home/lackerma/data/'



melbourne_airport_station_number_sonde = 94866
hobart_airport_station_number_sonde = 94975

cabramurra_lat_lon = (-35.938825, 148.379048)
blue_calf_lat_lon = (-36.387182, 148.394426)
murray_1_lat_lon = (-36.247138, 148.190369)
waga_waga_lat_lon = (-35.15, 147.45)

default_cm = cm.jet
cm_vir = cm.viridis
listed_cm_colors_list = ['silver', 'red', 'green', 'yellow', 'blue', 'black']
listed_cm = ListedColormap(listed_cm_colors_list, 'indexed')

colorbar_tick_labels_list_cloud_phase = ['Clear', 'Water', 'SLW', 'Mixed', 'Ice', 'Unknown']
listed_cm_colors_list_cloud_phase = ['white', 'red', 'green', 'yellow', 'blue', 'purple']
listed_cm_cloud_phase = ListedColormap(listed_cm_colors_list_cloud_phase, 'indexed')

# cloud top temperature cmap
def shiftedColorMap(cmap, midpoint=0.5, name=None):

    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(0, 1, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False),
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)

    if name is not None:
        plt.register_cmap(cmap=newcmap)

    return newcmap
colors1 = cm.Blues_r(np.linspace(0., .8, 128))
colors2 = cm.Reds(np.linspace(0.2, 1., 128))
colors = np.vstack((colors1, colors2))
cmap_cloud_temp_temp = LinearSegmentedColormap.from_list('my_colormap', colors)
vmin_cloudT = -40
vmax_cloudT = 20
cmap_cloud_temp1 = shiftedColorMap(cmap_cloud_temp_temp, -vmin_cloudT / (-vmin_cloudT +vmax_cloudT), None)#'cmap_cloud_temp1')
cmap_cloud_temp2 = shiftedColorMap(cm.bwr, -vmin_cloudT / (-vmin_cloudT +vmax_cloudT),  None)#'cmap_cloud_temp2')

cmap_ctt = cmap_cloud_temp1

W_cm = shiftedColorMap(cm.bwr_r, 1/3, None)#'W_cm')
W_cm_inverse = shiftedColorMap(cm.bwr, 2/3, None)#'W_cm_inverse')


avogadros_ = 6.022140857E+23 # molecules/mol
gas_const = 83144.598 # cm3  mbar  k-1   mol-1
gas_const_2 = 8.3144621 # J mol-1 K-1
gas_const_water = 461 # J kg-1 K-1
gas_const_dry = 287 # J kg-1 K-1

boltzmann_ = gas_const / avogadros_ #  cm3  mbar / k   molecules
gravity_ = 9.80665  # m/s
poisson_ = 2/7 # for dry air (k)
latent_heat_v = 2.501E+6 # J/kg
latent_heat_f = 3.337E+5 # J/kg
latent_heat_s = 2.834E+6 # J/kg

heat_capacity__Cp = 1005.7 # J kg-1 K-1    dry air
heat_capacity__Cv = 719 # J kg-1 K-1      water vapor

Rs_da = 287.05          # Specific gas const for dry air, J kg^{-1} K^{-1}
Rs_v = 461.51           # Specific gas const for water vapour, J kg^{-1} K^{-1}
Cp_da = 1004.6          # Specific heat at constant pressure for dry air
Cv_da = 719.            # Specific heat at constant volume for dry air
Cp_v = 1870.            # Specific heat at constant pressure for water vapour
Cv_v = 1410.            # Specific heat at constant volume for water vapour
Cp_lw = 4218	          # Specific heat at constant pressure for liquid water
Epsilon = 0.622         # Epsilon=Rs_da/Rs_v; The ratio of the gas constants
degCtoK = 273.15        # Temperature offset between K and C (deg C)
rho_w = 1000.           # Liquid Water density kg m^{-3}
grav = 9.80665          # Gravity, m s^{-2}
Lv = 2.5e6              # Latent Heat of vaporisation
boltzmann = 5.67e-8     # Stefan-Boltzmann constant
mv = 18.0153e-3         # Mean molar mass of water vapor(kg/mol)
m_a = 28.9644e-3        # Mean molar mass of air(kg/mol)
Rstar_a = 8.31432       # Universal gas constant for air (N m /(mol K))

# functions to load basemap and topographical data when first used
aus_coastline_loaded = False
glob_coastline_loaded = False
glob_topo_loaded = False
aus_topo_loaded = False
def load_aus_coastline():
    global aus_coast_lon, aus_coast_lat, aus_coastline_loaded
    aus_basemap_nc = nc.Dataset(AtmSciTools_path + '/aus_basemap.nc')
    aus_coast_lon = aus_basemap_nc.variables['lon'][:].filled(np.nan)
    aus_coast_lat = aus_basemap_nc.variables['lat'][:].filled(np.nan)
    aus_basemap_nc.close()
    aus_coastline_loaded = True
def load_global_coastline():
    global glob_coast_lat, glob_coast_lon, glob_coastline_loaded
    glob_basemap_lat_nc = nc.Dataset(AtmSciTools_path + '/glob_basemap_lat.nc')
    glob_coast_lat = glob_basemap_lat_nc.variables['lat'][:].filled(np.nan)
    glob_basemap_lat_nc.close()
    glob_basemap_lon_nc = nc.Dataset(AtmSciTools_path + '/glob_basemap_lon.nc')
    glob_coast_lon = glob_basemap_lon_nc.variables['lon'][:].filled(np.nan)
    glob_basemap_lon_nc.close()
    glob_coastline_loaded = True
def load_glob_topo():
    global topo_lat, topo_lon, topo_arr, glob_topo_loaded
    topo_nc = nc.Dataset(AtmSciTools_path + '/topo_0_1degrees.nc')
    topo_lat = topo_nc.variables['lat'][:].data
    topo_lon = topo_nc.variables['lon'][:].data
    topo_arr = topo_nc.variables['z'][:].data
    topo_nc.close()
    glob_topo_loaded = True
def load_aus_topo():
    global highres_lat, highres_lon, highres_topo, aus_topo_loaded
    access_nc_sfc = nc.Dataset(AtmSciTools_path + '/topo_1km_australia.nc')
    highres_lat = access_nc_sfc.variables['lat'][:].filled(np.nan)
    highres_lon = access_nc_sfc.variables['lon'][:].filled(np.nan)
    highres_topo = access_nc_sfc.variables['topog'][:].filled(np.nan)
    access_nc_sfc.close()
    aus_topo_loaded = True
def return_aus_coastline():
    aus_basemap_nc = nc.Dataset(AtmSciTools_path + '/aus_basemap.nc')
    aus_coast_lon = aus_basemap_nc.variables['lon'][:].filled(np.nan)
    aus_coast_lat = aus_basemap_nc.variables['lat'][:].filled(np.nan)
    aus_basemap_nc.close()
    return aus_coast_lon, aus_coast_lat
def return_global_coastline():
    glob_basemap_lat_nc = nc.Dataset(AtmSciTools_path + '/glob_basemap_lat.nc')
    glob_coast_lat = glob_basemap_lat_nc.variables['lat'][:].filled(np.nan)
    glob_basemap_lat_nc.close()
    glob_basemap_lon_nc = nc.Dataset(AtmSciTools_path + '/glob_basemap_lon.nc')
    glob_coast_lon = glob_basemap_lon_nc.variables['lon'][:].filled(np.nan)
    glob_basemap_lon_nc.close()
    return glob_coast_lat, glob_coast_lon
def return_glob_topo():
    topo_nc = nc.Dataset(AtmSciTools_path + '/topo_0_1degrees.nc')
    topo_lat = topo_nc.variables['lat'][:].data
    topo_lon = topo_nc.variables['lon'][:].data
    topo_arr = topo_nc.variables['z'][:].data
    topo_nc.close()
    return topo_lat, topo_lon, topo_arr
def return_aus_topo():
    access_nc_sfc = nc.Dataset(AtmSciTools_path + '/topo_1km_australia.nc')
    highres_lat = access_nc_sfc.variables['lat'][:].filled(np.nan)
    highres_lon = access_nc_sfc.variables['lon'][:].filled(np.nan)
    highres_topo = access_nc_sfc.variables['topog'][:].filled(np.nan)
    access_nc_sfc.close()
    return highres_lat, highres_lon, highres_topo

# NCI - Gadi
def gadi_get_job_id():
    return str(os.getenv('PBS_JOBID').split('.')[0])
def gadi_get_job_path():
    return f"/jobfs/{os.getenv('PBS_JOBID')}/"

# Hail
def shi_to_mesh75(SHI_):
    MESH_75 = 15.096 * SHI_ ** 0.20
    return MESH_75
def mesh_to_damages(MESH_mm, slope_, inflex_, max_y):
    damages_perc = max_y / (1 + (e_constant ** (-slope_ * (MESH_mm - inflex_))))
    return damages_perc
def Hdr_radar_calculate(dbz_array, zdr_array):
    """
    Hail Differential reflectivity Retrieval

    "Hail Differential Reflectivity developed by Aydin and Zhao (1990) doi:10.1109/TGRS.1990.572906"
    "description": "Hail Differential Reflectivity Hail Size developed by Depue et al. (2009) doi:10.1175/JAM2529.1",
        "comments": "transform from HDR (dB) to hail size (mm); function scaled from paper figure"

    Parameters:
    ===========
    dbz_array: numpy array or float. Radar reflectivity in dB.
    zdr_array: numpy array or float. Differential radar reflectivity in dB.
    Returns:
    ========
    hdr_dB: numpy array or float. Hail Differential reflectivity in dB.
    hdr_mm: numpy array or float. Hail Differential reflectivity in mm.
    """

    # calculate hdr
    # apply primary function
    zdr_fun = 19 * zdr_array + 27
    # set limits based on zdr
    zdr_fun[zdr_array <= 0] = 27
    zdr_fun[zdr_array > 1.74] = 60
    # apply to zhh
    hdr_dB = dbz_array - zdr_fun

    # use polynomial from Depue et al. 2009 to transform dB into mm
    hdr_mm = 0.0284 * (hdr_dB ** 2) - 0.366 * hdr_dB + 11.69
    hdr_mm[hdr_dB <= 0] = 0

    # return hdr data
    return hdr_dB, hdr_mm
def hail_damage_probability_spread(damage_freq_arr, lat_arr, lon_arr, lambda_decay=.00055, maximum_spread=5000):
    """
    Spreads hail damage probability spatially using an exponential decay function.

    This function takes a 2D array of hail damage frequencies and distributes the probability
    spatially based on an exponential decay function. The probability decays with distance from
    each damage point, and the spread is limited to a maximum distance.

    Parameters:
    ----------
    damage_freq_arr : np.ndarray
        A 2D array (n x m) where each element represents the frequency of hail damage occurrences
        at a specific grid point.

    lat_arr : np.ndarray
        A 2D array (n x m) containing latitude values corresponding to the grid points in `damage_freq_arr`.

    lon_arr : np.ndarray
        A 2D array (n x m) containing longitude values corresponding to the grid points in `damage_freq_arr`.

    lambda_decay : float, optional (default=0.00055)
        The decay constant for the exponential function. Larger values result in a faster drop-off of probability
        with distance.

    maximum_spread : float, optional (default=5000)
        The maximum distance (in meters) over which the probability is spread. Beyond this distance,
        the probability is set to zero.

    Returns:
    -------
    probability_array : np.ndarray
        A 2D array (n x m) representing the spatially distributed probability of hail damage.
        The total probability across all grid points sums to the total number of hail damage occurrences.

    Notes:
    ------
    - The function iterates through all grid points in `damage_freq_arr`, identifying locations where
      hail damage has occurred (values > 0).
    - For each hail damage occurrence, the function computes a distance array from that point to all
      other grid points using `distance_array_lat_lon_2D_arrays_degress_to_meters()`.
    - An exponential decay function is applied to distribute the probability spatially.
    - Probabilities beyond `maximum_spread` are set to zero.
    - The final probability array is the sum of all individual probability distributions.
    """

    probability_array_list = []
    for r_ in range(damage_freq_arr.shape[0]):
        for c_ in range(damage_freq_arr.shape[1]):
            point_frequency = damage_freq_arr[r_, c_]
            if point_frequency > 0:
                # get point location
                point_lat = lat_arr[r_, c_]
                point_lon = lon_arr[r_, c_]

                # get distance array from point
                distance_from_point = distance_array_lat_lon_2D_arrays_degress_to_meters(lat_arr, lon_arr, point_lat,
                                                                                         point_lon)

                # Apply the exponential decay function
                decay_function = np.exp(-lambda_decay * distance_from_point)
                decay_function[distance_from_point > maximum_spread] = 0

                # Normalize so the total probability sums to 1
                decay_function = decay_function * point_frequency / np.sum(decay_function)

                probability_array_list.append(decay_function)

    probability_array = np.sum(np.stack(probability_array_list, axis=0), axis=0)
    return probability_array


# Misc
def number_of_digits_in_integer(number_or_array):
    if type(number_or_array) == int:
        return int(np.array(np.floor(np.log10(number_or_array)) + 1, dtype=int))
    else:
        return np.array(np.floor(np.log10(number_or_array)) + 1, dtype=int)
def row_index_nearest(array_, value_):
    row_ = np.argmin(np.abs(array_ - value_))
    return row_
def no_nans(listOfArrays_or_2Darray, return_mask=False, return_2D_array=False):
    # only coincidences
    if type(listOfArrays_or_2Darray) == list:
        array_2D = np.column_stack(listOfArrays_or_2Darray)
    else:
        array_2D = listOfArrays_or_2Darray

    arr_1D = np.sum(array_2D, axis=1)
    mask_ = ~np.isnan(arr_1D)
    out_arr = array_2D[mask_]

    if return_2D_array:
        if return_mask:
            return out_arr, mask_
        else:
            return out_arr
    else:
        out_list = []
        for c_ in range(out_arr.shape[1]):
            out_list.append(out_arr[:,c_])
        if return_mask:
            return out_list, mask_
        else:
            return out_list
def invert_dict(original_dict, inverted_dict):
    inverted_dict = {}
    for k, v in original_dict.items():
        inverted_dict[v] = inverted_dict.get(v, []) + [k]
    return inverted_dict
def scientific_notation_stop_numpy():
    np.set_printoptions(suppress=True)
def scientific_notation_start_numpy():
    np.set_printoptions(suppress=False)
def error_except():
    correct_format = """
    except BaseException as error_msg:
    \tline_number = sys.exc_info()[-1].tb_lineno
    \tprint('error in line {0}, error message:\\n{1}'.format(line_number, error_msg))
    """
    print(correct_format)
def split_str_by_n_char(string_, n):
    return [string_[i:i + n] for i in range(0, len(string_), n)]
def get_last_line(filename_, line_return_index=-1):
    # get last line, last temperature reading
    with open(filename_, 'rb') as fh:
        first = next(fh)
        offs = -100
        while True:
            fh.seek(offs, 2)
            lines = fh.readlines()
            if len(lines) > np.abs(line_return_index):
                last_line = lines[line_return_index]
                break
            offs *= 2
    return last_line
def minimize_cmd():
    ctypes.windll.user32.ShowWindow( ctypes.windll.kernel32.GetConsoleWindow(), 6 )
def read_email_subjects_from_gmail(FROM_EMAIL, FROM_PWD, emails_to_be_read=6):
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(FROM_EMAIL,FROM_PWD)
    mail.select('inbox')

    type_search, data_search = mail.search(None, 'ALL')
    mail_ids = data_search[0]
    id_list = np.array(mail_ids.split(), dtype=int)

    email_list = []
    emails_to_be_read = 6
    if id_list.shape[0] < 6:
        emails_to_be_read = id_list.shape[0]

    for i in id_list[-emails_to_be_read:]:
        type_fetch, data_fetch = mail.fetch(str(i), '(RFC822)')
        for response_part in data_fetch:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode())
                email_subject = msg['subject']
                email_list.append(email_subject)
    return email_list
def send_gmail(subject_, body_text, to_, from_, password_, attachement_image_s=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = from_  # Type your own gmail address
        msg['To'] = to_  # Type your friend's mail address
        msg['Subject'] = subject_  # Type the subject of your message
        msg.attach(MIMEText(body_text, 'plain'))
        if attachement_image_s is not None:
            if type(attachement_image_s) is list:
                for img_filename in attachement_image_s:
                    with open(img_filename, 'rb') as fp:
                        img = MIMEImage(fp.read())
                    filename_without_path = img_filename.replace('\\','/').split('/')[-1]
                    img.add_header('Content-Disposition', "attachment; filename= %s" % filename_without_path)
                    msg.attach(img)
            else:
                with open(attachement_image_s, 'rb') as fp:
                    img = MIMEImage(fp.read())
                filename_without_path = attachement_image_s.replace('\\','/').split('/')[-1]
                img.add_header('Content-Disposition', "attachment; filename= %s" % filename_without_path)
                msg.attach(img)

        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        server.login(msg['From'], password_)
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
    except:
        print('error while sending email')
def bell_alarm(time_=1.):
    if platform.platform()[0] == "W":
        import winsound
        winsound.Beep(440, int(time_*1000))
    else:
        try:
            os.system('play -nq -t alsa synth {} sine {}'.format(time_, 440))
        except:
            print('command not found, may need to install sox package')
def log_msg(text_, process_id):
    log_file = open(path_log + process_id + '.log', 'a')
    log_file.write(time_seconds_to_str(time.time(), time_format_mod) + '\t' + text_ + '\n')
    log_file.close()
def show_dict_summary(d, indent=0, max_value_characters=8, max_value_items=8, indent_max=5):
    for key, value in d.items():
        if isinstance(value, dict):
            print('\t' * indent + str(key))
            if indent < indent_max:
                show_dict_summary(value, indent+1)
            else:
                print('\t' * indent + 'more dictionaries beyond max_indent, not shown')
        elif isinstance(value, list):
            print('\t' * indent + str(key) + '\t:\t',  value[:max_value_items])
        elif isinstance(value, tuple):
            print('\t' * indent + str(key) + '\t:\t', value)
        elif type(value) == np.ndarray:
            print('\t' * indent + str(key) + '\t:\t numpy array with shape',  value.shape)
        elif type(value) == np.ma.core.MaskedArray:
            print('\t' * indent + str(key) + '\t:\t masked numpy array with shape',  value.shape)
        elif isinstance(value, str):
            if len(value) > max_value_characters:
                print('\t' * indent + str(key) + '\t:\t', value[:max_value_characters], '...')
            else:
                print('\t' * indent + str(key) + '\t:\t', value)
        elif isinstance(value, float):
            print('\t' * indent + str(key) + '\t:\t', np.round(value,max_value_characters))
        elif isinstance(value, int):
            print('\t' * indent + str(key) + '\t:\t', value)
        else:
            print('\t' * indent + str(key) + '\t:\t', '[some object with unknown type]')
def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent+1)
class Object_create(object):
    pass
def p_(header_):
    # parameters list
    print('-' * 20)
    print('Parameters: ')
    parameter_list = ''
    fill_len = len(str(len(list(header_))))
    for i, parameter_ in enumerate(header_):
        parameter_list =  str(parameter_list) + str(i).rjust(fill_len) + " ---> " + str(parameter_) + '\n'
    print(parameter_list)
    print('-' * 20)
def p_progress(current_count, total_count, display_each_percent=10, extra_text='done'):
    if total_count <= display_each_percent:
        if total_count > 0:
            print(int(100 * current_count / total_count), '%', extra_text)
    else:
        total_count_corrected = int(total_count / display_each_percent) * display_each_percent
        if display_each_percent * current_count / total_count_corrected % 1 == 0:
            if 0 < int(100 * current_count / total_count_corrected) <= 100:
                print(int(100 * current_count / total_count_corrected), '%', extra_text)
def p_progress_bar(current_count, total_count, extra_text='done'):
    display_each_percent = 5
    units_ = int(100 / display_each_percent)

    if current_count == 0:
        print('|' + ' ' *  units_ + '| %', extra_text, end="", flush=True)

    if current_count == total_count -1:
        print('\r', end='')
        print('|' + '-' *  units_ + '| %', extra_text + '!finished!\n ')
    else:
        if total_count <= units_:
            if total_count > 0:
                print('\r', end='')
                print('|', end="", flush=True)
                str_ = '-' * current_count
                str_ = str_ + ' ' * (units_ - current_count)
                print(str_, end="", flush=True)
                print('| % ', extra_text, end="", flush=True)
        else:
            percentage_ = int((current_count / total_count) * 100)
            if percentage_ / display_each_percent % 1 == 0:
                if 0 < percentage_ <= 100:
                    print('\r', end='')
                    print('|', end="", flush=True)
                    str_ = '-' * int(percentage_ / display_each_percent)
                    str_ = str_ + ' ' * (units_ - int(percentage_ / display_each_percent))
                    print(str_, end="", flush=True)
                    print('| % ', extra_text, end="", flush=True)
def list_files(path_, filter_str='*'):
    file_list = sorted(glob.glob(str(path_ + filter_str)))
    return file_list
def list_folders(path_):
    return next(os.walk(path_))[1]
def list_files_recursive(path_, filter_str=None):
    # create list of raw spectra files
    file_list = []
    # r=root, d=directories, f = files
    if filter_str is None:
        for r, d, f in os.walk(path_):
            for file in f:
                filename_ = os.path.join(r, file)
                file_list.append(filename_.replace('\\','/'))
    else:
        for r, d, f in os.walk(path_):
            for file in f:
                if filter_str in file:
                    filename_ = os.path.join(r, file)
                    file_list.append(filename_.replace('\\', '/'))
    return sorted(file_list)
def coincidence(arr_1,arr_2):
    # only coincidences
    check_ = arr_1 * arr_2
    check_[check_ == check_] = 1

    arr_1_checked = arr_1 * check_
    arr_2_checked = arr_2 * check_

    return arr_1_checked[~np.isnan(arr_1_checked)], arr_2_checked[~np.isnan(arr_2_checked)]
def regrid_1D_to_2D(array_1D_values, array_1D_x, array_1D_y, array_2D_x, array_2D_y,
                    show_progress=True, nodata_value=np.nan):
    """
    Regrids a 1D array with 1D coordinates (x and y) into a 2D array with the x and y grid in the same scale.
    If multiple array_1D_values are found to fit inside any 2D grid box, the mean of these values will be inserted.
    If no array_1D_values are found to fit inside any 2D grid box, nodata_value will be inserted.
    :param array_1D_values: 1D numpy array with the values to be inserted into the output array, where they fit
    :param array_1D_x: 1D numpy array with the x coordinate values. Must be the same shape as array_1D_values
    :param array_1D_y: 1D numpy array with the y coordinate values. Must be the same shape as array_1D_values
    :param array_2D_x: 2D numpy array with the x coordinate values.
    :param array_2D_y: 2D numpy array with the y coordinate values. Must be the same shape as array_2D_x
    :param show_progress: Bool. If true a progress bar will be shown during processing.
    :param nodata_value: float or integer to be placed in the output array when no values where found inside 2D grid box
    :return: 2D array of array_1D_values
    """
    # check that the shapes are correct
    if array_2D_x.shape != array_2D_y.shape:
        raise ValueError('2D shapes are not equal')
    if array_1D_values.shape == array_1D_x.shape == array_1D_y.shape:
        pass
    else:
        raise ValueError('1D shapes are not equal')
    # define output shape
    rows_, cols_ = array_2D_x.shape

    # create output array
    output_array = np.ones((rows_, cols_), dtype=float) * nodata_value

    # create 2D vector of all 1D arrays
    vector_2D = np.column_stack((array_1D_y, array_1D_x, array_1D_values))
    vector_2D_y_sorted = array_2D_sort_ascending_by_column(vector_2D, 0)

    for r_2D in range(rows_-1):
        if show_progress: p_progress_bar(r_2D,rows_-1)
        for c_2D in range(cols_-1):
            y_start = array_2D_y[r_2D, c_2D]
            y_stop = array_2D_y[r_2D+1, c_2D]
            x_start = array_2D_x[r_2D, c_2D]
            x_stop = array_2D_x[r_2D, c_2D+1]

            r_1D_1 = time_to_row_sec(vector_2D_y_sorted[:,0], y_start)
            r_1D_2 = time_to_row_sec(vector_2D_y_sorted[:,0], y_stop)

            if r_1D_1 == r_1D_2:
                continue

            vector_2D_x_sorted_sub = array_2D_sort_ascending_by_column(vector_2D[r_1D_1:r_1D_2,1:], 0)

            c_1D_1 = time_to_row_sec(vector_2D_x_sorted_sub[:,0], x_start)
            c_1D_2 = time_to_row_sec(vector_2D_x_sorted_sub[:,0], x_stop)

            if c_1D_1 == c_1D_2:
                continue

            output_array[r_2D, c_2D] = np.nanmean(vector_2D_x_sorted_sub[c_1D_1:c_1D_2,1])

    return output_array
def array_2d_fill_gaps_by_interpolation_linear(array_):

    rows_ = array_.shape[0]
    cols_ = array_.shape[1]
    output_array_X = np.zeros((rows_, cols_), dtype=float)
    output_array_Y = np.zeros((rows_, cols_), dtype=float)

    row_sum = np.sum(array_, axis=1)
    col_index = np.arange(array_.shape[1])

    col_sum = np.sum(array_, axis=0)
    row_index = np.arange(array_.shape[0])

    for r_ in range(array_.shape[0]):
        if row_sum[r_] != row_sum[r_]:
            # get X direction interpolation
            coin_out = coincidence(col_index, array_[r_, :])
            if coin_out[0].shape[0] > 0:
                output_array_X[r_, :][np.isnan(array_[r_, :])] = interpolate_1d(
                    col_index[np.isnan(array_[r_, :])], coin_out[0], coin_out[1])

    for c_ in range(array_.shape[1]):
        if col_sum[c_] != col_sum[c_]:
            # get Y direction interpolation
            coin_out = coincidence(row_index, array_[:, c_])
            if coin_out[0].shape[0] > 0:
                output_array_Y[:, c_][np.isnan(array_[:, c_])] = interpolate_1d(
                    row_index[np.isnan(array_[:, c_])], coin_out[0], coin_out[1])

    output_array = np.array(array_)
    output_array[np.isnan(array_)] = 0

    return output_array + ((output_array_X + output_array_Y)/2)
def array_2d_fill_gaps_by_interpolation_cubic(array_):

    rows_ = array_.shape[0]
    cols_ = array_.shape[1]
    output_array_X = np.zeros((rows_, cols_), dtype=float)
    output_array_Y = np.zeros((rows_, cols_), dtype=float)

    row_sum = np.sum(array_, axis=1)
    col_index = np.arange(array_.shape[1])

    col_sum = np.sum(array_, axis=0)
    row_index = np.arange(array_.shape[0])

    for r_ in range(array_.shape[0]):
        if row_sum[r_] != row_sum[r_]:
            # get X direction interpolation
            coin_out = coincidence(col_index, array_[r_, :])
            if coin_out[0].shape[0] > 0:
                interp_function = interp1d(coin_out[0], coin_out[1], kind='cubic')
                output_array_X[r_, :][np.isnan(array_[r_, :])] = interp_function(col_index[np.isnan(array_[r_, :])])

    for c_ in range(array_.shape[1]):
        if col_sum[c_] != col_sum[c_]:
            # get Y direction interpolation
            coin_out = coincidence(row_index, array_[:, c_])
            if coin_out[0].shape[0] > 0:
                interp_function = interp1d(coin_out[0], coin_out[1], kind='cubic')
                output_array_Y[:, c_][np.isnan(array_[:, c_])] = interp_function(row_index[np.isnan(array_[:, c_])])

    output_array = np.array(array_)
    output_array[np.isnan(array_)] = 0

    return output_array + ((output_array_X + output_array_Y)/2)
def combine_2_time_series(time_1_reference, data_1, time_2, data_2,
                          forced_time_step=None, forced_start_time=None, forced_stop_time=None,
                          cumulative_var_1=False, cumulative_var_2=False):
    """
    takes two data sets with respective time series, and outputs the coincident stamps from both data sets
    It does this by using mean_discrete() for both sets with the same start stamp and averaging time, the averaging time
    is the forced_time_step
    :param time_1_reference: 1D array, same units as time_2, this series will define the returned time step reference
    :param data_1: can be 1D or 2D array, first dimention most be same as time_1
    :param time_2: 1D array, same units as time_1
    :param data_2: can be 1D or 2D array, first dimention most be same as time_2
    :param window_: optional, if 0 (default) the values at time_1 and time_2 most match exactly, else, the match can
                    be +- window_
    :param forced_time_step: if not none, the median of the differential of the time_1_reference will be used
    :param forced_start_time: if not none, the returned series will start at this time stamp
    :param forced_stop_time: if not none, the returned series will stop at this time stamp
    :param cumulative_var_1: True is you want the variable to be accumulated instead of means, only of 1D data
    :param cumulative_var_2: True is you want the variable to be accumulated instead of means, only of 1D data
    :return: Index_averaged_1: 1D array, smallest coincident time, without time stamp gaps
    :return: Values_mean_1: same shape as data_1 both according to Index_averaged_1 times
    :return: Values_mean_2: same shape as data_2 both according to Index_averaged_1 times
    """

    # define forced_time_step
    if forced_time_step is None:
        forced_time_step = np.median(np.diff(time_1_reference))

    # find time period
    if forced_start_time is None:
        first_time_stamp = max(np.nanmin(time_1_reference), np.nanmin(time_2))
    else:
        first_time_stamp = forced_start_time
    if forced_stop_time is None:
        last_time_stamp = min(np.nanmax(time_1_reference), np.nanmax(time_2))
    else:
        last_time_stamp = forced_stop_time

    # do the averaging
    print('starting averaging of data 1')
    if cumulative_var_1:
        Index_averaged_1, Values_mean_1 = mean_discrete(time_1_reference, data_1, forced_time_step,
                                                        first_time_stamp, last_index=last_time_stamp,
                                                        cumulative_parameter_indx=0)
    else:
        Index_averaged_1, Values_mean_1 = mean_discrete(time_1_reference, data_1, forced_time_step,
                                                        first_time_stamp, last_index=last_time_stamp)
    print('starting averaging of data 2')
    if cumulative_var_2:
        Index_averaged_2, Values_mean_2 = mean_discrete(time_2, data_2, forced_time_step,
                                                        first_time_stamp, last_index=last_time_stamp,
                                                        cumulative_parameter_indx=0)
    else:
        Index_averaged_2, Values_mean_2 = mean_discrete(time_2, data_2, forced_time_step,
                                                        first_time_stamp, last_index=last_time_stamp)


    # check that averaged indexes are the same
    if np.nansum(np.abs(Index_averaged_1 - Index_averaged_2)) != 0:
        print('error during averaging of series, times do no match ????')
        return None, None, None

    # return the combined, trimmed data
    return Index_averaged_1, Values_mean_1, Values_mean_2
def split_str_chunks(s, n):
    """Produce `n`-character chunks from `s`."""
    out_list = []
    for start in range(0, len(s), n):
        out_list.append(s[start:start+n])
    return out_list
def coincidence_multi(array_list):
    # only coincidences
    parameters_list = array_list

    check_ = parameters_list[0]
    for param_ in parameters_list[1:]:
        check_ = check_ * param_
    check_[check_ == check_] = 1
    new_arr_list = []
    for param_ in parameters_list:
        new_arr_list.append(param_ * check_)
        check_ = check_ * param_
    # delete empty rows_
    list_list = []
    for param_ in parameters_list:
        t_list = []
        for i in range(check_.shape[0]):
            if check_[i] == check_[i]:
                t_list.append(param_[i])
        list_list.append(t_list)
    # concatenate
    ar_list = []
    for ii in range(len(parameters_list)):
        ar_list.append(np.array(list_list[ii]))
    return ar_list
def coincidence_zero(arr_1,arr_2):
    # only coincidences
    check_ = arr_1 * arr_2
    # delete empty rows_
    list_1 = []
    list_2 = []
    for i in range(check_.shape[0]):
        if check_[i] != 0:
            list_1.append(arr_1[i])
            list_2.append(arr_2[i])
    return np.array(list_1),np.array(list_2)
def discriminate(X_, Y_, Z_, value_disc_list, discrmnt_invert_bin = False):
    if discrmnt_invert_bin:
        Z_mask = np.ones(Z_.shape[0])
        Z_mask[Z_ > value_disc_list[0]] = np.nan
        Z_mask[Z_ >= value_disc_list[1]] = 1

        Y_new = Y_ * Z_mask
        X_new = X_ * Z_mask

    else:
        Z_mask = np.ones(Z_.shape[0])
        Z_mask[Z_ < value_disc_list[0]] = np.nan
        Z_mask[Z_ > value_disc_list[1]] = np.nan

        Y_new = Y_ * Z_mask
        X_new = X_ * Z_mask

    return X_new, Y_new
def ox_nox_calc_save_data(filename_, o3_index, no_index, no2_index, name_add):
    header_, values_, time_str = load_data_to_return_return(filename_)
    time_sec = time_str_to_seconds(time_str, '%d-%m-%Y_%H:%M')

    O3_ = values_[:,o3_index]
    NO2_ = values_[:,no2_index]
    NO_ = values_[:,no_index]

    Ox_ = O3_ + NO2_
    NOx_ = NO_ + NO2_

    values_new = np.column_stack((values_,Ox_,NOx_))
    header_new = np.append(header_,'Ox_ppb')
    header_new = np.append(header_new,'NOx_ppb')


    output_filename = filename_.split('.')[0]
    output_filename += name_add + '.csv'
    save_array_to_disk(header_new[2:], time_sec, values_new[:,2:], output_filename)
def add_ratio_save_data(filename_, nominator_index, denominator_index, ratio_name, name_add, normalization_value=1.):
    header_, values_, time_str = load_data_to_return_return(filename_)
    time_sec = time_str_to_seconds(time_str, '%d-%m-%Y_%H:%M')

    nominator_data = values_[:,nominator_index]
    denominator_data = values_[:,denominator_index]

    ratio_ = normalization_value * nominator_data / denominator_data

    values_new = np.column_stack((values_,ratio_))
    header_new = np.append(header_,ratio_name)

    output_filename = filename_.split('.')[0]
    output_filename += name_add + '.csv'
    save_array_to_disk(header_new[2:], time_sec, values_new[:,2:], output_filename)
def add_ratio_to_values(header_, values_, nominator_index, denominator_index, ratio_name, normalization_value=1.):
    nominator_data = values_[:,nominator_index]
    denominator_data = values_[:,denominator_index]

    ratio_ = normalization_value * nominator_data / denominator_data

    values_new = np.column_stack((values_,ratio_))
    header_new = np.append(header_,ratio_name)

    return header_new, values_new
def bin_data(x_val_org,y_val_org, start_bin_edge=0, bin_size=1, min_bin_population=1):
    # get coincidences only
    x_val,y_val = coincidence(x_val_org,y_val_org)
    # combine x and y in matrix
    M_ = np.column_stack((x_val,y_val))
    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(x_val.shape[0]-1):
        if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
            if x_val[x+1] < x_val[x]:
                always_ascending = 0
    if always_ascending == 0:
        M_sorted = M_[M_[:,0].argsort()] # sort by first column
        M_ = M_sorted
    # convert data to list of bins
    y_binned = []
    x_binned = []
    last_row = 0
    last_row_temp = last_row
    while start_bin_edge <= np.nanmax(x_val):
        y_val_list = []
        for row_ in range(last_row, M_.shape[0]):
            if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                if M_[row_, 1] == M_[row_, 1]:
                    y_val_list.append(M_[row_, 1])
                    last_row_temp = row_
            if M_[row_, 0] >= start_bin_edge + bin_size:
                last_row_temp = row_
                break
        x_binned.append(start_bin_edge)
        if len(y_val_list) >= min_bin_population:
            y_binned.append(y_val_list)
        else:
            y_binned.append([])
        start_bin_edge += bin_size
        last_row = last_row_temp
    # add series
    if bin_size >= 1:
        x_binned_int = np.array(x_binned, dtype=int)
    else:
        x_binned_int = x_binned
    return x_binned_int, y_binned
def add_weekend_discrimination_save_data(filename_):
    header_, values_, time_str = load_data_to_return_return(filename_)
    time_sec = time_str_to_seconds(time_str, '%d-%m-%Y_%H:%M')

    week_end_bin = np.zeros(values_.shape[0])
    week_end_bin[values_[:,2] != values_[:,2]] = np.nan
    week_end_bin[values_[:,2] == 6] = 1
    week_end_bin[values_[:,2] == 7] = np.nan

    values_new = np.column_stack((values_,week_end_bin))
    header_new = np.append(header_,'weekday_weekend')


    output_filename = filename_.split('.')[0]
    output_filename += '_3.csv'
    save_array_to_disk(header_new[2:], time_sec, values_new[:,2:], output_filename)
def save_data_in_two_files_day_night(filename_,day_night_range_tuple):

    header_, values_, time_str = load_data_to_return_return(filename_)

    day_data, night_data = day_night_discrimination(values_[:,1],values_[:,2:],day_night_range_tuple)
    # day
    new_filename_day = filename_.split('.')[0] + '_day.csv'
    save_array_to_disk(header_[2:], time_str_to_seconds(time_str, '%d-%m-%Y_%H:%M'), day_data, new_filename_day)
    # night
    new_filename_night = filename_.split('.')[0] + '_night.csv'
    save_array_to_disk(header_[2:], time_str_to_seconds(time_str, '%d-%m-%Y_%H:%M'), night_data, new_filename_night)
def student_t_test(arr_1, arr_2):
    return ttest_ind(arr_1, arr_2, nan_policy='omit')
def k_means_clusters(array_, cluster_number, forced_centers=None):
    if forced_centers is None:
        centers_, x = kmeans(array_,cluster_number)
        data_id, x = vq(array_, centers_)
        return centers_, data_id
    else:
        data_id, x = vq(array_, forced_centers)
        return forced_centers, data_id
def grid_(x, y, z, resX=100, resY=100):
    "Convert 3 column data to matplotlib grid"
    xi = np.linspace(min(x), max(x), resX)
    yi = np.linspace(min(y), max(y), resY)
    Z = matplotlib.mlab.griddata(x, y, z, xi, yi)
    X, Y = np.meshgrid(xi, yi)
    return X, Y, Z
def find_max_index_2d_array(array_):
    return np.unravel_index(np.nanargmax(array_, axis=None), array_.shape)
def find_min_index_2d_array(array_):
    return np.unravel_index(np.nanargmin(array_, axis=None), array_.shape)
def find_max_index_1d_array(array_):
    return np.nanargmax(array_, axis=None)
def find_min_index_1d_array(array_):
    return np.nanargmin(array_, axis=None)
def time_series_interpolate_discrete(Index_, Values_, index_step, first_index,
                                     position_=0., last_index=None):
    """
    this will average values from Values_ that are between Index_[n:n+avr_size)
    :param Index_: n by 1 numpy array to look for position,
    :param Values_: n by m numpy array, values to be averaged
    :param index_step: in same units as Index_
    :param first_index: is the first discrete index on new arrays.
    :param position_: will determine where is the stamp located; 0 = beginning, .5 = mid, 1 = top (optional, default = 0)
    :param last_index: in case you want to force the returned series to some fixed period/length
    :return: Index_averaged, Values_averaged
    """

    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(Index_.shape[0]-1):
        if Index_[x]==Index_[x] and Index_[x+1]==Index_[x+1]:
            if Index_[x+1] < Index_[x]:
                always_ascending = 0
    if always_ascending == 0:
        MM_ = np.column_stack((Index_,Values_))
        MM_sorted = MM_[MM_[:,0].argsort()] # sort by first column
        Index_ = MM_sorted[:,0]
        Values_ = MM_sorted[:,1:]

    # error checking!
    if Index_.shape[0] != Values_.shape[0]:
        print('error during shape check! Index_.shape[0] != Values_.shape[0]')
        return None, None
    if Index_[-1] < first_index:
        print('error during shape check! Index_[-1] < first_index')
        return None, None


    # initialize output matrices
    if last_index is None:
        final_index = np.nanmax(Index_)
    else:
        final_index = last_index

    total_averaged_rows = int((final_index-first_index) / index_step) + 1
    if len(Values_.shape) == 1:
        Values_mean = np.zeros(total_averaged_rows)
        Values_mean[:] = np.nan
    else:
        Values_mean = np.zeros((total_averaged_rows,Values_.shape[1]))
        Values_mean[:,:] = np.nan
    Index_interp = np.zeros(total_averaged_rows)
    for r_ in range(total_averaged_rows):
        Index_interp[r_] = first_index + (r_ * index_step)

    Index_interp -= (position_ * index_step)

    Values_interp = interpolate_1d(Index_interp, Index_, Values_)

    Index_interp = Index_interp + (position_ * index_step)

    return Index_interp, Values_interp
def array_2D_sort_ascending_by_column(array_, column_=0):
    array_sorted = array_[array_[:, column_].argsort()]
    return array_sorted
def match_array_by_index(master_index, array_index, array_data, exact_match=True):
    """
    returns an array that is the same size as master_index in the first dimension, but same size of other dimensions
    (if any) for array_values. It is similar to an interpolation, but no interpolation is done, only exact matches of
    the data based on the indexes. Will fill with nan if array_index has indexes not found in array_index
    :param master_index: 1D array. MUST BE ASCENDING.
    :param array_index: 1D array in the same scale as with master, but not the same domain necessarily. MUST BE ASCENDING
    :param array_data: nD array with the first dimension equal to array_index
    :param exact_match: bool. If true exact match of master_index and array_index are required: if false, closest to master_index will be used (regardless of how far)
    :return: nD array with the first dimension equal to array_index, but with data from array_data wherever master_index == array_index
    """
    # check if unique values only
    if len(set(master_index)) != master_index.shape[0] or len(set(array_index)) != array_index.shape[0]:
        print('ERROR! one or both index have repeated values.',
              'Make sure master_index and array_index have only unique ascending values')
        return None

    # check if all index data is ascending
    if np.nanmin(np.diff(master_index)) <= 0 or np.nanmin(np.diff(array_index)) <= 0:
        print('ERROR! one or both index are not in ascending.',
              'Make sure master_index and array_index have only unique ascending values')
        return None

    # check if array_index and array_data has the same size of the first dimension
    if array_index.shape[0] != array_data.shape[0]:
        print('ERROR! the size of the first dimension of array_index and array_data are not equal.',
              'Make sure array_index and array_data have the same first dimension size')
        return None

    if exact_match:
        # create output array
        data_shape = array_data.shape
        output_shape = list(data_shape)
        output_shape[0] = master_index.shape[0]
        output_array = np.zeros(output_shape, dtype=float) * np.nan

        # loop through master_index and look for value in each array_index, increase performance by not looking in found rr_
        last_r_data = 0
        for r_ in range(master_index.shape[0]):
            p_progress_bar(r_,master_index.shape[0])
            for rr_ in range(last_r_data, array_index.shape[0]):
                if master_index[r_] == array_index[rr_]:
                    output_array[r_] = array_data[rr_]
                    last_r_data = rr_
                if array_index[rr_] > master_index[r_]:
                    last_r_data = rr_
                    break
    else:
        # create output array
        data_shape = array_data.shape
        output_shape = list(data_shape)
        output_shape[0] = master_index.shape[0]
        output_array = np.zeros(output_shape, dtype=float) * np.nan

        for r_, index_ in enumerate(master_index):
            p_progress_bar(r_,master_index.shape[0])
            output_array[r_] = array_data[time_to_row_sec(array_index, index_)]

    return output_array
def get_ax_range(ax):
    x_1 = ax.axis()[0]
    x_2 = ax.axis()[1]
    y_1 = ax.axis()[2]
    y_2 = ax.axis()[3]
    return x_1, x_2, y_1, y_2
def interpolate_1d(x, xp, fp, left_=None, right_=None):
    xp_fp_ascending = array_2D_sort_ascending_by_column(np.column_stack((xp, fp)))
    xp_ascending = xp_fp_ascending[:,0]
    fp_ascending = xp_fp_ascending[:,1]
    return np.interp(x, xp_ascending, fp_ascending, left=left_, right=right_)
def interpolate_contiguous_or_closest(x, xp, fp, sort_ascending=True, left_=np.nan, right_=np.nan):
    """
    Perform one-dimensional linear interpolation for monotonically increasing sample points.

    This function returns a one-dimensional piecewise linear interpolant to a function
    with given discrete data points (`xp`, `fp`), evaluated at `x`. It also handles cases
    where there are gaps (represented by NaNs) in the data, interpolating or setting values
    based on the closest valid points.

    Parameters:
    ----------
    :param x: ndarray
        The x-coordinates at which to evaluate the interpolated values.

    :param xp: 1-D sequence of floats
        The x-coordinates of the data points, must be increasing if argument
        `period` is not specified. Otherwise, `xp` is internally sorted after
        normalizing the periodic boundaries with `xp = xp % period`.

    :param fp: 1-D sequence of float or complex
        The y-coordinates of the data points, same length as `xp`.

    :param sort_ascending: bool, optional
        If True, the data will be sorted before interpolation. Default is True.

    :param left_: optional float or complex corresponding to fp
        Value to return for `x < xp[0]`, default is `fp[0]`.

    :param right_: optional float or complex corresponding to fp
        Value to return for `x > xp[-1]`, default is `fp[-1]`.

    Returns:
    ----------
    :return: ndarray
        The interpolated values at the specified `x` coordinates.

    Example:
    ----------
    >> x = np.array([0, 1, 2, 4, 5, 7, 8])
    >> xp = np.array([0, 2, 4, 5, 7, 8])
    >> fp = np.array([0, 1, np.nan, 2, 3, np.nan])
    >> interpolate_contiguous_or_closest(x, xp, fp)
    array([0., 1., 1.5, 2., 2.5, 3., 3.])

    """

    if sort_ascending:
        xp_fp_ascending = array_2D_sort_ascending_by_column(np.column_stack((xp, fp)))
        xp_ascending = xp_fp_ascending[:, 0]
        fp_ascending = xp_fp_ascending[:, 1]
    else:
        xp_ascending = xp
        fp_ascending = fp

    interpolated_ = np.interp(x, xp_ascending, fp_ascending, left=left_, right=right_)

    valid_indices = ~np.isnan(fp_ascending)

    valid_indeces_strides = sliding_window_view(valid_indices, (3,), (1,))
    valid_indeces_strides_sum = np.sum(valid_indeces_strides, axis=1)
    valid_indeces_strides_flag = (valid_indeces_strides_sum == 1) * (valid_indeces_strides[:, 1] == 1)

    if valid_indeces_strides[0, 0] == 1 and ~valid_indeces_strides[0, 1]:
        closest_end_index = np.argmin(np.abs(x - xp_ascending[0]))
        if closest_end_index == 0 or closest_end_index == interpolated_.shape[0] - 1:
            delta_ = x[1] - x[0]
            if np.abs(x[closest_end_index] - xp_ascending[-1]) <= delta_:
                interpolated_[closest_end_index] = fp_ascending[0]
        else:
            interpolated_[closest_end_index] = fp_ascending[0]

    if valid_indeces_strides[-1, 2] == 1 and ~valid_indeces_strides[-1, 1]:
        closest_end_index = np.argmin(np.abs(x - xp_ascending[-1]))
        if closest_end_index == 0 or closest_end_index == interpolated_.shape[0] - 1:
            delta_ = x[-1] - x[-2]
            if np.abs(x[closest_end_index] - xp_ascending[-1]) <= delta_:
                interpolated_[closest_end_index] = fp_ascending[-1]
        else:
            interpolated_[closest_end_index] = fp_ascending[-1]

    for i_, flag_ in enumerate(valid_indeces_strides_flag):
        if flag_:
            interpolated_[np.argmin(np.abs(x - xp_ascending[i_ + 1]))] = fp_ascending[i_ + 1]

    return interpolated_
def interpolate_2d(x_array, y_array, values_array_2d, x_point, y_point):
    """
    Finds the linearly interpolated value (in 2 dimensions) of values_array_2d at point (x_point, y_point).
    Given arrays of x-coordinates, y-coordinates, and corresponding values, this function performs linear
    interpolation in 2D. It computes the interpolated value at the specified point (x_point, y_point) within
    the grid defined by the input arrays. The interpolation is based on the distances between the point of
    interest and the surrounding grid points, and a weighted average is done to calculate the output value.
    The 9 closest points are used for the average with the closest point having a weight of 1 and the farthest
    point a weight of 0, with the rest of the distances linearly distributed. The result is returned as a float.

    Args:
        x_array (numpy.ndarray): 1D or 2D array of x-coordinates.
        y_array (numpy.ndarray): 1D or 2D array of y-coordinates.
        values_array_2d (numpy.ndarray): 2D array of values corresponding to the (x, y) coordinates.
        x_point (float): X-coordinate of the point for interpolation.
        y_point (float): Y-coordinate of the point for interpolation.

    Returns:
        float: Interpolated value at the specified (x_point, y_point).
    """

    # mesh if needed
    if len(x_array.shape) == 1:
        if len(y_array.shape) == 1:
            x_array_2d = np.zeros((x_array.shape[0], y_array.shape[0]))
            for c_ in range(y_array.shape[0]):
                x_array_2d[:, c_] = x_array
        else:
            x_array_2d = np.zeros((x_array.shape[0], y_array.shape[1]))
            for c_ in range(y_array.shape[1]):
                x_array_2d[:, c_] = x_array
    else:
        x_array_2d = x_array
    if len(y_array.shape) == 1:
        y_array_2d = np.zeros((x_array.shape[0], y_array.shape[0]))
        for r_ in range(x_array.shape[0]):
            y_array_2d[r_, :] = y_array
    else:
        y_array_2d = y_array

    # normalize both dimensions
    x_array_2d_norm = normalize_prescribed_min_max(x_array_2d, np.nanmin(x_array_2d), np.nanmax(x_array_2d))
    y_array_2d_norm = normalize_prescribed_min_max(y_array_2d, np.nanmin(y_array_2d), np.nanmax(y_array_2d))

    x_point_norm = normalize_prescribed_min_max(x_point, np.nanmin(x_array_2d), np.nanmax(x_array_2d))
    y_point_norm = normalize_prescribed_min_max(y_point, np.nanmin(y_array_2d), np.nanmax(y_array_2d))

    del_arr_x = np.abs(x_array_2d_norm - x_point_norm)
    del_arr_y = np.abs(y_array_2d_norm - y_point_norm)

    dist_arr_2d = (del_arr_x ** 2 + del_arr_y ** 2) ** 0.5

    closest_x_index, closest_y_index = find_min_index_2d_array(dist_arr_2d)

    weights = 1 - dist_arr_2d[closest_x_index - 1:closest_x_index + 2, closest_y_index - 1:closest_y_index + 2]
    weights_norm = normalize_prescribed_min_max(weights, np.min(weights), np.max(weights))

    output_interpolated_point_value = np.average(values_array_2d[closest_x_index - 1:closest_x_index + 2,
                                                 closest_y_index - 1:closest_y_index + 2],
                                                 weights=weights_norm)
    return output_interpolated_point_value
def list_duplicates(seq):
    tally = defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    list_of_duplicates =  ((key,locs) for key,locs in tally.items() if len(locs)>1)
    for dup in sorted(list_of_duplicates):
        print(dup)
    return sorted(list_of_duplicates)
def series_half_points(series_):
    half_diff = np.diff(series_) / 2
    return series_[:-1] + half_diff
def download_ftp_all_files_in_path(remote_path, output_path):
    # Open the FTP connection
    ftp = ftplib.FTP()
    ftp.cwd(remote_path)

    filenames = ftp.nlst()

    for filename in filenames:
        with open(filename, 'wb') as file:
            ftp.retrbinary('RETR %s' % filename, file.write)

            file.close()

    ftp.quit()
def ftp_put_file(local_filename, remote_path,
                 host_name, user_name, password_):
    from pathlib import Path
    local_file_path = Path(local_filename)

    ftp = ftplib.FTP(host=host_name, user=user_name, passwd=password_)
    ftp.cwd(remote_path)

    with open(local_filename, 'rb') as local_file:
        ftp.storbinary(f'STOR {local_file_path.name}', local_file)

    ftp.quit()
def ftp_get_file(remote_filename, local_path,
                 host_name, user_name, password_):
    from pathlib import Path
    remote_file_path = Path(remote_filename)

    ftp = ftplib.FTP(host=host_name, user=user_name, passwd=password_)

    with open(local_path + remote_file_path.name, 'wb') as local_file:
        ftp.retrbinary(f'RETR {remote_filename}', local_file.write)

    ftp.quit()
def left_justify(words, width):
    """Given an iterable of words, return a string consisting of the words
    left-justified in a line of the given width.

    >>> left_justify(["hello", "world"], 16)
    'hello world     '

    """
    return ' '.join(words).ljust(width)
def justify(words, width):
    """Divide words (an iterable of strings) into lines of the given
    width, and generate them. The lines are fully justified, except
    for the last line, and lines with a single word, which are
    left-justified.

    >>> words = "This is an example of text justification.".split()
    >>> list(justify(words, 16))
    ['This    is    an', 'example  of text', 'justification.  ']

    """
    line = []             # List of words in current line.
    col = 0               # Starting column of next word added to line.
    for word in words:
        if line and col + len(word) > width:
            if len(line) == 1:
                yield left_justify(line, width)
            else:
                # After n + 1 spaces are placed between each pair of
                # words, there are r spaces left over; these result in
                # wider spaces at the left.
                n, r = divmod(width - col + 1, len(line) - 1)
                narrow = ' ' * (n + 1)
                if r == 0:
                    yield narrow.join(line)
                else:
                    wide = ' ' * (n + 2)
                    yield wide.join(line[:r] + [narrow.join(line[r:])])
            line, col = [], 0
        line.append(word)
        col += len(word) + 1
    if line:
        yield left_justify(line, width)
def divergence(field):
    "return the divergence of a n-D field"
    return np.sum(np.gradient(field),axis=0)
def getDriveName(driveletter):
    return subprocess.check_output(["cmd","/c vol "+driveletter]).decode().split("\r\n")[0].split(" ").pop()
def rename_files_to_number_series(file_list, path_output=path_output, zfill_ = 3):
    for i_, filename_ in enumerate(file_list):
        os.rename(filename_, path_output + str(i_).zfill(zfill_) + '.png')
def SCP_get_file(remote_filename_or_path, local_destination_path,
                 user_name, host_name, password_, recursive=False, port_=22):
    if not paramiko_available:
        print('Optional module paramiko was not found, this functions is not available. Please install paramiko')
        return None
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh.connect(hostname=host_name,
                username=user_name,
                password=password_,
                port=port_,
                )

    scp = SCPClient(ssh.get_transport())

    scp.get(remote_filename_or_path, local_destination_path, recursive=recursive)

    scp.close()
def SCP_put_file(local_filename_or_path, remote_destination_path,
                 user_name, host_name, password_, port_=22):
    if not paramiko_available:
        print('Optional module paramiko was not found, this functions is not available. Please install paramiko')
        return None
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh.connect(hostname=host_name,
                username=user_name,
                password=password_,
                port=port_,
                )

    scp = SCPClient(ssh.get_transport(),)

    scp.put(local_filename_or_path, remote_destination_path)

    scp.close()
def list_files_remote(remote_path,
                      user_name, host_name, password_, recursive=False):
    if not paramiko_available:
        print('Optional module paramiko was not found, this functions is not available. Please install paramiko')
        return None
    ssh = SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(AutoAddPolicy())

    ssh.connect(hostname=host_name,
                username=user_name,
                password=password_,
                )


    sftp = ssh.open_sftp()
    sftp.chdir(remote_path)

    file_list = sftp.listdir()

    sftp.close()

    return file_list
def get_array_perimeter_only(array_):
    return np.concatenate([array_[0, :-1], array_[:-1, -1], array_[-1, ::-1], array_[-2:0:-1, 0]])
def int_to_en(num):
    """Given an int32 number, print it in English."""
    d = { 0 : 'zero', 1 : 'one', 2 : 'two', 3 : 'three', 4 : 'four', 5 : 'five',
          6 : 'six', 7 : 'seven', 8 : 'eight', 9 : 'nine', 10 : 'ten',
          11 : 'eleven', 12 : 'twelve', 13 : 'thirteen', 14 : 'fourteen',
          15 : 'fifteen', 16 : 'sixteen', 17 : 'seventeen', 18 : 'eighteen',
          19 : 'nineteen', 20 : 'twenty',
          30 : 'thirty', 40 : 'forty', 50 : 'fifty', 60 : 'sixty',
          70 : 'seventy', 80 : 'eighty', 90 : 'ninety' }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert(0 <= num)

    if (num < 20):
        return d[num]

    if (num < 100):
        if num % 10 == 0: return d[num]
        else: return d[num // 10 * 10] + '-' + d[num % 10]

    if (num < k):
        if num % 100 == 0: return d[num // 100] + ' hundred'
        else: return d[num // 100] + ' hundred and ' + int_to_en(num % 100)

    if (num < m):
        if num % k == 0: return int_to_en(num // k) + ' thousand'
        else: return int_to_en(num // k) + ' thousand, ' + int_to_en(num % k)

    if (num < b):
        if (num % m) == 0: return int_to_en(num // m) + ' million'
        else: return int_to_en(num // m) + ' million, ' + int_to_en(num % m)

    if (num < t):
        if (num % b) == 0: return int_to_en(num // b) + ' billion'
        else: return int_to_en(num // b) + ' billion, ' + int_to_en(num % b)

    if (num % t == 0): return int_to_en(num // t) + ' trillion'
    else: return int_to_en(num // t) + ' trillion, ' + int_to_en(num % t)

    raise AssertionError('num is too large: %s' % str(num))
def find_color_pixel(arr_, red_, green_, blue_):
    arr_ = np.array(arr_, dtype=float)
    color_delta = np.abs(arr_[:,:,0]-red_) + np.abs(arr_[:,:,1]-green_) + np.abs(arr_[:,:,2]-blue_)
    return find_min_index_2d_array(color_delta)
def unicode_symbols():
    text_ = """
    \\u0394	Δ	GREEK CAPITAL LETTER DELTA
    \\u03A9	Ω	GREEK CAPITAL LETTER OMEGA
    \\u03C0	π	GREEK SMALL LETTER PI
    \\u03F4	ϴ	GREEK CAPITAL THETA SYMBOL
    \\u03BB	λ	GREEK SMALL LETTER LAMDA
    \\u03B8	θ	GREEK SMALL LETTER THETA
    \\u03B1	°	DEGREE SYMBOL
    i\\u0302	î	i HAT
    j\\u0302	ĵ	j HAT
    k\\u0302	k̂	k HAT
    u\\u0302	û	u HAT
    
    \\u03B1	α	GREEK SMALL LETTER ALPHA
    \\u03B2	β	GREEK SMALL LETTER BETA
    \\u03B3	γ	GREEK SMALL LETTER GAMMA
    \\u03B4	δ	GREEK SMALL LETTER DELTA
    \\u03B5	ε	GREEK SMALL LETTER EPSILON
    \\u03B6	ζ	GREEK SMALL LETTER ZETA
    \\u03B7	η	GREEK SMALL LETTER ETA
    \\u03B8	θ	GREEK SMALL LETTER THETA
    \\u03B9	ι	GREEK SMALL LETTER IOTA
    \\u03BA	κ	GREEK SMALL LETTER KAPPA
    \\u03BB	λ	GREEK SMALL LETTER LAMDA
    \\u03BC	μ	GREEK SMALL LETTER MU
    \\u03BD	ν	GREEK SMALL LETTER NU
    \\u03BE	ξ	GREEK SMALL LETTER XI
    \\u03BF	ο	GREEK SMALL LETTER OMICRON
    \\u03C0	π	GREEK SMALL LETTER PI
    \\u03C1	ρ	GREEK SMALL LETTER RHO
    \\u03C2	ς	GREEK SMALL LETTER FINAL SIGMA
    \\u03C3	σ	GREEK SMALL LETTER SIGMA
    \\u03C4	τ	GREEK SMALL LETTER TAU
    \\u03C5	υ	GREEK SMALL LETTER UPSILON
    \\u03C6	φ	GREEK SMALL LETTER PHI
    \\u03C7	χ	GREEK SMALL LETTER CHI
    \\u03C8	ψ	GREEK SMALL LETTER PSI
    \\u03C9	ω	GREEK SMALL LETTER OMEGA
    
    \\u0391	Α	GREEK CAPITAL LETTER ALPHA
    \\u0392	Β	GREEK CAPITAL LETTER BETA
    \\u0393	Γ	GREEK CAPITAL LETTER GAMMA
    \\u0394	Δ	GREEK CAPITAL LETTER DELTA
    \\u0395	Ε	GREEK CAPITAL LETTER EPSILON
    \\u0396	Ζ	GREEK CAPITAL LETTER ZETA
    \\u0397	Η	GREEK CAPITAL LETTER ETA
    \\u0398	Θ	GREEK CAPITAL LETTER THETA
    \\u0399	Ι	GREEK CAPITAL LETTER IOTA
    \\u039A	Κ	GREEK CAPITAL LETTER KAPPA
    \\u039B	Λ	GREEK CAPITAL LETTER LAMDA
    \\u039C	Μ	GREEK CAPITAL LETTER MU
    \\u039D	Ν	GREEK CAPITAL LETTER NU
    \\u039E	Ξ	GREEK CAPITAL LETTER XI
    \\u039F	Ο	GREEK CAPITAL LETTER OMICRON
    \\u03A0	Π	GREEK CAPITAL LETTER PI
    \\u03A1	Ρ	GREEK CAPITAL LETTER RHO
    \\u03A3	Σ	GREEK CAPITAL LETTER SIGMA
    \\u03A4	Τ	GREEK CAPITAL LETTER TAU
    \\u03A5	Υ	GREEK CAPITAL LETTER UPSILON
    \\u03A6	Φ	GREEK CAPITAL LETTER PHI
    \\u03A7	Χ	GREEK CAPITAL LETTER CHI
    \\u03A8	Ψ	GREEK CAPITAL LETTER PSI
    \\u03A9	Ω	GREEK CAPITAL LETTER OMEGA
    \\u03F4	ϴ	GREEK CAPITAL THETA SYMBOL
    """

    print(text_)
def pdf_convert_pages_to_images(pdf_filename, pdi=500):
    if not pdf_available:
        print('Optional module pdf2image was not found, this functions is not available. Please install pdf2image')
        return None
    pdf_image_list = pdf2image.convert_from_path(pdf_filename, dpi=pdi)
    root_name_for_images = pdf_filename[:-4]
    for i_, page_image in enumerate(pdf_image_list):
        page_number_str = str(i_).zfill(3)
        page_filename = root_name_for_images + '_' + page_number_str + '.png'
        page_image.save(page_filename)
def raise_error(text_):
    raise ValueError(text_)
def orthogonal_index_to_flat(x_index, y_index, total_number_of_columns):
    if x_index.shape != y_index.shape:
        raise_error('shapes of indexes are not the same')
    if x_index.max() > total_number_of_columns:
        raise_error('x index array has values larger than the defined total number of columns')

    return np.array(x_index + (y_index * total_number_of_columns), dtype=int)
def normalize_prescribed_min_max(arr_, min_, max_):
    return (arr_ - min_) / (max_ - min_)
def show_counts_per_unique(array_, sort_=True, print_=False):
    from collections import Counter
    string_counts = Counter(array_)
    if sort_:
        string_list = []
        count_list = []
        for string, count in string_counts.items():
            string_list.append(string)
            count_list.append(count)

        string_list = np.array(string_list)[np.array(count_list).argsort()[::-1]]
        count_list = np.array(count_list)[np.array(count_list).argsort()[::-1]]
        for string, count in zip(string_list, count_list):
            if print_:
                print(f"{string}: {count}")


    else:
        string_list = []
        count_list = []
        for string, count in string_counts.items():
            string_list.append(string)
            count_list.append(count)
            print(f"{string}: {count}")

    return string_list, count_list




# WRF
def get_WRF_domain_periometer_only(output_filename):
    d01_nc = nc.Dataset(output_filename)
    d01_lat = d01_nc.variables['XLAT'][0,:,:].filled(np.nan)
    d01_lon = d01_nc.variables['XLONG'][0,:,:].filled(np.nan)
    d01_nc.close()

    d01_lat = np.concatenate([d01_lat[0,:-1], d01_lat[:-1,-1], d01_lat[-1,::-1], d01_lat[-2:0:-1,0]])
    d01_lon = np.concatenate([d01_lon[0,:-1], d01_lon[:-1,-1], d01_lon[-1,::-1], d01_lon[-2:0:-1,0]])

    return d01_lat, d01_lon
def plot_WRF_domain(d01_filename, d02_filename, d03_filename, figure_filename='',
                    min_lat=None,max_lat=None,min_lon=None,max_lon=None,
                    d01_color='red',d02_color='green',d03_color='blue',
                    d01_alpha=.7,d02_alpha=.7,d03_alpha=.7,
                    d01_skip=2,d02_skip=8,d03_skip=16,
                    perimeter_only=True, grid_step=10,
                    fig_ax=None,
                    ):

    d01_nc = nc.Dataset(d01_filename)
    d02_nc = nc.Dataset(d02_filename)
    d03_nc = nc.Dataset(d03_filename)

    d01_lat = d01_nc.variables['XLAT'][0,:,:].filled(np.nan)
    d02_lat = d02_nc.variables['XLAT'][0,:,:].filled(np.nan)
    d03_lat = d03_nc.variables['XLAT'][0,:,:].filled(np.nan)
    d01_lon = d01_nc.variables['XLONG'][0,:,:].filled(np.nan)
    d02_lon = d02_nc.variables['XLONG'][0,:,:].filled(np.nan)
    d03_lon = d03_nc.variables['XLONG'][0,:,:].filled(np.nan)

    d01_nc.close()
    d02_nc.close()
    d03_nc.close()


    d01_lat = d01_lat[::d01_skip,::d01_skip]
    d02_lat = d02_lat[::d01_skip,::d01_skip]
    d03_lat = d03_lat[::d01_skip,::d01_skip]
    d01_lon = d01_lon[::d01_skip,::d01_skip]
    d02_lon = d02_lon[::d01_skip,::d01_skip]
    d03_lon = d03_lon[::d01_skip,::d01_skip]


    if perimeter_only:
        d01_lat = np.concatenate([d01_lat[0,:-1], d01_lat[:-1,-1], d01_lat[-1,::-1], d01_lat[-2:0:-1,0]])
        d02_lat = np.concatenate([d02_lat[0,:-1], d02_lat[:-1,-1], d02_lat[-1,::-1], d02_lat[-2:0:-1,0]])
        d03_lat = np.concatenate([d03_lat[0,:-1], d03_lat[:-1,-1], d03_lat[-1,::-1], d03_lat[-2:0:-1,0]])
        d01_lon = np.concatenate([d01_lon[0,:-1], d01_lon[:-1,-1], d01_lon[-1,::-1], d01_lon[-2:0:-1,0]])
        d02_lon = np.concatenate([d02_lon[0,:-1], d02_lon[:-1,-1], d02_lon[-1,::-1], d02_lon[-2:0:-1,0]])
        d03_lon = np.concatenate([d03_lon[0,:-1], d03_lon[:-1,-1], d03_lon[-1,::-1], d03_lon[-2:0:-1,0]])



    if min_lat is None: min_lat = np.nanmin(d01_lat)
    if max_lat is None: max_lat = np.nanmax(d01_lat)
    if min_lon is None: min_lon = np.nanmin(d01_lon)
    if max_lon is None: max_lon = np.nanmax(d01_lon)




    fig, ax, map_ = plot_series_over_map(d01_lat.flatten(),
                                         d01_lon.flatten(),
                                         size_=10,
                                         resolution_='i',
                                         color_=d01_color,
                                         projection_='lcc',
                                         show_grid=True,
                                         min_lat=min_lat,
                                         max_lat=max_lat,
                                         min_lon=min_lon,
                                         max_lon=max_lon,
                                         lake_area_thresh=9999,
                                         alpha_=d01_alpha,
                                         grid_step=grid_step,
                                         fig_ax=fig_ax,
                                         )

    fig, ax, map_ = plot_series_over_map(d02_lat.flatten(),
                                         d02_lon.flatten(),
                                         # resolution_='c',
                                         color_=d02_color,
                                         projection_='lcc',
                                         # map_pad=2,
                                         fig_ax=(fig,ax),
                                         map_=map_,
                                         alpha_=d02_alpha,
                                         grid_step=grid_step,
                                         )

    fig, ax, map_ = plot_series_over_map(d03_lat.flatten(),
                                         d03_lon.flatten(),
                                         # resolution_='c',
                                         color_=d03_color,
                                         projection_='lcc',
                                         # map_pad=2,
                                         fig_ax=(fig,ax),
                                         map_=map_,
                                         alpha_=d03_alpha,
                                         grid_step=grid_step,
                                         )

    plt.tight_layout()
    if figure_filename !='':
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight', dpi=500)
    return fig, ax, map_
def wrf_var_search(wrf_nc, description_str):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_nc_file = nc.Dataset(wrf_nc)
    else:
        wrf_nc_file = wrf_nc

    description_str_lower = description_str.lower()
    for var_ in sorted(wrf_nc_file.variables):
        try:
            if description_str_lower in wrf_nc_file.variables[var_].description.lower():
                print(var_, '|', wrf_nc_file.variables[var_].description)
        except:
            pass
    if original_arg_type_str:
        wrf_nc_file.close()
def calculate_mountain_height_from_WRF(filename_TS, filename_PR,
                                       filename_UU, filename_VV,
                                       filename_TH, filename_QR,
                                       filename_QV, filename_PH,
                                       surface_height=None, reference_height=1000,
                                       half_sigma=True,
                                       return_arrays=False, u_wind_mode='u', range_line_degrees=None,
                                       ):
    """
    calculates H_hat from WRF point output text files
    u_wind_mode: can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most not be none
    if range_line_degrees is not None, u_wind_mode will automatically be set to normal_to_range

    range_line_degrees: degress (decimals) from north, clockwise, of the mountain range line.
    :param filename_TS: fullpath filename of surface variables file, the 10th column must be surface pressure
    :param filename_PR: fullpath filename of pressure file
    :param filename_UU: fullpath filename of u wind file
    :param filename_VV: fullpath filename of v wind file
    :param filename_TH: fullpath filename of potential temperature file
    :param filename_QR: fullpath filename of rain water mixing ratio file
    :param filename_QV: fullpath filename of Water vapor mixing ratio file
    :param filename_PH: fullpath filename of geopotential height file
    :param return_arrays: if true, will return also brunt vaisalla and wind component squared
    :param u_wind_mode: can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most not be none
    :param range_line_degrees: if not None, u_wind_mode will automatically be set to normal_to_range
    :param reference_height: mean height of mountain range
    :return:
    H_hat_2
    """


    # load arrays from text
    SP_array = genfromtxt(filename_TS, dtype=float, skip_header=1)[:,9] / 100 # hPa
    PR_array =  genfromtxt(filename_PR, dtype=float, skip_header=1)[:,1:] / 100 # hPa
    UU_array =  genfromtxt(filename_UU, dtype=float, skip_header=1)[:,1:]
    VV_array =  genfromtxt(filename_VV, dtype=float, skip_header=1)[:,1:]
    TH_array =  genfromtxt(filename_TH, dtype=float, skip_header=1)[:,1:]
    QR_array =  genfromtxt(filename_QR, dtype=float, skip_header=1)[:,1:]
    QV_array =  genfromtxt(filename_QV, dtype=float, skip_header=1)[:,1:]

    if half_sigma:
        Z_array =  genfromtxt(filename_PH, dtype=float, skip_header=1)[:,1:] # already in meters
    else:
        Z_array =  genfromtxt(filename_PH, dtype=float, skip_header=1)[:,1:] # already in meters
        half_diff = np.diff(Z_array, axis=1)/2
        Z_array[:, :-1] = Z_array[:, :-1] + half_diff
        Z_array[:, -1] = Z_array[:, -1] + half_diff[:, -1]

    # calculate arrays
    if range_line_degrees is not None:
        WD_, WS_ = cart_to_polar(VV_array.flatten(), UU_array.flatten())
        WD_delta = WD_ - range_line_degrees

        range_normal_component = WS_ * np.sin(np.deg2rad(WD_delta))
        U_array = range_normal_component.reshape((UU_array.shape[0], UU_array.shape[1]))
    else:
        if u_wind_mode == 'u':
            U_array =  UU_array
        else:
            U_array = np.sqrt(UU_array ** 2 + VV_array ** 2)

    T_array = calculate_temperature_from_potential_temperature(TH_array, PR_array)
    RH_array = calculate_RH_from_QV_T_P(QV_array, T_array, PR_array*100)

    q_s = calculate_saturation_mixing_ratio_g_kg(PR_array, T_array) / 1000
    e_ = gas_const_dry / gas_const_water

    # create output array
    H_hat_2 = np.zeros(PR_array.shape[0], dtype=float)

    # create debug lists
    debug_header = [
        'surface_p',
        'pressure_1000m',
        'ql_0',
        'z__0',
        'th_0',
        'qs_0',
        't__1000',
        'u__1000',
        'ql_1000',
        'z__1000',
        'th_1000',
        'qs_1000',
        'd_ln_TH',
        'd_z',
        'd_q_s',
        'd_q_w',
        'term_1_1',
        'term_1_2',
        'term_2_1',
        'term_2_2',
        'term_2_3',
        'term_3',
        'N_2',
        'H_hat_2'
    ]
    debug_array = np.zeros((PR_array.shape[0], len(debug_header))) * np.nan

    # loop tru time stamps
    for r_ in range(PR_array.shape[0]):
        p_progress_bar(r_, PR_array.shape[0])

        # find surface pressure at this time stamp
        if surface_height is None:
            surface_p = SP_array[r_]
        else:
            surface_p = interpolate_1d(surface_height, Z_array[r_, :], PR_array[r_, :])

        # find pressure at 1000 meters
        pressure_1000m = interpolate_1d(reference_height, Z_array[r_, :], PR_array[r_, :])
        pressure_1000m_index = np.argmin(np.abs(PR_array[r_, :] - pressure_1000m))

        # find extrapolations
        ql_0  = interpolate_1d(np.log(surface_p), np.log(PR_array[r_, :]), QR_array[r_, :])
        z__0  = interpolate_1d(np.log(surface_p), np.log(PR_array[r_, :]), Z_array[r_, :])
        th_0  = interpolate_1d(np.log(surface_p), np.log(PR_array[r_, :]), TH_array[r_, :])
        qs_0  = interpolate_1d(np.log(surface_p), np.log(PR_array[r_, :]), q_s[r_, :])

        t__1000 = interpolate_1d(reference_height, Z_array[r_, :], T_array[r_, :])
        u__1000 = interpolate_1d(reference_height, Z_array[r_, :], U_array[r_, :])
        ql_1000 = interpolate_1d(reference_height, Z_array[r_, :], QR_array[r_, :])
        z__1000 = reference_height
        th_1000 = interpolate_1d(reference_height, Z_array[r_, :], TH_array[r_, :])
        qs_1000 = interpolate_1d(reference_height, Z_array[r_, :], q_s[r_, :])


        # gradients
        d_ln_TH = np.log(th_1000) - np.log(th_0)
        d_z     = z__1000 - z__0
        d_q_s   = qs_1000 - qs_0
        d_q_w   = (d_q_s) + (ql_1000 - ql_0)


        # Brunt - Vaisala
        if np.max(RH_array[r_, pressure_1000m_index:])>= 90:
            # Moist
            term_1_1 = 1 + (  latent_heat_v * qs_1000 / (gas_const_dry * t__1000)  )
            term_1_2 = 1 + (  e_ * (latent_heat_v**2) * qs_1000 /
                              (heat_capacity__Cp * gas_const_dry * (t__1000**2) )  )

            term_2_1 = d_ln_TH / d_z
            term_2_2 = latent_heat_v / (heat_capacity__Cp * t__1000)
            term_2_3 = d_q_s / d_z

            term_3 = d_q_w / d_z

            N_2 = gravity_ * (  (term_1_1 / term_1_2) * (term_2_1 + ( term_2_2 * term_2_3) )  -  term_3  )

        else:
            # Dry
            N_2 = gravity_ * d_ln_TH / d_z

            term_1_1    =   np.nan
            term_1_2    =   np.nan
            term_2_1    =   np.nan
            term_2_2    =   np.nan
            term_2_3    =   np.nan
            term_3      =   np.nan


        # populate each time stamp
        H_hat_2[r_] = N_2 * (reference_height ** 2) / (u__1000 ** 2)

        # debug
        debug_array[r_, 0]  = surface_p
        debug_array[r_, 1]  = pressure_1000m
        debug_array[r_, 2]  = ql_0
        debug_array[r_, 3]  = z__0
        debug_array[r_, 4]  = th_0
        debug_array[r_, 5]  = qs_0
        debug_array[r_, 6]  = t__1000
        debug_array[r_, 7]  = u__1000
        debug_array[r_, 8]  = ql_1000
        debug_array[r_, 9]  = z__1000
        debug_array[r_, 10] = th_1000
        debug_array[r_, 11] = qs_1000
        debug_array[r_, 12] = d_ln_TH
        debug_array[r_, 13] = d_z
        debug_array[r_, 14] = d_q_s
        debug_array[r_, 15] = d_q_w
        debug_array[r_, 16] = term_1_1
        debug_array[r_, 17] = term_1_2
        debug_array[r_, 18] = term_2_1
        debug_array[r_, 19] = term_2_2
        debug_array[r_, 20] = term_2_3
        debug_array[r_, 21] = term_3
        debug_array[r_, 22] = N_2
        debug_array[r_, 23] = N_2 * (reference_height ** 2) / (u__1000 ** 2)


    if return_arrays:
        return H_hat_2, debug_array, debug_header
    else:
        return H_hat_2
def create_virtual_sonde_from_wrf(sonde_dict, filelist_wrf_output,
                                  wrf_filename_time_format = 'wrfout_d03_%Y-%m-%d_%H_%M_%S'):
    # create time array
    filelist_wrf_output_noPath = []
    for filename_ in filelist_wrf_output:
        filelist_wrf_output_noPath.append(filename_.split('/')[-1])
    wrf_time_file_list = np.array(time_str_to_seconds(filelist_wrf_output_noPath, wrf_filename_time_format))

    # create lat and lon arrays
    wrf_domain_file = nc.Dataset(filelist_wrf_output[0])
    # p(sorted(wrf_domain_file.variables))
    # wrf_vars = sorted(wrf_domain_file.variables)
    # for i_ in range(len(wrf_vars)):
    #     try:
    #         print(wrf_vars[i_], '\t\t', wrf_domain_file.variables[wrf_vars[i_]].description)
    #     except:
    #         print(wrf_vars[i_])

    wrf_lat = wrf_domain_file.variables['XLAT'][0, :, :].filled(np.nan)
    wrf_lon = wrf_domain_file.variables['XLONG'][0, :, :].filled(np.nan)
    wrf_lat_U = wrf_domain_file.variables['XLAT_U'][0, :, :].filled(np.nan)
    wrf_lon_U = wrf_domain_file.variables['XLONG_U'][0, :, :].filled(np.nan)
    wrf_lat_V = wrf_domain_file.variables['XLAT_V'][0, :, :].filled(np.nan)
    wrf_lon_V = wrf_domain_file.variables['XLONG_V'][0, :, :].filled(np.nan)
    wrf_domain_file.close()


    # load sonde's profile
    sonde_hght = sonde_dict['hght']  # m ASL
    sonde_pres = sonde_dict['pres']  # hPa
    sonde_time = sonde_dict['time']  # seconds since epoc
    sonde_lati = sonde_dict['lati']  # degrees
    sonde_long = sonde_dict['long']  # degrees


    # create output lists of virtual sonde
    list_p__ = []
    list_hgh = []
    list_th_ = []
    list_th0 = []
    list_qv_ = []
    list_U__ = []
    list_V__ = []
    list_tim = []
    list_lat = []
    list_lon = []


    wrf_point_abs_address_old = 0

    # loop thru real sonde's points
    for t_ in range(sonde_hght.shape[0]):
        p_progress_bar(t_, sonde_hght.shape[0])
        point_hght = sonde_hght[t_]
        point_pres = sonde_pres[t_]
        point_time = sonde_time[t_]
        point_lati = sonde_lati[t_]
        point_long = sonde_long[t_]

        # find closest cell via lat, lon
        index_tuple = find_index_from_lat_lon_2D_arrays(wrf_lat,wrf_lon, point_lati,point_long)
        index_tuple_U = find_index_from_lat_lon_2D_arrays(wrf_lat_U,wrf_lon_U, point_lati,point_long)
        index_tuple_V = find_index_from_lat_lon_2D_arrays(wrf_lat_V,wrf_lon_V, point_lati,point_long)

        # find closest file via time
        file_index = time_to_row_sec(wrf_time_file_list, point_time)

        # open wrf file
        wrf_domain_file = nc.Dataset(filelist_wrf_output[file_index])
        # get pressure array from wrf
        wrf_press = (wrf_domain_file.variables['PB'][0, :, index_tuple[0], index_tuple[1]].data +
                     wrf_domain_file.variables['P'][0, :, index_tuple[0], index_tuple[1]].data) / 100  # hPa

        # find closest model layer via pressure
        layer_index = find_min_index_1d_array(np.abs(wrf_press - point_pres))

        # define point absolute address and check if it is a new point
        wrf_point_abs_address_new = (index_tuple[0], index_tuple[1], file_index, layer_index)
        if wrf_point_abs_address_new != wrf_point_abs_address_old:
            wrf_point_abs_address_old = wrf_point_abs_address_new

            # get wrf data
            index_tuple_full   = (0, layer_index, index_tuple[0], index_tuple[1])
            index_tuple_full_U = (0, layer_index, index_tuple_U[0], index_tuple_U[1])
            index_tuple_full_V = (0, layer_index, index_tuple_V[0], index_tuple_V[1])


            # save to arrays
            list_p__.append(float(wrf_press[layer_index]))
            list_hgh.append(float(point_hght))
            list_th_.append(float(wrf_domain_file.variables['T'][index_tuple_full]))
            list_th0.append(float(wrf_domain_file.variables['T00'][0]))
            list_qv_.append(float(wrf_domain_file.variables['QVAPOR'][index_tuple_full]))
            list_U__.append(float(wrf_domain_file.variables['U'][index_tuple_full_U]))
            list_V__.append(float(wrf_domain_file.variables['V'][index_tuple_full_V]))
            list_tim.append(float(wrf_time_file_list[file_index]))
            list_lat.append(float(wrf_lat[index_tuple[0], index_tuple[1]]))
            list_lon.append(float(wrf_lon[index_tuple[0], index_tuple[1]]))

            wrf_domain_file.close()


    # convert lists to arrays
    array_p__ = np.array(list_p__)
    array_hgh = np.array(list_hgh)
    array_th_ = np.array(list_th_)
    array_th0 = np.array(list_th0)
    array_qv_ = np.array(list_qv_)
    array_U__ = np.array(list_U__)
    array_V__ = np.array(list_V__)
    array_tim = np.array(list_tim)
    array_lat = np.array(list_lat)
    array_lon = np.array(list_lon)

    # calculate derivative variables
    wrf_temp_K = calculate_temperature_from_potential_temperature(array_th_ + array_th0, array_p__)
    wrf_temp_C = kelvin_to_celsius(wrf_temp_K)
    wrf_e = MixR2VaporPress(array_qv_, array_p__*100)
    wrf_td_C = DewPoint(wrf_e)
    wrf_td_C[wrf_td_C > wrf_temp_C] = wrf_temp_C[wrf_td_C > wrf_temp_C]
    wrf_RH = calculate_RH_from_QV_T_P(array_qv_, wrf_temp_K,  array_p__*100)
    wrf_WD, wrf_WS = cart_to_polar(array_V__, array_U__)
    wrf_WD_met = wrf_WD + 180
    wrf_WD_met[wrf_WD_met >= 360] = wrf_WD_met[wrf_WD_met >= 360] - 360
    wrf_WS_knots = ws_ms_to_knots(wrf_WS)

    # create virtual sonde dict
    wrf_sonde_dict = {}
    wrf_sonde_dict['hght'] = array_hgh
    wrf_sonde_dict['pres'] = array_p__
    wrf_sonde_dict['temp'] = wrf_temp_C
    wrf_sonde_dict['dwpt'] = wrf_td_C
    wrf_sonde_dict['sknt'] = wrf_WS_knots
    wrf_sonde_dict['drct'] = wrf_WD_met
    wrf_sonde_dict['relh'] = wrf_RH
    wrf_sonde_dict['time'] = array_tim
    wrf_sonde_dict['lati'] = array_lat
    wrf_sonde_dict['long'] = array_lon



    return wrf_sonde_dict
def create_virtual_sonde_from_wrf_single_point(wrf_nc, point_lat, point_lon):
    if not wrf_available:
        print('Optional module wrf was not found, this functions is not available. Please install wrf')
        return None
    wrf_lat, wrf_lon = wrf_get_lat_lon(wrf_nc)

    sonde_wrf_index = find_index_from_lat_lon_2D_arrays(wrf_lat, wrf_lon, point_lat, point_lon)

    wrf_sonde = create_sonde_dict_from_arrays(
        wrf.getvar(wrf_nc, 'height').data[:,sonde_wrf_index[0],sonde_wrf_index[1]],
        wrf.getvar(wrf_nc, 'pressure').data[:,sonde_wrf_index[0],sonde_wrf_index[1]],
        wrf.getvar(wrf_nc, 'tc').data[:,sonde_wrf_index[0],sonde_wrf_index[1]],
        np.array(wrf.getvar(wrf_nc, 'td'))[:,sonde_wrf_index[0],sonde_wrf_index[1]],
        wrf.getvar(wrf_nc, 'ua').data[:,sonde_wrf_index[0],sonde_wrf_index[1]],
        wrf.getvar(wrf_nc, 'va').data[:,sonde_wrf_index[0],sonde_wrf_index[1]],
    )

    return wrf_sonde
def wrf_get_temp_K(wrf_nc, point_index_tuple_r_c=None):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    if point_index_tuple_r_c is None:
        wrf_press = (wrf_domain_file.variables['PB'][0, :, :, :].data + 300) / 100  # hPa

        wrf_theta = (wrf_domain_file.variables['T'][0, :, :, :].data + 300) # K

        wrf_temp_K = calculate_temperature_from_potential_temperature(wrf_theta, wrf_press)
    else:
        r_, c_ = point_index_tuple_r_c
        wrf_press = (wrf_domain_file.variables['PB'][0, :, r_, c_].data + 300) / 100  # hPa

        wrf_theta = (wrf_domain_file.variables['T'][0, :, r_, c_].data + 300)  # K

        wrf_temp_K = calculate_temperature_from_potential_temperature(wrf_theta, wrf_press)

    if original_arg_type_str:
        wrf_domain_file.close()

    return wrf_temp_K
def wrf_get_press_hPa(wrf_nc):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    wrf_press = (wrf_domain_file.variables['PB'][0, :, :, :].data +
                 wrf_domain_file.variables['P'][0, :, :, :].data) / 100  # hPa

    if original_arg_type_str:
        wrf_domain_file.close()

    return wrf_press
def wrf_get_height_m(wrf_nc, point_index_tuple_r_c=None, square_size_int=None):
    original_arg_type_str = False
    gravity = 9.81
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    if point_index_tuple_r_c is None:
        Z_ = (wrf_domain_file.variables['PH'][0,:,:,:].data + wrf_domain_file.variables['PHB'][0,:,:,:].data) / gravity
        wrf_height = Z_[:-1,:,:] + np.diff(Z_,axis=0)/2

    else:
        if square_size_int is None:
            Z_ = (wrf_domain_file.variables['PH'][0,:,point_index_tuple_r_c[0],point_index_tuple_r_c[1]].data +
                  wrf_domain_file.variables['PHB'][0,:,point_index_tuple_r_c[0],point_index_tuple_r_c[1]].data) / gravity
            wrf_height = Z_[:-1] + np.diff(Z_, axis=0) / 2
        else:
            Z_ = (wrf_domain_file.variables['PH'][0,:,point_index_tuple_r_c[0]:point_index_tuple_r_c[0]+square_size_int,
                  point_index_tuple_r_c[1]:point_index_tuple_r_c[1]+square_size_int].data +
                  wrf_domain_file.variables['PHB'][0,:,point_index_tuple_r_c[0]:point_index_tuple_r_c[0]+square_size_int,
                  point_index_tuple_r_c[1]:point_index_tuple_r_c[1]+square_size_int].data) / gravity
            wrf_height = Z_[:-1] + np.diff(Z_, axis=0) / 2

    if original_arg_type_str:
        wrf_domain_file.close()

    return wrf_height
def wrf_get_terrain_height_m(wrf_nc):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    wrf_height = (wrf_domain_file.variables['PH'][0,0,:,:].data +
                  wrf_domain_file.variables['PHB'][0,0,:,:].data) / gravity_

    if original_arg_type_str:
        wrf_domain_file.close()

    return wrf_height
def wrf_get_water_vapor_mixing_ratio(wrf_nc):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    wrf_QVAPOR = wrf_domain_file.variables['QVAPOR'][0,:,:,:].data

    if original_arg_type_str:
        wrf_domain_file.close()

    return wrf_QVAPOR
def wrf_get_cloud_water_mixing_ratio(wrf_nc):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    wrf_QCLOUD = wrf_domain_file.variables['QCLOUD'][0,:,:,:].data

    if original_arg_type_str:
      wrf_domain_file.close()

    return wrf_QCLOUD
def wrf_get_ice_mixing_ratio(wrf_nc):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    wrf_QICE = wrf_domain_file.variables['QICE'][0,:,:,:].data

    if original_arg_type_str:
        wrf_domain_file.close()

    return wrf_QICE
def wrf_get_lat_lon(wrf_nc):
    original_arg_type_str = False
    if type(wrf_nc) == str:
        original_arg_type_str = True
        wrf_domain_file = nc.Dataset(wrf_nc)
    else:
        wrf_domain_file = wrf_nc

    # get pressure array from wrf
    wrf_lat = wrf_domain_file.variables['XLAT'][0, :, :].filled(np.nan)
    wrf_lon = wrf_domain_file.variables['XLONG'][0, :, :].filled(np.nan)


    if original_arg_type_str:
        wrf_domain_file.close()

    return wrf_lat, wrf_lon
def wrf_rename_files_fix_time_format(filename_original_list, original_character=':', replacement_character='_'):
    for i_, filename_ in enumerate(filename_original_list):
        p_progress_bar(i_, len(filename_original_list))
        new_filename = filename_.replace(original_character,replacement_character)
        os.rename(filename_, new_filename)


# meteorology
def specific_humidity_from_relative_humidity(RH_perc, P_hpa, T_K):
    """
    Calculate specific humidity from relative humidity, pressure, and temperature.

    Parameters:
        RH_perc (float): Relative humidity (in the range of 0 to 100).
        P_hpa (float): Pressure (in hectaPascals).
        T_K (float): Temperature (in Kelvin).

    Returns:
        float: Specific humidity (in kg/kg).
    """

    RH = RH_perc / 100
    P = P_hpa * 100

    # Specific gas constants for dry air and water vapor
    R_d = 287.05  # J/(kg·K)
    R_v = 461.5  # J/(kg·K)

    # Calculate vapor pressure (p_v) in Pa
    p_vs = 610.78 * 10 ** (7.5 * (T_K - 273.15) / (T_K - 273.15 + 237.3))
    p_v = RH * p_vs

    # Calculate partial pressure of dry air (p_a) in Pa
    p_a = P - p_v

    # Calculate mass of water vapor (m_v) in kg
    m_v = (p_v / (R_v * T_K)) * (1 - (p_v / p_a))

    # Calculate mass of dry air (m_a) in kg
    m_a = p_a / (R_d * T_K)

    # Calculate specific humidity (q) in kg/kg
    q = m_v / (m_a + m_v)

    return q
def calculate_moist_Brunt_Vaisala_profile_V1(PR_array_hpa, T_array_K, RH_array_perc, Z_array_m):
    """
    calculates moist Brunt-Vaisala from WRF point output text files
    following equation 36 from Durran and Klemp 1982
    DOI: https://doi.org/10.1175/1520-0469(1982)039<2152:OTEOMO>2.0.CO;2
    :param PR_array_hpa: levels pressure array
    :param T_array_K: ambient temperature array
    :param RH_array_perc: relative humidity array
    :param Z_array_m: height array
    :return:
        N_2 [per second squared]
    """

    # calculate arrays
    TH_array_k = calculate_potential_temperature(T_array_K, PR_array_hpa)
    QR_array_kgkg = specific_humidity_from_relative_humidity(RH_array_perc, PR_array_hpa, T_array_K)

    q_s = calculate_saturation_mixing_ratio_g_kg(PR_array_hpa, T_array_K) / 1000
    e_ = gas_const_dry / gas_const_water

    # get mid-points such that the arrays have the same shape
    T_array_mid = series_half_points(T_array_K)
    q_s_mid = series_half_points(q_s)

    # gradients
    d_ln_TH = np.diff(np.log(TH_array_k))
    d_z     = np.diff(Z_array_m)
    d_q_s   = np.diff(q_s)
    d_q_w   = d_q_s + np.diff(QR_array_kgkg)

    # Brunt - Vaisala
    term_1_1 = 1 + (  latent_heat_v * q_s_mid / (gas_const_dry * T_array_mid)  )
    term_1_2 = 1 + (  e_ * (latent_heat_v**2) * q_s_mid /
                      (heat_capacity__Cp * gas_const_dry * (T_array_mid**2) )  )

    term_2_1 = d_ln_TH / d_z
    term_2_2 = latent_heat_v / (heat_capacity__Cp * T_array_mid)
    term_2_3 = d_q_s / d_z

    term_3 = d_q_w / d_z

    N_2 = gravity_ * (  (term_1_1 / term_1_2) * (term_2_1 + ( term_2_2 * term_2_3) )  -  term_3  )

    return N_2
def calculate_moist_Brunt_Vaisala_profile_V2(PR_array_hpa, TH_array_k, QR_array_kgkg, Z_array_m):
    """
    calculates moist Brunt-Vaisala from WRF point output text files
    following equation 36 from Durran and Klemp 1982
    DOI: https://doi.org/10.1175/1520-0469(1982)039<2152:OTEOMO>2.0.CO;2
    :param PR_array_hpa: levels pressure array
    :param TH_array_k: potential temperature array
    :param QR_array_kgkg: rain water mixing ratio array
    :param Z_array_m: height array
    :return:
        N_2 [per second squared]
    """

    # calculate arrays
    T_array = calculate_temperature_from_potential_temperature(TH_array_k, PR_array_hpa)
    q_s = calculate_saturation_mixing_ratio_g_kg(PR_array_hpa, T_array) / 1000
    e_ = gas_const_dry / gas_const_water

    # get mid-points such that the arrays have the same shape
    T_array_mid = series_half_points(T_array)
    q_s_mid = series_half_points(q_s)

    # gradients
    d_ln_TH = np.diff(np.log(TH_array_k))
    d_z     = np.diff(Z_array_m)
    d_q_s   = np.diff(q_s)
    d_q_w   = d_q_s + np.diff(QR_array_kgkg)

    # Brunt - Vaisala
    term_1_1 = 1 + (  latent_heat_v * q_s_mid / (gas_const_dry * T_array_mid)  )
    term_1_2 = 1 + (  e_ * (latent_heat_v**2) * q_s_mid /
                      (heat_capacity__Cp * gas_const_dry * (T_array_mid**2) )  )

    term_2_1 = d_ln_TH / d_z
    term_2_2 = latent_heat_v / (heat_capacity__Cp * T_array_mid)
    term_2_3 = d_q_s / d_z

    term_3 = d_q_w / d_z

    N_2 = gravity_ * (  (term_1_1 / term_1_2) * (term_2_1 + ( term_2_2 * term_2_3) )  -  term_3  )

    return N_2
def calculate_saturation_vapor_pressure_wexler(T_array_K):
    """
    From Wexler taken from Flatau, P.J.; Walko, R.L.; Cotton, W.R. (1992):
    Wexler, A. (1976). "Vapor pressure formulation for water in range 0 to 100°C. A revision".
                        Journal of Research of the National Bureau of Standards Section A. 80A (5–6): 775–785.
                         doi:10.6028/jres.080a.071.
    Wexler, A. (1977). "Vapor pressure formulation for ice".
                        Journal of Research of the National Bureau of Standards Section A. 81A (1): 5–20.
                        doi:10.6028/jres.081a.003.
    Flatau, P.J.; Walko, R.L.; Cotton, W.R. (1992). "Polynomial fits to saturation vapor pressure".
                        Journal of Applied Meteorology. 31 (12): 1507–13. Bibcode:1992JApMe..31.1507F.
                        doi:10.1175/1520-0450(1992)031<1507:PFTSVP>2.0.CO;2

    :param T_array_K: temperature array in kelvin
    :return: water saturation vapor pressure in hPa
    """
    # for liquid case (T > 273.15)
    G0 = -0.29912729E+4
    G1 = -0.60170128E+4
    G2 =  0.1887643854E+2
    G3 = -0.28354721E-1
    G4 =  0.17838301E-4
    G5 = -0.84150417E-9
    G6 =  0.44412543E-12
    G7 =  0.2858487E+1

    e_s_liquid = np.exp((G0 * (T_array_K ** -2)) +
                        (G1 * (T_array_K ** -1)) +
                         G2 +
                        (G3 * T_array_K) +
                        (G4 * (T_array_K ** 2)) +
                        (G5 * (T_array_K ** 3)) +
                        (G6 * (T_array_K ** 4)) +
                        (G7 * np.log(T_array_K)))
    e_s_liquid[T_array_K <= 273.15] = 0

    # for ice case (T <= 273.15)
    K0 = -0.58653696E+4
    K1 =  0.2224103300E+2
    K2 =  0.13749042E-1
    K3 = -0.34031775E-4
    K4 =  0.26967687E-7
    K5 =  0.6918651E0

    e_s_ice = np.exp(
        (K0 + (K1 + K5*np.log(T_array_K) + (K2 + (K3 + K4*T_array_K)*T_array_K)*T_array_K)*T_array_K)/T_array_K
    )
    e_s_ice[T_array_K > 273.15] = 0

    e_s = e_s_liquid + e_s_ice

    return e_s * 0.01
def calculate_saturation_mixing_ratio_g_kg(P_array_hPa, T_array_K):
    """
    Calculates mixin ratio for saturated state, returns in g/kg
    :param P_array_hPa: pressure array in hPa
    :param T_array_K: temperature array in kelvin
    :return: water vapor saturation mixing ratio in g/kg
    """
    e_s = calculate_saturation_vapor_pressure_wexler(T_array_K) # hPa
    q_s = 0.622 * (e_s / (P_array_hPa - e_s)) # g/kg
    return q_s
def calculate_potential_temperature(T_array_K, P_array_hPa):
    potential_temp = T_array_K * ((1000 / P_array_hPa) ** poisson_)
    return potential_temp
def calculate_equivalent_potential_temperature(T_array_K, P_array_hPa, R_array_kg_over_kg):
    P_o = 1000
    T_e = T_array_K + (latent_heat_v * R_array_kg_over_kg / heat_capacity__Cp)
    theta_e = T_e * ((P_o/P_array_hPa)**poisson_)
    return theta_e
def calculate_temperature_from_potential_temperature(theta_array_K, P_array_hPa):
    temperature_ = theta_array_K * ( (P_array_hPa/1000) ** poisson_ )
    return temperature_
def calculate_mountain_height_from_sonde(sonde_dict):
    """
    calculates H_hat from given values of u_array, v_array, T_array, effective_height, rh_array, q_array, p_array
    """
    # Set initial conditions
    height = 1000  # metres

    # define arrays
    WS_array = ws_knots_to_ms(sonde_dict['SKNT'])
    U_array, V_array = polar_to_cart(sonde_dict['DRCT'], WS_array)
    T_array = celsius_to_kelvin(sonde_dict['TEMP'])
    RH_array = sonde_dict['RELH']
    P_array = sonde_dict['PRES']
    Z_array = sonde_dict['HGHT']
    Q_array = sonde_dict['MIXR']/1000
    TH_array = sonde_dict['THTA']

    # calculated arrays
    q_s = calculate_saturation_mixing_ratio_g_kg(P_array, T_array) / 1000
    e_ = gas_const_dry / gas_const_water

    # gradients
    d_ln_TH = np.gradient(np.log(TH_array))
    d_z = np.gradient(Z_array)
    d_q_s = np.gradient(q_s)

    # Dry Brunt - Vaisala
    N_dry = gravity_ * d_ln_TH / d_z
    N_dry[RH_array >= 90] = 0


    # Moist Brunt - Vaisala
    term_1_1 = 1 + (  latent_heat_v * q_s / (gas_const_dry * T_array)  )
    term_1_2 = 1 + (  e_ * (latent_heat_v**2) * q_s / (heat_capacity__Cp * gas_const_dry * (T_array**2) )  )

    term_2_1 = d_ln_TH / d_z
    term_2_2 = latent_heat_v / (heat_capacity__Cp * T_array)
    term_2_3 = d_q_s / d_z

    term_3 = d_q_s / d_z # should be d_q_w but sonde data has no cloud water data

    N_moist = gravity_ * (  (term_1_1 / term_1_2) * (term_2_1 + ( term_2_2 * term_2_3) )  -  term_3  )
    N_moist[RH_array < 90] = 0

    # define output array
    N_2 = (N_dry + N_moist)**2


    H_hat_2 = N_2 * (height**2) / (U_array**2)

    return H_hat_2
def abs_humidity_calc_save_data(filename_,rh_index,t_index, name_add):
    header_, values_, time_str = load_data_to_return_return(filename_)
    time_sec = time_str_to_seconds(time_str, '%d-%m-%Y_%H:%M')

    c_constant = 2.16679

    RH_ = values_[:,rh_index]
    T_ = values_[:,t_index]

    Pws = 6.116441*10**(7.591386*T_/(T_+240.7263))
    Pw = Pws * RH_

    AH_ = c_constant * Pw/(273.15+T_) # Absolute humidity...

    values_new = np.column_stack((values_,AH_))
    header_new = np.append(header_,'AH g/m3')


    output_filename = filename_.split('.')[0]
    output_filename += name_add + '.csv'
    save_array_to_disk(header_new[2:], time_sec, values_new[:,2:], output_filename)
def calculate_mountain_height_from_era5(era5_pressures_filename, era5_surface_filename, point_lat, point_lon,
                                        return_arrays=False, u_wind_mode='u', range_line_degrees=None,
                                        time_start_str_YYYYmmDDHHMM='',time_stop_str_YYYYmmDDHHMM='',
                                        surface_height=None, reference_height=1000, return_debug_arrays=False):
    """
    calculates H_hat from given values of u_array, v_array, T_array, effective_height, rh_array, q_array, p_array
    u_wind_mode: can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most not be none
    if range_line_degrees is not None, u_wind_mode will automatically be set to normal_to_range

    :param era5_pressures_filename: filename with path of ERA5 pressure levels file
    :param era5_surface_filename: filename with path of ERA5 surface level file (must be for same time period as above
                                    file)
    :param point_lat: latitude that H hat will be computed
    :param point_lon: longitude that H hat will be computed
    :param return_arrays: If true 2 numpy arrays will be returned (time and h_hat_2), else a dictionary will be
                            returned with time (in seconds) keys.
    :param u_wind_mode: String. can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most
                            not be none
    :param range_line_degrees: degress (decimals) from north, clockwise, of the mountain range axes.
    :param time_start_str_YYYYmmDDHHMM: String. If provided, H_hat will be calculated starting from this time (inclusive)
    :param time_stop_str_YYYYmmDDHHMM: String. If provided, H_hat will be calculated until this time (inclusive)
    :param surface_height: If provided the profile will be calculated starting from this height (like to avoid surface
                            effects from affecting the results)
    :param reference_height: mean height of mountain range in meters
    :param return_debug_arrays: If true (and return_arrays also true) extra arrays will be returned for debug purposes.

    :return:
        non dimensional mountain height squared, which equals the square of the Brunt-Vaisala times the square of the
        reference height divided by the square of the wind speed (which might be just the cross mountain).
        The Brunt-Vaisala freq. is calculated using equation 1b (if RH less than 90%) or equation 36 (otherwise) from
        Durran and Klemp 1982.
    """

    # load files
    era5_sur = nc.Dataset(era5_surface_filename, 'r')
    era5_pre = nc.Dataset(era5_pressures_filename, 'r')


    # check if times are the same for both files
    dif_sum = np.sum(np.abs(era5_pre.variables['time'][:] - era5_sur.variables['time'][:]))
    if dif_sum > 0:
        print('Error, times in selected files are not the same')
        return

    # check if lat lon are the same for both files
    dif_sum = np.sum(np.abs(era5_pre.variables['latitude'][:] - era5_sur.variables['latitude'][:]))
    dif_sum = dif_sum + np.sum(np.abs(era5_pre.variables['longitude'][:] - era5_sur.variables['longitude'][:]))
    if dif_sum > 0:
        print('Error, latitude or longitude in selected files are not the same')
        return

    # find lat lon index
    lat_index, lon_index = find_index_from_lat_lon(era5_sur.variables['latitude'][:],
                                                   era5_sur.variables['longitude'][:], [point_lat], [point_lon])
    lat_index = lat_index[0]
    lon_index = lon_index[0]


    # copy arrays
    time_array = time_era5_to_seconds(np.array(era5_sur.variables['time'][:]))
    r_1 = 0
    r_2 = -1
    if time_start_str_YYYYmmDDHHMM != '':
        r_1 = time_to_row_str(time_array, time_start_str_YYYYmmDDHHMM)
    if time_stop_str_YYYYmmDDHHMM != '':
        r_2 = time_to_row_str(time_array, time_stop_str_YYYYmmDDHHMM)
    time_array = time_array[r_1:r_2]

    sp_array = np.array(era5_sur.variables['sp'][r_1:r_2, lat_index, lon_index]) / 100 # hPa
    P_array =  np.array(era5_pre.variables['level'][:]) # hPa
    if range_line_degrees is not None:
        WD_, WS_ = cart_to_polar(np.array(era5_pre.variables['v'][r_1:r_2,:,lat_index,lon_index]).flatten(),
                                 np.array(era5_pre.variables['u'][r_1:r_2,:,lat_index,lon_index]).flatten())
        WD_delta = WD_ - range_line_degrees

        range_normal_component = WS_ * np.sin(np.deg2rad(WD_delta))
        U_array = range_normal_component.reshape((sp_array.shape[0], P_array.shape[0]))
    else:
        if u_wind_mode == 'u':
            U_array =  np.array(era5_pre.variables['u'][r_1:r_2,:,lat_index,lon_index])
        else:
            U_array = np.sqrt(np.array(era5_pre.variables['v'][r_1:r_2,:,lat_index,lon_index]) ** 2 +
                              np.array(era5_pre.variables['u'][r_1:r_2,:,lat_index,lon_index]) ** 2)
    T_array = np.array(era5_pre.variables['t'][r_1:r_2, :, lat_index, lon_index])
    Q_L_array = np.array(era5_pre.variables['crwc'][r_1:r_2, :, lat_index, lon_index])
    RH_array = np.array(era5_pre.variables['r'][r_1:r_2, :, lat_index, lon_index])
    Z_array = np.array(era5_pre.variables['z'][r_1:r_2, :, lat_index, lon_index]) / gravity_


    # calculate arrays
    TH_array = np.zeros((time_array.shape[0], P_array.shape[0]), dtype=float)
    for t_ in range(time_array.shape[0]):
        TH_array[t_,:] = calculate_potential_temperature(T_array[t_,:], P_array[:])

    # calculated arrays
    q_s = calculate_saturation_mixing_ratio_g_kg(P_array, T_array) / 1000
    e_ = gas_const_dry / gas_const_water

    # create output dict
    H_hat_2 = {}

    # create debug lists
    debug_header = [
        'surface_p',
        'pressure_1000m',
        'ql_0',
        'z__0',
        'th_0',
        'qs_0',
        't__1000',
        'u__1000',
        'ql_1000',
        'z__1000',
        'th_1000',
        'qs_1000',
        'd_ln_TH',
        'd_z',
        'd_q_s',
        'd_q_w',
        'rh',
        'term_1_1',
        'term_1_2',
        'term_2_1',
        'term_2_2',
        'term_2_3',
        'term_3',
        'N_2',
        'H_hat_2'
    ]
    debug_array = np.zeros((time_array.shape[0], len(debug_header))) * np.nan


    # loop tru time stamps
    for t_ in range(time_array.shape[0]):
        p_progress_bar(t_,time_array.shape[0])

        # find surface pressure at this time stamp
        if surface_height is None:
            surface_p = sp_array[t_]
        else:
            surface_p = interpolate_1d(surface_height, Z_array[t_, :], P_array)

         # find pressure at 1000 meters
        pressure_1000m = interpolate_1d(reference_height, Z_array[t_, :], P_array)
        pressure_1000m_index = np.argmin(np.abs(P_array - pressure_1000m))

        # find extrapolations
        ql_0  = interpolate_1d(np.log(surface_p), np.log(P_array), Q_L_array[t_, :])
        z__0  = interpolate_1d(np.log(surface_p), np.log(P_array), Z_array[t_, :])
        th_0  = interpolate_1d(np.log(surface_p), np.log(P_array), TH_array[t_, :])
        qs_0  = interpolate_1d(np.log(surface_p), np.log(P_array), q_s[t_, :])

        t__1000 = interpolate_1d(reference_height, Z_array[t_, :], T_array[t_, :])
        u__1000 = interpolate_1d(reference_height, Z_array[t_, :], U_array[t_, :])
        ql_1000 = interpolate_1d(reference_height, Z_array[t_, :], Q_L_array[t_, :])
        z__1000 = reference_height
        th_1000 = interpolate_1d(reference_height, Z_array[t_, :], TH_array[t_, :])
        qs_1000 = interpolate_1d(reference_height, Z_array[t_, :], q_s[t_, :])


        # gradients
        d_ln_TH = np.log(th_1000) - np.log(th_0)
        d_z     = z__1000 - z__0
        d_q_s   = qs_1000 - qs_0
        d_q_w   = d_q_s + (ql_1000 - ql_0)


        #



        # Brunt - Vaisala
        rh_max = np.max(RH_array[t_, pressure_1000m_index:])
        if rh_max >= 90:
            # Moist
            term_1_1 = 1 + (  latent_heat_v * qs_1000 / (gas_const_dry * t__1000)  )
            term_1_2 = 1 + (  e_ * (latent_heat_v**2) * qs_1000 /
                              (heat_capacity__Cp * gas_const_dry * (t__1000**2) )  )

            term_2_1 = d_ln_TH / d_z
            term_2_2 = latent_heat_v / (heat_capacity__Cp * t__1000)
            term_2_3 = d_q_s / d_z

            term_3 = d_q_w / d_z

            N_2 = gravity_ * (  (term_1_1 / term_1_2) * (term_2_1 + ( term_2_2 * term_2_3) )  -  term_3  )


        else:
            # Dry
            N_2 = gravity_ * d_ln_TH / d_z

            term_1_1    =   np.nan
            term_1_2    =   np.nan
            term_2_1    =   np.nan
            term_2_2    =   np.nan
            term_2_3    =   np.nan
            term_3      =   np.nan

        # populate each time stamp
        H_hat_2[time_array[t_]] = N_2 * (reference_height ** 2) / (u__1000 ** 2)
        # debug
        debug_array[t_, 0]  = surface_p
        debug_array[t_, 1]  = pressure_1000m
        debug_array[t_, 2]  = ql_0
        debug_array[t_, 3]  = z__0
        debug_array[t_, 4]  = th_0
        debug_array[t_, 5]  = qs_0
        debug_array[t_, 6]  = t__1000
        debug_array[t_, 7]  = u__1000
        debug_array[t_, 8]  = ql_1000
        debug_array[t_, 9]  = z__1000
        debug_array[t_, 10] = th_1000
        debug_array[t_, 11] = qs_1000
        debug_array[t_, 12] = d_ln_TH
        debug_array[t_, 13] = d_z
        debug_array[t_, 14] = d_q_s
        debug_array[t_, 15] = d_q_w
        debug_array[t_, 16] = rh_max
        debug_array[t_, 17] = term_1_1
        debug_array[t_, 18] = term_1_2
        debug_array[t_, 19] = term_2_1
        debug_array[t_, 20] = term_2_2
        debug_array[t_, 21] = term_2_3
        debug_array[t_, 22] = term_3
        debug_array[t_, 23] = N_2
        debug_array[t_, 24] = N_2 * (reference_height ** 2) / (u__1000 ** 2)

    era5_sur.close()
    era5_pre.close()

    if return_arrays:
        H_hat_2_time = sorted(H_hat_2.keys())
        H_hat_2_time = np.array(H_hat_2_time)
        H_hat_2_vals = np.zeros(H_hat_2_time.shape[0], dtype=float)
        for r_ in range(H_hat_2_time.shape[0]):
            H_hat_2_vals[r_] = H_hat_2[H_hat_2_time[r_]]
        if return_debug_arrays:
            return H_hat_2_time, H_hat_2_vals, debug_array, debug_header
        else:
            return H_hat_2_time, H_hat_2_vals
    else:
        return H_hat_2
def calculate_mountain_height_from_arrays_1(SP_array_hpa, PR_array_hpa,
                                            UU_array_ms, VV_array_ms,
                                            TH_array_k, QR_array_kgkg,
                                            QV_array_kgkg, Z_array_m,
                                            return_arrays=False, u_wind_mode='u', range_line_degrees=None,
                                            reference_height=1000):
    """
    calculates H_hat from WRF point output text files
    u_wind_mode: can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most not be none
    if range_line_degrees is not None, u_wind_mode will automatically be set to normal_to_range
    :param SP_array_hpa: surface pressure array
    :param PR_array_hpa: levels pressure array
    :param UU_array_ms: u wind component array
    :param VV_array_ms: v wind component array
    :param TH_array_k: pothential temperature array
    :param QR_array_kgkg: rain water mixing ratio array
    :param QV_array_kgkg: water vapor mixing ratio array
    :param Z_array_m: height array
    :param return_arrays: bolian, if true it will return brunt-vaisala and cross-mountain wind speed in addition to H_2
    :param u_wind_mode: can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most not be none
    :param range_line_degrees: if not None, u_wind_mode will automatically be set to normal_to_range
    :param reference_height: mean height of mountain range
    :return:
        H_hat_2
    """



    # calculate arrays
    if range_line_degrees is not None:
        WD_, WS_ = cart_to_polar(VV_array_ms.flatten(), UU_array_ms.flatten())
        WD_delta = WD_ - range_line_degrees

        range_normal_component = WS_ * np.sin(np.deg2rad(WD_delta))
        U_array = range_normal_component.reshape((UU_array_ms.shape[0], UU_array_ms.shape[1]))
    else:
        if u_wind_mode == 'u':
            U_array =  UU_array_ms
        else:
            U_array = np.sqrt(UU_array_ms ** 2 + VV_array_ms ** 2)

    T_array = calculate_temperature_from_potential_temperature(TH_array_k, PR_array_hpa)
    RH_array = calculate_RH_from_QV_T_P(QV_array_kgkg, T_array, PR_array_hpa*100)

    q_s = calculate_saturation_mixing_ratio_g_kg(PR_array_hpa, T_array) / 1000
    e_ = gas_const_dry / gas_const_water

    # create output array
    H_hat_2 = np.zeros(PR_array_hpa.shape[0], dtype=float)

    # create debug lists
    debug_header = [
        'surface_p',
        'pressure_1000m',
        'ql_0',
        'z__0',
        'th_0',
        'qs_0',
        't__1000',
        'u__1000',
        'ql_1000',
        'z__1000',
        'th_1000',
        'qs_1000',
        'd_ln_TH',
        'd_z',
        'd_q_s',
        'd_q_w',
        'rh',
        'term_1_1',
        'term_1_2',
        'term_2_1',
        'term_2_2',
        'term_2_3',
        'term_3',
        'N_2',
        'H_hat_2'
    ]
    debug_array = np.zeros((PR_array_hpa.shape[0], len(debug_header))) * np.nan

    # loop tru time stamps
    for r_ in range(PR_array_hpa.shape[0]):
        p_progress_bar(r_, PR_array_hpa.shape[0])

        # find surface pressure at this time stamp
        surface_p = SP_array_hpa[r_]

         # find pressure at 1000 meters
        pressure_1000m = interpolate_1d(reference_height, Z_array_m[r_, :], PR_array_hpa[r_, :])
        pressure_1000m_index = np.argmin(np.abs(PR_array_hpa[r_, :] - pressure_1000m))

        # find extrapolations
        ql_0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), QR_array_kgkg[r_, :])
        z__0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), Z_array_m[r_, :])
        th_0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), TH_array_k[r_, :])
        qs_0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), q_s[r_, :])

        t__1000 = interpolate_1d(reference_height, Z_array_m[r_, :], T_array[r_, :])
        u__1000 = interpolate_1d(reference_height, Z_array_m[r_, :], U_array[r_, :])
        ql_1000 = interpolate_1d(reference_height, Z_array_m[r_, :], QR_array_kgkg[r_, :])
        z__1000 = reference_height
        th_1000 = interpolate_1d(reference_height, Z_array_m[r_, :], TH_array_k[r_, :])
        qs_1000 = interpolate_1d(reference_height, Z_array_m[r_, :], q_s[r_, :])


        # gradients
        d_ln_TH = np.log(th_1000) - np.log(th_0)
        d_z     = z__1000 - z__0
        d_q_s   = qs_1000 - qs_0
        d_q_w   = (d_q_s) + (ql_1000 - ql_0)


        # Brunt - Vaisala
        rh_max = np.max(RH_array[r_, pressure_1000m_index:])
        if rh_max >= 90:
            # Moist
            term_1_1 = 1 + (  latent_heat_v * qs_1000 / (gas_const_dry * t__1000)  )
            term_1_2 = 1 + (  e_ * (latent_heat_v**2) * qs_1000 /
                              (heat_capacity__Cp * gas_const_dry * (t__1000**2) )  )

            term_2_1 = d_ln_TH / d_z
            term_2_2 = latent_heat_v / (heat_capacity__Cp * t__1000)
            term_2_3 = d_q_s / d_z

            term_3 = d_q_w / d_z

            N_2 = gravity_ * (  (term_1_1 / term_1_2) * (term_2_1 + ( term_2_2 * term_2_3) )  -  term_3  )

        else:
            # Dry
            N_2 = gravity_ * d_ln_TH / d_z

            term_1_1 = np.nan
            term_1_2 = np.nan
            term_2_1 = np.nan
            term_2_2 = np.nan
            term_2_3 = np.nan
            term_3 = np.nan

        # populate each time stamp
        H_hat_2[r_] = N_2 * (reference_height ** 2) / (u__1000 ** 2)

        # debug
        debug_array[r_, 0] = surface_p
        debug_array[r_, 1] = pressure_1000m
        debug_array[r_, 2] = ql_0
        debug_array[r_, 3] = z__0
        debug_array[r_, 4] = th_0
        debug_array[r_, 5] = qs_0
        debug_array[r_, 6] = t__1000
        debug_array[r_, 7] = u__1000
        debug_array[r_, 8] = ql_1000
        debug_array[r_, 9] = z__1000
        debug_array[r_, 10] = th_1000
        debug_array[r_, 11] = qs_1000
        debug_array[r_, 12] = d_ln_TH
        debug_array[r_, 13] = d_z
        debug_array[r_, 14] = d_q_s
        debug_array[r_, 15] = d_q_w
        debug_array[r_, 16] = rh_max
        debug_array[r_, 17] = term_1_1
        debug_array[r_, 18] = term_1_2
        debug_array[r_, 19] = term_2_1
        debug_array[r_, 20] = term_2_2
        debug_array[r_, 21] = term_2_3
        debug_array[r_, 22] = term_3
        debug_array[r_, 23] = N_2
        debug_array[r_, 24] = N_2 * (reference_height ** 2) / (u__1000 ** 2)

    if return_arrays:
        return H_hat_2, debug_array, debug_header
    else:
        return H_hat_2
def calculate_mountain_height_from_arrays_2(SP_array_hpa, PR_array_hpa,
                                            UU_array_ms, VV_array_ms,
                                            T_array_k, QR_array_kgkg,
                                            Z_array_m, RH_array_perc,
                                            return_arrays=False, u_wind_mode='u', range_line_degrees=None,
                                            reference_height=1000):
    """
    calculates H_hat from WRF point output text files
    u_wind_mode: can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most not be none
    if range_line_degrees is not None, u_wind_mode will automatically be set to normal_to_range
    :param SP_array_hpa: surface pressure array
    :param PR_array_hpa: levels pressure array
    :param UU_array_ms: u wind component array
    :param VV_array_ms: v wind component array
    :param T_array_k: temperature array
    :param QR_array_kgkg: rain water mixing ratio array
    :param Z_array_m: height array
    :param RH_array_perc: relative humidity array
    :param return_arrays: bolian, if true it will return brunt-vaisala and cross-mountain wind speed in addition to H_2
    :param u_wind_mode: can be u, wind_speed, normal_to_range. If normal_to_range, then range_line most not be none
    :param range_line_degrees: if not None, u_wind_mode will automatically be set to normal_to_range
    :param reference_height: mean height of mountain range
    :return:
        H_hat_2
    """



    # calculate arrays
    if range_line_degrees is not None:
        WD_, WS_ = cart_to_polar(VV_array_ms.flatten(), UU_array_ms.flatten())
        WD_delta = WD_ - range_line_degrees

        range_normal_component = WS_ * np.sin(np.deg2rad(WD_delta))
        U_array = range_normal_component.reshape((UU_array_ms.shape[0], UU_array_ms.shape[1]))
    else:
        if u_wind_mode == 'u':
            U_array =  UU_array_ms
        else:
            U_array = np.sqrt(UU_array_ms ** 2 + VV_array_ms ** 2)

    TH_array_k = np.zeros((T_array_k.shape[0], PR_array_hpa.shape[0]), dtype=float)
    for t_ in range(T_array_k.shape[0]):
        TH_array_k[t_,:] = calculate_potential_temperature(T_array_k[t_,:], PR_array_hpa[:])


    q_s = calculate_saturation_mixing_ratio_g_kg(PR_array_hpa, T_array_k) / 1000
    e_ = gas_const_dry / gas_const_water

    # create output array
    H_hat_2 = np.zeros(PR_array_hpa.shape[0], dtype=float)

    # create debug lists
    N_2_list = []
    u__1000_list = []

    # loop tru time stamps
    for r_ in range(PR_array_hpa.shape[0]):
        p_progress_bar(r_, PR_array_hpa.shape[0])

        # find surface pressure at this time stamp
        surface_p = SP_array_hpa[r_]

         # find pressure at 1000 meters
        pressure_1000m = interpolate_1d(reference_height, Z_array_m[r_, :], PR_array_hpa[r_, :])
        pressure_1000m_index = np.argmin(np.abs(PR_array_hpa[r_, :] - pressure_1000m))

        # find extrapolations
        ql_0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), QR_array_kgkg[r_, :])
        z__0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), Z_array_m[r_, :])
        th_0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), TH_array_k[r_, :])
        qs_0  = interpolate_1d(np.log(surface_p), np.log(PR_array_hpa[r_, :]), q_s[r_, :])

        t__1000 = interpolate_1d(reference_height, Z_array_m[r_, :], T_array_k[r_, :])
        u__1000 = interpolate_1d(reference_height, Z_array_m[r_, :], U_array[r_, :])
        ql_1000 = interpolate_1d(reference_height, Z_array_m[r_, :], QR_array_kgkg[r_, :])
        z__1000 = reference_height
        th_1000 = interpolate_1d(reference_height, Z_array_m[r_, :], TH_array_k[r_, :])
        qs_1000 = interpolate_1d(reference_height, Z_array_m[r_, :], q_s[r_, :])


        # gradients
        d_ln_TH = np.log(th_1000) - np.log(th_0)
        d_z     = z__1000 - z__0
        d_q_s   = qs_1000 - qs_0
        d_q_w   = (d_q_s) + (ql_1000 - ql_0)


        # Brunt - Vaisala
        if np.max(RH_array_perc[r_, pressure_1000m_index:])>= 90:
            # Moist
            term_1_1 = 1 + (  latent_heat_v * qs_1000 / (gas_const_dry * t__1000)  )
            term_1_2 = 1 + (  e_ * (latent_heat_v**2) * qs_1000 /
                              (heat_capacity__Cp * gas_const_dry * (t__1000**2) )  )

            term_2_1 = d_ln_TH / d_z
            term_2_2 = latent_heat_v / (heat_capacity__Cp * t__1000)
            term_2_3 = d_q_s / d_z

            term_3 = d_q_w / d_z

            N_2 = gravity_ * (  (term_1_1 / term_1_2) * (term_2_1 + ( term_2_2 * term_2_3) )  -  term_3  )

        else:
            # Dry
            N_2 = gravity_ * d_ln_TH / d_z

        # populate each time stamp
        H_hat_2[r_] = N_2 * (reference_height ** 2) / (u__1000 ** 2)

        N_2_list.append(N_2)
        u__1000_list.append(u__1000 ** 2)


    if return_arrays:
        return H_hat_2, np.array(N_2_list), np.array(u__1000_list)
    else:
        return H_hat_2
def calculate_dewpoint_from_T_RH(T_, RH_):
    """
    from Magnus formula, using Bolton's constants
    :param T_: ambient temperature [Celsius]
    :param RH_: relative humidity
    :return: Td_ dew point temperature [celsius]
    """
    a = 6.112
    b = 17.67
    c = 243.5

    y_ = np.log(RH_/100) + ((b*T_)/(c+T_))

    Td_ = (c * y_) / (b - y_)

    # fix small error when RH is very high
    try:
        # see if it is an array
        rows_ = T_.shape[0]
        Td_[Td_ > T_] = T_[Td_ > T_]
    except:
        if Td_ > T_:
            Td_ = T_

    return Td_
def calculate_RH_from_QV_T_P(arr_qvapor, arr_temp_K, arr_press_Pa):
    tv_ = 6.11 * e_constant**((2500000/461) * ((1/273) - (1/arr_temp_K)))
    pv_ = arr_qvapor * (arr_press_Pa/100) / (arr_qvapor + 0.622)
    return np.array(100 * pv_ / tv_)
def calculate_profile_input_for_cluster_analysis_from_ERA5(p_profile, t_profile, td_profile, q_profile,
                                                           u_profile, v_profile, h_profile, surface_p):
    """
    takes data from ERA5 for only one time stamp for all pressure levels from 250 to 1000 hPa
    :param p_profile: in hPa
    :param t_profile: in Celsius
    :param td_profile: in Celsius
    :param q_profile: in kg/kg
    :param u_profile: in m/s
    :param v_profile: in m/s
    :param h_profile: in m
    :param surface_p: in hPa
    :return: surface_p, qv_, qu_, tw_, sh_, tt_
    """

    # trim profiles from surface to top
    # find which levels should be included
    levels_total = 0
    for i_ in range(p_profile.shape[0]):
        if p_profile[i_] > surface_p:
            break
        levels_total += 1

    ####################################### find extrapolations
    surface_t = interpolate_1d(np.log(surface_p), np.log(p_profile), t_profile)
    surface_td = interpolate_1d(np.log(surface_p), np.log(p_profile), td_profile)
    surface_q = interpolate_1d(np.log(surface_p), np.log(p_profile), q_profile)
    surface_u = interpolate_1d(np.log(surface_p), np.log(p_profile), u_profile)
    surface_v = interpolate_1d(np.log(surface_p), np.log(p_profile), v_profile)
    surface_h = interpolate_1d(np.log(surface_p), np.log(p_profile), h_profile)

    # create temp arrays
    T_array = np.zeros(levels_total + 1, dtype=float)
    Td_array = np.zeros(levels_total + 1, dtype=float)
    Q_array = np.zeros(levels_total + 1, dtype=float)
    U_array = np.zeros(levels_total + 1, dtype=float)
    V_array = np.zeros(levels_total + 1, dtype=float)
    H_array = np.zeros(levels_total + 1, dtype=float)
    P_array = np.zeros(levels_total + 1, dtype=float)

    T_array[:levels_total] = t_profile[:levels_total]
    Td_array[:levels_total] = td_profile[:levels_total]
    Q_array[:levels_total] = q_profile[:levels_total]
    U_array[:levels_total] = u_profile[:levels_total]
    V_array[:levels_total] = v_profile[:levels_total]
    H_array[:levels_total] = h_profile[:levels_total]
    P_array[:levels_total] = p_profile[:levels_total]

    T_array[-1] = surface_t
    Td_array[-1] = surface_td
    Q_array[-1] = surface_q
    U_array[-1] = surface_u
    V_array[-1] = surface_v
    H_array[-1] = surface_h
    P_array[-1] = surface_p
    ######################################

    r_850 = np.argmin(np.abs(P_array - 850))
    r_500 = np.argmin(np.abs(P_array - 500))

    dp_ = np.abs(np.gradient(P_array))
    tt_ = (T_array[r_850] - (2 * T_array[r_500]) + Td_array[r_850])

    qu_ = np.sum(Q_array * U_array * dp_) / gravity_
    qv_ = np.sum(Q_array * V_array * dp_) / gravity_
    tw_ = np.sum(Q_array * dp_) / gravity_

    del_u = U_array[r_850] - U_array[r_500]
    del_v = V_array[r_850] - V_array[r_500]
    del_z = H_array[r_850] - H_array[r_500]

    sh_ = ((del_u / del_z) ** 2 + (del_v / del_z) ** 2) ** 0.5

    return surface_p, qv_, qu_, tw_, sh_, tt_
def barometric_equation(presb_pa, tempb_k, deltah_m, Gamma=-0.0065):
    """The barometric equation models the change in pressure with
    height in the atmosphere.

    INPUTS:
    presb_k (pa):     The base pressure
    tempb_k (K):      The base temperature
    deltah_m (m):     The height differential between the base height and the
                      desired height
    Gamma [=-0.0065]: The atmospheric lapse rate

    OUTPUTS
    pres (pa):        Pressure at the requested level

    REFERENCE:
    http://en.wikipedia.org/wiki/Barometric_formula
    """

    return presb_pa * \
        (tempb_k/(tempb_k+Gamma*deltah_m))**(grav*m_a/(Rstar_a*Gamma))
def barometric_equation_inv(heightb_m, tempb_k, presb_pa,
                            prest_pa, Gamma=-0.0065):
    """The barometric equation models the change in pressure with height in
    the atmosphere. This function returns altitude given
    initial pressure and base altitude, and pressure change.

    INPUTS:
    heightb_m (m):
    presb_pa (pa):    The base pressure
    tempb_k (K)  :    The base temperature
    deltap_pa (m):    The pressure differential between the base height and the
                      desired height

    Gamma [=-0.0065]: The atmospheric lapse rate

    OUTPUTS
    heightt_m

    REFERENCE:
    http://en.wikipedia.org/wiki/Barometric_formula
    """

    return heightb_m + \
        tempb_k * ((presb_pa/prest_pa)**(Rstar_a*Gamma/(grav*m_a))-1) / Gamma
def Theta(tempk, pres, pref=100000.):
    """Potential Temperature

    INPUTS:
    tempk (K)
    pres (Pa)
    pref: Reference pressure (default 100000 Pa)

    OUTPUTS: Theta (K)

    Source: Wikipedia
    Prints a warning if a pressure value below 2000 Pa input, to ensure
    that the units were input correctly.
    """

    try:
        minpres = min(pres)
    except TypeError:
        minpres = pres

    if minpres < 2000:
        print("WARNING: P<2000 Pa; did you input a value in hPa?")

    return tempk * (pref/pres)**(Rs_da/Cp_da)
def TempK(theta, pres, pref=100000.):
    """Inverts Theta function."""

    try:
        minpres = min(pres)
    except TypeError:
        minpres = pres

    if minpres < 2000:
        print("WARNING: P<2000 Pa; did you input a value in hPa?")

    return theta * (pres/pref)**(Rs_da/Cp_da)
def ThetaE(tempk, pres, e):
    """Calculate Equivalent Potential Temperature
        for lowest model level (or surface)

    INPUTS:
    tempk:      Temperature [K]
    pres:       Pressure [Pa]
    e:          Water vapour partial pressure [Pa]

    OUTPUTS:
    theta_e:    equivalent potential temperature

    References:
    Eq. (9.40) from Holton (2004)
    Eq. (22) from Bolton (1980)
    Michael P. Byrne and Paul A. O'Gorman (2013), 'Land-Ocean Warming
    Contrast over a Wide Range of Climates: Convective Quasi-Equilibrium
    Theory and Idealized Simulations', J. Climate """

    # tempc
    tempc = tempk - degCtoK
    # Calculate theta
    theta = Theta(tempk, pres)

    # T_lcl formula needs RH
    es = VaporPressure(tempc)
    RH = 100. * e / es

    # theta_e needs q (water vapour mixing ratio)
    qv = MixRatio(e, pres)

    # Calculate the temp at the Lifting Condensation Level
    T_lcl = ((tempk-55)*2840 / (2840-(np.log(RH/100)*(tempk-55)))) + 55

    # print "T_lcl :%.3f"%T_lcl

    # DEBUG STUFF ####
    theta_l = tempk * \
        (100000./(pres-e))**(Rs_da/Cp_da)*(tempk/T_lcl)**(0.28*qv)
    # print "theta_L: %.3f"%theta_l

    # Calculate ThetaE
    theta_e = theta_l * np.exp((Lv * qv) / (Cp_da * T_lcl))

    return theta_e
def ThetaE_Bolton(tempk, pres, e, pref=100000.):
    """Theta_E following Bolton (1980)
    INPUTS:
    tempk:      Temperature [K]
    pres:       Pressure [Pa]
    e:          Water vapour partial pressure [Pa]

    See http://en.wikipedia.org/wiki/Equivalent_potential_temperature
    """

    # Preliminary:
    T = tempk
    qv = MixRatio(e, pres)
    Td = DewPoint(e) + degCtoK
    kappa_d = Rs_da / Cp_da

    # Calculate TL (temp [K] at LCL):
    TL = 56 + ((Td-56.)**-1+(np.log(T/Td)/800.))**(-1)

    # print "TL: %.3f"%TL

    # Calculate Theta_L:
    thetaL = T * (pref/(pres-e))**kappa_d*(T/TL)**(0.28*qv)

    # print "theta_L: %.3f"%thetaL

    # put it all together to get ThetaE
    thetaE = thetaL * np.exp((3036./TL-0.78)*qv*(1+0.448*qv))

    return thetaE
def ThetaV(tempk, pres, e):
    """Virtual Potential Temperature

    INPUTS
    tempk (K)
    pres (Pa)
    e: Water vapour pressure (Pa) (Optional)

    OUTPUTS
    theta_v    : Virtual potential temperature
    """

    mixr = MixRatio(e, pres)
    theta = Theta(tempk, pres)

    return theta * (1+mixr/Epsilon) / (1+mixr)
def GammaW(tempk, pres):
    """Function to calculate the moist adiabatic lapse rate (deg C/Pa) based
    on the environmental temperature and pressure.

    INPUTS:
    tempk (K)
    pres (Pa)
    RH (%)

    RETURNS:
    GammaW: The moist adiabatic lapse rate (Deg C/Pa)
    REFERENCE:
    http://glossary.ametsoc.org/wiki/Moist-adiabatic_lapse_rate
    (Note that I multiply by 1/(grav*rho) to give MALR in deg/Pa)

    """

    tempc = tempk-degCtoK
    es = VaporPressure(tempc)
    ws = MixRatio(es, pres)

    # tempv=VirtualTempFromMixR(tempk,ws)
    tempv = VirtualTemp(tempk, pres, es)
    latent = Latentc(tempc)

    Rho = pres / (Rs_da*tempv)

    # This is the previous implementation:
    # A=1.0+latent*ws/(Rs_da*tempk)
    # B=1.0+Epsilon*latent*latent*ws/(Cp_da*Rs_da*tempk*tempk)
    # Gamma=(A/B)/(Cp_da*Rho)

    # This is algebraically identical but a little clearer:
    A = -1. * (1.0+latent*ws/(Rs_da*tempk))
    B = Rho * (Cp_da+Epsilon*latent*latent*ws/(Rs_da*tempk*tempk))
    Gamma = A / B

    return Gamma
def DensHumid(tempk, pres, e):
    """Density of moist air.
    This is a bit more explicit and less confusing than the method below.

    INPUTS:
    tempk: Temperature (K)
    pres: static pressure (Pa)
    mixr: mixing ratio (kg/kg)

    OUTPUTS:
    rho_air (kg/m^3)

    SOURCE: http://en.wikipedia.org/wiki/Density_of_air
    """

    pres_da = pres - e
    rho_da = pres_da / (Rs_da * tempk)
    rho_wv = e/(Rs_v * tempk)

    return rho_da + rho_wv
def Density(tempk, pres, mixr):
    """Density of moist air

    INPUTS:
    tempk: Temperature (K)
    pres: static pressure (Pa)
    mixr: mixing ratio (kg/kg)

    OUTPUTS:
    rho_air (kg/m^3)
    """

    virtualT = VirtualTempFromMixR(tempk, mixr)
    return pres / (Rs_da * virtualT)
def VirtualTemp(tempk, pres, e):
    """Virtual Temperature

    INPUTS:
    tempk: Temperature (K)
    e: vapour pressure (Pa)
    p: static pressure (Pa)

    OUTPUTS:
    tempv: Virtual temperature (K)

    SOURCE: hmmmm (Wikipedia)."""

    tempvk = tempk / (1-(e/pres)*(1-Epsilon))
    return tempvk
def VirtualTempFromMixR(tempk, mixr):
    """Virtual Temperature

    INPUTS:
    tempk: Temperature (K)
    mixr: Mixing Ratio (kg/kg)

    OUTPUTS:
    tempv: Virtual temperature (K)

    SOURCE: hmmmm (Wikipedia). This is an approximation
    based on a m
    """

    return tempk * (1.0+0.6*mixr)
def Latentc(tempc):
    """Latent heat of condensation (vapourisation)

    INPUTS:
    tempc (C)

    OUTPUTS:
    L_w (J/kg)

    SOURCE:
    http://en.wikipedia.org/wiki/Latent_heat#Latent_heat_for_condensation_of_water
    """

    return 1000 * (2500.8 - 2.36*tempc + 0.0016*tempc**2 - 0.00006*tempc**3)
def VaporPressure(tempc, phase="liquid"):
    """Water vapor pressure over liquid water or ice.

    INPUTS:
    tempc: (C) OR dwpt (C), if SATURATION vapour pressure is desired.
    phase: ['liquid'],'ice'. If 'liquid', do simple dew point. If 'ice',
    return saturation vapour pressure as follows:

    Tc>=0: es = es_liquid
    Tc <0: es = es_ice


    RETURNS: e_sat  (Pa)

    SOURCE: http://cires.colorado.edu/~voemel/vp.html (#2:
    CIMO guide (WMO 2008), modified to return values in Pa)

    This formulation is chosen because of its appealing simplicity,
    but it performs very well with respect to the reference forms
    at temperatures above -40 C. At some point I'll implement Goff-Gratch
    (from the same resource).
    """

    over_liquid = 6.112 * np.exp(17.67*tempc/(tempc+243.12))*100.
    over_ice = 6.112 * np.exp(22.46*tempc/(tempc+272.62))*100.
    # return where(tempc<0,over_ice,over_liquid)

    if phase == "liquid":
        # return 6.112*exp(17.67*tempc/(tempc+243.12))*100.
        return over_liquid
    elif phase == "ice":
        # return 6.112*exp(22.46*tempc/(tempc+272.62))*100.
        return np.where(tempc < 0, over_ice, over_liquid)
    else:
        raise NotImplementedError
def SatVap(dwpt, phase="liquid"):
    """This function is deprecated, return ouput from VaporPres"""

    print("WARNING: This function is deprecated, please use VaporPressure()" +
          " instead, with dwpt as argument")
    return VaporPressure(dwpt, phase)
def MixRatio(e, p):
    """Mixing ratio of water vapour
    INPUTS
    e (Pa) Water vapor pressure
    p (Pa) Ambient pressure

    RETURNS
    qv (kg kg^-1) Water vapor mixing ratio`
    """

    return Epsilon * e / (p - e)
def MixR2VaporPress(qv, p):
    """Return Vapor Pressure given Mixing Ratio and Pressure
    INPUTS
    qv (kg kg^-1) Water vapor mixing ratio`
    p (Pa) Ambient pressure

    RETURNS
    e (Pa) Water vapor pressure
    """

    return qv * p / (Epsilon + qv)
def DewPoint(e):
    """ Use Bolton's (1980, MWR, p1047) formulae to find tdew.
    INPUTS:
    e (Pa) Water Vapor Pressure
    OUTPUTS:
    Td (C)
      """

    ln_ratio = np.log(e/611.2)
    Td = ((17.67-ln_ratio)*degCtoK+243.5*ln_ratio)/(17.67-ln_ratio)
    return Td - degCtoK
def WetBulb(tempc, RH):
    """Stull (2011): Wet-Bulb Temperature from Relative Humidity and Air
    Temperature.
    INPUTS:
    tempc (C)
    RH (%)
    OUTPUTS:
    tempwb (C)
    """

    Tw = tempc * np.arctan(0.151977*(RH+8.313659)**0.5) + \
        np.arctan(tempc+RH) - np.arctan(RH-1.676331) + \
        0.00391838*RH**1.5*np.arctan(0.023101*RH) - \
        4.686035

    return Tw
def calculate_liquid_water_terminal_velocity_simple(radious_arr_mm):
    radious_arr_cm = radious_arr_mm / 10
    U_t_0_40 = 1.19e6 * (radious_arr_cm**2)
    U_t_40_600 = 8e3 * (radious_arr_cm)
    U_t_600_ = 2.01e3 * (radious_arr_cm**0.5)

    U_t_cms = U_t_0_40
    U_t_cms[radious_arr_mm>0.04] = U_t_40_600[radious_arr_mm>0.04]
    U_t_cms[radious_arr_mm>0.6] = U_t_600_[radious_arr_mm>0.6]

    return U_t_cms / 100
def calculate_liquid_water_terminal_velocity(radious_arr_mm, T_K=293.15, P_hPa=1013.25):
    radious_arr_cm = radious_arr_mm / 10

    l_o = 6.62e-6  # cm
    n_o = 1.818e-5  # kg m-1 s-1
    p_o = 1013.25  # hPa
    den_o = 1.204  # kg m-3

    n_ = 1.832e-5 * (1 + 0.00266 * (T_K - 296))
    den_ = 0.348 * P_hPa / T_K

    # 0.001 mm to 0.02 mm
    c_ = np.array([10.5035, 1.08750, -0.133245, -0.00659969])
    l_ = l_o * (n_/n_o) * (((p_o * den_o)/(P_hPa * den_))**0.5)
    f_ = (n_o/n_) * (1 + 1.255 * l_ / radious_arr_cm) / (1 + 1.255 * l_o / radious_arr_cm)

    U_T_low = f_ * e_constant ** (
            (c_[0] * ((np.log(2 * radious_arr_cm))**1) ) +
            (c_[1] * ((np.log(2 * radious_arr_cm))**2) ) +
            (c_[2] * ((np.log(2 * radious_arr_cm))**3) ) +
            (c_[3] * ((np.log(2 * radious_arr_cm))**4) )
    )





    # 0.02 mm to 3 mm
    c_ = np.array([6.5639,-1.0391,-1.4001,-0.82736,-0.34277,-0.083072,-0.010583,-0.00054208])
    e_s = (n_o/n_) - 1
    e_c = ((den_o/den_) ** 0.5) - 1
    f_ = 1.104 * e_s + (1.058 * e_c - 1.104 * e_s) * ((6.21 + np.log(radious_arr_cm)) / 5.01) + 1

    U_T_hig = f_ * e_constant ** (
            (c_[0] * ((np.log(2 * radious_arr_cm))**0) ) +
            (c_[1] * ((np.log(2 * radious_arr_cm))**1) ) +
            (c_[2] * ((np.log(2 * radious_arr_cm))**2) ) +
            (c_[3] * ((np.log(2 * radious_arr_cm))**3) ) +
            (c_[4] * ((np.log(2 * radious_arr_cm))**4) ) +
            (c_[5] * ((np.log(2 * radious_arr_cm))**5) ) +
            (c_[6] * ((np.log(2 * radious_arr_cm))**6) ) +
            (c_[7] * ((np.log(2 * radious_arr_cm))**7) )
    )


    U_t_cms = U_T_low
    U_t_cms[radious_arr_mm >= 0.02] = U_T_hig[radious_arr_mm >= 0.02]

    return U_t_cms / 100
def calculate_liquid_water_terminal_velocity_mod(radious_arr_mm, T_K=293.15, P_hPa=1013.25):
    """
    same as calculate_liquid_water_terminal_velocity but with a fix (9.198 m/s) velocity after 2.726 mm radius

    """
    radious_arr_cm = radious_arr_mm / 10

    l_o = 6.62e-6  # cm
    n_o = 1.818e-5  # kg m-1 s-1
    p_o = 1013.25  # hPa
    den_o = 1.204  # kg m-3

    n_ = 1.832e-5 * (1 + 0.00266 * (T_K - 296))
    den_ = 0.348 * P_hPa / T_K

    # 0.001 mm to 0.02 mm
    c_ = np.array([10.5035, 1.08750, -0.133245, -0.00659969])
    l_ = l_o * (n_/n_o) * (((p_o * den_o)/(P_hPa * den_))**0.5)
    f_ = (n_o/n_) * (1 + 1.255 * l_ / radious_arr_cm) / (1 + 1.255 * l_o / radious_arr_cm)

    U_T_low = f_ * e_constant ** (
            (c_[0] * ((np.log(2 * radious_arr_cm))**1) ) +
            (c_[1] * ((np.log(2 * radious_arr_cm))**2) ) +
            (c_[2] * ((np.log(2 * radious_arr_cm))**3) ) +
            (c_[3] * ((np.log(2 * radious_arr_cm))**4) )
    )





    # 0.02 mm to 3 mm
    c_ = np.array([6.5639,-1.0391,-1.4001,-0.82736,-0.34277,-0.083072,-0.010583,-0.00054208])
    e_s = (n_o/n_) - 1
    e_c = ((den_o/den_) ** 0.5) - 1
    f_ = 1.104 * e_s + (1.058 * e_c - 1.104 * e_s) * ((6.21 + np.log(radious_arr_cm)) / 5.01) + 1

    U_T_hig = f_ * e_constant ** (
            (c_[0] * ((np.log(2 * radious_arr_cm))**0) ) +
            (c_[1] * ((np.log(2 * radious_arr_cm))**1) ) +
            (c_[2] * ((np.log(2 * radious_arr_cm))**2) ) +
            (c_[3] * ((np.log(2 * radious_arr_cm))**3) ) +
            (c_[4] * ((np.log(2 * radious_arr_cm))**4) ) +
            (c_[5] * ((np.log(2 * radious_arr_cm))**5) ) +
            (c_[6] * ((np.log(2 * radious_arr_cm))**6) ) +
            (c_[7] * ((np.log(2 * radious_arr_cm))**7) )
    )


    U_t_cms = U_T_low
    U_t_cms[radious_arr_mm >= 0.02] = U_T_hig[radious_arr_mm >= 0.02]

    U_t_cms[radious_arr_mm >= 2.726] = 9.198 * 100

    return U_t_cms / 100
def calculate_liquid_water_terminal_velocity_literature(radious_arr_mm):
    """


    """
    U_t = 9.65 - 10.3 * np.exp(-6 * (radious_arr_mm / 10.))

    return U_t


# unit conversions
def convert_unit_and_save_data_ppb_ugm3(filename_, station_name):
    # https://uk-air.defra.gov.uk/assets/documents/reports/cat06/0502160851_Conversion_Factors_Between_ppb_and.pdf
    # http://www2.dmu.dk/AtmosphericEnvironment/Expost/database/docs/PPM_conversion.pdf

    parameters_unit_scaling = {'11' : 1.96, # O3
                               '10' : 1.25, # NO
                               '9' : 1.88, # NO2
                               '16' : 2.62, # SO2
                               '8' : 1.15} # CO

    new_unit_name = '[$\mu$g/m$^3$]'

    parameter_name_mod = {'9' : 'NO$_2$',
                          '11' : 'O$_3$',
                          '12' : 'PM$_1$$_0$',
                          '13' : 'PM$_2$$_.$$_5$',
                          '7' : 'CO$_2$',
                          '16' : 'SO$_2$',
                          }

    # station_name = 'QF_01'


    data_array = open_csv_file(filename_)
    current_header = data_array[0,:]
    new_header = np.array(current_header)
    v_current = np.array(data_array[1:,:],dtype=float)
    v_new = np.array(v_current)

    for keys_ in parameters_unit_scaling.keys():
        v_new[:, int(keys_)] = v_current[:, int(keys_)] * parameters_unit_scaling[str(keys_)]

    # add station name suffix
    for i_ in range(5,22):
        if str(i_) in parameter_name_mod.keys():
            parameter_name = parameter_name_mod[str(i_)]
        else:
            parameter_name = current_header[i_].split('_')[0]

        if str(i_) in parameters_unit_scaling.keys():
            parameter_unit = new_unit_name
        else:
            parameter_unit = current_header[i_].split('_')[1]

        new_header[i_] = station_name + '_' + parameter_name + '_' + parameter_unit


    data_array[1:,:] = v_new
    data_array[0,:] = new_header

    filename_new = filename_.replace('\\','/').split('/')[-1].split('.')[0] + '_unit_converted.csv'
    current_filename_without_path = filename_.replace('\\','/').split('/')[-1]
    current_filename_path = filename_[:-len(current_filename_without_path)]

    numpy_save_txt(current_filename_path + filename_new, data_array)

    print('done!')
def save_data_with_unit_conversion_ppb_ugm3(file_list_path):
    file_list = sorted(glob.glob(str(file_list_path + '/' + '*.csv')))

    # https://uk-air.defra.gov.uk/assets/documents/reports/cat06/0502160851_Conversion_Factors_Between_ppb_and.pdf
    # http://www2.dmu.dk/AtmosphericEnvironment/Expost/database/docs/PPM_conversion.pdf

    parameters_unit_scaling = {'12' : 1.96, # O3
                               '13' : 1.25, # NO
                               '14' : 1.88, # NO2
                               '15' : 2.62, # SO2
                               '16' : 1.15} # CO


    parameters_new_names = ['YYYY', # 0
                            'MM', # 1
                            'DD', # 2
                            'HH', # 3
                            'mm', # 4
                            'Day of the week', # 5
                            'WD degrees', # 6
                            'WS m/s', # 7
                            'Temp Celsius', # 8
                            'RH %', # 9
                            'SR W/m2', # 10
                            'ATP mbar', # 11
                            'O3 ug/m3', # 12
                            'NO ug/m3', # 13
                            'NO2 ug/m3', # 14
                            'SO2 ug/m3', # 15
                            'CO mg/m3', # 16
                            'CO2 ppm', # 17
                            'PM10 ug/m3', # 18
                            'PM2.5 ug/m3', # 19
                            'THC ppm', # 20
                            'Rain mm', # 21
                            'Ox ppb', # 22
                            'NOx ppb'] # 23



    for month_ in range(1,13):
        print(month_)

        filename_old = file_list[month_ -1]
        data_array = open_csv_file(file_list[month_ -1])
        v_ppb = np.array(data_array[1:,:],dtype=float)
        v_ug_m3 = np.array(v_ppb)

        for keys_ in parameters_unit_scaling.keys():
            v_ug_m3[:, int(keys_)] = v_ppb[:, int(keys_)] * parameters_unit_scaling[str(keys_)]

        data_array[0, :] = parameters_new_names
        data_array[1:,:] = v_ug_m3

        filename_new = filename_old.replace('\\','/').split('/')[-1].split('.')[0] + '_ugm3.csv'

        numpy_save_txt(file_list_path + '/' + filename_new, data_array)

    print('done!')
def RH_to_abs_conc(arr_RH,arr_T):
    a_ = 1-(373.15/arr_T)
    c_1 = 13.3185
    c_2 = -1.97
    c_3 = -.6445
    c_4 = -.1299
    Po_H2O = 1013.25 * e_constant ** ((c_1 * (a_**1)) +
                                      (c_2 * (a_**2)) +
                                      (c_3 * (a_**3)) +
                                      (c_4 * (a_**4)) )   # mbar

    return (arr_RH * Po_H2O) / (100 * boltzmann_ * arr_T)
def Mixing_Ratio_to_molecules_per_cm3(arr_MR, ATP_mbar, Temp_C):
    arr_temp = Temp_C + 273.15 # kelvin
    arr_Molec_per_cm3 = arr_MR * ( ATP_mbar / ( boltzmann_ * arr_temp ) ) # molecules / cm3
    return arr_Molec_per_cm3
def molecules_per_cm3_to_Mixing_Ratio(arr_Molec_per_cm3, ATP_mbar, Temp_C):
    arr_temp = Temp_C + 273.15 # kelvin
    arr_MR = (arr_Molec_per_cm3 * boltzmann_ * arr_temp) / ATP_mbar
    return arr_MR
def ws_knots_to_ms(arr_):
    return arr_ * .514444
def ws_ms_to_knots(arr_):
    return arr_ / .514444
def kelvin_to_celsius(arr_temp_k):
    return arr_temp_k - 273.15
def celsius_to_kelvin(arr_temp_c):
    return arr_temp_c + 273.15

# geo reference
def lat_lon_series_to_2d_arrays(lat_series, lon_series):
    lat_array_1D = np.array(lat_series)
    lon_array_1D = np.array(lon_series)

    # reshaping
    lon_arr = np.zeros((lat_array_1D.shape[0], lon_array_1D.shape[0]), dtype=float)
    for r_ in range(lat_array_1D.shape[0]):
        lon_arr[r_, :] = lon_array_1D

    lat_arr = np.zeros((lat_array_1D.shape[0], lon_array_1D.shape[0]), dtype=float)
    for c_ in range(lon_array_1D.shape[0]):
        lat_arr[:, c_] = lat_array_1D

    return lat_arr, lon_arr
def lat_lon_to_x_y_PlateCarree(lat_, lon_):
    crs_wgs = proj.Proj(init='EPSG:4326')
    crs_plc = proj.Proj(init='EPSG:32662')
    return proj.transform(crs_wgs, crs_plc, lon_, lat_)
def lat_lon_to_x_y_aus(lat_, lon_):
    crs_wgs = proj.Proj(init='EPSG:4326')
    crs_aus = proj.Proj(init='EPSG:3577')
    return proj.transform(crs_wgs, crs_aus, lon_, lat_)
def lat_lon_to_x_y_geos_HIM(lat_, lon_):
    crs_wgs = proj.Proj(init='EPSG:4326')
    crs_HIM = proj.Proj('+proj=geos +lon_0=140.7 +h=35785863 +x_0=0 +y_0=0 +a=6378137 +b=6356752.3 +units=m +no_defs ')

    x_, y_zeros = proj.transform(crs_wgs, crs_HIM, lon_, np.zeros(lon_.shape[0]))
    x_zeros, y_ = proj.transform(crs_wgs, crs_HIM, lon_, np.zeros(lon_.shape[0]))

    return x_, y_
def x_y_to_lon_lat_aus(x_, y_):
    crs_wgs = proj.Proj(init='EPSG:4326')
    crs_aus = proj.Proj(init='EPSG:3577')

    lon_, lat_zeros = proj.transform(crs_aus, crs_wgs, x_, np.zeros(x_.shape[0]))
    lon_zeros, lat_ = proj.transform(crs_aus, crs_wgs, np.zeros(y_.shape[0]), y_)

    return lon_, lat_
def x_y_to_lon_lat_geos_HIM(x_, y_):
    crs_wgs = proj.Proj(init='EPSG:4326')
    crs_HIM = proj.Proj('+proj=geos +lon_0=140.7 +h=35785863 +x_0=0 +y_0=0 +a=6378137 +b=6356752.3 +units=m +no_defs ')

    lon_, lat_zeros = proj.transform(crs_HIM, crs_wgs, x_, np.zeros(x_.shape[0]))
    lon_zeros, lat_ = proj.transform(crs_HIM, crs_wgs, np.zeros(y_.shape[0]), y_)

    return lon_, lat_
def find_index_from_lat_lon(series_lat, series_lon, point_lat_list, point_lon_list):
    lat_index_list = []
    lon_index_list = []

    # mask arrays
    lat_m = series_lat
    lon_m = series_lon
    if np.sum(lat_m) != np.sum(lat_m) or np.sum(lon_m) != np.sum(lon_m):
        lat_m = np.ma.masked_where(np.isnan(lat_m), lat_m)
        lat_m = np.ma.masked_where(np.isinf(lat_m), lat_m)
        lon_m = np.ma.masked_where(np.isnan(lon_m), lon_m)
        lon_m = np.ma.masked_where(np.isinf(lon_m), lon_m)


    if type(point_lat_list) == tuple or type(point_lat_list) == list:
        for lat_ in point_lat_list:
            lat_index_list.append(np.argmin(np.abs(lat_m - lat_)))

        for lon_ in point_lon_list:
            lon_index_list.append(np.argmin(np.abs(lon_m - lon_)))
    else:
        lat_index_list = np.argmin(np.abs(lat_m - point_lat_list))
        lon_index_list = np.argmin(np.abs(lon_m - point_lon_list))

    return lat_index_list, lon_index_list
def find_index_from_lat_lon_2D_arrays(lat_arr, lon_arr, point_lat, point_lon):

    lat_del_arr = lat_arr - point_lat
    lon_del_arr = lon_arr - point_lon

    dist_arr = ( lat_del_arr**2  +  lon_del_arr**2 )**0.5

    return find_min_index_2d_array(dist_arr)
def find_index_from_lat_lon_1D_arrays(lat_arr, lon_arr, point_lat, point_lon):

    lat_del_arr = lat_arr - point_lat
    lon_del_arr = lon_arr - point_lon

    dist_arr = ( lat_del_arr**2  +  lon_del_arr**2 )**0.5

    return find_min_index_1d_array(dist_arr)
def distance_array_lat_lon_2D_arrays_degrees(lat_arr, lon_arr, point_lat, point_lon):
    lat_del_arr = lat_arr - point_lat
    lon_del_arr = lon_arr - point_lon

    return ( lat_del_arr**2  +  lon_del_arr**2 )**0.5
def meter_per_degrees(lat_point):
    lat_mean_rad = np.deg2rad(np.abs(lat_point))

    m_per_deg_lat = 111132.954 - 559.822 * np.cos(2 * lat_mean_rad) + 1.175 * np.cos(4 * lat_mean_rad)
    m_per_deg_lon = 111132.954 * np.cos(lat_mean_rad)

    return m_per_deg_lat, m_per_deg_lon
def degrees_per_meter(lat_point):
    m_per_deg_lat, m_per_deg_lon = meter_per_degrees(lat_point)

    return 1/m_per_deg_lat, 1/m_per_deg_lon
def distance_array_lat_lon_2D_arrays_degress_to_meters(lat_arr, lon_arr, point_lat, point_lon):
    m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.nanmean(lat_arr))

    lat_del_arr_m = (lat_arr - point_lat) * m_per_deg_lat
    lon_del_arr_m = (lon_arr - point_lon) * m_per_deg_lon

    return ( lat_del_arr_m**2  +  lon_del_arr_m**2 )**0.5
def distance_between_to_points_in_meters(point_1_latlon, point_2_latlon):
    latMid = (point_1_latlon[0] + point_2_latlon[0]) / 2

    m_per_deg_lat, m_per_deg_lon = meter_per_degrees(latMid)

    del_lat = (point_1_latlon[0] - point_2_latlon[0]) * m_per_deg_lat
    del_lon = (point_1_latlon[1] - point_2_latlon[1]) * m_per_deg_lon

    return ((del_lat**2) + (del_lon**2))**0.5
def make_circle_x_y_arrays_lat_lon(center_lat, center_lon, radius_meters, points_=360):
    theta = np.linspace(0, 2 * np.pi, points_)
    deg_per_m_lat, deg_per_m_lon = degrees_per_meter(center_lat)
    radius_lat = deg_per_m_lat * radius_meters
    radius_lon = deg_per_m_lon * radius_meters
    x_ = radius_lon * np.cos(theta) + center_lon
    y_ = radius_lat * np.sin(theta) + center_lat
    return x_, y_
def make_circle_x_y_arrays(center_x, center_y, radius_, points_=360):
    theta = np.linspace(0, 2 * np.pi, points_)
    x_ = radius_ * np.cos(theta) + center_x
    y_ = radius_ * np.sin(theta) + center_y
    return x_, y_
def component_distance_array_lat_lon_degress_to_meters(lat_arr, lon_arr, point_lat, point_lon):
    m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.nanmean(lat_arr))
    lat_del_arr_m = (lat_arr - point_lat) * m_per_deg_lat
    lon_del_arr_m = (lon_arr - point_lon) * m_per_deg_lon
    return lon_del_arr_m, lat_del_arr_m

# Data Loading
def load_data_to_return_return(filename_):
    ## user defined variables
    day_column_number = 2
    month_column_number = 1
    year_column_number = 0
    hour_column_number = 3
    minute_column_number = 4
    time_header = 'Time' #defining time header

    # define file extension
    ext_ = filename_.split('.')[-1]
    # open file with correct protocol
    if ext_[:3] == 'xls':
        data_array = open_excel_file(filename_)
    else:
        data_array = open_csv_file(filename_)
    # define arrays
    values_str = data_array[1:,5:]
    values_ = np.zeros((values_str.shape[0],values_str.shape[1]),dtype=float)
    for r_ in range(values_.shape[0]):
        for c_ in range(values_.shape[1]):
            try:
                values_[r_,c_] = float(values_str[r_,c_])
            except:
                values_[r_,c_] = np.nan
    header_ = data_array[0 ,3:]
    # defining time arrays
    time_str = data_array[1:,0].astype('<U32')
    for r_ in range(time_str.shape[0]):
        time_str[r_] = (data_array[r_+1,day_column_number].split('.')[0] + '-' +
                        data_array[r_+1,month_column_number].split('.')[0] + '-' +
                        data_array[r_+1,year_column_number].split('.')[0] + '_' +
                        data_array[r_+1,hour_column_number].split('.')[0] + ':' +
                        data_array[r_+1,minute_column_number].split('.')[0])
    time_days = np.array([mdates.date2num(datetime.utcfromtimestamp(
                                calendar.timegm(time.strptime(time_string_record, '%d-%m-%Y_%H:%M'))))
                                for time_string_record in time_str])
    diurnal_hour = np.array([datetime.utcfromtimestamp(
                            calendar.timegm(time.strptime(time_string_record, '%d-%m-%Y_%H:%M'))).hour
                                    for time_string_record in time_str], dtype=int)
    # compile names
    header_[0] = time_header
    header_[1] = 'Hour of day'
    # compile values
    values_ = np.column_stack((time_days,diurnal_hour,values_))


    return header_, values_, time_str
def numpy_load_txt(filename_, delimiter_=",", format_=float, skip_head=0):
    return genfromtxt(filename_, delimiter=delimiter_, dtype=format_, skip_header=skip_head)
def open_excel_file(filename_):
    # open file
    workbook_ = open_workbook(filename_)
    # copy data from first sheet to data_array
    first_sheet = workbook_.sheets()[0]
    data_array = np.zeros((first_sheet.nrows,first_sheet.ncols),dtype='<U32')
    for r_ in range(first_sheet.nrows):
        for c_ in range(first_sheet.ncols):
            data_array[r_,c_] = first_sheet.cell(r_,c_).value
    return data_array
def load_time_excel(filename_):
    # define file extension
    ext_ = filename_.split('.')[-1]
    # open file with correct protocol
    if ext_[:3] == 'xls':
        data_array, date_mode_excel = open_excel_file(filename_)
    else:
        data_array = open_csv_file(filename_)
        date_mode_excel = 0
    # define arrays
    values_str = data_array[1:,1:]
    values_ = np.zeros((values_str.shape[0],values_str.shape[1]),dtype=float)
    for r_ in range(values_.shape[0]):
        for c_ in range(values_.shape[1]):
            try:
                values_[r_,c_] = float(values_str[r_,c_])
            except:
                values_[r_,c_] = np.nan

    # defining time arrays
    time_days = np.zeros(data_array.shape[0] - 1, dtype=float)
    time_month = np.zeros(data_array.shape[0] - 1, dtype=int)
    time_weekday = np.zeros(data_array.shape[0] - 1, dtype=int)
    time_hour = np.zeros(data_array.shape[0] - 1)
    for r_ in range(data_array.shape[0]-1):
        try:
            time_days[r_] = mdates.date2num(xldate_as_datetime(float(data_array[r_+1,0]), date_mode_excel))
            time_month[r_] = xldate_as_datetime(float(data_array[r_+1,0]), date_mode_excel).month
            time_weekday[r_] = datetime.weekday(mdates.num2date(time_days[r_]))
            time_hour[r_] = (xldate_as_datetime(float(data_array[r_+1,0]), date_mode_excel).hour +
                            (xldate_as_datetime(float(data_array[r_+1,0]), date_mode_excel).minute / 60))
        except:
            time_days[r_] = np.nan
            time_month[r_] = np.nan
            time_weekday[r_] = np.nan
            time_hour[r_] = np.nan

    # compile names
    header_ = np.zeros(data_array.shape[1] + 3,dtype="<U64")
    header_[0] = data_array[0,0]
    header_[1] = 'Month'
    header_[2] = 'Day of week'
    header_[3] = 'Hour of day'
    header_[4:] = data_array[0,1:]

    # compile values
    values_ = np.column_stack((time_days, time_month, time_weekday, time_hour, values_))

    return header_, values_
def open_csv_file(filename_, delimiter=',', skip_head=0, dtype='<U32'):
    # load data
    return np.array(genfromtxt(filename_, delimiter=delimiter, dtype=dtype, skip_header=skip_head))
def select_filename(path_):
    file_name = filedialog.askopenfilename(defaultextension = '.npz', initialdir = path_)
    return file_name
def select_folder(path_):
    folder_str = filedialog.askdirectory(initialdir = path_)
    return folder_str
def load_time_columns(filename_):
    ## user defined variables
    day_column_number = 2
    month_column_number = 1
    year_column_number = 0
    hour_column_number = 3
    minute_column_number = 4
    time_header = 'Time' #defining time header

    data_array = open_csv_file(filename_)
    # define arrays
    values_str = data_array[1:,5:]
    values_ = np.zeros((values_str.shape[0],values_str.shape[1]),dtype=float)
    for r_ in range(values_.shape[0]):
        for c_ in range(values_.shape[1]):
            try:
                values_[r_,c_] = float(values_str[r_,c_])
            except:
                values_[r_,c_] = np.nan
    header_ = data_array[0 ,1:]
    # defining time arrays
    time_days = np.zeros(data_array.shape[0] - 1, dtype=float)
    time_month = np.zeros(data_array.shape[0] - 1, dtype=int)
    time_weekday = np.zeros(data_array.shape[0] - 1, dtype=int)
    time_hour = np.zeros(data_array.shape[0] - 1)
    for r_ in range(data_array.shape[0] - 1):
        time_days[r_] = mdates.date2num(datetime(
            int(float(data_array[r_+1,year_column_number])),
            int(float(data_array[r_+1,month_column_number])),
            int(float(data_array[r_+1,day_column_number])),
            int(float(data_array[r_+1,hour_column_number])),
            int(float(data_array[r_+1,minute_column_number]))))
        time_month[r_] = int(float(data_array[r_+1,month_column_number]))
        time_weekday[r_] = datetime.weekday(mdates.num2date(time_days[r_]))
        time_hour[r_] = float(data_array[r_+1,hour_column_number]) + (float(data_array[r_+1,minute_column_number]) / 60)
    # compile names
    header_[0] = time_header
    header_[1] = 'Month'
    header_[2] = 'Day of week'
    header_[3] = 'Hour of day'
    # compile values
    values_ = np.column_stack((time_days, time_month, time_weekday, time_hour, values_))

    return header_, values_
def load_traffic_img_to_01234_arr(filename_):
    img_arr = np.array(PIL_Image.open(filename_))
    out_arr = np.zeros((img_arr.shape[0], img_arr.shape[1]), dtype=int)
    out_arr[img_arr==63] = 1
    out_arr[img_arr==127] = 2
    out_arr[img_arr==191] = 3
    out_arr[img_arr==255] = 4
    return out_arr
def load_file_list_of_arrays_to_single_3d_array(file_list):
    array_list = []

    for array_filename in file_list:
        array_list.append(load_traffic_img_to_01234_arr(array_filename))

    out_array = np.zeros((len(file_list), array_list[0].shape[0], array_list[0].shape[1]))

    for time_stamp, array_ in enumerate(array_list):
        out_array[time_stamp, :, :] = array_[:,:]

    print('done')
    return out_array
def create_list_of_arrays_from_file_list(file_list):
    ext_ = file_list[0][-3:]

    arr_list = []

    if ext_ == 'csv':
        for file_ in file_list:
            arr_list.append(genfromtxt(file_, delimiter=','))
        print('files_loaded')
    else:
        for file_ in file_list:
            arr_list.append(read_png_to_array(file_))
        print('files_loaded')

    scale_min = np.min(arr_list)
    scale_max = np.max(arr_list)
    max_min_tuple = (scale_min, scale_max)

    return arr_list, max_min_tuple
def load_nucleation_data(filename_):
    # open file
    workbook_ = open_workbook(filename_)

    days_data_dict = {}

    sheet_number_total = len(workbook_.sheets())
    for sheet_number in range(sheet_number_total):
        sheet_ = workbook_.sheets()[sheet_number]
        rows_ = sheet_.nrows
        columns_ = sheet_.ncols
        name_ = sheet_.name

        time_series = np.zeros(rows_ - 2, dtype=float)
        last_time_stamp = -1
        for r_ in range(2, rows_):
            current_time_stamp = sheet_.cell(r_,1).value
            if current_time_stamp > last_time_stamp:
                time_series[r_-2] = current_time_stamp
                last_time_stamp =current_time_stamp
            else:
                time_series[r_ - 2] = current_time_stamp + 1
                last_time_stamp = current_time_stamp + 1

        diameter_series = np.zeros(columns_ - 3, dtype=float)
        for c_ in range(2, columns_-1): diameter_series[c_-2] =  sheet_.cell(0,c_).value

        tota_number_conc = np.zeros(rows_ - 2, dtype=float)
        for r_ in range(2, rows_): tota_number_conc[r_ - 2] = sheet_.cell(r_, columns_-1).value


        data_array = np.zeros((rows_ - 2, columns_ - 3), dtype=float) * np.nan
        for r_ in range(2,rows_):
            for c_ in range(2,columns_-1):
                try:
                    data_array[r_-2,c_-2] = sheet_.cell(r_,c_).value
                except:
                    pass

        days_data_dict[name_] = [time_series, diameter_series, data_array, tota_number_conc]

    return days_data_dict
def load_img_to_array(filename_):
    return np.array(PIL_Image.open(filename_))
def load_object(filename):
    with open(filename, 'rb') as input_object:
        object_ = pickle.load(input_object)
    return object_
def read_one_line_from_text_file(filename_, line_number):
    file_ = open(filename_)
    for i, line in enumerate(file_):
        if i == line_number :
            line_str = line
        elif i > line_number:
            break
    file_.close()
    return line_str
def load_dictionary(filename_):
    dict_ = np.load(filename_, allow_pickle=True).item()
    return dict_
def load_numpy_array_comprezed(filename_):
    arr_ = np.load(filename_, allow_pickle=True)['arr_0']
    return arr_


# data saving/output
def save_time_variable_as_csv(output_filename, var_name, time_in_secs, var_values, time_format_output='%Y%m%d%H%M%S'):
    out_file = open(output_filename, 'w')

    # write header
    out_file.write(time_format_output)
    out_file.write(',')
    out_file.write(var_name)
    out_file.write('\n')

    for r_ in range(time_in_secs.shape[0]):
        p_progress_bar(r_, time_in_secs.shape[0])
        out_file.write(time_seconds_to_str(time_in_secs[r_], time_format_output))
        out_file.write(',' + str(var_values[r_]))
        out_file.write('\n')

    out_file.close()
def numpy_save_txt(filename_, array_, delimiter_=",", format_='%s'):
    np.savetxt(filename_, array_, delimiter=delimiter_, fmt=format_)
def compile_data_and_save(file_list, path_new_file, new_filename):
    # load data list
    data_list = []
    for file_ in file_list:
        data_list.append(load_data_to_return_return(file_))
        print('loaded ' + file_)

    values_new = np.array(data_list[0][1])
    time_str_new = np.array(data_list[0][2])

    for i, month_data in enumerate(data_list[1:]):
        values_new = np.row_stack((values_new, month_data[1]))
        time_str_new = np.concatenate((time_str_new, month_data[2]))

    time_sec = time_str_to_seconds(time_str_new, '%d-%m-%Y_%H:%M')
    output_filename = path_new_file + new_filename
    save_array_to_disk(data_list[0][0][2:], time_sec, values_new[:, 2:], output_filename)
def save_array_to_disk(header_with_units, time_in_seconds, values_in_floats, filename):
    #
    if len(values_in_floats.shape) == 1:
        header_to_print = ['YYYY', 'MM', 'DD', 'HH', 'mm', header_with_units]
    else:
        header_to_print = ['YYYY', 'MM', 'DD', 'HH', 'mm']
        for parameter_ in header_with_units:
            header_to_print.append(parameter_)
    # create values block
    T_ = time_seconds_to_5C_array(time_in_seconds)
    P_ = np.column_stack((T_, values_in_floats))
    # change type to str
    P_str = np.array(P_, dtype='<U32')
    # join header with values
    P_final = np.row_stack((header_to_print, P_str))
    # save to hard drive
    numpy_save_txt(filename, P_final)
    print('final data saved to: ' + filename)
def save_HVF(header_, values_, filename):
    # check if all shapes match
    if len(header_) != values_.shape[1]:
        print('shape of header is not compatible with shape of values')
        return

    time_in_seconds = mdates.num2epoch(values_[:, 0])

    header_with_units = header_[2:]
    values_in_floats = values_[:, 2:]
    header_to_print = ['YYYY', 'MM', 'DD', 'HH', 'mm']
    for parameter_ in header_with_units:
        header_to_print.append(parameter_)
    # create values block
    T_ = np.zeros((time_in_seconds.shape[0], 5), dtype='<U32')
    for r_ in range(time_in_seconds.shape[0]):
        if time_in_seconds[r_] == time_in_seconds[r_]:
            T_[r_] = time.strftime("%Y,%m,%d,%H,%M", time.gmtime(time_in_seconds[r_])).split(',')
    P_ = np.column_stack((T_, values_in_floats))
    # change type to str
    P_str = np.array(P_, dtype='<U32')
    # join header with values
    P_final = np.row_stack((header_to_print, P_str))
    # save to hard drive
    numpy_save_txt(filename, P_final)
    print('final data saved to: ' + filename)
def save_simple_array_to_disk(header_list, values_array, filename_):
    # change type to str
    values_str = np.array(values_array, dtype='<U32')
    # join header with values
    array_final = np.row_stack((header_list, values_str))
    # save to hard drive
    numpy_save_txt(filename_, array_final)
    print('final data saved to: ' + filename_)
def save_array_as_is(array_, filename_):
    np.savetxt(filename_, array_, delimiter=",", fmt='%s')
def save_array_as_txt(array_, filename_, header_=None,
                      time_format=time_format_parsivel, first_column_as_time=False, delimeter_=','):
    output_file = open(filename_, 'w')
    # write header
    if header_ is not None:
        if len(header_) == array_.shape[1]:
            for var_name in header_[:-1]:
                output_file.write(str(var_name) + delimeter_)
            output_file.write(str(header_[-1]) + '\n')
        elif len(header_) == array_.shape[1] - 1 and first_column_as_time:
            output_file.write(time_format + delimeter_)
            for var_name in header_[:-1]:
                output_file.write(str(var_name) + delimeter_)
            output_file.write(str(header_[-1]) + '\n')
        else:
            print('error with size of header given, no array saved')
            return


    if first_column_as_time:
        time_series = time_seconds_to_str(
            time_days_to_seconds(convert_any_time_type_to_days(array_[:, 0])), time_format)

        for r_ in range(array_.shape[0]):
            output_file.write(time_series[r_])
            for c_ in range(1,array_.shape[1]):
                output_file.write(delimeter_ + str(array_[r_, c_]))
            output_file.write('\n')

    else:
        for r_ in range(array_.shape[0]):
            output_file.write(str(array_[r_, 0]))
            for c_ in range(1, array_.shape[1]):
                output_file.write(delimeter_ + str(array_[r_, c_]))
            output_file.write('\n')


    output_file.close()
def split_data_by_month(filename_, out_path, new_file_tag):
    header_, values_, time_str = load_data_to_return_return(filename_)
    print('loaded file: ' + filename_)
    time_seconds = time_str_to_seconds(time_str, '%d-%m-%Y_%H:%M')
    # # calculate how many years
    # year_list = []
    # last_year = 0
    # for time_str_stamp in time_str:
    #     current_year = int(time_str_stamp.split('-')[-1].split('_')[0])
    #     if last_year != current_year:
    #         year_list.append(current_year)
    #         last_year = current_year
    # calculate how many months
    month_array = np.zeros(time_str.shape[0])
    month_list = []
    last_month = 0
    index_ = 0
    for time_str_stamp in time_str:
        current_month = int(time_str_stamp.split('-')[1])
        month_array[index_] = current_month
        index_ += 1
        if last_month != current_month:
            month_list.append(current_month)
            last_month = current_month
    print('month list')
    print(month_list)

    mask_array = np.zeros(time_str.shape[0])
    for month_ in month_list:
        mask_array[month_array == month_] = 1

        start_ = -1
        stop_ = -1
        for r_ in range(mask_array.shape[0]):
            if mask_array[r_] == 1 and start_ == -1:
                start_ = r_
            if mask_array[r_] == 0 and start_ != -1 and stop_ == -1:
                stop_ = r_
        if stop_ == -1: stop_ = mask_array.shape[0]

        print('start: ' + str(start_))
        print('stop: ' + str(stop_))
        print('mask sum: ' + str(np.sum(mask_array)))

        values_out_array = values_[start_:stop_, :]
        time_sec_out_array = time_seconds[start_:stop_]
        # check
        if time_sec_out_array.shape[0] != np.sum(mask_array):
            print("error, months stamps are discontinuous for month: " + str(month_))

        start_time_str = datetime.utcfromtimestamp(time_seconds[start_]).strftime('%Y%m%d_%H%M')
        stop_time_str = datetime.utcfromtimestamp(time_seconds[stop_ - 1]).strftime('%Y%m%d_%H%M')
        new_filename = out_path + new_file_tag + '_' + start_time_str + '_' + stop_time_str + '.csv'

        save_array_to_disk(header_[2:], time_sec_out_array, values_out_array[:, 2:], new_filename)
        print('-' * 10)
        mask_array[:] = 0
def image_remove_color(image_filename):
    img = PIL_Image.open(image_filename)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] > 200 or item[1] > 200 or item[2] > 200:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(image_filename[:-4] + '_mod.png', "PNG")
def save_object(obj, filename):
    with open(filename, 'wb') as output:  # Overwrites any existing file.
        pickle.dump(obj, output, pickle.HIGHEST_PROTOCOL)
def extract_item_from_zip_file(zip_filename, item_name, output_path):
    zip_archive = zipfile.ZipFile(zip_filename)
    output_filename = zip_archive.extract(item_name, output_path)
    zip_archive.close()
    return output_filename.replace('\\','/')
def extract_all_from_zip_file(zip_filename, output_path):
    zip_archive = zipfile.ZipFile(zip_filename)
    zip_archive.extractall(output_path)
    zip_archive.close()
def compress_file_list_zip(filename_list, output_filename, compression_='ZIP_DEFLATED', item_labels=None):
    """
    adds all files in filename_list to a zipped archive named output_filename, using defined compression
    :param filename_list: list of string with full filenames
    :param output_filename: string with full filename to be used for new zipped archive. will be replaced if already exists
    :param compression_: can be ZIP_STORED (no compression), ZIP_DEFLATED (requires zlib), ZIP_BZIP2 (requires bz2) or ZIP_LZMA (requires lzma).
    :param item_labels: list of unique strings with the same size of filename_list used inside the zip. if none, full filenames will be used
    :return: 0 if all good, 1 if error
    """
    try:
        zip_archive = zipfile.ZipFile(output_filename, mode='w', compression=compression_)

        if item_labels is None:
            for filename_ in filename_list:
                zip_archive.write(filename_)
        else:
            for item_ in zip(filename_list, item_labels):
                zip_archive.write(item_[0], item_[1])

        zip_archive.close()
        return 0
    except BaseException as error_msg:
        try:
            zip_archive.close()
        except:
            pass
        print(error_msg)
        return 1
def zip_file_list_all_items_inside(zip_filename):
    """
    Lists all the contents' names inside a zip file

    Parameters:
    ===========
        zip_filename: str
            Full filename to zip file

    Returns:
    ========
        item_names: list
            a sorted list of all item names inside the zip file.
    """

    zip_archive = zipfile.ZipFile(zip_filename)
    zip_file_list_full = list(zip_archive.filelist)
    zip_archive.close()
    item_names = []
    for item_ in zip_file_list_full:
        item_names.append(item_.filename)
    return sorted(item_names)
def extract_all_from_zip_to_memory(zip_filename):
    """
    Extracts all items inside a zip file and creates a dictionary that is loaded to ram
    :param zip_filename: string with the filename of the zip file
    :return: dictionary with the name of the items as keys
    """
    input_zip = zipfile.ZipFile(zip_filename)
    return {name: input_zip.read(name) for name in input_zip.namelist()}
def extract_item_from_zip_to_memory(zip_filename, item_name):
    """
    Extracts the bytes of an item from inside a zip file

    Parameters:
    ===========
        zip_filename: str
            Full filename to zip file

        item_name: str
            name of the item to be extracted

    Returns:
    ========
        item_bytes_str: str
            bytes of the extracted item

    """
    zip_archive = zipfile.ZipFile(zip_filename)
    item_bytes_str = zip_archive.read(item_name)
    zip_archive.close()

    return item_bytes_str


# sattelite data load
def load_OMI_NO2_monthly_data(filename_):
    # # [molec./cm-2]
    # filename_ = 'C:/_input/no2_201601.grd'
    # arr_NO2, lat_arr_NO2, lon_arr_NO2 = load_OMI_NO2_monthly_data(filename_)
    # [440: -820, 1650: 1960]
    data_array = genfromtxt(filename_, dtype=float, skip_header=7)
    file_object = open(filename_,mode='r')
    ncols = int(file_object.readline().split()[-1])
    nrows = int(file_object.readline().split()[-1])
    xllcorner = float(file_object.readline().split()[-1])
    yllcorner = float(file_object.readline().split()[-1])
    cellsize = float(file_object.readline().split()[-1])
    nodata_value = float(file_object.readline().split()[-1])
    # version = file_object.readline().split()[-1]
    file_object.close()

    lat_arr = np.zeros((nrows, ncols), dtype=float)
    lon_arr = np.zeros((nrows, ncols), dtype=float)

    lat_series = np.linspace(yllcorner + (cellsize * nrows), yllcorner, nrows)
    lon_series = np.linspace(xllcorner, xllcorner + (cellsize * ncols), ncols)

    for r_ in range(nrows):
        lon_arr[r_, :] = lon_series

    for c_ in range(ncols):
        lat_arr[:, c_] = lat_series

    data_array[data_array==nodata_value] = np.nan

    data_array = data_array * 1e13

    return data_array[1:-1,:], lat_arr[1:-1,:], lon_arr[1:-1,:]
def load_OMI_HCHO_monthly_data(filename_):
    # # [molec./cm-2]
    # filename_ = 'C:/_input/OMIH2CO_Grid_720x1440_201601.dat'
    # arr_HCHO, lat_arr_HCHO, lon_arr_HCHO = load_OMI_HCHO_monthly_data(filename_)
    # [220: -410, 825: 980]
    data_array = genfromtxt(filename_, dtype=float, skip_header=7)
    ncols = 1440
    nrows = 720
    xllcorner = -180
    yllcorner = -90
    cellsize = 0.25

    lat_arr = np.zeros((nrows, ncols), dtype=float)
    lon_arr = np.zeros((nrows, ncols), dtype=float)

    lat_series = np.linspace(yllcorner + (cellsize * nrows), yllcorner, nrows)
    lon_series = np.linspace(xllcorner, xllcorner + (cellsize * ncols), ncols)

    for r_ in range(nrows):
        lon_arr[r_, :] = lon_series

    for c_ in range(ncols):
        lat_arr[:, c_] = lat_series

    data_array = data_array * 1e15

    return data_array[1:-1,:], lat_arr[1:-1,:], lon_arr[1:-1,:]
def download_HIM8_IR_AUS(datetime_start_str_YYYYmmDDHHMMSS, datetime_end_str_YYYYmmDDHHMMSS):
    url_prefix_ir = 'http://rammb.cira.colostate.edu/ramsdis/online/images/himawari-8/himawari-8_band_07_sector_04/himawari-8_band_07_sector_04_'
    # create date strings list
    datetime_start_sec = time_str_to_seconds(datetime_start_str_YYYYmmDDHHMMSS, '%Y%m%d%H%M%S')
    datetime_end_sec = time_str_to_seconds(datetime_end_str_YYYYmmDDHHMMSS, '%Y%m%d%H%M%S')
    time_steps_in_sec = 10*60
    number_of_images = (datetime_end_sec - datetime_start_sec) / time_steps_in_sec
    datetime_list_str = []
    for time_stamp_index in range(int(number_of_images)):
        datetime_list_str.append(time_seconds_to_str(datetime_start_sec + (time_stamp_index * time_steps_in_sec),
                                                     '%Y%m%d%H%M%S'))

    # create url list
    url_list = []
    for time_stamp_index in range(int(number_of_images)):
        url_list.append(url_prefix_ir + datetime_list_str[time_stamp_index] + '.gif')


    # download image list
    img_list = []
    datetime_downloaded_list = []
    datetime_not_downloaded_list = []
    for time_stamp_index in range(int(number_of_images)):
        try:
            img_list.append(np.array(PIL_Image.open(BytesIO(requests.get(url_list[time_stamp_index],
                                                                         timeout = 5).content)).convert('RGB')))
            datetime_downloaded_list.append(datetime_list_str[time_stamp_index])

            img_arr = PIL_Image.fromarray(img_list[-1])
            img_arr.save(path_output  + datetime_list_str[time_stamp_index] + '.png')
            print(datetime_list_str[time_stamp_index], 'downloaded')

        except:
            print(datetime_list_str[time_stamp_index], 'failed')
            datetime_not_downloaded_list.append(datetime_list_str[time_stamp_index])
def download_HIM8_AUS_ch3_500m(YYYYmmddHHMM_str):
    url_ = 'http://dapds00.nci.org.au/thredds/dodsC/rr5/satellite/obs/himawari8/FLDK/' + \
           YYYYmmddHHMM_str[:4] + \
             '/' + \
           YYYYmmddHHMM_str[4:6] + \
             '/' + \
           YYYYmmddHHMM_str[6:8] + \
             '/' + \
           YYYYmmddHHMM_str[8:12] + \
             '/' + \
           YYYYmmddHHMM_str + '00' \
             '-P1S-ABOM_BRF_B03-PRJ_GEOS141_500-HIMAWARI8-AHI.nc'
    f_ = nc.Dataset(url_)

    r_1 = 13194
    r_2 = 19491
    c_1 = 4442
    c_2 = 14076

    return f_.variables['channel_0003_brf'][0, r_1:r_2, c_1:c_2]
def download_HIM8_AUS_2000m(YYYYmmddHHMM_str, channel_number_str, print_=True):
    url_ = 'http://dapds00.nci.org.au/thredds/dodsC/rr5/satellite/obs/himawari8/FLDK/' + \
           YYYYmmddHHMM_str[:4] + '/' + YYYYmmddHHMM_str[4:6] + '/' + YYYYmmddHHMM_str[6:8] + \
           '/' + YYYYmmddHHMM_str[8:12] + \
           '/' + YYYYmmddHHMM_str + '00' + \
           '-P1S-ABOM_OBS_' \
           'B' + channel_number_str + \
           '-PRJ_GEOS141_2000-HIMAWARI8-AHI.nc'

    if print_: print('downloading HIM_8', YYYYmmddHHMM_str, channel_number_str)

    f_ = nc.Dataset(url_)

    r_1 = 3298
    r_2 = 4873
    c_1 = 1110
    c_2 = 3519

    variable_name = ''
    for var_key in f_.variables.keys():
        if len(var_key.split('channel')) > 1:
            variable_name = var_key
            break


    return f_.variables[variable_name][0, r_1:r_2, c_1:c_2]
def download_HIM8_2000m(YYYYmmddHHMM_str, channel_number_str):
    url_ = 'http://dapds00.nci.org.au/thredds/dodsC/rr5/satellite/obs/himawari8/FLDK/' + \
           YYYYmmddHHMM_str[:4] + '/' + YYYYmmddHHMM_str[4:6] + '/' + YYYYmmddHHMM_str[6:8] + \
           '/' + YYYYmmddHHMM_str[8:12] + \
           '/' + YYYYmmddHHMM_str + '00' + \
           '-P1S-ABOM_OBS_' \
           'B' + channel_number_str + \
           '-PRJ_GEOS141_2000-HIMAWARI8-AHI.nc'

    f_ = nc.Dataset(url_)

    variable_name = ''
    for var_key in f_.variables.keys():
        if len(var_key.split('channel')) > 1:
            variable_name = var_key
            break

    print('downloading variable:', variable_name)
    return f_.variables[variable_name][0, :,:]
def download_HIM8(YYYYmmddHHMM_str, channel_number_str, print_=True,
                  prefix_='https://dapds00.nci.org.au/thredds/dodsC/ra22/satellite-products/arc/obs/himawari-ahi/fldk/v1-0/'):

    resolution_1000 = [1,2,4]
    resolution_500 = [3]
    channel_number_int = int(channel_number_str)

    resolution_ = 2000
    if channel_number_int in resolution_1000:
        resolution_ = 1000
    elif channel_number_int in resolution_500:
        resolution_ = 500

    year_ = YYYYmmddHHMM_str[:4]
    month_ = YYYYmmddHHMM_str[4:6]
    day_ = YYYYmmddHHMM_str[6:8]
    hour_min = YYYYmmddHHMM_str[8:]

    url_ = prefix_ + '{0}/{1}/{2}/{3}/{4}00-P1S-ABOM_OBS_B{5}-PRJ_GEOS141_{6}-HIMAWARI8-AHI.nc'.format(year_,
                                                                                                       month_,
                                                                                                       day_,
                                                                                                       hour_min,
                                                                                                       YYYYmmddHHMM_str,
                                                                                                       channel_number_str,
                                                                                                       resolution_)


    if print_: print('downloading\n' + YYYYmmddHHMM_str + '\n' + channel_number_str + '\n' + url_)

    f_ = nc.Dataset(url_)

    variable_name = ''

    for var_key in f_.variables.keys():
        if len(var_key.split('channel')) > 1:
            variable_name = var_key
            break

    rows_ = f_.variables[variable_name].shape[1]
    rows_size = int(rows_ / 100)

    array_list = []
    for row_part in range(100):
        p_progress_bar(row_part, 100)
        array_list.append(f_.variables[variable_name][0,(row_part*rows_size):((row_part+1)*rows_size),:].filled(np.nan))

    f_.close()
    return np.row_stack(array_list)
def download_HIM8_truecolor(YYYYmmddHHMM_str):
    slope_ = 12
    inflex_ = .2
    max_ = 256

    H8_r_500 = download_HIM8(YYYYmmddHHMM_str, '03')
    H8_r = column_average_discrete_2D(row_average_discrete_2D(H8_r_500, 2), 2)
    H8_g = download_HIM8(YYYYmmddHHMM_str, '02')
    H8_b = download_HIM8(YYYYmmddHHMM_str, '01')


    img_ = np.zeros((H8_b.shape[0], H8_b.shape[1], 3), dtype='uint8')
    img_[:, :, 0] = sigmoid(H8_r, slope_, inflex_, max_)
    img_[:, :, 1] = sigmoid(H8_g, slope_, inflex_, max_)
    img_[:, :, 2] = sigmoid(H8_b, slope_, inflex_, max_)
    return img_
def download_lat_lon_arrays_HIM8_500():
    url_ = 'http://dapds00.nci.org.au/thredds/dodsC/rr5/satellite/obs/himawari8/FLDK/ancillary/' \
                     '20150127000000-P1S-ABOM_GEOM_SENSOR-PRJ_GEOS141_500-HIMAWARI8-AHI.nc'

    lat_ = download_big_nc_array_in_parts(url_, 'lat')
    lon_ = download_big_nc_array_in_parts(url_, 'lon')

    lat_[lat_ > 360] = np.nan
    lon_[lon_ > 360] = np.nan

    return lat_, lon_
def download_lat_lon_arrays_HIM8_2000():
    url_ = 'http://dapds00.nci.org.au/thredds/dodsC/rr5/satellite/obs/himawari8/FLDK/ancillary/' \
           '20150127000000-P1S-ABOM_GEOM_SENSOR-PRJ_GEOS141_2000-HIMAWARI8-AHI.nc'

    lat_ = download_big_nc_array_in_parts(url_, 'lat')
    lon_ = download_big_nc_array_in_parts(url_, 'lon')

    lat_[lat_ > 360] = np.nan
    lon_[lon_ > 360] = np.nan

    return lat_, lon_
def download_big_nc_array_in_parts(url_, variable_name, parts_=4):
    f_ = nc.Dataset(url_)

    var_shape = f_.variables[variable_name].shape
    print('downloading variable', variable_name, 'with shape:', var_shape)

    if len(var_shape) == 0:
        print('ERROR! variable is not an array')
        return None
    elif len(var_shape) == 1:
        if var_shape[0] == 1:
            print('ERROR! variable is a scalar')
            return None
        else:
            rows_per_part = int(var_shape[0] / parts_)
            if rows_per_part == 0:
                print('ERROR! variable size is too small to be divided, should be downloaded directly')
                return None
            else:
                output_array = np.zeros(var_shape[0])
                for part_ in range(parts_ - 1):
                    output_array[int(part_*rows_per_part):int((part_+1)*rows_per_part)] =\
                        f_.variables[variable_name][int(part_*rows_per_part):int((part_+1)*rows_per_part)]
                output_array[int((parts_ -1)*rows_per_part):] = \
                    f_.variables[variable_name][int((parts_ -1)*rows_per_part):]
                return output_array

    elif len(var_shape) == 2:
        rows_per_part = int(var_shape[1] / parts_)
        if rows_per_part == 0:
            print('ERROR! variable size is too small to be divided, should be downloaded directly')
            return None
        else:
            output_array = np.zeros((var_shape[0],var_shape[1]))
            for part_ in range(parts_ - 1):
                output_array[:,int(part_ * rows_per_part):int((part_ + 1) * rows_per_part)] = \
                    f_.variables[variable_name][:,int(part_ * rows_per_part):int((part_ + 1) * rows_per_part)]
            output_array[:,int((parts_ - 1) * rows_per_part):] = \
                f_.variables[variable_name][:,int((parts_ - 1) * rows_per_part):]
            return output_array

    elif len(var_shape) == 3:
        rows_per_part = int(var_shape[1] / parts_)
        if rows_per_part == 0:
            print('ERROR! variable size is too small to be divided, should be downloaded directly')
            return None
        else:
            output_array = np.zeros((var_shape[0],var_shape[1],var_shape[2]))
            for part_ in range(parts_ - 1):
                output_array[:,int(part_ * rows_per_part):int((part_ + 1) * rows_per_part),:] = \
                    f_.variables[variable_name][:,int(part_ * rows_per_part):int((part_ + 1) * rows_per_part),:]
            output_array[:,int((parts_ - 1) * rows_per_part):,:] = \
                f_.variables[variable_name][:,int((parts_ - 1) * rows_per_part):,:]
            return output_array

    elif len(var_shape) == 4:
        rows_per_part = int(var_shape[1] / parts_)
        if rows_per_part == 0:
            print('ERROR! variable size is too small to be divided, should be downloaded directly')
            return None
        else:
            output_array = np.zeros((var_shape[0],var_shape[1],var_shape[2],var_shape[3]))
            for part_ in range(parts_ - 1):
                output_array[:,int(part_ * rows_per_part):int((part_ + 1) * rows_per_part),:,:] = \
                    f_.variables[variable_name][:,int(part_ * rows_per_part):int((part_ + 1) * rows_per_part),:,:]
            output_array[:,int((parts_ - 1) * rows_per_part):,:,:] = \
                f_.variables[variable_name][:,int((parts_ - 1) * rows_per_part):,:,:]
            return output_array

    elif len(var_shape) > 4:
        print('ERROR! variable has more than 4 dimensions, not implemented for this many dimentions')
        return None
def get_himawari8_2000m_NCI(YYYYmmddHHMM_str, channel_number, output_format='png',
                            output_path='/g/k10/la6753/data/', row_start=0, row_stop=5500, col_start=0,
                            col_stop=5500):
    """
    gets array from himawari-8 netcdf files and extracts only the indicated channel at the indicated time. saves to output_path
    :param YYYYmmddHHMM_str: string with the time in four digits for year, two digits for months...
    :param channel_number: int or float with the number of the channel ('01'-'16')
    :param output_format: string with either 'png' or 'numpy'. If png the array will be saved used store_array_to_png, otherwise numpy.save will be used
    :param output_path: string with the path, or full filename to be used to save the file
    :param row_start: int with the row number to start the crop
    :param row_stop: int with the row number to stop the crop
    :param col_start: int with the coloumn number to start the crop
    :param col_stop: int with the coloumn number to stop the crop
    :return: None
    """
    channel_number_str = str(int(channel_number)).zfill(2)

    filename_ = '/g/data/rr5/satellite/obs/himawari8/FLDK/' + \
                YYYYmmddHHMM_str[:4] + '/' + YYYYmmddHHMM_str[4:6] + '/' + YYYYmmddHHMM_str[6:8] + \
                '/' + YYYYmmddHHMM_str[8:12] + \
                '/' + YYYYmmddHHMM_str + '00' + \
                '-P1S-ABOM_OBS_' \
                'B' + channel_number_str + \
                '-PRJ_GEOS141_2000-HIMAWARI8-AHI.nc'

    if os.path.exists(filename_):

        f_ = nc.Dataset(filename_)

        variable_name = ''
        for var_key in f_.variables.keys():
            if len(var_key.split('channel')) > 1:
                variable_name = var_key
                break

        array_ = f_.variables[variable_name][0, row_start:row_stop, col_start:col_stop]

        if output_path[-1] == '/' or output_path[-1] == '\\':
            if output_format == 'png':
                output_filename = output_path + 'him_2000m_ch' + channel_number_str + '_' + YYYYmmddHHMM_str + '.png'
            else:
                output_filename = output_path + 'him_2000m_ch' + channel_number_str + '_' + YYYYmmddHHMM_str + '.npy'
        else:
            output_filename = output_path

        if output_format == 'png':
            store_array_to_png(array_, output_filename)
        else:
            np.save(output_filename, array_)

    else:
        print('File not available for time stamp:', YYYYmmddHHMM_str)
def get_HIM8_NCI(YYYYmmddHHMM_str, channel_number_str, minlat_minlon_maxlat_maxlon_tuple=None,
                 path_='/g/data/ra22/satellite-products/arc/obs/himawari-ahi/fldk/v1.0/',
                 return_latlon_arr=False):

    resolution_1000 = [1,2,4]
    resolution_500 = [3]
    channel_number_int = int(channel_number_str)

    resolution_ = 2000
    if channel_number_int in resolution_1000:
        resolution_ = 1000
    elif channel_number_int in resolution_500:
        resolution_ = 500

    year_ = YYYYmmddHHMM_str[:4]
    month_ = YYYYmmddHHMM_str[4:6]
    day_ = YYYYmmddHHMM_str[6:8]
    hour_min = YYYYmmddHHMM_str[8:]

    filename_ = path_ + '{0}/{1}/{2}/{3}/{4}00-P1S-ABOM_OBS_B{5}-PRJ_GEOS141_{6}-HIMAWARI8-AHI.nc'.format(
        year_, month_, day_, hour_min, YYYYmmddHHMM_str, channel_number_str, resolution_)

    if minlat_minlon_maxlat_maxlon_tuple is not None:
        minlat_ = minlat_minlon_maxlat_maxlon_tuple[0]
        minlon_ = minlat_minlon_maxlat_maxlon_tuple[1]
        maxlat_ = minlat_minlon_maxlat_maxlon_tuple[2]
        maxlon_ = minlat_minlon_maxlat_maxlon_tuple[3]


        filename_latlon = path_ + 'ancillary/00000000000000-P1S-ABOM_GEOM_SENSOR-' \
                                  'PRJ_GEOS141_{0}-HIMAWARI8-AHI.nc'.format(resolution_)

        with nc.Dataset(filename_latlon) as file_:
            shape_tuple = file_.variables['lat'].shape

            mid_point_x = int(shape_tuple[1]/2)
            mid_point_y = int(shape_tuple[2]/2)

            lat_array = file_.variables['lat'][0,:,mid_point_x].filled(np.nan)
            lon_array = file_.variables['lon'][0,mid_point_y,:].filled(np.nan)

            row_1 = np.nanargmin(np.abs(lat_array - maxlat_))
            row_2 = np.nanargmin(np.abs(lat_array - minlat_))
            col_1 = np.nanargmin(np.abs(lon_array - minlon_))
            col_2 = np.nanargmin(np.abs(lon_array - maxlon_))

            if return_latlon_arr:
                lat_array_2D = file_.variables['lat'][0,row_1:row_2,col_1:col_2].filled(np.nan)
                lon_array_2D = file_.variables['lon'][0,row_1:row_2,col_1:col_2].filled(np.nan)

        with nc.Dataset(filename_) as file_:
            variable_name = ''
            for var_key in file_.variables.keys():
                if len(var_key.split('channel')) > 1:
                    variable_name = var_key
                    break
            output_array = file_.variables[variable_name][0,row_1:row_2,col_1:col_2].filled(np.nan)


    else:
        with nc.Dataset(filename_) as file_:
            variable_name = ''
            for var_key in file_.variables.keys():
                if len(var_key.split('channel')) > 1:
                    variable_name = var_key
                    break
            output_array = file_.variables[variable_name][0,:,:].filled(np.nan)

    if return_latlon_arr:
        return output_array, lat_array_2D, lon_array_2D
    else:
        return output_array
def get_HIM8_truecolor_NCI(YYYYmmddHHMM_str, minlat_minlon_maxlat_maxlon_tuple=None, return_latlon_arr=False):
    slope_ = 12
    inflex_ = .2
    max_ = 256

    H8_r_500 = get_HIM8_NCI(YYYYmmddHHMM_str, '03', minlat_minlon_maxlat_maxlon_tuple)
    H8_r = column_average_discrete_2D(row_average_discrete_2D(H8_r_500, 2), 2)
    H8_g = get_HIM8_NCI(YYYYmmddHHMM_str, '02', minlat_minlon_maxlat_maxlon_tuple)
    if return_latlon_arr or minlat_minlon_maxlat_maxlon_tuple is not None:
        H8_b, lat_array_2D, lon_array_2D = get_HIM8_NCI(YYYYmmddHHMM_str, '01',
                                                        minlat_minlon_maxlat_maxlon_tuple, return_latlon_arr=True)

        # trim if needed
        shape_500 = H8_r.shape
        shape_1000 = H8_g.shape
        if shape_1000[0] > shape_500[0]:
            H8_g = H8_g[1:, :]
            H8_b = H8_b[1:, :]
            lat_array_2D = lat_array_2D[1:, :]
            lon_array_2D = lon_array_2D[1:, :]
        if shape_1000[0] < shape_500[0]:
            H8_r = H8_r[1:, :]
        if shape_1000[1] > shape_500[1]:
            H8_g = H8_g[:, 1:]
            H8_b = H8_b[:, 1:]
            lat_array_2D = lat_array_2D[:, 1:]
            lon_array_2D = lon_array_2D[:, 1:]
        if shape_1000[1] < shape_500[1]:
            H8_r = H8_r[:, 1:]
    else:
        H8_b = get_HIM8_NCI(YYYYmmddHHMM_str, '01')

    img_ = np.zeros((H8_b.shape[0], H8_b.shape[1], 3), dtype='uint8')
    img_[:, :, 0] = sigmoid(H8_r, slope_, inflex_, max_)
    img_[:, :, 1] = sigmoid(H8_g, slope_, inflex_, max_)
    img_[:, :, 2] = sigmoid(H8_b, slope_, inflex_, max_)

    if return_latlon_arr:
        return img_, lat_array_2D, lon_array_2D
    else:
        return img_



# ERA5 and interim data
def create_virtual_sondes_from_ERA5(time_stamp_sec, lat_lon_tuple, era5_file_levels_ncFile, era5_file_surface_ncFile,
                                    max_time_delta_sec=21600, show_prints=True):
    close_level_file=False
    close_surface_file=False

    if type(era5_file_levels_ncFile) == str:
        era5_file_levels = nc.Dataset(era5_file_levels_ncFile)
        close_level_file = True
    else:
        era5_file_levels = era5_file_levels_ncFile
    if type(era5_file_surface_ncFile) == str:
        era5_file_surface = nc.Dataset(era5_file_surface_ncFile)
        close_surface_file = True
    else:
        era5_file_surface = era5_file_surface_ncFile

    time_era5_levels_sec = time_era5_to_seconds(era5_file_levels.variables['time'][:])
    time_era5_surface_sec = time_era5_to_seconds(era5_file_surface.variables['time'][:])
    r_era5_levels_1 = time_to_row_sec(time_era5_levels_sec, time_stamp_sec)
    r_era5_surface_1 = time_to_row_sec(time_era5_surface_sec, time_stamp_sec)

    if np.abs(time_era5_levels_sec[r_era5_levels_1] - time_stamp_sec) > max_time_delta_sec:
        if show_prints: print('error time gap is too large', )
        return None

    # find row and column for the lat lon
    lat_index, lon_index = find_index_from_lat_lon(era5_file_levels.variables['latitude'][:].data,
                                                   era5_file_levels.variables['longitude'][:].data,
                                                   lat_lon_tuple[0], lat_lon_tuple[1])


    if show_prints: print('creating input arrays')
    t_profile = kelvin_to_celsius(era5_file_levels.variables['t'][r_era5_levels_1, :, lat_index, lon_index].data)
    if show_prints: print('created t_array')
    td_profile = calculate_dewpoint_from_T_RH(t_profile, era5_file_levels.variables['r'][r_era5_levels_1, :, lat_index, lon_index].data)
    if show_prints: print('created Td_array')
    h_profile = era5_file_levels.variables['z'][r_era5_levels_1, :, lat_index, lon_index].data / gravity_
    if show_prints: print('created z_array')
    u_profile = era5_file_levels.variables['u'][r_era5_levels_1, :, lat_index, lon_index].data
    if show_prints: print('created u_array')
    v_profile = era5_file_levels.variables['v'][r_era5_levels_1, :, lat_index, lon_index].data
    if show_prints: print('created v_array')
    p_profile = era5_file_levels.variables['level'][:].data  # hPa
    if show_prints: print('created p_array')
    surface_p = era5_file_surface.variables['sp'][r_era5_surface_1, lat_index, lon_index] / 100 # / 100 to convert Pa to hPa
    if show_prints: print('created sp_array')



    # trim profiles from surface to top
    # find which levels should be included
    levels_total = 0
    for i_ in range(p_profile.shape[0]):
        if p_profile[i_] > surface_p:
            break
        levels_total += 1

    ####################################### find extrapolations
    surface_t = interpolate_1d(np.log(surface_p), np.log(p_profile), t_profile)
    surface_td = interpolate_1d(np.log(surface_p), np.log(p_profile), td_profile)
    surface_u = interpolate_1d(np.log(surface_p), np.log(p_profile), u_profile)
    surface_v = interpolate_1d(np.log(surface_p), np.log(p_profile), v_profile)
    surface_h = interpolate_1d(np.log(surface_p), np.log(p_profile), h_profile)

    # create temp arrays
    T_array = np.zeros(levels_total + 1, dtype=float)
    Td_array = np.zeros(levels_total + 1, dtype=float)
    Q_array = np.zeros(levels_total + 1, dtype=float)
    U_array = np.zeros(levels_total + 1, dtype=float)
    V_array = np.zeros(levels_total + 1, dtype=float)
    H_array = np.zeros(levels_total + 1, dtype=float)
    P_array = np.zeros(levels_total + 1, dtype=float)

    T_array[:levels_total] = t_profile[:levels_total]
    Td_array[:levels_total] = td_profile[:levels_total]
    U_array[:levels_total] = u_profile[:levels_total]
    V_array[:levels_total] = v_profile[:levels_total]
    H_array[:levels_total] = h_profile[:levels_total]
    P_array[:levels_total] = p_profile[:levels_total]

    T_array[-1] = surface_t
    Td_array[-1] = surface_td
    U_array[-1] = surface_u
    V_array[-1] = surface_v
    H_array[-1] = surface_h
    P_array[-1] = surface_p

    if close_level_file:
        era5_file_levels.close()
    if close_surface_file:
        era5_file_surface.close()

    return P_array, H_array, T_array, Td_array, U_array, V_array
def era5_download_save(year_str, month_str_list, day_str_list, output_filename, surface_only=False, format_="netcdf",
                       time_str_list=None, variable_name_list=None, pressure_level_list=None, area_="-10/108/-45/155"):
    """
    Downloads 0.25 degree resolution ERA5 data from official repository. Make sure you follow efficiency guidelines
    :param year_str: string of the year you want the data from. cannot be a list of years.
    :param month_str_list: list of strings, or single string, of the months you want. example ['08', '09']
    :param day_str_list: same as months but for days
    :param output_filename: full path and filename of the output file
    :param surface_only: If true then only surface variables will be downloaded. Default is false, (pressure levels)
    :param format_: can be "netcdf" (default) or 'grib"
    :param time_str_list: list of hours strings in HH:MM format, default is full day hourly
    :param variable_name_list: list of variable name strings, see
    https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-pressure-levels?tab=form for all available vars.
    if None, default variables will be downloaded, see which below under variable_name_list
    :param pressure_level_list: list of string of pressure levels to be downloaded. If none will download all between
    1000 and 250.
    :param area_: string of longitudes and latitudes of the domain to be downloaded. Default is set to Australia. Set
    to None for global. The format is upperLeft_Lat/upperLeft_Lon/lowerRight_Lat/lowerRight_Lon.
    :return: None
    """

    # get ERA5 data
    client_ = cdsapi.Client()

    if pressure_level_list is None:
        pressure_level_list = [
            '250','300','350',
            '400','450','500',
            '550','600','650',
            '700','750','775',
            '800','825','850',
            '875','900','925',
            '950','975','1000'
        ]

    if variable_name_list is None:
        if surface_only:
            variable_name_list = [
                'surface_pressure',
                'total_precipitation',
                '2m_temperature',
                '2m_dewpoint_temperature'
            ]
        else:
            variable_name_list = [
                'geopotential',
                'relative_humidity',
                'specific_humidity',
                'specific_rain_water_content',
                'temperature',
                'u_component_of_wind',
                'v_component_of_wind'
            ]

    if time_str_list is None:
        time_str_list = [
                            '00:00', '01:00', '02:00',
                            '03:00', '04:00', '05:00',
                            '06:00', '07:00', '08:00',
                            '09:00', '10:00', '11:00',
                            '12:00', '13:00', '14:00',
                            '15:00', '16:00', '17:00',
                            '18:00', '19:00', '20:00',
                            '21:00', '22:00', '23:00'
                        ]

    if surface_only:
        client_.retrieve('reanalysis-era5-single-levels',
                         {
                             'variable':variable_name_list,
                             "product_type": "reanalysis",
                             'year': year_str,
                             'month': month_str_list,
                             'day': day_str_list,
                             'time': time_str_list,
                             "area": area_,
                             "grid": "0.25/0.25",
                             "format": format_
                         },
                         output_filename)
    else:
        client_.retrieve("reanalysis-era5-pressure-levels",
                        {
                            'variable': variable_name_list,
                            'pressure_level': pressure_level_list,
                            "product_type": "reanalysis",
                            'year': year_str,
                            'month': month_str_list,
                            'day': day_str_list,
                            'time': time_str_list,
                            "area": area_,
                            "grid": "0.25/0.25",
                            "format": format_
                        },
                        output_filename)
def era_interim_download_save(year_str, month_str_list, day_str_list, output_filename,
                       time_str_list=None, variable_name_list=None, pressure_level_list=None, area_="-10/108/-45/155"):
    # get interim data
    client_ = cdsapi.Client()

    if pressure_level_list is None:
        pressure_level_list = [
            '250','300','350',
            '400','450','500',
            '550','600','650',
            '700','750','775',
            '800','825','850',
            '875','900','925',
            '950','975','1000'
        ]

    if variable_name_list is None:
        variable_name_list = [
            'geopotential','ozone_mass_mixing_ratio','potential_vorticity',
            'relative_humidity','specific_humidity','temperature',
            'u_component_of_wind','v_component_of_wind','vertical_velocity'
        ]

    if time_str_list is None:
        time_str_list = [
                            '00:00', '01:00', '02:00',
                            '03:00', '04:00', '05:00',
                            '06:00', '07:00', '08:00',
                            '09:00', '10:00', '11:00',
                            '12:00', '13:00', '14:00',
                            '15:00', '16:00', '17:00',
                            '18:00', '19:00', '20:00',
                            '21:00', '22:00', '23:00'
                        ]


    client_.retrieve("reanalysis-era5-pressure-levels",
                    {
                        'variable': variable_name_list,
                        'pressure_level': pressure_level_list,
                        "product_type": "reanalysis",
                        'year': year_str,
                        'month': month_str_list,
                        'day': day_str_list,
                        'time': time_str_list,
                        "area": area_,
                        "grid": "0.25/0.25",
                        "format": "netcdf"
                    },
                    output_filename)
def era5_get_surface_interpolated_vars(era5_file_levels_ncFile, era5_file_surface_ncFile, show_prints=True,
                                       time_start_str_YYYYmmDDHHMM=None, time_stop_str_YYYYmmDDHHMM=None):
    close_level_file=False
    close_surface_file=False

    if type(era5_file_levels_ncFile) == str:
        era5_file_levels = nc.Dataset(era5_file_levels_ncFile)
        close_level_file = True
    else:
        era5_file_levels = era5_file_levels_ncFile
    if type(era5_file_surface_ncFile) == str:
        era5_file_surface = nc.Dataset(era5_file_surface_ncFile)
        close_surface_file = True
    else:
        era5_file_surface = era5_file_surface_ncFile

    time_era5_levels_sec = time_era5_to_seconds(era5_file_levels.variables['time'][:])


    # trim time
    r_1 = 0
    r_2 = -1
    if time_start_str_YYYYmmDDHHMM is not None:
        r_1 = time_to_row_str(time_era5_levels_sec, time_start_str_YYYYmmDDHHMM)
    if time_stop_str_YYYYmmDDHHMM is not None:
        r_2 = time_to_row_str(time_era5_levels_sec, time_stop_str_YYYYmmDDHHMM)

    time_era5_sec = time_era5_levels_sec[r_1:r_2]


    if show_prints: print('creating input arrays')
    t_profile = kelvin_to_celsius(era5_file_levels.variables['t'][r_1:r_2, 10:, :, :].data)
    if show_prints: print('created t_array')
    td_profile = calculate_dewpoint_from_T_RH(t_profile, era5_file_levels.variables['r'][r_1:r_2, 10:, :, :].data)
    if show_prints: print('created Td_array')
    h_profile = era5_file_levels.variables['z'][r_1:r_2, 10:, :, :].data / gravity_
    if show_prints: print('created z_array')
    u_profile = era5_file_levels.variables['u'][r_1:r_2, 10:, :, :].data
    if show_prints: print('created u_array')
    v_profile = era5_file_levels.variables['v'][r_1:r_2, 10:, :, :].data
    if show_prints: print('created v_array')
    p_profile = era5_file_levels.variables['level'][10:].data  # hPa
    if show_prints: print('created p_array')
    surface_p = era5_file_surface.variables['sp'][r_1:r_2, :, :] / 100 # / 100 to convert Pa to hPa
    if show_prints: print('created sp_array')
    q_profile = era5_file_levels.variables['q'][r_1:r_2, 10:, :, :].data
    if show_prints: print('created q_array')



    ####################################### find extrapolations
    surface_t = np.zeros((surface_p.shape), dtype=float)
    surface_td = np.zeros((surface_p.shape), dtype=float)
    surface_u = np.zeros((surface_p.shape), dtype=float)
    surface_v = np.zeros((surface_p.shape), dtype=float)
    surface_h = np.zeros((surface_p.shape), dtype=float)
    surface_q = np.zeros((surface_p.shape), dtype=float)

    if show_prints: print('starting interpolation of every point in time')
    for r_ in range(time_era5_sec.shape[0]):
        p_progress_bar(r_,time_era5_sec.shape[0])
        for lat_ in range(surface_p.shape[1]):
            for lon_ in range(surface_p.shape[2]):

                surface_t [r_,lat_,lon_] = interpolate_1d(np.log(surface_p[r_,lat_,lon_]),
                                                     np.log(p_profile), t_profile [r_,:,lat_,lon_])
                surface_td[r_,lat_,lon_] = interpolate_1d(np.log(surface_p[r_,lat_,lon_]),
                                                     np.log(p_profile), td_profile[r_,:,lat_,lon_])
                surface_u [r_,lat_,lon_] = interpolate_1d(np.log(surface_p[r_,lat_,lon_]),
                                                     np.log(p_profile), u_profile [r_,:,lat_,lon_])
                surface_v [r_,lat_,lon_] = interpolate_1d(np.log(surface_p[r_,lat_,lon_]),
                                                     np.log(p_profile), v_profile [r_,:,lat_,lon_])
                surface_h [r_,lat_,lon_] = interpolate_1d(np.log(surface_p[r_,lat_,lon_]),
                                                     np.log(p_profile), h_profile [r_,:,lat_,lon_])
                surface_q [r_,lat_,lon_] = interpolate_1d(np.log(surface_p[r_,lat_,lon_]),
                                                     np.log(p_profile), q_profile [r_,:,lat_,lon_])



    if close_level_file:
        era5_file_levels.close()
    if close_surface_file:
        era5_file_surface.close()

    return surface_t, surface_td, surface_u, surface_v, surface_h, surface_q, time_era5_sec
def get_era5_gadi_data(variable_name,
                       time_start_YYYYmmddHH=None, time_stop_YYYYmmddHH=None,
                       lat_min_max_tuple=None, lon_min_max_tuple=None, level_min_max_tuple=None, verbose_=False):
    """
    Retrieve ERA5 reanalysis data from Gadi's supercomputer archive.

    This function extracts specific ERA5 atmospheric or surface data based on the provided parameters, including
    variable type, spatial region, pressure levels, and temporal range.

    Args:
        variable_name (str): The name of the variable to retrieve. Must match a key in `era5_name_dict`.
                             Examples include 't' (temperature) and 'q' (specific humidity).
        time_start_YYYYmmddHH (str, optional): Start time in the format 'YYYYmmddHH'. Defaults to None
                                              (includes all times).
        time_stop_YYYYmmddHH (str, optional): Stop time in the format 'YYYYmmddHH'. Defaults to None
                                              (includes all times).
        lat_min_max_tuple (tuple, optional): Latitude range as (min_lat, max_lat). Defaults to None
                                             (includes all latitudes).
        lon_min_max_tuple (tuple, optional): Longitude range as (min_lon, max_lon). Defaults to None
                                             (includes all longitudes).
        level_min_max_tuple (tuple, optional): Pressure level range as (min_level, max_level).
                                               Only applicable for pressure-level variables. Defaults to None.
        verbose_ (bool, optional): If True, prints additional information during execution. Defaults to False.

    Returns:
        dict: A dictionary containing the requested ERA5 data with the following keys:
            - 'time_arr' (numpy.ndarray): Array of time steps (in seconds since a reference epoch, i.e. unix time).
            - 'level_arr' (numpy.ndarray, optional): Array of pressure levels (only for pressure-level variables).
            - 'lat_arr' (numpy.ndarray): Array of latitude values.
            - 'lon_arr' (numpy.ndarray): Array of longitude values.
            - 'desc_' (str): Description of the requested variable.
            - 'var_type' (str): Type of variable ('pressure' or 'single').
            - 'data_arr' (numpy.ndarray): Data array for the requested variable.

    Raises:
        KeyError: If the `variable_name` is not found in `era5_name_dict`.
        ValueError: If `level_min_max_tuple` is provided for a single-level variable.
        Exception: For invalid or inconsistent input data.

    Example:
        Retrieve temperature data for a specific region and time range:

        ```python
        data = get_era5_gadi_data(
            variable_name='t',
            time_start_YYYYmmddHH='2023010100',
            time_stop_YYYYmmddHH='2023013123',
            lat_min_max_tuple=(-10, 10),
            lon_min_max_tuple=(100, 150),
            level_min_max_tuple=(500, 850),
            verbose_=True
        )
        print(data['data_arr'])
        ```
    """


    era5_name_dict = {
        'crwc': ('crwc', 'Specific rain water content', 'pressure'),
        't': ('t', 'Temperature', 'pressure'),
        'clwc': ('clwc', 'Specific cloud liquid water content', 'pressure'),
        'q': ('q', 'Specific humidity', 'pressure'),
        'w': ('w', 'Vertical velocity', 'pressure'),
        'cc': ('cc', 'Fraction of cloud cover', 'pressure'),
        'ciwc': ('ciwc', 'Specific cloud ice water content', 'pressure'),
        'cswc': ('cswc', 'Specific snow water content', 'pressure'),
        'vo': ('vo', 'Vorticity (relative)', 'pressure'),
        'o3': ('o3', 'Ozone mass mixing ratio', 'pressure'),
        'v': ('v', 'V component of wind', 'pressure'),
        'z': ('z', 'Geopotential', 'pressure'),
        'pv': ('pv', 'Potential vorticity', 'pressure'),
        'd': ('d', 'Divergence', 'pressure'),
        'u': ('u', 'U component of wind', 'pressure'),
        'r': ('r', 'Relative humidity', 'pressure'),
        'lssfr': ('lssfr', 'Large scale snowfall rate water equivalent', 'single'),
        'mlssr': ('mlssr', 'Mean large-scale snowfall rate', 'single'),
        'viman': ('p66.162', 'Vertical integral of northward mass flux', 'single'),
        'mp1': ('mp1', 'Mean wave period based on first moment', 'single'),
        'tvl': ('tvl', 'Type of low vegetation', 'single'),
        'src': ('src', 'Skin reservoir content', 'single'),
        'deg0l': ('deg0l', '0 degrees C isothermal level (atm)', 'single'),
        'skt': ('skt', 'Skin temperature', 'single'),
        '100v': ('v100', '100 metre V wind component', 'single'),
        'viiwn': ('p91.162', 'Vertical integral of northward cloud frozen water flux ', 'single'),
        'aluvp': ('aluvp', 'UV visible albedo for direct radiation', 'single'),
        'mvimd': ('mvimd', 'Mean vertically integrated moisture divergence', 'single'),
        'wss': ('wss', 'Wave Spectral Skewness', 'single'),
        'vst': ('vst', 'V-component stokes drift', 'single'),
        'vimd': ('vimd', 'Vertically integrated moisture divergence', 'single'),
        'ishf': ('ishf', 'Instantaneous surface sensible heat flux', 'single'),
        'chnk': ('chnk', 'Charnock', 'single'),
        'rhoao': ('p140209', 'Air density over the oceans', 'single'),
        'sd': ('sd', 'Snow depth', 'single'),
        'mx2t': ('mx2t', 'Maximum temperature at 2 metres since previous post-processing', 'single'),
        'str': ('str', 'Surface net thermal radiation', 'single'),
        'ewss': ('ewss', 'Eastward turbulent surface stress', 'single'),
        '10fg': ('fg10', '10 metre wind gust since previous post-processing', 'single'),
        'mntss': ('mntss', 'Mean northward turbulent surface stress', 'single'),
        'tco3': ('tco3', 'Total column ozone', 'single'),
        'swvl1': ('swvl1', 'Volumetric soil water layer 1', 'single'),
        'ttrc': ('ttrc', 'Top net thermal radiation, clear sky', 'single'),
        'mlspr': ('mlspr', 'Mean large-scale precipitation rate', 'single'),
        'ssr': ('ssr', 'Surface net solar radiation', 'single'),
        'mtdwswrf': ('mtdwswrf', 'Mean top downward short-wave radiation flux', 'single'),
        'vimad': ('p81.162', 'Vertical integral of divergence of mass flux', 'single'),
        'vithen': ('p70.162', 'Vertical integral of northward heat flux', 'single'),
        'dctb': ('dctb', 'Duct base height', 'single'),
        'alnip': ('alnip', 'Near IR albedo for direct radiation', 'single'),
        'cbh': ('cbh', 'Cloud base height', 'single'),
        'fdir': ('fdir', 'Total sky direct solar radiation at surface', 'single'),
        'sshf': ('sshf', 'Surface sensible heat flux', 'single'),
        'i10fg': ('i10fg', 'Instantaneous 10 metre wind gust', 'single'),
        'lblt': ('lblt', 'Lake bottom temperature', 'single'),
        'swvl4': ('swvl4', 'Volumetric soil water layer 4', 'single'),
        '10u': ('u10', '10 metre U wind component', 'single'),
        'mwp1': ('p140123', 'Mean wave period of first swell partition', 'single'),
        'megwss': ('megwss', 'Mean eastward gravity wave surface stress', 'single'),
        'ltlt': ('ltlt', 'Lake total layer temperature', 'single'),
        'dwps': ('dwps', 'Wave spectral directional width for swell', 'single'),
        'e': ('e', 'Evaporation', 'single'),
        'lgws': ('lgws', 'Eastward gravity wave surface stress', 'single'),
        'msdrswrf': ('msdrswrf', 'Mean surface direct short-wave radiation flux', 'single'),
        'stl4': ('stl4', 'Soil temperature level 4', 'single'),
        'strd': ('strd', 'Surface thermal radiation downwards', 'single'),
        'ptype': ('ptype', 'Precipitation type', 'single'),
        'viwvn': ('p72.162', 'Vertical integral of northward water vapour flux', 'single'),
        'csfr': ('csfr', 'Convective snowfall rate water equivalent', 'single'),
        'mssror': ('mssror', 'Mean sub-surface runoff rate', 'single'),
        'gwd': ('gwd', 'Gravity wave dissipation', 'single'),
        'vitoen': ('p76.162', 'Vertical integral of northward total energy flux', 'single'),
        'cvh': ('cvh', 'High vegetation cover', 'single'),
        'lmlt': ('lmlt', 'Lake mix-layer temperature', 'single'),
        'istl3': ('istl3', 'Ice temperature layer 3', 'single'),
        'p2ww': ('p2ww', 'Mean wave period based on second moment for wind waves', 'single'),
        'tcsw': ('tcsw', 'Total column snow water', 'single'),
        'p1ps': ('p1ps', 'Mean wave period based on first moment for swell', 'single'),
        'vima': ('p53.162', 'Vertical integral of mass of atmosphere', 'single'),
        'vithe': ('p60.162', 'Vertical integral of thermal energy', 'single'),
        'msqs': ('msqs', 'Mean square slope of waves', 'single'),
        'lai-hv': ('lai_hv', 'Leaf area index, high vegetation', 'single'),
        'tcw': ('tcw', 'Total column water', 'single'),
        'ssrd': ('ssrd', 'Surface solar radiation downwards', 'single'),
        'mxtpr': ('mxtpr', 'Maximum total precipitation rate since previous post-processing', 'single'),
        'uvb': ('uvb', 'Downward UV radiation at the surface', 'single'),
        'acwh': ('acwh', 'Altimeter corrected wave height', 'single'),
        'vipie': ('p61.162', 'Vertical integral of potential+internal energy', 'single'),
        'mcpr': ('mcpr', 'Mean convective precipitation rate', 'single'),
        'slt': ('slt', 'Soil type', 'single'),
        'msl': ('msl', 'Mean sea level pressure', 'single'),
        'mer': ('mer', 'Mean evaporation rate', 'single'),
        'totalx': ('totalx', 'Total totals index', 'single'),
        'swh': ('swh', 'Significant height of combined wind waves and swell', 'single'),
        'sst': ('sst', 'Sea surface temperature', 'single'),
        'mpww': ('mpww', 'Mean period of wind waves', 'single'),
        'vithee': ('p69.162', 'Vertical integral of eastward heat flux', 'single'),
        'tsn': ('tsn', 'Temperature of snow layer', 'single'),
        '100u': ('u100', '100 metre U wind component', 'single'),
        'dwww': ('dwww', 'Wave spectral directional width for wind waves', 'single'),
        'tciw': ('tciw', 'Total column cloud ice water', 'single'),
        'blh': ('blh', 'Boundary layer height', 'single'),
        'vimat': ('p92.162', 'Vertical integral of mass tendency', 'single'),
        'tclw': ('tclw', 'Total column cloud liquid water', 'single'),
        'mwp': ('mwp', 'Mean wave period', 'single'),
        'hcc': ('hcc', 'High cloud cover', 'single'),
        'mp2': ('mp2', 'Mean zero-crossing wave period', 'single'),
        'ilspf': ('ilspf', 'Instantaneous large-scale surface precipitation fraction', 'single'),
        'cp': ('cp', 'Convective precipitation', 'single'),
        'nsss': ('nsss', 'Northward turbulent surface stress', 'single'),
        'pev': ('pev', 'Potential evaporation', 'single'),
        'viwve': ('p71.162', 'Vertical integral of eastward water vapour flux', 'single'),
        'istl2': ('istl2', 'Ice temperature layer 2', 'single'),
        'msr': ('msr', 'Mean snowfall rate', 'single'),
        'wdw': ('wdw', 'Wave spectral directional width', 'single'),
        'viec': ('p64.162', 'Vertical integral of energy conversion', 'single'),
        'vioze': ('p77.162', 'Vertical integral of eastward ozone flux', 'single'),
        'mtnlwrfcs': ('mtnlwrfcs', 'Mean top net long-wave radiation flux, clear sky', 'single'),
        'mdts': ('mdts', 'Mean direction of total swell', 'single'),
        'licd': ('licd', 'Lake ice depth', 'single'),
        'msnswrfcs': ('msnswrfcs', 'Mean surface net short-wave radiation flux, clear sky', 'single'),
        'strdc': ('strdc', 'Surface thermal radiation downward clear-sky', 'single'),
        'mwp3': ('p140129', 'Mean wave period of third swell partition', 'single'),
        'stl1': ('stl1', 'Soil temperature level 1', 'single'),
        'awh': ('awh', 'Altimeter wave height', 'single'),
        'ro': ('ro', 'Runoff', 'single'),
        'alnid': ('alnid', 'Near IR albedo for diffuse radiation', 'single'),
        'sf': ('sf', 'Snowfall', 'single'),
        'iews': ('iews', 'Instantaneous eastward turbulent surface stress', 'single'),
        'bld': ('bld', 'Boundary layer dissipation', 'single'),
        'zust': ('zust', 'Friction velocity', 'single'),
        'aluvd': ('aluvd', 'UV visible albedo for diffuse radiation', 'single'),
        'inss': ('inss', 'Instantaneous northward turbulent surface stress', 'single'),
        'wmb': ('wmb', 'Model bathymetry', 'single'),
        'msdwswrfcs': ('msdwswrfcs', 'Mean surface downward short-wave radiation flux, clear sky', 'single'),
        'mtpr': ('mtpr', 'Mean total precipitation rate', 'single'),
        'swvl3': ('swvl3', 'Volumetric soil water layer 3', 'single'),
        'tmax': ('tmax', 'Period corresponding to maximum individual wave height', 'single'),
        'mwp2': ('p140126', 'Mean wave period of second swell partition', 'single'),
        'crr': ('crr', 'Convective rain rate', 'single'),
        'cl': ('cl', 'Lake cover', 'single'),
        'cdww': ('cdww', 'Coefficient of drag with waves', 'single'),
        'lcc': ('lcc', 'Low cloud cover', 'single'),
        'tsr': ('tsr', 'Top net solar radiation', 'single'),
        'mcsr': ('mcsr', 'Mean convective snowfall rate', 'single'),
        'tcslw': ('tcslw', 'Total column supercooled liquid water', 'single'),
        'vitoee': ('p75.162', 'Vertical integral of eastward total energy flux', 'single'),
        'ssrdc': ('ssrdc', 'Surface solar radiation downward clear-sky', 'single'),
        'flsr': ('flsr', 'Forecast logarithm of surface roughness for heat', 'single'),
        'ust': ('ust', 'U-component stokes drift', 'single'),
        'fsr': ('fsr', 'Forecast surface roughness', 'single'),
        'msnlwrfcs': ('msnlwrfcs', 'Mean surface net long-wave radiation flux, clear sky', 'single'),
        'tauoc': ('tauoc', 'Normalized stress into ocean', 'single'),
        'lsrr': ('lsrr', 'Large scale rain rate', 'single'),
        'vign': ('p74.162', 'Vertical integral of northward geopotential flux', 'single'),
        'vike': ('p59.162', 'Vertical integral of kinetic energy', 'single'),
        'asn': ('asn', 'Snow albedo', 'single'),
        'vige': ('p73.162', 'Vertical integral of eastward geopotential flux', 'single'),
        'mbld': ('mbld', 'Mean boundary layer dissipation', 'single'),
        'msror': ('msror', 'Mean surface runoff rate', 'single'),
        'vigd': ('p85.162', 'Vertical integral of divergence of geopotential flux', 'single'),
        'tp': ('tp', 'Total precipitation', 'single'),
        'vikee': ('p67.162', 'Vertical integral of eastward kinetic energy flux', 'single'),
        'vilwe': ('p88.162', 'Vertical integral of eastward cloud liquid water flux', 'single'),
        'dndza': ('dndza', 'Mean vertical gradient of refractivity inside trapping layer', 'single'),
        'swh2': ('p140124', 'Significant wave height of second swell partition', 'single'),
        'v10n': ('v10n', 'Neutral wind at 10 m v-component', 'single'),
        'swh1': ('p140121', 'Significant wave height of first swell partition', 'single'),
        'mn2t': ('mn2t', 'Minimum temperature at 2 metres since previous post-processing', 'single'),
        'msdrswrfcs': ('msdrswrfcs', 'Mean surface direct short-wave radiation flux, clear sky', 'single'),
        'mtnswrfcs': ('mtnswrfcs', 'Mean top net short-wave radiation flux, clear sky', 'single'),
        'lshf': ('lshf', 'Lake shape factor', 'single'),
        'istl1': ('istl1', 'Ice temperature layer 1', 'single'),
        '2d': ('d2m', '2 metre dewpoint temperature', 'single'),
        'mpts': ('mpts', 'Mean period of total swell', 'single'),
        'tplt': ('tplt', 'Trapping layer top height', 'single'),
        '10v': ('v10', '10 metre V wind component', 'single'),
        'mntpr': ('mntpr', 'Minimum total precipitation rate since previous post-processing', 'single'),
        'vilwd': ('p79.162', 'Vertical integral of divergence of cloud liquid water flux', 'single'),
        'shww': ('shww', 'Significant height of wind waves', 'single'),
        'viiwe': ('p90.162', 'Vertical integral of eastward cloud frozen water flux', 'single'),
        'bfi': ('bfi', 'Benjamin-Feir index', 'single'),
        'mper': ('mper', 'Mean potential evaporation rate', 'single'),
        'vilwn': ('p89.162', 'Vertical integral of northward cloud liquid water flux', 'single'),
        'fal': ('fal', 'Forecast albedo', 'single'),
        'anor': ('anor', 'Angle of sub-gridscale orography', 'single'),
        'tcc': ('tcc', 'Total cloud cover', 'single'),
        'mwd1': ('p140122', 'Mean wave direction of first swell partition', 'single'),
        'wsk': ('wsk', 'Wave spectral kurtosis', 'single'),
        'msnlwrf': ('msnlwrf', 'Mean surface net long-wave radiation flux', 'single'),
        'msmr': ('msmr', 'Mean snowmelt rate', 'single'),
        'ttr': ('ttr', 'Top net thermal radiation', 'single'),
        'swvl2': ('swvl2', 'Volumetric soil water layer 2', 'single'),
        'ssro': ('ssro', 'Sub-surface runoff', 'single'),
        'sdfor': ('sdfor', 'Standard deviation of filtered subgrid orography', 'single'),
        'viiwd': ('p80.162', 'Vertical integral of divergence of cloud frozen water flux', 'single'),
        'sp': ('sp', 'Surface pressure', 'single'),
        'msdwswrf': ('msdwswrf', 'Mean surface downward short-wave radiation flux', 'single'),
        'viwvd': ('p84.162', 'Vertical integral of divergence of moisture flux', 'single'),
        'p1ww': ('p1ww', 'Mean wave period based on first moment for wind waves', 'single'),
        'wstar': ('p140208', 'Free convective velocity over the oceans', 'single'),
        'ssrc': ('ssrc', 'Surface net solar radiation, clear sky', 'single'),
        'smlt': ('smlt', 'Snowmelt', 'single'),
        'arrc': ('arrc', 'Altimeter range relative correction', 'single'),
        'tisr': ('tisr', 'TOA incident solar radiation', 'single'),
        'wsp': ('wsp', 'Wave spectral peakedness', 'single'),
        'cape': ('cape', 'Convective available potential energy', 'single'),
        'isor': ('isor', 'Anisotropy of sub-gridscale orography', 'single'),
        'tsrc': ('tsrc', 'Top net solar radiation, clear sky', 'single'),
        'slhf': ('slhf', 'Surface latent heat flux', 'single'),
        'mror': ('mror', 'Mean runoff rate', 'single'),
        'vitoed': ('p86.162', 'Vertical integral of divergence of total energy flux', 'single'),
        'lsp': ('lsp', 'Large-scale precipitation', 'single'),
        'cin': ('cin', 'Convective inhibition', 'single'),
        'lsf': ('lsf', 'Large-scale snowfall', 'single'),
        'vimae': ('p65.162', 'Vertical integral of eastward mass flux', 'single'),
        'tcwv': ('tcwv', 'Total column water vapour', 'single'),
        'viken': ('p68.162', 'Vertical integral of northward kinetic energy flux', 'single'),
        'tvh': ('tvh', 'Type of high vegetation', 'single'),
        'lai-lv': ('lai_lv', 'Leaf area index, low vegetation', 'single'),
        'msdwuvrf': ('msdwuvrf', 'Mean surface downward UV radiation flux', 'single'),
        'ie': ('ie', 'Instantaneous moisture flux', 'single'),
        'strc': ('strc', 'Surface net thermal radiation, clear sky', 'single'),
        'mser': ('mser', 'Mean snow evaporation rate', 'single'),
        'mdww': ('mdww', 'Mean direction of wind waves', 'single'),
        'rsn': ('rsn', 'Snow density', 'single'),
        'tcrw': ('tcrw', 'Total column rain water', 'single'),
        'vithed': ('p83.162', 'Vertical integral of divergence of thermal energy flux', 'single'),
        'mcc': ('mcc', 'Medium cloud cover', 'single'),
        'lsm': ('lsm', 'Land-sea mask', 'single'),
        'u10n': ('u10n', 'Neutral wind at 10 m u-component', 'single'),
        'cdir': ('cdir', 'Clear-sky direct solar radiation at surface', 'single'),
        'cvl': ('cvl', 'Low vegetation cover', 'single'),
        'csf': ('csf', 'Convective snowfall', 'single'),
        'mtnlwrf': ('mtnlwrf', 'Mean top net long-wave radiation flux', 'single'),
        'kx': ('kx', 'K index', 'single'),
        'viozd': ('p87.162', 'Vertical integral of divergence of ozone flux', 'single'),
        'vitoe': ('p63.162', 'Vertical integral of total energy', 'single'),
        'sro': ('sro', 'Surface runoff', 'single'),
        'shts': ('shts', 'Significant height of total swell', 'single'),
        'mgws': ('mgws', 'Northward gravity wave surface stress', 'single'),
        'lspf': ('lspf', 'Large-scale precipitation fraction', 'single'),
        'dl': ('dl', 'Lake depth', 'single'),
        'vit': ('p54.162', 'Vertical integral of temperature', 'single'),
        'mwd3': ('p140128', 'Mean wave direction of third swell partition', 'single'),
        '2t': ('t2m', '2 metre temperature', 'single'),
        'slor': ('slor', 'Slope of sub-gridscale orography', 'single'),
        'swh3': ('p140127', 'Significant wave height of third swell partition', 'single'),
        'lmld': ('lmld', 'Lake mix-layer depth', 'single'),
        'istl4': ('istl4', 'Ice temperature layer 4', 'single'),
        'ci': ('siconc', 'Sea ice area fraction', 'single'),
        'mngwss': ('mngwss', 'Mean northward gravity wave surface stress', 'single'),
        'mgwd': ('mgwd', 'Mean gravity wave dissipation', 'single'),
        'mwd': ('mwd', 'Mean wave direction', 'single'),
        'lict': ('lict', 'Lake ice temperature', 'single'),
        'pp1d': ('pp1d', 'Peak wave period', 'single'),
        'vipile': ('p62.162', 'Vertical integral of potential+internal+latent energy', 'single'),
        'hmax': ('hmax', 'Maximum individual wave height', 'single'),
        'viozn': ('p78.162', 'Vertical integral of northward ozone flux', 'single'),
        'stl3': ('stl3', 'Soil temperature level 3', 'single'),
        'viked': ('p82.162', 'Vertical integral of divergence of kinetic energy flux', 'single'),
        'mtnswrf': ('mtnswrf', 'Mean top net short-wave radiation flux', 'single'),
        'dwi': ('dwi', '10 metre wind direction', 'single'),
        'p2ps': ('p2ps', 'Mean wave period based on second moment for swell', 'single'),
        'wind': ('wind', '10 metre wind speed', 'single'),
        'sdor': ('sdor', 'Standard deviation of orography', 'single'),
        'mlspf': ('mlspf', 'Mean large-scale precipitation fraction', 'single'),
        'tplb': ('tplb', 'Trapping layer base height', 'single'),
        'mwd2': ('p140125', 'Mean wave direction of second swell partition', 'single'),
        'mslhf': ('mslhf', 'Mean surface latent heat flux', 'single'),
        'msdwlwrfcs': ('msdwlwrfcs', 'Mean surface downward long-wave radiation flux, clear sky', 'single'),
        'es': ('es', 'Snow evaporation', 'single'),
        'msnswrf': ('msnswrf', 'Mean surface net short-wave radiation flux', 'single'),
        'stl2': ('stl2', 'Soil temperature level 2', 'single'),
        'metss': ('metss', 'Mean eastward turbulent surface stress', 'single'),
        'dndzn': ('dndzn', 'Minimum vertical gradient of refractivity inside trapping layer', 'single'),
        'phioc': ('phioc', 'Normalized energy flux into ocean', 'single'),
        'msshf': ('msshf', 'Mean surface sensible heat flux', 'single'),
        'phiaw': ('phiaw', 'Normalized energy flux into waves', 'single'),
        'msdwlwrf': ('msdwlwrf', 'Mean surface downward long-wave radiation flux', 'single'),

    }

    # get the filename variable name and the in-file variable name
    variable_name_infile, desc_, var_type = era5_name_dict[variable_name]
    data_path = f'/g/data/rt52/era5/{var_type}-levels/reanalysis/{variable_name}/'
    if verbose_:
        print(f"variable: {variable_name}, in-file variable name: {variable_name_infile}, variable type: {var_type}")

    if var_type == 'single' and level_min_max_tuple is not None:
        raise_error('The variable name provided is a single level variable but level min max tuple was provided.')

    # get file list
    filename_list = list_files_recursive(data_path)
    if verbose_:
        print(f"{len(filename_list)} files found for this variable")

    # get file list times
    filename_time_start = []
    filename_time_stop = []
    for filename_ in filename_list:
        filename_time_start.append(time_str_to_seconds(filename_.split('_')[-1].split('-')[0], time_format_YMD))
        filename_time_stop.append(time_str_to_seconds(filename_.split('_')[-1].split('-')[1][:-3], time_format_YMD)+
                                  (24*60*60))
    filename_time_start = np.array(filename_time_start)
    filename_time_stop = np.array(filename_time_stop)

    # get filename range
    if time_start_YYYYmmddHH is not None:
        time_start_sec = time_str_to_seconds(time_start_YYYYmmddHH, '%Y%m%d%H')
        index_filename_start = time_to_row_sec(filename_time_start, time_start_sec)
        if filename_time_start[index_filename_start] > time_start_sec:
            index_filename_start -= 1
            if index_filename_start < 0:
                index_filename_start = 0
    else:
        index_filename_start = 0
    if time_stop_YYYYmmddHH is not None:
        time_stop_sec = time_str_to_seconds(time_stop_YYYYmmddHH, '%Y%m%d%H')
        index_filename_stop = time_to_row_sec(filename_time_stop, time_stop_sec)
        if filename_time_stop[index_filename_stop] <= time_stop_sec:
            index_filename_stop += 1
            if index_filename_stop >= len(filename_list) - 1:
                index_filename_stop = len(filename_list) - 1
    else:
        index_filename_stop = len(filename_list) - 1
    # get file list
    file_list = filename_list[index_filename_start:index_filename_stop+1]
    if verbose_:
        print(f"{len(file_list)} files found for the specified time range")

    # get levels index
    if var_type == 'pressure':
        with nc.Dataset(file_list[0]) as file_:
            level_arr_full = file_.variables['level'][:].data
        if level_min_max_tuple is not None:
            level_start, level_stop = level_min_max_tuple
            level_index_start = time_to_row_sec(level_arr_full, level_start)
            if level_arr_full[level_index_start] > level_start:
                level_index_start -= 1
                if level_index_start < 0:
                    level_index_start = 0
            level_index_stop = time_to_row_sec(level_arr_full, level_stop)
            if level_arr_full[level_index_stop] < level_stop:
                level_index_stop += 1
                if level_index_stop > level_arr_full.size:
                    level_index_stop = level_arr_full.size - 1
        else:
            level_index_start = 0
            level_index_stop = level_arr_full.size - 1
        # crop level array
        level_arr = level_arr_full[level_index_start:level_index_stop+1]
        if verbose_:
            print(f"level array loaded and cropped, resulting shape: {level_arr.shape}, min value: {np.min(level_arr)},"
                  f" max value: {np.max(level_arr)}")

    # get spatial domain indexes
    with nc.Dataset(file_list[0]) as file_:
        lat_arr_full = file_.variables['latitude'][:].data
        lon_arr_full = file_.variables['longitude'][:].data
    # lat
    if lat_min_max_tuple is not None:
        lat_start, lat_stop = lat_min_max_tuple
        lat_index_start = time_to_row_sec(lat_arr_full, lat_start)
        if lat_arr_full[lat_index_start] > lat_start:
            lat_index_start += 1
            if lat_index_start > lat_arr_full.size:
                lat_index_start = lat_arr_full.size - 1
        lat_index_stop = time_to_row_sec(lat_arr_full, lat_stop)
        if lat_arr_full[lat_index_stop] < lat_stop:
            lat_index_stop -= 1
            if lat_index_stop < 0:
                lat_index_stop = 0
    else:
        lat_index_start = lat_arr_full.size - 1
        lat_index_stop = 0
    # crop lat array
    lat_arr = lat_arr_full[lat_index_stop:lat_index_start+1]  # inverted because the era5 lat array is decreasing
    if verbose_:
        print(f"latitude array loaded and cropped, resulting shape: {lat_arr.shape}, min value: {np.min(lat_arr)},"
              f" max value: {np.max(lat_arr)}")
    # lon
    if lon_min_max_tuple is not None:
        lon_start, lon_stop = lon_min_max_tuple
        lon_index_start = time_to_row_sec(lon_arr_full, lon_start)
        if lon_arr_full[lon_index_start] > lon_start:
            lon_index_start -= 1
            if lon_index_start < 0:
                lon_index_start = 0
        lon_index_stop = time_to_row_sec(lon_arr_full, lon_stop)
        if lon_arr_full[lon_index_stop] < lon_stop:
            lon_index_stop += 1
            if lon_index_stop > lon_arr_full.size:
                lon_index_stop = lon_arr_full.size - 1
    else:
        lon_index_start = 0
        lon_index_stop = lon_arr_full.size - 1
    # crop lon array
    lon_arr = lon_arr_full[lon_index_start:lon_index_stop+1]
    if verbose_:
        print(f"longitude array loaded and cropped, resulting shape: {lon_arr.shape}, min value: {np.min(lon_arr)},"
              f" max value: {np.max(lon_arr)}")
    # get data array
    time_arr_list = []
    data_arr_list = []
    for filename_ in file_list:
        # get intra file time
        with nc.Dataset(filename_) as file_:
            time_arr_temp_full = time_era5_to_seconds(file_.variables['time'][:].data)
        if time_start_YYYYmmddHH is not None:
            time_start_sec = time_str_to_seconds(time_start_YYYYmmddHH, '%Y%m%d%H')
            index_time_start = time_to_row_sec(time_arr_temp_full, time_start_sec)
            if time_arr_temp_full[index_time_start] > time_start_sec:
                index_time_start -= 1
                if index_time_start < 0:
                    index_time_start = 0
        else:
            index_time_start = 0
        if time_stop_YYYYmmddHH is not None:
            time_stop_sec = time_str_to_seconds(time_stop_YYYYmmddHH, '%Y%m%d%H')
            index_time_stop = time_to_row_sec(time_arr_temp_full, time_stop_sec)
            if time_arr_temp_full[index_time_stop] <= time_stop_sec:
                index_time_stop += 1
                if index_time_stop >= time_arr_temp_full.size - 1:
                    index_time_stop = time_arr_temp_full.size - 1
        else:
            index_time_stop = time_arr_temp_full.size - 1
        # crop time and store in list
        time_arr_list.append(time_arr_temp_full[index_time_start:index_time_stop + 1])

        # get intra file data and store in list
        with nc.Dataset(filename_) as file_:
            if var_type == 'pressure':
                data_arr_list.append(file_.variables[variable_name_infile][
                                     index_time_start:index_time_stop + 1,
                                     level_index_start:level_index_stop + 1,
                                     lat_index_stop:lat_index_start + 1,
                                     lon_index_start:lon_index_stop + 1
                                     ].data)
            else:
                data_arr_list.append(file_.variables[variable_name_infile][
                                     index_time_start:index_time_stop + 1,
                                     lat_index_stop:lat_index_start + 1,
                                     lon_index_start:lon_index_stop + 1
                                     ].data)

    # define output dict
    if var_type == 'pressure':
        output_dict = {
            'time_arr':np.concatenate(time_arr_list, axis=0),
            'level_arr':level_arr,
            'lat_arr':lat_arr,
            'lon_arr':lon_arr,
            'desc_':desc_,
            'var_type':var_type,
            'data_arr': np.concatenate(data_arr_list, axis=0),
        }
    else:
        output_dict = {
            'time_arr':np.concatenate(time_arr_list, axis=0),
            'lat_arr':lat_arr,
            'lon_arr':lon_arr,
            'desc_':desc_,
            'var_type':var_type,
            'data_arr': np.concatenate(data_arr_list, axis=0),
        }
    if verbose_:
        print(f"final time loaded and cropped, resulting shape: {output_dict['time_arr'].shape},"
              f" min value: {time_seconds_to_str(np.min(output_dict['time_arr']), time_format_easy)},"
              f" max value: {time_seconds_to_str(np.max(output_dict['time_arr']), time_format_easy)}")
        print(f"final data loaded and cropped, resulting shape: {output_dict['data_arr'].shape}")

    return  output_dict



# particle trajectory
def trajectory_lat_lon_to_mean_altitude_2D(traj_lat_array, traj_lon_array, traj_alt_array,
                                           lat_min, lat_max, lat_bin_number,
                                           lon_min, lon_max, lon_bin_number,
                                           return_bin_centers=False):


    range_ = [[lon_min, lon_max], [lat_min, lat_max]]
    bins_ = [lon_bin_number, lat_bin_number]
    hist_counts,lon_edges,lat_edges = np.histogram2d(traj_lon_array, traj_lat_array, bins=bins_ ,range=range_)
    hist_alt_sum,lon_edges,lat_edges = np.histogram2d(traj_lon_array, traj_lat_array, bins=bins_ ,range=range_,
                                                      weights=traj_alt_array)

    hist_alt = hist_alt_sum / hist_counts

    hist_alt[hist_counts == 0] = np.nan

    hist_alt = hist_alt.T

    if return_bin_centers:
        lon_centers = lon_edges[:-1] + np.diff(lon_edges)/2
        lat_centers = lat_edges[:-1] + np.diff(lat_edges)/2
        return hist_alt, lon_centers, lat_centers
    else:
        return hist_alt
def trajectory_lat_lon_to_frequency_2D(traj_lat_array, traj_lon_array,
                                        lat_min, lat_max, lat_bin_number,
                                        lon_min, lon_max, lon_bin_number,
                                        return_bin_centers=False):


    range_ = [[lon_min, lon_max], [lat_min, lat_max]]
    bins_ = [lon_bin_number, lat_bin_number]
    hist_counts,lon_edges,lat_edges = np.histogram2d(traj_lon_array, traj_lat_array, bins=bins_ ,range=range_)

    hist_bool = np.array([hist_counts>0])[0,:,:].T

    if return_bin_centers:
        lon_centers = lon_edges[:-1] + np.diff(lon_edges)/2
        lat_centers = lat_edges[:-1] + np.diff(lat_edges)/2
        return hist_bool, lon_centers, lat_centers
    else:
        return hist_bool
def hysplit_traj_array_list_to_frequency_array(trajectories_list,
                                               lat_min, lat_max, lat_bin_number,
                                               lon_min, lon_max, lon_bin_number,
                                               lat_column = 7, lon_column = 8 ):

    # load first to get shape and centers
    hist_bool, lon_centers, lat_centers = trajectory_lat_lon_to_frequency_2D(trajectories_list[0][:,lat_column],
                                                                             trajectories_list[0][:,lon_column],
                                                                             lat_min, lat_max, lat_bin_number,
                                                                             lon_min, lon_max, lon_bin_number,
                                                                             return_bin_centers=True)

    frequency_array_final = np.zeros(hist_bool.shape, dtype=float)
    for trajec_array in trajectories_list:
        frequency_array_final += trajectory_lat_lon_to_frequency_2D(trajec_array[:, lat_column],
                                                                    trajec_array[:, lon_column],
                                                                    lat_min, lat_max, lat_bin_number,
                                                                    lon_min, lon_max, lon_bin_number,
                                                                    return_bin_centers=False)

    return frequency_array_final.T, lat_centers, lon_centers
def hysplit_traj_filename_list_to_frequency_array(list_of_trajectory_filenames, trajectory_hours,
                                                  lat_min, lat_max, lat_bin_number,
                                                  lon_min, lon_max, lon_bin_number,
                                                  lat_column = 7, lon_column = 8 ):

    trajec_array = hysplit_load_freq_endpoints(list_of_trajectory_filenames[0], trajectory_hours)

    # load first to get shape and centers
    hist_bool, lon_centers, lat_centers = trajectory_lat_lon_to_frequency_2D(trajec_array[:,lat_column],
                                                                             trajec_array[:,lon_column],
                                                                             lat_min, lat_max, lat_bin_number,
                                                                             lon_min, lon_max, lon_bin_number,
                                                                             return_bin_centers=True)

    frequency_array_final = np.zeros(hist_bool.shape, dtype=float)
    for trajec_filename in list_of_trajectory_filenames:
        trajec_array = hysplit_load_freq_endpoints(trajec_filename, trajectory_hours)
        frequency_array_final += trajectory_lat_lon_to_frequency_2D(trajec_array[:, lat_column],
                                                                    trajec_array[:, lon_column],
                                                                    lat_min, lat_max, lat_bin_number,
                                                                    lon_min, lon_max, lon_bin_number,
                                                                    return_bin_centers=False)

    return frequency_array_final.T, lat_centers, lon_centers
def trajectory_filename_list_to_frequency_array(list_of_trajectory_filenames,
                                                lat_min, lat_max, lat_bin_number,
                                                lon_min, lon_max, lon_bin_number,
                                                lat_column = 1, lon_column = 2 , lat_offset=0, lon_offset=0):

    trajec_array = np.load(list_of_trajectory_filenames[0])

    # load first to get shape and centers
    hist_bool, lon_centers, lat_centers = trajectory_lat_lon_to_frequency_2D(trajec_array[:,lat_column]-lat_offset,
                                                                             trajec_array[:,lon_column]-lon_offset,
                                                                             lat_min, lat_max, lat_bin_number,
                                                                             lon_min, lon_max, lon_bin_number,
                                                                             return_bin_centers=True)

    frequency_array_final = np.zeros(hist_bool.shape, dtype=float)
    for trajec_filename in list_of_trajectory_filenames:
        trajec_array = np.load(trajec_filename)
        frequency_array_final += trajectory_lat_lon_to_frequency_2D(trajec_array[:, lat_column]-lat_offset,
                                                                    trajec_array[:, lon_column]-lon_offset,
                                                                    lat_min, lat_max, lat_bin_number,
                                                                    lon_min, lon_max, lon_bin_number,
                                                                    return_bin_centers=False)

    return frequency_array_final.T, lat_centers, lon_centers
def trajectory_filename_list_to_3D_altitude_array(list_of_trajectory_filenames,
                                                  lat_min, lat_max, lat_bin_number,
                                                  lon_min, lon_max, lon_bin_number,
                                                  lat_column = 1, lon_column = 2, alt_column = 3,
                                                  lat_offset = 0, lon_offset = 0):

    trajec_array = np.load(list_of_trajectory_filenames[0])

    # load first to get shape and centers
    hist_bool, lon_centers, lat_centers = trajectory_lat_lon_to_mean_altitude_2D(trajec_array[:,lat_column]-lat_offset,
                                                                                 trajec_array[:,lon_column]-lon_offset,
                                                                                 trajec_array[:,alt_column],
                                                                                 lat_min, lat_max, lat_bin_number,
                                                                                 lon_min, lon_max, lon_bin_number,
                                                                                 return_bin_centers=True)

    frequency_array_final = np.zeros((len(list_of_trajectory_filenames),hist_bool.shape[0],hist_bool.shape[1]),
                                     dtype=float)
    for i_, trajec_filename in enumerate(list_of_trajectory_filenames):
        trajec_array = np.load(trajec_filename)
        frequency_array_final[i_,:,:] = trajectory_lat_lon_to_mean_altitude_2D(trajec_array[:,lat_column]-lat_offset,
                                                                               trajec_array[:,lon_column]-lon_offset,
                                                                               trajec_array[:,alt_column],
                                                                               lat_min, lat_max, lat_bin_number,
                                                                               lon_min, lon_max, lon_bin_number,
                                                                               return_bin_centers=False)

    return frequency_array_final, lat_centers, lon_centers


# HYSPLIT
def hysplit_load_freq_endpoints(filename_, number_of_hours):


    file_obj = open(filename_,'r')

    line_list = file_obj.readlines()

    file_obj.close()

    file_traj_list = []
    traj_number = -1
    for line_inx, line_str in enumerate(line_list):
        if line_str == '     1 PRESSURE\n':
            traj_number += 1
            for r_ in range(number_of_hours + 1):
                new_line_list = line_list[line_inx + r_ + 1].split()
                new_line_list.append(traj_number)
                file_traj_list.append(new_line_list)


    arr_ = np.zeros((len(file_traj_list),12), dtype=float)
    for r_ in range(len(file_traj_list)):
        for c_ in range(12):
            arr_[r_,c_] = file_traj_list[r_][c_ + 2]

    return arr_
def hysplit_load_freq_endpoints_all(file_list):

    file_traj_list = []

    for filename_ in file_list:

        file_obj = open(filename_,'r')

        line_list = file_obj.readlines()

        file_obj.close()


        for line_inx, line_str in enumerate(line_list):
            if line_str == '     1 PRESSURE\n':
                for r_ in range(25):
                    file_traj_list.append(line_list[line_inx + r_ + 1].split())

    arr_ = np.zeros((len(file_traj_list),11), dtype=float)
    for r_ in range(len(file_traj_list)):
        for c_ in range(11):
            arr_[r_,c_] = file_traj_list[r_][c_ + 2]

    return arr_
def hysplit_download_and_save_gifs():

    filename_ = 'C:/_output/hysplit_10/gif_list.txt'

    file_obj = open(filename_,'r')

    line_list = file_obj.readlines()

    file_obj.close()

    for line_inx, line_str in enumerate(line_list[:-1]):
        line_list[line_inx] = line_str[:-1]


    for i in range(len(line_list)):
        month_str = '%02.0i' % i

        img_ = PIL_Image.open(BytesIO(requests.get(line_list[i]).content)).convert('RGB')
        img_.save('C:/_output/' + month_str + '.png')

        img_arr = np.array(img_)[88:500,34:450]
        PIL_Image.fromarray(img_arr).save('C:/_output/' + month_str + '_cropped.png')
def plot_hysplit_traj(arr_, resolution_='i', format_='%.2f', cbar_label='', cmap_ = default_cm,
                      color_='gray',dot_size = 15, map_pad=0.05,
                      min_lat=None,max_lat=None,min_lon=None,max_lon=None, ticks_=5., linewidth_=5):
    if not basemap_available:
        print('Optional module basemap was not found, this functions is not available. Please install basemap')
        return None

    fig, ax = plt.subplots()

    if min_lat is None: min_lat = np.nanmin(arr_[:,7])
    if max_lat is None: max_lat = np.nanmax(arr_[:,7])
    if min_lon is None: min_lon = np.nanmin(arr_[:,8])
    if max_lon is None: max_lon = np.nanmax(arr_[:,8])

    m = Basemap(projection='merc',
                llcrnrlat=min_lat -((max_lat-min_lat)*map_pad),urcrnrlat=max_lat +((max_lat-min_lat)*map_pad),
                llcrnrlon=min_lon -((max_lon-min_lon)*map_pad),urcrnrlon=max_lon +((max_lon-min_lon)*map_pad),
                resolution=resolution_)

    parallels = np.arange(0.,90,ticks_)
    meridians = np.arange(0.,360.,ticks_)

    m.fillcontinents(color=color_, zorder=0)
    m.drawmeridians(meridians, labels=[0,0,0,1])
    m.drawparallels(parallels, labels=[1,0,0,0])


    x, y = m(arr_[:,8], arr_[:,7])

    trajs_ = ax.scatter(x, y,lw=0,c=arr_[:,6],s=dot_size, cmap = cmap_)

    m.drawcoastlines(linewidth=linewidth_)
    m.drawcountries(linewidth=linewidth_)

    color_bar = m.colorbar(trajs_, pad="5%", format=format_)
    color_bar.ax.set_ylabel(cbar_label)

    plt.show()
def plot_hysplit_traj_fix(file_list, lat_tuple, lon_tuple, out_path):
    if not basemap_available:
        print('Optional module basemap was not found, this functions is not available. Please install basemap')
        return None

    number_of_hours = 24
    for filename_ in file_list:
        arr_ = hysplit_load_freq_endpoints(filename_, number_of_hours)

        fig = plt.figure(figsize=(8,8))
        ax = fig.add_axes([0.1,0.1,0.8,0.8])

        lon_0 = lon_tuple[0] + (lon_tuple[1] - lon_tuple[0]/2)
        lat_0 = lat_tuple[0] + (lat_tuple[1] - lat_tuple[0]/2)



        m = Basemap(projection='stere',lon_0=lon_0,lat_0=lat_0,
                    llcrnrlat=lat_tuple[0],urcrnrlat=lat_tuple[1],
                    llcrnrlon=lon_tuple[0],urcrnrlon=lon_tuple[1],
                    rsphere=6371200.,resolution='h',area_thresh=10000)

        m.drawcoastlines()
        m.drawcountries()

        x, y = m(arr_[:,8], arr_[:,7])

        trajs_ = ax.scatter(x, y,lw=0,c=arr_[:,6],s=arr_[:,6]+5, cmap = default_cm)

        # cs = m.contour(x,y,arr_[:,6],cmap = cm.jet_r)



        color_bar = m.colorbar(trajs_, pad="5%")
        color_bar.ax.set_ylabel('Hours after release')

        fig.savefig(out_path + filename_.replace('\\','/').split('/')[-1][:-3] +  '.png', bbox_inches='tight')
    # plt.show()
def calculate_mean_time(file_list, lat_tuple, lon_tuple):
    # file_list_irn = sorted(glob.glob(str('E:/hysplit_IRN/' + '*.txt')))
    # file_list_uae = sorted(glob.glob(str('E:/hysplit_UAE/' + '*.txt')))
    # lat_tuple = tuple((24.889974, 26.201930))
    # lon_tuple = tuple((50.727086, 51.729315))

    hit_counter_list = []
    total_counter_list = []
    # month_list_list = []
    month_mean_time = []
    month_std_time = []

    month_probability_list = []

    for filename_ in file_list:
        arr_ = hysplit_load_freq_endpoints(filename_, 24)
        hit_counter = 0
        hit_age = []

        total_number_of_trajs = int(np.max(arr_[:,-1]))

        for traj_ in range(total_number_of_trajs + 1):
            for r_ in range(arr_.shape[0]):
                if arr_[r_,-1] == traj_:
                    if lat_tuple[0] < arr_[r_, 7] < lat_tuple[1] and lon_tuple[0] < arr_[r_, 8] < lon_tuple[1]:
                        hit_counter += 1
                        hit_age.append(arr_[r_, 6])
                        break



        hit_counter_list.append(hit_counter)
        total_counter_list.append(total_number_of_trajs)

        month_probability_list.append(100*hit_counter/total_number_of_trajs)

        # month_list_list.append(hit_age)
        month_mean_time.append(np.mean(hit_age))
        month_std_time.append(np.std(hit_age))

    return month_probability_list, np.array(month_mean_time), hit_counter_list, total_counter_list, np.array(month_std_time)
# WRF
def particle_trajectory_from_wrf(wrf_data_path, start_time_YYYYmmDDHHMM_str, hours_int,
                                 start_point_lat, start_point_lon, start_point_height_m_ASL,
                                 domain_start_number=3, show_progress=False, use_other_domains=True,
                                 time_format_wrf_filename='%Y-%m-%d_%H_%M_%S'):
    """
    Calculates the trajectory of a particle using WRF netcdf output files. Forward and back trajectories are possible.

    Returns a dictionary with four arrays (time, lat, lon, height); these arrays are for the particle. time is in epoch

    :param wrf_data_path: str, absolute path to the folder where the data files are located. i.e. 'C:/out/'

    :param start_time_YYYYmmDDHHMM_str: str, time the trajectory is to start i.e. '201808182350'

    :param hours_int: int, number of hours to follow the particle. Negative for backwards, positive for forward trajs

    :param start_point_lat: float, latitude in degrees of the start point. Negative for southern hemisphere

    :param start_point_lon: float, longitude in degrees of the start point. Can be from -179.99 to 180 or from 0 to 359.99

    :param start_point_height_m_ASL: float, height of the start of the trajectory in meters above sea level

    :param domain_start_number: int, number of the domain name to use to start the path. 3 will look for d03 files

    :param show_progress: bool, if true a progress bar will be printed to show progress of calculation

    :param use_other_domains: bool, if true further paths will be used from outter domains upon reaching the edge of the start domain (if reached)

    :param time_format_wrf_filename: str, format in which WRF output files show their times. Change if the files are using different format

    :return: Dictionary with 'time', 'lat', 'lon', 'height' keys with numpy arrays inside each key.
    """

    # create back trajectory from wrf output
    start_time_sec = time_str_to_seconds(start_time_YYYYmmDDHHMM_str, '%Y%m%d%H%M')
    start_time_sec_original = start_time_sec * 1
    point_lat_lon = [start_point_lat, start_point_lon]
    point_height = start_point_height_m_ASL
    backtraj_hours = hours_int
    backtraj_secs = np.abs(backtraj_hours * 60 * 60)
    if hours_int < 0:
        traj_direction = -1
    elif hours_int > 0:
        traj_direction = 1
    stop_time_sec = start_time_sec + backtraj_secs * traj_direction

    # list wrf files and create file time series
    wrf_file_list = list_files_recursive(wrf_data_path, '_d0' + str(domain_start_number))
    wrf_file_list_times_sec = []
    for filename_ in wrf_file_list:
        wrf_file_list_times_sec.append(time_str_to_seconds(filename_[-19:], time_format_wrf_filename))
    wrf_file_times_sec = np.array(wrf_file_list_times_sec)

    # check that there is enoght data to do particle trajectory
    if traj_direction == -1:
        if wrf_file_times_sec[0] >= start_time_sec + backtraj_secs:
            print('ERROR! the starting time is too close to the start of the simulation')
            return None
    else:
        if wrf_file_times_sec[-1] <= start_time_sec + backtraj_secs:
            print('ERROR! the starting time is too close to the start of the simulation')
            return None

    # get lat lon
    lat_, lon_ = wrf_get_lat_lon(wrf_file_list[0])

    # calculate median grid distance
    lat_delta_mean = np.mean(np.diff(lat_, axis=0))
    lon_delta_mean = np.mean(np.diff(lon_, axis=1))
    m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.mean(lat_))
    lat_delta_mean_meters = lat_delta_mean * m_per_deg_lat
    lon_delta_mean_meters = lon_delta_mean * m_per_deg_lon
    mean_grid_size = np.mean([lat_delta_mean_meters, lon_delta_mean_meters])

    # start output lists
    output_list_time = [start_time_sec]
    output_list_lat = [point_lat_lon[0]]
    output_list_lon = [point_lat_lon[1]]
    output_list_heigh = [point_height]

    if traj_direction == -1:
        while start_time_sec > stop_time_sec:

            if show_progress: p_progress_bar(start_time_sec_original - start_time_sec, backtraj_secs)

            # find spatial index of point
            point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0], point_lat_lon[1])

            # check if point is at edge of domain
            if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                if use_other_domains:
                    # try outer domain
                    if domain_start_number > 1:
                        domain_start_number -= 1
                        wrf_file_list = list_files_recursive(wrf_data_path, '_d0' + str(domain_start_number))
                        if len(wrf_file_list) == 0:
                            print('\nback trajectory reached edge of domain before',
                                  'stipulated hours reached and no outer domain files found')
                            print('hours elapsed:', '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                            break
                        wrf_file_list_times_sec = []
                        for filename_ in wrf_file_list:
                            wrf_file_list_times_sec.append(time_str_to_seconds(filename_[-19:], time_format_wrf_filename))
                        wrf_file_times_sec = np.array(wrf_file_list_times_sec)

                        lat_, lon_ = wrf_get_lat_lon(wrf_file_list[0])
                        point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0], point_lat_lon[1])
                        if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                            print('\nback trajectory reached edge of domain before stipulated hours reached')
                            print('hours elapsed:', '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                            break

                        # calculate median grid distance
                        lat_delta_mean = np.mean(np.diff(lat_, axis=0))
                        lon_delta_mean = np.mean(np.diff(lon_, axis=1))
                        m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.mean(lat_))
                        lat_delta_mean_meters = lat_delta_mean * m_per_deg_lat
                        lon_delta_mean_meters = lon_delta_mean * m_per_deg_lon
                        mean_grid_size = np.mean([lat_delta_mean_meters, lon_delta_mean_meters])


                    else:

                        print('\nback trajectory reached edge of outermost domain before stipulated hours reached')
                        print('hours elapsed:', '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                        break
                else:
                    print('\nback trajectory reached edge selected domain before stipulated hours reached')
                    print('hours elapsed:', '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                    break

            # find starting files index
            file_index_1 = time_to_row_sec(wrf_file_times_sec, start_time_sec)
            file_index_2 = file_index_1 - 1
            if wrf_file_times_sec[file_index_1] - start_time_sec < 0:
                file_index_1 += 1
                file_index_2 += 1

            # calculate temporal weight for each file
            Weight_T_1 = np.abs(wrf_file_times_sec[file_index_1] - start_time_sec)
            Weight_T_2 = np.abs(wrf_file_times_sec[file_index_2] - start_time_sec)
            W_T_sum = Weight_T_2 + Weight_T_1
            Weight_T_1 = 1 - (Weight_T_1 / W_T_sum)
            Weight_T_2 = 1 - (Weight_T_2 / W_T_sum)

            # find the 4 grids closest to the point, place point_r and point_c on the top-left of the point
            if lat_[point_r, point_c] - point_lat_lon[0] > 0:
                point_r -= 1
            if lon_[point_r, point_c] - point_lat_lon[1] > 0:
                point_c -= 1

            # create distance array to closest 4 points (2 by 2 square)
            D_H = distance_array_lat_lon_2D_arrays_degress_to_meters(lat_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     lon_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     point_lat_lon[0], point_lat_lon[1])

            # get point height array
            Z_ = wrf_get_height_m(wrf_file_list[file_index_1], (point_r, point_c), square_size_int=2)

            # find height index, place Z_index on the bottom of the point
            Z_square_mean = np.mean(np.mean(Z_, axis=-1), axis=-1)
            Z_index = find_min_index_1d_array(np.abs(Z_square_mean - point_height))
            if Z_square_mean[Z_index] - point_height > 0:
                Z_index -= 1
            if Z_index < 0: Z_index += 1  # in case it is bellow surface...

            # create vertical distance array to closest 2 layers
            D_Z = np.abs(Z_[Z_index:Z_index + 2] - point_height)

            # create absolute distance array to closest 8 points
            D_ = np.zeros(D_Z.shape)
            D_[0, :, :] = (D_Z[0, :, :] ** 2 + D_H ** 2) ** 0.5
            D_[1, :, :] = (D_Z[1, :, :] ** 2 + D_H ** 2) ** 0.5

            # check if point is exactly at some grid center, if yes set weight to 1, else, distribute weights (avoids error x/0)
            if np.sum(D_ == 0) == 0:
                # calculate model points' weights
                D_reciprocal = 1 / D_
                Weights_D = D_reciprocal / np.sum(D_reciprocal)
            else:
                # set model points' weights to 1 for exact grid where point happens to be
                Weights_D = D_ * 0
                Weights_D[D_ == 0] = 1

            ################ get 3D wind data ############
            # file 1
            wrf_nc_1 = nc.Dataset(wrf_file_list[file_index_1])
            U_1_stg = wrf_nc_1.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_1_stg = wrf_nc_1.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_1_stg = wrf_nc_1.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_1.close()

            # file 0
            wrf_nc_2 = nc.Dataset(wrf_file_list[file_index_2])
            U_2_stg = wrf_nc_2.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_2_stg = wrf_nc_2.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_2_stg = wrf_nc_2.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_2.close()

            # convert to mass point grid (un-stagger)
            U_1_arr = U_1_stg[:, :, :-1] + np.diff(U_1_stg, axis=2) / 2
            V_1_arr = V_1_stg[:, :-1, :] + np.diff(V_1_stg, axis=1) / 2
            W_1_arr = W_1_stg[:-1, :, :] + np.diff(W_1_stg, axis=0) / 2
            U_2_arr = U_2_stg[:, :, :-1] + np.diff(U_2_stg, axis=2) / 2
            V_2_arr = V_2_stg[:, :-1, :] + np.diff(V_2_stg, axis=1) / 2
            W_2_arr = W_2_stg[:-1, :, :] + np.diff(W_2_stg, axis=0) / 2

            # calculate weighed mean wind components
            U_1_weighed = (Weight_T_1 * np.sum(U_1_arr * Weights_D)) + (Weight_T_2 * np.sum(U_2_arr * Weights_D))
            U_ = U_1_weighed * traj_direction

            V_1_weighed = (Weight_T_1 * np.sum(V_1_arr * Weights_D)) + (Weight_T_2 * np.sum(V_2_arr * Weights_D))
            V_ = V_1_weighed * traj_direction

            W_1_weighed = (Weight_T_1 * np.sum(W_1_arr * Weights_D)) + (Weight_T_2 * np.sum(W_2_arr * Weights_D))
            W_ = W_1_weighed * traj_direction

            # calculate horizontal wind speed
            WS_ = (U_ ** 2 + V_ ** 2) ** 0.5

            # if gotten to a dead point with absolutely no wind, exit loop as it will never leave this point
            if WS_ <= 0:
                break

            # calculate time to move to next grid
            time_grid_change_sec = mean_grid_size / WS_
            # set next time stamp
            start_time_sec = start_time_sec - int(time_grid_change_sec)

            # calculate vertical displacement
            vertical_delta = W_ * time_grid_change_sec

            # calculate horizontal displacement
            lat_delta_meter = V_ * time_grid_change_sec
            lon_delta_meter = U_ * time_grid_change_sec

            # get new point lat lon
            deg_per_m_lat, deg_per_m_lon = degrees_per_meter(point_lat_lon[0])
            point_lat_lon = [point_lat_lon[0] + (deg_per_m_lat * lat_delta_meter),
                             point_lat_lon[1] + (deg_per_m_lon * lon_delta_meter)]

            # get new point height
            point_height = point_height + vertical_delta

            # store data
            output_list_time.append(start_time_sec)
            output_list_lat.append(point_lat_lon[0])
            output_list_lon.append(point_lat_lon[1])
            output_list_heigh.append(point_height)
    else:
        while start_time_sec < stop_time_sec:

            if show_progress: p_progress_bar(start_time_sec - start_time_sec_original, backtraj_secs)

            # find spatial index of point
            point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0], point_lat_lon[1])

            # check if point is at edge of domain
            if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                if use_other_domains:
                    # try outer domain
                    if domain_start_number > 1:
                        domain_start_number -= 1
                        wrf_file_list = list_files_recursive(wrf_data_path, '_d0' + str(domain_start_number))
                        if len(wrf_file_list) == 0:
                            print('\nback trajectory reached edge of domain before',
                                  'stipulated hours reached and no outer domain files found')
                            print('hours elapsed:',
                                  '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                            break
                        wrf_file_list_times_sec = []
                        for filename_ in wrf_file_list:
                            wrf_file_list_times_sec.append(
                                time_str_to_seconds(filename_[-19:], time_format_wrf_filename))
                        wrf_file_times_sec = np.array(wrf_file_list_times_sec)

                        lat_, lon_ = wrf_get_lat_lon(wrf_file_list[0])
                        point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0],
                                                                             point_lat_lon[1])
                        if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                            print('\nback trajectory reached edge of domain before stipulated hours reached')
                            print('hours elapsed:',
                                  '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                            break

                        # calculate median grid distance
                        lat_delta_mean = np.mean(np.diff(lat_, axis=0))
                        lon_delta_mean = np.mean(np.diff(lon_, axis=1))
                        m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.mean(lat_))
                        lat_delta_mean_meters = lat_delta_mean * m_per_deg_lat
                        lon_delta_mean_meters = lon_delta_mean * m_per_deg_lon
                        mean_grid_size = np.mean([lat_delta_mean_meters, lon_delta_mean_meters])


                    else:

                        print('\nback trajectory reached edge of outermost domain before stipulated hours reached')
                        print('hours elapsed:', '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                        break
                else:
                    print('\nback trajectory reached edge selected domain before stipulated hours reached')
                    print('hours elapsed:', '{0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                    break

            # find starting files index
            file_index_1 = time_to_row_sec(wrf_file_times_sec, start_time_sec)
            file_index_2 = file_index_1 + 1
            if wrf_file_times_sec[file_index_1] - start_time_sec < 0:
                file_index_1 += 1
                file_index_2 += 1

            # calculate temporal weight for each file
            Weight_T_1 = np.abs(wrf_file_times_sec[file_index_1] - start_time_sec)
            Weight_T_2 = np.abs(wrf_file_times_sec[file_index_2] - start_time_sec)
            W_T_sum = Weight_T_2 + Weight_T_1
            Weight_T_1 = 1 - (Weight_T_1 / W_T_sum)
            Weight_T_2 = 1 - (Weight_T_2 / W_T_sum)

            # find the 4 grids closest to the point, place point_r and point_c on the top-left of the point
            if lat_[point_r, point_c] - point_lat_lon[0] > 0:
                point_r -= 1
            if lon_[point_r, point_c] - point_lat_lon[1] > 0:
                point_c -= 1

            # create distance array to closest 4 points (2 by 2 square)
            D_H = distance_array_lat_lon_2D_arrays_degress_to_meters(lat_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     lon_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     point_lat_lon[0], point_lat_lon[1])

            # get point height array
            Z_ = wrf_get_height_m(wrf_file_list[file_index_1], (point_r, point_c), square_size_int=2)

            # find height index, place Z_index on the bottom of the point
            Z_square_mean = np.mean(np.mean(Z_, axis=-1), axis=-1)
            Z_index = find_min_index_1d_array(np.abs(Z_square_mean - point_height))
            if Z_square_mean[Z_index] - point_height > 0:
                Z_index -= 1
            if Z_index < 0: Z_index += 1  # in case it is bellow surface...

            # create vertical distance array to closest 2 layers
            D_Z = np.abs(Z_[Z_index:Z_index + 2] - point_height)

            # create absolute distance array to closest 8 points
            D_ = np.zeros(D_Z.shape)
            D_[0, :, :] = (D_Z[0, :, :] ** 2 + D_H ** 2) ** 0.5
            D_[1, :, :] = (D_Z[1, :, :] ** 2 + D_H ** 2) ** 0.5

            # check if point is exactly at some grid center, if yes set weight to 1, else, distribute weights (avoids error x/0)
            if np.sum(D_ == 0) == 0:
                # calculate model points' weights
                D_reciprocal = 1 / D_
                Weights_D = D_reciprocal / np.sum(D_reciprocal)
            else:
                # set model points' weights to 1 for exact grid where point happens to be
                Weights_D = D_ * 0
                Weights_D[D_ == 0] = 1

            ################ get 3D wind data ############
            # file 1
            wrf_nc_1 = nc.Dataset(wrf_file_list[file_index_1])
            U_1_stg = wrf_nc_1.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_1_stg = wrf_nc_1.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_1_stg = wrf_nc_1.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_1.close()

            # file 0
            wrf_nc_2 = nc.Dataset(wrf_file_list[file_index_2])
            U_2_stg = wrf_nc_2.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_2_stg = wrf_nc_2.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_2_stg = wrf_nc_2.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_2.close()

            # convert to mass point grid (un-stagger)
            U_1_arr = U_1_stg[:, :, :-1] + np.diff(U_1_stg, axis=2) / 2
            V_1_arr = V_1_stg[:, :-1, :] + np.diff(V_1_stg, axis=1) / 2
            W_1_arr = W_1_stg[:-1, :, :] + np.diff(W_1_stg, axis=0) / 2
            U_2_arr = U_2_stg[:, :, :-1] + np.diff(U_2_stg, axis=2) / 2
            V_2_arr = V_2_stg[:, :-1, :] + np.diff(V_2_stg, axis=1) / 2
            W_2_arr = W_2_stg[:-1, :, :] + np.diff(W_2_stg, axis=0) / 2

            # calculate weighed mean wind components
            U_1_weighed = (Weight_T_1 * np.sum(U_1_arr * Weights_D)) + (Weight_T_2 * np.sum(U_2_arr * Weights_D))
            U_ = U_1_weighed * traj_direction

            V_1_weighed = (Weight_T_1 * np.sum(V_1_arr * Weights_D)) + (Weight_T_2 * np.sum(V_2_arr * Weights_D))
            V_ = V_1_weighed * traj_direction

            W_1_weighed = (Weight_T_1 * np.sum(W_1_arr * Weights_D)) + (Weight_T_2 * np.sum(W_2_arr * Weights_D))
            W_ = W_1_weighed * traj_direction

            # calculate horizontal wind speed
            WS_ = (U_ ** 2 + V_ ** 2) ** 0.5

            # if gotten to a dead point with absolutely no wind, exit loop as it will never leave this point
            if WS_ <= 0:
                break

            # calculate time to move to next grid
            time_grid_change_sec = mean_grid_size / WS_
            # set next time stamp
            start_time_sec = start_time_sec + int(time_grid_change_sec)

            # calculate vertical displacement
            vertical_delta = W_ * time_grid_change_sec

            # calculate horizontal displacement
            lat_delta_meter = V_ * time_grid_change_sec
            lon_delta_meter = U_ * time_grid_change_sec

            # get new point lat lon
            deg_per_m_lat, deg_per_m_lon = degrees_per_meter(point_lat_lon[0])
            point_lat_lon = [point_lat_lon[0] + (deg_per_m_lat * lat_delta_meter),
                             point_lat_lon[1] + (deg_per_m_lon * lon_delta_meter)]

            # get new point height
            point_height = point_height + vertical_delta

            # store data
            output_list_time.append(start_time_sec)
            output_list_lat.append(point_lat_lon[0])
            output_list_lon.append(point_lat_lon[1])
            output_list_heigh.append(point_height)

    # convert lists to output dictionary
    output_dict = {
        'time'   : np.array(output_list_time),
        'lat'    : np.array(output_list_lat),
        'lon'    : np.array(output_list_lon),
        'height' : np.array(output_list_heigh)
    }

    return output_dict
def particle_trajectory_from_wrf_V2(wrf_data_path, start_time_YYYYmmDDHHMM_str, hours_int,
                                 start_point_lat, start_point_lon, start_point_height_m_ASL,
                                 domain_start_number=3, use_other_domains=True,
                                 time_format_wrf_filename='%Y-%m-%d_%H_%M_%S',
                                 output_time_average_sec=None, output_path=None, array_instead_of_dict=False):
    """
    Calculates the trajectory of a particle using WRF netcdf output files. Forward and back trajectories are possible.

    Returns a dictionary with four arrays (time, lat, lon, height); these arrays are for the particle. time is in epoch

    :param wrf_data_path: str, absolute path to the folder where the data files are located. i.e. 'C:/out/'

    :param start_time_YYYYmmDDHHMM_str: str, time the trajectory is to start i.e. '201808182350'

    :param hours_int: int, number of hours to follow the particle. Negative for backwards, positive for forward trajs

    :param start_point_lat: float, latitude in degrees of the start point. Negative for southern hemisphere

    :param start_point_lon: float, longitude in degrees of the start point. Can be from -179.99 to 180 or from 0 to 359.99

    :param start_point_height_m_ASL: float, height of the start of the trajectory in meters above sea level

    :param domain_start_number: int, number of the domain name to use to start the path. 3 will look for d03 files

    :param use_other_domains: bool, if true further paths will be used from outter domains upon reaching the edge of the start domain (if reached)

    :param time_format_wrf_filename: str, format in which WRF output files show their times. Change if the files are using different format

    :param output_time_average_sec: int, if not None the data will be averaged in discrete time intervals of given seconds

    :param output_path: str, if not None the data will be saved to a file in this path instead of returned

    :param array_instead_of_dict: bool, if True the data will be returned in a numpy array where the columns are time, lat, lon, height

    :return: Dictionary with 'time', 'lat', 'lon', 'height' keys with numpy arrays inside each key.
    """

    process_id = 'wrf_traj'

    # create back trajectory from wrf output
    start_time_sec = time_str_to_seconds(start_time_YYYYmmDDHHMM_str, '%Y%m%d%H%M')
    start_time_sec_original = start_time_sec * 1
    point_lat_lon = [start_point_lat, start_point_lon]
    point_height = start_point_height_m_ASL
    backtraj_hours = hours_int
    backtraj_secs = np.abs(backtraj_hours * 60 * 60)
    if hours_int < 0:
        traj_direction = -1
    elif hours_int > 0:
        traj_direction = 1
    stop_time_sec = start_time_sec + backtraj_secs * traj_direction

    # list wrf files and create file time series
    wrf_file_list = list_files_recursive(wrf_data_path, '_d0' + str(domain_start_number))
    wrf_file_list_times_sec = []
    for filename_ in wrf_file_list:
        wrf_file_list_times_sec.append(time_str_to_seconds(filename_[-19:], time_format_wrf_filename))
    wrf_file_times_sec = np.array(wrf_file_list_times_sec)

    # check that there is enoght data to do particle trajectory
    if traj_direction == -1:
        if wrf_file_times_sec[0] >= start_time_sec + backtraj_secs:
            log_msg('ERROR! the starting time is too close to the start of the simulation',process_id)
            return None
    else:
        if wrf_file_times_sec[-1] <= start_time_sec + backtraj_secs:
            log_msg('ERROR! the starting time is too close to the start of the simulation',process_id)
            return None

    # get lat lon
    lat_, lon_ = wrf_get_lat_lon(wrf_file_list[0])

    # calculate median grid distance
    lat_delta_mean = np.mean(np.diff(lat_, axis=0))
    lon_delta_mean = np.mean(np.diff(lon_, axis=1))
    m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.mean(lat_))
    lat_delta_mean_meters = lat_delta_mean * m_per_deg_lat
    lon_delta_mean_meters = lon_delta_mean * m_per_deg_lon
    mean_grid_size = np.mean([lat_delta_mean_meters, lon_delta_mean_meters])

    # start output lists
    output_list_time = [start_time_sec]
    output_list_lat = [point_lat_lon[0]]
    output_list_lon = [point_lat_lon[1]]
    output_list_heigh = [point_height]

    if traj_direction == -1:
        while start_time_sec > stop_time_sec:

            # find spatial index of point
            point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0], point_lat_lon[1])

            # check if point is at edge of domain
            if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                if use_other_domains:
                    # try outer domain
                    if domain_start_number > 1:
                        domain_start_number -= 1
                        wrf_file_list = list_files_recursive(wrf_data_path, '_d0' + str(domain_start_number))
                        if len(wrf_file_list) == 0:
                            log_msg('\nback trajectory reached edge of domain before' +
                                  'stipulated hours reached and no outer domain files found',process_id)
                            log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60),process_id)
                            break
                        wrf_file_list_times_sec = []
                        for filename_ in wrf_file_list:
                            wrf_file_list_times_sec.append(time_str_to_seconds(filename_[-19:], time_format_wrf_filename))
                        wrf_file_times_sec = np.array(wrf_file_list_times_sec)

                        lat_, lon_ = wrf_get_lat_lon(wrf_file_list[0])
                        point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0], point_lat_lon[1])
                        if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                            log_msg('\nback trajectory reached edge of domain before stipulated hours reached',process_id)
                            log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60),process_id)
                            break

                        # calculate median grid distance
                        lat_delta_mean = np.mean(np.diff(lat_, axis=0))
                        lon_delta_mean = np.mean(np.diff(lon_, axis=1))
                        m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.mean(lat_))
                        lat_delta_mean_meters = lat_delta_mean * m_per_deg_lat
                        lon_delta_mean_meters = lon_delta_mean * m_per_deg_lon
                        mean_grid_size = np.mean([lat_delta_mean_meters, lon_delta_mean_meters])


                    else:

                        log_msg('\nback trajectory reached edge of outermost domain before stipulated hours reached',process_id)
                        log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                        break
                else:
                    log_msg('\nback trajectory reached edge selected domain before stipulated hours reached',process_id)
                    log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60))
                    break

            # find starting files index
            file_index_1 = time_to_row_sec(wrf_file_times_sec, start_time_sec)
            file_index_2 = file_index_1 - 1
            if wrf_file_times_sec[file_index_1] - start_time_sec < 0:
                file_index_1 += 1
                file_index_2 += 1

            # calculate temporal weight for each file
            Weight_T_1 = np.abs(wrf_file_times_sec[file_index_1] - start_time_sec)
            Weight_T_2 = np.abs(wrf_file_times_sec[file_index_2] - start_time_sec)
            W_T_sum = Weight_T_2 + Weight_T_1
            Weight_T_1 = 1 - (Weight_T_1 / W_T_sum)
            Weight_T_2 = 1 - (Weight_T_2 / W_T_sum)

            # find the 4 grids closest to the point, place point_r and point_c on the top-left of the point
            if lat_[point_r, point_c] - point_lat_lon[0] > 0:
                point_r -= 1
            if lon_[point_r, point_c] - point_lat_lon[1] > 0:
                point_c -= 1

            # create distance array to closest 4 points (2 by 2 square)
            D_H = distance_array_lat_lon_2D_arrays_degress_to_meters(lat_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     lon_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     point_lat_lon[0], point_lat_lon[1])

            # get point height array
            Z_ = wrf_get_height_m(wrf_file_list[file_index_1], (point_r, point_c), square_size_int=2)

            # find height index, place Z_index on the bottom of the point
            Z_square_mean = np.mean(np.mean(Z_, axis=-1), axis=-1)
            Z_index = find_min_index_1d_array(np.abs(Z_square_mean - point_height))
            if Z_square_mean[Z_index] - point_height > 0:
                Z_index -= 1
            if Z_index < 0: Z_index += 1  # in case it is bellow surface...

            # create vertical distance array to closest 2 layers
            D_Z = np.abs(Z_[Z_index:Z_index + 2] - point_height)

            # create absolute distance array to closest 8 points
            D_ = np.zeros(D_Z.shape)
            D_[0, :, :] = (D_Z[0, :, :] ** 2 + D_H ** 2) ** 0.5
            D_[1, :, :] = (D_Z[1, :, :] ** 2 + D_H ** 2) ** 0.5

            # check if point is exactly at some grid center, if yes set weight to 1, else, distribute weights (avoids error x/0)
            if np.sum(D_ == 0) == 0:
                # calculate model points' weights
                D_reciprocal = 1 / D_
                Weights_D = D_reciprocal / np.sum(D_reciprocal)
            else:
                # set model points' weights to 1 for exact grid where point happens to be
                Weights_D = D_ * 0
                Weights_D[D_ == 0] = 1

            ################ get 3D wind data ############
            # file 1
            wrf_nc_1 = nc.Dataset(wrf_file_list[file_index_1])
            U_1_stg = wrf_nc_1.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_1_stg = wrf_nc_1.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_1_stg = wrf_nc_1.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_1.close()

            # file 0
            wrf_nc_2 = nc.Dataset(wrf_file_list[file_index_2])
            U_2_stg = wrf_nc_2.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_2_stg = wrf_nc_2.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_2_stg = wrf_nc_2.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_2.close()

            # convert to mass point grid (un-stagger)
            U_1_arr = U_1_stg[:, :, :-1] + np.diff(U_1_stg, axis=2) / 2
            V_1_arr = V_1_stg[:, :-1, :] + np.diff(V_1_stg, axis=1) / 2
            W_1_arr = W_1_stg[:-1, :, :] + np.diff(W_1_stg, axis=0) / 2
            U_2_arr = U_2_stg[:, :, :-1] + np.diff(U_2_stg, axis=2) / 2
            V_2_arr = V_2_stg[:, :-1, :] + np.diff(V_2_stg, axis=1) / 2
            W_2_arr = W_2_stg[:-1, :, :] + np.diff(W_2_stg, axis=0) / 2

            # calculate weighed mean wind components
            U_1_weighed = (Weight_T_1 * np.sum(U_1_arr * Weights_D)) + (Weight_T_2 * np.sum(U_2_arr * Weights_D))
            U_ = U_1_weighed * traj_direction

            V_1_weighed = (Weight_T_1 * np.sum(V_1_arr * Weights_D)) + (Weight_T_2 * np.sum(V_2_arr * Weights_D))
            V_ = V_1_weighed * traj_direction

            W_1_weighed = (Weight_T_1 * np.sum(W_1_arr * Weights_D)) + (Weight_T_2 * np.sum(W_2_arr * Weights_D))
            W_ = W_1_weighed * traj_direction

            # calculate horizontal wind speed
            WS_ = (U_ ** 2 + V_ ** 2) ** 0.5

            # if gotten to a dead point with absolutely no wind, exit loop as it will never leave this point
            if WS_ <= 0:
                break

            # calculate time to move to next grid
            time_grid_change_sec = mean_grid_size / WS_
            # set next time stamp
            start_time_sec = start_time_sec - int(time_grid_change_sec)

            # calculate vertical displacement
            vertical_delta = W_ * time_grid_change_sec

            # calculate horizontal displacement
            lat_delta_meter = V_ * time_grid_change_sec
            lon_delta_meter = U_ * time_grid_change_sec

            # get new point lat lon
            deg_per_m_lat, deg_per_m_lon = degrees_per_meter(point_lat_lon[0])
            point_lat_lon = [point_lat_lon[0] + (deg_per_m_lat * lat_delta_meter),
                             point_lat_lon[1] + (deg_per_m_lon * lon_delta_meter)]

            # get new point height
            point_height = point_height + vertical_delta

            # store data
            output_list_time.append(start_time_sec)
            output_list_lat.append(point_lat_lon[0])
            output_list_lon.append(point_lat_lon[1])
            output_list_heigh.append(point_height)
    else:
        while start_time_sec < stop_time_sec:


            # find spatial index of point
            point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0], point_lat_lon[1])

            # check if point is at edge of domain
            if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                if use_other_domains:
                    # try outer domain
                    if domain_start_number > 1:
                        domain_start_number -= 1
                        wrf_file_list = list_files_recursive(wrf_data_path, '_d0' + str(domain_start_number))
                        if len(wrf_file_list) == 0:
                            log_msg('\nback trajectory reached edge of domain before '+
                                  'stipulated hours reached and no outer domain files found',process_id)
                            log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60),process_id)
                            break
                        wrf_file_list_times_sec = []
                        for filename_ in wrf_file_list:
                            wrf_file_list_times_sec.append(
                                time_str_to_seconds(filename_[-19:], time_format_wrf_filename))
                        wrf_file_times_sec = np.array(wrf_file_list_times_sec)

                        lat_, lon_ = wrf_get_lat_lon(wrf_file_list[0])
                        point_r, point_c = find_index_from_lat_lon_2D_arrays(lat_, lon_, point_lat_lon[0],
                                                                             point_lat_lon[1])
                        if point_r == 0 or point_r > lat_.shape[0] - 2 or point_c == 0 or point_c > lat_.shape[1] - 2:
                            log_msg('\nback trajectory reached edge of domain before stipulated hours reached',process_id)
                            log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60),process_id)
                            break

                        # calculate median grid distance
                        lat_delta_mean = np.mean(np.diff(lat_, axis=0))
                        lon_delta_mean = np.mean(np.diff(lon_, axis=1))
                        m_per_deg_lat, m_per_deg_lon = meter_per_degrees(np.mean(lat_))
                        lat_delta_mean_meters = lat_delta_mean * m_per_deg_lat
                        lon_delta_mean_meters = lon_delta_mean * m_per_deg_lon
                        mean_grid_size = np.mean([lat_delta_mean_meters, lon_delta_mean_meters])


                    else:

                        log_msg('\nback trajectory reached edge of outermost domain before stipulated hours reached',process_id)
                        log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60),process_id)
                        break
                else:
                    log_msg('\nback trajectory reached edge selected domain before stipulated hours reached',process_id)
                    log_msg('hours elapsed: {0:.2f}'.format((start_time_sec_original - start_time_sec) / 60 / 60),process_id)
                    break

            # find starting files index
            file_index_1 = time_to_row_sec(wrf_file_times_sec, start_time_sec)
            file_index_2 = file_index_1 + 1
            if wrf_file_times_sec[file_index_1] - start_time_sec < 0:
                file_index_1 += 1
                file_index_2 += 1

            # calculate temporal weight for each file
            Weight_T_1 = np.abs(wrf_file_times_sec[file_index_1] - start_time_sec)
            Weight_T_2 = np.abs(wrf_file_times_sec[file_index_2] - start_time_sec)
            W_T_sum = Weight_T_2 + Weight_T_1
            Weight_T_1 = 1 - (Weight_T_1 / W_T_sum)
            Weight_T_2 = 1 - (Weight_T_2 / W_T_sum)

            # find the 4 grids closest to the point, place point_r and point_c on the top-left of the point
            if lat_[point_r, point_c] - point_lat_lon[0] > 0:
                point_r -= 1
            if lon_[point_r, point_c] - point_lat_lon[1] > 0:
                point_c -= 1

            # create distance array to closest 4 points (2 by 2 square)
            D_H = distance_array_lat_lon_2D_arrays_degress_to_meters(lat_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     lon_[point_r:point_r + 2, point_c:point_c + 2],
                                                                     point_lat_lon[0], point_lat_lon[1])

            # get point height array
            Z_ = wrf_get_height_m(wrf_file_list[file_index_1], (point_r, point_c), square_size_int=2)

            # find height index, place Z_index on the bottom of the point
            Z_square_mean = np.mean(np.mean(Z_, axis=-1), axis=-1)
            Z_index = find_min_index_1d_array(np.abs(Z_square_mean - point_height))
            if Z_square_mean[Z_index] - point_height > 0:
                Z_index -= 1
            if Z_index < 0: Z_index += 1  # in case it is bellow surface...

            # create vertical distance array to closest 2 layers
            D_Z = np.abs(Z_[Z_index:Z_index + 2] - point_height)

            # create absolute distance array to closest 8 points
            D_ = np.zeros(D_Z.shape)
            D_[0, :, :] = (D_Z[0, :, :] ** 2 + D_H ** 2) ** 0.5
            D_[1, :, :] = (D_Z[1, :, :] ** 2 + D_H ** 2) ** 0.5

            # check if point is exactly at some grid center, if yes set weight to 1, else, distribute weights (avoids error x/0)
            if np.sum(D_ == 0) == 0:
                # calculate model points' weights
                D_reciprocal = 1 / D_
                Weights_D = D_reciprocal / np.sum(D_reciprocal)
            else:
                # set model points' weights to 1 for exact grid where point happens to be
                Weights_D = D_ * 0
                Weights_D[D_ == 0] = 1

            ################ get 3D wind data ############
            # file 1
            wrf_nc_1 = nc.Dataset(wrf_file_list[file_index_1])
            U_1_stg = wrf_nc_1.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_1_stg = wrf_nc_1.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_1_stg = wrf_nc_1.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_1.close()

            # file 0
            wrf_nc_2 = nc.Dataset(wrf_file_list[file_index_2])
            U_2_stg = wrf_nc_2.variables['U'][0, Z_index:Z_index + 2, point_r:point_r + 2, point_c:point_c + 3].data
            V_2_stg = wrf_nc_2.variables['V'][0, Z_index:Z_index + 2, point_r:point_r + 3, point_c:point_c + 2].data
            W_2_stg = wrf_nc_2.variables['W'][0, Z_index:Z_index + 3, point_r:point_r + 2, point_c:point_c + 2].data
            wrf_nc_2.close()

            # convert to mass point grid (un-stagger)
            U_1_arr = U_1_stg[:, :, :-1] + np.diff(U_1_stg, axis=2) / 2
            V_1_arr = V_1_stg[:, :-1, :] + np.diff(V_1_stg, axis=1) / 2
            W_1_arr = W_1_stg[:-1, :, :] + np.diff(W_1_stg, axis=0) / 2
            U_2_arr = U_2_stg[:, :, :-1] + np.diff(U_2_stg, axis=2) / 2
            V_2_arr = V_2_stg[:, :-1, :] + np.diff(V_2_stg, axis=1) / 2
            W_2_arr = W_2_stg[:-1, :, :] + np.diff(W_2_stg, axis=0) / 2

            # calculate weighed mean wind components
            U_1_weighed = (Weight_T_1 * np.sum(U_1_arr * Weights_D)) + (Weight_T_2 * np.sum(U_2_arr * Weights_D))
            U_ = U_1_weighed * traj_direction

            V_1_weighed = (Weight_T_1 * np.sum(V_1_arr * Weights_D)) + (Weight_T_2 * np.sum(V_2_arr * Weights_D))
            V_ = V_1_weighed * traj_direction

            W_1_weighed = (Weight_T_1 * np.sum(W_1_arr * Weights_D)) + (Weight_T_2 * np.sum(W_2_arr * Weights_D))
            W_ = W_1_weighed * traj_direction

            # calculate horizontal wind speed
            WS_ = (U_ ** 2 + V_ ** 2) ** 0.5

            # if gotten to a dead point with absolutely no wind, exit loop as it will never leave this point
            if WS_ <= 0:
                break

            # calculate time to move to next grid
            time_grid_change_sec = mean_grid_size / WS_
            # set next time stamp
            start_time_sec = start_time_sec + int(time_grid_change_sec)

            # calculate vertical displacement
            vertical_delta = W_ * time_grid_change_sec

            # calculate horizontal displacement
            lat_delta_meter = V_ * time_grid_change_sec
            lon_delta_meter = U_ * time_grid_change_sec

            # get new point lat lon
            deg_per_m_lat, deg_per_m_lon = degrees_per_meter(point_lat_lon[0])
            point_lat_lon = [point_lat_lon[0] + (deg_per_m_lat * lat_delta_meter),
                             point_lat_lon[1] + (deg_per_m_lon * lon_delta_meter)]

            # get new point height
            point_height = point_height + vertical_delta

            # store data
            output_list_time.append(start_time_sec)
            output_list_lat.append(point_lat_lon[0])
            output_list_lon.append(point_lat_lon[1])
            output_list_heigh.append(point_height)

    # convert data to array
    output_ = np.column_stack((
        np.array(output_list_time),
        np.array(output_list_lat),
        np.array(output_list_lon),
        np.array(output_list_heigh)
    ))

    # average time wise?
    if output_time_average_sec is not None:
        if traj_direction == -1:
           time_mean, vals_mean = mean_discrete(output_[:,0], output_[:,1:], output_time_average_sec,
                                                stop_time_sec, last_index=start_time_sec_original)
        else:
            time_mean, vals_mean = mean_discrete(output_[:, 0], output_[:, 1:], output_time_average_sec,
                                                 start_time_sec_original, last_index=stop_time_sec)
        output_ = np.column_stack((time_mean, vals_mean))

    # convert lists to output dictionary
    if array_instead_of_dict:
        pass
    else:
        output_ = {
            'time'   : output_[:,0],
            'lat'    : output_[:,1],
            'lon'    : output_[:,2],
            'height' : output_[:,3]
        }

    # save instead of return?
    if output_path is not None:
        filename_ = output_path + start_time_YYYYmmDDHHMM_str + '_' + str(hours_int) + '_' + str(start_point_lat) + '_' + str(start_point_lon) + '_' + str(start_point_height_m_ASL) + '_'
        np.save(filename_, output_)
    else:
        return output_
def create_file_for_particle_trajectory_from_wrf(filename_, time_lat_lon_height__tuple_list, hours_int,
                                                 wrf_data_path='/g/data/k10/la6753/WRF/output_files/',
                                                 domain_start_number=3,
                                                 use_other_domains=True,
                                                 time_format_wrf_filename='%Y-%m-%d_%H_%M_%S',
                                                 output_time_average_sec=300,
                                                 output_path='/scratch/k10/la6753/tmp/WRF_trajectories_200/',
                                                 array_instead_of_dict=True
                                                 ):
    file_header = 'wrf_data_path,' \
                  'start_time_YYYYmmDDHHMM_str,' \
                  'hours_int,' \
                  'start_point_lat,' \
                  'start_point_lon,' \
                  'start_point_height_m_ASL,' \
                  'domain_start_number,' \
                  'use_other_domains,' \
                  'time_format_wrf_filename,' \
                  'output_time_average_sec,' \
                  'output_path,' \
                  'array_instead_of_dict'

    file_ = open(filename_, 'w')

    file_.write(file_header)

    for r_ in range(len(time_lat_lon_height__tuple_list)):
        file_.write('\n')
        file_.write(wrf_data_path + ',')
        file_.write(time_lat_lon_height__tuple_list[r_][0] + ',')
        file_.write(str(hours_int) + ',')
        file_.write(str(time_lat_lon_height__tuple_list[r_][1]) + ',')
        file_.write(str(time_lat_lon_height__tuple_list[r_][2]) + ',')
        file_.write(str(time_lat_lon_height__tuple_list[r_][3]) + ',')
        file_.write(str(domain_start_number) + ',')
        file_.write(str(use_other_domains) + ',')
        file_.write(time_format_wrf_filename + ',')
        file_.write(str(output_time_average_sec) + ',')
        file_.write(output_path + ',')
        file_.write(str(array_instead_of_dict))
    file_.close()

# ACCESS
def create_file_for_particle_trajectory_from_ACCESS(filename_, time_lat_lon_height__tuple_list, hours_int,
                                                    output_time_average_sec=300, array_instead_of_dict=True
                                                    ):
    file_header = 'start_time_YYYYmmDDHHMM_str,' \
                  'hours_int,' \
                  'start_point_lat,' \
                  'start_point_lon,' \
                  'start_point_height_m_ASL,' \
                  'output_time_average_sec,' \
                  'array_instead_of_dict'

    file_ = open(filename_, 'w')

    file_.write(file_header)

    for r_ in range(len(time_lat_lon_height__tuple_list)):
        file_.write('\n')
        file_.write(time_lat_lon_height__tuple_list[r_][0] + ',')
        file_.write(str(hours_int) + ',')
        file_.write(str(time_lat_lon_height__tuple_list[r_][1]) + ',')
        file_.write(str(time_lat_lon_height__tuple_list[r_][2]) + ',')
        file_.write(str(time_lat_lon_height__tuple_list[r_][3]) + ',')
        file_.write(str(output_time_average_sec) + ',')
        file_.write(str(array_instead_of_dict))

    file_.close()

# Radar
def radar_spherical_to_cartesian(azimuth_, elevation_, range_, radar_alt=0.):
    """
    Converts spherical coordinates (azimuth, elevation, range) to Cartesian coordinates (altitude, distance_north,
     distance_east) for a radar.

    Args:
        azimuth_ (ndarray): Array of azimuth angles in degrees.
        elevation_ (ndarray): Array of elevation angles in degrees.
        range_ (ndarray): Array of range values in meters.
        radar_alt (float, optional): Radar altitude in meters. Defaults to 0.

    Returns:
        tuple: Tuple containing altitude array, northward distance array, and eastward distance array. In meters

    """
    radius_earth = 6371000

    # prepare input
    elevation_rad = np.deg2rad(elevation_)
    range_2d, elevation_rad_2d = np.meshgrid(range_, elevation_rad)

    azimuth_1D_rad = np.deg2rad(azimuth_)
    range_2d, azimuth_rad_2d = np.meshgrid(range_, azimuth_1D_rad)


    altitude_m = radar_alt + ((range_2d * np.cos(elevation_rad_2d))**2 +
                              (radius_earth + range_2d * np.sin(elevation_rad_2d))**2 )**0.5 - radius_earth

    horizontal_dist_m = radius_earth * np.arctan((range_2d * np.cos(elevation_rad_2d) /
                                                  ((range_2d * np.sin(elevation_rad_2d)) + radius_earth)))

    distance_north_m = horizontal_dist_m * np.cos(azimuth_rad_2d)
    distance_east__m = horizontal_dist_m * np.sin(azimuth_rad_2d)

    return altitude_m, distance_north_m, distance_east__m
def radar_spherical_to_cartesian_ppi(azimuth_, elevation_, range_, radar_alt=0.):
    """
    Converts spherical coordinates (azimuth, elevation, range) to Cartesian coordinates (altitude, distance_north,
    distance_east) for a radar using a different approach that is faster but has a limitation.
    This function only works for ppi scanning strategies (the radar antenna rotates in a horizontal plane at a fixed
    elevation angle and for every different elevation it has the same azimuthal resolution)

    Args:
        azimuth_ (ndarray): Array of azimuth angles in degrees.
        elevation_ (ndarray): Array of elevation angles in degrees.
        range_ (ndarray): Array of range values in meters.
        radar_alt (float, optional): Radar altitude in meters. Defaults to 0.

    Returns:
        tuple: Tuple containing altitude array, northward distance array, and eastward distance array. In meters

    """
    radius_earth = 6371000

    # prepare input
    elevation_unique = np.array(sorted(set(elevation_)))
    elevation_unique_rad = np.deg2rad(elevation_unique)
    range_2d, elevation_unique_rad2d = np.meshgrid(range_, elevation_unique_rad)

    azimuth_unique = np.array(sorted(set(azimuth_)))
    azimuth_size = azimuth_unique.shape[0]
    azimuth_unique_rad = np.deg2rad(azimuth_unique)
    azimuth_unique_rad_cos = np.cos(azimuth_unique_rad)
    azimuth_unique_rad_sin = np.sin(azimuth_unique_rad)
    _, azimuth_unique_rad_cos_2d = np.meshgrid(range_, azimuth_unique_rad_cos)
    _, azimuth_unique_rad_sin_2d = np.meshgrid(range_, azimuth_unique_rad_sin)

    altitude_m = radar_alt + ((range_2d * np.cos(elevation_unique_rad2d)) ** 2 +
                              (radius_earth + range_2d * np.sin(elevation_unique_rad2d)) ** 2) ** 0.5 - radius_earth

    horizontal_dist_m = radius_earth * np.arctan((range_2d * np.cos(elevation_unique_rad2d) /
                                                  ((range_2d * np.sin(elevation_unique_rad2d)) + radius_earth)))


    altitude_m_2D       = np.zeros((elevation_.shape[0], range_.shape[0]))
    distance_north_m_2D = np.zeros((elevation_.shape[0], range_.shape[0]))
    distance_east__m_2D = np.zeros((elevation_.shape[0], range_.shape[0]))


    for elev_ in range(elevation_unique.shape[0]):
        altitude_m_2D[(elev_*azimuth_size):((elev_+1)*azimuth_size), :] = altitude_m[elev_,:]

        distance_north_m_2D[(elev_*azimuth_size):((elev_+1)*azimuth_size), :] = \
            horizontal_dist_m[elev_, :] * azimuth_unique_rad_cos_2d

        distance_east__m_2D[(elev_*azimuth_size):((elev_+1)*azimuth_size), :] = \
            horizontal_dist_m[elev_, :] * azimuth_unique_rad_sin_2d

    return altitude_m_2D, distance_north_m_2D, distance_east__m_2D
def radar_cartesian_m_to_degrees(distance_north_m, distance_east__m, radar_lat_lon_tuple):

    deg_per_m_lat, deg_per_m_lon = degrees_per_meter(radar_lat_lon_tuple[0])

    distance_north_deg = radar_lat_lon_tuple[0] + deg_per_m_lat * distance_north_m
    distance_east_deg = radar_lat_lon_tuple[1] + deg_per_m_lon * distance_east__m

    return distance_north_deg, distance_east_deg
def radar_reshape_field_3d(field_, azimuth_, range_, sweep_size=360):
    return field_.reshape((int(azimuth_.shape[0] / sweep_size), sweep_size, range_.shape[0]))
def plot_radar_field_ppi(radar_obj, field_name='reflectivity', elevation_angle=0.5, x_range=(-150, 150),
                         y_range=(-150, 150), n_colors=12, add_coastline=False, coastline_color='black',
                         fig_ax=None, cbar_ax=None, cbar_orient='horizontal', vmin_=None, vmax_=None, figsize_=(8,8)):
    """
    Plot a radar field in a Plan Position Indicator (PPI) format.

    This function generates a PPI plot of a specified radar field at a given elevation angle.

    :param radar_obj: (dict) Py-ART radar object containing radar data.
    :param field_name: (str, optional) Name of the radar field to plot. Default is 'reflectivity'.
    :param elevation_angle: (float, optional) Desired elevation angle for the PPI plot. Default is 0.5 degrees.
    :param x_range: (tuple, optional) Custom x-axis range for the plot. Default is (-150, 150).
    :param y_range: (tuple, optional) Custom y-axis range for the plot. Default is (-150, 150).
    :param n_colors: (int, optional) Number of color levels in the colormap. Default is 12.
    :param add_coastline: (bool, optional) Whether to add a coastline to the plot. Default is False.
    :param coastline_color: (str, optional) Color of the coastline (if added). Default is 'black'.
    :param fig_ax: (tuple, optional) Tuple of matplotlib figure and axis for custom plot configuration.
    :param cbar_ax: (tuple, optional) Tuple of matplotlib figure and axis for custom colorbar configuration.
    :param cbar_orient: (str, optional) Orientation of the colorbar ('horizontal' or 'vertical'). Default is 'horizontal'.
    :param vmin_: (float, optional) Minimum value for the color scale. Default is None (automatic).
    :param vmax_: (float, optional) Maximum value for the color scale. Default is None (automatic).

    :return:
        o_: (tuple) Tuple containing the figure, axis, and colorbar instances.
    """
    # find the closest elevation angle
    elevation_angle_closest = radar_obj.elevation['data'][np.argmin(np.abs(radar_obj.elevation['data'] -
                                                                           elevation_angle))]


    o_ = radar_spherical_to_cartesian(radar_obj.azimuth['data'][radar_obj.elevation['data'] == elevation_angle_closest],
                                      radar_obj.elevation['data'][radar_obj.elevation['data'] == elevation_angle_closest],
                                      radar_obj.range['data'],
                                      radar_alt=radar_obj.altitude['data'][0]
                                      )
    altitude_m, distance_north_m, distance_east__m = o_

    if add_coastline:
        deg_per_m_lat, deg_per_m_lon = degrees_per_meter(radar_obj.latitude['data'][0])
        lat_ppi = deg_per_m_lat * distance_north_m + radar_obj.latitude['data'][0]
        lon_ppi = deg_per_m_lon * distance_east__m + radar_obj.longitude['data'][0]

        o_ = p_plot_arr(radar_obj.fields[field_name]['data'][radar_obj.elevation['data'] == elevation_angle_closest],
                        lon_ppi,
                        lat_ppi,
                        # custom_x_range_tuple=x_range, custom_y_range_tuple=y_range,
                        x_header='longitude',
                        y_header='latitude',
                        figsize_=figsize_,
                        cbar_label=field_name,
                        cmap_=cm.get_cmap('jet', n_colors),
                        add_coastlines=add_coastline, coastline_color=coastline_color,
                        fig_ax=fig_ax, cbar_ax=cbar_ax, cbar_orient=cbar_orient,
                        vmin_=vmin_, vmax_=vmax_,
                        )
        fig_adjust(o_[0], left=0.15)
    else:
        o_ = p_plot_arr(radar_obj.fields[field_name]['data'][radar_obj.elevation['data'] == elevation_angle_closest],
                        distance_east__m/1000,
                        distance_north_m/1000,
                        custom_x_range_tuple=x_range, custom_y_range_tuple=y_range,
                        x_header='distance from radar (west-east, km)',
                        y_header='distance from radar (south-north, km)',
                        figsize_=figsize_,
                        cbar_label=field_name,
                        cmap_=cm.get_cmap('jet', n_colors),
                        fig_ax=fig_ax, cbar_ax=cbar_ax, cbar_orient=cbar_orient,
                        vmin_=vmin_, vmax_=vmax_,
                        )
        fig_adjust(o_[0], left=0.15)
    return o_
def get_radar_arr_nonans_from_radar_obj(radar_obj, field_list):
    some_fields_missing = False
    for field_req in field_list:
        if field_req not in radar_obj.fields:
            some_fields_missing = True

    if some_fields_missing:
        output_dict = {}
        for field_name in field_list:
            output_dict[field_name] = np.array([])
        return output_dict

    temp_list = []
    for field_name in field_list:
        temp_list.append(radar_obj.fields[field_name]['data'].filled(np.nan).flatten())

    # remove nans
    output_list = no_nans(temp_list)

    output_dict = {}
    for c_, field_name in enumerate(field_list):
        output_dict[field_name] = output_list[c_]

    return output_dict
def grid_radar_data_visually(radar_obj, variable_to_grid_list,
                             grid_horizontal_size_m=150000, grid_horizontal_resolution_m=1000,
                             grid_vertical_size_m=20000, grid_vertical_resolution_m=500,
                             ray_angular_width=0.5, ray_gate_width=125, edge_threshold=.6, verbose_=False):
    """
    This function is designed for gridding radar ppi data into a cartesian grid format.
    It takes a pyart radar object (radar_obj) and a list of variables (variable_to_grid_list) to be gridded.
    The data is gridded horizontally by using matplolib's pcolormesh and retrieving the image render orthogonal
    grid and then vertically interpolating these into the final 3D grid.

    :param radar_obj: (dict) A pyart radar object containing data to be gridded.
    :param variable_to_grid_list: (list) List of variable names to be gridded.
    :param grid_horizontal_size_m: (float, optional) Horizontal size of the grid in meters.
    :param grid_horizontal_resolution_m: (float, optional) Horizontal resolution of the grid in meters.
    :param grid_vertical_size_m: (float, optional) Vertical size of the grid in meters.
    :param grid_vertical_resolution_m: (float, optional) Vertical resolution of the grid in meters.
    :param ray_angular_width: (float, optional) Angular width of radar rays in degrees.
    :param ray_gate_width: (float, optional) Gate width of radar rays in meters.
    :param edge_threshold: (float, optional) Threshold value for masking edges.
    :param verbose_: (bool, optional) If True, display progress information. Default is False.

    :return:
        gridded_variables_dict: (dict) Dictionary containing gridded variables.
        X_: (ndarray) Array of x-coordinates for the grid.
        Y_: (ndarray) Array of y-coordinates for the grid.
        Z_: (ndarray) Array of z-coordinates for the grid.
        grid_lat: (ndarray) Array of latitude values for the grid.
        grid_lon: (ndarray) Array of longitude values for the grid.
    """

    # setup
    new_grid_lenght = int(grid_horizontal_size_m / grid_horizontal_resolution_m) * 2 + 1
    fig_size = (new_grid_lenght * 2 / 100, new_grid_lenght * 2 / 100)
    downscale_factor = 2  # e.g., from 1000x1000 to 333x333 (approximately)
    new_shape = (new_grid_lenght, new_grid_lenght)

    X_ = np.arange(-grid_horizontal_size_m, grid_horizontal_size_m+1, grid_horizontal_resolution_m)
    Y_ = np.arange(-grid_horizontal_size_m, grid_horizontal_size_m+1, grid_horizontal_resolution_m)
    Z_ = np.arange(0, grid_vertical_size_m+1, grid_vertical_resolution_m)
    deg_per_m_lat, deg_per_m_lon = degrees_per_meter(radar_obj.latitude['data'][0])
    grid_lat = deg_per_m_lat * Y_ + radar_obj.latitude['data'][0]
    grid_lon = deg_per_m_lon * X_ + radar_obj.longitude['data'][0]

    # get unique elevations
    elevation_set = list(sorted(set(radar_obj.elevation['data'])))

    # initialize intermediate output arrays
    altitude_by_elev_array = np.zeros((X_.shape[0], Y_.shape[0], len(elevation_set)))
    values_by_elev_dict = {}
    for var_name in variable_to_grid_list:
        values_by_elev_dict[var_name] = np.zeros((X_.shape[0], Y_.shape[0], len(elevation_set)))

    # grid per elevation angle to intermediate arrays
    for i_, elevation_ in enumerate(elevation_set):
        if verbose_: print('gridding elevation {0}'.format(elevation_))

        # binding boxes for azimuth and range
        azimuth_ = radar_obj.azimuth['data'][radar_obj.elevation['data'] == elevation_]
        azimuth_bnd = np.zeros(azimuth_.shape[0] + 1)
        azimuth_bnd[:-1] = azimuth_ - ray_angular_width
        azimuth_bnd[-1] = azimuth_[-1] + ray_angular_width
        range_ = radar_obj.range['data']
        range_bnd = np.zeros(range_.shape[0] + 1)
        range_bnd[:-1] = range_ - ray_gate_width
        range_bnd[-1] = range_[-1] + ray_gate_width

        # get dimensions in orthogonal scale
        o_ = radar_spherical_to_cartesian(azimuth_bnd, np.zeros(azimuth_bnd.shape[0])+elevation_, range_bnd,
                                              radar_alt=radar_obj.altitude['data'][0])
        altitude_m, distance_north_m, distance_east__m = o_

        # grid altitude
        # normalize array
        vmin_ = np.min(altitude_m)
        vmax_ = np.max(altitude_m)
        array_norm_2D = (altitude_m - vmin_) / (vmax_ - vmin_)
        array_norm = np.zeros((altitude_m.shape[0], altitude_m.shape[1], 3), dtype='uint8')
        array_norm[:,:,0] = array_norm_2D * 255
        array_norm[:,:,1] = array_norm_2D * 255
        array_norm[:,:,2] = array_norm_2D * 255
        # plot
        fig, ax = create_fig_ax(1, 1, figsize=fig_size)
        ax.set_facecolor('black')
        fig_adjust(fig, 0, 1, 0, 1)
        mesh_ = ax.pcolormesh(distance_east__m, distance_north_m, array_norm)
        plt.axis('auto')
        ax.set_xlim((-grid_horizontal_size_m, grid_horizontal_size_m))
        ax.set_ylim((-grid_horizontal_size_m, grid_horizontal_size_m))
        fig.canvas.draw()
        # get orthogonal render of image
        img_arr = np.array(fig.canvas.renderer.buffer_rgba())[::-1, :]
        close_fig(fig)
        # re-scale array
        img_arr_scaled = np.array(img_arr[:, :, 0]) / 255
        original_data = (img_arr_scaled * (vmax_ - vmin_)) + vmin_
        # Reshape the original data into non-overlapping windows
        windowed_data = original_data[:new_shape[0] * downscale_factor, :new_shape[1] * downscale_factor].reshape(
            new_shape[0], downscale_factor, new_shape[1], downscale_factor)
        # Calculate the mean within each window to downscale the data
        alt_grid = np.mean(windowed_data, axis=(1, 3))
        # store gridded altitude to dictionary
        altitude_by_elev_array[:,:,i_] = alt_grid

        for var_name in variable_to_grid_list:
            #  #####  grid variable
            # get variable values and mask
            var_to_grid = radar_obj.fields[var_name]['data'][radar_obj.elevation['data'] == elevation_]
            var_mask = radar_obj.fields[var_name]['data'][radar_obj.elevation['data'] == elevation_].mask

            # plot mask
            fig, ax = create_fig_ax(1,1, figsize=fig_size)
            ax.set_facecolor('black')
            fig_adjust(fig, 0,1,0,1)
            mesh_ = ax.pcolormesh(distance_east__m, distance_north_m, var_mask,
                                  cmap=cm.Greys, vmin=0, vmax=1,)
            plt.axis('auto')
            ax.set_xlim((-grid_horizontal_size_m, grid_horizontal_size_m))
            ax.set_ylim((-grid_horizontal_size_m, grid_horizontal_size_m))
            fig.canvas.draw()
            # get orthogonal render of image
            img_arr = np.array(fig.canvas.renderer.buffer_rgba())
            close_fig(fig)
            img_arr_scaled = np.array(img_arr[:, :, 0]) / 255
            # Reshape the original data into non-overlapping windows
            windowed_data = img_arr_scaled[:new_shape[0] * downscale_factor, :new_shape[1] * downscale_factor].reshape(
                new_shape[0], downscale_factor, new_shape[1], downscale_factor)
            # Calculate the mean within each window to downscale the data
            arr_mask = np.mean(windowed_data, axis=(1, 3)) < edge_threshold

            # normalize array
            vmin_ = np.min(var_to_grid)
            vmax_ = np.max(var_to_grid)
            array_norm_2D = (var_to_grid - vmin_) / (vmax_ - vmin_)
            array_norm = np.zeros((var_to_grid.shape[0], var_to_grid.shape[1], 3), dtype='uint8')
            array_norm[:,:,0] = array_norm_2D * 255
            array_norm[:,:,1] = array_norm_2D * 255
            array_norm[:,:,2] = array_norm_2D * 255
            # plot
            fig, ax = create_fig_ax(1, 1, figsize=fig_size)
            ax.set_facecolor('black')
            fig_adjust(fig, 0, 1, 0, 1)
            mesh_ = ax.pcolormesh(distance_east__m, distance_north_m, array_norm)
            plt.axis('auto')
            ax.set_xlim((-grid_horizontal_size_m, grid_horizontal_size_m))
            ax.set_ylim((-grid_horizontal_size_m, grid_horizontal_size_m))
            fig.canvas.draw()
            # get orthogonal render of image
            img_arr = np.array(fig.canvas.renderer.buffer_rgba())
            close_fig(fig)
            # re-scale array
            img_arr_scaled = np.array(img_arr[:, :, 0]) / 255
            original_data = (img_arr_scaled * (vmax_ - vmin_)) + vmin_
            # Reshape the original data into non-overlapping windows
            windowed_data = original_data[:new_shape[0] * downscale_factor, :new_shape[1] * downscale_factor].reshape(
                new_shape[0], downscale_factor, new_shape[1], downscale_factor)
            # Calculate the mean within each window to downscale the data
            arr_grid = np.mean(windowed_data, axis=(1, 3))
            arr_grid[arr_mask] = np.nan
            arr_grid = arr_grid[::-1, :]

            # store gridded variable to dictionary
            values_by_elev_dict[var_name][:, :, i_] = arr_grid

    gridded_variables_dict = {}
    for var_name in variable_to_grid_list:
        gridded_variables_dict[var_name] = np.zeros((X_.shape[0], Y_.shape[0], Z_.shape[0])) * np.nan

    # interpolate on the vertical
    if verbose_: print('interpolating on the vertical')
    for var_name in variable_to_grid_list:
        for r_ in range(Y_.shape[0]):
            for c_ in range(X_.shape[0]):
                if np.sum(np.isnan(values_by_elev_dict[var_name][r_,c_,:])) < len(elevation_set):
                    gridded_variables_dict[var_name][r_, c_, :] = interpolate_contiguous_or_closest(
                        Z_, altitude_by_elev_array[r_, c_, :], values_by_elev_dict[var_name][r_, c_, :], False)


    return gridded_variables_dict, X_, Y_, Z_, grid_lat, grid_lon
def calculate_SHI_profile(Ze_profile, Alt_profile, height_0C, height_m20C):
    """
    Calculate the Severe Hail Index (SHI) profile using radar reflectivity and temperature profile data.

    The Severe Hail Index is a measure of the potential for severe hail in a vertical profile of the atmosphere.
    It combines radar reflectivity data with temperature information to assess the likelihood of hail formation.

    :param Ze_profile: (numpy.ndarray) Array of radar reflectivity values (in dBZ) at various altitudes.
    :param Alt_profile: (numpy.ndarray) Array of altitudes corresponding to the Ze_profile data (in meters).
    :param height_0C: (float) Height (in meters) of the 0°C isotherm in the atmosphere.
    :param height_m20C: (float) Height (in meters) of the -20°C isotherm in the atmosphere.

    :return:
        SHI: (float) Severe Hail Index value representing the potential for severe hail formation.
            It quantifies the risk of hail in the specified vertical profile of the atmosphere.
    """
    z_lower_bound = 40
    z_upper_bound = 50

    SHI = 0
    if Ze_profile.shape[0] > 1 and Ze_profile.max() > z_lower_bound:
        # sort ascending by height
        Alt_profile_asc = Alt_profile[np.argsort(Alt_profile)]
        Ze_profile_asc = Ze_profile[np.argsort(Alt_profile)]

        # calc reflectivity weighting function
        weight_ref = (Ze_profile_asc - z_lower_bound) / (z_upper_bound - z_lower_bound)
        weight_ref[Ze_profile_asc <= z_lower_bound] = 0
        weight_ref[Ze_profile_asc >= z_upper_bound] = 1

        # calc hail kenitic energy
        hail_KE = (5 * 10 ** -6) * 10 ** (0.084 * Ze_profile_asc) * weight_ref

        # calc temperature based weighting function
        weight_height = (Alt_profile_asc - height_0C) / (height_m20C - height_0C)
        weight_height[Alt_profile_asc <= height_0C] = 0
        weight_height[Alt_profile_asc >= height_m20C] = 1

        # calc severe hail index
        del_alt_cropped = np.diff(Alt_profile_asc)
        del_alt = np.concatenate((del_alt_cropped, np.array([del_alt_cropped[-1]])))
        SHI = 0.1 * np.sum(weight_height * hail_KE * del_alt, axis=0)


    return SHI
def calculate_SHI_from_radar_PPI(radar_obj, radar_id, height_0C, height_m20C,
                                 reflectivity_variable_name='reflectivity',
                                 grid_horizontal_size_m=150000, grid_horizontal_resolution_m=1000):
    """
    Calculate the Severe Hail Index (SHI) from radar PPI data.

    This function computes the Severe Hail Index (SHI) from radar Plan Position Indicator (PPI) data.
    It utilizes radar reflectivity data and radar location information to generate a gridded SHI field.

    :param radar_obj: (dict) Py-ART radar object containing radar data.
    :param radar_id: (str) Unique identifier for the radar.
    :param height_0C: (float) Height (in meters) of the 0°C isotherm in the atmosphere.
    :param height_m20C: (float) Height (in meters) of the -20°C isotherm in the atmosphere.
    :param reflectivity_variable_name: (str, optional) Name of the reflectivity variable in radar_obj.
                                      Default is 'reflectivity'.
    :param grid_horizontal_size_m: (float, optional) Horizontal size of the output grid (in meters).
                                   Default is 150,000 meters.
    :param grid_horizontal_resolution_m: (float, optional) Horizontal resolution of the output grid (in meters).
                                        Default is 1,000 meters.

    :return:
        SHI_2D: (numpy.ndarray) 2D array representing the Severe Hail Index on a grid.
        Ze_max_2D: (numpy.ndarray) 2D array representing the maximum reflectivity on the same grid.
        X_: (numpy.ndarray) Array of x-coordinates for the grid.
        Y_: (numpy.ndarray) Array of y-coordinates for the grid.
        grid_lon: (numpy.ndarray) Array of longitude values for the grid.
        grid_lat: (numpy.ndarray) Array of latitude values for the grid.
    """

    radar_lat = radar_obj.latitude['data'][0]
    radar_lon = radar_obj.longitude['data'][0]
    radar_alt = radar_obj.altitude['data'][0]
    azimuth_ppi = radar_obj.azimuth['data']
    elevation_ppi = radar_obj.elevation['data']
    range_ppi = radar_obj.range['data']
    Ze_ppi = radar_obj.fields[reflectivity_variable_name]['data'].filled(np.nan)
    ppi_size = azimuth_ppi.shape[0] * range_ppi.shape[0]

    # get orthogonal dimensions
    altitude_m_ppi, dist_north_m_ppi, dist_east_m_ppi = radar_spherical_to_cartesian_ppi(azimuth_ppi,
                                                                                         elevation_ppi,
                                                                                         range_ppi, radar_alt)

    # create grid dimensions arrays
    X_ = np.arange(-grid_horizontal_size_m, grid_horizontal_size_m + 1, grid_horizontal_resolution_m)
    Y_ = np.arange(-grid_horizontal_size_m, grid_horizontal_size_m + 1, grid_horizontal_resolution_m)
    deg_per_m_lat, deg_per_m_lon = degrees_per_meter(radar_lat)
    grid_lat = deg_per_m_lat * Y_ + radar_lat
    grid_lon = deg_per_m_lon * X_ + radar_lon

    # create vector for efficient computation
    vector_ = np.column_stack((
        np.zeros(ppi_size),  # for final flat index

        dist_north_m_ppi.flatten(),  # Y
        dist_east_m_ppi.flatten(),  # X

        Ze_ppi.flatten(),  # Ze
        altitude_m_ppi.flatten(),  # Z

    ))

    vector_[(vector_[:, 2] ** 2 + vector_[:, 3] ** 2) ** 0.5 > 150000] = np.nan
    vector_ = no_nans(vector_, False, True)

    # add flatten index to vector based on orthogonal dimensions index
    vector_[:, 0] = orthogonal_index_to_flat(np.array(vector_[:, 2] / grid_horizontal_resolution_m, dtype=int) +
                                             (grid_horizontal_size_m / grid_horizontal_resolution_m),
                                             np.array(vector_[:, 1] / grid_horizontal_resolution_m, dtype=int) +
                                             (grid_horizontal_size_m / grid_horizontal_resolution_m),
                                             ((grid_horizontal_size_m / grid_horizontal_resolution_m) * 2) + 1)

    # sort ascending with respect to flat index
    vector_ = array_2D_sort_ascending_by_column(vector_, 0)

    # get flat index as an integer and get sorted set of unique indexes
    vector_flat_index_array = np.array(vector_[:, 0], dtype=int)
    vector_flat_index_set = list(sorted(set(vector_flat_index_array)))

    # get chunk_indexes (indexes where the vector has the same flat index)
    indices_chunk = np.where(np.diff(vector_flat_index_array) != 0)[0] + 1

    # get list of arrays of these chunks
    Ze_chunks_by_flat_index = np.split(vector_[:, 3], indices_chunk)
    Alt_chunks_by_flat_index = np.split(vector_[:, 4], indices_chunk)

    # initialize output array
    SHI_flat = np.zeros(Y_.shape[0] * X_.shape[0]) * np.nan
    Ze_max_flat = np.zeros(Y_.shape[0] * X_.shape[0]) * np.nan
    for i_, flat_index in enumerate(vector_flat_index_set):
        SHI_flat[flat_index] = calculate_SHI_profile(Ze_chunks_by_flat_index[i_],
                                                     Alt_chunks_by_flat_index[i_],
                                                     height_0C, height_m20C)
        Ze_max_flat[flat_index] = np.max(Ze_chunks_by_flat_index[i_])

    SHI_2D = SHI_flat.reshape((Y_.shape[0], X_.shape[0]))
    Ze_max_2D = Ze_max_flat.reshape((Y_.shape[0], X_.shape[0]))

    return SHI_2D, Ze_max_2D, X_, Y_, grid_lon, grid_lat
def radar_detail_csv_to_dict(filename_csv, filename_dict):

    # load csv
    csv_data = open_csv_file(filename_csv)

    # get list of fields
    field_list = list(csv_data[0,1:])

    # convert to dict
    dict_ = {}
    for r_ in range(1, csv_data.shape[0]):
        radar_id_int = int(csv_data[r_,0])
        dict_[radar_id_int] = {}
        for c_ in range(1, csv_data.shape[1]):
            field_ = field_list[c_ - 1]
            if field_ in ['site_lat', 'site_lon', 'site_alt', 'beamwidth']:
                dict_[radar_id_int][field_] = float(csv_data[r_, c_])
            elif field_ in ['doppler', 'dp']:
                if csv_data[r_, c_] == 'Yes':
                    dict_[radar_id_int][field_] = True
                else:
                    dict_[radar_id_int][field_] = False
            else:
                dict_[radar_id_int][field_] = csv_data[r_, c_]
        
        dict_[radar_id_int]['lat'] = dict_[radar_id_int]['site_lat']
        dict_[radar_id_int]['lon'] = dict_[radar_id_int]['site_lon']
        dict_[radar_id_int]['alt'] = dict_[radar_id_int]['site_alt']

    np.save(filename_dict, dict_)


# BOM
def Lidar_compile_and_convert_txt_to_dict(main_folder_path):
    # main_folder_path = 'D:/Data/LIDAR Data/'

    # create the full file list
    filename_list = []
    path_folders_list = next(os.walk(main_folder_path))[1]
    for sub_folder in path_folders_list:
        if sub_folder[0] == '2':
            path_sub_folders_list = next(os.walk(main_folder_path + sub_folder + '/'))[1]
            for sub_sub_folder in path_sub_folders_list:
                path_sub_sub_sub = main_folder_path + sub_folder + '/' + sub_sub_folder + '/'
                ssss_filelist = sorted(glob.glob(str(path_sub_sub_sub + '*.*')))
                for filename_min in ssss_filelist:
                    filename_list.append(filename_min)
    total_files = len(filename_list)
    print(' number of files to compile:', str(total_files))

    # get first file to get shape
    convertion_output = Lidar_convert_txt_to_array(filename_list[0])
    range_shape = convertion_output[1].shape[0]

    # create arrays
    time_array = np.zeros(total_files)
    range_array = convertion_output[1][:,0]
    ch0_pr2 = np.zeros((total_files, range_shape), dtype=float)
    ch0_mrg = np.zeros((total_files, range_shape), dtype=float)
    ch1_pr2 = np.zeros((total_files, range_shape), dtype=float)
    ch1_mrg = np.zeros((total_files, range_shape), dtype=float)
    ch2_pr2 = np.zeros((total_files, range_shape), dtype=float)
    ch2_mrg = np.zeros((total_files, range_shape), dtype=float)
    print('arrays initialized')

    # populate arrays
    for i_, filename_ in enumerate(filename_list):
        p_progress(i_, total_files)
        convertion_output = Lidar_convert_txt_to_array(filename_)
        time_array[i_] = convertion_output[0]
        ch0_pr2[i_, :] = convertion_output[1][:,1]
        ch0_mrg[i_, :] = convertion_output[1][:,2]
        ch1_pr2[i_, :] = convertion_output[1][:,3]
        ch1_mrg[i_, :] = convertion_output[1][:,4]
        ch2_pr2[i_, :] = convertion_output[1][:,5]
        ch2_mrg[i_, :] = convertion_output[1][:,6]

    # move to dict
    output_dict = {}
    output_dict['time'] = time_array
    output_dict['range'] = range_array
    output_dict['ch0_pr2'] = ch0_pr2
    output_dict['ch0_mrg'] = ch0_mrg
    output_dict['ch1_pr2'] = ch1_pr2
    output_dict['ch1_mrg'] = ch1_mrg
    output_dict['ch2_pr2'] = ch2_pr2
    output_dict['ch2_mrg'] = ch2_mrg


    return output_dict
def Lidar_convert_txt_to_array(filename_):
    file_time_str = filename_[-25:-6]
    time_stamp_seconds = time_str_to_seconds(file_time_str, '%Y-%m-%d_%H-%M-%S')

    # read the data into an array
    data_array_raw = genfromtxt(filename_,dtype=float, delimiter='\t',skip_header=133)

    # only keep one altitude column
    data_array_out = np.zeros((data_array_raw.shape[0], 7), dtype=float)
    data_array_out[:,0] = data_array_raw[:,0]
    data_array_out[:,1] = data_array_raw[:,1]
    data_array_out[:,2] = data_array_raw[:,2]
    data_array_out[:,3] = data_array_raw[:,4]
    data_array_out[:,4] = data_array_raw[:,5]
    data_array_out[:,5] = data_array_raw[:,7]
    data_array_out[:,6] = data_array_raw[:,8]
    return time_stamp_seconds, data_array_out
def compile_AWAP_precip_datafiles(file_list):
    # load first file to get shape
    print('loading file: ', file_list[0])
    arr_1, start_date_sec_1 = load_AWAP_data(file_list[0])
    rows_ = arr_1.shape[0]
    columns_ = arr_1.shape[1]

    # create lat and lon series
    series_lat = np.arange(-44.5, -9.95, 0.05)[::-1]
    series_lon = np.arange(112, 156.29, 0.05)

    # create time array
    output_array_time = np.zeros(len(file_list), dtype=float)

    # create output array
    output_array = np.zeros((len(file_list), rows_, columns_), dtype=float)

    # load first array data into output array
    output_array[0,:,:] = arr_1
    output_array_time[0] = start_date_sec_1

    # loop thru remainning files to populate ouput_array
    for t_, filename_ in enumerate(file_list[1:]):
        print('loading file: ', filename_)
        arr_t, start_date_sec_t = load_AWAP_data(filename_)
        output_array[t_+1, :, :] = arr_t
        output_array_time[t_+1] = start_date_sec_t

    return output_array, output_array_time, series_lat, series_lon
def load_AWAP_data(filename_):
    start_date_str = filename_.replace('\\','/').split('/')[-1][:8]
    # stop_date_str = filename_.replace('\\','/').split('/')[-1][8:16]
    start_date_sec = time_str_to_seconds(start_date_str, '%Y%m%d')

    arr_precip = np.genfromtxt(filename_, float, skip_header=6, skip_footer=18)

    return arr_precip , start_date_sec
def get_means_from_filelist(file_list, lat_lon_ar):
    # lat_lon_points_list = [ 147.8,
    #                         149,
    #                         -36.8,
    #                         -35.4]

    # box domain indexes
    index_c = [716, 740]
    index_r = [508, 536]

    series_lat = np.arange(-44.5, -9.95, 0.05)[::-1]
    series_lon = np.arange(112,156.3,0.05)

    lat_index_list, lon_index_list = find_index_from_lat_lon(series_lat, series_lon, lat_lon_ar[:,1], lat_lon_ar[:,0])


    time_secs_list = []

    precip_array = np.zeros((277,9),dtype=float)


    for r_, filename_ in enumerate(file_list):
        print('loading file: ', filename_)
        arr_precip, start_date_sec = load_AWAP_data(filename_)
        time_secs_list.append(start_date_sec)

        precip_array[r_, 0] = start_date_sec
        precip_array[r_, 1] = np.mean(arr_precip[index_r[0]:index_r[1]+1, index_c[0]:index_c[1]+1])

        for i_ in range(2,9):
            precip_array[r_, i_] = arr_precip[lat_index_list[i_-2],lon_index_list[i_-2]]

    save_array_to_disk(['box mean precip [mm]','1 precip [mm]','2 precip [mm]','3 precip [mm]',
                        '4 precip [mm]','5 precip [mm]','6 precip [mm]','7 precip [mm]'],
                       precip_array[:,0], precip_array[:,1:], 'C:/_output/test_fimi_2.csv')
    # save_HVF(['box','1','2','3','4','5','6','7'], precip_array, 'C:/_output/test_fimi_1.csv')

    print("done")

    return precip_array
def compile_BASTA_days_and_save_figure(directory_where_nc_file_are):
    # compile BASTA data per day and save plot (per day)

    time_format_basta = 'seconds since %Y-%m-%d %H:%M:%S'

    # directory_where_nc_file_are = '/home/luis/Data/BASTA/L0/12m5/'
    path_input = directory_where_nc_file_are

    file_label = path_input.split('/')[-4] + '_' + path_input.split('/')[-3] + '_' + path_input.split('/')[-2] + '_'

    file_list_all = sorted(glob.glob(str(path_input + '/*.nc')))

    first_day_str = file_list_all[0][-18:-10]
    last_day_str = file_list_all[-1][-18:-10]

    first_day_int = time_seconds_to_days(time_str_to_seconds(first_day_str,'%Y%m%d'))
    last_day_int = time_seconds_to_days(time_str_to_seconds(last_day_str,'%Y%m%d'))

    total_number_of_days = last_day_int - first_day_int

    print('The data in the folder encompasses', total_number_of_days, 'days')

    days_list_int = np.arange(first_day_int, last_day_int + 1)
    days_list_str = time_seconds_to_str(time_days_to_seconds(days_list_int),'%Y%m%d')

    for day_str in days_list_str:

        print('-|' * 20)
        file_list_day = sorted(glob.glob(str(path_input + file_label + day_str + '*.nc')))

        print('Compiling day',  day_str, len(file_list_day), 'files found for this day.')


        if len(file_list_day) > 0:

            filename_ = file_list_day[0]

            print('loading file:', filename_)

            netcdf_file_object = nc.Dataset(filename_, 'r')

            # variable_names = sorted(netcdf_file_object.variables.keys())

            time_raw = netcdf_file_object.variables['time'][:].copy()
            file_first_time_stamp = time_str_to_seconds(netcdf_file_object.variables['time'].units,
                                                        time_format_basta)

            compiled_time_days = time_seconds_to_days(np.array(time_raw, dtype=int) + file_first_time_stamp)
            compiled_raw_reflectivity_array = netcdf_file_object.variables['raw_reflectivity'][:].copy()
            compiled_range_array = netcdf_file_object.variables['range'][:].copy()

            netcdf_file_object.close()

            if len(file_list_day) > 1:
                for filename_ in file_list_day[1:]:

                    print('loading file:', filename_)

                    netcdf_file_object = nc.Dataset(filename_, 'r')


                    time_raw = netcdf_file_object.variables['time'][:].copy()

                    file_first_time_stamp = time_str_to_seconds(netcdf_file_object.variables['time'].units,
                                                                time_format_basta)

                    time_days = time_seconds_to_days(np.array(time_raw, dtype = int) + file_first_time_stamp)
                    compiled_time_days = np.append(compiled_time_days, time_days)
                    raw_reflectivity_array = netcdf_file_object.variables['raw_reflectivity'][:].copy()
                    compiled_raw_reflectivity_array = np.vstack((compiled_raw_reflectivity_array,
                                                                 raw_reflectivity_array))

                    netcdf_file_object.close()

            figure_output_name = path_input + file_label + day_str + '.png'
            print('saving figure to:', figure_output_name)
            p_arr_vectorized_2(compiled_raw_reflectivity_array, compiled_time_days, compiled_range_array/1000,
                               cmap_=default_cm, figsize_=(12, 8), vmin_=80, vmax_=140,
                               cbar_label='Raw Reflectivity dB', x_header='UTC',y_header='Range AGL [km]',
                               figure_filename=figure_output_name,
                               time_format_ = '%H')
def compile_BASTA_into_one_file(directory_where_nc_file_are):
    # compile BASTA data into one netcdf file

    time_format_basta = 'seconds since %Y-%m-%d %H:%M:%S'

    # directory_where_nc_file_are = '/home/luis/Data/BASTA/L0/12m5/'
    path_input = directory_where_nc_file_are

    file_list_all = sorted(glob.glob(str(path_input + '/*.nc')))

    # first_day_str = file_list_all[0][-18:-10]
    # last_day_str = file_list_all[-1][-18:-10]

    # first_day_int = time_seconds_to_days(time_str_to_seconds(first_day_str,'%Y%m%d'))
    # last_day_int = time_seconds_to_days(time_str_to_seconds(last_day_str,'%Y%m%d'))

    # days_list_int = np.arange(first_day_int, last_day_int + 1)

    # create copy of first file
    netcdf_file_object = nc.Dataset(file_list_all[-1], 'r')
    last_second_raw = netcdf_file_object.variables['time'][:][-1]
    file_first_time_stamp = time_str_to_seconds(netcdf_file_object.variables['time'].units,
                                                time_format_basta)
    netcdf_file_object.close()
    last_second_epoc = last_second_raw + file_first_time_stamp
    last_time_str = time_seconds_to_str(last_second_epoc, '%Y%m%d_%H%M%S')
    output_filename = file_list_all[0][:-3] + '_' + last_time_str + '.nc'
    shutil.copyfile(file_list_all[0], output_filename)
    print('Created output file with name:', output_filename)


    # open output file for appending data
    netcdf_output_file_object = nc.Dataset(output_filename, 'a')
    file_first_time_stamp_seconds_epoc = time_str_to_seconds(netcdf_output_file_object.variables['time'].units,
                                                             time_format_basta)

    variable_names = sorted(netcdf_output_file_object.variables.keys())
    # create references to variables in output file
    variable_objects_dict = {}
    for var_name in variable_names:
        variable_objects_dict[var_name] = netcdf_output_file_object.variables[var_name]


    for filename_ in file_list_all[1:]:

        print('-' * 5)
        print('loading file:', filename_)

        # open file
        netcdf_file_object = nc.Dataset(filename_, 'r')
        # create file's time series
        file_time_stamp_seconds_epoc = time_str_to_seconds(netcdf_file_object.variables['time'].units,
                                                                 time_format_basta)
        time_raw = netcdf_file_object.variables['time'][:].copy()
        time_seconds_epoc = np.array(time_raw, dtype=int) + file_time_stamp_seconds_epoc

        row_start = variable_objects_dict['time'].shape[0]
        row_end = time_raw.shape[0] + row_start

        # append time array
        variable_objects_dict['time'][row_start:row_end] = time_seconds_epoc - file_first_time_stamp_seconds_epoc
        # append raw_reflectivity array
        variable_objects_dict['raw_reflectivity'][row_start:row_end] = \
            netcdf_file_object.variables['raw_reflectivity'][:].copy()
        # append raw_velocity array
        variable_objects_dict['raw_velocity'][row_start:row_end] = \
            netcdf_file_object.variables['raw_velocity'][:].copy()



        # append all other variables that only time dependent
        for var_name in variable_names:
            if var_name != 'time' and var_name != 'range' and \
                    var_name != 'raw_reflectivity' and var_name != 'raw_velocity':
                if len(netcdf_file_object.variables[var_name].shape) == 1:
                    variable_objects_dict[var_name][row_start:row_end] = \
                        netcdf_file_object.variables[var_name][:].copy()


        netcdf_file_object.close()

    netcdf_output_file_object.close()

    print('done')
def load_BASTA_data_from_netcdf_to_arrays(filename_):
    # load BASTA data from netcdf to arrays

    # path_input = '/home/luis/Data/BASTA/L0/'
    # filename_ = path_input + 'BASTA_L0_12m5_20180606_071716_20180806_025422.nc'
    time_format_basta = 'seconds since %Y-%m-%d %H:%M:%S'

    # open file
    netcdf_file_object = nc.Dataset(filename_, 'r')

    # load time as seconds and days
    file_time_stamp_seconds_epoc = time_str_to_seconds(netcdf_file_object.variables['time'].units, time_format_basta)
    time_raw = netcdf_file_object.variables['time'][:].copy()
    time_seconds_epoc = np.array(time_raw, dtype=int) + file_time_stamp_seconds_epoc
    time_days_epoc = time_seconds_to_days(time_seconds_epoc)

    # append range array
    array_range = netcdf_file_object.variables['range'][:].copy()
    # append raw_reflectivity array
    array_raw_reflectivity = netcdf_file_object.variables['raw_reflectivity']#[:].copy()
    # append raw_velocity array
    array_raw_velocity = netcdf_file_object.variables['raw_velocity']#[:].copy()


    # close file
    # netcdf_file_object.close()

    return array_raw_reflectivity, array_raw_velocity, array_range, time_seconds_epoc, time_days_epoc
def BASTA_load_period_to_dict(start_time_YMDHM, stop_time_YMDHM, folder_path,
                                variable_names=('time', 'range', 'raw_reflectivity', 'raw_velocity')):
    time_format_basta = 'seconds since %Y-%m-%d %H:%M:%S'

    out_dict = {}
    temp_dict = {}
    variables_with_time_dimension = []

    if not 'time' in variable_names:
        variable_names_temp_list = ['time']
        for variable_name in variable_names:
            variable_names_temp_list.append(variable_name)
        variable_names = variable_names_temp_list

    # data_folder
    data_folder = folder_path

    # get all data files filenames
    file_list = sorted(glob.glob(str(data_folder + '/*.nc')))
    file_times_tuple_list = []
    file_times_tuple_list_str = []
    for i_, filename_ in enumerate(file_list):
        file_time_str_start = filename_.split('_')[-2] + filename_.split('_')[-1].split('.')[0]
        file_time_sec_start = time_str_to_seconds(file_time_str_start, '%Y%m%d%H%M%S')
        if i_ < len(file_list) -1:
            file_time_str_stop = file_list[i_+1].split('_')[-2] + file_list[i_+1].split('_')[-1].split('.')[0]
            file_time_sec_stop = time_str_to_seconds(file_time_str_stop, '%Y%m%d%H%M%S')
        else:
            file_time_sec_stop = file_time_sec_start + (24*60*60)
        file_times_tuple_list.append(tuple((file_time_sec_start, file_time_sec_stop)))
        file_times_tuple_list_str.append(tuple((file_time_str_start, time_seconds_to_str(file_time_sec_stop,
                                                                                         '%Y%m%d%H%M%S'))))

    # select only files inside time range
    event_start_sec = time_str_to_seconds(start_time_YMDHM, '%Y%m%d%H%M')
    event_stop_sec = time_str_to_seconds(stop_time_YMDHM, '%Y%m%d%H%M')
    selected_file_list = []
    for file_index in range(len(file_list)):
        if event_start_sec <= file_times_tuple_list[file_index][0] <= event_stop_sec:
            selected_file_list.append(file_list[file_index])
        elif event_start_sec <= file_times_tuple_list[file_index][1] <= event_stop_sec:
            selected_file_list.append(file_list[file_index])
        elif file_times_tuple_list[file_index][0] <= event_start_sec <= file_times_tuple_list[file_index][1]:
            selected_file_list.append(file_list[file_index])
        elif file_times_tuple_list[file_index][0] <= event_stop_sec <= file_times_tuple_list[file_index][1]:
            selected_file_list.append(file_list[file_index])
    print('found files:')
    p_(selected_file_list)

    # load data
    if len(selected_file_list) == 0:
        print('No files inside time range!')
        return out_dict
    else:
        cnt = 0
        for filename_ in selected_file_list:
            if cnt == 0:
                nc_file = nc.Dataset(filename_, 'r')
                print('reading file:',filename_)
                for variable_name in variable_names:
                    if 'time' in nc_file.variables[variable_name].dimensions:
                        variables_with_time_dimension.append(variable_name)
                    if variable_name == 'time':
                        file_time_stamp_seconds_epoc = time_str_to_seconds(nc_file.variables['time'].units,
                                                                           time_format_basta)
                        time_raw = nc_file.variables['time'][:].copy()
                        time_seconds_epoc = np.array(time_raw, dtype=int) + file_time_stamp_seconds_epoc
                        temp_dict[variable_name] = time_seconds_epoc
                    else:
                        temp_dict[variable_name] = nc_file.variables[variable_name][:].filled(np.nan)
                nc_file.close()
                cnt += 1
            else:
                nc_file = nc.Dataset(filename_, 'r')
                print('reading file:', filename_)
                for variable_name in variable_names:
                    if 'time' in nc_file.variables[variable_name].dimensions:
                        variables_with_time_dimension.append(variable_name)
                        if len(nc_file.variables[variable_name].shape) == 1:

                            if variable_name == 'time':
                                file_time_stamp_seconds_epoc = time_str_to_seconds(nc_file.variables['time'].units,
                                                                                   time_format_basta)
                                time_raw = nc_file.variables['time'][:].copy()
                                time_seconds_epoc = np.array(time_raw, dtype=int) + file_time_stamp_seconds_epoc
                                temp_dict[variable_name] = np.hstack((temp_dict[variable_name], time_seconds_epoc))
                            else:
                                temp_dict[variable_name] = np.hstack((temp_dict[variable_name],
                                                                      nc_file.variables[variable_name][:].filled(np.nan)))
                        else:
                            temp_dict[variable_name] = np.vstack((temp_dict[variable_name],
                                                                  nc_file.variables[variable_name][:].filled(np.nan)))
                nc_file.close()

    # find row for start and end of event
    start_row = np.argmin(np.abs(temp_dict['time'] - event_start_sec))
    end_row = np.argmin(np.abs(temp_dict['time'] - event_stop_sec))

    for variable_name in variable_names:
        if variable_name in variables_with_time_dimension:
            out_dict[variable_name] = temp_dict[variable_name][start_row:end_row]
        else:
            out_dict[variable_name] = temp_dict[variable_name]

    return out_dict
def download_MSLP(datetime_start_str_YYYYmmDD, datetime_end_str_YYYYmmDD, path_output='C:/_output/'):

    # url_prefix_ir = 'http://www.bom.gov.au/archive/charts/2018/08/IDX0102.201808050600.gif'
    url_prefix_ir = 'http://www.bom.gov.au/archive/charts/'

    # create date strings list
    datetime_start_sec = time_str_to_seconds(datetime_start_str_YYYYmmDD, '%Y%m%d')
    datetime_end_sec = time_str_to_seconds(datetime_end_str_YYYYmmDD, '%Y%m%d')
    time_steps_in_sec = 60 * 60 * 6
    number_of_images = (datetime_end_sec - datetime_start_sec) / time_steps_in_sec
    datetime_list_str = []
    year_str_list = []
    month_str_list = []
    for time_stamp_index in range(int(number_of_images)):
        year_str_list.append(time_seconds_to_str(datetime_start_sec + (time_stamp_index * time_steps_in_sec),
                                                     '%Y'))
        month_str_list.append(time_seconds_to_str(datetime_start_sec + (time_stamp_index * time_steps_in_sec),
                                                     '%m'))
        datetime_list_str.append(time_seconds_to_str(datetime_start_sec + (time_stamp_index * time_steps_in_sec),
                                                     '%Y%m%d%H%M'))

    # create url list
    url_list = []

    for time_stamp_index in range(int(number_of_images)):
        url_list.append(url_prefix_ir +
                        year_str_list[time_stamp_index] + '/' +
                        month_str_list[time_stamp_index] + '/IDX0102.' +
                        datetime_list_str[time_stamp_index] + '.gif')


    # download image list
    img_list = []
    datetime_downloaded_list = []
    datetime_not_downloaded_list = []
    for time_stamp_index in range(int(number_of_images)):
        try:
            img_list.append(np.array(PIL_Image.open(BytesIO(requests.get(url_list[time_stamp_index],
                                                                         timeout = 5).content)).convert('RGB')))
            datetime_downloaded_list.append(datetime_list_str[time_stamp_index])

            img_arr = PIL_Image.fromarray(img_list[-1])
            img_arr.save(path_output  + 'MSLP_' + datetime_list_str[time_stamp_index] + '.png')
            print(datetime_list_str[time_stamp_index], 'downloaded')

        except:
            print(datetime_list_str[time_stamp_index], 'failed')
            datetime_not_downloaded_list.append(datetime_list_str[time_stamp_index])
    return datetime_downloaded_list, datetime_not_downloaded_list
def download_MSLP_single(datetime_str_YYYYmmDDHHMM, path_output='C:/_output/', output_image_obj=False, save_=True):

    # url_prefix_ir = 'http://www.bom.gov.au/archive/charts/2018/08/IDX0102.201808050600.gif'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36',
               }


    url_prefix_ir = 'http://www.bom.gov.au/archive/charts/'

    MSLP_url = (url_prefix_ir + datetime_str_YYYYmmDDHHMM[:4] + '/' + datetime_str_YYYYmmDDHHMM[4:6] +
                '/IDX0102.' +
                datetime_str_YYYYmmDDHHMM + '.gif')

    # download image list
    try:

        img_ = PIL_Image.open(BytesIO(requests.get(MSLP_url, timeout=5, headers=headers).content)).convert('RGB')
        if save_: img_.save(path_output  + 'MSLP_' + datetime_str_YYYYmmDDHHMM + '.png')
        print(datetime_str_YYYYmmDDHHMM, 'downloaded')

    except:
        print(datetime_str_YYYYmmDDHHMM, 'failed')

    if output_image_obj:
        return img_



# MRR
def MRR_read_MRR2_ave_to_array(filename_):
    # read lines into output lists
    mrr_time_str_list = []
    Z_list = []
    W_list = []
    range_not_loaded = True

    # read MRR file
    mrr_file = open(filename_, mode='r')
    for line_str in mrr_file:
        if line_str[:3] == 'MRR':
            mrr_time_str_list.append(line_str[4:16])  # %d.%m.%Y_%H:%M:%S
        if range_not_loaded:
            if line_str[0] == 'H':
                range_list = line_str[2:].split()
                range_not_loaded = False
        if line_str[0] == 'Z':
            Z_list.append(split_str_chunks(line_str[3:], 7))
        if line_str[0] == 'W':
            W_list.append(split_str_chunks(line_str[3:], 7))
    mrr_file.close()

    # create arrays
    MRR_time = time_str_to_seconds(mrr_time_str_list, '%y%m%d%H%M%S')
    range_ = np.array(range_list, dtype=float)
    Z_ = np.zeros((len(Z_list), len(Z_list[0]) - 1), dtype=float)
    W_ = np.zeros((len(Z_list), len(Z_list[0]) - 1), dtype=float)
    Z_[:, :] = np.nan
    W_[:, :] = np.nan
    for r_ in range(len(MRR_time)):
        for c_ in range(len(range_list)):
            try:
                Z_[r_, c_] = Z_list[r_][c_]
                W_[r_, c_] = W_list[r_][c_]
            except:
                pass

    return MRR_time, range_, Z_, W_
def MRR_pro_to_raw(MRR_pro_nc_filename, output_filename):
    """
    reformat MRR-Pro NC to MRR-2 raw text format
    :param MRR_pro_nc_filename: file to be read and reformmated to old format
    :param output_filename: should include path and extension
    :return: output filename and size
    """
    # open input file and copy non variable series
    file_CM = nc.Dataset(MRR_pro_nc_filename)
    time_raw = np.array(file_CM.variables['time'][:].data)
    H_raw = np.array(file_CM.variables['range'][:].data)
    TF_raw = np.array(file_CM.variables['transfer_function'][:].data)
    calibration_constant = int(file_CM.variables['calibration_constant'][:].data)

    # create output file
    filename_ = output_filename
    output_text_file = open(filename_, 'w')

    time_stamp_str_list = time_seconds_to_str(time_raw, '%y%m%d%H%M%S')
    H_raw_avr = row_average_discrete_1D(H_raw,4)
    H_raw_avr_line = 'H  '
    for h_ in H_raw_avr:
        H_raw_avr_line += ' ' + str(int(h_)).rjust(8)
    H_raw_avr_line += '\n'
    TF_raw_avr = row_average_discrete_1D(TF_raw,4)
    TF_raw_avr_line = 'TF '
    for tf_ in TF_raw_avr:
        TF_raw_avr_line += ' ' + str(round(tf_,6)).rjust(8)
    TF_raw_avr_line += '\n'

    for t_ in range(time_raw.shape[0]):
        p_progress(t_, time_raw.shape[0])
        output_text_file.write('MRR ' + time_stamp_str_list[t_] +
                               ' UTC DVS 6.10 DSN 0510126919 BW 39050 CC ' +
                               str(calibration_constant) +
                               ' MDQ 100 58 58 TYP RAW\n')
        output_text_file.write(H_raw_avr_line)
        output_text_file.write(TF_raw_avr_line)

        stamp_spectrum = np.array(file_CM.variables['spectrum_reflectivity'][t_,:,::-1].data)

        for f_ in range(64):
            output_text_file.write('F' + str(f_).zfill(2))

            for fs_ in row_average_discrete_1D(stamp_spectrum[:,f_],4):
                output_text_file.write(' ' + str(int(fs_)).rjust(8))
            output_text_file.write('\n')

    output_text_file.close()
    print(filename_, int(os.stat(filename_).st_size / 1024), 'MB')
def MRR_quicklook(ncFile, imgFile, imgTitle):
    """
    Makes Quicklooks of MRR data


    @parameter site (str): code for the site where the data was recorded (usually 3 letter)
    @parameter ncFile (str): netcdf file name incl. path, usually "path/mrr_site_yyyymmdd.nc"
    @parameter imgFile (str): image file name, incl. path, extensions determines file format (e.g. png, eps, pdf ...)
    @parameter imgTitle (str): plot title
    """
    print("##### " + imgTitle + "######")

    if isinstance(ncFile, str):
        ncData = nc.Dataset(ncFile, 'r')

        timestampsNew = ncData.variables["time"][:]
        HNew = ncData.variables["height"][:]
        ZeNew = ncData.variables["Ze"][:]
        noiseAveNew = ncData.variables["etaNoiseAve"][:]
        spectralWidthNew = ncData.variables["spectralWidth"][:]
        WNew = ncData.variables["W"][:]
        qualityNew = ncData.variables["quality"][:]

        ncData.close()
    else:
        timestampsNew = ncFile.time
        HNew = ncFile.H
        ZeNew = ncFile.Ze
        noiseAveNew = ncFile.etaNoiseAve
        spectralWidthNew = ncFile.specWidth
        WNew = ncFile.W
        qualityNew, qualDescription = IMProToo_mod.MrrZe.getQualityBinArray(ncFile, ncFile.qual)

    date = datetime.utcfromtimestamp(timestampsNew[0]).strftime("%Y%m%d")
    starttime = calendar.timegm(
        datetime(year=int(date[0:4]), month=int(date[4:6]), day=int(date[6:8]), hour=0,
                          minute=0, second=0).timetuple())
    endtime = starttime + 60 * 60 * 24

    HNew[np.isnan(HNew)] = -9999
    timestampsNew = IMProToo_mod.oneD2twoD(timestampsNew, ZeNew.shape[1], 1)

    fig = plt.figure(figsize=(10, 13))

    sp1 = fig.add_subplot(511)
    sp1.set_title(imgTitle)
    levels = np.arange(-15, 40, 0.1)
    plotCF = sp1.contourf(timestampsNew, HNew, ZeNew, levels, cmap=plt.get_cmap("Spectral"), extend="both")  #
    cbZe = plt.colorbar(plotCF)
    cbZe.set_label('MRR Ze [dBz]')
    sp1.set_ylim(np.min(HNew[HNew != -9999]), np.max(HNew))
    sp1.set_xlim(starttime, endtime)

    sp1.axhline(HNew[-1, 2])
    sp1.axhline(HNew[-1, 29])

    sp2 = fig.add_subplot(512)
    levels = np.arange(-10, 18, 0.1)
    plotCF = sp2.contourf(timestampsNew, HNew, WNew, levels, cmap=plt.get_cmap("Spectral"), extend="both")  #
    cbZe = plt.colorbar(plotCF)
    cbZe.set_label('MRR W [m/s]')
    sp2.set_ylim(np.min(HNew[HNew != -9999]), np.max(HNew))
    sp2.set_xlim(starttime, endtime)

    sp2.axhline(HNew[-1, 2])
    sp2.axhline(HNew[-1, 29])

    sp3 = fig.add_subplot(513)
    levels = np.arange(0, 1.5, 0.1)
    plotCF = sp3.contourf(timestampsNew, HNew, spectralWidthNew, levels, cmap=plt.get_cmap("Spectral"),
                          extend="both")  #
    cbZe = plt.colorbar(plotCF)
    cbZe.set_label('spectralWidth [m/s]')
    sp3.set_ylim(np.min(HNew[HNew != -9999]), np.max(HNew))
    sp3.set_xlim(starttime, endtime)

    sp3.axhline(HNew[-1, 2])
    sp3.axhline(HNew[-1, 29])

    sp4 = fig.add_subplot(514)
    levels = np.arange(1e-10, 1e-8, 2e-10)
    plotCF = sp4.contourf(timestampsNew, HNew, noiseAveNew, levels, cmap=plt.get_cmap("Spectral"), extend="both")  #
    cbZe = plt.colorbar(plotCF)
    cbZe.set_label('mean spectral noise [1/m]')
    sp4.set_ylim(np.min(HNew[HNew != -9999]), np.max(HNew))
    sp4.set_xlim(starttime, endtime)
    sp4.axhline(HNew[-1, 2])
    sp4.axhline(HNew[-1, 29])
    # import pdb;pdb.set_trace()

    sp5 = fig.add_subplot(515)
    levels = np.arange(20)
    for i in levels:
        levels[i] = 2 ** i
    plotCF = sp5.contourf(timestampsNew, HNew, qualityNew, levels, cmap=plt.get_cmap("Spectral"),
                          norm=matplotlib.colors.LogNorm())  #
    cbZe = plt.colorbar(plotCF)
    cbZe.set_label('quality array')
    sp5.set_ylim(np.min(HNew[HNew != -9999]), np.max(HNew))
    sp5.set_xlim(starttime, endtime)
    sp5.axhline(HNew[-1, 2])
    sp5.axhline(HNew[-1, 29])

    # sp1.set_xlim(np.min(timestampsNew),np.max(timestampsNew))
    sp1.set_xticks(np.arange(sp1.get_xlim()[0], sp1.get_xlim()[1], 7200))
    sp1.set_xticklabels([])

    # sp2.set_xlim(np.min(timestampsNew),np.max(timestampsNew))
    sp2.set_xticks(np.arange(sp1.get_xlim()[0], sp1.get_xlim()[1], 7200))
    sp2.set_xticklabels([])

    # sp3.set_xlim(np.min(timestampsNew),np.max(timestampsNew))
    sp3.set_xticks(np.arange(sp1.get_xlim()[0], sp1.get_xlim()[1], 7200))
    sp3.set_xticklabels([])

    # sp4.set_xlim(np.min(timestampsNew),np.max(timestampsNew))
    sp4.set_xticks(np.arange(sp1.get_xlim()[0], sp1.get_xlim()[1], 7200))
    sp4.set_xticklabels([])

    # pdb.set_trace()
    # sp5.set_xlim(np.min(timestampsNew)-60,np.max(timestampsNew))
    sp5.set_xticks(np.arange(sp5.get_xlim()[0], sp5.get_xlim()[1] + 7200, 7200))
    niceDates = list()
    for timestamp in np.arange(sp5.get_xlim()[0], sp5.get_xlim()[1] + 7200, 7200):
        niceDates.append(str(datetime.utcfromtimestamp(timestamp).strftime("%H:%M")))
    sp5.set_xticklabels(niceDates)

    plt.subplots_adjust(hspace=0.02, left=0.085, right=0.78)

    plt.savefig(imgFile)
    print(imgFile)

    plt.close()
    return
def MRR_rawdata_to_netcdf(arg_list):
    filename_, output_filename_without_extension, quicklook_ = arg_list
    try:
        rawData = IMProToo_mod.mrrRawData(filename_)
        processedSpec = IMProToo_mod.MrrZe(rawData)

        processedSpec.averageSpectra(60)
        processedSpec.rawToSnow()
        processedSpec.writeNetCDF(output_filename_without_extension + '.nc')

        title_ = output_filename_without_extension.replace('\\','/').split('/')[-1]
        if quicklook_:
            MRR_quicklook(processedSpec, output_filename_without_extension + '.png', title_)
        return 0
    except:
        return filename_
def compile_MRR_hourly_nc_into_one_nc(directory_where_nc_file_are, output_path=''):
    # compile MRR_Pro data into one netcdf file per day

    time_format_MRR_Pro = 'seconds since %Y-%m-%dT%H:%M:%SZ'

    path_input = directory_where_nc_file_are

    file_list_all = sorted(glob.glob(str(path_input + '*.nc')))

    # create copy of first file
    netcdf_file_object = nc.Dataset(file_list_all[-1], 'r')
    last_second_raw = netcdf_file_object.variables['time'][:][-1]
    file_first_time_stamp = time_str_to_seconds(netcdf_file_object.variables['time'].units,
                                                time_format_MRR_Pro)
    netcdf_file_object.close()
    last_second_epoc = last_second_raw + file_first_time_stamp
    last_time_str = time_seconds_to_str(last_second_epoc, '%Y%m%d_%H%M%S')
    if output_path == '':
        output_filename = file_list_all[0][:-3] + '_' + last_time_str + '.nc'
    else:
        output_filename = output_path + file_list_all[0].replace('\\','/').split('/')[-1][:-3]+ '_' + last_time_str + '.nc'
    shutil.copyfile(file_list_all[0], output_filename)
    print('Created output file with name:', output_filename)


    # open output file for appending data
    netcdf_output_file_object = nc.Dataset(output_filename, 'a')

    vars_list = sorted(netcdf_output_file_object.variables)

    for filename_ in file_list_all[1:]:

        print('-' * 5)
        print('loading file:', filename_)

        # open hourly file
        netcdf_file_object = nc.Dataset(filename_, 'r')
        # get time array
        time_hourly = np.array(netcdf_file_object.variables['time'][:], dtype=float)

        row_start = netcdf_output_file_object.variables['time'].shape[0]
        row_end = time_hourly.shape[0] + row_start

        # append time array
        netcdf_output_file_object.variables['time'][row_start:row_end] = time_hourly

        # append all other variables that only time dependent
        for var_name in vars_list:
            if var_name != 'time':
                if 'time' in netcdf_output_file_object.variables[var_name].dimensions:
                    netcdf_output_file_object.variables[var_name][row_start:row_end] = \
                        netcdf_file_object.variables[var_name][:].copy()

        netcdf_file_object.close()

    netcdf_output_file_object.close()

    print('done')
def compile_MRR_PRO_and_process_daily(arg_list):
    day_directory, output_path, site_str = arg_list
    try:

        day_str = day_directory.replace('\\','/').split('/')[-2]
        error_file_list = []
        file_list = sorted(glob.glob(str(day_directory + day_str + '_??????.nc')))

        # open and compile
        out_object = Object_create()

        files_read = 0
        rh_array_temp = np.zeros(1)
        tf_array_temp = np.zeros(1)
        for filename_ in file_list:
            if files_read == 0:
                try:
                    file_nc = nc.Dataset(filename_, 'r')
                    out_object.mrrRawTime = file_nc.variables['time'][:]
                    out_object.mrrRawSpectrum = file_nc.variables['spectrum_reflectivity'][:, :, :]
                    out_object.header = file_nc.getncattr('instrument_name')
                    out_object.missingNumber = -9999
                    out_object.mrrRawCC = int(file_nc.variables['calibration_constant'][0])
                    rh_array_temp = row_average_discrete_1D(file_nc.variables['range'][:],4)
                    tf_array_temp = np.array(file_nc.variables['transfer_function'][:])

                    file_nc.close()
                    files_read = 1
                except:
                    error_file_list.append(filename_)
            else:
                try:
                    file_nc = nc.Dataset(filename_, 'r')
                    out_object.mrrRawTime = np.hstack((out_object.mrrRawTime, file_nc.variables['time'][:]))
                    out_object.mrrRawSpectrum = np.vstack((out_object.mrrRawSpectrum,
                                                       file_nc.variables['spectrum_reflectivity'][:, :, :]))
                    file_nc.close()
                except:
                    error_file_list.append(filename_)


        # average by height
        out_object.mrrRawSpectrum = column_average_discrete_3D(out_object.mrrRawSpectrum, 4)
        out_object.shape3D = out_object.mrrRawSpectrum.shape
        out_object.shape2D = out_object.mrrRawSpectrum.shape[:2]

        rh_array = np.zeros((out_object.shape3D[0], out_object.shape3D[1]))
        for t_ in range(out_object.shape3D[0]):
            rh_array[t_, :] = rh_array_temp
        out_object.mrrRawHeight = rh_array

        tf_array = np.zeros((out_object.shape3D[0], tf_array_temp.shape[0]))
        for t_ in range(out_object.shape3D[0]):
            tf_array[t_, :] = tf_array_temp
            out_object.mrrRawTF = tf_array

        out_object.mrrRawNoSpec = np.ones(out_object.shape3D[0]) * 58


        processedSpec_ = IMProToo_mod.MrrZe(out_object)

        processedSpec_.averageSpectra(60)
        processedSpec_.rawToSnow()



        processedSpec_.writeNetCDF(output_path + site_str + '_' + day_str + '.nc')

        return error_file_list
    except:
        return day_directory
def compile_MRR_PRO_daily(arg_list):
    day_directory, output_path, site_str = arg_list
    try:

        day_str = day_directory.replace('\\','/').split('/')[-2]
        error_file_list = []
        file_list = sorted(glob.glob(str(day_directory + day_str + '_??????.nc')))

        # open and compile
        out_object = Object_create()

        files_read = 0
        rh_array_temp = np.zeros(1)
        for filename_ in file_list:
            if files_read == 0:
                try:
                    file_nc = nc.Dataset(filename_, 'r')
                    out_object.time = file_nc.variables['time'][:]
                    out_object.Ze = file_nc.variables['Ze'][:]
                    out_object.W = file_nc.variables['WIDTH'][:]
                    rh_array_temp = file_nc.variables['range'][:]

                    file_nc.close()
                    files_read = 1
                except:
                    error_file_list.append(filename_)
            else:
                try:
                    file_nc = nc.Dataset(filename_, 'r')
                    out_object.time = np.hstack((out_object.time, file_nc.variables['time'][:]))
                    out_object.Ze = np.vstack((out_object.Ze, file_nc.variables['Ze'][:, :]))
                    out_object.W = np.vstack((out_object.W, file_nc.variables['WIDTH'][:, :]))
                    file_nc.close()
                except:
                    error_file_list.append(filename_)


        rh_array = np.zeros((out_object.time.shape[0], rh_array_temp.shape[0]))
        for t_ in range(out_object.time.shape[0]):
            rh_array[t_, :] = rh_array_temp
        out_object.range = rh_array

        # save file
        output_filename = output_path + site_str + '_' + day_str + '.nc'
        output_file = nc.Dataset(output_filename,'w')

        ##write meta data
        output_file.history = "Created by Luis Ackermann at " + datetime.now().strftime(
            "%Y/%m/%d %H:%M:%S")

        # make frequsnions
        output_file.createDimension('time', out_object.time.shape[0])
        output_file.createDimension('height', rh_array_temp.shape[0])

        ncShape2D = ("time", "height",)

        fillVDict = dict()
        # little cheat to avoid hundreds of if, else...
        fillVDict["fill_value"] = -9999

        nc_time = output_file.createVariable('time', 'i', ('time',), **fillVDict)
        nc_time.description = "measurement time. Following Meteks convention, the dataset at e.g. 11:55 contains all recorded raw between 11:54:00 and 11:54:59 (if delta t = 60s)!"
        nc_time.units = 'seconds since 1970-01-01'
        nc_time[:] = np.array(out_object.time, dtype="i4")
        # commented because of Ubuntu bug: https://bugs.launchpad.net/ubuntu/+source/python-scientific/+bug/1005571
        # if not pyNc: nc_time._FillValue =int(self.missingNumber)

        nc_height = output_file.createVariable('height', 'f', ncShape2D, **fillVDict)  # = missingNumber)
        nc_height.description = "height above instrument"
        nc_height.units = 'm'
        nc_height[:] = np.array(out_object.range, dtype="f4")
        # if not pyNc: nc_range._FillValue =int(self.missingNumber)

        nc_ze = output_file.createVariable('Ze', 'f', ncShape2D, **fillVDict)
        nc_ze.description = "reflectivity"
        nc_ze.units = "dBz"
        nc_ze[:] = np.array(out_object.Ze, dtype="f4")

        nc_ze = output_file.createVariable('W', 'f', ncShape2D, **fillVDict)
        nc_ze.description = "spectral width"
        nc_ze.units = "m/s"
        nc_ze[:] = np.array(out_object.W, dtype="f4")

        output_file.close()

        return error_file_list
    except:
        return day_directory
def MRR_PRO_process_IMProToo_2(filename_netcdf_MRR_Pro, output_filename=None,
                             time_interval_YmdHM_YmdHM='', return_=True):
    file_CM = nc.Dataset(filename_netcdf_MRR_Pro)

    MRR_CM_time = np.array(file_CM.variables['time'][:])

    # define start and end rows according to time_interval
    if time_interval_YmdHM_YmdHM == '':
        e1_1 = 0
        e1_2 = MRR_CM_time.shape[0]
    else:
        e1_1 = time_to_row_str(MRR_CM_time, time_interval_YmdHM_YmdHM.split('_')[0])
        e1_2 = time_to_row_str(MRR_CM_time, time_interval_YmdHM_YmdHM.split('_')[1])

    # add attributes
    file_CM_object = Object_create()
    file_CM_object.header                   = file_CM.instrument_name
    file_CM_object.missingNumber            = -9999
    file_CM_object.mrrRawCC                 = int(file_CM.variables['calibration_constant'][0])

    rh_array                                = np.zeros((file_CM.variables['time'][e1_1:e1_2].shape[0],
                                                        file_CM.variables['transfer_function'].shape[0]))
    rh_array                                = np.ma.array(rh_array, mask=np.zeros((rh_array.shape)))
    for t_ in range(file_CM.variables['time'][e1_1:e1_2].shape[0]):
        rh_array[t_,:] = file_CM.variables['range'][:]
    file_CM_object.mrrRawHeight             = rh_array
    file_CM_object.mrrRawNoSpec             = np.ones(file_CM.variables['time'][e1_1:e1_2].shape[0]) * 5.7
    mrrRawSpectrum_array                    = np.ma.array(
        np.e ** (np.array(file_CM.variables['spectrum_reflectivity'][e1_1:e1_2])[:,:,:]/10) ,
        mask=np.zeros((file_CM.variables['spectrum_reflectivity'][e1_1:e1_2].data.shape)))
    file_CM_object.mrrRawSpectrum           = mrrRawSpectrum_array

    tf_array                                = np.zeros((file_CM.variables['time'][e1_1:e1_2].shape[0],
                                                        file_CM.variables['transfer_function'].shape[0]))
    tf_array                                = np.ma.array(tf_array, mask=np.zeros((tf_array.shape)))
    for t_ in range(file_CM.variables['time'][e1_1:e1_2].shape[0]):
        tf_array[t_,:] = file_CM.variables['transfer_function'][:]
    file_CM_object.mrrRawTF                 = tf_array
    file_CM_object.mrrRawTime               = file_CM.variables['time'][e1_1:e1_2]
    file_CM_object.shape2D                  = tuple((file_CM.variables['time'][e1_1:e1_2].shape[0],
                                                    file_CM.variables['range'].shape[0]))
    file_CM_object.shape3D                  = file_CM.variables['spectrum_reflectivity'].shape

    processedSpec_CM = IMProToo_mod.MrrZe(file_CM_object)
    # processedSpec_CM.co["mrrFrequency"] = lamb_ # 24.15e9  24.23e9 #in Hz,]
    print('converted raw to mrrZe')
    processedSpec_CM.averageSpectra(60)
    print('averaged')
    processedSpec_CM.rawToSnow()
    print('calculated moments')
    if output_filename is not None:
        processedSpec_CM.writeNetCDF(output_filename)
        print('saved')

    if return_:
        return processedSpec_CM
def MRR_PRO_process_IMProToo_3(filename_netcdf_MRR_Pro, output_filename=None,
                             time_interval_YmdHM_YmdHM='', return_=True, var_list=None):
    file_CM = nc.Dataset(filename_netcdf_MRR_Pro)

    MRR_CM_time = np.array(file_CM.variables['time'][:])

    # define start and end rows according to time_interval
    e1_1 = 0
    e1_2 = MRR_CM_time.shape[0]

    # create mask
    mask_ = np.load('D:/Data/MRR_CM/MRR_PRO_spectra_mask_2.npy')
    mask_[mask_ == 1] = np.nan
    mask_[mask_ == 0] = 1
    mask_3D = np.zeros((file_CM.variables['spectrum_reflectivity'][e1_1:e1_2].data.shape), dtype=float)
    mask_3D[:] = mask_

    # mask spectra
    spectrum_reflectivity_array = np.array(file_CM.variables['spectrum_reflectivity'][e1_1:e1_2])
    spectrum_reflectivity_array_masked = spectrum_reflectivity_array * mask_3D

    # interpolate the interference in the spectrum
    for t_ in range(e1_2):
        p_progress(t_, e1_2, extra_text='spectrum interpolated')
        spectrum_reflectivity_array[t_, :, :] = \
            array_2d_fill_gaps_by_interpolation_linear(spectrum_reflectivity_array_masked[t_, :, :])

    # get constants
    range_array = file_CM.variables['range'][:].data
    delta_H = np.median(np.diff(range_array))
    calibration_constant = int(file_CM.variables['calibration_constant'][0])  # * .015)
    tranfer_function = file_CM.variables['transfer_function'][:].data

    # convert x to s
    s_array = np.array(10 ** (spectrum_reflectivity_array / 10), dtype=int)

    # add attributes
    file_CM_object = Object_create()
    file_CM_object.header = file_CM.instrument_name
    file_CM_object.missingNumber = -9999
    file_CM_object.mrrRawCC = calibration_constant

    rh_array = np.zeros((e1_2, tranfer_function.shape[0]))
    rh_array = np.ma.array(rh_array, mask=np.zeros(rh_array.shape))
    for t_ in range(e1_2):
        rh_array[t_, :] = range_array
    file_CM_object.mrrRawHeight = rh_array
    file_CM_object.mrrRawNoSpec = np.ones(e1_2) * 5.7
    mrrRawSpectrum_array = np.ma.array(s_array, mask=np.zeros(s_array.shape))
    file_CM_object.mrrRawSpectrum = mrrRawSpectrum_array

    tf_array = np.zeros((e1_2, tranfer_function.shape[0]))
    tf_array = np.ma.array(tf_array, mask=np.zeros((tf_array.shape)))
    for t_ in range(e1_2):
        tf_array[t_, :] = tranfer_function
    file_CM_object.mrrRawTF = tf_array
    file_CM_object.mrrRawTime = file_CM.variables['time'][e1_1:e1_2]
    file_CM_object.shape2D = tuple((e1_2, file_CM.variables['range'].shape[0]))
    file_CM_object.shape3D = file_CM.variables['spectrum_reflectivity'].shape

    processedSpec_CM = IMProToo_mod.MrrZe(file_CM_object)
    # processedSpec_CM.co["mrrFrequency"] = lamb_ # 24.15e9  24.23e9 #in Hz,]
    print('converted raw to mrrZe')
    processedSpec_CM.averageSpectra(60)
    print('averaged')
    processedSpec_CM.rawToSnow()
    print('calculated moments')
    if output_filename is not None:
        processedSpec_CM.writeNetCDF(output_filename, varsToSave=var_list)
        print('saved')

    if return_:
        return processedSpec_CM
def MRR_PRO_process_IMProToo_4(filename_netcdf_MRR_Pro, output_filename,
                               mask_filename='D:/Data/MRR_CM/MRR_PRO_spectra_mask_latest.npy'):
    file_CM = nc.Dataset(filename_netcdf_MRR_Pro)

    MRR_CM_time = np.array(file_CM.variables['time'][:])

    # define start and end rows according to time_interval
    e1_1 = 0
    e1_2 = MRR_CM_time.shape[0]

    # create mask
    mask_ = np.load(mask_filename)
    mask_[mask_ == 1] = np.nan
    mask_[mask_ == 0] = 1
    mask_3D = np.zeros((file_CM.variables['spectrum_reflectivity'][e1_1:e1_2].data.shape), dtype=float)
    mask_3D[:] = mask_

    # mask spectra
    spectrum_reflectivity_array = np.array(file_CM.variables['spectrum_reflectivity'][e1_1:e1_2])
    spectrum_reflectivity_array_masked = spectrum_reflectivity_array * mask_3D

    # interpolate the interference in the spectrum
    for t_ in range(e1_2):
        p_progress(t_, e1_2, extra_text='spectrum interpolated')
        spectrum_reflectivity_array[t_, :, :] = \
            array_2d_fill_gaps_by_interpolation_linear(spectrum_reflectivity_array_masked[t_, :, :])

    # get constants
    range_array = file_CM.variables['range'][:].data
    delta_H = np.median(np.diff(range_array))
    calibration_constant = int(file_CM.variables['calibration_constant'][0])  # * .015)
    tranfer_function = file_CM.variables['transfer_function'][:].data

    # convert x to s
    s_array = np.array(10 ** (spectrum_reflectivity_array / 10), dtype=int)


    # add attributes
    file_CM_object = Object_create()
    file_CM_object.header = file_CM.instrument_name
    file_CM_object.missingNumber = -9999
    file_CM_object.mrrRawCC = calibration_constant

    rh_array = np.zeros((e1_2, tranfer_function.shape[0]))
    rh_array = np.ma.array(rh_array, mask=np.zeros(rh_array.shape))
    for t_ in range(e1_2):
        rh_array[t_, :] = range_array
    file_CM_object.mrrRawHeight = rh_array
    file_CM_object.mrrRawNoSpec = np.ones(e1_2) * 5.7
    mrrRawSpectrum_array = np.ma.array(s_array, mask=np.zeros(s_array.shape))
    file_CM_object.mrrRawSpectrum = mrrRawSpectrum_array

    tf_array = np.zeros((e1_2, tranfer_function.shape[0]))
    tf_array = np.ma.array(tf_array, mask=np.zeros((tf_array.shape)))
    for t_ in range(e1_2):
        tf_array[t_, :] = tranfer_function
    file_CM_object.mrrRawTF = tf_array
    file_CM_object.mrrRawTime = file_CM.variables['time'][e1_1:e1_2]
    file_CM_object.shape2D = tuple((e1_2, file_CM.variables['range'].shape[0]))
    file_CM_object.shape3D = file_CM.variables['spectrum_reflectivity'].shape

    processedSpec_Pro = IMProToo_mod.MrrZe(file_CM_object)
    # processedSpec_CM.co["mrrFrequency"] = lamb_ # 24.15e9  24.23e9 #in Hz,]
    print('converted raw to mrrZe')
    processedSpec_Pro.averageSpectra(60)
    print('averaged')
    processedSpec_Pro.rawToSnow()
    print('calculated moments')

    # get data and correct
    dict_ = {}
    dict_['variables'] = {}
    dict_['dimensions'] = ('time', 'range', 'doppler_velocity')

    attribute_list = [
        ('author', 'Luis Ackermann'),
        ('author email', 'ackermannluis@gmail.com'),
        ('version', '4'),
        ('time of file creation', time_seconds_to_str(time.time(), '%Y-%m-%d_%H:%M UTC')),
    ]
    dict_['attributes'] = attribute_list


    # time
    dict_['variables']['time'] = {}
    dict_['variables']['time']['dimensions'] = ('time',)
    dict_['variables']['time']['attributes'] = [
        ('units', 'seconds since 1970-01-01_00:00:00'),
        ('description', 'time stamp is at beginning of average period')]
    dict_['variables']['time']['data'] = np.array(processedSpec_Pro.time[:].data) \
                            - 60 # the subtraction is such that time stamp is at beginning of average period

    # range
    dict_['variables']['range'] = {}
    dict_['variables']['range']['dimensions'] = ('range',)
    dict_['variables']['range']['attributes'] = [
        ('units', 'm'),
        ('description', 'height of sample in meters above instrument')]
    dict_['variables']['range']['data'] = processedSpec_Pro.H.data[0,:]

    # doppler_velocity
    dict_['variables']['doppler_velocity'] = {}
    dict_['variables']['doppler_velocity']['dimensions'] = ('doppler_velocity',)
    dict_['variables']['doppler_velocity']['attributes'] = [
        ('units', 'm/s'),
        ('description', 'fall speed of expanded spectra, positive is towards instrument')]
    dict_['variables']['doppler_velocity']['data'] = processedSpec_Pro.specVel

    # Ze_uncorrected
    dict_['variables']['Ze_uncorrected'] = {}
    dict_['variables']['Ze_uncorrected']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze_uncorrected']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'effective reflectivity uncorrected'),
        ('note', 'linearized => 10**(spectrum_reflectivity/10), has not been offset corrected')]
    Ze_imp = np.array(processedSpec_Pro.Ze[:, :].data)
    Ze_imp[Ze_imp == -9999] = np.nan
    dict_['variables']['Ze_uncorrected']['data'] = Ze_imp

    # W
    dict_['variables']['W'] = {}
    dict_['variables']['W']['dimensions'] = ('time', 'range',)
    dict_['variables']['W']['attributes'] = [
        ('units', 'm/s'),
        ('description', 'positive is towards the instrument'),
        ('long_name', 'particle fall speed')]
    W_imp = np.array(processedSpec_Pro.W[:, :].data)
    W_imp[W_imp == -9999] = np.nan
    W_imp[W_imp < -6] = np.nan
    W_imp[W_imp > 12] = np.nan
    dict_['variables']['W']['data'] = W_imp

    # Ze_metek
    dict_['variables']['Ze_metek'] = {}
    dict_['variables']['Ze_metek']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze_metek']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by Metek original software in MRR-Pro'),
        ('long_name', 'effective reflectivity from Metek'),
        ('note', 'assumes all particles are liquid and spherical, clutter masked using Impros Ze')]
    Ze_imp_mask = np.array(Ze_imp)
    Ze_imp_mask[~np.isnan(Ze_imp_mask)] = 1
    Ze_metek = file_CM.variables['Ze'][:, 1:].filled(np.nan)
    # Ze_metek_1mMean = row_average_discrete_2D(Ze_metek, 6)
    MRR_CM_time_1mMean, Ze_metek_1mMean = mean_discrete(MRR_CM_time, Ze_metek, 60,
                                                        dict_['variables']['time']['data'][0],
                                                        last_index=dict_['variables']['time']['data'][-1])
    Ze_metek_1mMean_mskd = Ze_metek_1mMean * Ze_imp_mask
    dict_['variables']['Ze_metek']['data'] = Ze_metek_1mMean_mskd

    # melted mask
    dict_['variables']['melted_mask'] = {}
    dict_['variables']['melted_mask']['dimensions'] = ('time', 'range',)
    dict_['variables']['melted_mask']['attributes'] = [
        ('description', 'computed by Metek original software in MRR-Pro, modified to include samples below ML'),
        ('long_name', 'bins below the melted layer computed by Metek, 1 = melted, nan = might be not melted')]
    ML_array = file_CM.variables['ML'][e1_1:e1_2,1:].filled(np.nan)
    ML_array[ML_array > 0.5] = 1
    # extend ML to surface
    for t_ in range(e1_2):
        if np.sum(ML_array[t_, :]) > 0:
            temp_c_index = np.arange(ML_array.shape[1]) * ML_array[t_, :]
            heights_ML = np.argmax(temp_c_index)
            ML_array[t_, :heights_ML] = 1
    # ML_array_1mMean = row_average_discrete_2D(ML_array, 6)
    MRR_CM_time_1mMean, ML_array_1mMean  = mean_discrete(MRR_CM_time, ML_array, 60,
                                                         dict_['variables']['time']['data'][0],
                                                         last_index=dict_['variables']['time']['data'][-1])
    ML_array_1mMean[ML_array_1mMean < 1] = 0
    ML_Mask = np.array(ML_array_1mMean)
    ML_Mask[ML_Mask == 0] = np.nan
    dict_['variables']['melted_mask']['data'] = ML_Mask

    # eta
    dict_['variables']['eta'] = {}
    dict_['variables']['eta']['dimensions'] = ('time', 'range','doppler_velocity',)
    dict_['variables']['eta']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'expanded reflectivity spectrum'),
        ('note', 'has not been offset corrected or linearized')]
    dict_['variables']['eta']['data'] = processedSpec_Pro.eta[:,:]

    # skewness
    dict_['variables']['skewness'] = {}
    dict_['variables']['skewness']['dimensions'] = ('time', 'range',)
    dict_['variables']['skewness']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'skewness of predominant peak')]
    dict_['variables']['skewness']['data'] = processedSpec_Pro.skewness[:,:]

    # kurtosis
    dict_['variables']['kurtosis'] = {}
    dict_['variables']['kurtosis']['dimensions'] = ('time', 'range',)
    dict_['variables']['kurtosis']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'kurtosis of predominant peak')]
    dict_['variables']['kurtosis']['data'] = processedSpec_Pro.kurtosis[:,:]

    # specWidth
    dict_['variables']['specWidth'] = {}
    dict_['variables']['specWidth']['dimensions'] = ('time', 'range',)
    dict_['variables']['specWidth']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'specWidth of predominant peak')]
    dict_['variables']['specWidth']['data'] = processedSpec_Pro.specWidth[:,:]


    save_dictionary_to_netcdf(dict_, output_filename)

    file_CM.close()
def MRR_PRO_process_IMProToo_5(filename_netcdf_MRR_Pro, output_filename,
                               mask_filename='D:/Data/MRR_CM/MRR_PRO_spectra_mask_latest.npy',
                               offset_correction=-26.168364489766237):
    file_CM = nc.Dataset(filename_netcdf_MRR_Pro)

    MRR_CM_time = np.array(file_CM.variables['time'][:])

    # define start and end rows according to time_interval
    e1_1 = 0
    e1_2 = MRR_CM_time.shape[0]

    # create mask
    mask_ = np.load(mask_filename)
    mask_[mask_ == 1] = np.nan
    mask_[mask_ == 0] = 1
    mask_3D = np.zeros((file_CM.variables['spectrum_reflectivity'][e1_1:e1_2].data.shape), dtype=float)
    mask_3D[:] = mask_

    # mask spectra
    spectrum_reflectivity_array = np.array(file_CM.variables['spectrum_reflectivity'][e1_1:e1_2])
    spectrum_reflectivity_array_masked = spectrum_reflectivity_array * mask_3D

    # interpolate the interference in the spectrum
    for t_ in range(e1_2):
        p_progress(t_, e1_2, extra_text='spectrum interpolated')
        spectrum_reflectivity_array[t_, :, :] = \
            array_2d_fill_gaps_by_interpolation_linear(spectrum_reflectivity_array_masked[t_, :, :])

    # get constants
    range_array = file_CM.variables['range'][:].data
    delta_H = np.median(np.diff(range_array))
    calibration_constant = int(file_CM.variables['calibration_constant'][0])  # * .015)
    tranfer_function = file_CM.variables['transfer_function'][:].data

    # convert x to s
    s_array = np.array(10 ** (spectrum_reflectivity_array / 10), dtype=int)


    # add attributes
    file_CM_object = Object_create()
    file_CM_object.header = file_CM.instrument_name
    file_CM_object.missingNumber = -9999
    file_CM_object.mrrRawCC = calibration_constant

    rh_array = np.zeros((e1_2, tranfer_function.shape[0]))
    rh_array = np.ma.array(rh_array, mask=np.zeros(rh_array.shape))
    for t_ in range(e1_2):
        rh_array[t_, :] = range_array
    file_CM_object.mrrRawHeight = rh_array
    file_CM_object.mrrRawNoSpec = np.ones(e1_2) * 5.7
    mrrRawSpectrum_array = np.ma.array(s_array, mask=np.zeros(s_array.shape))
    file_CM_object.mrrRawSpectrum = mrrRawSpectrum_array

    tf_array = np.zeros((e1_2, tranfer_function.shape[0]))
    tf_array = np.ma.array(tf_array, mask=np.zeros((tf_array.shape)))
    for t_ in range(e1_2):
        tf_array[t_, :] = tranfer_function
    file_CM_object.mrrRawTF = tf_array
    file_CM_object.mrrRawTime = file_CM.variables['time'][e1_1:e1_2]
    file_CM_object.shape2D = tuple((e1_2, file_CM.variables['range'].shape[0]))
    file_CM_object.shape3D = file_CM.variables['spectrum_reflectivity'].shape

    processedSpec_Pro = IMProToo_mod.MrrZe(file_CM_object)
    # processedSpec_CM.co["mrrFrequency"] = lamb_ # 24.15e9  24.23e9 #in Hz,]
    print('converted raw to mrrZe')
    processedSpec_Pro.averageSpectra(60)
    print('averaged')
    processedSpec_Pro.rawToSnow()
    print('calculated moments')

    # get data and correct
    dict_ = {}
    dict_['variables'] = {}
    dict_['dimensions'] = ('time', 'range', 'doppler_velocity')

    attribute_list = [
        ('author', 'Luis Ackermann'),
        ('author email', 'ackermannluis@gmail.com'),
        ('version', '4'),
        ('time of file creation', time_seconds_to_str(time.time(), '%Y-%m-%d_%H:%M UTC')),
    ]
    dict_['attributes'] = attribute_list


    # time
    dict_['variables']['time'] = {}
    dict_['variables']['time']['dimensions'] = ('time',)
    dict_['variables']['time']['attributes'] = [
        ('units', 'seconds since 1970-01-01_00:00:00'),
        ('description', 'time stamp is at beginning of average period')]
    dict_['variables']['time']['data'] = np.array(processedSpec_Pro.time[:].data) \
                            - 60 # the subtraction is such that time stamp is at beginning of average period

    # range
    dict_['variables']['range'] = {}
    dict_['variables']['range']['dimensions'] = ('range',)
    dict_['variables']['range']['attributes'] = [
        ('units', 'm'),
        ('description', 'height of sample in meters above instrument')]
    dict_['variables']['range']['data'] = processedSpec_Pro.H.data[0,:]

    # doppler_velocity
    dict_['variables']['doppler_velocity'] = {}
    dict_['variables']['doppler_velocity']['dimensions'] = ('doppler_velocity',)
    dict_['variables']['doppler_velocity']['attributes'] = [
        ('units', 'm/s'),
        ('description', 'fall speed of expanded spectra, positive is towards instrument')]
    dict_['variables']['doppler_velocity']['data'] = processedSpec_Pro.specVel

    # Ze_uncorrected
    dict_['variables']['Ze_uncorrected'] = {}
    dict_['variables']['Ze_uncorrected']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze_uncorrected']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'effective reflectivity uncorrected'),
        ('note', 'linearized => 10**(spectrum_reflectivity/10), has not been offset corrected')]
    Ze_imp = np.array(processedSpec_Pro.Ze[:, :].data)
    Ze_imp[Ze_imp == -9999] = np.nan
    dict_['variables']['Ze_uncorrected']['data'] = Ze_imp

    # Ze
    dict_['variables']['Ze'] = {}
    dict_['variables']['Ze']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'effective reflectivity corrected using Ze_metek below melted layer'),
        ('correction_applied', str(offset_correction)),
        ('note', 'linearized => 10**(spectrum_reflectivity/10), has not been offset corrected')]
    dict_['variables']['Ze']['data'] = Ze_imp + offset_correction

    # W
    dict_['variables']['W'] = {}
    dict_['variables']['W']['dimensions'] = ('time', 'range',)
    dict_['variables']['W']['attributes'] = [
        ('units', 'm/s'),
        ('description', 'positive is towards the instrument'),
        ('long_name', 'particle fall speed')]
    W_imp = np.array(processedSpec_Pro.W[:, :].data)
    W_imp[W_imp == -9999] = np.nan
    W_imp[W_imp < -6] = np.nan
    W_imp[W_imp > 12] = np.nan
    dict_['variables']['W']['data'] = W_imp

    # Ze_metek
    dict_['variables']['Ze_metek'] = {}
    dict_['variables']['Ze_metek']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze_metek']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by Metek original software in MRR-Pro'),
        ('long_name', 'effective reflectivity from Metek'),
        ('note', 'assumes all particles are liquid and spherical, clutter masked using Impros Ze')]
    Ze_imp_mask = np.array(Ze_imp)
    Ze_imp_mask[~np.isnan(Ze_imp_mask)] = 1
    Ze_metek = file_CM.variables['Ze'][:, 1:].filled(np.nan)
    # Ze_metek_1mMean = row_average_discrete_2D(Ze_metek, 6)
    MRR_CM_time_1mMean, Ze_metek_1mMean = mean_discrete(MRR_CM_time, Ze_metek, 60,
                                                        dict_['variables']['time']['data'][0],
                                                        last_index=dict_['variables']['time']['data'][-1])
    Ze_metek_1mMean_mskd = Ze_metek_1mMean * Ze_imp_mask
    dict_['variables']['Ze_metek']['data'] = Ze_metek_1mMean_mskd


    # melted mask
    dict_['variables']['melted_mask'] = {}
    dict_['variables']['melted_mask']['dimensions'] = ('time', 'range',)
    dict_['variables']['melted_mask']['attributes'] = [
        ('description', 'computed by Metek original software in MRR-Pro, modified to include samples below ML'),
        ('long_name', 'bins below the melted layer computed by Metek, 1 = melted, nan = might be not melted')]
    ML_array = file_CM.variables['ML'][e1_1:e1_2,1:].filled(np.nan)
    ML_array[ML_array > 0.5] = 1
    # extend ML to surface
    for t_ in range(e1_2):
        if np.sum(ML_array[t_, :]) > 0:
            temp_c_index = np.arange(ML_array.shape[1]) * ML_array[t_, :]
            heights_ML = np.argmax(temp_c_index)
            ML_array[t_, :heights_ML] = 1
    # ML_array_1mMean = row_average_discrete_2D(ML_array, 6)
    MRR_CM_time_1mMean, ML_array_1mMean  = mean_discrete(MRR_CM_time, ML_array, 60,
                                                         dict_['variables']['time']['data'][0],
                                                         last_index=dict_['variables']['time']['data'][-1])
    ML_array_1mMean[ML_array_1mMean < 1] = 0
    ML_Mask = np.array(ML_array_1mMean)
    ML_Mask[ML_Mask == 0] = np.nan
    dict_['variables']['melted_mask']['data'] = ML_Mask

    # eta
    dict_['variables']['eta'] = {}
    dict_['variables']['eta']['dimensions'] = ('time', 'range','doppler_velocity',)
    dict_['variables']['eta']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'expanded reflectivity spectrum'),
        ('note', 'has not been offset corrected or linearized')]
    dict_['variables']['eta']['data'] = processedSpec_Pro.eta[:,:]

    # skewness
    dict_['variables']['skewness'] = {}
    dict_['variables']['skewness']['dimensions'] = ('time', 'range',)
    dict_['variables']['skewness']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'skewness of predominant peak')]
    dict_['variables']['skewness']['data'] = processedSpec_Pro.skewness[:,:]

    # kurtosis
    dict_['variables']['kurtosis'] = {}
    dict_['variables']['kurtosis']['dimensions'] = ('time', 'range',)
    dict_['variables']['kurtosis']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'kurtosis of predominant peak')]
    dict_['variables']['kurtosis']['data'] = processedSpec_Pro.kurtosis[:,:]

    # specWidth
    dict_['variables']['specWidth'] = {}
    dict_['variables']['specWidth']['dimensions'] = ('time', 'range',)
    dict_['variables']['specWidth']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'specWidth of predominant peak')]
    dict_['variables']['specWidth']['data'] = processedSpec_Pro.specWidth[:,:]


    save_dictionary_to_netcdf(dict_, output_filename)

    file_CM.close()
def MRR_PRO_process_add_Ze_to_IMProToo_4_V6(filename_postprocessed_V4, offset_correction, output_filename,
                                            use_metek_to_mask_imp_Ze=False):
    dict_ = load_netcdf_to_dictionary(filename_postprocessed_V4, print_debug=False)

    # Ze
    dict_['variables']['Ze'] = {}
    dict_['variables']['Ze']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'effective reflectivity corrected'),
        ('note', 'linearized => 10**(spectrum_reflectivity/10), has been offset corrected'),
        ('correction_offset', offset_correction)]
    Ze_uncorrected = np.array(dict_['variables']['Ze_uncorrected']['data'])

    if use_metek_to_mask_imp_Ze:
        Ze_metek = np.array(dict_['variables']['Ze_metek']['data'])
        Ze_metek_mask = np.zeros(Ze_metek.shape) * np.nan
        Ze_metek_mask[~np.isnan(Ze_metek)] = 1

        dict_['variables']['Ze']['data'] = (Ze_uncorrected * Ze_metek_mask) + offset_correction

        W_ = np.array(dict_['variables']['W']['data'])
        dict_['variables']['W']['data'] = W_ * Ze_metek_mask
    else:
        dict_['variables']['Ze']['data'] = Ze_uncorrected + offset_correction


    save_dictionary_to_netcdf(dict_, output_filename, print_debug=False)
def MRR_PRO_process_IMProToo_7(filename_netcdf_MRR_Pro, output_filename,
                               mask_filename='D:/Data/MRR_CM/MRR_PRO_spectra_mask_latest.npy'):
    file_CM = nc.Dataset(filename_netcdf_MRR_Pro)

    MRR_CM_time = np.array(file_CM.variables['time'][:])

    # define start and end rows according to time_interval
    e1_1 = 0
    e1_2 = MRR_CM_time.shape[0]

    # create mask
    mask_ = np.load(mask_filename)
    mask_[mask_ == 1] = np.nan
    mask_[mask_ == 0] = 1
    mask_3D = np.zeros((file_CM.variables['spectrum_raw'][e1_1:e1_2].data.shape), dtype=float)
    mask_3D[:] = mask_

    # mask spectra
    spectrum_reflectivity_array = np.array(file_CM.variables['spectrum_raw'][e1_1:e1_2])
    spectrum_reflectivity_array_masked = spectrum_reflectivity_array * mask_3D

    # interpolate the interference in the spectrum
    for t_ in range(e1_2):
        p_progress(t_, e1_2, extra_text='spectrum interpolated')
        spectrum_reflectivity_array[t_, :, :] = \
            array_2d_fill_gaps_by_interpolation_linear(spectrum_reflectivity_array_masked[t_, :, :])

    # get constants
    range_array = file_CM.variables['range'][:].data
    delta_H = np.median(np.diff(range_array))
    calibration_constant = int(file_CM.variables['calibration_constant'][0])  # * .015)
    tranfer_function = file_CM.variables['transfer_function'][:].data

    # convert x to s
    s_array = np.array(10 ** (spectrum_reflectivity_array / 10), dtype=int)


    # add attributes
    file_CM_object = Object_create()
    file_CM_object.header = file_CM.instrument_name
    file_CM_object.missingNumber = -9999
    file_CM_object.mrrRawCC = calibration_constant

    rh_array = np.zeros((e1_2, tranfer_function.shape[0]))
    rh_array = np.ma.array(rh_array, mask=np.zeros(rh_array.shape))
    for t_ in range(e1_2):
        rh_array[t_, :] = range_array
    file_CM_object.mrrRawHeight = rh_array
    file_CM_object.mrrRawNoSpec = np.ones(e1_2) * 5.7
    mrrRawSpectrum_array = np.ma.array(s_array, mask=np.zeros(s_array.shape))
    file_CM_object.mrrRawSpectrum = mrrRawSpectrum_array

    tf_array = np.zeros((e1_2, tranfer_function.shape[0]))
    tf_array = np.ma.array(tf_array, mask=np.zeros((tf_array.shape)))
    for t_ in range(e1_2):
        tf_array[t_, :] = tranfer_function
    file_CM_object.mrrRawTF = tf_array
    file_CM_object.mrrRawTime = file_CM.variables['time'][e1_1:e1_2]
    file_CM_object.shape2D = tuple((e1_2, file_CM.variables['range'].shape[0]))
    file_CM_object.shape3D = file_CM.variables['spectrum_raw'].shape

    processedSpec_Pro = IMProToo_mod.MrrZe(file_CM_object)
    # processedSpec_CM.co["mrrFrequency"] = lamb_ # 24.15e9  24.23e9 #in Hz,]
    print('converted raw to mrrZe')
    processedSpec_Pro.averageSpectra(60)
    print('averaged')
    processedSpec_Pro.rawToSnow()
    print('calculated moments')

    # get data and correct
    dict_ = {}
    dict_['variables'] = {}
    dict_['dimensions'] = ('time', 'range', 'doppler_velocity')

    attribute_list = [
        ('author', 'Luis Ackermann'),
        ('author email', 'ackermannluis@gmail.com'),
        ('version', '4'),
        ('time of file creation', time_seconds_to_str(time.time(), '%Y-%m-%d_%H:%M UTC')),
    ]
    dict_['attributes'] = attribute_list


    # time
    dict_['variables']['time'] = {}
    dict_['variables']['time']['dimensions'] = ('time',)
    dict_['variables']['time']['attributes'] = [
        ('units', 'seconds since 1970-01-01_00:00:00'),
        ('description', 'time stamp is at beginning of average period')]
    dict_['variables']['time']['data'] = np.array(processedSpec_Pro.time[:].data) \
                            - 60 # the subtraction is such that time stamp is at beginning of average period

    # range
    dict_['variables']['range'] = {}
    dict_['variables']['range']['dimensions'] = ('range',)
    dict_['variables']['range']['attributes'] = [
        ('units', 'm'),
        ('description', 'height of sample in meters above instrument')]
    dict_['variables']['range']['data'] = processedSpec_Pro.H.data[0,:]

    # doppler_velocity
    dict_['variables']['doppler_velocity'] = {}
    dict_['variables']['doppler_velocity']['dimensions'] = ('doppler_velocity',)
    dict_['variables']['doppler_velocity']['attributes'] = [
        ('units', 'm/s'),
        ('description', 'fall speed of expanded spectra, positive is towards instrument')]
    dict_['variables']['doppler_velocity']['data'] = processedSpec_Pro.specVel

    # Ze_uncorrected
    dict_['variables']['Ze_uncorrected'] = {}
    dict_['variables']['Ze_uncorrected']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze_uncorrected']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'effective reflectivity uncorrected'),
        ('note', 'linearized => 10**(spectrum_reflectivity/10), has not been offset corrected')]
    Ze_imp = np.array(processedSpec_Pro.Ze[:, :].data)
    Ze_imp[Ze_imp == -9999] = np.nan
    dict_['variables']['Ze_uncorrected']['data'] = Ze_imp

    # W
    dict_['variables']['W'] = {}
    dict_['variables']['W']['dimensions'] = ('time', 'range',)
    dict_['variables']['W']['attributes'] = [
        ('units', 'm/s'),
        ('description', 'positive is towards the instrument'),
        ('long_name', 'particle fall speed')]
    W_imp = np.array(processedSpec_Pro.W[:, :].data)
    W_imp[W_imp == -9999] = np.nan
    W_imp[W_imp < -6] = np.nan
    W_imp[W_imp > 12] = np.nan
    dict_['variables']['W']['data'] = W_imp

    # Ze_metek
    dict_['variables']['Ze_metek'] = {}
    dict_['variables']['Ze_metek']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze_metek']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by Metek original software in MRR-Pro'),
        ('long_name', 'effective reflectivity from Metek'),
        ('note', 'assumes all particles are liquid and spherical, clutter masked using Impros Ze')]
    Ze_imp_mask = np.array(Ze_imp)
    Ze_imp_mask[~np.isnan(Ze_imp_mask)] = 1
    Ze_metek = file_CM.variables['Ze'][:, 1:].filled(np.nan)
    # Ze_metek_1mMean = row_average_discrete_2D(Ze_metek, 6)
    MRR_CM_time_1mMean, Ze_metek_1mMean = mean_discrete(MRR_CM_time, Ze_metek, 60,
                                                        dict_['variables']['time']['data'][0],
                                                        last_index=dict_['variables']['time']['data'][-1])
    Ze_metek_1mMean_mskd = Ze_metek_1mMean * Ze_imp_mask
    dict_['variables']['Ze_metek']['data'] = Ze_metek_1mMean_mskd

    # melted mask
    dict_['variables']['melted_mask'] = {}
    dict_['variables']['melted_mask']['dimensions'] = ('time', 'range',)
    dict_['variables']['melted_mask']['attributes'] = [
        ('description', 'computed by Metek original software in MRR-Pro, modified to include samples below ML'),
        ('long_name', 'bins below the melted layer computed by Metek, 1 = melted, nan = might be not melted')]
    ML_array = file_CM.variables['ML'][e1_1:e1_2,1:].filled(np.nan)
    ML_array[ML_array > 0.5] = 1
    # extend ML to surface
    for t_ in range(e1_2):
        if np.sum(ML_array[t_, :]) > 0:
            temp_c_index = np.arange(ML_array.shape[1]) * ML_array[t_, :]
            heights_ML = np.argmax(temp_c_index)
            ML_array[t_, :heights_ML] = 1
    # ML_array_1mMean = row_average_discrete_2D(ML_array, 6)
    MRR_CM_time_1mMean, ML_array_1mMean  = mean_discrete(MRR_CM_time, ML_array, 60,
                                                         dict_['variables']['time']['data'][0],
                                                         last_index=dict_['variables']['time']['data'][-1])
    ML_array_1mMean[ML_array_1mMean < 1] = 0
    ML_Mask = np.array(ML_array_1mMean)
    ML_Mask[ML_Mask == 0] = np.nan
    dict_['variables']['melted_mask']['data'] = ML_Mask

    # eta
    dict_['variables']['eta'] = {}
    dict_['variables']['eta']['dimensions'] = ('time', 'range','doppler_velocity',)
    dict_['variables']['eta']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'expanded reflectivity spectrum'),
        ('note', 'has not been offset corrected or linearized')]
    dict_['variables']['eta']['data'] = processedSpec_Pro.eta[:,:]

    # skewness
    dict_['variables']['skewness'] = {}
    dict_['variables']['skewness']['dimensions'] = ('time', 'range',)
    dict_['variables']['skewness']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'skewness of predominant peak')]
    dict_['variables']['skewness']['data'] = processedSpec_Pro.skewness[:,:]

    # kurtosis
    dict_['variables']['kurtosis'] = {}
    dict_['variables']['kurtosis']['dimensions'] = ('time', 'range',)
    dict_['variables']['kurtosis']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'kurtosis of predominant peak')]
    dict_['variables']['kurtosis']['data'] = processedSpec_Pro.kurtosis[:,:]

    # specWidth
    dict_['variables']['specWidth'] = {}
    dict_['variables']['specWidth']['dimensions'] = ('time', 'range',)
    dict_['variables']['specWidth']['attributes'] = [
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'specWidth of predominant peak')]
    dict_['variables']['specWidth']['data'] = processedSpec_Pro.specWidth[:,:]


    save_dictionary_to_netcdf(dict_, output_filename)

    file_CM.close()
def MRR_fix_raw_file(filename_):
    # get file text into line list
    with open(filename_, 'r') as file_:
        line_txt = ' '
        counter_ = 0
        line_txt_list = []
        while line_txt != '':
            try:
                line_txt = file_.readline()
            except:
                pass
            line_txt_list.append(line_txt)
            counter_ += 1

    final_line_list = []
    r_ = -1
    while r_ < len(line_txt_list) and line_txt_list[r_+1] != '':
        r_ += 1
        if line_txt_list[r_][0] == 'M':
            #start new scan
            scan_lines = [line_txt_list[r_]]
            while r_ < len(line_txt_list) and line_txt_list[r_+1] != '':
                r_ += 1
                if line_txt_list[r_][0] != 'M':
                    scan_lines.append(line_txt_list[r_])
                else:
                    r_ -= 1
                    break
            if len(scan_lines) == 67 and scan_lines[1][0] == 'H' and scan_lines[2][:2] == 'TF':
                all_Fs_present = True
                for i_, lines_ in enumerate(scan_lines[3:]):
                    if lines_[:3] != 'F' + str(i_).zfill(2):
                        all_Fs_present = False

                if all_Fs_present:
                    for line_ in scan_lines:
                        final_line_list.append(line_)

    with open(filename_, 'w') as file_:
        for line_txt in final_line_list:
            file_.write(line_txt)


def MRR_load_snow_period_to_dict(site_name_or_path, start_time_YMDHM, stop_time_YMDHM,
                                 variable_names=('time', 'height', 'Ze', 'W')):

    out_dict = {}
    temp_dict = {}

    if not 'time' in variable_names:
        variable_names_temp_list = ['time']
        for variable_name in variable_names:
            variable_names_temp_list.append(variable_name)
        variable_names = variable_names_temp_list

    # data_folder
    if len(site_name_or_path.replace('\\','/').split('/')) == 1:
        data_folder = 'D:/Data/MRR_' + site_name_or_path + '/Snow/'
    else:
        data_folder = site_name_or_path

    # get all data files filenames
    file_list = sorted(glob.glob(str(data_folder + '/*.nc')))
    file_times_tuple_list = []
    for filename_ in file_list:
        file_time_sec = time_str_to_seconds(filename_.replace('\\','/').split('/')[-1][3:-3], '%Y%m%d')
        file_times_tuple_list.append(tuple((file_time_sec, file_time_sec + (24*60*60))))


    # select only files inside time range
    event_start_sec = time_str_to_seconds(start_time_YMDHM, '%Y%m%d%H%M')
    event_stop_sec = time_str_to_seconds(stop_time_YMDHM, '%Y%m%d%H%M')
    selected_file_list = []
    for file_index in range(len(file_list)):
        if event_start_sec <= file_times_tuple_list[file_index][0] <= event_stop_sec:
            selected_file_list.append(file_list[file_index])
        elif event_start_sec <= file_times_tuple_list[file_index][1] <= event_stop_sec:
            selected_file_list.append(file_list[file_index])
        elif file_times_tuple_list[file_index][0] <= event_start_sec <= file_times_tuple_list[file_index][1]:
            selected_file_list.append(file_list[file_index])
    print('found files:')
    p_(selected_file_list)


    # load data
    if len(selected_file_list) == 0:
        print('No files inside time range!')
        return out_dict
    else:
        cnt = 0
        for filename_ in selected_file_list:
            if cnt == 0:
                nc_file = nc.Dataset(filename_, 'r')
                for variable_name in variable_names:
                    temp_dict[variable_name] = np.array(nc_file.variables[variable_name][:],dtype=float)
                nc_file.close()
                cnt += 1
            else:
                nc_file = nc.Dataset(filename_, 'r')
                for variable_name in variable_names:
                    if len(nc_file.variables[variable_name].shape) == 1:
                        temp_dict[variable_name] = np.hstack((temp_dict[variable_name],
                                                              np.array(nc_file.variables[variable_name][:])))
                    else:
                        temp_dict[variable_name] = np.vstack((temp_dict[variable_name],
                                                              np.array(nc_file.variables[variable_name][:])))
                nc_file.close()


    # find row for start and end of event
    start_row = np.argmin(np.abs(temp_dict['time'] - event_start_sec))
    end_row = np.argmin(np.abs(temp_dict['time'] - event_stop_sec))

    for variable_name in variable_names:
        temp_dict[variable_name][temp_dict[variable_name] == -9999] = np.nan
        out_dict[variable_name] = temp_dict[variable_name][start_row:end_row]

    return out_dict
def MRR_load_PRO_period_to_dict(start_time_YMDHM, stop_time_YMDHM,
                                variable_names=('time', 'range', 'Ze', 'WIDTH', 'VEL', 'Z', 'Za', 'Zea')):
    out_dict = {}
    temp_dict = {}
    variables_with_time_dimension = []

    if not 'time' in variable_names:
        variable_names_temp_list = ['time']
        for variable_name in variable_names:
            variable_names_temp_list.append(variable_name)
        variable_names = variable_names_temp_list

    # data_folder
    data_folder = 'D:/Data/MRR_CM/Daily files'

    # get all data files filenames
    file_list = sorted(glob.glob(str(data_folder + '/*.nc')))
    file_times_tuple_list = []
    for filename_ in file_list:
        file_time_sec = time_str_to_seconds(filename_.replace('\\','/').split('/')[-1][:15], '%Y%m%d_%H%M%S')
        file_times_tuple_list.append(tuple((file_time_sec, file_time_sec + (24*60*60))))

    # select only files inside time range
    event_start_sec = time_str_to_seconds(start_time_YMDHM, '%Y%m%d%H%M')
    event_stop_sec = time_str_to_seconds(stop_time_YMDHM, '%Y%m%d%H%M')
    selected_file_list = []
    for file_index in range(len(file_list)):
        if event_start_sec <= file_times_tuple_list[file_index][0] <= event_stop_sec:
            selected_file_list.append(file_list[file_index])
        elif event_start_sec <= file_times_tuple_list[file_index][1] <= event_stop_sec:
            selected_file_list.append(file_list[file_index])
        elif file_times_tuple_list[file_index][0] <= event_start_sec <= file_times_tuple_list[file_index][1]:
            selected_file_list.append(file_list[file_index])
    print('found files:')
    p_(selected_file_list)

    # load data
    if len(selected_file_list) == 0:
        print('No files inside time range!')
        return out_dict
    else:
        cnt = 0
        for filename_ in selected_file_list:
            if cnt == 0:
                nc_file = nc.Dataset(filename_, 'r')
                print('reading file:',filename_)
                for variable_name in variable_names:
                    temp_dict[variable_name] = np.array(nc_file.variables[variable_name][:],dtype=float)
                nc_file.close()
                cnt += 1
            else:
                nc_file = nc.Dataset(filename_, 'r')
                print('reading file:', filename_)
                for variable_name in variable_names:
                    if 'time' in nc_file.variables[variable_name].dimensions:
                        variables_with_time_dimension.append(variable_name)
                        if len(nc_file.variables[variable_name].shape) == 1:
                            temp_dict[variable_name] = np.hstack((temp_dict[variable_name],
                                                                  np.array(nc_file.variables[variable_name][:])))
                        else:
                            temp_dict[variable_name] = np.vstack((temp_dict[variable_name],
                                                                  np.array(nc_file.variables[variable_name][:])))
                nc_file.close()

    # find row for start and end of event
    start_row = np.argmin(np.abs(temp_dict['time'] - event_start_sec))
    end_row = np.argmin(np.abs(temp_dict['time'] - event_stop_sec))

    for variable_name in variable_names:
        temp_dict[variable_name][temp_dict[variable_name] == -9999] = np.nan
        if variable_name in variables_with_time_dimension:
            out_dict[variable_name] = temp_dict[variable_name][start_row:end_row]
        else:
            out_dict[variable_name] = temp_dict[variable_name]

    return out_dict
def MRR_CFAD(range_array, Ze_array, bins_=(12, np.arange(-10, 40, 2)), normalize_height_wise = True, x_header='dBZe',
             y_header='Height [km]', custom_y_range_tuple=None, custom_x_range_tuple=None, figure_filename=None,
             cbar_label='', cmap_=default_cm, figsize_ = (10,6), title_str = '', contourF_=True, cbar_format='%.2f',
             vmin_=None,vmax_=None, grid_=True, fig_ax=None, show_cbar=True, level_threshold_perc=10, invert_y=False,
             levels=None,custom_ticks_x=None, custom_ticks_y=None, cbar_ax=None, cbar_orient='vertical',
             extend_='neither'):
    """
    :param range_array:
    :param Ze_array:
    :param bins_:
    :param normalize_height_wise:
    :param x_header:
    :param y_header:
    :param custom_y_range_tuple:
    :param custom_x_range_tuple:
    :param figure_filename:
    :param cbar_label:
    :param cmap_:
    :param figsize_:
    :param title_str:
    :param contourF_:
    :param cbar_format:
    :param vmin_:
    :param vmax_:
    :param grid_:
    :param fig_ax:
    :param show_cbar:
    :param level_threshold_perc:
    :param invert_y:
    :param levels:
    :param custom_ticks_x:
    :param custom_ticks_y:
    :param cbar_ax:
    :param cbar_orient:
    :param extend_: {'neither', 'both', 'min', 'max'}
    :return:
    """


    if len(range_array.shape) == 1:
        temp_array = np.zeros((Ze_array.shape))
        for r_ in range(Ze_array.shape[0]):
            temp_array[r_,:] = range_array
        range_array = temp_array

    if type(bins_[0]) == int:
        if bins_[0] < 1:
            bins_ = (int(range_array.shape[1] * bins_[0]), bins_[1])

    hist_out = np.histogram2d(range_array.flatten()[~np.isnan(Ze_array.flatten())] / 1000,
                              Ze_array.flatten()[~np.isnan(Ze_array.flatten())],
                              normed=False, bins=bins_)
    hist_array, hist_r, hist_c = hist_out
    hist_r = (hist_r[:-1] + hist_r[1:]) * 0.5
    hist_c = (hist_c[:-1] + hist_c[1:]) * 0.5

    hist_r_2d = np.zeros((hist_array.shape), dtype=float)
    hist_c_2d = np.zeros((hist_array.shape), dtype=float)

    for r_ in range(hist_array.shape[0]):
        for c_ in range(hist_array.shape[1]):
            hist_r_2d[r_, c_] = hist_r[r_]
            hist_c_2d[r_, c_] = hist_c[c_]

    # normalize height wise
    if normalize_height_wise:
        heights_counts = np.sum(hist_array, axis=1)
        maximum_count_at_some_height = np.max(heights_counts)
        cbar_label_final = 'Height normalized frequency'
        for r_ in range(hist_array.shape[0]):
            if heights_counts[r_] < maximum_count_at_some_height * (level_threshold_perc/100):
                hist_array[r_, :] = np.nan
            else:
                 hist_array[r_, :] = hist_array[r_, :] / heights_counts[r_]
    else:
        cbar_label_final = 'Normalized frequency'

    if cbar_label == '': cbar_label = cbar_label_final

    fig_ax = p_arr_vectorized_3(hist_array, hist_c_2d, hist_r_2d, contourF_=contourF_, grid_=grid_,
                                custom_y_range_tuple=custom_y_range_tuple, custom_x_range_tuple=custom_x_range_tuple,
                                x_header=x_header, y_header=y_header, cmap_=cmap_, figsize_=figsize_, cbar_ax=cbar_ax,
                                cbar_label=cbar_label, title_str=title_str, vmin_=vmin_, vmax_=vmax_,levels=levels,
                                figure_filename=figure_filename, fig_ax=fig_ax,show_cbar=show_cbar, invert_y=invert_y,
                                custom_ticks_x=custom_ticks_x, custom_ticks_y=custom_ticks_y,cbar_format=cbar_format,
                                cbar_orient=cbar_orient, extend_=extend_)
    return fig_ax, hist_array.T, hist_c[:-1], hist_r[:-1]
def CFAD(Y_array, x_values_array, bins_tuple_y_x=(12, np.arange(-10, 40, 2)), normalize_height_wise = True,
         x_header='', y_header='', custom_y_range_tuple=None, custom_x_range_tuple=None, figure_filename=None,
         cbar_label='', cmap_=default_cm, figsize_ = (10 ,6), title_str = '', contourF_=True, cbar_format='%.2f',
         vmin_=None ,vmax_=None, grid_=True, fig_ax=None, show_cbar=True, level_threshold_perc=10,
         invert_y=False, levels=None ,custom_ticks_x=None, custom_ticks_y=None, cbar_ax=None, cbar_orient='vertical',
         font_size_axes_labels=14, font_size_title=16, font_size_ticks=10, extend_='neither'):
    """
    creates a figure with a countour frequency by altitude diagram.
    :param Y_array: can be 1d with lenght equal to x_values_array first dimension,
                    or 2d with the same shape as x_values_array
    :param x_values_array: 2d array with values that will be used to define the x axis.
    :param bins_tuple_y_x: a tuple with two items. These will define the grid of the figure (y bins, x bins).
                  each tuple item can be a fraction (only for y), an integer, or a list/1d array.
                    if it is a fraction, then there will be fraction * the number of rows or columns (only for y)
                    if it is an integer, then there will be integer number of bins
                    if it is a list/array, the elements will be the boundaries of the bins
    :param normalize_height_wise: if True, each row will be divided by the total count (sum) of that row
    :param x_header: str with the desired x header
    :param y_header: str with the desired y header
    :param custom_y_range_tuple: tuple with min and max y values to be shown in figure, this is just for display
    :param custom_x_range_tuple: tuple with min and max x values to be shown in figure, this is just for display
    :param figure_filename: If set to a str with a path and filename, the figure will be saved and closed
    :param cbar_label: str with the desired color bar label
    :param cmap_: matplotlib object colormap
    :param figsize_: tuple with the size of the figure in inches (x, y)
    :param title_str: str with title of figure
    :param contourF_: If true, the figure will be of filled countours, else it will be a pcolormesh
    :param cbar_format: the str format for the ticks of the colorbar, if only integers wanted set to '%i'
    :param vmin_: minimum frequency to be displayed in the figure (sets the range of the colorbar)
    :param vmax_: maximum frequency to be displayed in the figure (sets the range of the colorbar)
    :param grid_: if true, the grid will be shown
    :param fig_ax: tuple with a figure and axes object from matplotlib. use this if you already have a figure and want
                    to add a CFAD to it, or for multiple panels
    :param show_cbar: If true the cbar is shown.
    :param level_threshold_perc: if the total count at a row is less than this % of the row with most counts, it will
                                    not be shown
    :param invert_y: if true the y axes will be inversed in the display, usefull for CFTDs (by temperature)
    :param levels: list/array with the ticks for the colorbar
    :param custom_ticks_x: list/array with the ticks for the x axes
    :param custom_ticks_y: list/array with the ticks for the y axes
    :param cbar_ax: axes object from matplotlib where the colorbar will be placed, usefull when multiple CFADs are in
                    the same figure and share one colorbar.
    :param cbar_orient: 'vertical' or 'horizontal'
    :param font_size_axes_labels: size of font of axes labels in graph
    :param font_size_title: size of font of title in graph
    :param font_size_ticks: size of font of ticks in graph
    :return:
        fig_ax_surf: tuple with:
                                fig: figure objects
                                ax: axes objects
                                surface: the point colection from matplotlib
        hist_array: 2d array with the frequency data
        hist_c: 1d array with the x axes series
        hist_r: 1d array with the y axes series
    """

    if len(Y_array.shape) == 1:
        temp_array = np.zeros(x_values_array.shape)
        for r_ in range(x_values_array.shape[0]):
            temp_array[r_ ,:] = Y_array
        Y_array = temp_array

    if type(bins_tuple_y_x[0]) == int:
        if bins_tuple_y_x[0] < 1:
            bins_tuple_y_x = (int(Y_array.shape[1] * bins_tuple_y_x[0]), bins_tuple_y_x[1])




    hist_out = np.histogram2d(Y_array.flatten()[~np.isnan(x_values_array.flatten())],
                              x_values_array.flatten()[~np.isnan(x_values_array.flatten())],
                              bins=bins_tuple_y_x)
    hist_array, hist_r, hist_c = hist_out
    hist_r = (hist_r[:-1] + hist_r[1:]) * 0.5
    hist_c = (hist_c[:-1] + hist_c[1:]) * 0.5

    hist_r_2d = np.zeros(hist_array.shape, dtype=float)
    hist_c_2d = np.zeros(hist_array.shape, dtype=float)

    for r_ in range(hist_array.shape[0]):
        for c_ in range(hist_array.shape[1]):
            hist_r_2d[r_, c_] = hist_r[r_]
            hist_c_2d[r_, c_] = hist_c[c_]

    # normalize height wise
    if normalize_height_wise:
        heights_counts = np.sum(hist_array, axis=1)
        maximum_count_at_some_height = np.max(heights_counts)
        cbar_label_final = 'Height normalized frequency'
        for r_ in range(hist_array.shape[0]):
            if heights_counts[r_] < maximum_count_at_some_height * (level_threshold_perc /100):
                hist_array[r_, :] = np.nan
            else:
                hist_array[r_, :] = hist_array[r_, :] / heights_counts[r_]
    else:
        hist_array = hist_array / np.sum(hist_array)
        cbar_label_final = 'Normalized frequency'

    if cbar_label == '': cbar_label = cbar_label_final

    fig_ax = p_arr_vectorized_3(hist_array, hist_c_2d, hist_r_2d, contourF_=contourF_, grid_=grid_,
                                custom_y_range_tuple=custom_y_range_tuple, custom_x_range_tuple=custom_x_range_tuple,
                                x_header=x_header, y_header=y_header, cmap_=cmap_, figsize_=figsize_, cbar_ax=cbar_ax,
                                cbar_label=cbar_label, title_str=title_str, vmin_=vmin_, vmax_=vmax_ ,levels=levels,
                                figure_filename=figure_filename, fig_ax=fig_ax ,show_cbar=show_cbar, invert_y=invert_y,
                                custom_ticks_x=custom_ticks_x, custom_ticks_y=custom_ticks_y ,cbar_format=cbar_format,
                                font_size_axes_labels=font_size_axes_labels, font_size_title=font_size_title,
                                font_size_ticks=font_size_ticks, extend_=extend_, cbar_orient=cbar_orient)
    return fig_ax, hist_array.T, hist_c[:-1], hist_r[:-1]


# parsivel
def parsivel_raw_csv_to_netcdf(filename_input_csv, filename_output_nc, delimeter_=','):
    """
    Reads the raw data generated using https://github.com/ackermannluis/parsivel2_datalogger from a
    parsive-2 disdrometer, calculates the spectrum concentration, and other supporting variables, and saves
    data to a netcdf file.
    :param filename_input_csv: full path of input file created by https://github.com/ackermannluis/parsivel2_datalogger
    :param filename_output_nc: should include full path and extension. It will replace file if already exist!
    :param delimeter_: string with the file's delimiter, default is ','
    :return: None
    """

    # read data
    with open(filename_input_csv, 'r') as file_:
        file_lines_list = file_.readlines()

    # get header
    file_header_list = file_lines_list[0].split(delimeter_)[:-1]

    # segregate data into variables using a dictionary with keys from the header
    dict_raw_lists = {}
    for var_name in file_header_list:
        dict_raw_lists[var_name] = []

    # populate raw dictionary
    for row_ in range(1, len(file_lines_list)):
        row_list = file_lines_list[row_].split(delimeter_)
        if len(row_list) == 1040:
            for col_, var_name in enumerate(file_header_list):
                if var_name == 'raw_spectra':
                    dict_raw_lists[var_name].append(row_list[15:-1])  # spectra is a flat list, not a single value
                else:
                    dict_raw_lists[var_name].append(row_list[col_])

    # create data quality mask
    sensor_status_arr = np.array(dict_raw_lists['sensor_status'], dtype=int)
    mask_ = np.zeros(sensor_status_arr.size, dtype=bool)
    mask_[sensor_status_arr > 1] = True

    # reformat time
    time_arr = time_str_to_seconds(dict_raw_lists['datetime'], time_format_mod) # unix time

    # reshape spectrum data
    raw_spectrum_list = dict_raw_lists['raw_spectra']
    spectrum_array = np.zeros((len(raw_spectrum_list), 32, 32), dtype=float)
    for row_ in range(len(raw_spectrum_list)):
        spectrum_array[row_, :, :] = np.array(raw_spectrum_list[row_], dtype=float).reshape((32,32))

    # create spectrum axis arrays
    size_scale = np.array([0.062,0.187,0.312,0.437,0.562,0.687,0.812,0.937,1.062,1.187,1.375,1.625,1.875,
                  2.125,2.375,2.75,3.25,3.75,4.25,4.75,5.5,6.5,7.5,8.5,9.5,11,13,15,17,19,21.5,24.5])
    speed_scale = np.array([0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.1,1.3,1.5,1.7,1.9,2.2,2.6,3,3.4,
                   3.8,4.4,5.2,6,6.8,7.6,8.8,10.4,12,13.6,15.2,17.6,20.8])
    speed_array = np.zeros((32,32), dtype=float)
    size_array = np.zeros((32, 32), dtype=float)
    for i in range(32):
        speed_array[:,i] = speed_scale
        size_array[i, :] = size_scale

    # get sampling volume
    sampling_volume_2d = parsivel_sampling_volume(size_array, speed_array)

    # calculate spectrum concentration
    particle_concentration_spectrum = spectrum_array / sampling_volume_2d

    # create particle_concentration_total_m-3
    particle_concentration_total = np.nansum(np.nansum(particle_concentration_spectrum, axis=-1), axis=-1)

    # get hydrometer type
    hydrometeor_type = parsivel_convert_METAR_code_to_numbers(np.array(dict_raw_lists['rain_intensity_mm/hr'],
                                                                       dtype=float),
                                                              np.array(dict_raw_lists['weather_code_METAR'],
                                                                       dtype=str))

    # calculate PSD per size bin
    PSD_array = np.sum(particle_concentration_spectrum, axis=1)





    # start output dictionary
    dict_ = {}
    dict_['variables'] = {}
    dict_['dimensions'] = ('time', 'particle_fall_speed', 'particle_optical_diameter')

    attribute_list = [
        ('author', 'Luis Ackermann'),
        ('author email', 'ackermannluis@gmail.com'),
        ('version', '1'),
        ('time of file creation', time_seconds_to_str(time.time(), '%Y-%m-%d_%H:%M UTC')),
        ('data source', 'parsivel-2 disdrometer, from custom acquisition software'),
        ('custom acquisition software source', 'https://github.com/ackermannluis/parsivel2_datalogger'),
        ('sensor serial number', dict_raw_lists['sensor_serial_number'][0]),
    ]
    dict_['attributes'] = attribute_list

    # ############################   dimensions   # ############################
    # ############################
    variable_name = 'time'
    day_time_str = time_seconds_to_str(0, '%Y-%m-%d_%H:%M:%S UTC')
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'seconds since ' + day_time_str),
        ('description', 'time stamp is at end of average period')]
    dict_['variables'][variable_name]['data'] = time_arr

    # ############################
    variable_name = 'particle_fall_speed'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('particle_fall_speed',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'm s-1'),
        ('description', 'speed at which the particle is falling. Directly measured by parsivel')]
    dict_['variables'][variable_name]['data'] = speed_scale

    # ############################
    variable_name = 'particle_optical_diameter'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('particle_optical_diameter',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'center of bin size of the effective optical diameter of particles. '
                        'Directly measured by parsivel')]
    dict_['variables'][variable_name]['data'] = size_scale

    # ############################   variables   # ############################

    # ############################
    variable_name = 'datetime'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'YYYY-mm-dd_HH:MM:SS'),
        ('description', 'string with time in YYYY-mm-dd_HH:MM:SS format')]
    dict_['variables'][variable_name]['data'] = np.array(dict_raw_lists[variable_name], dtype=str)

    # ############################
    variable_name = 'particle_count_spectrum'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time', 'particle_fall_speed', 'particle_optical_diameter')
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'particles per minute'),
        ('description', 'number of particles observed during the minute for each speed and size bin')]
    spectrum_array[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = spectrum_array

    # ############################
    variable_name = 'particle_concentration_spectrum'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time', 'particle_fall_speed', 'particle_optical_diameter')
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'particles per m3'),
        ('description', 'concentration of particles observed during the minute for each speed and size bin')]
    particle_concentration_spectrum[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = particle_concentration_spectrum

    # ############################
    variable_name = 'particle_concentration_total'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'particles per m3'),
        ('description', 'sum of concentration of particles observed during the minute')]
    particle_concentration_total[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = particle_concentration_total

    # ############################
    variable_name = 'rain_intensity'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'mm hr-1'),
        ('description', 'rain intensity of the last minute in millimeters per hour')]
    rain_intensity = np.array(dict_raw_lists['rain_intensity_mm/hr'], dtype=float)
    rain_intensity[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = rain_intensity

    # ############################
    variable_name = 'rain_accumulated'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'rain accumulated since restart of instrument')]
    rain_accumulated = np.array(dict_raw_lists['rain_accumulated_mm'], dtype=float)
    rain_accumulated[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = rain_accumulated

    # ############################
    variable_name = 'weather_code_METAR'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'flag string'),
        ('description', 'type of precipitation flagged using METAR codes. '
                        'see function "parsivel_convert_METAR_code_to_numbers" in '
                        'https://github.com/ackermannluis/AtmSciTools for further details')]
    dict_['variables'][variable_name]['data'] = np.array(dict_raw_lists['weather_code_METAR'], dtype=str)

    # ############################
    variable_name = 'weather_code_SYNOP'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'flag int'),
        ('description', 'type of precipitation flagged using SYNOP codes')]
    dict_['variables'][variable_name]['data'] = np.array(dict_raw_lists['weather_code_SYNOP'], dtype=int)

    # ############################
    variable_name = 'hydrometeor_type'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'flag int'),
        ('description', '0=no precip, 1=rain, 2=freezing rain, 3=mix, 4=frozen')]
    dict_['variables'][variable_name]['data'] = hydrometeor_type

    # ############################
    variable_name = 'radar_reflectivity'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'dBz'),
        ('description', 'radar reflectivity derived from the particle size distribution')]
    radar_reflectivity = np.array(dict_raw_lists['radar_reflectivity_dBz'], dtype=float)
    radar_reflectivity[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = radar_reflectivity

    # ############################
    variable_name = 'MOR_visibility'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'meters'),
        ('description', 'Meteorological Optical Range')]
    MOR_visibility = np.array(dict_raw_lists['MOR_visibility_m'], dtype=float)
    MOR_visibility[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = MOR_visibility

    # ############################
    variable_name = 'number_of_particles_detected'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'counts per minute'),
        ('description', 'total number of particles detected in last minute')]
    number_of_particles_detected = np.array(dict_raw_lists['number_of_particles_detected'], dtype=float)
    number_of_particles_detected[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = number_of_particles_detected

    # ############################
    variable_name = 'sensor_temperature'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'celsius'),
        ('description', 'temperature of the sensor. Course measurement, not equal to ambient temperature')]
    dict_['variables'][variable_name]['data'] = np.array(dict_raw_lists['sensor_temperature'], dtype=int)

    # ############################
    variable_name = 'power_supply_voltage'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'volts'),
        ('description', 'voltage of the power supply for the instrument')]
    dict_['variables'][variable_name]['data'] = np.array(dict_raw_lists['power_supply_voltage_V'], dtype=float)

    # ############################
    variable_name = 'sensor_status'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'flag int'),
        ('description', 'error flag regarding the status of the instrument, 0 means all good, 1 means warning, '
                        '2 means needs cleaning bad data, 3 means full error')]
    dict_['variables'][variable_name]['data'] = np.array(dict_raw_lists['sensor_status'], dtype=int)

    # ############################
    variable_name = 'kinetic_energy'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'J m-2 h-1'),
        ('description', 'total kinetic energy of hydrometeors')]
    kinetic_energy = np.array(dict_raw_lists['kinetic_energy_J/m2h'], dtype=float)
    kinetic_energy[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = kinetic_energy

    # ############################
    variable_name = 'snow_intensity'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time',)
    dict_['variables'][variable_name]['attributes'] = [
        ('units', ' mm hr-1'),
        ('description', 'estimate of equivalent liquid volume of snow precipitation rate')]
    snow_intensity = np.array(dict_raw_lists['snow_intensity_mm/h'], dtype=float)
    snow_intensity[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = snow_intensity

    # ############################
    variable_name = 'PSD'
    dict_['variables'][variable_name] = {}
    dict_['variables'][variable_name]['dimensions'] = ('time', 'particle_optical_diameter')
    dict_['variables'][variable_name]['attributes'] = [
        ('units', 'particles per m3'),
        ('description', 'sum of concentration of particles at different speeds as a function of optical diameter.')]
    PSD_array[mask_] = np.nan  # mask bad data
    dict_['variables'][variable_name]['data'] = PSD_array


    save_dictionary_to_netcdf(dict_, filename_output_nc)
def create_DSD_plot(DSD_arr, time_parsivel_seconds, size_arr, events_period_str, figfilename='',
                    output_data=False, x_range=(0, 7.5), y_range=(-1, 3.1), figsize_=(5, 5)):
    size_series = size_arr[0, :]

    event_row_start = time_to_row_str(time_parsivel_seconds, events_period_str.split('_')[0])
    event_row_stop_ = time_to_row_str(time_parsivel_seconds, events_period_str.split('_')[1])

    # normalize
    DSD_arr_over_D = DSD_arr / size_arr

    DSD_arr_over_D_by_D = np.sum(DSD_arr_over_D, axis=1)

    DSD_arr_over_D_by_D_no_zero = DSD_arr_over_D_by_D * 1
    DSD_arr_over_D_by_D_no_zero[DSD_arr_over_D_by_D_no_zero == 0] = np.nan

    DSD_arr_over_D_by_D_log = np.log10(DSD_arr_over_D_by_D_no_zero)

    DSD_arr_over_D_by_D_log_event_1_bin = np.array(DSD_arr_over_D_by_D_log[event_row_start:event_row_stop_])

    DSD_arr_over_D_by_D_log_event_1_bin[~np.isnan(DSD_arr_over_D_by_D_log_event_1_bin)] = 1

    DSD_arr_over_D_by_D_log_event_1_bin_sum = np.nansum(DSD_arr_over_D_by_D_log_event_1_bin, axis=0)

    DSD_arr_over_D_by_D_log_event_1_meanbyD = np.nanmean(np.array(
        DSD_arr_over_D_by_D_log[event_row_start:event_row_stop_]), axis=0)

    DSD_arr_over_D_by_D_log_event_1_meanbyD[DSD_arr_over_D_by_D_log_event_1_bin_sum < 10] = np.nan

    fig, ax = plt.subplots(figsize=figsize_)
    ax.set_title('Mean value of drop concentrations in each diameter bin')
    ax.set_xlabel('D [mm]')
    ax.set_ylabel('log10 N(D) [m-3 mm-1]')
    ax.plot(size_series, DSD_arr_over_D_by_D_log_event_1_meanbyD, '-or', label='Event 1')
    ax.set_xlim(x_range)
    ax.set_ylim(y_range)
    ax.grid()
    if figfilename != '':
        fig.savefig(figfilename, transparent=True, bbox_inches='tight')
        plt.close(fig)
    if output_data:
        return size_series, DSD_arr_over_D_by_D_log_event_1_meanbyD
def parsivel_nc_format_V2(input_filename, output_filename):
    """
    Transform the not so good nc V1 version produced by save_parsivel_arrays_to_netcdf to V2
    :param input_filename: output from save_parsivel_arrays_to_netcdf
    :param output_filename: a path and filename
    :return:
    """
    # create file
    netcdf_output_file_object = nc.Dataset(output_filename, 'w')
    print('created new file')
    netcdf_first_file_object = nc.Dataset(input_filename)

    # create attributes
    netcdf_output_file_object.setncattr('author', 'Luis Ackermann (ackermannluis@gmail.com')
    netcdf_output_file_object.setncattr('version', 'V2')
    netcdf_output_file_object.setncattr('created', time_seconds_to_str(time.time(), '%Y-%m-%d_%H:%M UTC'))
    print('added attributes')

    # create list for dimensions and variables
    dimension_names_list = sorted(netcdf_first_file_object.dimensions)
    variable_names_list = sorted(netcdf_first_file_object.variables)

    # create dimensions
    for dim_name in dimension_names_list:
        if dim_name == 'time':
            netcdf_output_file_object.createDimension('time', size=0)
            print('time', 'dimension created')
        else:
            netcdf_output_file_object.createDimension(dim_name,
                                                      size=netcdf_first_file_object.dimensions[dim_name].size)
            print(dim_name, 'dimension created')

    # create variables
    # time
    var_name = 'time'
    netcdf_output_file_object.createVariable(var_name, 'int64', (var_name,), zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units',
                                                            'seconds since ' + time_seconds_to_str(0, time_format_mod))
    time_parsivel_seconds = time_str_to_seconds(np.array(netcdf_first_file_object.variables[var_name][:], dtype=str),
                                                time_format_parsivel)
    netcdf_output_file_object.variables[var_name][:] = np.array(time_parsivel_seconds, dtype='int64')
    print('created time variable')

    # time_YmdHM
    var_name = 'YYYYmmddHHMM'
    netcdf_output_file_object.createVariable(var_name, 'str', ('time',), zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'YYYYmmddHHMM in string type')
    netcdf_output_file_object.variables[var_name][:] = np.array(netcdf_first_file_object.variables['time'][:],
                                                                dtype=str)
    print('created time_YmdHM variable')

    # particle_fall_speed
    var_name = 'particles_spectrum'
    if var_name in variable_names_list:
        netcdf_output_file_object.createVariable(var_name,
                                                 netcdf_first_file_object.variables[var_name].dtype,
                                                 netcdf_first_file_object.variables[var_name].dimensions, zlib=True)
        netcdf_output_file_object.variables[var_name].setncattr('units', 'particle counts per bin per minute')
        netcdf_output_file_object.variables[var_name].setncattr('description',
                                                                'for each time stamp, the array varies with respect'
                                                                ' to fall speed on the y axis (rows) starting from the top'
                                                                ' and varies with respect to size on the x axis (columns) '
                                                                'starting from the left')
        netcdf_output_file_object.variables[var_name][:] = netcdf_first_file_object.variables[var_name][:].copy()
        print('created particles_spectrum variable')

        # particle_fall_speed
        var_name = 'particle_fall_speed'
        netcdf_output_file_object.createVariable(var_name,
                                                 netcdf_first_file_object.variables[var_name].dtype,
                                                 ('particle_fall_speed',), zlib=True)
        netcdf_output_file_object.variables[var_name].setncattr('units', 'm/s')
        netcdf_output_file_object.variables[var_name][:] = netcdf_first_file_object.variables[var_name][:, 0].copy()
        print('created particle_fall_speed variable')

        # particle_size
        var_name = 'particle_size'
        netcdf_output_file_object.createVariable(var_name,
                                                 netcdf_first_file_object.variables[var_name].dtype,
                                                 ('particle_size',), zlib=True)
        netcdf_output_file_object.variables[var_name].setncattr('units', 'mm')
        netcdf_output_file_object.variables[var_name][:] = netcdf_first_file_object.variables[var_name][0, :].copy()
        print('created particle_size variable')

    # precipitation_intensity
    var_name = 'precipitation_intensity'
    netcdf_output_file_object.createVariable(var_name,
                                             'float',
                                             netcdf_first_file_object.variables[
                                                 'Intensity of precipitation (mm|h)'].dimensions, zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'mm/h')
    netcdf_output_file_object.variables[var_name][:] = np.array(
        netcdf_first_file_object.variables['Intensity of precipitation (mm|h)'][:], dtype=float)
    print('created precipitation_intensity variable')

    # sensor_temperature
    var_name = 'sensor_temperature'
    netcdf_output_file_object.createVariable(var_name,
                                             'float',
                                             netcdf_first_file_object.variables[
                                                 'Temperature in sensor (°C)'].dimensions, zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'Celsius')
    netcdf_output_file_object.variables[var_name][:] = np.array(
        netcdf_first_file_object.variables['Temperature in sensor (°C)'][:], dtype=float)
    print('created sensor_temperature variable')

    # Weather_code_SYNOP_WaWa
    var_name = 'weather_code_SYNOP_WaWa'
    netcdf_output_file_object.createVariable(var_name,
                                             netcdf_first_file_object.variables['Weather code SYNOP WaWa'].dtype,
                                             netcdf_first_file_object.variables['Weather code SYNOP WaWa'].dimensions,
                                             zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'n/a')
    netcdf_output_file_object.variables[var_name][:] = \
        netcdf_first_file_object.variables['Weather code SYNOP WaWa'][:].copy()

    # Weather_code_SYNOP_WaWa
    var_name = 'weather_code_METAR_SPECI'
    netcdf_output_file_object.createVariable(var_name,
                                             netcdf_first_file_object.variables['Weather code METAR|SPECI'].dtype,
                                             netcdf_first_file_object.variables['Weather code METAR|SPECI'].dimensions,
                                             zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'n/a')
    netcdf_output_file_object.variables[var_name][:] = \
        netcdf_first_file_object.variables['Weather code METAR|SPECI'][:].copy()
    print('created weather_code_METAR_SPECI variable')

    # Weather_code_NWS
    var_name = 'weather_code_NWS'
    netcdf_output_file_object.createVariable(var_name,
                                             netcdf_first_file_object.variables['Weather code NWS'].dtype,
                                             netcdf_first_file_object.variables['Weather code NWS'].dimensions,
                                             zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'n/a')
    NWS_description = '''precip_type_dict = {
        'C': 'No Precip',
        'Kein Niederschlag': 'No Precip',
        'A': 'Hail',
        'L': 'Drizzle',
        'L+': 'heavy Drizzle',
        'L-': 'light Drizzle',
        'R': 'Rain',
        'R+': 'heavy Rain',
        'R-': 'light Rain',
        'RL': 'Drizzle and Rain',
        'RL+': 'heavy Drizzle and Rain',
        'RL-': 'light Drizzle and Rain',
        'RLS': 'Rain, Drizzle and Snow',
        'RLS+': 'heavy Rain, Drizzle and Snow',
        'RLS-': 'light Rain, Drizzle and Snow',
        'S': 'Snow',
        'S+': 'heavy Snow',
        'S-': 'light Snow',
        'SG': 'Snow Grains',
        'SP': 'Freezing Rain'
    }'''
    netcdf_output_file_object.variables[var_name].setncattr('description', NWS_description)
    netcdf_output_file_object.variables[var_name][:] = \
        netcdf_first_file_object.variables['Weather code NWS'][:].copy()
    print('created weather_code_NWS variable')

    # Radar_reflectivity (dBz)
    var_name = 'radar_reflectivity'
    netcdf_output_file_object.createVariable(var_name,
                                             'float',
                                             netcdf_first_file_object.variables['Radar reflectivity (dBz)'].dimensions,
                                             zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'dBz')
    netcdf_output_file_object.variables[var_name][:] = np.array(
        netcdf_first_file_object.variables['Radar reflectivity (dBz)'][:], dtype=float)
    print('created radar_reflectivity variable')

    # particle_count
    var_name = 'particle_count'
    netcdf_output_file_object.createVariable(var_name,
                                             'int64',
                                             netcdf_first_file_object.variables[
                                                 'Number of detected particles'].dimensions, zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', 'counts')
    netcdf_output_file_object.variables[var_name].setncattr('description', 'Number of detected particles per minute')
    netcdf_output_file_object.variables[var_name][:] = np.array(
        netcdf_first_file_object.variables['Number of detected particles'][:], dtype='int64')
    print('created particle_count variable')

    # particle_concentration_spectrum
    var_name = 'particle_concentration_spectrum'
    var_name_old = 'particle_concentration_spectrum_m-3'
    if var_name_old in variable_names_list:
        netcdf_output_file_object.createVariable(var_name,
                                                 netcdf_first_file_object.variables[var_name_old].dtype,
                                                 netcdf_first_file_object.variables[var_name_old].dimensions, zlib=True)
        netcdf_output_file_object.variables[var_name].setncattr('units', '1/m3')
        netcdf_output_file_object.variables[var_name].setncattr('description', 'particles per meter cube per class')
        netcdf_output_file_object.variables[var_name][:] = netcdf_first_file_object.variables[var_name_old][:].copy()
        print('created particle_concentration_spectrum variable')

        # N_total
        var_name = 'N_total'
        var_name_old = 'particle_concentration_total_m-3'
        netcdf_output_file_object.createVariable(var_name,
                                                 netcdf_first_file_object.variables[var_name_old].dtype,
                                                 netcdf_first_file_object.variables[var_name_old].dimensions, zlib=True)
        netcdf_output_file_object.variables[var_name].setncattr('units', '1/m3')
        netcdf_output_file_object.variables[var_name].setncattr('description', 'total particles per meter cube')
        netcdf_output_file_object.variables[var_name][:] = netcdf_first_file_object.variables[var_name_old][:].copy()
        print('created N_total variable')

        # psd
        var_name = 'psd'
        var_name_old = 'particle_concentration_spectrum_m-3'
        netcdf_output_file_object.createVariable(var_name,
                                                 'float',
                                                 ('time', 'particle_size',), zlib=True)
        netcdf_output_file_object.variables[var_name].setncattr('units', '1/m3')
        netcdf_output_file_object.variables[var_name].setncattr('description', 'particle size distribution, same as '
                                                                               'particle_concentration_spectrum but all speeds'
                                                                               'bins are summed, only varies with time and size')
        netcdf_output_file_object.variables[var_name][:] = np.sum(netcdf_first_file_object.variables[var_name_old][:],
                                                                  axis=1)
        print('created psd variable')

    # rain mask
    rain_only_list = ['R', 'R+', 'R-']
    RR_ = np.array(netcdf_first_file_object.variables['Intensity of precipitation (mm|h)'][:], dtype=float)
    NWS_ = netcdf_first_file_object.variables['Weather code NWS'][:].copy()
    rain_mask = np.zeros(RR_.shape[0], dtype=int) + 1
    for r_ in range(RR_.shape[0]):
        if RR_[r_] > 0 and NWS_[r_] in rain_only_list:
            rain_mask[r_] = 0
    var_name = 'rain_mask'
    netcdf_output_file_object.createVariable(var_name,
                                             'int',
                                             ('time',), zlib=True)
    netcdf_output_file_object.variables[var_name].setncattr('units', '0 if rain, 1 if not rain')
    netcdf_output_file_object.variables[var_name].setncattr('description', 'using the NWS code, only used R, R+ and R-')
    netcdf_output_file_object.variables[var_name][:] = rain_mask
    print('rain_mask')

    # close all files
    netcdf_output_file_object.close()
    netcdf_first_file_object.close()
def parsivel_sampling_volume(particle_size_2d, particle_fall_speed_2d):
    sampling_area = 0.18 * (0.03 - ((particle_size_2d/1000) / 2)) # m2
    sampling_time = 60 # seconds
    sampling_height = particle_fall_speed_2d * sampling_time # meters

    sampling_volume_2d = sampling_area * sampling_height # m3

    return sampling_volume_2d
def load_parsivel_txt_to_array(filename_, delimiter_=';'):
    # filename_ = 'C:/_input/parsivel_2018-07-26-00_2018-08-02-00_1.txt'

    size_scale = [0.062,0.187,0.312,0.437,0.562,0.687,0.812,0.937,1.062,1.187,1.375,1.625,1.875,
                  2.125,2.375,2.75,3.25,3.75,4.25,4.75,5.5,6.5,7.5,8.5,9.5,11,13,15,17,19,21.5,24.5]
    speed_scale = [0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.1,1.3,1.5,1.7,1.9,2.2,2.6,3,3.4,
                   3.8,4.4,5.2,6,6.8,7.6,8.8,10.4,12,13.6,15.2,17.6,20.8]

    speed_array = np.zeros((32,32), dtype=float)
    size_array = np.zeros((32, 32), dtype=float)

    for i in range(32):
        speed_array[:,i] = speed_scale
        size_array[i, :] = size_scale

    # read parsivel file
    spectrum_array_list = []
    data_array_list = []

    with open(filename_,encoding='latin1') as file_object:
        header_ = file_object.readline().split(delimiter_)
        line_str = file_object.readline()
        line_split = np.array(line_str.split(delimiter_))
        if len(line_split) == 17:
            line_split[16] = '0'
            data_array_list.append(line_split[:-1])
            spectrum_array_list.append(np.zeros((32,32)))
        elif len(line_split) > 17:
            line_split[16] = '0'
            data_array_list.append(line_split[:16])
            line_split[line_split == ''] = '0'
            spectrum_array_list.append(np.array(line_split[16:-1]).reshape((32, 32)))
        elif len(line_split) == 16:
            data_array_list.append(line_split[:-1])
            spectrum_array_list.append(np.zeros((32,32)))

        for line in file_object:
            line_split = np.array(line.split(delimiter_))
            if len(line_split) == 17:
                line_split[16] = '0'
                data_array_list.append(line_split[:-1])
                spectrum_array_list.append(np.zeros((32, 32)))
            elif len(line_split) > 17:
                line_split[16] = '0'
                data_array_list.append(line_split[:16])
                line_split[line_split == ''] = '0'
                spectrum_array_list.append(np.array(line_split[16:-1]).reshape((32, 32)))
            elif len(line_split) == 16:
                if line_split[0] != 'Date':
                    data_array_list.append(line_split[:-1])
                    spectrum_array_list.append(np.zeros((32, 32)))

    data_array = np.stack(data_array_list)
    spectrum_array = np.stack(spectrum_array_list).astype(float)
    t_list = []
    for t_ in range(data_array.shape[0]):
        t_list.append(data_array[t_][0] + '  ' + data_array[t_][1])

    if len(header_) == 16:
        # no spectra was set to record
        return data_array, None, t_list, size_array, speed_array, header_
    else:
        return data_array, spectrum_array, t_list, size_array, speed_array, header_

def save_parsivel_arrays_to_netcdf(raw_spectra_filename, nedcdf_output_filename,
                                   delimiter_=';', raw_time_format='%d.%m.%Y %H:%M:%S'):
    # save_parsivel_arrays_to_netcdf('C:/_input/parsivel_2018-07-26-00_2018-08-02-00_1.txt', 'C:/_input/parsivel_compiled_3.nc')

    print('reading txt to array')
    data_array, spectrum_array, t_list, size_array, speed_array, header_ = \
        load_parsivel_txt_to_array(raw_spectra_filename, delimiter_=delimiter_)
    print('arrays created')

    file_attributes_tuple_list = [('Compiled by', 'Luis Ackermann @: '  + str(datetime.now())),
                                  ('Data source', 'Parsivel Disdrometer'),
                                  ('time format', 'YYYYMMDDHHmm in uint64 data type, each ' +
                                                  'time stamp is the acumulated precip for one minute')]

    # time from str to int
    time_array = np.zeros(data_array.shape[0], dtype='<U12')
    # for t_ in range(data_array.shape[0]):
    #     time_array[t_] = int(t_list[t_][6:10] + # YYYY
    #                            t_list[t_][3:5] + # MM
    #                            t_list[t_][:2] + # DD
    #                            t_list[t_][12:14] + # HH
    #                            t_list[t_][15:17]) # mm
    for t_ in range(data_array.shape[0]):
        time_array[t_] = int(time_seconds_to_str(time_str_to_seconds(t_list[t_],raw_time_format),
                                                time_format_parsivel))


    pollutant_attributes_tuple_list = [('units', 'particles per minute')]

    # create output file
    file_object_nc4 = nc.Dataset(nedcdf_output_filename,'w')#,format='NETCDF4_CLASSIC')
    print('output file started')

    # create dimensions
    file_object_nc4.createDimension('particle_fall_speed', speed_array.shape[0])
    file_object_nc4.createDimension('particle_size', size_array.shape[1])
    file_object_nc4.createDimension('time', time_array.shape[0])


    # create dimension variables
    file_object_nc4.createVariable('particle_fall_speed', 'f4', ('particle_fall_speed','particle_size',), zlib=True)
    file_object_nc4.createVariable('particle_size', 'f4', ('particle_fall_speed','particle_size',), zlib=True)
    file_object_nc4.createVariable('time', 'u8', ('time',), zlib=True)


    # populate dimension variables
    file_object_nc4.variables['time'][:] = time_array[:]
    file_object_nc4.variables['particle_fall_speed'][:] = speed_array[:]
    file_object_nc4.variables['particle_size'][:] = size_array[:]


    # create particles_spectrum array
    if spectrum_array is not None:
        file_object_nc4.createVariable('particles_spectrum', 'u2',
                                       ('time', 'particle_fall_speed', 'particle_size',), zlib=True)

        # populate
        file_object_nc4.variables['particles_spectrum'][:] = spectrum_array[:]


        # create particle_concentration_spectrum_m-3
        # get sampling volume
        sampling_volume_2d = parsivel_sampling_volume(size_array, speed_array)
        particle_concentration_spectrum = spectrum_array / sampling_volume_2d
        # create variable
        file_object_nc4.createVariable('particle_concentration_spectrum_m-3', 'float32',
                                       ('time', 'particle_fall_speed', 'particle_size',), zlib=True)
        # populate
        file_object_nc4.variables['particle_concentration_spectrum_m-3'][:] = particle_concentration_spectrum[:]

        # create particle_concentration_total_m-3
        particle_concentration_total = np.nansum(np.nansum(particle_concentration_spectrum, axis=-1), axis=-1)
        # create variable
        file_object_nc4.createVariable('particle_concentration_total_m-3', 'float32',
                                       ('time', ), zlib=True)
        # populate
        file_object_nc4.variables['particle_concentration_total_m-3'][:] = particle_concentration_total[:]

        for attribute_ in pollutant_attributes_tuple_list:
            setattr(file_object_nc4.variables['particles_spectrum'], attribute_[0], attribute_[1])

    # create other data variables
    for i_, head_ in enumerate(header_[:-1]):
        var_name = head_.replace('/','|')
        print('storing var name: ' , var_name)
        temp_ref = file_object_nc4.createVariable(var_name, str, ('time',), zlib=True)
        temp_ref[:] = data_array[:, i_]


    for attribute_ in file_attributes_tuple_list:
        setattr(file_object_nc4, attribute_[0], attribute_[1])



    file_object_nc4.close()

    print('Done!')
def load_parsivel_from_nc(netcdf_filename):
    netcdf_file_object = nc.Dataset(netcdf_filename, 'r')
    file_var_values_dict = {}

    variable_name_list = netcdf_file_object.variables.keys()

    for var_ in variable_name_list:
        file_var_values_dict[var_] = netcdf_file_object.variables[var_][:].copy()

    netcdf_file_object.close()
    return file_var_values_dict, variable_name_list
def parsivel_plot_spectrum_counts(arr_, title_='', x_range_tuple=(0, 6), y_range_tuple=(0, 10), save_filename=None,
                                  contourF=False, bins_=(0,2,5,10,20,50,100,200), fig_size=(5,5)):
    cmap_parsivel = ListedColormap(['white', 'yellow', 'orange', 'lime', 'darkgreen',
                                    'aqua', 'purple', 'navy', 'red'], 'indexed')

    size_scale = [0.062,0.187,0.312,0.437,0.562,0.687,0.812,0.937,1.062,1.187,1.375,1.625,1.875,
                  2.125,2.375,2.75,3.25,3.75,4.25,4.75,5.5,6.5,7.5,8.5,9.5,11,13,15,17,19,21.5,24.5]
    speed_scale = [0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.1,1.3,1.5,1.7,1.9,2.2,2.6,3,3.4,
                   3.8,4.4,5.2,6,6.8,7.6,8.8,10.4,12,13.6,15.2,17.6,20.8]

    speed_array = np.zeros((32,32), dtype=float)
    size_array = np.zeros((32, 32), dtype=float)


    radious_arr = np.linspace(0.01,3,100)
    U_t = calculate_liquid_water_terminal_velocity(radious_arr)

    for i in range(32):
        speed_array[:,i] = speed_scale
        size_array[i, :] = size_scale

    spectrum_array_color = np.zeros((arr_.shape[0], arr_.shape[1]), dtype=float)
    bin_labels = []
    i_ = 0
    for i_, bin_ in enumerate(bins_):
        spectrum_array_color[arr_ > bin_] = i_ + 1
        bin_labels.append(str(bin_))
    bin_labels[i_] = '>' + bin_labels[i_]

    fig, ax = plt.subplots(figsize=fig_size)
    if contourF:
        quad1 = ax.contourf(size_array, speed_array, spectrum_array_color, cmap=cmap_parsivel,
                              vmin=0, vmax=8)
    else:
        quad1 = ax.pcolormesh(size_array, speed_array, spectrum_array_color, cmap=cmap_parsivel,
                              vmin=0, vmax=8)

    ax.set_ylim(y_range_tuple)
    ax.set_xlim(x_range_tuple)

    ax.set_xlabel('particle size [mm]')
    ax.set_ylabel('particle speed [m/s]')
    ax.set_title(title_)
    cbar_label = 'Particles per bin'

    cb2 = fig.colorbar(quad1)#, ticks=[0,1,2,3,4,5,6,7])
    ticks_ = np.linspace(0.5, i_+0.5, len(bins_))
    cb2.set_ticks(ticks_)
    cb2.set_ticklabels(bin_labels)
    cb2.ax.set_ylabel(cbar_label)


    o_ = p_plot(radious_arr, U_t, c_='black', add_line=True, S_=1, fig_ax=(fig,ax))


    if save_filename is None:
        plt.show()
    else:
        fig.savefig(save_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
    return fig, ax
def parsivel_plot_spectrum_DSD(arr_, title_='', x_range_tuple=(0, 6), y_range_tuple=(0, 10), save_filename=None,
                               contourF=False, fig_size=(5,5), cmap_=default_cm, cbar_label='PSD [m$^-$$^3$]',
                               x_header='particle size [mm]', y_header='particle speed [m s$^-$$^1$]',
                               nozeros_=True, vmin_=None, vmax_=None, fig_ax=None, show_cbar=True, cbar_ax=None,
                               show_GunnKinzer_line=True):

    size_scale = [0.062,0.187,0.312,0.437,0.562,0.687,0.812,0.937,1.062,1.187,1.375,1.625,1.875,
                  2.125,2.375,2.75,3.25,3.75,4.25,4.75,5.5,6.5,7.5,8.5,9.5,11,13,15,17,19,21.5,24.5]
    speed_scale = [0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.1,1.3,1.5,1.7,1.9,2.2,2.6,3,3.4,
                   3.8,4.4,5.2,6,6.8,7.6,8.8,10.4,12,13.6,15.2,17.6,20.8]

    speed_array = np.zeros((32,32), dtype=float)
    size_array = np.zeros((32, 32), dtype=float)

    for i in range(32):
        speed_array[:,i] = speed_scale
        size_array[i, :] = size_scale

    radious_arr = np.linspace(0.01,3,100)
    U_t = calculate_liquid_water_terminal_velocity(radious_arr)

    if nozeros_:
        arr_ = np.array(arr_, dtype=float)
        arr_[arr_ == 0] = np.nan

    if fig_ax is None:
        fig, ax = plt.subplots(figsize=fig_size)
    else:
        fig, ax =fig_ax

    if contourF:
        quad1 = ax.contourf(size_array, speed_array, arr_, cmap=cmap_, vmin=vmin_, vmax=vmax_)
    else:
        quad1 = ax.pcolormesh(size_array, speed_array, arr_, cmap=cmap_, vmin=vmin_, vmax=vmax_)

    ax.set_ylim(y_range_tuple)
    ax.set_xlim(x_range_tuple)

    ax.set_xlabel(x_header)
    ax.set_ylabel(y_header)
    ax.set_title(title_)

    if show_cbar:
        if cbar_ax is None:
            color_bar = fig.colorbar(quad1,  )
        else:
            color_bar = fig.colorbar(quad1, cax=cbar_ax, )

        color_bar.ax.set_ylabel(cbar_label)

    if show_GunnKinzer_line:
        o_ = p_plot(radious_arr, U_t, c_='black', add_line=True, S_=1, fig_ax=(fig,ax), title_str=title_)


    if save_filename is None:
        plt.show()
    else:
        fig.savefig(save_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
    return fig, ax
def parsivel_calculate_percentage_precip_type(rain_rate_array, precipitation_type_number, fig_ax=None,
                                              y_header='Total contribution [%]', label_rot=0,
                                              figure_filename=None, show_figure=True, figsize_=(5,3),
                                              labels_=('Rain', 'SLW', 'Mixed', 'Frozen')):
    # calculate percentage of precip type
    precip_subset_sums_list = np.zeros(4)  # rain, SLW, mix, frozen

    RR_, Ty_ = coincidence(rain_rate_array, precipitation_type_number)

    for r_ in range(RR_.shape[0]):
        if RR_[r_] == 0:
            continue
        else:
            if Ty_[r_] == 1:
                precip_subset_sums_list[0] += RR_[r_]
                continue
            elif Ty_[r_] == 2:
                precip_subset_sums_list[1] += RR_[r_]
                continue
            elif Ty_[r_] == 3:
                precip_subset_sums_list[2] += RR_[r_]
                continue
            elif Ty_[r_] == 4:
                precip_subset_sums_list[3] += RR_[r_]
                continue
            else:
                precip_subset_sums_list[2] += rain_rate_array[r_]

    precip_type_percent_array = 100 * precip_subset_sums_list / np.nansum(precip_subset_sums_list)

    if show_figure:
        if fig_ax is not None:
            fig, ax = fig_ax
        else:
            fig, ax = plt.subplots(figsize=figsize_)
        ax.bar(np.arange(4), precip_type_percent_array, color=['red', 'green', 'yellow', 'blue'],
               tick_label=labels_, align='center')
        ax.set_xticklabels(labels_, rotation = label_rot)

        if y_header is not None: ax.set_ylabel(y_header)
        ax.set_ylim((0, 100))
        ax.grid()

        if figure_filename is not None:
            fig.savefig(figure_filename , transparent=True, bbox_inches='tight')
            plt.close(fig)

    return precip_type_percent_array, precip_subset_sums_list
def parsivel_convert_NWS_code_to_numbers(precipitation_rate_array, weather_code_NWS_array):
    """
    SHOULD NOT BE USED, ERROR FOUND, USE parsivel_convert_METAR_code_to_numbers INSTEAD
    creates an array with a phase number by grouping similar NWS flags into broad classes
    (0=no precip, 1=rain, 2=freezing rain, 3=mix, 4=snow, 5=hail or graupel)
    :param precipitation_rate_array: 1d array with precipitation rate data (mm/hr)
    :param weather_code_NWS_array: 1d array or list (same size as precipitation_rate_array) with NWS codes from PARSIVEL
    :return: 1d array with integers between [0 and 5], same size as precipitation_rate_array
    """
    precip_type_dict = {
        'C': 'No Precip',
        'Kein Niederschlag': 'No Precip',
        'A': 'Hail',
        'L': 'Drizzle',
        'L+': 'heavy Drizzle',
        'L-': 'light Drizzle',
        'R': 'Rain',
        'R+': 'heavy Rain',
        'R-': 'light Rain',
        'RL': 'Drizzle and Rain',
        'RL+': 'heavy Drizzle and Rain',
        'RL-': 'light Drizzle and Rain',
        'RLS': 'Rain, Drizzle and Snow',
        'RLS+': 'heavy Rain, Drizzle and Snow',
        'RLS-': 'light Rain, Drizzle and Snow',
        'S': 'Snow',
        'S+': 'heavy Snow',
        'S-': 'light Snow',
        'SG': 'Snow Grains',
        'SP': 'Freezing Rain'
    }
    rain_list = [
        'L',
        'L+',
        'L-',
        'R',
        'R+',
        'R-',
        'RL',
        'RL+',
        'RL-'
    ]
    SLW_list = ['SP']
    mix_list = [
        'RLS',
        'RLS+',
        'RLS-'
    ]
    snow_list = [
        'S',
        'S+',
        'S-',
    ]
    hail_list = [
        'A',
        'SG'
    ]
    print('SHOULD NOT BE USED, ERROR FOUND, USE parsivel_convert_METAR_code_to_numbers INSTEAD')
    precip_type_array = np.zeros(precipitation_rate_array.shape[0], dtype=int)  # rain, SLW, mix, snow, hail
    for r_ in range(precipitation_rate_array.shape[0]):
        if precipitation_rate_array[r_] == 0:
            pass
        else:
            if weather_code_NWS_array[r_] in rain_list:
                precip_type_array[r_] = 1
                continue
            elif weather_code_NWS_array[r_] in SLW_list:
                precip_type_array[r_] = 2
                continue
            elif weather_code_NWS_array[r_] in mix_list:
                precip_type_array[r_] = 3
                continue
            elif weather_code_NWS_array[r_] in snow_list:
                precip_type_array[r_] = 4
                continue
            elif weather_code_NWS_array[r_] in hail_list:
                precip_type_array[r_] = 5
                continue
            else:
                precip_type_array[r_] = 3
    return precip_type_array
def parsivel_convert_METAR_code_to_numbers(precipitation_rate_array, weather_code_METAR_array):
    """
    creates an array with a phase number by grouping similar NWS flags into broad classes
    (0=no precip, 1=rain, 2=freezing rain, 3=mix, 4=snow)
    :param precipitation_rate_array: 1d array with precipitation rate data (mm/hr)
    :param weather_code_METAR_array: 1d array or list (same size as precipitation_rate_array) with NWS codes from PARSIVEL
    :return: 1d array with integers between [0 and 5], same size as precipitation_rate_array
    """
    rain_list = [
        'RA',
        '-RA',
        '+RA',
        'DZ',
        '+DZ',
        '-DZ',
        '-RADZ',
        '+RADZ',
    ]
    SLW_list = ['FZ']
    mix_list = [
        '+RASN',
        '-RASN',
    ]
    snow_list = [
        'SN',
        '+SN',
        '-SN',
        '+GS',
        '-GS',
        'GR'
    ]

    precip_type_array = np.zeros(precipitation_rate_array.shape[0], dtype=int)  # none, rain, SLW, mix, snow, graupel, hail
    for r_ in range(precipitation_rate_array.shape[0]):
        if precipitation_rate_array[r_] == 0:
            pass
        else:
            if weather_code_METAR_array[r_] in rain_list:
                precip_type_array[r_] = 1
                continue
            elif weather_code_METAR_array[r_] in SLW_list:
                precip_type_array[r_] = 2
                continue
            elif weather_code_METAR_array[r_] in mix_list:
                precip_type_array[r_] = 3
                continue
            elif weather_code_METAR_array[r_] in snow_list:
                precip_type_array[r_] = 4
                continue
            else:
                precip_type_array[r_] = 3
    return precip_type_array
def parsivel_estimate_rimed_ratio(PSD_array, precip_type_array):
    """
    estimates the ratio of rimed snow from the particle size distribution spectra (which includes particle fall speed)
    and the type of precipitation (which flags as 4 frozen hydrometeors).
    This algorithm assumes that all particles falling faster than 0.85 m/w are rimed, and all falling at or below
    0.85 m/s are un-rimed. This assumption can overestimate un-rimed ratio if all particles are very small.
    To perform the estimation, the maximum and minimum density of rimed snow is assumed to be 0.4 and 0.6 (*1e-6 kg/m3)
    and the density of un-rimed snow is assumed to be 0.3 * 10**-6 kg/m3. All particles are assumed to be spherical
    to calculate mass per spectral bin from the effective diameter.
    :param PSD_array: 3D array with the dimensions time, fall speed, size. Particles count per m3
    :param precip_type_array: 1D array with same time dimension as PSD_array, with integer flags. 4 = frozen
    :return: [1D array with estimated rimed_to_total_ratio, 1D array with max ratio bound, 1D array with min ratio bound]
    """
    # den_unrimed_snow = 0.3  *  1e-6
    # den_graupel_min = 0.4  *  1e-6
    # den_graupel_max = 0.6  *  1e-6


    size_scale = np.array([0.062,0.187,0.312,0.437,0.562,0.687,0.812,0.937,1.062,1.187,1.375,1.625,1.875,
                           2.125,2.375,2.75,3.25,3.75,4.25,4.75,5.5,6.5,7.5,8.5,9.5,11,13,15,17,19,21.5,24.5])

    speed_scale = [0.05,0.15,0.25,0.35,0.45,0.55,0.65,0.75,0.85,0.95,1.1,1.3,1.5,1.7,1.9,2.2,2.6,3,3.4,
                   3.8,4.4,5.2,6,6.8,7.6,8.8,10.4,12,13.6,15.2,17.6,20.8]


    snow_mask    = precip_type_array * np.nan
    snow_mask[precip_type_array==4] = 1


    # create MIN rimed fraction
    den_rimed   = 0.4  *  1e-6
    den_unrimed = 0.3  *  1e-6


    # rimed imbedded in the snow class
    rimed_total_V_sum = np.nansum(((PSD_array.T * snow_mask).T)[:,8:,:], axis=1)
    rimed_total_V_sum_volumes = rimed_total_V_sum * ((4/3) * np.pi * ((size_scale*0.001)**3))
    rimed_total_V_sum_mass = np.nansum(rimed_total_V_sum_volumes * den_rimed, axis=-1)

    unrimed_total_V_sum = np.nansum(((PSD_array.T * snow_mask).T)[:,:8,:], axis=1)
    unrimed_total_V_sum_volumes = unrimed_total_V_sum * ((4/3) * np.pi * ((size_scale*0.001)**3))
    unrimed_total_V_sum_mass = np.nansum(unrimed_total_V_sum_volumes * den_unrimed, axis=-1)

    total_mass = unrimed_total_V_sum_mass + rimed_total_V_sum_mass
    min_rimed_ratio = rimed_total_V_sum_mass  / total_mass


    # create MAX rimed fraction
    den_rimed   = 0.6  *  1e-6
    den_unrimed = 0.3  *  1e-6


    # rimed imbedded in the snow class
    rimed_total_V_sum = np.nansum(((PSD_array.T * snow_mask).T)[:,8:,:], axis=1)
    rimed_total_V_sum_volumes = rimed_total_V_sum * ((4/3) * np.pi * ((size_scale*0.001)**3))
    rimed_total_V_sum_mass = np.nansum(rimed_total_V_sum_volumes * den_rimed, axis=-1)

    unrimed_total_V_sum = np.nansum(((PSD_array.T * snow_mask).T)[:,:8,:], axis=1)
    unrimed_total_V_sum_volumes = unrimed_total_V_sum * ((4/3) * np.pi * ((size_scale*0.001)**3))
    unrimed_total_V_sum_mass = np.nansum(unrimed_total_V_sum_volumes * den_unrimed, axis=-1)

    total_mass = unrimed_total_V_sum_mass + rimed_total_V_sum_mass
    max_rimed_ratio = rimed_total_V_sum_mass  / total_mass


    # mid_rimed_ratio
    mid_rimed_ratio = (max_rimed_ratio + min_rimed_ratio) / 2


    return mid_rimed_ratio, max_rimed_ratio, min_rimed_ratio
def calculate_cumulative_precipitation_parsivel(parsivel_precipitation_mm_per_hour, parsivel_time_sec, time_period_str):
    return np.nansum(
        parsivel_precipitation_mm_per_hour[time_to_row_str(parsivel_time_sec, time_period_str.split('_')[0]):
                                           time_to_row_str(parsivel_time_sec, time_period_str.split('_')[1])]) / 60
def calculate_D_m(N_D, D_series):
    D_grad = np.gradient(D_series)
    D_m = np.nansum((N_D * (D_series**4) * D_grad))  /  np.nansum((N_D * (D_series ** 3) * D_grad))
    return D_m
def calculate_LWC(N_D, D_series):
    D_grad = np.gradient(D_series)
    water_density = 1E6 # g/m3
    LWC_ = (np.pi * water_density / 6) *  np.nansum((N_D * (D_series**3) * D_grad))
    return LWC_
def calculate_liquid_water_terminal_velocity_empirical(diameter_arr_mm):
    fall_speed_m_per_s = 10.5 - 11 * np.exp(-4.5 * (diameter_arr_mm / 10.))

    slope_small_drops = .387 / .187
    fall_speed_m_per_s_small_drops = slope_small_drops * diameter_arr_mm

    fall_speed_m_per_s[fall_speed_m_per_s<0]=fall_speed_m_per_s_small_drops[fall_speed_m_per_s<0]
    return fall_speed_m_per_s
def calculate_liquid_water_terminal_velocity_empirical_min(diameter_arr_mm):
    fall_speed_m_per_s = 6 - 9 * np.exp(-4 * (diameter_arr_mm / 10.))
    fall_speed_m_per_s[fall_speed_m_per_s<0]=0
    return fall_speed_m_per_s
def calculate_liquid_water_terminal_velocity_empirical_max(diameter_arr_mm):
    fall_speed_m_per_s = 12 - 10.3 * np.exp(-9 * (diameter_arr_mm / 10.))
    fall_speed_m_per_s[fall_speed_m_per_s<0]=0
    return fall_speed_m_per_s
def calculate_volume_of_oblate_liquid_drop(maximum_horizontal_diameter_mm):
    def get_axis_ratio_for_drop_diameters(maximum_horizontal_diameter_mm):
        def b_a_f_low(d):
            """
            for d [0, 1.25)
            """
            return -.016 * d + 1
        def b_a_f_mid(d):
            """
            for d [1.25, 9.25]
            """
            return -0.06574 * d + 1.057
        def b_a_f_high(d):
            """
            for d (9.25, 12.52]
            """
            b_a_f_high = (2.55595364e-05 * d ** 4 - 1.92677045e-03 * d ** 3 + 5.18238620e-02 * d ** 2
                          - 5.92248004e-01 * d + 2.8308484700798413)
            return b_a_f_high
        def b_a_f_end(d):
            """
            for d (12.52, infinity)
            """
            return np.zeros(len(d)) + 0.386

        b_a_f_l = b_a_f_low(maximum_horizontal_diameter_mm)
        b_a_f_m = b_a_f_mid(maximum_horizontal_diameter_mm)
        b_a_f_h = b_a_f_high(maximum_horizontal_diameter_mm)
        b_a_f_e = b_a_f_end(maximum_horizontal_diameter_mm)
        mask_l = np.logical_and(0 <= maximum_horizontal_diameter_mm, maximum_horizontal_diameter_mm < 1.25)
        mask_m = np.logical_and(1.25 <= maximum_horizontal_diameter_mm, maximum_horizontal_diameter_mm <= 9.25)
        mask_h = np.logical_and(9.25 < maximum_horizontal_diameter_mm, maximum_horizontal_diameter_mm <= 12.52)
        mask_e = 12.52 < maximum_horizontal_diameter_mm
        b_a_f = np.zeros(len(maximum_horizontal_diameter_mm))

        b_a_f[mask_l] = b_a_f_l[mask_l]
        b_a_f[mask_m] = b_a_f_m[mask_m]
        b_a_f[mask_h] = b_a_f_h[mask_h]
        b_a_f[mask_e] = b_a_f_e[mask_e]
        return b_a_f

    b_a = get_axis_ratio_for_drop_diameters(maximum_horizontal_diameter_mm)

    b_ = maximum_horizontal_diameter_mm * b_a

    volume_mm3 = (4/3) * np.pi * ((maximum_horizontal_diameter_mm/2)**2) * (b_/2)

    return volume_mm3
def calculate_volume_of_sphere(diameter_mm):
    volume_mm3 = (4 / 3) * np.pi * ((diameter_mm / 2) ** 3)
    return volume_mm3
def parsivel_plot_spectrum_counts_new(spectrum_array, title_str=None):
    size_scale = [0.062, 0.187, 0.312, 0.437, 0.562, 0.687, 0.812, 0.937, 1.062, 1.187, 1.375, 1.625, 1.875,
                  2.125, 2.375, 2.75, 3.25, 3.75, 4.25, 4.75, 5.5, 6.5, 7.5, 8.5, 9.5, 11, 13, 15, 17, 19, 21.5, 24.5]
    speed_scale = [0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95, 1.1, 1.3, 1.5, 1.7, 1.9, 2.2, 2.6, 3,
                   3.4,
                   3.8, 4.4, 5.2, 6, 6.8, 7.6, 8.8, 10.4, 12, 13.6, 15.2, 17.6, 20.8]

    speed_array = np.zeros((32, 32), dtype=float)
    size_array = np.zeros((32, 32), dtype=float)

    size_scale_line = np.linspace(0, 25, 100)
    U_t = calculate_liquid_water_terminal_velocity_empirical(size_scale_line)

    for i in range(32):
        speed_array[:, i] = speed_scale
        size_array[i, :] = size_scale

    spectrum_array_nozeros = spectrum_array*1.
    spectrum_array_nozeros[spectrum_array_nozeros==0]=np.nan
    o_ = p_plot_arr(spectrum_array_nozeros, size_array, speed_array,
                    # custom_y_range_tuple=(0,10), custom_x_range_tuple=(0,10),
                    grid_=True,
                    x_header='particle size [mm]', y_header='particle speed [m/s]',
                    cbar_label='particle counts', cbar_format='%.0f',
                    cbar_number_of_colors=10, cmap_='jet', extend_='max', vmin_=0.5, vmax_=10.5,
                    figsize_=(12,8),
                    # colorbar_tick_labels_list=list(np.arange(.5,10.5).astype(str)),
                    )
    # Set custom x-ticks and y-ticks on the axis
    o_[1].set_xticks(series_half_points(size_scale))  # Set x-ticks at the x values
    plt.setp(o_[1].get_xticklabels(), rotation=90)
    o_[1].set_yticks(series_half_points(speed_scale))  # Set y-ticks at the y values
    o_[1].set_ylim((0,10.5))
    o_[1].set_xlim((0,10))

    o_ = p_plot(size_scale_line, U_t, c_='black', add_line=True, S_=1, fig_ax=o_[:2],
                title_str=title_str,
                )
    fig_adjust(o_[0], right=1.05, top=.95)

    return o_[0], o_[1]


# Vaisala
def convert_vaisala_FD70_raw_to_netcdf_V1(filename_raw, path_output,
                                          filename_prefix='FD70_', use_header_location_in_filename=True,
                                          print_debug=False):
    """
    Converts raw text files with data from the Vaisala Forward Scatter Sensor FD70 into nice netCDF files,
    keeping all information from the original raw file. Assumes the message is MES8.
    :param filename_raw: full path and filename to raw data
    :param path_output: full path to output directory, no filename to be included.
    :param filename_prefix: first part of output filename to be added
    :param use_header_location_in_filename: looks for "#    location: " as part of the filename (striped of bad chars)
    :param print_debug: bool, if True multiple messages will be printed that shows the status of the script.
    :return: None
    """

    data_start_line = 259
    PSD_bins = 41
    PVD_bins = 26

    """    
    from the manual...

    Table 37 Droplet size distribution
    Position | Name | Example | Bin | Mean(mm) | Bin width(mm) | Droplet size range(mm)
    7 … 10    | B001 | 21 | 1  | 0.12 | 0.02 | 0.110 … 0.130
    12 … 15   | B002 | 22 | 2  | 0.14 | 0.02 | 0.130 … 0.150
    17 … 20   | B003 | 25 | 3  | 0.17 | 0.03 | 0.155 … 0.185
    22 … 25   | B004 | 11 | 4  | 0.2  | 0.03 | 0.185 … 0.215
    27 … 30   | B005 | 9  | 5  | 0.23 | 0.04 | 0.210 … 0.250
    32 … 35   | B006 | 1  | 6  | 0.27 | 0.05 | 0.245 … 0.295
    37 … 40   | B007 | 7  | 7  | 0.32 | 0.05 | 0.295 … 0.345
    42 … 45   | B008 | 0  | 8  | 0.38 | 0.06 | 0.350 … 0.410
    47 … 50   | B009 | 0  | 9  | 0.45 | 0.07 | 0.415 … 0.485
    52 … 55   | B010 | 0  | 10 | 0.53 | 0.09 | 0.485 … 0.575
    57 … 60   | B011 | 0  | 11 | 0.62 | 0.10 | 0.570 … 0.670
    62 … 65   | B012 | 0  | 12 | 0.73 | 0.12 | 0.670 … 0.790
    67 … 70   | B013 | 0  | 13 | 0.86 | 0.15 | 0.785 … 0.935
    72 … 75   | B014 | 0  | 14 | 1.02 | 0.16 | 0.940 … 1.100
    77 … 80   | B015 | 3  | 15 | 1.14 | 0.08 | 1.100 … 1.180
    82 … 85   | B016 | 0  | 16 | 1.23 | 0.09 | 1.185 … 1.275
    87 … 90   | B017 | 0  | 17 | 1.32 | 0.09 | 1.275 … 1.365
    92 … 95   | B018 | 0  | 18 | 1.41 | 0.10 | 1.360 … 1.460
    97 … 100  | B019 | 0  | 19 | 1.52 | 0.11 | 1.465 … 1.575
    102 … 105 | B020 | 0  | 20 | 1.63 | 0.12 | 1.570 … 1.690
    107 … 110 | B021 | 0  | 21 | 1.75 | 0.12 | 1.690 … 1.810
    112 … 115 | B022 | 0  | 22 | 1.88 | 0.14 | 1.810 … 1.950
    117 … 120 | B023 | 0  | 23 | 2.02 | 0.14 | 1.950 … 2.090
    122 … 125 | B024 | 0  | 24 | 2.16 | 0.15 | 2.085 … 2.350
    127 … 130 | B025 | 0  | 25 | 2.32 | 0.17 | 2.235 … 2.405
    132 … 135 | B026 | 0  | 26 | 2.49 | 0.17 | 2.405 … 2.575
    137 … 140 | B027 | 0  | 27 | 2.68 | 0.19 | 2.585 … 2.775
    142 … 145 | B028 | 0  | 28 | 2.87 | 0.21 | 2.765 … 2.975
    147 … 150 | B029 | 0  | 29 | 3.08 | 0.22 | 2.970 … 3.190
    152 … 155 | B030 | 0  | 30 | 3.31 | 0.23 | 3.195 … 3.425
    157 … 160 | B031 | 0  | 31 | 3.55 | 0.25 | 3.425 … 3.675
    162 … 165 | B032 | 0  | 32 | 3.82 | 0.27 | 3.470 … 3.955
    167 … 170 | B033 | 0  | 33 | 4.10 | 0.29 | 3.955 … 4.245
    172 … 175 | B034 | 0  | 34 | 4.40 | 0.32 | 4.240 … 4.560
    177 … 180 | B035 | 0  | 35 | 4.72 | 0.33 | 4.555 … 4.885
    182 … 185 | B036 | 0  | 36 | 5.07 | 0.36 | 4.890 … 5.250
    187 … 190 | B037 | 0  | 37 | 5.44 | 0.39 | 5.245 … 5.635
    192 … 195 | B038 | 0  | 38 | 5.84 | 0.41 | 5.635 … 6.045
    197 … 200 | B039 | 0  | 39 | 6.27 | 0.45 | 6.045 … 6.495
    202 … 205 | B040 | 0  | 40 | 6.73 | 0.47 | 6.495 … 6.965
    207 … 210 | B041 | 0  | 41 | >7
    """
    PSD_bins_means = np.array([
        0.12,
        0.14,
        0.17,
        0.2,
        0.23,
        0.27,
        0.32,
        0.38,
        0.45,
        0.53,
        0.62,
        0.73,
        0.86,
        1.02,
        1.14,
        1.23,
        1.32,
        1.41,
        1.52,
        1.63,
        1.75,
        1.88,
        2.02,
        2.16,
        2.32,
        2.49,
        2.68,
        2.87,
        3.08,
        3.31,
        3.55,
        3.82,
        4.10,
        4.40,
        4.72,
        5.07,
        5.44,
        5.84,
        6.27,
        6.73,
        21.5,
    ])
    PSD_bins_mins = np.array([
        0.110,
        0.130,
        0.155,
        0.185,
        0.210,
        0.245,
        0.295,
        0.350,
        0.415,
        0.485,
        0.570,
        0.670,
        0.785,
        0.940,
        1.100,
        1.185,
        1.275,
        1.360,
        1.465,
        1.570,
        1.690,
        1.810,
        1.950,
        2.085,
        2.235,
        2.405,
        2.585,
        2.765,
        2.970,
        3.195,
        3.425,
        3.470,
        3.955,
        4.240,
        4.555,
        4.890,
        5.245,
        5.635,
        6.045,
        6.495,
        6.965,
    ])
    PSD_bins_maxs = np.array([
        0.130,
        0.150,
        0.185,
        0.215,
        0.250,
        0.295,
        0.345,
        0.410,
        0.485,
        0.575,
        0.670,
        0.790,
        0.935,
        1.100,
        1.180,
        1.275,
        1.365,
        1.460,
        1.575,
        1.690,
        1.810,
        1.950,
        2.090,
        2.350,
        2.405,
        2.575,
        2.775,
        2.975,
        3.190,
        3.425,
        3.675,
        3.955,
        4.245,
        4.560,
        4.885,
        5.250,
        5.635,
        6.045,
        6.495,
        6.965,
        35.00,
    ])

    """
    from the manual...
    Table 39 Droplet fall speed distribution
    Position | Name | Example | Bin Mean (m/s) | Droplet fall speed range (m/s)
    9 … 12    | B001 | 100 | 1  | 0.2 | 0 … 0.4
    14 … 17   | B002 | 200 | 2  | 0.6 | 0.4 … 0.8
    19 … 22   | B003 | 300 | 3  | 1.0 | 0.8 … 1.2
    24 … 27   | B004 | 50  | 4  | 1.4 | 1.2 … 1.6
    29 … 32   | B005 | 20  | 5  | 1.8 | 1.6 … 2.0
    34 … 37   | B006 | 11  | 6  | 2.2 | 2.0 … 2.4
    39 … 42   | B007 | 5   | 7  | 2.6 | 2.4 … 2.8
    44 … 47   | B008 | 4   | 8  | 3.0 | 2.8 … 3.2
    49 … 52   | B009 | 0   | 9  | 3.4 | 3.2 … 3.6
    54 … 57   | B010 | 0   | 10 | 3.8 | 3.6 … 4.0
    59 … 62   | B011 | 0   | 11 | 4.2 | 4.0 … 4.4
    64 … 67   | B012 | 0   | 12 | 4.6 | 4.4 … 4.8
    69 … 72   | B013 | 0   | 13 | 5.0 | 4.8 … 5.2
    74 … 77   | B014 | 0   | 14 | 5.4 | 5.2 … 5.6
    79 … 82   | B015 | 0   | 15 | 5.8 | 5.6 … 6.0
    84 … 87   | B016 | 3   | 16 | 6.2 | 6.0 … 6.4
    89 … 92   | B017 | 0   | 17 | 6.6 | 6.4 … 6.8
    94 … 97   | B018 | 0   | 18 | 7.0 | 6.8 … 7.2
    99 … 102  | B019 | 0   | 19 | 7.4 | 7.2 … 7.6
    104 … 107 | B020 | 0   | 20 | 7.8 | 7.6 … 8.0
    109 … 112 | B021 | 0   | 21 | 8.2 | 8.0 … 8.4
    114 … 117 | B022 | 0   | 22 | 8.6 | 8.4 … 8.8
    119 … 122 | B023 | 0   | 23 | 9.0 | 8.8 … 9.2
    124 … 127 | B024 | 0   | 24 | 9.4 | 9.2 … 9.6
    129 … 132 | B025 | 0   | 25 | 9.8 | 9.6 … 10.0
    134 … 137 | B026 | 0   | 26 | >10

    """
    PVD_bins_means = np.array([
        0.2,
        0.6,
        1.0,
        1.4,
        1.8,
        2.2,
        2.6,
        3.0,
        3.4,
        3.8,
        4.2,
        4.6,
        5.0,
        5.4,
        5.8,
        6.2,
        6.6,
        7.0,
        7.4,
        7.8,
        8.2,
        8.6,
        9.0,
        9.4,
        9.8,
        10.2,
    ])
    PVD_bins_mins = np.array([
        0,
        0.4,
        0.8,
        1.2,
        1.6,
        2.0,
        2.4,
        2.8,
        3.2,
        3.6,
        4.0,
        4.4,
        4.8,
        5.2,
        5.6,
        6.0,
        6.4,
        6.8,
        7.2,
        7.6,
        8.0,
        8.4,
        8.8,
        9.2,
        9.6,
        10,
    ])
    PVD_bins_maxs = np.array([
        0.4,
        0.8,
        1.2,
        1.6,
        2.0,
        2.4,
        2.8,
        3.2,
        3.6,
        4.0,
        4.4,
        4.8,
        5.2,
        5.6,
        6.0,
        6.4,
        6.8,
        7.2,
        7.6,
        8.0,
        8.4,
        8.8,
        9.2,
        9.6,
        10.0,
        10.4,
    ])


    precip_type_dict_NWS = """
        'C': 'No Precip',
        'A': 'Hail',
        'L': 'Drizzle',
        'L+': 'heavy Drizzle',
        'L-': 'light Drizzle',
        'R': 'Rain',
        'R+': 'heavy Rain',
        'R-': 'light Rain',
        'RL': 'Drizzle and Rain',
        'RL+': 'heavy Drizzle and Rain',
        'RL-': 'light Drizzle and Rain',
        'RLS': 'Rain, Drizzle and Snow',
        'RLS+': 'heavy Rain, Drizzle and Snow',
        'RLS-': 'light Rain, Drizzle and Snow',
        'S': 'Snow',
        'S+': 'heavy Snow',
        'S-': 'light Snow',
        'SG': 'Snow Grains',
        'SP': 'Freezing Rain'
        """

    if print_debug: print('-' * 40 + f'\nreading raw file text\n{filename_raw}\n')
    with open(filename_raw, 'r') as file_:
        file_lines = file_.readlines()

    # define file header
    file_header = ''
    for line_ in file_lines[:data_start_line]:
        file_header += line_
    # get site location variables from header
    site_lat = float(file_lines[17].split(':')[-1].strip().replace('*','').strip())
    site_lon = float(file_lines[18].split(':')[-1].strip().replace('*','').strip())
    site_alt = float(file_lines[19].split(':')[-1].strip().replace('*','').strip())
    site_location = re.sub('[^A-Za-z0-9]+', '', file_header.split('#    location: ')[-1])
    if print_debug: print('file header defined')

    # define raw data lines list (without header)
    data_raw_lines_list = file_lines[data_start_line:]
    # remove path from first time stamp
    data_raw_lines_list[0] = data_raw_lines_list[0][-123:]
    # remove possible empty lines from list
    for row_index_original in np.arange(len(data_raw_lines_list))[::-1]:  # goes in reverse order since size changes
        if data_raw_lines_list[row_index_original] == '\n':
            data_raw_lines_list.pop(row_index_original)
    # check that first time stamp is from the start of message (not partial from previous communication)
    data_raw_lines_list[0].split('::')
    if len(data_raw_lines_list[0].split('::')) != 3:
        raise_error('First time stamp in file is not complete, possibly corropted initial reading.\n' +
                    f'problem encountered on filename: {filename_raw}\n' +
                    f'at time stamp {data_raw_lines_list[0][:21]}')
    # # remove last lines if the file was cut mid creating of last message
    # if int(len(data_raw_lines_list)/6) - len(data_raw_lines_list)/6 != 0:
    #     if print_debug: print('file seems to have cut mid storing of last message, attempting to clean')
    #     data_raw_lines_list = data_raw_lines_list[:int(int(len(data_raw_lines_list)/6)*6)]
    #     if len(data_raw_lines_list[-6].split('::')) == 3:
    #         if print_debug: print('cleaning seems to have worked, continuing compilation')
    #     else:
    #         raise_error('file seems to be missing some time stamps in the body of the data (not the end or start) ' +
    #                     'will continue but an error during the loop is likely. ' +
    #                     'See error time stamp for manual cleaning')
    if print_debug: print('initial data cleaning done')

    # loop through lines to get individual time stamps (each time stamp takes 6 lines)
    number_of_time_stamps = int(len(data_raw_lines_list) / 6)
    # initialize arrays
    time_stamps_logger = np.zeros(number_of_time_stamps, dtype=float)
    time_stamps_msg = np.zeros(number_of_time_stamps, dtype=float)
    HW_flag = np.zeros(number_of_time_stamps, dtype='<U1')
    maintenance_flag = np.zeros(number_of_time_stamps, dtype='<U1')
    MOR_1min = np.zeros(number_of_time_stamps, dtype=int)
    MOR_10min = np.zeros(number_of_time_stamps, dtype=int)
    NWS_code_main = np.zeros(number_of_time_stamps, dtype='<U3')
    NWS_code_2nd = np.zeros(number_of_time_stamps, dtype='<U3')
    NWS_code_3rd = np.zeros(number_of_time_stamps, dtype='<U3')
    SYNOP_1min = np.zeros(number_of_time_stamps, dtype=int)
    SYNOP_15min = np.zeros(number_of_time_stamps, dtype=int)
    SYNOP_1hr = np.zeros(number_of_time_stamps, dtype=int)
    precip_int = np.zeros(number_of_time_stamps, dtype=float)
    precip_acc = np.zeros(number_of_time_stamps, dtype=float)
    snow_acc = np.zeros(number_of_time_stamps, dtype=int)
    amb_temp = np.zeros(number_of_time_stamps, dtype=float)
    dew_point = np.zeros(number_of_time_stamps, dtype=float)
    RH_ = np.zeros(number_of_time_stamps, dtype=float)
    luminance_ = np.zeros(number_of_time_stamps, dtype='<U5')
    present_METAR = np.zeros(number_of_time_stamps, dtype='<U5')
    recent_METAR = np.zeros(number_of_time_stamps, dtype='<U5')
    Ze_ = np.zeros(number_of_time_stamps, dtype=float)
    PSD_ = np.zeros((number_of_time_stamps, PSD_bins), dtype=int)
    KE_ = np.zeros(number_of_time_stamps, dtype=float)
    PVD_ = np.zeros((number_of_time_stamps, PVD_bins), dtype=int)
    if print_debug: print('output arrays initialized, starting loop through each time stamp')
    # start loop (skipping internal content of message)
    valid_data_flag = np.zeros(number_of_time_stamps, dtype=bool)
    index_output = -1
    index_raw = -6
    while index_raw < len(data_raw_lines_list)-11:
        index_output += 1
        index_raw += 6
        line_1_txt = data_raw_lines_list[index_raw]
        line_2_txt = data_raw_lines_list[index_raw + 1]
        line_3_txt = data_raw_lines_list[index_raw + 2]
        line_4_txt = data_raw_lines_list[index_raw + 3]
        line_5_txt = data_raw_lines_list[index_raw + 4]

        # check that all time stamps from datalogger are within 1 second
        datalogger_time_stamps_list = []
        for temp_index in range(5):
            datalogger_time_stamps_list.append(
                time_str_to_seconds(data_raw_lines_list[index_raw + temp_index].split('::')[1],
                                    '%Y-%m-%d %H:%M:%S'))
        if np.max(np.abs(np.diff(datalogger_time_stamps_list))) > 1:
            if print_debug:
                print('\ttimes shown by datalogger within the same message time stamp are not consistent.\n'+
                      '\tlikely due to corruption of data or incomplete transmission.\n' +
                      f'\tproblem encountered on filename: {filename_raw}\n' +
                      f'\tat time stamp {data_raw_lines_list[index_raw].split("::")[1]}.\n' +
                      f'\tAttempting to find start of new uncorrupted stamps')

            index_output -= 1
            index_raw -= 5
            continue

        # add data from line 1 to output arrays
        time_stamps_logger[index_output] = time_str_to_seconds(line_1_txt.split('::')[1], '%Y-%m-%d %H:%M:%S')
        time_stamps_msg[index_output] = time_str_to_seconds(line_1_txt.split('::')[2][:20], time_format_iso)
        HW_flag[index_output] = line_1_txt[44]
        maintenance_flag[index_output] = line_1_txt[45]
        MOR_1min[index_output] = line_1_txt[47:52]
        MOR_10min[index_output] = line_1_txt[53:58]
        NWS_code_main[index_output] = line_1_txt[59:62]
        NWS_code_2nd[index_output] = line_1_txt[63:66]
        NWS_code_3rd[index_output] = line_1_txt[67:70]
        SYNOP_1min[index_output] = line_1_txt[71:73]
        SYNOP_15min[index_output] = line_1_txt[74:76]
        SYNOP_1hr[index_output] = line_1_txt[77:79]
        precip_int[index_output] = line_1_txt[80:86]
        precip_acc[index_output] = line_1_txt[87:93]
        snow_acc[index_output] = line_1_txt[94:98]
        amb_temp[index_output] = line_1_txt[99:104]
        dew_point[index_output] = line_1_txt[105:110]
        RH_[index_output] = line_1_txt[111:116]
        luminance_[index_output] = line_1_txt[117:122]

        # add data from line 2 to output array
        present_METAR[index_output] = line_2_txt.split('::')[2].strip()

        # add data from line 3 to output array
        recent_METAR[index_output] = line_3_txt.split('::')[2].strip()

        # add data from line 4 to output arrays
        Ze_[index_output] = line_4_txt.split('::')[2].split()[0]
        PSD_[index_output, :] = line_4_txt.split('::')[2].split()[1:]

        # add data from line 5 to output arrays
        KE_[index_output] = line_5_txt.split('::')[2].split()[0]
        PVD_[index_output, :] = line_5_txt.split('::')[2].split()[1:]
        valid_data_flag[index_output] = True
    if print_debug: print('all time stamps read into output arrays')

    # keep only rows with valid data
    time_stamps_logger = time_stamps_logger[valid_data_flag]
    time_stamps_msg = time_stamps_msg[valid_data_flag]
    HW_flag = HW_flag[valid_data_flag]
    maintenance_flag = maintenance_flag[valid_data_flag]
    MOR_1min = MOR_1min[valid_data_flag]
    MOR_10min = MOR_10min[valid_data_flag]
    NWS_code_main = NWS_code_main[valid_data_flag]
    NWS_code_2nd = NWS_code_2nd[valid_data_flag]
    NWS_code_3rd = NWS_code_3rd[valid_data_flag]
    SYNOP_1min = SYNOP_1min[valid_data_flag]
    SYNOP_15min = SYNOP_15min[valid_data_flag]
    SYNOP_1hr = SYNOP_1hr[valid_data_flag]
    precip_int = precip_int[valid_data_flag]
    precip_acc = precip_acc[valid_data_flag]
    snow_acc = snow_acc[valid_data_flag]
    amb_temp = amb_temp[valid_data_flag]
    dew_point = dew_point[valid_data_flag]
    RH_ = RH_[valid_data_flag]
    luminance_ = luminance_[valid_data_flag]
    present_METAR = present_METAR[valid_data_flag]
    recent_METAR = recent_METAR[valid_data_flag]
    Ze_ = Ze_[valid_data_flag]
    PSD_ = PSD_[valid_data_flag]
    KE_ = KE_[valid_data_flag]
    PVD_ = PVD_[valid_data_flag]

    # place all data into dictionary
    dict_ = {}
    dict_['variables'] = {}
    dict_['dimensions'] = ('time', 'PSD_bins_means', 'PVD_bins_means')

    attribute_list = [
        ('author', 'Luis Ackermann'),
        ('author email', 'ackermann.luis@gmail.com'),
        ('version', '1'),
        ('time of file creation', time_seconds_to_str(time.time(), '%Y-%m-%d_%H:%M UTC')),
        ('raw file header', file_header),
        ('site_latitued', site_lat),
        ('site_longitude', site_lon),
        ('site_altitude_meters', site_alt),
        ('site_location', site_location),
        ('instrument_type', 'Vaisala FD70'),
    ]
    dict_['attributes'] = attribute_list

    # ##### dimensions

    # time
    var_name = 'time'
    day_time_str = time_seconds_to_str(0, '%Y-%m-%d_%H:%M:%S UTC')
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'seconds since ' + day_time_str),
        ('description', 'time stamp as reported by message in UTC')]
    dict_['variables'][var_name]['data'] = time_stamps_msg

    # time_logger
    var_name = 'time_from_datalogger'
    day_time_str = time_seconds_to_str(0, '%Y-%m-%d_%H:%M:%S UTC')
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'seconds since ' + day_time_str),
        ('description', 'time stamp as reported by datalogger in unknown time zone, likely local.')]
    dict_['variables'][var_name]['data'] = time_stamps_logger

    # PSD_bins_means
    var_name = 'PSD_bins_means'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('PSD_bins_means',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'mean bin size for each Particle Size Distribution bin'),
        ('note', 'on manual, the last bin is reported as more than 7mm, with the instrument range going to 35. ' +
         'no further details are provided about this bin so the mid-point between the bin edges was used for the mean.'),
    ]
    dict_['variables'][var_name]['data'] = PSD_bins_means

    # PSD_bins_mins
    var_name = 'PSD_bins_mins'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('PSD_bins_means',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'minimum bin size for each Particle Size Distribution bin. Left-side bin edge.'),
        ('note', 'on manual, the last bin is reported as more than 7mm, with the instrument range going to 35. ' +
         'no further details are provided about this bin so ' +
         'the right-size bin edge of the previous bin was used for the last bin.'),
    ]
    dict_['variables'][var_name]['data'] = PSD_bins_mins

    # PSD_bins_maxs
    var_name = 'PSD_bins_maxs'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('PSD_bins_means',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'maximum bin size for each Particle Size Distribution bin. Right-side bin edge.'),
        ('note', 'on manual, the last bin is reported as more than 7mm, with the instrument range going to 35. ' +
         'no further details are provided about this bin so the instrument maximum range is used for the last bin'),
    ]
    dict_['variables'][var_name]['data'] = PSD_bins_maxs


    # PVD_bins_means
    var_name = 'PVD_bins_means'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('PVD_bins_means',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'm/s'),
        ('description', 'mean bin fall speed for each Particle Velocity Distribution bin'),
        ('note', 'on manual, the last bin is reported as more than 10m/s, ' +
                 'with the instrument range not specifying an upper limit. ' +
                 'no further details are provided about this bin. ' +
                 'Since the bin spacing is consistent for all previous ones, '
                 'the last bin mean and edges were extrapolated from the previous one.'),
    ]
    dict_['variables'][var_name]['data'] = PVD_bins_means

    # PVD_bins_mins
    var_name = 'PVD_bins_mins'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('PVD_bins_means',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'm/s'),
        ('description', 'minimum bin fall speed for each Particle Velocity Distribution bin. Left-side bin edge.'),
        ('note', 'on manual, the last bin is reported as more than 10m/s, ' +
                 'with the instrument range not specifying an upper limit. ' +
                 'no further details are provided about this bin. ' +
                 'Since the bin spacing is consistent for all previous ones, '
                 'the last bin minimum was extrapolated from the previous one.'),
    ]
    dict_['variables'][var_name]['data'] = PVD_bins_mins

    # PVD_bins_maxs
    var_name = 'PVD_bins_maxs'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('PVD_bins_means',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'm/s'),
        ('description', 'maximum bin fall speed for each Particle Velocity Distribution bin. Right-side bin edge.'),
        ('note', 'on manual, the last bin is reported as more than 10m/s, ' +
                 'with the instrument range not specifying an upper limit. ' +
                 'no further details are provided about this bin. ' +
                 'Since the bin spacing is consistent for all previous ones, '
                 'the last bin maximum was extrapolated from the previous one.'),
    ]
    dict_['variables'][var_name]['data'] = PVD_bins_maxs


    # ##### other variables
    var_name = 'HW_flag'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', '0:OK,W:Warning,A:Alarm'),
        ('description', 'Overall hardware alert'),
    ]
    dict_['variables'][var_name]['data'] = HW_flag

    var_name = 'maintenance_flag'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', '0:OK,I:Info,W:Warning,A:Alarm'),
        ('description', 'Overall maintenance alert'),
    ]
    dict_['variables'][var_name]['data'] = maintenance_flag

    var_name = 'MOR_1min'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'm'),
        ('description', 'MOR, 1-minute average in meters'),
    ]
    dict_['variables'][var_name]['data'] = MOR_1min

    var_name = 'MOR_10min'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'm'),
        ('description', 'MOR, 10-minute average in meters'),
    ]
    dict_['variables'][var_name]['data'] = MOR_10min

    var_name = 'NWS_code_main'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', 'Most dominant Precipitation Type (NWS code)'),
        ('code_list', precip_type_dict_NWS)
    ]
    dict_['variables'][var_name]['data'] = NWS_code_main

    var_name = 'NWS_code_2nd'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', '2nd dominant Precipitation Type (NWS code)'),
        ('code_list', precip_type_dict_NWS)
    ]
    dict_['variables'][var_name]['data'] = NWS_code_2nd

    var_name = 'NWS_code_3rd'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', '3rd dominant Precipitation Type (NWS code)'),
        ('code_list', precip_type_dict_NWS)
    ]
    dict_['variables'][var_name]['data'] = NWS_code_3rd

    var_name = 'SYNOP_1min'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', 'Present weather instant (1 min) (SYNOP)'),
        ('code_list', 'see https://xwiki.avinor.no/display/ADD/Present+Weather+Codes%2C+WMO+SYNOP+4680%2C+WMO+4678'),
    ]
    dict_['variables'][var_name]['data'] = SYNOP_1min

    var_name = 'SYNOP_15min'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', 'Present weather instant (15 min) (SYNOP)'),
        ('code_list', 'see https://xwiki.avinor.no/display/ADD/Present+Weather+Codes%2C+WMO+SYNOP+4680%2C+WMO+4678'),
    ]
    dict_['variables'][var_name]['data'] = SYNOP_15min

    var_name = 'SYNOP_1hr'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', 'Present weather instant (1 hour) (SYNOP)'),
        ('code_list', 'see https://xwiki.avinor.no/display/ADD/Present+Weather+Codes%2C+WMO+SYNOP+4680%2C+WMO+4678'),
    ]
    dict_['variables'][var_name]['data'] = SYNOP_1hr

    var_name = 'precip_int'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'mm/h'),
        ('description', 'Precipitation intensity (mm/h). Calculated over last minute.'),
    ]
    dict_['variables'][var_name]['data'] = precip_int

    var_name = 'precip_acc'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'Precipitation accumulation (mm)'),
    ]
    dict_['variables'][var_name]['data'] = precip_acc

    var_name = 'snow_acc'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'Snow accumulation (mm)'),
    ]
    dict_['variables'][var_name]['data'] = snow_acc

    var_name = 'amb_temp'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'C'),
        ('description', 'Ambient temperature (°C). Instant value, updated every 10 seconds'),
    ]
    dict_['variables'][var_name]['data'] = amb_temp

    var_name = 'dew_point'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'C'),
        ('description', 'Dew point temperature (°C). Instant value, updated every 10 seconds'),
    ]
    dict_['variables'][var_name]['data'] = dew_point

    var_name = 'RH'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', '%'),
        ('description', 'Relative humidity (%). Instant value, updated every 10 seconds'),
    ]
    dict_['variables'][var_name]['data'] = RH_

    var_name = 'luminance'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'cd/m2'),
        ('description', 'Background luminance (cd/m2)'),
    ]
    dict_['variables'][var_name]['data'] = luminance_

    var_name = 'present_METAR'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', 'Present METAR according to METAR WMO table 4678. Variable length, 0-12 characters'),
    ]
    dict_['variables'][var_name]['data'] = present_METAR

    var_name = 'recent_METAR'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'na'),
        ('description', 'Recent METAR according to METAR WMO table 4678. ' +
                        'The prefix RE stands for "recent". Variable length, 0-12 characters'),
    ]
    dict_['variables'][var_name]['data'] = recent_METAR

    var_name = 'Z'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time',)
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'dBZ'),
        ('description', 'Reflectivity (dBZ)'),
        ('minimum_sensitivity', -9.9),
    ]
    dict_['variables'][var_name]['data'] = Ze_

    var_name = 'PSD'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time', 'PSD_bins_means')
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'mm'),
        ('description', 'Droplet size distribution in size classes 1 - 41'),
        ('note', 'Note that the bins are not uniform on means or widths, ' +
                 'For bin edges see variables PSD_bins_mins and PSD_bins_maxs')
    ]
    dict_['variables'][var_name]['data'] = PSD_

    var_name = 'KE'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time', )
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'J/m2 * h'),
        ('description', 'Kinetic energy'),
    ]
    dict_['variables'][var_name]['data'] = KE_

    var_name = 'PVD'
    dict_['variables'][var_name] = {}
    dict_['variables'][var_name]['dimensions'] = ('time', 'PVD_bins_means')
    dict_['variables'][var_name]['attributes'] = [
        ('units', 'm/s'),
        ('description', 'Droplet fall speed (velocity) distribution'),
        ('note', 'For bin edges see variables PVD_bins_mins and PVD_bins_maxs')
    ]
    dict_['variables'][var_name]['data'] = PVD_
    if print_debug: print('data formated for output to netcdf')

    # define filename output
    if use_header_location_in_filename:
        filename_output = path_output + filename_prefix + site_location + '_'
    else:
        filename_output = path_output + filename_prefix

    # add time range to filename_output
    time_start_str = time_seconds_to_str(time_stamps_msg[0], time_format_parsivel_seconds)
    time_stop_str = time_seconds_to_str(time_stamps_msg[-1], time_format_parsivel_seconds)
    filename_output += time_start_str + '_' + time_stop_str + '_.nc'
    if print_debug: print('output filename defined as ' + filename_output)

    save_dictionary_to_netcdf(dict_, filename_output, print_debug=print_debug)


# Holographic microscope
def convert_raw_to_array(filename_):
    print('converting file: ' + filename_.split('/')[-1])
    A = np.fromfile(filename_, dtype='uint8')
    evenEl = A[1::2]
    oddEl = A[0::2]
    B = 256 * evenEl + oddEl
    width = 2592
    height = 1944
    I = B.reshape(height, width)
    return I
def create_video_from_filelist(file_list, output_filename, cmap_):
    width = 2592
    height = 1944
    array_3d = np.zeros((len(file_list), height, width), dtype='uint8')
    time_list = []
    for t_, filename_ in enumerate(file_list):
        array_3d[t_,:,:] = convert_raw_to_array(filename_)
        time_list.append(filename_[-21:-4])


    create_video_animation_from_3D_array(array_3d, output_filename, colormap_= cmap_, title_list=time_list,
                                         axes_off=True, show_colorbar=False, interval_=500)

# png data handeling
def load_image_to_arr(filename_):
    return np.array(PIL_Image.open(filename_))
def store_array_to_png(array_, filename_out):
    # shape
    rows_ = array_.shape[0]
    columns_ = array_.shape[1]

    # nan layer
    array_nan =  np.zeros((rows_, columns_), dtype='uint8')
    array_nan[array_ != array_] = 100

    # replace nans
    array_[array_ != array_] = 0

    # convert to all positive
    array_positive = np.abs(array_)

    # sign layer
    array_sign = np.zeros((rows_, columns_), dtype='uint8')
    array_sign[array_ >= 0] = 100

    # zeros array
    array_zeros = np.zeros((rows_, columns_), dtype='uint8')
    array_zeros[array_positive != 0] = 1

    # sub 1 array
    array_sub1 = np.zeros((rows_, columns_), dtype='uint8')
    array_sub1[array_positive<1] = 1
    array_sub1 = array_sub1 * array_zeros

    # power array
    exp_ = np.array(np.log10(array_positive), dtype=int)
    exp_[array_zeros==0] = 0

    # integral array
    array_integral = array_positive / 10 ** np.array(exp_, dtype=float)

    # array_layer_1
    array_layer_1 = np.array(((array_sub1 * 9) + 1) * array_integral * 10, dtype='uint8') + array_sign

    # array_layer_2
    array_layer_2 = np.array(((array_integral * ((array_sub1 * 9) + 1) * 10)
                              - np.array(array_integral * ((array_sub1 * 9) + 1) * 10, dtype='uint8')) * 100,
                             dtype='uint8')
    array_layer_2 = array_layer_2 + array_nan

    # power sign layer
    exp_ = exp_ - array_sub1
    array_power_sign = np.zeros((rows_, columns_), dtype='uint8')
    array_power_sign[exp_ >= 0] = 100

    # array_layer_3
    array_layer_3 = np.abs(exp_) + array_power_sign

    # initialize out array
    out_array = np.zeros((rows_, columns_, 3), dtype='uint8')

    # dump into out array
    out_array[:, :, 0] = array_layer_1
    out_array[:, :, 1] = array_layer_2
    out_array[:, :, 2] = array_layer_3

    img_arr = PIL_Image.fromarray(out_array)
    img_arr.save(filename_out)
def read_png_to_array(filename_):
    # read image into array
    img_arr = np.array(PIL_Image.open(filename_))

    # shape
    rows_ = img_arr.shape[0]
    columns_ = img_arr.shape[1]

    # nan array
    nan_array = np.zeros((rows_, columns_), dtype='uint8')
    nan_array[img_arr[:,:,1] >= 100] = 1

    # power array
    power_array_magnitude = ((img_arr[:,:,2]/100) - np.array(img_arr[:,:,2]/100, dtype='uint8') ) * 100
    sign_array = np.zeros((rows_, columns_)) - 1
    sign_array[img_arr[:,:,2] >= 100] = 1
    power_array = power_array_magnitude * sign_array

    # sign array
    sign_array = np.array(img_arr[:,:,0]/100, dtype=int)
    sign_array[sign_array == 0] = -1

    # unit array
    unit_array = np.array(img_arr[:,:,0]/10, dtype='uint8') - (np.array(img_arr[:,:,0]/100, dtype='uint8') * 10)

    # decimal array
    decimal_array_1 = (img_arr[:,:,0]/10) - np.array(img_arr[:,:,0]/10, dtype='uint8')
    decimal_array_2 = ((img_arr[:,:,1]/100) - np.array(img_arr[:,:,1]/100, dtype='uint8') ) / 10

    # compute out array
    out_array = (sign_array * (unit_array + decimal_array_1 + decimal_array_2)) * 10 ** power_array

    # flag nans
    out_array[nan_array==1]=np.nan

    return out_array
def convert_array_to_png_img(array_):
    # shape
    rows_ = array_.shape[0]
    columns_ = array_.shape[1]

    # nan layer
    array_nan =  np.zeros((rows_, columns_), dtype='uint8')
    array_nan[array_ != array_] = 100

    # replace nans
    array_[array_ != array_] = 0

    # convert to all positive
    array_positive = np.abs(array_)

    # sign layer
    array_sign = np.zeros((rows_, columns_), dtype='uint8')
    array_sign[array_ >= 0] = 100

    # zeros array
    array_zeros = np.zeros((rows_, columns_), dtype='uint8')
    array_zeros[array_positive != 0] = 1

    # sub 1 array
    array_sub1 = np.zeros((rows_, columns_), dtype='uint8')
    array_sub1[array_positive<1] = 1
    array_sub1 = array_sub1 * array_zeros

    # power array
    exp_ = np.array(np.log10(array_positive), dtype=int)
    exp_[array_zeros==0] = 0

    # integral array
    array_integral = array_positive / 10 ** np.array(exp_, dtype=float)

    # array_layer_1
    array_layer_1 = np.array(((array_sub1 * 9) + 1) * array_integral * 10, dtype='uint8') + array_sign

    # array_layer_2
    array_layer_2 = np.array(((array_integral * ((array_sub1 * 9) + 1) * 10)
                              - np.array(array_integral * ((array_sub1 * 9) + 1) * 10, dtype='uint8')) * 100,
                             dtype='uint8')
    array_layer_2 = array_layer_2 + array_nan

    # power sign layer
    exp_ = exp_ - array_sub1
    array_power_sign = np.zeros((rows_, columns_), dtype='uint8')
    array_power_sign[exp_ >= 0] = 100

    # array_layer_3
    array_layer_3 = np.abs(exp_) + array_power_sign

    # initialize out array
    out_array = np.zeros((rows_, columns_, 3), dtype='uint8')

    # dump into out array
    out_array[:, :, 0] = array_layer_1
    out_array[:, :, 1] = array_layer_2
    out_array[:, :, 2] = array_layer_3

    return PIL_Image.fromarray(out_array)
def convert_array_to_png_array(array_):
    # shape
    rows_ = array_.shape[0]
    columns_ = array_.shape[1]

    # nan layer
    array_nan =  np.zeros((rows_, columns_), dtype='uint8')
    array_nan[array_ != array_] = 100

    # replace nans
    array_[array_ != array_] = 0

    # convert to all positive
    array_positive = np.abs(array_)

    # sign layer
    array_sign = np.zeros((rows_, columns_), dtype='uint8')
    array_sign[array_ >= 0] = 100

    # zeros array
    array_zeros = np.zeros((rows_, columns_), dtype='uint8')
    array_zeros[array_positive != 0] = 1

    # sub 1 array
    array_sub1 = np.zeros((rows_, columns_), dtype='uint8')
    array_sub1[array_positive<1] = 1
    array_sub1 = array_sub1 * array_zeros

    # power array
    exp_ = np.array(np.log10(array_positive), dtype=int)
    exp_[array_zeros==0] = 0

    # integral array
    array_integral = array_positive / 10 ** np.array(exp_, dtype=float)

    # array_layer_1
    array_layer_1 = np.array(((array_sub1 * 9) + 1) * array_integral * 10, dtype='uint8') + array_sign

    # array_layer_2
    array_layer_2 = np.array(((array_integral * ((array_sub1 * 9) + 1) * 10)
                              - np.array(array_integral * ((array_sub1 * 9) + 1) * 10, dtype='uint8')) * 100,
                             dtype='uint8')
    array_layer_2 = array_layer_2 + array_nan

    # power sign layer
    exp_ = exp_ - array_sub1
    array_power_sign = np.zeros((rows_, columns_), dtype='uint8')
    array_power_sign[exp_ >= 0] = 100

    # array_layer_3
    array_layer_3 = np.abs(exp_) + array_power_sign

    # initialize out array
    out_array = np.zeros((rows_, columns_, 3), dtype='uint8')

    # dump into out array
    out_array[:, :, 0] = array_layer_1
    out_array[:, :, 1] = array_layer_2
    out_array[:, :, 2] = array_layer_3

    return out_array

def compress_photos_to_video(image_filename_list, image_timestamp_string_list, output_full_filename, today_label):
    # get images
    im_list_vis = []
    for im_filename in image_filename_list:
        im_list_vis.append(imageio.imread(im_filename))
        image_timestamp_string_list.append(im_filename.replace('\\','/').split('/')[-1].split('_')[-1].split('.')[0])
    imageio.mimsave(output_full_filename, im_list_vis)
    # create time stamp log file
    output_file = open(path_output + '/' + today_label + '_vis' + '_time_log.txt', "w")
    for time_stamp in image_timestamp_string_list:
        output_file.write("%s\n" % time_stamp)
    output_file.close()


    # im_list_ir = []
    # im_time_list = []
    # for im_filename in sat_image_file_list_ir:
    #     im_list_ir.append(read_image(im_filename))
    #     im_time_list.append(im_filename.replace('\\','/').split('/')[-1].split('_')[-1].split('.')[0])
    # imageio.mimsave(path_output + '/' + today_label + '_ir.gif', im_list_ir)
    # # create time stamp log file
    # output_file = open(path_output + '/' + today_label + '_ir' + '_time_log.txt', "w")
    # for time_stamp in im_time_list:
    #     output_file.write("%s\n" % time_stamp)
    # output_file.close()

    # cleanup
    for im_filename in image_filename_list:
        os.remove(im_filename)
    # for im_filename in sat_image_file_list_ir:
    #     os.remove(im_filename)

def store_array_to_png_V2(array_, filename_out):
    # 255  99  99  99       ->  scaled data
    #             255       ->  nan
    #                       ->  scale and offset stored in metadata

    # shape
    rows_ = array_.shape[0]
    columns_ = array_.shape[1]

    # nan layer
    color_layer_4 =  np.zeros((rows_, columns_), dtype='uint8')
    color_layer_4[np.where(array_ != array_)] = 255

    # normalize:  0 - 255  99  99  99
    max_ = np.nanmax(array_)
    min_ = np.nanmin(array_)
    array_ = array_ - min_
    array_ = 255999999 * array_ / (max_ - min_)

    # replace nans
    array_[np.where(array_ != array_)] = 0

    # initialize out array
    out_array = np.zeros((rows_, columns_, 4), dtype='uint8')

    # populate color layers
    out_array[:, :, 0] = np.array(array_ / 1000000, dtype='uint8')
    color_layer_1_z = np.array(out_array[:, :, 0], dtype=int) * 1000000
    out_array[:, :, 1] = np.array((array_ - color_layer_1_z) / 10000, dtype='uint8')
    color_layer_2_z = np.array(out_array[:, :, 1], dtype=int) * 10000
    out_array[:, :, 2] = np.array((array_ - color_layer_2_z - color_layer_1_z) / 100, dtype='uint8')
    color_layer_3_z = np.array(out_array[:, :, 2], dtype=int) * 100
    out_array[:, :, 3] = np.array((array_ - color_layer_3_z - color_layer_2_z - color_layer_1_z),
                             dtype='uint8') + color_layer_4

    # convert to image
    img_arr = PIL_Image.fromarray(out_array)

    # save min_ and max_ to metadata
    metadata = PngInfo()
    metadata.add_text("min_", str(min_))
    metadata.add_text("max_", str(max_))

    img_arr.save(filename_out, pnginfo=metadata)
def read_png_to_array_V2(filename_):
    # read image into array
    img_ = PIL_Image.open(filename_)
    img_arr = np.array(img_)
    img_.load()
    min_ = float(img_.info['min_'])
    max_ = float(img_.info['max_'])

    # shape
    rows_ = img_arr.shape[0]
    columns_ = img_arr.shape[1]

    # nan array
    nan_array = np.ones((rows_, columns_), dtype=float)
    nan_array[np.where(img_arr[:,:,3] == 255)] = np.nan

    # convert colors to number
    layer_1 = np.array(img_arr[:,:,0], dtype=float) * 1000000
    layer_2 = np.array(img_arr[:,:,1], dtype=float) * 10000
    layer_3 = np.array(img_arr[:,:,2], dtype=float) * 100
    layer_4 = np.array(img_arr[:,:,3], dtype=float)

    # convine color columns into one number
    normalized_array = (layer_1 + layer_2 + layer_3 + layer_4) / 255999999

    # rescale to original data
    output_array = normalized_array * (max_ - min_)
    output_array = output_array + min_

    # flag nans
    output_array = output_array * nan_array

    return output_array
def crop_image(img,tol=0,pad_=0):
    # img is 2D image data
    # tol  is tolerance
    mask = img>tol
    rows_,cols_ = np.ix_(mask.any(1),mask.any(0))

    return img[rows_.min()-pad_:rows_.max()+pad_, cols_.min()-pad_:cols_.max()+pad_]
def crop_image_2(img, pad_=0, size_r_c_tuple=None):
    mask = img>0
    rows_,cols_ = np.ix_(mask.any(1),mask.any(0))

    if size_r_c_tuple is None:
        r_1 = rows_.min() - pad_
        r_2 = rows_.max() + pad_
        c_1 = cols_.min() - pad_
        c_2 = cols_.max() + pad_
        return img[r_1:r_2, c_1:c_2]
    else:
        r_half = int(size_r_c_tuple[0]/2)
        c_half = int(size_r_c_tuple[1]/2)

        r_1 = int((rows_.min() + rows_.max()) /2) - r_half
        r_2 = r_1 + size_r_c_tuple[0]
        c_1 = int((cols_.min() + cols_.max()) /2) - c_half
        c_2 = c_1 + size_r_c_tuple[1]
        return img[r_1:r_2, c_1:c_2]
def crop_image_3(img,label_):
    mask = img!=label_
    mask = mask.any(0)
    mask0,mask1 = mask.any(0),mask.any(1)
    colstart, colend = mask0.argmax(), len(mask0)-mask0[::-1].argmax()+1
    rowstart, rowend = mask1.argmax(), len(mask1)-mask1[::-1].argmax()+1
    return img[rowstart:rowend, colstart:colend]


# grib handling
def inspect_grib(grib_filename):
    """
    Provides a quick overview of a GRIB file by printing the total number of messages, unique variable names,
    number of vertical levels found, and spatial shape of first message.

    Parameters:
    -----------
    grib_filename : str
        Path to the GRIB file to be inspected.

    Outputs:
    --------
    Prints:
        - Number of messages in the file.
        - Number of unique variable names.
        - List of unique variable names.

    Note:
    -----
    This function does not load the actual data, making it efficient for large GRIB files.
    """
    grbs_file = pygrib.open(grib_filename)

    # Get the number of messages efficiently
    number_of_messages = sum(1 for _ in grbs_file)

    # Reset file pointer
    grbs_file.rewind()

    # Get unique variable names without loading the full data
    var_name_list = {grb.name for grb in grbs_file}

    # Reset file pointer
    grbs_file.rewind()

    # Get unique level names without loading the full data
    level_list = {grb.level for grb in grbs_file}

    # Read dimensions from first message
    first_var = next(iter(var_name_list))  # Get any available variable
    first_level = next(iter(level_list))
    data_tmp, lat_arr_2D, lon_arr_2D = grbs_file.select(name=first_var, level=first_level)[0].data()

    grbs_file.close()

    print(f"number of messages in file: {number_of_messages}")
    print(f"shape of lat array: {lat_arr_2D.shape}, shape of lon array: {lon_arr_2D.shape}")
    print(f"number of unique level names: {len(level_list)}")
    for level_name in list(sorted(level_list)):
        print(f"\t {level_name}")
    print(f"number of unique variable names: {len(var_name_list)}")
    print('Variable names:')
    for var_name in list(sorted(var_name_list)):
        print(f"\t {var_name}")
def load_grib_file_vars_to_dict(grib_filename, var_list=None):
    """
    Loads selected variables from a GRIB file into a dictionary. If no variables are specified, all are loaded.

    Parameters:
    -----------
    grib_filename : str
        Path to the GRIB file.

    var_list : list of str, optional
        List of variable names to load. If None, all variables are loaded.

    Returns:
    --------
    dict :
        A dictionary containing:
        - 'time_analysis': Analysis time of the dataset.
        - 'forecastTime': Forecast time step.
        - 'lat': 2D array of latitude values.
        - 'lon': 2D array of longitude values.
        - Variables: 4D numpy arrays of shape (1, num_levels, lat, lon).

    Notes:
    ------
    - If a variable does not exist in the GRIB file, it is skipped with a warning.
    - Latitude and longitude are always included.
    - This function efficiently reads only the requested variables to optimize performance.
    """
    grbs_file = pygrib.open(grib_filename)

    # Collect unique variable names and levels
    var_name_list = set()
    level_list = set()
    for grb in grbs_file:
        var_name_list.add(grb.name)
        level_list.add(grb.level)

    var_name_list = sorted(var_name_list)
    level_list = sorted(level_list)

    # If var_list is provided, filter the variables
    if var_list:
        selected_vars = set()
        for var_name in var_list:
            if var_name in var_name_list:  # Ensure valid variable names
                selected_vars.add(var_name)
            else:
                print(f"Warning: {var_name} not found in messages.")
        selected_vars = sorted(selected_vars)
    else:
        selected_vars = set(var_name_list)  # Load all variables if none specified

    # Get analysis time
    time_anal = grbs_file.message(1).analDate
    time_stamp_hr = grbs_file.message(1).forecastTime

    # Output dictionary
    array_dict = {'time_analysis': time_anal, 'forecastTime': time_stamp_hr}

    # Read dimensions from first message
    first_var = next(iter(selected_vars))  # Get any available variable
    first_level = level_list[0]
    data_tmp, lat_arr_2D, lon_arr_2D = grbs_file.select(name=first_var, level=first_level)[0].data()
    array_dict['lat'] = lat_arr_2D
    array_dict['lon'] = lon_arr_2D

    # Initialize 3D arrays for selected variables
    for var_name in selected_vars:
        array_dict[var_name] = np.zeros((1, len(level_list), lat_arr_2D.shape[0], lon_arr_2D.shape[1])) * np.nan
        for z_, level_ in enumerate(level_list):
            try:
                array_dict[var_name][0, z_, :, :] = grbs_file.select(name=var_name, level=level_)[0].data()[0]
            except BaseException as error_msg:
                print(f"Warning: {var_name} at level {level_} not found in the file.")

    grbs_file.close()
    return array_dict


# netcdf file handling
def nc_file_from_memory(memory_object):
    return nc.Dataset('inmemory.nc', diskless=True, memory=memory_object)
def nc_show_variable_info(nc_file, var_name=None):
    # open file in case the nc_file argument is a filename, close it when done
    close_nc=False
    if type(nc_file) == str:
        nc_file = nc.Dataset(nc_file)
        close_nc = True

    if var_name is None:
        variables_ =  sorted(nc_file.variables)
        variables_char_sizes = []
        for var_ in variables_:
            variables_char_sizes.append(len(var_))
        max_var_char_size = np.max(variables_char_sizes)
        parameter_list = ''
        fill_len = len(str(len(variables_)))
        for i, parameter_ in enumerate(variables_):
            parameter_list +=  str(i).rjust(fill_len) + " ---> " + str(parameter_) + \
                               str('').rjust(1 + max_var_char_size - len(parameter_)) + \
                str(nc_file.variables[parameter_].shape) + '\n'
        print(parameter_list)
    else:
        print(nc_file.variables[var_name])

    if close_nc: nc_file.close()
def nc_show_variable_info_extended(nc_file, show_units=True):
    # open file in case the nc_file argument is a filename, close it when done
    close_nc=False
    if type(nc_file) == str:
        nc_file = nc.Dataset(nc_file)
        close_nc = True

    var_name_list = sorted(nc_file.variables)

    for var_ in var_name_list:
        try:
            if show_units:
                print(var_,'|', nc_file[var_].shape,'|', nc_file[var_].dimensions,'|',nc_file[var_].units)
            else:
                print(var_,'|', nc_file[var_].shape,'|', nc_file[var_].dimensions)
        except:
            print(var_,'|', nc_file[var_].shape,'|', nc_file[var_].dimensions)


    if close_nc: nc_file.close()

def load_spatiotemporal_netcdf_to_dictionary(filename_,
                                             time_dimension_name='time',
                                             level_dimension_name='level',
                                             lat_dimension_name='lat',
                                             lon_dimension_name='lon',
                                             var_list=None,
                                             time_tuple_start_stop_index=(0, -1),
                                             level_tuple_start_stop_index=(0, -1),
                                             lat_tuple_start_stop_index=(0, -1),
                                             lon_tuple_start_stop_index=(0, -1),
                                             print_debug=True
                                             ):
    """
    creates a dictionary from a netcdf file the netcdf must have only four dimensions for the data variables, where
      time is the first dimension, height levels is the second, lat is the third, and lon is the last
      the four dimensional variables must be non dependent on each other (1D).
    :param filename_: filename with path of a netCDF4 file
    :param time_dimension_name: name of time dimension
    :param level_dimension_name: name of height/level dimension
    :param lat_dimension_name: name of latitude dimension
    :param lon_dimension_name: name of longitude dimension
    :param var_list: list of variables to be loaded, if none, all variables will be loaded
    :param time_tuple_start_stop_index: tuple with the indexes of start and end time to be loaded
    :param level_tuple_start_stop_index: tuple with the indexes of start and end levels to be loaded
    :param lat_tuple_start_stop_index: tuple with the indexes of start and end lat to be loaded
    :param lon_tuple_start_stop_index: tuple with the indexes of start and end lon to be loaded
    :return: dict_: have a dimensions key, a variables key, and a attributes key.
    Each var have a data key equal to a numpy array (can be masked) and a attribute key
    Each var have a dimensions key equal to a tuple, in the same order as the array's dimensions
    all attributes are tuples with name and description text
    """
    # create output dict
    out_dict = {}

    # open file
    file_obj = nc.Dataset(filename_, 'r')  # ,format='NETCDF4_CLASSIC')
    if print_debug: print('output file started')

    # get file's attr
    file_att_list_tuple = []
    for attr_ in file_obj.ncattrs():
        file_att_list_tuple.append((attr_, file_obj.getncattr(attr_)))
    out_dict['attributes'] = file_att_list_tuple

    # get dimensions
    out_dict['dimensions'] = sorted(file_obj.dimensions)

    # get variables
    if var_list is None:
        var_list = sorted(file_obj.variables)
    out_dict['variables'] = {}

    # check that time, lat, and lon are in dimensions and variables
    if time_dimension_name not in out_dict['dimensions']:
        raise ValueError('{0} is not in the dimension list of the nc file'.format(time_dimension_name))
    if level_dimension_name not in out_dict['dimensions']:
        raise ValueError('{0} is not in the dimension list of the nc file'.format(level_dimension_name))
    if lat_dimension_name not in out_dict['dimensions']:
        raise ValueError('{0} is not in the dimension list of the nc file'.format(lat_dimension_name))
    if lon_dimension_name not in out_dict['dimensions']:
        raise ValueError('{0} is not in the dimension list of the nc file'.format(lon_dimension_name))
    if time_dimension_name not in var_list:
        raise ValueError('{0} is not in the variable list of the nc file'.format(time_dimension_name))
    if level_dimension_name not in var_list:
        raise ValueError('{0} is not in the variable list of the nc file'.format(level_dimension_name))
    if lat_dimension_name not in var_list:
        raise ValueError('{0} is not in the variable list of the nc file'.format(lat_dimension_name))
    if lon_dimension_name not in var_list:
        raise ValueError('{0} is not in the variable list of the nc file'.format(lon_dimension_name))


    # get time, lat, and lon arrays
    nc_time = file_obj.variables[time_dimension_name][:].filled(np.nan)
    nc_lev = file_obj.variables[level_dimension_name][:].filled(np.nan)
    nc_lat = file_obj.variables[lat_dimension_name][:].filled(np.nan)
    nc_lon = file_obj.variables[lon_dimension_name][:].filled(np.nan)

    t_1, t_2 = time_tuple_start_stop_index
    l_1, l_2 = level_tuple_start_stop_index
    lat_1, lat_2 = lat_tuple_start_stop_index
    lon_1, lon_2 = lon_tuple_start_stop_index

    if t_2 == -1:       t_2      = nc_time.shape[0]
    if l_2 == -1:       l_2      = nc_lev.shape[0]
    if lat_2 == -1:     lat_2    = nc_lat.shape[0]
    if lon_2 == -1:     lon_2    = nc_lon.shape[0]

    # create variables
    for var_ in var_list:
        if var_ == time_dimension_name:
            out_dict['variables'][var_] = {}

            out_dict['variables'][var_]['data'] = file_obj.variables[var_][t_1:t_2]
            out_dict['variables'][var_]['attributes'] = file_obj.variables[var_].ncattrs()

            var_att_list_tuple = []
            for attr_ in file_obj.variables[var_].ncattrs():
                var_att_list_tuple.append((attr_, file_obj.variables[var_].getncattr(attr_)))
            out_dict['variables'][var_]['attributes'] = var_att_list_tuple

            out_dict['variables'][var_]['dimensions'] = file_obj.variables[var_].dimensions
        elif var_ == level_dimension_name:
            out_dict['variables'][var_] = {}

            out_dict['variables'][var_]['data'] = file_obj.variables[var_][l_1:l_2]
            out_dict['variables'][var_]['attributes'] = file_obj.variables[var_].ncattrs()

            var_att_list_tuple = []
            for attr_ in file_obj.variables[var_].ncattrs():
                var_att_list_tuple.append((attr_, file_obj.variables[var_].getncattr(attr_)))
            out_dict['variables'][var_]['attributes'] = var_att_list_tuple

            out_dict['variables'][var_]['dimensions'] = file_obj.variables[var_].dimensions
        elif var_ == lat_dimension_name:
            out_dict['variables'][var_] = {}

            out_dict['variables'][var_]['data'] = file_obj.variables[var_][lat_1:lat_2]
            out_dict['variables'][var_]['attributes'] = file_obj.variables[var_].ncattrs()

            var_att_list_tuple = []
            for attr_ in file_obj.variables[var_].ncattrs():
                var_att_list_tuple.append((attr_, file_obj.variables[var_].getncattr(attr_)))
            out_dict['variables'][var_]['attributes'] = var_att_list_tuple

            out_dict['variables'][var_]['dimensions'] = file_obj.variables[var_].dimensions
        elif var_ == lon_dimension_name:
            out_dict['variables'][var_] = {}

            out_dict['variables'][var_]['data'] = file_obj.variables[var_][lon_1:lon_2]
            out_dict['variables'][var_]['attributes'] = file_obj.variables[var_].ncattrs()

            var_att_list_tuple = []
            for attr_ in file_obj.variables[var_].ncattrs():
                var_att_list_tuple.append((attr_, file_obj.variables[var_].getncattr(attr_)))
            out_dict['variables'][var_]['attributes'] = var_att_list_tuple

            out_dict['variables'][var_]['dimensions'] = file_obj.variables[var_].dimensions
        else:
            out_dict['variables'][var_] = {}

            out_dict['variables'][var_]['data'] = file_obj.variables[var_][t_1:t_2, l_1:l_2,
                                                  lat_1:lat_2, lon_1:lon_2]
            out_dict['variables'][var_]['attributes'] = file_obj.variables[var_].ncattrs()

            var_att_list_tuple = []
            for attr_ in file_obj.variables[var_].ncattrs():
                var_att_list_tuple.append((attr_, file_obj.variables[var_].getncattr(attr_)))
            out_dict['variables'][var_]['attributes'] = var_att_list_tuple

            out_dict['variables'][var_]['dimensions'] = file_obj.variables[var_].dimensions

        if print_debug: print('read variable', var_)

    file_obj.close()

    if print_debug: print('Done!')

    return out_dict

def netCDF_crop_space_domain(input_filename, min_lat, max_lat, min_lon, max_lon,
                             output_filename=None, vars_to_keep=None,
                             lat_dimension_name='lat', lon_dimension_name='lon', print_debug=True):
    """
    this function crops the data from the inputed file with respect to domain.
    it will create a new file that only includes data within the given latitude and longitude bounds.
    IMPORTANT: lat and lon dimensions must be the last two dimensions, in that order.
    :param input_filename: netCDF4 file with path
    :param min_lat: float with minimum latitude to be included in the output file
    :param max_lat: float with maximum latitude to be included in the output file
    :param min_lon: float with minimum longitude to be included in the output file
    :param max_lon: float with maximum longitude to be included in the output file
    :param output_filename: filename with path and .nc extension. If none, output file will be in same folder as input
    :param vars_to_keep: list of variable names in str to be kept in output copy. If none, all variables will be copied
    :param lat_dimension_name: name of latitude dimension
    :param lon_dimension_name: name of longitude dimension
    :return:  0 if good, filename if error
    """

    error_file = 0

    try:

        nc_input_file = nc.Dataset(input_filename)
        lat_array = nc_input_file.variables[lat_dimension_name][:].copy()
        lon_array = nc_input_file.variables[lon_dimension_name][:].copy()
        nc_input_file.close()

        if len(lat_array.shape) == 1:
            lat_1 = time_to_row_sec(lat_array, min_lat)
            lat_2 = time_to_row_sec(lat_array, max_lat)
            lon_1 = time_to_row_sec(lon_array, min_lon)
            lon_2 = time_to_row_sec(lon_array, max_lon)
        else:
            lat_1, lon_2  = find_index_from_lat_lon_2D_arrays(lat_array, lon_array, max_lat, min_lon)
            lat_2, lon_1  = find_index_from_lat_lon_2D_arrays(lat_array, lon_array, min_lat, max_lon)

        r_1 = np.min([lat_1, lat_2])
        r_2 = np.max([lat_1, lat_2])
        c_1 = np.min([lon_1, lon_2])
        c_2 = np.max([lon_1, lon_2])

        dict_ = load_netcdf_to_dictionary(input_filename, var_list=vars_to_keep, print_debug=print_debug)

        dict_output = {}

        variable_names_list = sorted(dict_['variables'].keys())

        dict_output['attributes'] = dict_['attributes']
        dict_output['attributes'].append(('data spatially cropped between min_lat, max_lat, min_lon, max_lon',
                                          str(min_lat) +','+ str(max_lat) +','+ str(min_lon) +','+ str(max_lon)))
        dict_output['dimensions'] = dict_['dimensions']
        dict_output['variables'] = {}

        for var_name in variable_names_list:
            dict_output['variables'][var_name] = {}

            dict_output['variables'][var_name]['attributes'] = dict_['variables'][var_name]['attributes']
            dict_output['variables'][var_name]['dimensions'] = dict_['variables'][var_name]['dimensions']

            if var_name == lat_dimension_name:
                if len(dict_['variables'][var_name]['dimensions']) == 1: # 1d constant latitude array
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data'][r_1:r_2]
                elif len(dict_['variables'][var_name]['dimensions']) == 2: # 2d latitude array that varies with longitude
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data'][r_1:r_2,c_1:c_2]
                else: # 3d latitude array that varies with longitude and time
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data'][...,r_1:r_2,c_1:c_2]
            elif var_name == lon_dimension_name:
                if len(dict_['variables'][var_name]['dimensions']) == 1: # 1d constant longitude array
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data'][c_1:c_2]
                elif len(dict_['variables'][var_name]['dimensions']) == 2: # 2d longitude array that varies with latitude
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data'][r_1:r_2,c_1:c_2]
                else: # 3d longitude array that varies with latitude and time
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data'][...,r_1:r_2,c_1:c_2]
            else:
                if lat_dimension_name in dict_['variables'][var_name]['dimensions']: # spatial variable
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data'][...,r_1:r_2,c_1:c_2]
                else: # non spatial variable
                    dict_output['variables'][var_name]['data'] = dict_['variables'][var_name]['data']


        if output_filename is None:
            output_filename = input_filename[:-3] + '_cropped_' + str(min_lat) + '_' + str(max_lat) + str(min_lon) + '_' + str(max_lon) + '.nc'

        save_dictionary_to_netcdf(dict_output, output_filename, print_debug=print_debug)


    except BaseException as error_msg:
        print(error_msg)
        error_file = input_filename

    return error_file
def netCDF_crop_timewise(input_filename, time_stamp_start_str_YYYYmmDDHHMM, time_stamp_stop_str_YYYYmmDDHHMM,
                         output_filename=None, vars_to_keep=None, time_dimension_name='time'):
    """
    Creates a copy of an input netCDF4 file with only a subset of the data
    :param input_filename: netCDF4 file with path
    :param time_stamp_start_str_YYYYmmDDHHMMSS: String in YYYYmmDDHHMMSS format
    :param time_stamp_stop_str_YYYYmmDDHHMMSS:
    :param output_filename: filename with path and .nc extension. If none, output file will be in same folder as input
    :param vars_to_keep: list of variable names in str to be kept in output copy. If none, all variables will be copied
    :param time_dimension_name:  name of time dimension
    :return: 0 if good, filename if error
    """
    error_file = 0

    try:

        nc_input_file = nc.Dataset(input_filename)
        time_array = nc_input_file.variables[time_dimension_name][:].copy()
        nc_input_file.close()

        r_1 = time_to_row_str(time_array, time_stamp_start_str_YYYYmmDDHHMM)
        r_2 = time_to_row_str(time_array, time_stamp_stop_str_YYYYmmDDHHMM)

        dict_ = load_spatiotemporal_netcdf_to_dictionary(
            input_filename,
            var_list=vars_to_keep,
            time_tuple_start_stop_index=(r_1,r_2),
            time_dimension_name=time_dimension_name)

        if output_filename is None:
            output_filename = input_filename[:-3] + '_trimmed_' + str(r_1) + '_' + str(r_2) + '.nc'

        save_dictionary_to_netcdf(dict_, output_filename)


    except BaseException as error_msg:
        print(error_msg)
        error_file = input_filename

    return error_file
def add_variable_to_netcdf_file(nc_filename, variables_dict):
    """
    Opens and adds a variable(s) to the file. Will not add new dimensions.
    :param nc_filename: str including path
    :param variables_dict:
    must be a dictionary with keys as variables. inside each variables key should have a dictionary
    inside with variable names as keys
    Each var most have a data key equal to a numpy array (can be masked) and a attribute key
    Each var most have a dimensions key equal to a tuple, in the same order as the array's dimensions
    Each var most have a attributes key equal to a list of tuples with name and description text
    :return: None
    """
    # check if dict_ has the right format

    # create dimension and variables lists
    vars_list = variables_dict.keys()
    for var_ in vars_list:
        if 'dimensions' in variables_dict[var_].keys():
            pass
        else:
            print('dictionary has the wrong format, ' + var_ + 'variable is missing its dimensions')
            return
        if 'attributes' in variables_dict[var_].keys():
            pass
        else:
            print('dictionary has the wrong format, ' + var_ + 'variable is missing its attributes')
            return

    # open file
    file_obj = nc.Dataset(nc_filename,'a')
    print('file openned, do not close this threat or file might be corrupted')

    try:
        # check that variable shapes agree with destination file
        for var_ in vars_list:
            dim_list = list(variables_dict[var_]['dimensions'])
            var_shape = variables_dict[var_]['data'].shape
            for i_, dim_ in enumerate(dim_list):
                if dim_ in sorted(file_obj.dimensions):
                    if var_shape[i_] == file_obj.dimensions[dim_].size:
                        pass
                    else:
                        print('Variable', var_, 'has dimension', dim_,
                              'of different size compared to destination file\nfile closed')
                        file_obj.close()
                        return
                else:
                    print('Variable', var_, 'has dimension', dim_,
                          'which does not exist in destination file\nfile closed')
                    file_obj.close()
                    return

            # create variables
            print('creating', var_, 'variable')
            file_obj.createVariable(var_,
                                    variables_dict[var_]['data'].dtype,
                                    variables_dict[var_]['dimensions'], zlib=True)

            # populate variables
            file_obj.variables[var_][:] = variables_dict[var_]['data']

            for var_attr in variables_dict[var_]['attributes']:
                if var_attr[0] == '_FillValue' or var_attr[0] == 'fill_value':
                    pass
                else:
                    setattr(file_obj.variables[var_], var_attr[0], var_attr[1])

            print('created', var_, 'variable')

    except BaseException as error_msg:
        file_obj.close()
        print('error, file closed\n', error_msg)


    print('All good, closing file')
    file_obj.close()
    print('Done!')
def save_dictionary_to_netcdf(dict_, output_filename, print_debug=True ):
    """
    Saves a dictionary with the right format to a netcdf file. First dim will be set to unlimited.
    :param dict_: must have a dimensions key, a variables key, and a attributes key.
    dimensions key should have a list of the names of the dimensions
    variables key should have a dictionary inside with variable names as keys
    attributes key should have a list of tuples inside, with the name of the attribute and description in each tuple
    Each var most have a data key equal to a numpy array (can be masked) and a attribute key
    Each var most have a dimensions key equal to a tuple, in the same order as the array's dimensions
    all attributes are tuples with name and description text, if scale_factor, add_offset, _FillValue, or missing_value
    are in any of the variables attributes these will be removed from the saved list, this is beacuse these attributes
    are generated by the netcdf module and could potentially (depending on the version) affect the data values.
    :param output_filename: should include full path and extension
    :return: None
    """
    """
    dict_ = {}
    dict_['variables'] = {}
    dict_['dimensions'] = ('time', 'range')

    attribute_list = [
        ('author', 'Luis Ackermann'),
        ('author email', 'ackermannluis@gmail.com'),
        ('version', '4'),
        ('time of file creation', time_seconds_to_str(time.time(), '%Y-%m-%d_%H:%M UTC')),
    ]
    dict_['attributes'] = attribute_list

    # time
    day_time_str = time_seconds_to_str(time_period_start_secs,  '%Y-%m-%d_%H:%M:%S UTC')
    dict_['variables']['time'] = {}
    dict_['variables']['time']['dimensions'] = ('time',)
    dict_['variables']['time']['attributes'] = [
        ('units', 'seconds since ' + day_time_str),
        ('description', 'time stamp is at beginning of average period')]
    dict_['variables']['time']['data'] = time_array[r_e_1:r_e_2] - time_period_start_secs

    # range
    dict_['variables']['range'] = {}
    dict_['variables']['range']['dimensions'] = ('range',)
    dict_['variables']['range']['attributes'] = [
        ('units', 'm'),
        ('description', 'height of sample in meters above instrument')]
    dict_['variables']['range']['data'] = range_array

    # Ze
    dict_['variables']['Ze'] = {}
    dict_['variables']['Ze']['dimensions'] = ('time', 'range',)
    dict_['variables']['Ze']['attributes'] = [
        ('units', 'dB'),
        ('description', 'computed by ImProToo_mod from linearized MRR-Pro spectrum_reflectivity'),
        ('long_name', 'effective reflectivity corrected using Ze_metek below melted layer'),
        ('correction_applied' , merged_nc.variables['Ze'].correction_applied),
        ('correlation_between_melted_metek_and_improtoo_R2',
         merged_nc.variables['Ze'].correlation_between_melted_metek_and_improtoo_R2),
        ('note', 'linearized => 10**(spectrum_reflectivity/10)')
        ]
    dict_['variables']['Ze']['data'] = Ze_array[r_e_1:r_e_2,:]

    save_dictionary_to_netcdf(dict_, path_output + 'MRR_CM_sub_' + day_str + '.nc')
    """
    # check if dict_ has the right format
    if 'variables' in dict_.keys():
        pass
    else:
        print('dictionary has the wrong format, missing variables key')
        return
    if 'dimensions' in dict_.keys():
        pass
    else:
        print('dictionary has the wrong format, missing dimensions key')
        return
    if 'attributes' in dict_.keys():
        pass
    else:
        print('dictionary has the wrong format, missing attributes key')
        return
    # create dimension and variables lists
    vars_list = dict_['variables'].keys()
    dims_list = dict_['dimensions']
    for dim_ in dims_list:
        if dim_ in vars_list:
            pass
        else:
            print('dictionary has the wrong format, ' + dim_ + 'dimension is missing from variables')
    for var_ in vars_list:
        if 'dimensions' in dict_['variables'][var_].keys():
            pass
        else:
            print('dictionary has the wrong format, ' + var_ + 'variable is missing its dimensions')
            return
        if 'attributes' in dict_['variables'][var_].keys():
            pass
        else:
            print('dictionary has the wrong format, ' + var_ + 'variable is missing its attributes')
            return

    # create output file
    file_obj = nc.Dataset(output_filename,'w')#,format='NETCDF4_CLASSIC')
    if print_debug: print('output file started')

    # populate file's attributes
    for attribute_ in dict_['attributes']:
        setattr(file_obj, attribute_[0], attribute_[1])


    # create dimensions
    for i_, dim_ in enumerate(dims_list):
        if i_ == 0:
            file_obj.createDimension(dim_, size=0)
        else:
            shape_index = np.argwhere(np.array(dict_['variables'][dim_]['dimensions']) == dim_)[0][0]
            file_obj.createDimension(dim_, dict_['variables'][dim_]['data'].shape[shape_index])
    if print_debug: print('dimensions created')


    list_of_attributes_to_delete = ['scale_factor', 'add_offset', '_FillValue', 'missing_value', 'fill_value']

    # create variables
    for var_ in vars_list:
        if print_debug: print('creating', var_, 'variable')
        if '<U' in str(dict_['variables'][var_]['data'].dtype):
            file_obj.createVariable(var_,
                                    dict_['variables'][var_]['data'].dtype,
                                    dict_['variables'][var_]['dimensions'])
        else:
            file_obj.createVariable(var_,
                                    dict_['variables'][var_]['data'].dtype,
                                    dict_['variables'][var_]['dimensions'], zlib=True)

        # populate variables
        file_obj.variables[var_][:] = dict_['variables'][var_]['data']

        for var_attr in dict_['variables'][var_]['attributes']:
            if isinstance(var_attr[0], str) and isinstance(var_attr[1], str):
                if var_attr[0] in list_of_attributes_to_delete:
                    pass
                else:
                    setattr(file_obj.variables[var_], var_attr[0], var_attr[1])
        if print_debug: print('created', var_, 'variable')

    if print_debug: print('storing data to disk and closing file')
    file_obj.close()
    if print_debug: print('Done!')
def load_netcdf_to_dictionary(filename_, var_list=None, time_tuple_start_stop_row=None, time_dimension_name='time',
                              print_debug=True):
    """
    creates a dictionary from a netcdf file, with the following format
    :param filename_: filename with path of a netCDF4 file
    :param var_list: list of variables to be loaded, if none, all variables will be loaded
    :param time_tuple_start_stop_str: tuple with two time rows, time dimension will be trimmed r_1:r_2
    :param time_dimension_name:  name of time dimension
    :return: dict_: have a dimensions key, a variables key, and a attributes key.
    Each var have a data key equal to a numpy array (can be masked) and a attribute key
    Each var have a dimensions key equal to a tuple, in the same order as the array's dimensions
    all attributes are tuples with name and description text
    """
    # create output dict
    out_dict = {}

    # open file
    file_obj = nc.Dataset(filename_, 'r')  # ,format='NETCDF4_CLASSIC')
    if print_debug: print(f'Reading data from file: {filename_}')

    # get file's attr
    file_att_list_tuple = []
    for attr_ in file_obj.ncattrs():
        file_att_list_tuple.append((attr_, file_obj.getncattr(attr_)))
    out_dict['attributes'] = file_att_list_tuple

    # get dimensions
    out_dict['dimensions'] = sorted(file_obj.dimensions)

    # get variables
    if var_list is None:
        var_list = sorted(file_obj.variables)
    out_dict['variables'] = {}

    # create variables
    for var_ in var_list:
        out_dict['variables'][var_] = {}


        if time_tuple_start_stop_row is not None:
            if time_dimension_name in file_obj.variables[var_].dimensions:
                out_dict['variables'][var_]['data'] = file_obj.variables[var_][time_tuple_start_stop_row[0]:
                                                                               time_tuple_start_stop_row[1]]
            else:
                out_dict['variables'][var_]['data'] = file_obj.variables[var_][:]
        else:
            out_dict['variables'][var_]['data'] = file_obj.variables[var_][:]

        out_dict['variables'][var_]['attributes'] = file_obj.variables[var_].ncattrs()
        var_att_list_tuple = []
        for attr_ in file_obj.variables[var_].ncattrs():
            var_att_list_tuple.append((attr_, file_obj.variables[var_].getncattr(attr_)))
        out_dict['variables'][var_]['attributes'] = var_att_list_tuple

        out_dict['variables'][var_]['dimensions'] = file_obj.variables[var_].dimensions

        if print_debug: print('read variable', var_)
    file_obj.close()
    if print_debug: print('All data loaded!')

    return out_dict


def merge_multiple_netCDF_by_time_dimension(directory_where_nc_file_are_in_chronological_order, output_path='',
                                            time_variable_name='time', time_dimension_name=None,
                                            vars_to_keep=None, nonTimeVars_check_list=None,
                                            key_search_str='', seek_in_subfolders=False, force_file_list=None,
                                            time_variable_transform_format=None, time_variable_transform_scale=1,
                                            force_output_filename=None, use_file_time_for_name=False,
                                            output_filename_prefix='', verbose_=False):
    """
    Merges multiple files of netcdf format into one file with the name of the first file in the list with '_merged'
    :param directory_where_nc_file_are_in_chronological_order: string with the full path of the folder where the files are
    :param output_path: string with path where the merged file will be saved, if '' is provided, merged file will be
    saved in the same path where source.
    :param time_variable_name: string with the name of the time variable
    :param time_dimension_name: string with the name of the time variable, usefull when the variable and dimension
    names don't match (WRF)
    :param vars_to_keep: list of variables to keep in the merged file, if none provided, all variables will be kept
    :param nonTimeVars_check_list: list of variable names to check that they have the same values if they do not have
    a time dimension. Useful to check if for example the latitude has changed
    :param key_search_str: string that if provided, will be used to filter files from the input path, say you only
    want to merge files in the folder that have the string 'd03_' in their name
    :param seek_in_subfolders: If true, files in subfolders will be searched for the merger
    :param force_file_list: if a list of filenames is provided, then this will be used to merge regardless of contents
     of input folder, in the list order.
    :param time_variable_transform_format: string. if provided, it will be used to transform the values of the time
     variable to seconds since 1970-01-01T00:00:00Z (unix epoch). This assumes the start time is provided in the time
     variable units. Example: if the units attribute of the time variable says 'seconds since 2019-07-15T00:00:29Z',
     then set time_variable_transform to 'seconds since %Y-%m-%dT%H:%M:%SZ' and time_variable_transform_scale=1.
     if the units attribute of the time variable says 'hours since 2019-07-15 00:00',
     then set time_variable_transform to 'hours since %Y-%m-%d %H:%M' and time_variable_transform_scale=3600.
    :param time_variable_transform_scale: scalar that is only used if time_variable_transform is not None. Represent
     number of seconds per time variable unit
    :param force_output_filename: string used for merged file output. Assume full path is given and extension.
     If not none, output_path will be ignored as well as use_file_time_for_name and output_filename_prefix.
    :param use_file_time_for_name: boolean, if true the output filename will be
     output_path / output_filename_prefix _ time_start_YYYYmmDDHHMM _ time_stop_YYYYmmDDHHMM _ .nc
     If not none, output_path will be ignored.
    :param output_filename_prefix: string used in output filename when output_path and or use_file_time_for_name is set
     unless force_output_filename is set.
    :param verbose_: bool, if true will print status messages.
    :return:
    """
    if time_dimension_name is None: time_dimension_name = time_variable_name

    if force_file_list is not None:
        file_list_all = sorted(force_file_list)
    else:
        if seek_in_subfolders:
            if key_search_str == '':
                file_list_all = sorted(list_files_recursive(directory_where_nc_file_are_in_chronological_order))
            else:
                file_list_all = sorted(list_files_recursive(directory_where_nc_file_are_in_chronological_order,
                                                            filter_str=key_search_str))

        else:
            file_list_all = sorted(glob.glob(str(directory_where_nc_file_are_in_chronological_order
                                                 + '*' + key_search_str + '*.nc')))

    if verbose_: print('Files to be merged (in this order):')
    parameter_list = ''
    for i, parameter_ in enumerate(file_list_all):
        parameter_list = str(parameter_list) + str(i) + " ---> " + str(parameter_) + '\n'
    if verbose_: print(parameter_list)

    # create copy of first file in a temporary location
    with tempfile.TemporaryDirectory() as tmpdir1_obj:
        output_path_temp = str(Path_lib(tmpdir1_obj)) + '/'
        output_filename_temp = output_path_temp + 'temp_file_merging.nc'

        # check if time dimension is unlimited
        netcdf_first_file_object = nc.Dataset(file_list_all[0], 'r')

        if netcdf_first_file_object.dimensions[time_dimension_name].size == 0 and vars_to_keep is None:
            # all good, just make copy of file with output_filename name
            netcdf_first_file_object.close()
            shutil.copyfile(file_list_all[0], output_filename_temp)
            if verbose_: print('first file in merger list has unlimited time dimension, copy created with name:',
                               output_filename_temp)
        else:
            # not so good, create new file and copy everything from first, make time dimension unlimited...
            netcdf_output_file_object = nc.Dataset(output_filename_temp, 'w')
            if verbose_: print(
                'first file in merger list does not have unlimited time dimension, new file created with name:',
                output_filename_temp)

            # copy main attributes
            attr_list = netcdf_first_file_object.ncattrs()
            for attr_ in attr_list:
                netcdf_output_file_object.setncattr(attr_, netcdf_first_file_object.getncattr(attr_))
            if verbose_: print('main attributes copied')

            # create list for dimensions and variables
            dimension_names_list = sorted(netcdf_first_file_object.dimensions)
            if vars_to_keep is None:
                variable_names_list = sorted(netcdf_first_file_object.variables)
            else:
                variable_names_list = vars_to_keep

            # create dimensions
            for dim_name in dimension_names_list:
                if dim_name == time_dimension_name:
                    netcdf_output_file_object.createDimension(time_dimension_name, size=0)
                    if verbose_: print(time_dimension_name, 'dimension created')
                else:
                    netcdf_output_file_object.createDimension(dim_name,
                                                              size=netcdf_first_file_object.dimensions[dim_name].size)
                    if verbose_: print(dim_name, 'dimension created')

            # create variables
            for var_name in variable_names_list:

                if time_variable_transform_format is None or var_name != time_variable_name:
                    # create
                    if netcdf_first_file_object.variables[var_name].dtype == str:
                        netcdf_output_file_object.createVariable(var_name,
                                                                 netcdf_first_file_object.variables[var_name].dtype,
                                                                 netcdf_first_file_object.variables[
                                                                     var_name].dimensions,
                                                                 fill_value=-9999)
                    else:
                        netcdf_output_file_object.createVariable(var_name,
                                                                 netcdf_first_file_object.variables[var_name].dtype,
                                                                 netcdf_first_file_object.variables[
                                                                     var_name].dimensions,
                                                                 zlib=True, fill_value=-9999)
                    if verbose_: print(var_name, 'variable created')

                    # copy the attributes
                    attr_list = netcdf_first_file_object.variables[var_name].ncattrs()
                    for attr_ in attr_list:
                        if attr_ == '_FillValue':
                            pass
                        else:
                            netcdf_output_file_object.variables[var_name].setncattr(attr_,
                                                                                    netcdf_first_file_object.variables[
                                                                                        var_name].getncattr(attr_))
                    if verbose_: print('variable attributes copied')

                    # copy the data to the new file
                    netcdf_output_file_object.variables[var_name][:] = netcdf_first_file_object.variables[var_name][
                                                                       :].copy()
                    if verbose_: print('variable data copied')

                    if verbose_: print('-=' * 20)
                elif time_variable_transform_format is not None and var_name == time_variable_name:
                    # create
                    netcdf_output_file_object.createVariable(var_name,
                                                             netcdf_first_file_object.variables[var_name].dtype,
                                                             netcdf_first_file_object.variables[var_name].dimensions,
                                                             zlib=True, fill_value=-9999)
                    if verbose_: print(var_name, 'variable created')

                    # copy the attributes
                    attr_list = netcdf_first_file_object.variables[var_name].ncattrs()
                    for attr_ in attr_list:
                        if attr_ == '_FillValue':
                            pass
                        else:
                            netcdf_output_file_object.variables[var_name].setncattr(attr_,
                                                                                    netcdf_first_file_object.variables[
                                                                                        var_name].getncattr(attr_))
                    netcdf_output_file_object.variables[var_name].setncattr('units',
                                                                            'seconds since 1970-01-01T00:00:00Z')
                    if verbose_: print('variable attributes copied')

                    # copy the data to the new file
                    time_data = (time_variable_transform_scale * netcdf_first_file_object.variables[var_name][
                                                                 :].copy()) + \
                                time_str_to_seconds(netcdf_first_file_object.variables[var_name].units,
                                                    time_variable_transform_format)
                    netcdf_output_file_object.variables[var_name][:] = time_data
                    if verbose_: print('variable data copied')

                    if verbose_: print('-=' * 20)

            # close all files
            netcdf_output_file_object.close()
            netcdf_first_file_object.close()

        if verbose_: print('starting to copy other files into merged file')

        # open output file for appending data
        netcdf_output_file_object = nc.Dataset(output_filename_temp, 'a')

        if vars_to_keep is None:
            vars_list = sorted(netcdf_output_file_object.variables)
        else:
            vars_list = vars_to_keep

        for filename_ in file_list_all[1:]:

            if verbose_: print('-' * 5)
            if verbose_: print('loading file:', filename_)

            # open hourly file
            netcdf_file_object = nc.Dataset(filename_, 'r')
            # get time array
            time_raw = np.array(netcdf_file_object.variables[time_variable_name][:], dtype=float)

            row_start = netcdf_output_file_object.variables[time_variable_name].shape[0]
            row_end = time_raw.shape[0] + row_start

            if time_variable_transform_format is not None:
                time_data = (time_variable_transform_scale * time_raw) + \
                            time_str_to_seconds(netcdf_file_object.variables[time_variable_name].units,
                                                time_variable_transform_format)
            else:
                time_data = time_raw

            # append time array
            netcdf_output_file_object.variables[time_variable_name][row_start:row_end] = time_data

            # append all other variables that only time dependent
            for var_name in vars_list:
                if var_name != time_variable_name:
                    if time_dimension_name in netcdf_output_file_object.variables[var_name].dimensions:
                        netcdf_output_file_object.variables[var_name][row_start:row_end] = \
                            netcdf_file_object.variables[var_name][:].copy()

            # check non time dependent variables for consistency
            vars_list_sub = sorted(netcdf_file_object.variables)
            if vars_list_sub != sorted(netcdf_first_file_object.variables):
                if verbose_: print('Alert! Variables in first file are different than other files')
                if verbose_: print('first file variables:')
                if verbose_: p_(sorted(netcdf_first_file_object.variables))
                if verbose_: print(filename_, 'file variables:')
                if verbose_: p_(vars_list_sub)

            if nonTimeVars_check_list is not None:
                for var_name in nonTimeVars_check_list:
                    if np.nansum(np.abs(netcdf_file_object.variables[var_name][:].copy() -
                                        netcdf_output_file_object.variables[var_name][:].copy())) != 0:
                        if verbose_: print('Alert!', var_name, 'from file:', filename_, 'does not match the first file')

                        # copy the attributes
                        netcdf_output_file_object.variables[var_name].setncattr(
                            'values from file ' + filename_, netcdf_file_object.variables[var_name][:].copy()
                        )

            netcdf_file_object.close()

        netcdf_output_file_object.close()

        # change output filename as necessary
        if force_output_filename is None:
            if use_file_time_for_name:
                with nc.Dataset(output_filename_temp) as file_:
                    time_tmp_day = convert_any_time_type_to_days(file_.variables[time_variable_name][:].filled(np.nan))
                time_str_start = time_days_to_str(time_tmp_day[0], time_format_YMDHM)
                time_str_stop = time_days_to_str(time_tmp_day[-1], time_format_YMDHM)
                output_filename = output_path + output_filename_prefix + '{0}_{1}_.nc'.format(time_str_start,
                                                                                              time_str_stop)
            elif output_path == '':
                output_filename = file_list_all[0][:-3] + '_merged.nc'
            else:
                output_filename = output_path + file_list_all[0].replace('\\', '/').split('/')[-1][:-3] + '_merged.nc'
        else:
            output_filename = force_output_filename

        if verbose_: print('output filename set to ' + output_filename)

        shutil.copyfile(output_filename_temp, output_filename)
        os.remove(output_filename_temp)

        if verbose_: print('done')

    return output_filename


def compile_WRF_output_files(file_list, output_filename,
                             time_var_name, time_dimension_name,
                             height_dimension_name,
                             lat_var_name, lat_dimension_name,
                             lon_var_name, lon_dimension_name,
                             variable_list_all, variable_list_out):


    # variable_list_all = open_csv_file(path_program + 'WRF_var_list_all.txt')
    # variable_list_out = open_csv_file(path_program + 'WRF_var_list_out.txt')
    # path_input = "E:/WRF_output/aug_new/"
    # output_filename = "C:/_output/wrfout_d03_2015-08.nc"
    # file_list = sorted(glob.glob(str(path_input + '*')))
    # time_var_name = 'Times'
    # time_dimension_name = 'Time'
    # height_dimension_name = 'bottom_top'
    # lat_var_name = 'XLAT'
    # lat_dimension_name = 'south_north'
    # lon_var_name = 'XLONG'
    # lon_dimension_name = 'west_east'
    # compile_WRF_output_files(file_list, output_filename,
    #                          time_var_name, time_dimension_name,
    #                          height_dimension_name,
    #                          lat_var_name, lat_dimension_name,
    #                          lon_var_name, lon_dimension_name,
    #                          variable_list_all, variable_list_out)

    print('started compiling of WRF output files')

    # create dimension dict
    netcdf_file_object = nc.Dataset(file_list[0], 'r')
    file_attribute = netcdf_file_object._attributes
    dimesion_dict = netcdf_file_object.dimensions
    total_time_dimesion = netcdf_file_object.variables[time_var_name].shape[0]

    var_dim_dict = {}
    var_atr_dict = {}
    for variable_name in variable_list_out:
        var_dim_dict[variable_name] = netcdf_file_object.variables[variable_name].dimensions
        var_atr_dict[variable_name] = netcdf_file_object.variables[variable_name]._attributes

    # lat and lon series
    arr_lat = netcdf_file_object.variables[lat_var_name][0,:,:].copy()
    arr_lon = netcdf_file_object.variables[lon_var_name][0,:,:].copy()

    # check if all variables are present
    any_var_missing = False
    var_list_sorted = sorted(list(netcdf_file_object.variables))
    for var_ in variable_list_all:
        if not var_ in var_list_sorted:
            any_var_missing = True
            print(var_ + ' not present in WRF file')
    if any_var_missing:
        print('stopping compiling')
        netcdf_file_object.close()
        # return
    netcdf_file_object.close()

    for filename_ in file_list[1:]:
        netcdf_file_object = nc.Dataset(filename_, 'r')
        total_time_dimesion +=  netcdf_file_object.variables[time_var_name].shape[0]
        netcdf_file_object.close()
    dimesion_dict[time_dimension_name] = total_time_dimesion
    print('calculated all dimensions')


    # calculated variables
    var_list_calc = ['RH','ATP','Temp',
                     'PM2.5 Sulfate',
                     'PM2.5 Ammonium',
                     'PM2.5 Nitrate',
                     'PM2.5 Chloride',
                     'PM2.5 Sodium',
                     'PM2.5 Dust',
                     'PM2.5 OC',
                     'PM2.5 BC',
                     'PM Water',
                     'PM10 Sulfate',
                     'PM10 Ammonium',
                     'PM10 Nitrate',
                     'PM10 Chloride',
                     'PM10 Sodium',
                     'PM10 Dust',
                     'PM10 OC',
                     'PM10 BC',
                     'WS']

    # attributes
    var_atr_dict['RH'] = """tv_ = 6.11 * e_constant**((2500000/461) * ((1/273) - (1/arr_temp)))
                            pv_ = arr_qvapor * (arr_press/100) / (arr_qvapor + 0.622)
                            RH =  100 * pv_ / tv_"""
    var_atr_dict['ATP'] = 'Atmospheric pressure in pascal'
    var_atr_dict['Temp'] = 'Atmospheric temperature in celsius'

    var_atr_dict['PM2.5 Sulfate'] = "so4_a01 + so4_a02 + so4_a03 [in ug/m3]"
    var_atr_dict['PM2.5 Ammonium'] = "nh4_a01 + nh4_a02 + nh4_a03 [in ug/m3]"
    var_atr_dict['PM2.5 Nitrate'] = "no3_a01 + no3_a02 + no3_a03 [in ug/m3]"
    var_atr_dict['PM2.5 Chloride'] = "cl_a01 + cl_a02 + cl_a03 [in ug/m3]"
    var_atr_dict['PM2.5 Sodium'] = "na_a01 + na_a02 + na_a03 [in ug/m3]"
    var_atr_dict['PM2.5 Dust'] = "oin_a01 + oin_a02 + oin_a03 [in ug/m3]"
    var_atr_dict['PM2.5 OC'] = "oc_a01 + oc_a02 + oc_a03 [in ug/m3]"
    var_atr_dict['PM2.5 BC'] = "bc_a01 + bc_a02 + bc_a03 [in ug/m3]"

    var_atr_dict['PM Water'] = "water_a01 + water_a02 + water_a03 + water_a04 [in ug/m3]"

    var_atr_dict['PM10 Sulfate'] = "PM2.5 Sulfate + so4_a04 [in ug/m3]"
    var_atr_dict['PM10 Ammonium'] = "PM2.5 Ammonium + nh4_a04 [in ug/m3]"
    var_atr_dict['PM10 Nitrate'] = "PM2.5 Nitrate + no3_a04 [in ug/m3]"
    var_atr_dict['PM10 Chloride'] = "PM2.5 Chloride + cl_a04 [in ug/m3]"
    var_atr_dict['PM10 Sodium'] = "PM2.5 Sodium + na_a04 [in ug/m3]"
    var_atr_dict['PM10 Dust'] =  "PM2.5 Dust + oin_a04 [in ug/m3]"
    var_atr_dict['PM10 OC'] =  "PM2.5 OC + oc_a04 [in ug/m3]"
    var_atr_dict['PM10 BC'] =  "PM2.5 BC + bc_a04 [in ug/m3]"

    var_atr_dict['WS'] =  "((U**2) + (V**2))**0.5"


    var_dim_dict['RH'] = (time_dimension_name, lat_dimension_name, lon_dimension_name,)
    for variable_name in var_list_calc[1:]:
        var_dim_dict[variable_name] = (time_dimension_name, height_dimension_name, lat_dimension_name, lon_dimension_name,)


    # create file
    netcdf_file_object_out = nc.Dataset(output_filename, 'w')
    for dim_key in dimesion_dict:
        netcdf_file_object_out.createDimension(dim_key, dimesion_dict[dim_key])
        netcdf_file_object_out.createVariable(dim_key, 'f', (dim_key,))
        netcdf_file_object_out.variables[dim_key][:] = np.arange(dimesion_dict[dim_key])
        netcdf_file_object.flush()


    # store file attributes
    for attrib_ in file_attribute.keys():
        if attrib_ != 'variables' and file_attribute[attrib_] is not None:# and attrib_ != 'dimensions' and attrib_ != 'variables'
            setattr(netcdf_file_object_out, attrib_, file_attribute[attrib_])

    print('output file created')


    # create variables
    var_object = netcdf_file_object_out.createVariable(time_var_name, 'f', (time_dimension_name,))
    var_object[:] = 9999
    setattr(var_object, 'description', 'time in YYYYMMDDHHSS format as an integer')
    var_object = netcdf_file_object_out.createVariable(lat_var_name, 'f', (lat_dimension_name, lon_dimension_name))
    var_object[:,:] = arr_lat
    netcdf_file_object_out.flush()
    print(1)
    setattr(var_object, 'description', 'latitude in decimals of the center of the cell')
    var_object = netcdf_file_object_out.createVariable(lon_var_name, 'f', (lat_dimension_name, lon_dimension_name,))
    var_object[:,:] = arr_lon
    netcdf_file_object_out.flush()
    print(2)
    setattr(var_object, 'description', 'longitude in decimals of the center of the cell')

    netcdf_file_object_out.close()
    netcdf_file_object_out = nc.Dataset(output_filename, 'a')
    print('creating hard drive space for variables')
    for variable_name in variable_list_out:
        netcdf_file_object_out.createVariable(variable_name, 'f', var_dim_dict[variable_name])
        for attrib_ in var_atr_dict[variable_name].keys():
            setattr(netcdf_file_object_out.variables[variable_name], attrib_, var_atr_dict[variable_name][attrib_])

    for variable_name in var_list_calc:
        var_object = netcdf_file_object_out.createVariable(variable_name, 'f', var_dim_dict[variable_name])
        for attrib_ in var_atr_dict[variable_name]:
            setattr(var_object, 'description', attrib_)

    netcdf_file_object_out.close()
    print('space created')

    ###############################################################################

    t_s_s = 0
    for filename_ in file_list:
        netcdf_file_object_out = nc.Dataset(output_filename, 'a')
        netcdf_file_object_in = nc.Dataset(filename_, 'r')
        print('reading file: ' + filename_)

        # create time series
        time_series_list = []
        for time_step in range(netcdf_file_object_in.variables[time_var_name].shape[0]):
            time_step_str = ''
            for char_ in range(netcdf_file_object_in.variables[time_var_name].shape[1]):
                time_step_str += str(netcdf_file_object_in.variables[time_var_name][time_step,char_])[2]
            time_step_str = time_step_str.replace('-', '')
            time_step_str = time_step_str.replace('_', '')
            time_step_str = time_step_str.replace(':', '')
            time_step_str = time_step_str.replace(' ', '')
            time_series_list.append(time_step_str)
        print('writing time variable')


        netcdf_file_object_out.variables[time_var_name][t_s_s:t_s_s+len(time_series_list)] = np.array(time_series_list)


        for variable_name in variable_list_out:
            if var_dim_dict[variable_name][0] == time_dimension_name:
                print('writing variable: ' + variable_name)
                netcdf_file_object_out.variables[variable_name][t_s_s:t_s_s+len(time_series_list)] = \
                    netcdf_file_object_in.variables[variable_name][:].copy()


        print('calculating and writing variables')
        QVAPOR_array = netcdf_file_object_in.variables['QVAPOR'][:,0,:,:].copy()
        T2_array = netcdf_file_object_in.variables['T2'][:].copy()
        PSFC_array = netcdf_file_object_in.variables['PSFC'][:].copy()
        # T_array = netcdf_file_object_in.variables['T'][:].copy()

        netcdf_file_object_out.variables['RH'][t_s_s:t_s_s+len(time_series_list)] = calculate_RH_from_QV_T_P(QVAPOR_array, T2_array, PSFC_array)
        netcdf_file_object_out.variables['ATP'][t_s_s:t_s_s+len(time_series_list)] = \
            netcdf_file_object_in.variables['PB'][:] + netcdf_file_object_in.variables['P'][:]
        netcdf_file_object_out.variables['Temp'][t_s_s:t_s_s+len(time_series_list)] = \
            kelvin_to_celsius((netcdf_file_object_in.variables['T'][:] + 300) *
                              (((netcdf_file_object_in.variables['PB'][:] + netcdf_file_object_in.variables['P'][:])*0.01/1000)**(2/7)))

        density_ =  (netcdf_file_object_in.variables['PB'][:] + netcdf_file_object_in.variables['P'][:])/\
                    (287.058*((netcdf_file_object_in.variables['T'][:] + 300) *
                              (((netcdf_file_object_in.variables['PB'][:] + netcdf_file_object_in.variables['P'][:])*0.01/1000)**(2/7))))

        netcdf_file_object_out.variables['PM2.5 Sulfate'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['so4_a01'][:] +
             netcdf_file_object_in.variables['so4_a02'][:] +
             netcdf_file_object_in.variables['so4_a03'][:]) * density_
        netcdf_file_object_out.variables['PM2.5 Ammonium'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['nh4_a01'][:] +
             netcdf_file_object_in.variables['nh4_a02'][:] +
             netcdf_file_object_in.variables['nh4_a03'][:]) * density_
        netcdf_file_object_out.variables['PM2.5 Nitrate'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['no3_a01'][:] +
             netcdf_file_object_in.variables['no3_a02'][:] +
             netcdf_file_object_in.variables['no3_a03'][:]) * density_
        netcdf_file_object_out.variables['PM2.5 Chloride'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['cl_a01'][:] +
             netcdf_file_object_in.variables['cl_a02'][:] +
             netcdf_file_object_in.variables['cl_a03'][:]) * density_
        netcdf_file_object_out.variables['PM2.5 Sodium'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['na_a01'][:] +
             netcdf_file_object_in.variables['na_a02'][:] +
             netcdf_file_object_in.variables['na_a03'][:]) * density_
        netcdf_file_object_out.variables['PM2.5 Dust'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['oin_a01'][:] +
             netcdf_file_object_in.variables['oin_a02'][:] +
             netcdf_file_object_in.variables['oin_a03'][:]) * density_
        netcdf_file_object_out.variables['PM2.5 OC'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['oc_a01'][:] +
             netcdf_file_object_in.variables['oc_a02'][:] +
             netcdf_file_object_in.variables['oc_a03'][:]) * density_
        netcdf_file_object_out.variables['PM2.5 BC'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['bc_a01'][:] +
             netcdf_file_object_in.variables['bc_a02'][:] +
             netcdf_file_object_in.variables['bc_a03'][:]) * density_

        netcdf_file_object_out.variables['PM Water'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['water_a01'][:] +
             netcdf_file_object_in.variables['water_a02'][:] +
             netcdf_file_object_in.variables['water_a03'][:] +
             netcdf_file_object_in.variables['water_a04'][:]) * density_

        netcdf_file_object_out.variables['PM10 Sulfate'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['so4_a01'][:] +
             netcdf_file_object_in.variables['so4_a02'][:] +
             netcdf_file_object_in.variables['so4_a03'][:] +
             netcdf_file_object_in.variables['so4_a04'][:]) * density_
        netcdf_file_object_out.variables['PM10 Ammonium'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['nh4_a01'][:] +
             netcdf_file_object_in.variables['nh4_a02'][:] +
             netcdf_file_object_in.variables['nh4_a03'][:] +
             netcdf_file_object_in.variables['nh4_a04'][:]) * density_
        netcdf_file_object_out.variables['PM10 Nitrate'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['no3_a01'][:] +
             netcdf_file_object_in.variables['no3_a02'][:] +
             netcdf_file_object_in.variables['no3_a03'][:] +
             netcdf_file_object_in.variables['no3_a04'][:]) * density_
        netcdf_file_object_out.variables['PM10 Chloride'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['cl_a01'][:] +
             netcdf_file_object_in.variables['cl_a02'][:] +
             netcdf_file_object_in.variables['cl_a03'][:] +
             netcdf_file_object_in.variables['cl_a04'][:]) * density_
        netcdf_file_object_out.variables['PM10 Sodium'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['na_a01'][:] +
             netcdf_file_object_in.variables['na_a02'][:] +
             netcdf_file_object_in.variables['na_a03'][:] +
             netcdf_file_object_in.variables['na_a04'][:]) * density_
        netcdf_file_object_out.variables['PM10 Dust'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['oin_a01'][:] +
             netcdf_file_object_in.variables['oin_a02'][:] +
             netcdf_file_object_in.variables['oin_a03'][:] +
             netcdf_file_object_in.variables['oin_a04'][:]) * density_
        netcdf_file_object_out.variables['PM10 OC'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['oc_a01'][:] +
             netcdf_file_object_in.variables['oc_a02'][:] +
             netcdf_file_object_in.variables['oc_a03'][:] +
             netcdf_file_object_in.variables['oc_a04'][:]) * density_
        netcdf_file_object_out.variables['PM10 BC'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['bc_a01'][:] +
             netcdf_file_object_in.variables['bc_a02'][:] +
             netcdf_file_object_in.variables['bc_a03'][:] +
             netcdf_file_object_in.variables['bc_a04'][:]) * density_

        netcdf_file_object_out.variables['WS'][t_s_s:t_s_s+len(time_series_list)] = \
            (netcdf_file_object_in.variables['U'][:,:,:,:-1]**2 + netcdf_file_object_in.variables['V'][:,:,:-1,:]**2) ** 0.5



        t_s_s += len(time_series_list)
        netcdf_file_object_in.close()
        netcdf_file_object_out.close()

        print('data from ' + filename_ + ' written into output file')
def load_netcdf_file_variable(filename_, variable_name_list=None):
    netcdf_file_object = nc.Dataset(filename_, 'r')

    file_attributes_dict = {}
    file_var_values_dict = {}
    file_var_attrib_dict = {}
    file_dim_dict = {}

    if variable_name_list is None: variable_name_list = list(netcdf_file_object.variables)

    for atr_ in netcdf_file_object._attributes:
        file_attributes_dict[atr_] = netcdf_file_object._attributes[atr_]

    for dim_ in netcdf_file_object.dimensions:
        file_dim_dict[dim_] = netcdf_file_object.dimensions[dim_]

    for var_ in variable_name_list:
        file_var_values_dict[var_] = netcdf_file_object.variables[var_][:].copy()
        for atr_ in netcdf_file_object.variables[var_]._attributes:
            file_var_attrib_dict[var_] = netcdf_file_object.variables[var_]._attributes[atr_]

    netcdf_file_object.close()

    return file_attributes_dict, file_var_values_dict, file_var_attrib_dict, file_dim_dict
def save_array_list_as_netcdf(array_list, name_list, units_list, attributes_list, out_filename):
    file_object = nc.Dataset(out_filename, 'w')
    # file_object.history = 'Created for a test'

    for variable_ in range(len(array_list)):
        dim_list_name = []
        for dim_ in range(len(array_list[variable_].shape)):
            dim_name = str(variable_) + '_' + str(dim_)
            dim_list_name.append(dim_name)
            file_object.createDimension(dim_name, array_list[variable_].shape[dim_])

        dtype_ = str(array_list[variable_].dtype)[0]

        file_object.createVariable( name_list[variable_], dtype_, tuple(dim_list_name) )



        setattr(file_object.variables[name_list[variable_]], 'units',units_list[variable_])

        file_object.variables[name_list[variable_]] = array_list[variable_]
        # temp_variable_handle[:] = array_list[variable_][:]


    for atri_ in attributes_list:
        setattr(file_object, atri_[0], atri_[1])


    file_object.close()
def save_time_series_as_netcdf(array_list, name_list, units_list, attributes_list, out_filename):
    file_object = nc.Dataset(out_filename, 'w')

    # create time dimension
    file_object.createDimension('time', array_list[0].shape[0])

    for variable_ in range(len(array_list)):
        dtype_ = str(array_list[variable_].dtype)[0]
        if dtype_ == '<': dtype_ = 'S1'
        file_object.createVariable(name_list[variable_], dtype_, ('time',))

        setattr(file_object.variables[name_list[variable_]], 'units',units_list[variable_])

        file_object.variables[name_list[variable_]][:] = array_list[variable_][:]
        # temp_variable_handle[:] = array_list[variable_][:]


    for atri_ in attributes_list:
        setattr(file_object, atri_[0], atri_[1])


    file_object.close()
def save_emissions_to_new_netcdf(out_filename, emissions_array, pollutant_name, time_array, lat_array, lon_array,
                                 file_attributes_tuple_list, pollutant_attributes_tuple_list):
    file_object = nc.Dataset(out_filename, 'w')

    # create dimensions
    file_object.createDimension('lat', lat_array.shape[0])
    file_object.createDimension('lon', lon_array.shape[0])
    file_object.createDimension('time', time_array.shape[0])

    # create dimension variables
    file_object.createVariable('time', str(time_array.dtype)[0], ('time', ))
    file_object.createVariable('lat', str(lat_array.dtype)[0], ('lat',))
    file_object.createVariable('lon', str(lon_array.dtype)[0], ('lon',))

    # populate dimension variables
    file_object.variables['time'][:] = time_array[:]
    file_object.variables['lat'][:] = lat_array[:]
    file_object.variables['lon'][:] = lon_array[:]

    # create emission array
    file_object.createVariable(pollutant_name, str(emissions_array.dtype)[0], ('time', 'lat', 'lon',))
    # populate
    file_object.variables[pollutant_name][:] = emissions_array[:]

    for attribute_ in file_attributes_tuple_list:
        setattr(file_object, attribute_[0], attribute_[1])

    for attribute_ in pollutant_attributes_tuple_list:
        setattr(file_object.variables[pollutant_name], attribute_[0], attribute_[1])

    file_object.close()
def save_emissions_to_existing_netcdf(out_filename, emissions_array, pollutant_name, attributes_tuple_list):
    file_object = nc.Dataset(out_filename, 'a')

    file_object.createVariable(pollutant_name, str(emissions_array.dtype)[0], ('time', 'lat', 'lon',))
    file_object.variables[pollutant_name][:] = emissions_array[:]

    setattr(file_object.variables[pollutant_name], 'pollutant name', pollutant_name)
    for attribute_ in attributes_tuple_list:
        setattr(file_object.variables[pollutant_name], attribute_[0], attribute_[1])


    file_object.close()
def convert_png_list_to_netcdf(file_list, out_filename, lat_array, lon_array):
    # out_filename = path_output + 'test_6.nc'
    # lat_array = np.arange(10240)
    # lon_array = np.arange(9472)


    # time array
    time_array = np.zeros(len(file_list), float)
    for time_stamp in range(len(file_list)):
        time_stamp_str = file_list[time_stamp].replace('\\','/').split('/')[-1]
        time_stamp_number = time_seconds_to_days(calendar.timegm(time.strptime(time_stamp_str, 'data_%Y%m%d_%H%M%S.png')))
        time_array[time_stamp] = time_stamp_number

    # lat and lon dim sizes
    temp_array = load_traffic_img_to_01234_arr(file_list[0])
    lat_dim_size = temp_array.shape[0]
    lon_dim_size = temp_array.shape[1]

    # temp_array = np.arange(50).reshape((5,10))
    # lat_dim_size = temp_array.shape[0]
    # lon_dim_size = temp_array.shape[1]


    # create file
    file_object = nc.Dataset(out_filename, 'w')
    file_object.createDimension('time', len(file_list))
    file_object.createDimension('lat', lat_dim_size)
    file_object.createDimension('lon', lon_dim_size)

    # create variables
    variable_object_time = file_object.createVariable('time', 'f', ('time',))
    variable_object_lat = file_object.createVariable('lat', 'f', ('lat',))
    variable_object_lon = file_object.createVariable('lon', 'f', ('lon',))
    variable_object_arr = file_object.createVariable('raw_traffic', 'i', ('time', 'lat', 'lon',))

    # populate dimention variables
    variable_object_time[:] = time_array[:]
    variable_object_lat[:] = lat_array[:]
    variable_object_lon[:] = lon_array[:]

    # populate the file
    for time_stamp in range(len(file_list)):
        variable_object_arr[time_stamp,:,:] = load_traffic_img_to_01234_arr(file_list[time_stamp])[:,:]
        print('loaded file ' + file_list[time_stamp])

    print('done')

    file_object.close()
def WRF_emission_file_modify(filename_, variable_name, cell_index_west_east, cell_index_south_north, new_value):
    netcdf_file_object = nc.Dataset(filename_, 'a')

    current_array = netcdf_file_object.variables[variable_name][0,0,:,:].copy()

    current_value = current_array[cell_index_south_north, cell_index_west_east]
    print(current_value)

    current_array[cell_index_south_north, cell_index_west_east] = new_value

    netcdf_file_object.variables[variable_name][0,0,:,:] = current_array[:,:]

    netcdf_file_object.close()
def find_wrf_3d_cell_from_latlon_to_south_north_west_east(lat_, lon_, wrf_output_filename,
                                                          wrf_lat_variablename='XLAT', wrf_lon_variablename='XLONG',
                                                          flatten_=False):
    if not wrf_available:
        print('Optional module wrf was not found, this functions is not available. Please install wrf')
        return None
    netcdf_file_object_wrf = nc.Dataset(wrf_output_filename, 'r')
    wrf_lat_array = netcdf_file_object_wrf.variables[wrf_lat_variablename][:,:].copy()
    wrf_lon_array = netcdf_file_object_wrf.variables[wrf_lon_variablename][:,:].copy()
    netcdf_file_object_wrf.close()

    wrf_abs_distance = ( (np.abs(wrf_lat_array - lat_)**2) + (np.abs(wrf_lon_array - lon_)**2) )**0.5

    if flatten_:
        return np.argmin(wrf_abs_distance)
    else:
        return np.unravel_index(np.argmin(wrf_abs_distance), wrf_abs_distance.shape)
def create_grevee_to_wrf_map_array(grevee_lat_series, grevee_lon_series, wrf_output_filename):
    # create grevee to wrf map array
    grevee_to_wrf_map_flat_array = np.zeros((grevee_lat_series.shape[0] * grevee_lon_series.shape[0]), dtype=int)
    grevee_flat_index = 0
    for r_grevee in range(grevee_lat_series.shape[0]):
        for c_grevee in range(grevee_lon_series.shape[0]):
            # get r_wrf and c_wrf
            lat_ = grevee_lat_series[r_grevee]
            lon_ = grevee_lon_series[c_grevee]

            wrf_index = find_wrf_3d_cell_from_latlon_to_south_north_west_east(lat_, lon_, wrf_output_filename, flatten_=True)
            grevee_to_wrf_map_flat_array[grevee_flat_index] = wrf_index

            grevee_flat_index += 1

    return grevee_to_wrf_map_flat_array




# specialized tools
def vectorize_array(array_):
    output_array = np.zeros((array_.shape[0] * array_.shape[1], 3), dtype=float)
    for r_ in range(array_.shape[0]):
        for c_ in range(array_.shape[1]):
            output_array[r_,0] = r_
            output_array[r_, 1] = c_
            output_array[r_, 2] = array_[r_,c_]
    return output_array
def exceedance_rolling(arr_time_seconds, arr_values, standard_, rolling_period, return_rolling_arrays=False):
    ## assumes data is in minutes and in same units as standard
    time_secs_1h, values_mean_disc_1h = mean_discrete(arr_time_seconds, arr_values, 3600, arr_time_seconds[0], min_data=45)
    values_rolling_mean = row_average_rolling(values_mean_disc_1h, rolling_period)
    counter_array = np.zeros(values_rolling_mean.shape[0])
    counter_array[values_rolling_mean > standard_] = 1
    total_number_of_exceedances = np.sum(counter_array)

    #create date str array
    T_ = np.zeros((time_secs_1h.shape[0],5),dtype='<U32')
    for r_ in range(time_secs_1h.shape[0]):
        if time_secs_1h[r_] == time_secs_1h[r_]:
            T_[r_] = time.strftime("%Y_%m_%d",time.gmtime(time_secs_1h[r_])).split(',')

    exceedance_date_list = []
    for r_, rolling_stamp in enumerate(values_rolling_mean):
        if rolling_stamp > standard_:
            exceedance_date_list.append(T_[r_])
    exc_dates_array = np.array(exceedance_date_list)
    exc_dates_array_unique = np.unique(exc_dates_array)

    if return_rolling_arrays:
        return total_number_of_exceedances, exc_dates_array_unique, time_secs_1h, values_rolling_mean
    else:
        return total_number_of_exceedances, exc_dates_array_unique
def statistical_tables(filename_, parameter_list):
    header_, values_, time_str = load_data_to_return_return(filename_)
    result_array = np.zeros((len(parameter_list),9),dtype = '<U32')
    result_array[:,:] = 'nan'
    for r_, par_index in enumerate(parameter_list):
        par_values_arr = values_[:,par_index]
        stats_list = [np.nanmean(par_values_arr),
                      np.nanpercentile(par_values_arr,50),
                      np.nanpercentile(par_values_arr, 25),
                      np.nanpercentile(par_values_arr, 75),
                      np.nanmax(par_values_arr),
                      np.nanmin(par_values_arr),
                      np.nanstd(par_values_arr)]
        # counting valid values
        par_count = np.array(par_values_arr)
        par_count[:] = 0
        par_count [par_values_arr==par_values_arr] = 1
        #
        stats_list.append(100 * np.sum(par_count)/par_count.shape[0])
        # place data in result array
        result_array[r_, 0] = header_[par_index]
        result_array[r_,1:] = stats_list
    header_list = ['parameter', 'mean', 'median', '25 percentile', '75 percentile', 'maximum', 'minimum', 'stdv', '% capture rate']
    output_filename = filename_.split('.')[0] + 'stats_table.csv'
    save_simple_array_to_disk(header_list, result_array, output_filename)
def get_point_x_y_from_start_angle_distance(point_x_y_tuple, angle_, distance):
    """
    finds the point that is distance away from the point_x_y_tuple location in angle_ direction
    :param point_x_y_tuple: tuple or list or array with two elements, elements can be floats
    :param angle_: in degrees from the positive x direction counterclockwise
    :param distance: scalar in the same units as x and y
    :return: tuple with x and y location of result point
    """
    angle_rad = np.pi * angle_ / 180
    x_delta = distance * np.cos(angle_rad)
    y_delta = distance * np.sin(angle_rad)
    return point_x_y_tuple[0] + x_delta, point_x_y_tuple[1] + y_delta
def create_line_x_y_series_from_start_point_and_angle(start_point_x_y, angle_deg, length_, line_resolution):
    # define stop point
    stop_point_x_y = get_point_x_y_from_start_angle_distance(start_point_x_y, angle_deg, length_)

    # create line
    line_x = np.linspace(start_point_x_y[0],stop_point_x_y[0],line_resolution)
    line_y = np.linspace(start_point_x_y[1],stop_point_x_y[1],line_resolution)

    return line_x, line_y
def create_rectangular_mask_from_array_start_point_angle(array_, start_point_x_y, angle_deg, length_, width_,
                                                         array_x_min, array_x_max, array_y_min, array_y_max,
                                                         ):
    line_resolution = np.max(array_.shape)
    x_bin_number = array_.shape[1]
    y_bin_number = array_.shape[0]

    line_to_first_corner_x_y = create_line_x_y_series_from_start_point_and_angle(start_point_x_y,
                                                                                 angle_deg + 90, width_ / 2,
                                                                                 int(line_resolution))

    line_from_first_corner_to_second_corner_x_y = create_line_x_y_series_from_start_point_and_angle(
        (line_to_first_corner_x_y[0][-1], line_to_first_corner_x_y[1][-1]),
        angle_deg - 90, width_,
        int(line_resolution * width_ / length_))

    master_line_x_list = []
    master_line_y_list = []
    for i_ in range(len(line_from_first_corner_to_second_corner_x_y[0])):
        start_x = line_from_first_corner_to_second_corner_x_y[0][i_]
        start_y = line_from_first_corner_to_second_corner_x_y[1][i_]
        line_temp_x_y = create_line_x_y_series_from_start_point_and_angle((start_x, start_y),
                                                                          angle_deg, length_,
                                                                          int(line_resolution))
        for ii_ in range(len(line_temp_x_y[0])):
            master_line_x_list.append(line_temp_x_y[0][ii_])
            master_line_y_list.append(line_temp_x_y[1][ii_])


    array_bool = trajectory_lat_lon_to_frequency_2D(np.array(master_line_y_list), np.array(master_line_x_list),
                                                             array_y_min, array_y_max, y_bin_number,
                                                             array_x_min, array_x_max, x_bin_number)


    return array_bool
def create_thick_cross_section_mean_std_series(array_values, array_x, array_y,
                                               start_point_x_y, angle_deg, length_, width_):
    # <editor-fold desc="reshape axis arrays to 2D if needed">
    if len(array_x.shape) == 1:
        array_x_reshaped = np.zeros(array_values.shape, dtype=float)
        for r_ in range(array_values.shape[0]):
            array_x_reshaped[r_, :] = array_x
    else:
        array_x_reshaped = array_x
    array_x = array_x_reshaped

    if len(array_y.shape) == 1:
        array_y_reshaped = np.zeros(array_values.shape, dtype=float)
        for c_ in range(array_values.shape[1]):
            array_y_reshaped[:, c_] = array_y
    else:
        array_y_reshaped = array_y
    array_y = array_y_reshaped
    # </editor-fold>

    ## define suitable resolution of transverse line cuts to minimize overlap but insure no skips

    # define stop point
    stop_point_x_y = get_point_x_y_from_start_angle_distance(start_point_x_y, angle_deg, length_)

    # get grid spacing
    d_x = np.nanmedian(np.diff(array_x, axis=1))
    d_y = np.nanmedian(np.diff(array_y, axis=0))

    # get number of grids between start point and end point
    x_cells = np.ceil(np.abs((start_point_x_y[0] - stop_point_x_y[0]) / d_x))
    y_cells = np.ceil(np.abs((start_point_x_y[1] - stop_point_x_y[1]) / d_y))
    diagonal_cells = int(np.ceil((x_cells ** 2 + y_cells ** 2) ** 0.5))

    # create line between start and end point
    line_x_arr, line_y_arr = create_line_x_y_series_from_start_point_and_angle(start_point_x_y,
                                                                               angle_deg, length_,
                                                                               diagonal_cells)
    # p_plot(line_x_arr, line_y_arr, S_=20, add_line=True, fig_ax=o_[:2])

    # loop through each line point and create transverse lines, get bool array of cells touching lines, and store
    cells_along_trans_lines_list = []
    bool_list = []
    for line_x, line_y in zip(line_x_arr, line_y_arr):
        point_1_x_y = get_point_x_y_from_start_angle_distance((line_x, line_y), angle_deg + 90, width_ / 2)
        line_2_x_y = create_line_x_y_series_from_start_point_and_angle(point_1_x_y, angle_deg - 90, width_,
                                                                       diagonal_cells)

        array_bool = trajectory_lat_lon_to_frequency_2D(line_2_x_y[1], line_2_x_y[0],
                                                        np.nanmin(array_y) - d_y / 2,
                                                        np.nanmax(array_y) + d_y / 2,
                                                        array_values.shape[0],
                                                        np.nanmin(array_x) - d_x / 2,
                                                        np.nanmax(array_x) + d_x / 2,
                                                        array_values.shape[1])
        bool_list.append(array_bool)
        cells_along_trans_lines_list.append(array_values[array_bool])

    mean_list = []
    std_list = []
    for i_ in cells_along_trans_lines_list:
        mean_list.append(np.nanmean(i_))
        std_list.append(np.nanstd(i_))

    return line_x_arr, line_y_arr, np.array(mean_list), np.array(std_list)
def divide_array_into_chunks_with_overlap_multiprocessing(array_, number_of_chunks, overlap_size):
    # chunkify array with overlap
    rows_ = array_.shape[0]
    chunk_size = int(rows_ / number_of_chunks)

    array_list = []
    for chunk_number in range(number_of_chunks):
        if chunk_number == 0:
            array_list.append(array_[:chunk_size + overlap_size,:])
        elif chunk_number == number_of_chunks-1:
            array_list.append(array_[(chunk_size * chunk_number)-overlap_size:, :])
        else:
            array_list.append(array_[(chunk_size * chunk_number)-overlap_size:(chunk_size * (chunk_number+1))
                                                                              + overlap_size, :])
    return array_list
def stitch_array_from_list_of_chunks_with_overlap(chunk_list, overlap_size):
    number_of_chunks = len(chunk_list)

    cropped_arrays_list = []
    for chunk_number in range(number_of_chunks):
        array_ = chunk_list[chunk_number]
        if chunk_number == 0:
            cropped_arrays_list.append(array_[:-overlap_size,:])
        elif chunk_number == number_of_chunks-1:
            cropped_arrays_list.append(array_[overlap_size:, :])
        else:
            cropped_arrays_list.append(array_[overlap_size:-overlap_size, :])


    return np.row_stack(cropped_arrays_list)
def show_stats(array_, max_number_of_uniques_to_show=20):
    type_ = array_.dtype
    shape_ = array_.shape
    mean_ = np.nanmean(array_)
    median_ = np.nanmedian(array_)
    std_ = np.nanstd(array_)
    max_ = np.nanmax(array_)
    min_ = np.nanmin(array_)
    perc_05_ = np.nanpercentile(array_, 5)
    perc_25_ = np.nanpercentile(array_, 25)
    perc_75_ = np.nanpercentile(array_, 75)
    perc_95_ = np.nanpercentile(array_, 95)
    contains_nans_ = False
    if np.sum(np.isnan(array_)) > 0:
        contains_nans_ = True

    unique_values = list(sorted(set(array_[~np.isnan(array_)])))

    print('-' * 20)
    print('type:', type_)
    print('shape:', shape_)
    print('mean:', mean_)
    print('median:', median_)
    print('std:', std_)
    print('max:', max_)
    print('min:', min_)
    print('perc_05:', perc_05_)
    print('perc_25:', perc_25_)
    print('perc_75:', perc_75_)
    print('perc_95:', perc_95_)
    print('contains_nans:', contains_nans_)

    print('Number of unique values:', len(unique_values))
    if len(unique_values) <= max_number_of_uniques_to_show:
        print('-' * 10)
        for unique_val in unique_values:
            print('\t', unique_val, '\t', np.sum(array_ == unique_val))
    print('-' * 20)


# ozonesonde and radiosonde related
def load_sonde_data(filename_, mode_='PBL'):  ##Loads data and finds inversions, creates I_
    # global V_, M_, H_, ASL_, time_header, I_, I_line
    # global ASL_avr, L_T, L_RH, time_string, time_days, time_seconds, year_, flight_name


    ## user defined variables
    delimiter_ = ','
    error_flag = -999999
    first_data_header = 'Day_[GMT]'
    day_column_number = 0
    month_column_number = 1
    year_column_number = 2
    hour_column_number = 3
    minute_column_number = 4
    second_column_number = 5
    # time_header = 'Local Time'  # defining time header

    # main data array
    sample_data = filename_

    # look for data start (header size)
    with open(sample_data) as file_read:
        header_size = -1
        r_ = 0
        for line_string in file_read:
            if (len(line_string) >= len(first_data_header) and
                        line_string[:len(first_data_header)] == first_data_header):
                header_size = r_
                break
            r_ += 1
        if header_size == -1:
            print('no data found!')
            sys.exit()

    data_array = np.array(genfromtxt(sample_data,
                                     delimiter=delimiter_,
                                     skip_header=header_size,
                                     dtype='<U32'))
    # defining header  and data arrays
    M_ = data_array[1:, 6:].astype(float)
    H_ = data_array[0, 6:]
    ASL_ = M_[:, -1]
    # year_ = data_array[1, year_column_number]
    ASL_[ASL_ == error_flag] = np.nan

    # defining time arrays
    time_str = data_array[1:, 0].astype('<U32')
    for r_ in range(time_str.shape[0]):
        time_str[r_] = (str(data_array[r_ + 1, day_column_number]) + '-' +
                           str(data_array[r_ + 1, month_column_number]) + '-' +
                           str(data_array[r_ + 1, year_column_number]) + '_' +
                           str(data_array[r_ + 1, hour_column_number]) + ':' +
                           str(data_array[r_ + 1, minute_column_number]) + ':' +
                           str(data_array[r_ + 1, second_column_number]))

    time_days = np.array([mdates.date2num(datetime.utcfromtimestamp(
                                calendar.timegm(time.strptime(time_string_record, '%d-%m-%Y_%H:%M:%S'))))
                                for time_string_record in time_str])
    time_seconds = time_days_to_seconds(time_days)
    V_ = M_.astype(float)
    V_[V_ == error_flag] = np.nan

    T_avr = np.ones(V_[:, 1].shape)
    RH_avr = np.ones(V_[:, 1].shape)
    ASL_avr = np.ones(V_[:, 1].shape)
    L_T = np.zeros(V_[:, 1].shape)
    L_RH = np.zeros(V_[:, 1].shape)
    I_ = np.zeros(V_[:, 1].shape)
    I_[:] = np.nan
    # rolling average of T RH and ASL
    mean_size = 7  # 5
    for r_ in range(mean_size, V_[:, 1].shape[0] - mean_size):
        T_avr[r_] = np.nanmean(V_[r_ - mean_size: r_ + mean_size, 1])
        RH_avr[r_] = np.nanmean(V_[r_ - mean_size: r_ + mean_size, 2])
        ASL_avr[r_] = np.nanmean(ASL_[r_ - mean_size: r_ + mean_size])
    for r_ in range(mean_size, V_[:, 1].shape[0] - mean_size):
        if (ASL_avr[r_ + 1] - ASL_avr[r_]) > 0:
            L_T[r_] = ((T_avr[r_ + 1] - T_avr[r_]) /
                       (ASL_avr[r_ + 1] - ASL_avr[r_]))
            L_RH[r_] = ((RH_avr[r_ + 1] - RH_avr[r_]) /
                        (ASL_avr[r_ + 1] - ASL_avr[r_]))

    # define location of inversion
    # PBL or TSI
    if mode_ == 'PBL':
        for r_ in range(mean_size, V_[:, 1].shape[0] - mean_size):
            if L_T[r_] > 7 and L_RH[r_] < -20:  # PBL = 7,20 / TSI = 20,200
                I_[r_] = 1

        # get one of I_ only per layer
        temperature_gap = .4  # kilometres
        I_line = np.zeros((1, 3))  # height, time, intensity
        if np.nansum(I_) > 1:
            r_ = -1
            while r_ < I_.shape[0] - mean_size:
                r_ += 1
                if I_[r_] == 1 and ASL_avr[r_] < 4:
                    layer_temp = T_avr[r_]
                    layer_h = ASL_avr[r_]
                    layer_time = time_seconds[r_]
                    for rr_ in range(r_, I_.shape[0] - mean_size):
                        if T_avr[rr_] < layer_temp - temperature_gap:
                            delta_h = ASL_avr[rr_] - layer_h
                            altitude_ = layer_h
                            stanking_temp = np.array([altitude_, layer_time, delta_h])
                            I_line = np.row_stack((I_line, stanking_temp))
                            r_ = rr_
                            break

        if np.max(I_line[:, 0]) != 0:
            I_line = I_line[1:, :]
        else:
            I_line[:, :] = np.nan
    else:
        for r_ in range(mean_size, V_[:, 1].shape[0] - mean_size):
            if L_T[r_] > 20 and L_RH[r_] < -200:  # PBL = 7,20 / TSI = 20,200
                I_[r_] = 1

        # get one of I_ only per layer
        temperature_gap = .4  # kilometres
        I_line = np.zeros((1, 3))  # height, time, intensity
        if np.nansum(I_) > 1:
            r_ = -1
            while r_ < I_.shape[0] - mean_size:
                r_ += 1
                if I_[r_] == 1 and 4 < ASL_avr[r_] < 8:
                    layer_temp = T_avr[r_]
                    layer_h = ASL_avr[r_]
                    layer_time = time_seconds[r_]
                    for rr_ in range(r_, I_.shape[0] - mean_size):
                        if T_avr[rr_] < layer_temp - temperature_gap:
                            delta_h = ASL_avr[rr_] - layer_h
                            altitude_ = layer_h
                            stanking_temp = np.array([altitude_, layer_time, delta_h])
                            I_line = np.row_stack((I_line, stanking_temp))
                            r_ = rr_
                            break

        if np.max(I_line[:, 0]) != 0:
            I_line = I_line[1:, :]
        else:
            I_line[:, :] = np.nan

    return H_, V_, time_days, time_seconds, I_, I_line, L_T, L_RH
def plot_X1_X2_Y(X1_blue, X2_green, Y):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twiny()

    ax1.plot(X1_blue, Y, s=5, color='b', edgecolor='none')
    ax1.axvline(0, c='k')
    ax2.scatter(X2_green, Y, s=5, color='g', edgecolor='none')
    ax2.axvline(0, c='k')

    plt.show()
def plot_T_RH_I_(V_, I_line):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twiny()

    ASL_ = V_[:, -1]

    ax1.set_ylabel('ASL')
    ax1.set_xlabel('Temp')
    ax2.set_xlabel('RH')

    ax1.scatter(V_[:, 1], ASL_, s=5, color='b', edgecolor='none')
    ax1.axvline(0, c='k')
    RH_temp = V_[:, 2]
    RH_temp = RH_temp
    ax2.scatter(RH_temp, ASL_, s=5, color='g', edgecolor='none')
    ax2.axvline(0, c='k')
    for x in range(I_line.shape[0]):
        plt.axhline(I_line[x, 0], c='r')
    plt.show()
def plot_ThetaVirtual_I_(V_, I_line):
    fig, ax1 = plt.subplots()

    ASL_ = V_[:, -1]

    ax1.set_ylabel('ASL')
    ax1.set_xlabel('Virtual Potential Temperature [K]')

    ax1.scatter(V_[:, 5], ASL_, s=5, color='b', edgecolor='none')


    for x in range(I_line.shape[0]):
        plt.axhline(I_line[x, 0], c='r')

    plt.show()
def last_lat_lon_alt_ozonesonde(filename_):
    data_array = genfromtxt(filename_, delimiter=',', dtype='<U32', skip_header=23)
    return data_array[-1,31], data_array[-1,32], data_array[-1,33], data_array[-1,0]
def download_sonde_data_Wyoming(station_number, start_time_YYYYmmDDHH, end_time_YYYYmmDDHH):
    url_prefix = 'http://weather.uwyo.edu/cgi-bin/sounding?region=pac&TYPE=TEXT%3ALIST&'

    station_str = str(station_number)
    datetime_start_sec = time_str_to_seconds(start_time_YYYYmmDDHH, '%Y%m%d%H')
    datetime_end_sec = time_str_to_seconds(end_time_YYYYmmDDHH, '%Y%m%d%H')

    # create date strings list
    time_steps_in_sec = 60 * 60 * 24
    number_of_days = (datetime_end_sec - datetime_start_sec) / time_steps_in_sec
    url_datetime_str_list = []
    for time_stamp_index in range(int(number_of_days+1)):
        url_datetime_str_list.append(time_seconds_to_str(datetime_start_sec + (time_stamp_index * time_steps_in_sec),
                                                     'YEAR=%Y&MONTH=%m&FROM=%d00&TO=%d23&STNM='))

    # create the output dictionary
    page_dict = {}

    for day_index in range(len(url_datetime_str_list)):
        p_progress(day_index, len(url_datetime_str_list))
        url_ = url_prefix + url_datetime_str_list[day_index] + station_str

        page_str = requests.get(url_).text

        page_launches = page_str.split('<H2>' + station_str)[1:]
        number_of_launches = len(page_launches)

        if number_of_launches > 0:
            station_name_long = page_str.split('<H2>')[1].split('</H2>')[0][:-19]
            profile_header = page_launches[0].split('PRE>')[1].split('\n')[2].split()
            profile_header_units = page_launches[0].split('PRE>')[1].split('\n')[3].split()

            for launch_index in range(len(page_launches)):

                launch_time_sec = time_str_to_seconds(page_launches[launch_index].split('</H2>')[0][-15:],
                                                      '%HZ %d %b %Y')
                launch_time_str = time_seconds_to_str(launch_time_sec, '%Y%m%d%H')

                # add dict to launch key
                page_dict[launch_time_str] = {}
                # add static information
                page_dict[launch_time_str]['profile_header'] = profile_header
                page_dict[launch_time_str]['profile_header_units'] = profile_header_units
                page_dict[launch_time_str]['station_name_long'] = station_name_long


                # launches_times_list.append(launch_time_sec)
                profile_str_list = page_launches[launch_index].split('PRE>')[1].split('\n')[5:-1]
                profile_array_all = np.zeros((len(profile_str_list),len(profile_header)))
                for r_ in range(profile_array_all.shape[0]):
                    line_list = [profile_str_list[r_][i:i+7] for i in range(0, len(profile_str_list[r_]), 7)]
                    for c_ in range(len(profile_header)):
                        value_str = line_list[c_]
                        try:
                            value_float = float(value_str)
                        except:
                            value_float = np.nan
                        profile_array_all[r_,c_] = value_float

                for c_ in range(len(profile_header)):
                    page_dict[launch_time_str][profile_header[c_]] = profile_array_all[:,c_]

                extra_info_list = page_launches[launch_index].split('PRE>')[3].split('\n')[1:-1]

                for e_str in extra_info_list:
                    key_str = e_str.split(':')[0].strip()
                    values_str = e_str.split(':')[1].strip()

                    try:
                        page_dict[launch_time_str][key_str] = float(values_str)
                    except:
                        page_dict[launch_time_str][key_str] = values_str


    return page_dict
def load_khancoban_sondes(filename_):
    line_number = -1
    dict_ = {}
    dict_['filename'] = filename_.replace('\\','/').split('/')[-1]
    dict_['date'] = '20' + filename_.replace('\\','/').split('/')[-1][2:]
    profile_header = []
    profile_units = []
    profile_data = []
    with open(filename_) as file_object:
        for line in file_object:
            line_number += 1
            line_items = line.split()

            if  17 <= line_number <= 35:
                profile_header.append(line_items[0])
                profile_units.append(line_items[1])

            if line_number >= 39 and len(line_items)>1:
                profile_data.append(line_items)

    profile_array = np.zeros((len(profile_data), len(profile_data[0])), dtype=float)

    for r_ in range(len(profile_data)):
        profile_array[r_, :] = profile_data[r_]

    for c_ in range(len(profile_header)):
        dict_[profile_header[c_]] = {}
        dict_[profile_header[c_]]['data'] = profile_array[:, c_]
        dict_[profile_header[c_]]['units'] = profile_units[c_]


    return dict_
def convert_khan_sonde_data_to_skewt_dict(khan_dict, sonde_name):

    # create time array in seconds since epoc
    date_seconds = time_str_to_seconds(khan_dict[sonde_name]['date'], '%Y%m%d.0%H')
    time_sonde_sec = date_seconds + khan_dict[sonde_name]['time']['data']



    mydata_0=dict(zip(('hght','pres','temp','dwpt', 'sknt', 'drct', 'relh', 'time', 'lati', 'long'),
                      (khan_dict[sonde_name]['Height']['data'],
                       khan_dict[sonde_name]['P']['data'],
                       kelvin_to_celsius(khan_dict[sonde_name]['T']['data']),
                       kelvin_to_celsius(khan_dict[sonde_name]['TD']['data']),
                       ws_ms_to_knots(khan_dict[sonde_name]['FF']['data']),
                       khan_dict[sonde_name]['DD']['data'],
                       khan_dict[sonde_name]['RH']['data'],
                       time_sonde_sec,
                       khan_dict[sonde_name]['Lat']['data'],
                       khan_dict[sonde_name]['Lon']['data']
                       )))
    return mydata_0
def p_plot_SkewT(khan_dict, sonde_name, figure_filename=None, ws_in_knots=False):
    sonde_dict = convert_khan_sonde_data_to_skewt_dict(khan_dict, sonde_name)
    S=SkewT.Sounding(soundingdata=sonde_dict)
    S.plot_skewt(color='r',title=sonde_name, ws_in_knots=ws_in_knots)
    fig = plt.figure(1)
    ax = fig.axes[0]

    if figure_filename is not None:
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
        return figure_filename

    return fig,ax
def p_plot_SkewT_from_dict_wyoming(sonde_dict, figure_filename=None, tittle_str=None, color_='r',
                                   parcel_type='most_unstable',
                                   ws_in_knots=False, tmin=-40, tmax=30, pmin_=100, pmax_=1050,plot_lift_text=True,
                                   skip_divisor=32,
                                   fig=None, ax_space_box_LBRT=(0,0,1,1), ax_skewt_wbax_tuple=None):

    H_array_m   = sonde_dict['HGHT']
    P_array_hPa = sonde_dict['PRES']
    T_array_C   = sonde_dict['TEMP']
    Td_array_C  = sonde_dict['DWPT']
    WD_array_D  = sonde_dict['DRCT']
    WS_array_kn = sonde_dict['SKNT']

    # order ascending
    ascending_2d_array = array_2D_sort_ascending_by_column(
        np.column_stack((H_array_m,
                         P_array_hPa,
                         T_array_C,
                         Td_array_C,
                         WD_array_D,
                         WS_array_kn)), 0)
    H_array_m   = ascending_2d_array[:, 0]
    P_array_hPa = ascending_2d_array[:, 1]
    T_array_C   = ascending_2d_array[:, 2]
    Td_array_C  = ascending_2d_array[:, 3]
    WD_array_D  = ascending_2d_array[:, 4]
    WS_array_kn = ascending_2d_array[:, 5]


    # convert wind to polar

    data_dict  = dict(zip(('hght', 'pres', 'temp', 'dwpt', 'sknt', 'drct'),
                          (H_array_m,
                           P_array_hPa,
                           T_array_C,
                           Td_array_C,
                           WS_array_kn,
                           WD_array_D
                           )))

    Sounding_=SkewT.Sounding(soundingdata=data_dict)
    Sounding_.plot_skewt(color=color_,title=tittle_str, parcel_type=parcel_type, ws_in_knots=ws_in_knots,
                         tmin=tmin, tmax=tmax, plot_lift_text=plot_lift_text, skip_divisor=skip_divisor,
                         fig=fig, ax_space_box_LBRT=ax_space_box_LBRT, ax_skewt_wbax_tuple=ax_skewt_wbax_tuple,
                         pmax=pmax_, pmin=pmin_)
    fig = plt.figure(1)
    ax = fig.axes[0]

    if figure_filename is not None:
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
        return figure_filename

    return fig, ax, Sounding_

def p_plot_SkewT_sonde(H_array_m, P_array_hPa, T_array_C, Td_array_C, U_array_ms, V_array_ms,
                       figure_filename=None, tittle_str=None, color_='r', parcel_type='most_unstable',
                       ws_in_knots=False, tmin=-40, tmax=30, pmin_=100, pmax_=1050,plot_lift_text=True, skip_divisor=32,
                       fig=None, ax_space_box_LBRT=(0,0,1,1), ax_skewt_wbax_tuple=None):

    # order ascending
    ascending_2d_array = array_2D_sort_ascending_by_column(
        np.column_stack((H_array_m, P_array_hPa, T_array_C, Td_array_C, U_array_ms, V_array_ms)), 0)
    H_array_m   = ascending_2d_array[:, 0]
    P_array_hPa = ascending_2d_array[:, 1]
    T_array_C   = ascending_2d_array[:, 2]
    Td_array_C  = ascending_2d_array[:, 3]
    U_array_ms  = ascending_2d_array[:, 4]
    V_array_ms  = ascending_2d_array[:, 5]


    # convert wind to polar
    WD_, WS_ = cart_to_polar(V_array_ms, U_array_ms)
    # fix wind direction to meteorological (dumb) tradition (shifted by 180)
    drct_array = WD_ + 180
    drct_array[drct_array >= 360] = drct_array[drct_array >= 360]-360
    # convert winds to meteorological (dumb) tradition (knots)
    sknt_array = ws_ms_to_knots(WS_)

    data_dict  = dict(zip(('hght', 'pres', 'temp', 'dwpt', 'sknt', 'drct'),
                          (H_array_m,
                           P_array_hPa,
                           T_array_C,
                           Td_array_C,
                           sknt_array,
                           drct_array
                           )))

    Sounding_=SkewT.Sounding(soundingdata=data_dict)
    Sounding_.plot_skewt(color=color_,title=tittle_str, parcel_type=parcel_type, ws_in_knots=ws_in_knots,
                         tmin=tmin, tmax=tmax, plot_lift_text=plot_lift_text, skip_divisor=skip_divisor,
                         fig=fig, ax_space_box_LBRT=ax_space_box_LBRT, ax_skewt_wbax_tuple=ax_skewt_wbax_tuple,
                         pmax=pmax_, pmin=pmin_)
    fig = plt.figure(1)
    ax = fig.axes[0]

    if figure_filename is not None:
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
        return figure_filename

    return fig, ax, Sounding_
def create_sonde_dict_from_arrays(H_array_m, P_array_hPa, T_array_C, Td_array_C, U_array_ms, V_array_ms):
    # order ascending
    ascending_2d_array = array_2D_sort_ascending_by_column(
        np.column_stack((H_array_m, P_array_hPa, T_array_C, Td_array_C, U_array_ms, V_array_ms)), 0)
    H_array_m   = ascending_2d_array[:, 0]
    P_array_hPa = ascending_2d_array[:, 1]
    T_array_C   = ascending_2d_array[:, 2]
    Td_array_C  = ascending_2d_array[:, 3]
    U_array_ms  = ascending_2d_array[:, 4]
    V_array_ms  = ascending_2d_array[:, 5]


    # convert wind to polar
    WD_, WS_ = cart_to_polar(V_array_ms, U_array_ms)
    # fix wind direction to meteorological (dumb) tradition (shifted by 180)
    drct_array = WD_ + 180
    drct_array[drct_array >= 360] = drct_array[drct_array >= 360]-360
    # convert winds to meteorological (dumb) tradition (knots)
    sknt_array = ws_ms_to_knots(WS_)

    data_dict  = dict(zip(('hght', 'pres', 'temp', 'dwpt', 'sknt', 'drct'),
                          (H_array_m,
                           P_array_hPa,
                           T_array_C,
                           Td_array_C,
                           sknt_array,
                           drct_array
                           )))
    return data_dict
def create_sonde_dict_from_some_arrays(P_array_hPa, T_array_C, Td_array_C,
                                       U_array_ms=None, V_array_ms=None, H_array_m=None):

    if U_array_ms is None: U_array_ms = np.zeros(P_array_hPa.shape[0]) * np.nan
    if V_array_ms is None: V_array_ms = np.zeros(P_array_hPa.shape[0]) * np.nan
    if H_array_m is None: H_array_m = np.zeros(P_array_hPa.shape[0]) * np.nan

    # order ascending
    ascending_2d_array = array_2D_sort_ascending_by_column(
        np.column_stack((P_array_hPa, H_array_m, T_array_C, Td_array_C, U_array_ms, V_array_ms)), 0)[::-1,:]
    P_array_hPa = ascending_2d_array[:, 0]
    H_array_m   = ascending_2d_array[:, 1]
    T_array_C   = ascending_2d_array[:, 2]
    Td_array_C  = ascending_2d_array[:, 3]
    U_array_ms  = ascending_2d_array[:, 4]
    V_array_ms  = ascending_2d_array[:, 5]


    # convert wind to polar
    WD_, WS_ = cart_to_polar(V_array_ms, U_array_ms)
    # fix wind direction to meteorological (dumb) tradition (shifted by 180)
    drct_array = WD_ + 180
    drct_array[drct_array >= 360] = drct_array[drct_array >= 360]-360
    # convert winds to meteorological (dumb) tradition (knots)
    sknt_array = ws_ms_to_knots(WS_)

    data_dict  = dict(zip(('hght', 'pres', 'temp', 'dwpt', 'sknt', 'drct'),
                          (H_array_m,
                           P_array_hPa,
                           T_array_C,
                           Td_array_C,
                           sknt_array,
                           drct_array
                           )))
    return data_dict




# PBL and LIA related
def load_dot_file(filename_):
    # file first column is days and second is meters
    return np.array(genfromtxt(filename_, delimiter=',', skip_header=1, dtype=float))
def load_LIA_monthly_PBL(filename_):
    # file format: Y, M, D, H, m, PBL_ASL [m]
    header_, values_, time_str = load_data_to_return_return(filename_)
    return values_
def load_raw_CL51_file(filename_, height_low = 170, height_high = 3500):
    file_name_first_number = filename_[-11]
    year_ = '201' + file_name_first_number

    M_raw = np.array(genfromtxt(filename_, delimiter=',', skip_header=5, skip_footer=1))
    M_t = M_raw[:, 8:]
    M_t = M_t[:, int(height_low / 10): int(height_high / 10) + 1]
    date_time_str = np.array(genfromtxt(filename_, dtype=str, delimiter=',', skip_header=5, skip_footer=1, usecols=(0, 1)))

    time_str = []
    for r_ in range(date_time_str.shape[0]):
        time_str.append(year_ + date_time_str[r_,0] + date_time_str[r_,1])

    time_seconds = time_str_to_seconds(time_str, '%Y%d-%b%H:%M:%S')

    time_t = time_seconds_to_days(time_seconds)

    return time_t, M_t
def compare_WRF_PBL_to_CL51(wrf_filename, cl51_filename_list, dot_filename):

    dot_4 = load_dot_file(dot_filename)

    WRF_PBL_H, WRF_PBL_V, WRF_PBL_str = load_data_to_return_return(wrf_filename)

    fig, ax = plt.subplots(figsize=(10,6))

    CL_list_T = []
    CL_list_V = []
    # img_list = []
    for filename_ in cl51_filename_list:
        temp_T, temp_V = load_raw_CL51_file(filename_, height_low = 0, height_high = 2000)

        temp_V = np.rot90(temp_V, 1)

        temp_V[temp_V < 0] = 0
        temp_V[temp_V > 400] = 400

        # temp_V_2 = temp_V[:-1,:] * 0
        # for r_ in range(temp_V.shape[0]-1):
        #     temp_V_2[r_,:] = temp_V[r_,:] - temp_V[r_+1,:]

        # temp_V = temp_V_2

        CL_list_T.append(temp_T)
        CL_list_V.append(temp_V)

        x_ = np.zeros((temp_V.shape[0], temp_V.shape[1]), dtype=float)
        y_ = np.zeros((temp_V.shape[0], temp_V.shape[1]), dtype=float)
        for r_ in range(temp_V.shape[0]):
            x_[r_,:] = temp_T
        for c_ in range(temp_V.shape[1]):
            y_[:,c_] = np.arange(0,2010,10)

        y_ = y_[::-1,:]

        # levels = matplotlib.ticker.MaxNLocator(nbins=20).tick_values(temp_V[:-1,:-1].min(), temp_V[:-1,:-1].max())
        # norm = matplotlib.colors.BoundaryNorm(levels, ncolors=cm.jet, clip=True)
        # cf = ax.contourf(x_[:-1, :-1],
        #                   y_[:-1, :-1], temp_V[:-1,:-1], levels=levels,
        #                   cmap=cm.jet)

        ax.pcolormesh(x_, y_, temp_V, cmap=default_cm, vmin=0, vmax=300)

        # img_ = ax.imshow(temp_V, interpolation='none', cmap=cm.Greys, aspect= 0.1,
        #     extent=[temp_T[0], temp_T[-1], 0, 2000])

        # img_list.append(surf_)

    # color_list = ['r', 'b', 'g']
    line_style_list = [':', '-', '--']
    for i, WRF_skeem_name in enumerate(WRF_PBL_H[2:]):
        ax.plot(WRF_PBL_V[:,0], WRF_PBL_V[:,i + 2], color='black', label=WRF_PBL_H[i + 2], lw=5,
                linestyle=line_style_list[i])

    # color_bar = fig.colorbar(img_)
    ax.scatter(dot_4[:, 0], dot_4[:, 1], c='w', s=150, lw=5, label='Radiosonde')

    ax.legend()



    plot_format_mayor = mdates.DateFormatter('%H:%M %d %b %y', tz=tz_UTC)
    ax.xaxis.set_major_formatter(plot_format_mayor)

    plt.show()
    return fig, ax
def save_chart_WRF_PBL_CL51(wrf_filename, cl51_filename_list, dot_filename):

    dot_4 = load_dot_file(dot_filename)

    WRF_PBL_H, WRF_PBL_V, WRF_PBL_str = load_data_to_return_return(wrf_filename)


    CL_list_T = []
    CL_list_V = []
    # img_list = []
    for filename_ in cl51_filename_list:
        fig, ax = plt.subplots(figsize=(10, 5))

        temp_T, temp_V = load_raw_CL51_file(filename_, height_low = 0, height_high = 2000)

        temp_V = np.rot90(temp_V, 1)

        temp_V[temp_V < 0] = 0
        temp_V[temp_V > 300] = 300

        # temp_V_2 = temp_V[:-1,:] * 0
        # for r_ in range(temp_V.shape[0]-1):
        #     temp_V_2[r_,:] = temp_V[r_,:] - temp_V[r_+1,:]

        # temp_V = temp_V_2

        CL_list_T.append(temp_T)
        CL_list_V.append(temp_V)

        x_ = np.zeros((temp_V.shape[0], temp_V.shape[1]), dtype=float)
        y_ = np.zeros((temp_V.shape[0], temp_V.shape[1]), dtype=float)
        for r_ in range(temp_V.shape[0]):
            x_[r_,:] = temp_T
        for c_ in range(temp_V.shape[1]):
            y_[:,c_] = np.arange(0,2010,10)

        y_ = y_[::-1,:]

        # levels = matplotlib.ticker.MaxNLocator(nbins=20).tick_values(temp_V[:-1,:-1].min(), temp_V[:-1,:-1].max())
        # norm = matplotlib.colors.BoundaryNorm(levels, ncolors=cm.jet, clip=True)
        # cf = ax.contourf(x_[:-1, :-1],
        #                   y_[:-1, :-1], temp_V[:-1,:-1], levels=levels,
        #                   cmap=cm.jet)

        surf_ = ax.pcolormesh(x_, y_, temp_V, cmap=default_cm, vmin=0, vmax=300)

        # img_ = ax.imshow(temp_V, interpolation='none', cmap=cm.Greys, aspect= 0.1,
        #     extent=[temp_T[0], temp_T[-1], 0, 2000])

        # img_list.append(surf_)

        # color_list = ['r', 'b', 'g']
        line_style_list = ['-', '-.', '--']
        for i, WRF_skeem_name in enumerate(WRF_PBL_H[2:]):
            ax.plot(WRF_PBL_V[:,0], WRF_PBL_V[:,i + 2], color='black', label=WRF_PBL_H[i + 2],
                    lw=5, linestyle=line_style_list[i])

        # color_bar = fig.colorbar(img_)
        ax.scatter(dot_4[:, 0], dot_4[:, 1], c='w', s=150, lw=5, label='Radiosonde')

        ax.legend()



        plot_format_mayor = mdates.DateFormatter('%H %d-%b-%y', tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)

        ax.set_xlim(temp_T[0],temp_T[-1])
        ax.set_ylim(0,2000)

        color_bar = fig.colorbar(surf_, fraction=0.046, pad=0.04)

        # axes labels
        ax.set_xlabel('Local Time')
        ax.set_ylabel('Meters Above Sea Level')
        color_bar.ax.set_ylabel('Backscatter Intensity [1/100000*srad*km]')

        plt.show()
        name_ = filename_[-12:-4]
        fig.savefig(path_output + 'image_' + name_ + '.png',transparent=True, bbox_inches='tight')

        plt.close(fig)

    # return fig, ax


# AQMS raw_raw data read
def AQMS_read_ISO_data(filename_):
    # filename_ = 'C:/_input/60400077.18I'
    # H_, T_secs, T_days, V_, F_ = AQMS_read_ISO_data(filename_)
    try:
        year_ = '20' + filename_[-3:-1]
        day_ = filename_[-7:-4]
        year_day = year_ + '-' + day_

        # find time zone reported
        line_text = ''
        file_object = open(filename_, 'r')
        for i_ in range(8):
            line_text = file_object.readline()
        file_object.close()
        time_zone_correction_hours = float(line_text[-35:-32]) / 10

        # find start and end date-time
        start_in_seconds = time_str_to_seconds(year_day, '%Y-%j')

        T_secs = np.arange(start_in_seconds, start_in_seconds + (1440*60), 60, dtype=int) - (
        time_zone_correction_hours * 60 * 60)
        T_days = time_seconds_to_days(T_secs)

        file_object = open(filename_, 'r')

        number_of_minutes = 0

        for i_ in range(6):
            line_text = file_object.readline()

        number_of_parameters_listed = int(line_text[:5])
        number_of_parameters_shown = int(line_text[5:])

        parameter_codes = {}
        for par_ in range(number_of_parameters_listed):
            line_text = file_object.readline()
            par_name = line_text[6:28]
            parameter_code = line_text[3:6]
            parameter_codes[parameter_code] = par_name
            file_object.readline()

        values_dict = {}
        minutes_dict = {}
        for parameter_number in range(number_of_parameters_shown):
            line_text = file_object.readline()
            parameter_code = line_text[:3]
            parameter_name = parameter_codes[parameter_code]
            number_of_minutes = int(line_text[-6:-1])
            exponent_number = int(line_text[-10:-6])

            parameter_values_list = []
            parameter_flags_list = []
            for line_ in range(number_of_minutes):
                line_text = file_object.read(1)
                if line_text == '\n':
                    line_text = file_object.read(1)
                    parameter_flags_list.append(line_text)
                else:
                    parameter_flags_list.append(line_text)
                line_text = file_object.read(5)
                if parameter_flags_list[-1] == 'N':
                    parameter_values_list.append(0)
                else:
                    parameter_values_list.append(int(line_text) * (10 ** exponent_number))
            file_object.read(1)
            values_dict[parameter_name] = [parameter_values_list, parameter_flags_list]
            minutes_dict[parameter_name] = number_of_minutes

        file_object.close()

        parameter_list_sorted =sorted(list(values_dict.keys()))

        if number_of_minutes > 0 and number_of_parameters_shown > 0:
            V_ = np.zeros((1440, number_of_parameters_shown), dtype=float)
            F_ = np.zeros((1440, number_of_parameters_shown), dtype='<U1')
            F_[:,:] = 'N'
            H_ = np.zeros(number_of_parameters_shown, dtype= '<U22')
            # T_secs = np.zeros(1440, dtype=float)
            # T_days = np.zeros(1440, dtype=float)

            # day_in_seconds = time_str_to_seconds(year_day, '%Y-%j')

            # for r_ in range(number_of_minutes):
            #     T_secs[r_] = day_in_seconds + (r_ * 60)
            #     T_days[r_] = time_seconds_to_days(T_secs[r_])

            for c_, parameter_name in enumerate(parameter_list_sorted):
                H_[c_] = parameter_name
                V_[:minutes_dict[parameter_name], c_] = values_dict[parameter_name][0]
                F_[:minutes_dict[parameter_name], c_] = values_dict[parameter_name][1]

            return H_, T_secs, T_days, V_, F_
        else:
            print('Error, no minutes or no parameters shown')
            print('Filename: ' + filename_)
            print('number_of_minutes: ' + str(number_of_minutes))
            print('number_of_parameters_shown: ' + str(number_of_parameters_shown))
    except BaseException as error_msg:
        exc_type, exc_obj, tb = sys.exc_info()
        print('ERROR loading file:')
        print(filename_)
        print('Error in line: ' + str(tb.tb_lineno) + '\n' + 'Error while refreshing chart \n' + str(error_msg))
        return
def compile_AQMS_ISO_data(file_list, path_output, force_parameters_from_first=False):
    # path_input = "C:/_input/"
    # station_path = 'QF_02/ISO_Data/'
    # file_list = sorted(glob.glob(str(path_input + station_path + '????????.??B')))
    # path_output = "C:/_output/"
    # compile_AQMS_ISO_data(file_list, path_output, force_parameters_from_first=True)


    # check if all files from same station
    station_name = file_list[0][-12:-7]
    # all_files_from_same_station = True
    for filename_ in file_list[1:]:
        if station_name != filename_[-12:-7]:
            print('ERROR! some of the files in file list are not from the same station')
            return

    print('number of files to compile: ' + str(len(file_list)))

    # create file list in chronological order
    file_list_dates_dict = {}
    for filename_ in file_list:
        year_ = '20' + filename_[-3:-1]
        day_ = filename_[-7:-4]
        year_day = year_ + '-' + day_
        file_list_dates_dict[year_day] = filename_
    ordered_file_dict_keys =sorted(list(file_list_dates_dict.keys()))
    file_list_ordered = []
    for key_ in ordered_file_dict_keys:
        file_list_ordered.append(file_list_dates_dict[key_])

    # find time zone reported
    line_text = ''
    file_object = open(file_list[0], 'r')
    for i_ in range(8):
        line_text = file_object.readline()
    file_object.close()
    time_zone_correction_hours = float(line_text[-35:-32]) / 10
    print('time zone correction: ' + str(time_zone_correction_hours))

    # find start and end date-time
    year_ = '20' + file_list_ordered[0][-3:-1]
    day_ = file_list_ordered[0][-7:-4]
    year_day = year_ + '-' + day_
    start_in_seconds = time_str_to_seconds(year_day, '%Y-%j')
    print('start date and time: ' + time_seconds_to_str(start_in_seconds, '%Y-%m-%d %H:%M:%S'))
    #
    year_ = '20' + file_list_ordered[-1][-3:-1]
    day_ = file_list_ordered[-1][-7:-4]
    year_day = year_ + '-' + day_
    stop_in_seconds = time_str_to_seconds(year_day, '%Y-%j') + (24*60*60)
    print('stop date and time: ' + time_seconds_to_str(stop_in_seconds, '%Y-%m-%d %H:%M:%S'))

    number_of_minutes = int((stop_in_seconds - start_in_seconds) / 60)
    print('total number of rows in compiled array: ' + str(number_of_minutes))

    number_of_available_rows = 1440 * len(file_list_ordered)
    print('total number of rows in available data: ' + str(number_of_available_rows))

    # load first file
    print('loading file: ' + file_list_ordered[0])
    H_compiled, T_secs, T_days, V_, F_ = AQMS_read_ISO_data(file_list_ordered[0])

    Master_H = H_compiled

    # initialize out array
    # T_secs_compiled = np.zeros(number_of_minutes, dtype=int)
    T_secs_compiled = np.arange(start_in_seconds, stop_in_seconds, 60, dtype=int) - (time_zone_correction_hours * 60*60)
    # T_days_compiled = np.zeros(number_of_minutes, dtype=float)
    T_days_compiled = time_seconds_to_days(T_secs_compiled)
    V_compiled = np.zeros((number_of_minutes, V_.shape[1]), dtype=float)
    F_compiled = np.zeros((number_of_minutes, V_.shape[1]), dtype='<U1')
    F_compiled[:,:] = 'D'

    # place first file values in out array
    # T_secs_compiled[:1440] = T_secs
    # T_days_compiled[:1440] = T_days
    V_compiled[:1440,:] = V_
    F_compiled[:1440,:] = F_

    for filename_ in file_list_ordered[1:]:
        print('loading file: ' + filename_)
        year_ = '20' + filename_[-3:-1]
        day_ = filename_[-7:-4]
        year_day = year_ + '-' + day_
        start_secs_file = time_str_to_seconds(year_day, '%Y-%j')
        start_row_file = int((start_secs_file - start_in_seconds) / 60)

        H_, T_secs, T_days, V_, F_ = AQMS_read_ISO_data(filename_)

        for par_index in range(H_compiled.shape[0]):
            if H_compiled[par_index] != H_[par_index]:
                if force_parameters_from_first:
                    V_temp = np.zeros((V_.shape[0], Master_H.shape[0]), dtype=float)
                    F_temp = np.zeros((F_.shape[0], Master_H.shape[0]), dtype='<U1')
                    F_temp[:, :] = 'N'
                    for c_master in range(Master_H.shape[0]):
                        for c_temp in range(H_.shape[0]):
                            if Master_H[c_master] == H_[c_temp]:
                                V_temp[:,c_master] = V_[:,c_temp]
                                F_temp[:, c_master] = F_[:, c_temp]
                                break
                    V_ = V_temp
                    F_ = F_temp
                    break
                else:
                    print('ERROR! not the same number/order of parameters in the files')
                    print('last file uploaded: ' + filename_)
                    return

        # place data from file values in out array
        # T_secs_compiled[start_row_file:start_row_file + 1440] = T_secs
        # T_days_compiled[start_row_file:start_row_file + 1440] = T_days
        V_compiled[start_row_file:start_row_file + 1440, :] = V_
        F_compiled[start_row_file:start_row_file + 1440, :] = F_


    time_range_1 = time_seconds_to_str(start_in_seconds, '%Y%m%d_%H%M')
    time_range_2 = time_seconds_to_str(stop_in_seconds, '%Y%m%d_%H%M')
    time_range = time_range_1 + '_' + time_range_2
    station_name = H_compiled[0].split('_')[0]
    np.savez_compressed(path_output + time_range  + '_' + station_name,
                        header_=H_compiled,
                        time_seconds=T_secs_compiled,
                        time_days = T_days_compiled,
                        values_=V_compiled,
                        flags_=F_compiled)
    print('Compiled data saved to: ' + path_output + time_range  + '_' + station_name)
def compile_AQMS_ISO_data_to_netcdf(file_list, path_output):
    # path_input = "C:/_input/"
    # station_path = 'QF_00/ISO_Data/'
    # file_list = sorted(glob.glob(str(path_input + station_path + '????????.??B')))
    # path_output = "C:/_output/"
    # compile_AQMS_ISO_data_to_netcdf(file_list, path_output)


    # check if all files from same station
    station_code = file_list[0][-12:-7]
    # all_files_from_same_station = True
    for filename_ in file_list[1:]:
        if station_code != filename_[-12:-7]:
            print('ERROR! some of the files in file list are not from the same station')
            return

    print('number of files to compile: ' + str(len(file_list)))

    # create file list in chronological order
    file_list_dates_dict = {}
    for filename_ in file_list:
        year_ = '20' + filename_[-3:-1]
        day_ = filename_[-7:-4]
        year_day = year_ + '-' + day_
        file_list_dates_dict[year_day] = filename_
    ordered_file_dict_keys =sorted(list(file_list_dates_dict.keys()))
    file_list_ordered = []
    for key_ in ordered_file_dict_keys:
        file_list_ordered.append(file_list_dates_dict[key_])

    # find start and end date-time
    year_ = '20' + file_list_ordered[0][-3:-1]
    day_ = file_list_ordered[0][-7:-4]
    year_day = year_ + '-' + day_
    start_in_seconds = time_str_to_seconds(year_day, '%Y-%j')
    print('start date and time: ' + time_seconds_to_str(start_in_seconds, '%Y-%m-%d %H:%M:%S'))
    #
    year_ = '20' + file_list_ordered[-1][-3:-1]
    day_ = file_list_ordered[-1][-7:-4]
    year_day = year_ + '-' + day_
    stop_in_seconds = time_str_to_seconds(year_day, '%Y-%j') + (24*60*60)
    print('stop date and time: ' + time_seconds_to_str(stop_in_seconds, '%Y-%m-%d %H:%M:%S'))

    number_of_minutes = int((stop_in_seconds - start_in_seconds) / 60)
    print('total number of rows in compiled array: ' + str(number_of_minutes))

    number_of_available_rows = 1440 * len(file_list_ordered)
    print('total number of rows in available data: ' + str(number_of_available_rows))

    # load first file
    H_compiled, T_secs, T_days, V_, F_ = AQMS_read_ISO_data(file_list_ordered[0])

    # initialize out array
    # T_secs_compiled = np.zeros(number_of_minutes, dtype=int)
    T_secs_compiled = np.arange(start_in_seconds, stop_in_seconds, 60, dtype=int)
    # T_days_compiled = np.zeros(number_of_minutes, dtype=float)
    T_days_compiled = time_seconds_to_days(T_secs_compiled)
    T_str_date = np.array(time_seconds_to_str(T_secs_compiled, '%Y%m%d')).astype(int)
    T_str_time =  np.array(time_seconds_to_str(T_secs_compiled, '%H%M%S')).astype(int)
    V_compiled = np.zeros((number_of_minutes, V_.shape[1]), dtype=float)
    F_compiled = np.zeros((number_of_minutes, V_.shape[1]), dtype=str)
    F_compiled[:,:] = 'N'

    # place first file values in out array
    V_compiled[:1440,:] = V_
    F_compiled[:1440,:] = F_

    for filename_ in file_list_ordered[1:]:
        year_ = '20' + filename_[-3:-1]
        day_ = filename_[-7:-4]
        year_day = year_ + '-' + day_
        start_secs_file = time_str_to_seconds(year_day, '%Y-%j')
        start_row_file = int((start_secs_file - start_in_seconds) / 60)

        H_, T_secs, T_days, V_, F_ = AQMS_read_ISO_data(filename_)

        for par_index in range(H_compiled.shape[0]):
            if H_compiled[par_index] != H_[par_index]:
                print('ERROR! not the same number/order of parameters in the files')
                print('last file uploaded: ' + filename_)
                return

        # place data from file values in out array
        # T_secs_compiled[start_row_file:start_row_file + 1440] = T_secs
        # T_days_compiled[start_row_file:start_row_file + 1440] = T_days
        V_compiled[start_row_file:start_row_file + 1440, :] = V_
        F_compiled[start_row_file:start_row_file + 1440, :] = F_


    time_range_1 = time_seconds_to_str(start_in_seconds, '%Y%m%d_%H%M')
    time_range_2 = time_seconds_to_str(stop_in_seconds, '%Y%m%d_%H%M')
    time_range = time_range_1 + '_' + time_range_2

    station_name = H_compiled[0].split('_')[0]
    out_filename = str(path_output + time_range  + '_' + station_name + '.nc')

    # create save lists
    name_list = []
    units_list = []
    array_list = []
    for par_index in range(H_compiled.shape[0]):
        # values
        name_list.append(H_compiled[par_index][5:].split(' ')[0])
        units_list.append(H_compiled[par_index][-6:].split(' ')[0])
        array_list.append(V_compiled[:,par_index])
        # flags
        name_list.append('flag_' + H_compiled[par_index][5:].split(' ')[0])
        units_list.append('N = no data, A = valid, C = calibration, Z = zero, D = drift')
        array_list.append(F_compiled[:,par_index])

    # add the actual time series in string, seconds, and days
    name_list.append('date_in_YYYYmmDD')
    units_list.append('YYYYmmDD in local time (UTC+3)')
    array_list.append(T_str_date)
    name_list.append('time_in_HHMMSS')
    units_list.append('HHMMSS in local time (UTC+3)')
    array_list.append(T_str_time)
    #
    name_list.append('time_in_seconds')
    units_list.append('each unit is a second since [1970 jan 01 00:00:00] in local time (UTC+3)')
    array_list.append(T_secs_compiled)
    #
    name_list.append('time_in_days')
    units_list.append('each unit is a days since 0001-01-01 in local time (UTC+3)')
    array_list.append(T_days_compiled)

    # create attribute list
    attributes_tuple_list = [('station_name', station_name),
                             ('station_code', station_code),
                             ('number_of_compiled_files', str(len(file_list))),
                             ('number_of_missin_rows', str(number_of_minutes - number_of_available_rows))]

    save_time_series_as_netcdf(array_list, name_list, units_list, attributes_tuple_list, out_filename)


    # np.savez_compressed(str(path_output + time_range  + '_' + station_name),
    #                     header_=H_compiled,
    #                     time_seconds=T_secs_compiled,
    #                     time_days = T_days_compiled,
    #                     values_=V_compiled,
    #                     flags_=F_compiled)
    print('Compiled data saved to: ' + out_filename)


# data averaging
def average_all_data_files(filename_, number_of_seconds, WD_index = None, WS_index = None,
                           min_data_number=None, cumulative_parameter_list=None):
    header_, values_ = load_time_columns(filename_)
    time_sec = time_days_to_seconds(values_[:,0])

    # wind tratment
    if WD_index is not None and WS_index is not None:
        print('wind averaging underway for parameters: ' + header_[WD_index] + ' and ' + header_[WS_index])
        # converting wind parameters to cartesian
        WD_ = values_[:,WD_index]
        WS_ = values_[:,WS_index]
        North_, East_ = polar_to_cart(WD_, WS_)
        values_[:,WD_index] = North_
        values_[:,WS_index] = East_

    # averaging
    if min_data_number is None: min_data_number = int(number_of_seconds/60 * .75)
    if cumulative_parameter_list is None:
        Index_mean,Values_mean = mean_discrete(time_sec, values_[:,2:], number_of_seconds,
                                               time_sec[0], min_data = min_data_number,
                                               cumulative_parameter_indx= None)
    else:
        Index_mean,Values_mean = mean_discrete(time_sec, values_[:,2:], number_of_seconds,
                                               time_sec[0], min_data = min_data_number,
                                               cumulative_parameter_indx=np.array(cumulative_parameter_list) - 2)


    if WD_index is not None and WS_index is not None:
        # converting wind parameters to polar
        North_ = Values_mean[:,WD_index - 2]
        East_ = Values_mean[:,WS_index - 2]
        WD_, WS_ = cart_to_polar(North_, East_)
        Values_mean[:,WD_index - 2] = WD_
        Values_mean[:,WS_index - 2] = WS_

    output_filename = filename_.split('.')[0]
    output_filename += '_' + str(int(number_of_seconds/60)) + '_minute_mean' + '.csv'
    save_array_to_disk(header_[2:], Index_mean, Values_mean, output_filename)
    print('Done!')
    print('saved at: ' + output_filename)
def median_discrete(Index_, Values_, avr_size, first_index, min_data=1, position_=0.0):
    # Index_: n by 1 numpy array to look for position,
    # Values_: n by m numpy array, values to be averaged
    # avr_size in same units as Index_,
    # first_index is the first discrete index on new arrays.
    # min_data is minimum amount of data for average to be made (optional, default = 1)
    # position_ will determine where is the stamp located; 0 = beginning, .5 = mid, 1 = top (optional, default = 0)
    # this will average values from Values_ that are between Index_[n:n+avr_size)
    # will return: Index_averaged, Values_averaged

    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(Index_.shape[0]-1):
        if Index_[x]==Index_[x] and Index_[x+1]==Index_[x+1]:
            if Index_[x+1] < Index_[x]:
                always_ascending = 0
    if always_ascending == 0:
        MM_ = np.column_stack((Index_,Values_))
        MM_sorted = MM_[MM_[:,0].argsort()] # sort by first column
        Index_ = MM_sorted[:,0]
        Values_ = MM_sorted[:,1:]

    # error checking!
    if Index_.shape[0] != Values_.shape[0]:
        return None, None
    if Index_[-1] < first_index:
        return None, None
    if min_data < 1:
        return None, None

    # initialize averaged matrices
    final_index = np.nanmax(Index_)
    total_averaged_rows = int((final_index-first_index)/avr_size) + 1
    if len(Values_.shape) == 1:
        Values_median = np.zeros(total_averaged_rows)
        Values_median[:] = np.nan
    else:
        Values_median = np.zeros((total_averaged_rows,Values_.shape[1]))
        Values_median[:,:] = np.nan
    Index_averaged = np.zeros(total_averaged_rows)
    for r_ in range(total_averaged_rows):
        Index_averaged[r_] = first_index + (r_ * avr_size)

    Index_averaged -= (position_ * avr_size)
    Values_25pr = np.array(Values_median)
    Values_75pr = np.array(Values_median)
    Std_ = np.array(Values_median)


    indx_avr_r = -1
    last_raw_r = 0
    r_raw_a = 0
    r_raw_b = 1
    while indx_avr_r <= total_averaged_rows-2:
        indx_avr_r += 1
        indx_a = Index_averaged[indx_avr_r]
        indx_b = Index_averaged[indx_avr_r] + avr_size
        stamp_population = 0
        for r_raw in range(last_raw_r,Index_.shape[0]):
            if indx_a <= Index_[r_raw] < indx_b:
                if stamp_population == 0: r_raw_a = r_raw
                r_raw_b = r_raw + 1
                stamp_population += 1
            if Index_[r_raw] >= indx_b:
                last_raw_r = r_raw
                break
        if stamp_population >= min_data:
            if len(Values_.shape) == 1:
                Values_median[indx_avr_r] = np.nanmedian(Values_[r_raw_a:r_raw_b])
                Values_25pr[indx_avr_r] = np.nanmedian(Values_[r_raw_a:r_raw_b])
                Values_75pr[indx_avr_r] = np.nanmedian(Values_[r_raw_a:r_raw_b])
                Std_[indx_avr_r] = np.nanstd(Values_[r_raw_a:r_raw_b])
            else:
                for c_ in range(Values_.shape[1]):
                    Values_median[indx_avr_r,c_] = np.nanmedian(Values_[r_raw_a:r_raw_b,c_])
                    Values_25pr[indx_avr_r,c_] = np.nanpercentile(Values_[r_raw_a:r_raw_b,c_],25)
                    Values_75pr[indx_avr_r,c_] = np.nanpercentile(Values_[r_raw_a:r_raw_b,c_],75)
                    Std_[indx_avr_r] = np.nanstd(Values_[r_raw_a:r_raw_b],c_)


    Index_averaged = Index_averaged + (position_ * avr_size)

    return Index_averaged,Values_median,Values_25pr,Values_75pr, Std_
def mean_discrete(Index_, Values_, avr_size, first_index,
                  min_data=1, position_=0., cumulative_parameter_indx=None, last_index=None, show_progress=True):
    """
    this will average values from Values_ that are between Index_[n:n+avr_size)
    :param Index_: n by 1 numpy array to look for position,
    :param Values_: n by m numpy array, values to be averaged
    :param avr_size: in same units as Index_
    :param first_index: is the first discrete index on new arrays.
    :param min_data: is minimum amount of data for average to be made (optional, default = 1)
    :param position_: will determine where is the stamp located; 0 = beginning, .5 = mid, 1 = top (optional, default = 0)
    :param cumulative_parameter_indx: in case there is any column in Values_ to be summed, not averaged. Most be a list
    :param last_index: in case you want to force the returned series to some fixed period/length
    :param show_progress: bool, if true will print a progress bar
    :return: Index_averaged, Values_averaged
    """

    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(Index_.shape[0]-1):
        if Index_[x]==Index_[x] and Index_[x+1]==Index_[x+1]:
            if Index_[x+1] < Index_[x]:
                always_ascending = 0
    if always_ascending == 0:
        MM_ = np.column_stack((Index_,Values_))
        MM_sorted = MM_[MM_[:,0].argsort()] # sort by first column
        Index_ = MM_sorted[:,0]
        Values_ = MM_sorted[:,1:]

    # error checking!
    if Index_.shape[0] != Values_.shape[0]:
        print('error during shape check! Index_.shape[0] != Values_.shape[0]')
        return None, None
    if Index_[-1] < first_index:
        print('error during shape check! Index_[-1] < first_index')
        return None, None
    if min_data < 1:
        print('error during shape check! min_data < 1')
        return None, None

    # initialize averaged matrices
    if last_index is None:
        final_index = np.nanmax(Index_)
    else:
        final_index = last_index

    total_averaged_rows = int((final_index-first_index)/avr_size) + 1
    if len(Values_.shape) == 1:
        Values_mean = np.zeros(total_averaged_rows)
        Values_mean[:] = np.nan
    else:
        Values_mean = np.zeros((total_averaged_rows,Values_.shape[1]))
        Values_mean[:,:] = np.nan
    Index_averaged = np.zeros(total_averaged_rows)
    for r_ in range(total_averaged_rows):
        Index_averaged[r_] = first_index + (r_ * avr_size)

    Index_averaged -= (position_ * avr_size)

    indx_avr_r = -1
    last_raw_r = 0
    r_raw_a = 0
    r_raw_b = 1
    while indx_avr_r <= total_averaged_rows-2:
        if show_progress: p_progress_bar(indx_avr_r, total_averaged_rows-2, extra_text='averaged')
        indx_avr_r += 1
        indx_a = Index_averaged[indx_avr_r]
        indx_b = Index_averaged[indx_avr_r] + avr_size
        stamp_population = 0
        for r_raw in range(last_raw_r,Index_.shape[0]):
            if indx_a <= Index_[r_raw] < indx_b:
                if stamp_population == 0: r_raw_a = r_raw
                r_raw_b = r_raw + 1
                stamp_population += 1
            if Index_[r_raw] >= indx_b:
                last_raw_r = r_raw
                break
        if stamp_population >= min_data:
            if len(Values_.shape) == 1:
                if cumulative_parameter_indx is not None:
                    Values_mean[indx_avr_r] = np.nansum(Values_[r_raw_a:r_raw_b])
                else:
                    Values_mean[indx_avr_r] = np.nanmean(Values_[r_raw_a:r_raw_b])
            else:
                for c_ in range(Values_.shape[1]):
                    if cumulative_parameter_indx is not None:
                        if c_ in cumulative_parameter_indx:
                            Values_mean[indx_avr_r, c_] = np.nansum(Values_[r_raw_a:r_raw_b, c_])
                        else:
                            Values_mean[indx_avr_r, c_] = np.nanmean(Values_[r_raw_a:r_raw_b, c_])
                    else:
                        Values_mean[indx_avr_r,c_] = np.nanmean(Values_[r_raw_a:r_raw_b,c_])

    Index_averaged = Index_averaged + (position_ * avr_size)

    return Index_averaged,Values_mean
def mean_discrete_std(Index_, Values_, avr_size, first_index, min_data=1, position_=0.):
    # Index_: n by 1 numpy array to look for position,
    # Values_: n by m numpy array, values to be averaged
    # avr_size in same units as Index_,
    # first_index is the first discrete index on new arrays.
    # min_data is minimum amount of data for average to be made (optional, default = 1)
    # position_ will determine where is the stamp located; 0 = beginning, .5 = mid, 1 = top (optional, default = 0)
    # this will average values from Values_ that are between Index_[n:n+avr_size)
    # will return: Index_averaged, Values_averaged

    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(Index_.shape[0]-1):
        if Index_[x]==Index_[x] and Index_[x+1]==Index_[x+1]:
            if Index_[x+1] < Index_[x]:
                always_ascending = 0
    if always_ascending == 0:
        MM_ = np.column_stack((Index_,Values_))
        MM_sorted = MM_[MM_[:,0].argsort()] # sort by first column
        Index_ = MM_sorted[:,0]
        Values_ = MM_sorted[:,1:]

    # error checking!
    if Index_.shape[0] != Values_.shape[0]:
        return None, None
    if Index_[-1] < first_index:
        return None, None
    if min_data < 1:
        return None, None

    # initialize averaged matrices
    final_index = np.nanmax(Index_)
    total_averaged_rows = int((final_index-first_index)/avr_size) + 1
    if len(Values_.shape) == 1:
        Values_mean = np.zeros(total_averaged_rows)
        Values_mean[:] = np.nan
    else:
        Values_mean = np.zeros((total_averaged_rows,Values_.shape[1]))
        Values_mean[:,:] = np.nan
    Index_averaged = np.zeros(total_averaged_rows)
    for r_ in range(total_averaged_rows):
        Index_averaged[r_] = first_index + (r_ * avr_size)

    Index_averaged -= (position_ * avr_size)
    Std_ = np.array(Values_mean)

    indx_avr_r = -1
    last_raw_r = 0
    r_raw_a = 0
    r_raw_b = 1
    while indx_avr_r <= total_averaged_rows-2:
        indx_avr_r += 1
        indx_a = Index_averaged[indx_avr_r]
        indx_b = Index_averaged[indx_avr_r] + avr_size
        stamp_population = 0
        for r_raw in range(last_raw_r,Index_.shape[0]):
            if indx_a <= Index_[r_raw] < indx_b:
                if stamp_population == 0: r_raw_a = r_raw
                r_raw_b = r_raw + 1
                stamp_population += 1
            if Index_[r_raw] >= indx_b:
                last_raw_r = r_raw
                break
        if stamp_population >= min_data:
            if len(Values_.shape) == 1:
                Values_mean[indx_avr_r] = np.nanmean(Values_[r_raw_a:r_raw_b])
                Std_[indx_avr_r] = np.nanstd(Values_[r_raw_a:r_raw_b])
            else:
                for c_ in range(Values_.shape[1]):
                    Values_mean[indx_avr_r,c_] = np.nanmean(Values_[r_raw_a:r_raw_b,c_])
                    Std_[indx_avr_r] = np.nanstd(Values_[r_raw_a:r_raw_b],c_)

    Index_averaged = Index_averaged + (position_ * avr_size)

    return Index_averaged,Values_mean,Std_
def sum_discrete_3D_array(Index_, array_3D, sum_size, first_index, min_data=1, position_=0.):
    # Index_: n by 1 numpy array to look for position,
    # Values_: n by m numpy array, values to be averaged
    # avr_size in same units as Index_,
    # first_index is the first discrete index on new arrays.
    # min_data is minimum amount of data for average to be made (optional, default = 1)
    # position_ will determine where is the stamp located; 0 = beginning, .5 = mid, 1 = top (optional, default = 0)
    # this will average values from Values_ that are between Index_[n:n+avr_size)
    # will return: Index_averaged, Values_averaged

    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(Index_.shape[0]-1):
        if Index_[x]==Index_[x] and Index_[x+1]==Index_[x+1]:
            if Index_[x+1] < Index_[x]:
                always_ascending = 0
    if always_ascending == 0:
        print('Error, index must always be ascending')
        return None, None

    # error checking!
    if Index_.shape[0] != array_3D.shape[0]:
        print('Error, axes 0 of 3D array must be equal to Index size')
        return None, None
    if Index_[-1] < first_index:
        print('Error, first')
        return None, None

    # initialize averaged matrices
    final_index = np.nanmax(Index_)
    total_summed_rows = int((final_index-first_index)/sum_size) + 1

    Values_sum = np.zeros((total_summed_rows, array_3D.shape[1], array_3D.shape[2]))
    Values_sum[:,:,:] = np.nan
    Index_summed = np.zeros(total_summed_rows)
    for r_ in range(total_summed_rows):
        Index_summed[r_] = first_index + (r_ * sum_size)

    Index_summed -= (position_ * sum_size)

    indx_sum_r = -1
    last_raw_r = 0
    r_raw_a = 0
    r_raw_b = 1
    while indx_sum_r <= total_summed_rows-2:
        indx_sum_r += 1
        indx_a = Index_summed[indx_sum_r]
        indx_b = Index_summed[indx_sum_r] + sum_size
        stamp_population = 0
        for r_raw in range(last_raw_r,Index_.shape[0]):
            if indx_a <= Index_[r_raw] < indx_b:
                if stamp_population == 0: r_raw_a = r_raw
                r_raw_b = r_raw + 1
                stamp_population += 1
            if Index_[r_raw] >= indx_b:
                last_raw_r = r_raw
                break
        if stamp_population >= min_data:
            Values_sum[indx_sum_r,:,:] = np.nansum(array_3D[r_raw_a:r_raw_b,:,:],axis=0)
    Index_summed = Index_summed + (position_ * sum_size)

    return Index_summed,Values_sum
def row_average_rolling(arr_, average_size):
    result_ = np.array(arr_) * np.nan

    for r_ in range(arr_.shape[0] +1 - int(average_size)):
        result_[r_] = np.nanmean(arr_[r_ : r_ + average_size])

    return result_
def row_average_std_rolling(arr_, average_size):
    means_ = np.zeros(arr_.shape[0]) * np.nan
    STDS_ =np.zeros(arr_.shape[0]) * np.nan
    for r_ in range(arr_.shape[0] + 1 - int(average_size)):
        means_[r_] = np.nanmean(arr_[r_: r_ + average_size])
        STDS_[r_] = np.nanstd(arr_[r_: r_ + average_size])

    return means_, STDS_
def row_average_discrete_1D(arr_, average_size):
    result_ = np.zeros(int(arr_.shape[0]/average_size)) * np.nan

    for r_ in range(result_.shape[0]):
        result_[r_] = np.nanmean(arr_[int(r_* average_size) : int(r_* average_size) + average_size], axis=0)

    return result_
def row_average_discrete_2D(arr_, average_size):
    result_ = np.zeros((int(arr_.shape[0]/average_size), arr_.shape[1])) * np.nan

    for r_ in range(result_.shape[0]):
        result_[r_,:] = np.nanmean(arr_[int(r_* average_size) : int(r_* average_size) + average_size], axis=0)

    return result_
def row_average_discrete_3D(arr_, average_size):
    result_ = np.zeros((int(arr_.shape[0]/average_size), arr_.shape[1], arr_.shape[2])) * np.nan

    for r_ in range(result_.shape[0]):
        result_[r_,:,:] = np.nanmean(arr_[int(r_* average_size) : int(r_* average_size) + average_size], axis=0)

    return result_
def column_average_discrete_2D(arr_, average_size):
    result_ = np.zeros((arr_.shape[0], int(arr_.shape[1]/average_size))) * np.nan

    for c_ in range(result_.shape[1]):
        result_[:, c_] = np.nanmean(arr_[:, int(c_* average_size) : int(c_* average_size) + average_size], axis=1)

    return result_
def column_average_discrete_3D(arr_, average_size):
    result_ = np.zeros((arr_.shape[0], int(arr_.shape[1]/average_size), arr_.shape[2])) * np.nan

    for c_ in range(result_.shape[1]):
        result_[:, c_,:] = np.nanmean(arr_[:, int(c_* average_size) : int(c_* average_size) + average_size,:], axis=1)

    return result_
def row_sum_discrete_2D(arr_, sum_size):
    result_ = np.zeros((int(arr_.shape[0]/sum_size), arr_.shape[1])) * np.nan

    for r_ in range(result_.shape[0]):
        result_[r_,:] = np.nansum(arr_[int(r_* sum_size) : int(r_* sum_size) + sum_size], axis=0)

    return result_
def column_sum_discrete_2D(arr_, sum_size):
    result_ = row_sum_discrete_2D(arr_.T, sum_size).T

    return result_
def average_all_data_files_monthly(filename_, number_of_seconds, min_data_number = None,
                                   WD_index = None, WS_index = None, cumulative_parameter_list=None):
    header_, values_ = load_time_columns(filename_)
    time_sec = time_days_to_seconds(values_[:,0])

    # wind tratment
    if WD_index is not None and WS_index is not None:
        print('wind averaging underway for parameters: ' + header_[WD_index] + ' and ' + header_[WS_index])
        # converting wind parameters to cartesian
        WD_ = values_[:,WD_index]
        WS_ = values_[:,WS_index]
        North_, East_ = polar_to_cart(WD_, WS_)
        values_[:,WD_index] = North_
        values_[:,WS_index] = East_

    # averaging
    if min_data_number is None: min_data_number = int(number_of_seconds/60 * .75)
    if cumulative_parameter_list is None:
        Index_mean,Values_mean = mean_discrete(time_sec, values_[:,2:], number_of_seconds,
                                               time_sec[0], min_data = min_data_number,
                                               cumulative_parameter_indx= None)
    else:
        Index_mean,Values_mean = mean_discrete(time_sec, values_[:,2:], number_of_seconds,
                                               time_sec[0], min_data = min_data_number,
                                               cumulative_parameter_indx=np.array(cumulative_parameter_list) - 2)


    if WD_index is not None and WS_index is not None:
        # converting wind parameters to polar
        North_ = Values_mean[:,WD_index - 2]
        East_ = Values_mean[:,WS_index - 2]
        WD_, WS_ = cart_to_polar(North_, East_)
        Values_mean[:,WD_index - 2] = WD_
        Values_mean[:,WS_index - 2] = WS_

    output_filename = filename_.split('.')[0]
    output_filename += '_' + str(int(number_of_seconds/60)) + '_minute_mean' + '.csv'
    save_array_to_disk(header_[2:], Index_mean, Values_mean, output_filename)
    print('Done!')
    print('saved at: ' + output_filename)
def rolling_window(array_, window_size):
    shape = array_.shape[:-1] + (array_.shape[-1] - window_size + 1, window_size)
    strides = array_.strides + (array_.strides[-1],)
    return np.lib.stride_tricks.as_strided(array_, shape=shape, strides=strides)
def sliding_window_view(arr, window_shape, steps):
    """ Produce a view from a sliding, striding window over `arr`.
        The window is only placed in 'valid' positions - no overlapping
        over the boundary.
        Parameters
        ----------
        arr : numpy.ndarray, shape=(...,[x, (...), z])
            The array to slide the window over.
        window_shape : Sequence[int]
            The shape of the window to raster: [Wx, (...), Wz],
            determines the length of [x, (...), z]
        steps : Sequence[int]
            The step size used when applying the window
            along the [x, (...), z] directions: [Sx, (...), Sz]
        Returns
        -------
        view of `arr`, shape=([X, (...), Z], ..., [Wx, (...), Wz])
            Where X = (x - Wx) // Sx + 1
        Notes
        -----
        In general, given
          `out` = sliding_window_view(arr,
                                      window_shape=[Wx, (...), Wz],
                                      steps=[Sx, (...), Sz])
           out[ix, (...), iz] = arr[..., ix*Sx:ix*Sx+Wx,  (...), iz*Sz:iz*Sz+Wz]
         Examples
         --------
         >>> import numpy as np
         >>> x = np.arange(9).reshape(3,3)
         >>> x
         array([[0, 1, 2],
                [3, 4, 5],
                [6, 7, 8]])
         >>> y = sliding_window_view(x, window_shape=(2, 2), steps=(1, 1))
         >>> y
         array([[[[0, 1],
                  [3, 4]],
                 [[1, 2],
                  [4, 5]]],
                [[[3, 4],
                  [6, 7]],
                 [[4, 5],
                  [7, 8]]]])
        >>> np.shares_memory(x, y)
         True
        # Performing a neural net style 2D conv (correlation)
        # placing a 4x4 filter with stride-1
        >>> data = np.random.rand(10, 3, 16, 16)  # (N, C, H, W)
        >>> filters = np.random.rand(5, 3, 4, 4)  # (F, C, Hf, Wf)
        >>> windowed_data = sliding_window_view(data,
        ...                                     window_shape=(4, 4),
        ...                                     steps=(1, 1))
        >>> conv_out = np.tensordot(filters,
        ...                         windowed_data,
        ...                         axes=[[1,2,3], [3,4,5]])
        # (F, H', W', N) -> (N, F, H', W')
        >>> conv_out = conv_out.transpose([3,0,1,2])
         """
    import numpy as np
    from numpy.lib.stride_tricks import as_strided
    in_shape = np.array(arr.shape[-len(steps):])  # [x, (...), z]
    window_shape = np.array(window_shape)  # [Wx, (...), Wz]
    steps = np.array(steps)  # [Sx, (...), Sz]
    nbytes = arr.strides[-1]  # size (bytes) of an element in `arr`

    # number of per-byte steps to take to fill window
    window_strides = tuple(np.cumprod(arr.shape[:0:-1])[::-1]) + (1,)
    # number of per-byte steps to take to place window
    step_strides = tuple(window_strides[-len(steps):] * steps)
    # number of bytes to step to populate sliding window view
    strides = tuple(int(i) * nbytes for i in step_strides + window_strides)

    outshape = tuple((in_shape - window_shape) // steps + 1)
    # outshape: ([X, (...), Z], ..., [Wx, (...), Wz])
    outshape = outshape + arr.shape[:-len(steps)] + tuple(window_shape)
    return as_strided(arr, shape=outshape, strides=strides, writeable=False)



# wind direction related
def polar_to_cart(WD_, WS_):
    WD_rad = np.radians(WD_)
    North_ = WS_ * np.cos(WD_rad)
    East_ = WS_ * np.sin(WD_rad)
    return North_, East_
def cart_to_polar(North_, East_):
    try:
        WS_ = np.sqrt(North_**2 + East_**2)
        WD_with_neg = np.degrees(np.arctan2(East_, North_))
        mask_ = np.zeros(WD_with_neg.shape[0])
        mask_[WD_with_neg < 0] = 360
        WD_ = WD_with_neg + mask_
    except:
        WS_ = np.sqrt(North_**2 + East_**2)
        WD_with_neg = np.degrees(np.arctan2(East_, North_))
        mask_ = 0
        if WD_with_neg < 0:
            mask_ = 360
        WD_ = WD_with_neg + mask_
    return WD_, WS_


# time transforms
def create_time_series_seconds(start_time_str, stop_time_str, step_size):
    start_time_sec = float(time_days_to_seconds(convert_any_time_type_to_days(start_time_str)))
    stop__time_sec = float(time_days_to_seconds(convert_any_time_type_to_days(stop_time_str )))

    time_list = []

    t_ = start_time_sec

    while t_ < stop__time_sec:
        time_list.append(t_)
        t_ += step_size

    return np.array(time_list)
def combine_by_index(reference_index, var_index, var_values):
    """
    finds point from var_index to each reference_index point, has to be exact, if not found then nan
    :param reference_index: 1d array
    :param var_index: 1d array of same size as var_values
    :param var_values: 1d array of same size as var_index
    :return: reindexed_var_values of same size as reference_index
    """

    if len(var_values.shape) > 1:
        raise_error('var_values array is 2D, this is not yet implemented. Get to it...')


    rows_ref = reference_index.shape[0]
    rows_var = var_index.shape[0]

    # check that both index arrs are ascending
    if np.nanmin(np.diff(reference_index)) < 0:
        # sort
        reference_index_asc = reference_index[reference_index.argsort()]
    else:
        reference_index_asc = reference_index

    if np.nanmin(np.diff(var_index)) < 0:
        # sort
        vars_2D_arr_sorted = array_2D_sort_ascending_by_column(np.column_stack((var_index, var_values)))
        var_index_asc = vars_2D_arr_sorted[: , 0]
        var_values_asc = vars_2D_arr_sorted[: , 1:]
    else:
        var_index_asc = var_index
        var_values_asc = var_values

    r_ref = -1
    r_var = -1  # time_to_row_sec(reference_index_asc, var_index_asc[0])
    output_ref_var = np.zeros(reference_index_asc.shape, dtype=float) * np.nan
    while r_ref < rows_ref -1:
        r_ref += 1
        while r_var < rows_var -1:
            r_var += 1
            if var_index_asc[r_var] == reference_index_asc[r_ref]:
                output_ref_var[r_ref] = var_values_asc[r_var]
                break
            elif var_index_asc[r_var] > reference_index_asc[r_ref]:
                r_var -= 1
                break
    return output_ref_var
def time_seconds_to_days(time_in_seconds):
    try:
        # try array type first
        time_days = time_in_seconds / 86400
    except:
        # must likely list
        time_days = np.array(time_in_seconds) / 86400
    return time_days
def time_days_to_seconds(time_in_days):
    try:
        # try array type first
        time_secs = time_in_days * 86400
    except:
        # must likely list
        time_secs = np.array(time_in_days) * 86400
    return time_secs
def time_str_to_seconds(time_str, time_format):
    # defining time arrays
    if isinstance(time_str, str):
        time_seconds = calendar.timegm(time.strptime(time_str, time_format))
    else:
        time_seconds = np.array([calendar.timegm(time.strptime(time_string_record, time_format))
                                 for time_string_record in time_str])
    return time_seconds
def time_seconds_to_str(time_in_seconds, time_format):
    try:
        x = len(time_in_seconds)
        if isinstance(time_in_seconds, list):
            time_in_seconds = np.array(time_in_seconds)
        temp_array = np.zeros(time_in_seconds.shape[0],dtype="<U32")
        for r_ in range(time_in_seconds.shape[0]):
            temp_array[r_] = datetime.utcfromtimestamp(time_in_seconds[r_]).strftime(time_format)
        return temp_array
    except:
        return datetime.utcfromtimestamp(time_in_seconds).strftime(time_format)
def time_str_to_days(time_str, time_format):
    return time_seconds_to_days(time_str_to_seconds(time_str, time_format))
def time_days_to_str(time_in_days, time_format):
    return time_seconds_to_str(time_days_to_seconds(time_in_days), time_format)
def time_seconds_to_5C_array(time_in_seconds):
    if isinstance(time_in_seconds, int):
        out_array = np.zeros(5, dtype=int)
        out_array[0] = datetime.utcfromtimestamp(time_in_seconds).strftime('%Y')
        out_array[1] = datetime.utcfromtimestamp(time_in_seconds).strftime('%m')
        out_array[2] = datetime.utcfromtimestamp(time_in_seconds).strftime('%d')
        out_array[3] = datetime.utcfromtimestamp(time_in_seconds).strftime('%H')
        out_array[4] = datetime.utcfromtimestamp(time_in_seconds).strftime('%M')
    else:
        out_array = np.zeros((time_in_seconds.shape[0], 5), dtype=int)
        for r_ in range(time_in_seconds.shape[0]):
            out_array[r_, 0] = datetime.utcfromtimestamp(time_in_seconds[r_]).strftime('%Y')
            out_array[r_, 1] = datetime.utcfromtimestamp(time_in_seconds[r_]).strftime('%m')
            out_array[r_, 2] = datetime.utcfromtimestamp(time_in_seconds[r_]).strftime('%d')
            out_array[r_, 3] = datetime.utcfromtimestamp(time_in_seconds[r_]).strftime('%H')
            out_array[r_, 4] = datetime.utcfromtimestamp(time_in_seconds[r_]).strftime('%M')
    return out_array
def time_era5_to_seconds(time_in_era5):
    time_in_era5_in_seconds = np.array(time_in_era5, dtype=float) * 60 * 60
    time_format_era5 = 'hours since %Y-%m-%d %H:%M'
    time_seconds_start = calendar.timegm(time.strptime('hours since 1900-01-01 00:00', time_format_era5))
    time_seconds_epoc = time_in_era5_in_seconds + time_seconds_start
    return time_seconds_epoc
def time_seconds_to_era5(time_in_seconds):
    time_in_hours = time_in_seconds / 3600
    time_hours_start = time_era5_to_seconds(0)/3600
    time_era5 = time_in_hours - time_hours_start
    return time_era5
def time_seconds_to_struct(time_in_seconds):
    time_struct_list = []
    for t_ in time_in_seconds:
        time_struct_list.append(time.gmtime(t_))
    return time_struct_list
def time_struct_to_seconds(time_struct):
    time_sec = time_str_to_seconds(time_struct.strftime(time_format_YMDHMS), time_format_YMDHMS)
    return time_sec
def time_to_row_str(time_array_seconds, time_stamp_str_YYYYmmDDHHMM):
    time_stamp_seconds = time_str_to_seconds(time_stamp_str_YYYYmmDDHHMM, time_format_parsivel)
    row_ = np.argmin(np.abs(time_array_seconds - time_stamp_seconds))
    return row_
def time_to_row_sec(time_array_seconds, time_stamp_sec):
    row_ = np.argmin(np.abs(time_array_seconds - time_stamp_sec))
    return row_
def time_period_to_row_tuple(time_array_seconds, time_stamp_start_stop_str_YYYYmmDDHHMM):
    time_start_seconds = time_str_to_seconds(time_stamp_start_stop_str_YYYYmmDDHHMM.split('_')[0], time_format_parsivel)
    time_stop_seconds = time_str_to_seconds(time_stamp_start_stop_str_YYYYmmDDHHMM.split('_')[1], time_format_parsivel)
    row_1 = np.argmin(np.abs(time_array_seconds - time_start_seconds))
    row_2 = np.argmin(np.abs(time_array_seconds - time_stop_seconds))
    return row_1, row_2
def convert_any_time_type_to_days(time_series, print_show=False):
    time_secs_normal_range = [646800000, 2540240000]
    time_days_normal_range = time_seconds_to_days(time_secs_normal_range)

    # check if it is a str
    if isinstance(time_series, str):
        # try each known str_time_format and return time_seconds_to_days()
        for time_str_format in time_str_formats:
            try:
                time_in_secs = time_str_to_seconds(time_series, time_str_format)
                return time_seconds_to_days(time_in_secs)
            except:
                pass
        if print_show: print('could not find correct time string format! returning nan')
        return np.nan

    # if not str, check if it is a single number
    if isinstance(time_series, float) or isinstance(time_series, int):
        if time_secs_normal_range[0] < time_series < time_secs_normal_range[1]:
            return time_seconds_to_days(time_series)
        elif time_days_normal_range[0] < time_series < time_days_normal_range[1]:
            return time_series
        else:
            if print_show: print('could not find correct time number correction! returning nan')
            return np.nan
    else:
        # multiple items
        # check if series of strs
        try:
            if isinstance(time_series[0], str):
                # try each known str_time_format and return time_seconds_to_days()
                for time_str_format in time_str_formats:
                    try:
                        time_in_secs = time_str_to_seconds(time_series, time_str_format)
                        return time_seconds_to_days(time_in_secs)
                    except:
                        pass
                if print_show: print('could not find correct time string format! returning None')
                return None
            else:
                # get max and min
                time_series_min = np.nanmin(time_series)
                time_series_max = np.nanmax(time_series)

                if time_secs_normal_range[0] < time_series_min and time_series_max < time_secs_normal_range[1]:
                    return time_seconds_to_days(time_series)
                elif time_days_normal_range[0] < time_series_min and time_series_max < time_days_normal_range[1]:
                    return time_series
                else:
                    if print_show: print('could not find correct time number correction! returning None')
                    return None

        except:
            if print_show: print('unknown type of data, returning None')
            return None
def time_rman_blist_to_seconds(rman_2D_b_array, time_format='%H:%M:%S %d/%m/%Y'):
    """
    takes bite arrays and converts to seconds
    :param rman_2D_b_array: array where each row is a time stamp and columns are a character in bite format
    :param time_format: string that defines the structure of the characters in each time stamp
    :return: seconds array
    """

    time_str_list = []
    for row_ in range(rman_2D_b_array.shape[0]):
        t_str = ''
        for i in rman_2D_b_array[row_]:
            t_str = t_str + i.decode('UTF-8')
        time_str_list.append(t_str)

    time_seconds = time_str_to_seconds(time_str_list, time_format)

    return time_seconds

def day_night_discrimination(hour_of_day,values_,day_hours_range_tuple_inclusive):
    day_ = np.array(values_) * np.nan
    night_ = np.array(values_) * np.nan
    for r_ in range(values_.shape[0]):
        if day_hours_range_tuple_inclusive[0] <= hour_of_day[r_] <= day_hours_range_tuple_inclusive[1]:
            day_[r_,:] = values_[r_,:]
        else:
            night_[r_,:] = values_[r_,:]
    return day_, night_
def create_time_stamp_list_between_two_times(datetime_start_str,
                                             datetime_end_str,
                                             time_steps_in_sec,
                                             input_time_format='%Y%m%d%H%M',
                                             output_list_format='%Y%m%d%H%M'):

    datetime_start_sec = time_str_to_seconds(datetime_start_str, input_time_format)
    datetime_end_sec = time_str_to_seconds(datetime_end_str, input_time_format)
    number_of_images = (datetime_end_sec - datetime_start_sec) / time_steps_in_sec
    datetime_list_str = []
    for time_stamp_index in range(int(number_of_images)):
        datetime_list_str.append(time_seconds_to_str(datetime_start_sec + (time_stamp_index * time_steps_in_sec),
                                                     output_list_format))

    return datetime_list_str



# save charts
def save_time_series_charts(filename_, parameter_list):
    header_, values_, time_str = load_data_to_return_return(filename_)

    for par_index in parameter_list:
        plot_format_mayor = mdates.DateFormatter('%b', tz=tz_UTC)
        fig, ax = plt.subplots(figsize=(20, 10))
        ax.plot_date(values_[:,0],values_[:,par_index],'ko-', markersize=2, markeredgewidth=0)
        ax.xaxis.set_major_formatter(plot_format_mayor)

        ax.set_xlabel('Local Time')
        par_name = header_[par_index].replace('_',' ')
        ax.set_ylabel(par_name)

        name_ = header_[par_index].replace('/','-')
        fig.savefig(path_output + '/' + 'time_series_' +  name_ + '.pdf', bbox_inches='tight')
def save_all_polar_plots(header_, values_f, wd_index,par_list,name_label):

    # save_all_polar_plots(values_[:,3],[4,9,10,11,12,13,14,15,16,17],'01')

    wd_ = values_f[:,wd_index]

    for parameter_column in par_list:
        parameter_name = header_[parameter_column]
        va_ = values_f[:,parameter_column]

        # convert data to mean, 25pc, 75pc
        wd_off = np.array(wd_)
        for i,w in enumerate(wd_):
            if w > 360-11.25:
                wd_off [i] = w - 360 #offset wind such that north is correct
        # calculate statistical distribution per wind direction bin
        # wd_bin, ws_bin_mean, ws_bin_25, ws_bin_75
        table_ = np.column_stack((median_discrete(wd_off, va_, 22.5, 0, position_=.5)))
        # repeating last value to close lines
        table_ = np.row_stack((table_,table_[0,:]))

        # start figure
        fig, ax = plt.subplots(figsize=(16, 10), subplot_kw={'projection': 'polar'})
        # ax = plt.subplot(projection='polar')
        wd_rad = np.radians(table_[:,0])
        # format chart
        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        theta_angles = np.arange(0, 360, 45)
        theta_labels = ['N', 'N-E','E','S-E', 'S', 'S-W', 'W', 'N-W']
        ax.set_thetagrids(angles=theta_angles, labels=theta_labels)
        # add series
        ax.plot(wd_rad, table_[:,1], 'ko-', linewidth=3, label = 'Median')
        ax.plot(wd_rad, table_[:,2], 'b-', linewidth=3, label = '25 percentile')
        ax.plot(wd_rad, table_[:,3], 'r-', linewidth=3, label = '75 percentile')
        ax.legend(title=parameter_name, loc=(1,.75))
        name_ = parameter_name.replace('/','-')
        fig.savefig(path_output + '/' + name_label + '_WR_' + name_ + '.png', bbox_inches='tight')
def save_all_box_plots(header_, values_f, x_index,par_list,name_label):

    # save_all_box_plots(values_[:,1],[4,5,6,7,8,9,10,11,12,13,14,15,16,17],'01')
    x_val = values_f[:,x_index]

    for parameter_column in par_list:
        parameter_name = header_[parameter_column]
        y_val = values_f[:,parameter_column]

        # box x bin size
        bin_size = 1
        # combine x and y in matrix
        M_ = np.column_stack((x_val,y_val))
        # checking if always ascending to increase efficiency
        always_ascending = 1
        for x in range(x_val.shape[0]-1):
            if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
                if x_val[x+1] < x_val[x]:
                    always_ascending = 0
        if always_ascending == 0:
            M_sorted = M_[M_[:,0].argsort()] # sort by first column
            M_ = M_sorted
        # convert data to list of bins
        y_binned = []
        x_binned = []
        start_bin_edge = np.nanmin(x_val)
        last_row = 0
        last_row_temp = last_row
        while start_bin_edge <= np.nanmax(x_val):
            y_val_list = []
            for row_ in range(last_row, M_.shape[0]):
                if start_bin_edge <= M_[row_, 0] < start_bin_edge +bin_size:
                    if M_[row_, 1] == M_[row_, 1]:
                        y_val_list.append(M_[row_, 1])
                        last_row_temp = row_
                if M_[row_, 0] >= start_bin_edge +bin_size:
                    last_row_temp = row_
                    break
            x_binned.append(start_bin_edge)
            y_binned.append(y_val_list)
            start_bin_edge += bin_size
            last_row = last_row_temp
        # start figure
        fig, ax = plt.subplots(figsize=(16, 10))
        # add series
        x_binned_int = np.array(x_binned, dtype=int)
        ax.boxplot(y_binned, 0, '', whis=[5,95], positions = x_binned_int, showmeans = True)
        # ax.grid(True)
        ax.yaxis.grid()
        # add axes labels
        ax.set_xlabel('Hour of Day')
        ax.set_ylabel(parameter_name)

        # save
        name_ = parameter_name.replace('/','-')
        fig.savefig(path_output + '/' + name_label + '_DV_' + name_ + '.png', bbox_inches='tight')

def save_box_plot(filename_,x_val_index,y_val_index, new_file_label, bin_size=1,min_bin_population=10):
    print(filename_)
    # get data
    header_, values_, time_str = load_data_to_return_return(filename_)
    x_val_original = values_[:,x_val_index]
    y_val_original = values_[:,y_val_index]

    # get coincidences only
    x_val,y_val = coincidence(x_val_original,y_val_original)

    # start figure
    fig, ax = plt.subplots()#figsize=(16, 10))

    # combine x and y in matrix
    M_ = np.column_stack((x_val,y_val))
    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(x_val.shape[0]-1):
        if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
            if x_val[x+1] < x_val[x]:
                always_ascending = 0
    if always_ascending == 0:
        M_sorted = M_[M_[:,0].argsort()] # sort by first column
        M_ = M_sorted
    # convert data to list of bins
    y_binned = []
    x_binned = []
    start_bin_edge = np.nanmin(x_val)
    last_row = 0
    last_row_temp = last_row
    while start_bin_edge <= np.nanmax(x_val):
        y_val_list = []
        for row_ in range(last_row, M_.shape[0]):
            if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                if M_[row_, 1] == M_[row_, 1]:
                    y_val_list.append(M_[row_, 1])
                    last_row_temp = row_
            if M_[row_, 0] >= start_bin_edge + bin_size:
                last_row_temp = row_
                break
        x_binned.append(start_bin_edge)
        if len(y_val_list) >= min_bin_population:
            y_binned.append(y_val_list)
        else:
            y_binned.append([])
        start_bin_edge += bin_size
        last_row = last_row_temp
    if bin_size >= 1:
        x_binned_int = np.array(x_binned, dtype=int)
    else:
        x_binned_int = x_binned
    # add series
    ax.boxplot(y_binned, 0, '', whis=[5,95], positions = x_binned_int, showmeans = True, widths = bin_size * .9)
    # axes labels
    ax.set_xlabel(header_[x_val_index])
    ax.set_ylabel(header_[y_val_index])
    ######################################################
    w_day = np.array(y_binned[0])
    # w_end = np.array(y_binned[1])
    print('median')
    print(np.median(w_day))
    # print('week end median')
    # print(np.median(w_end))
    print('-'*10)
    print('mean')
    print(np.mean(w_day))
    # print('week end mean')
    # print(np.mean(w_end))
    print('-'*10)

    print('97 percentile')
    print(np.percentile(w_day,97))
    print('-'*10)


    ax.set_ylim(0,550)
    ######################################################
    #
    name_ = header_[y_val_index].replace('/','-')
    fig.savefig(path_output + '/' + new_file_label + 'custom_BX_' + name_ + '.png', bbox_inches='tight')

def save_nucleation_charts(filename_):
    output_path = filename_[:-len(filename_.replace('\\','/').split('/')[-1])]
    sheets_dict = load_nucleation_data(filename_)


    for sheet_key in sheets_dict.keys():
        A_ = np.rot90(sheets_dict[sheet_key][2], 1)
        x_ = sheets_dict[sheet_key][0] + 1000
        y_ = sheets_dict[sheet_key][1][::-1] * 1e-9

        fig, ax_ = p_arr_vectorized(A_, cbar_label='dN/dlog$_1$$_0$D [cm$^-$$^3$]', figsize_=(20,10))

        plot_format_mayor = mdates.DateFormatter('%H:%M', tz=tz_UTC)
        ax_.xaxis.set_major_formatter(plot_format_mayor)

        ax_.set_title(sheet_key)

        ax_.set_ylim((y_.min(), y_.max()))
        ax_.set_xlim((x_.min(), x_.max()))
        ax_.set_yscale("log", nonposy='clip')

        ax_.xaxis.set_ticks(np.arange(1000, 1001, 1/8))

        ax_.set_xlabel('Time')
        ax_.set_ylabel('Diameter [m]')
        ax_.grid(True)


        fig.savefig(output_path + sheet_key + '.png', transparent=True, bbox_inches='tight')


        plt.close(fig)


# animation
def update_animation_img(frame_number, img_animation, ax_, frame_list, title_list):
    p_progress_bar(frame_number, len(frame_list), extra_text='of video created')
    try:
        new_frame = frame_list[frame_number,:,:]
    except:
        new_frame = frame_list[frame_number]
    img_animation.set_data(new_frame)
    ax_.set_title(str(title_list[frame_number]))
    # ax_.set_xlabel(title_list[frame_number])
    return img_animation
def update_animation_img_pcolormesh(frame_number, img_animation, ax_, frame_list, title_list):
    p_progress(frame_number, len(frame_list), extra_text='of video created')
    try:
        new_frame = frame_list[frame_number,:,:]
    except:
        new_frame = frame_list[frame_number]
    img_animation.set_array(new_frame.ravel())
    ax_.set_title(str(title_list[frame_number]))
    return img_animation
def update_animation_img_img_list(frame_number, img_animation, ax_, frame_list, title_list):
    p_progress(frame_number, len(frame_list), extra_text='of video created')
    new_frame = frame_list[frame_number]
    img_animation.set_data(new_frame)
    ax_.set_title(str(title_list[frame_number]))
    # ax_.set_xlabel(title_list[frame_number])
    return img_animation
def update_animation_img_scatter_list(frame_number, img_plot, sca_plot, ax_img,
                                      frame_list, scatter_array_x, scatter_array_y, title_list):
    p_progress(frame_number, len(frame_list), extra_text='of video created')
    new_frame_img = frame_list[frame_number]
    new_frame_sca_x = scatter_array_x[:frame_number]
    new_frame_sca_y = scatter_array_y[:frame_number]
    img_plot.set_data(new_frame_img)
    sca_plot.set_data(new_frame_sca_x, new_frame_sca_y)
    ax_img.set_title(str(title_list[frame_number]))
    # ax_.set_xlabel(title_list[frame_number])
    return img_plot
def animate_parsivel(frame_number, t_list, size_array, speed_array, spectrum_array_color, cmap_parsivel, img_plot, ax):
    img_plot.remove()
    img_plot = ax.pcolormesh(size_array, speed_array, spectrum_array_color[frame_number, :, :],
                             cmap=cmap_parsivel, vmin=0, vmax=8)
    ax.set_title(str(t_list[frame_number]))
    return img_plot
def create_video_animation_from_csv(file_list, out_filename, colormap_, extend_='', interval_=50, dpi_=200, show_=True,
                                    save_=False, cbar_label=''):
    arr_list, max_min_tuple = create_list_of_arrays_from_file_list(file_list)

    fig, ax_ = plt.subplots()


    if extend_=='':
        img_figure = ax_.imshow(arr_list[0], interpolation='none', cmap=colormap_)
    else:
        img_figure = ax_.imshow(arr_list[0], interpolation='none', cmap=colormap_,
                        extent=[extend_[1], extend_[3], extend_[2], extend_[0]])
    color_bar = fig.colorbar(img_figure)
    color_bar.set_clim(max_min_tuple[0], max_min_tuple[1])
    color_bar.ax.set_ylabel(cbar_label)

    img_animation = FuncAnimation(fig, update_animation_img, len(arr_list), fargs=(img_figure, ax_, arr_list, file_list), interval=interval_)

    if show_: plt.show()
    if save_:
        img_animation.save(out_filename, metadata={'artist':'Guido'}, dpi=dpi_)
        plt.close(fig)
def create_video_animation_from_array_list(array_list, out_filename, colormap_=default_cm, extend_='', interval_=50,
                                           dpi_=200, show_=False, save_=True, cbar_label='', title_list=None,
                                           vmin_=None, vmax_=None):
    fig, ax_ = plt.subplots()

    if vmin_ is None:
        min_ = np.nanmin(array_list)
    else:
        min_ = vmin_

    if vmax_ is None:
        max_ = np.nanmax(array_list)
    else:
        max_ = vmax_

    if title_list is None:
        title_list_ = np.arange(len(array_list))
    else:
        title_list_ = title_list
    if extend_=='':
        img_figure = ax_.imshow(array_list[0], interpolation='none', cmap=colormap_, vmin=min_, vmax=max_)
    else:
        img_figure = ax_.imshow(array_list[0], interpolation='none', cmap=colormap_, vmin=min_, vmax=max_,
                        extent=[extend_[1], extend_[3], extend_[2], extend_[0]])
    color_bar = fig.colorbar(img_figure)
    color_bar.ax.set_ylabel(cbar_label)

    img_animation = FuncAnimation(fig, update_animation_img, len(array_list), fargs=(img_figure, ax_, array_list, title_list_), interval=interval_)

    if show_: plt.show()
    if save_:
        img_animation.save(out_filename, metadata={'artist':'Guido'}, dpi=dpi_)
        plt.close(fig)

    print('Done')
def create_video_animation_from_3D_array(array_, out_filename, colormap_=default_cm, extend_='', interval_=50, dpi_=200,
                                         show_=False, save_=True, cbar_label='', title_list=None, format_='%.2f',
                                         axes_off=False, show_colorbar=True, vmin_=None, vmax_=None):
    fig, ax_ = plt.subplots()

    if vmin_ is None: vmin_ = np.nanmin(array_)
    if vmax_ is None: vmax_ = np.nanmax(array_)

    if title_list is None or len(title_list) != array_.shape[0]:
        title_list_ = np.arange(array_.shape[0])
    else:
        title_list_ = title_list
    if extend_=='':
        img_figure = ax_.imshow(array_[0,:,:], interpolation='none', cmap=colormap_, vmin=vmin_, vmax=vmax_)
    else:
        img_figure = ax_.imshow(array_[0,:,:], interpolation='none', cmap=colormap_, vmin=vmin_, vmax=vmax_,
                                extent=[extend_[1], extend_[3], extend_[2], extend_[0]])
    if show_colorbar:
        color_bar = fig.colorbar(img_figure,format=format_)
        color_bar.ax.set_ylabel(cbar_label)

    if axes_off: ax_.set_axis_off()

    img_animation = FuncAnimation(fig, update_animation_img, array_.shape[0], fargs=(img_figure, ax_, array_, title_list_), interval=interval_)

    if show_: plt.show()
    if save_:
        # img_animation.save(out_filename, writer='ffmpeg', codec='rawvideo')
        img_animation.save(out_filename, metadata={'artist':'Guido'}, dpi=dpi_)
        plt.close(fig)

    print('Done')
def create_video_animation_from_img_arrays_list(array_list, out_filename, interval_=50, dpi_=200, show_=False,
                                                save_=True, title_list=None):
    fig, ax_ = plt.subplots()

    if title_list is None:
        title_list_ = np.arange(len(array_list))
    else:
        title_list_ = title_list
    img_figure = ax_.imshow(array_list[0], interpolation='none')

    ax_.set_axis_off()

    img_animation = FuncAnimation(fig, update_animation_img_img_list, len(array_list),
                                  fargs=(img_figure, ax_, array_list, title_list_), interval=interval_)

    if show_: plt.show()
    if save_:
        img_animation.save(out_filename, metadata={'artist':'Guido'}, dpi=dpi_)
        plt.close(fig)

    print('Done')
def create_video_animation_from_3D_array_pcolormesh(array_values, array_x, array_y, out_filename, colormap_=default_cm,
                                                    interval_=50, dpi_=200, show_=False, save_=True,
                                                    cbar_label='', title_list=None,format_='%.2f', axes_off=False,
                                                    show_colorbar=True, x_header='', y_header='',
                                                    custom_y_range_tuple=None, custom_x_range_tuple=None,
                                                    vmin_=None, vmax_=None):
    fig, ax_ = plt.subplots()

    if vmin_ is None: vmin_ = np.nanmin(array_values)
    if vmax_ is None: vmax_ = np.nanmax(array_values)

    if title_list is None or len(title_list) != array_values.shape[0]:
        title_list_ = np.arange(array_values.shape[0])
    else:
        title_list_ = title_list

    img_figure = ax_.pcolormesh(array_x, array_y, array_values[0,:,:], cmap=colormap_,
                                vmin=vmin_, vmax=vmax_)#, shading='gouraud')
    ax_.set_xlabel(x_header)
    ax_.set_ylabel(y_header)

    if custom_y_range_tuple is not None: ax_.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax_.set_xlim(custom_x_range_tuple)

    if show_colorbar:
        color_bar = fig.colorbar(img_figure,format=format_)
        color_bar.ax.set_ylabel(cbar_label)

    if axes_off: ax_.set_axis_off()


    img_animation = FuncAnimation(fig, update_animation_img_pcolormesh, frames=array_values.shape[0],
                                  fargs=(img_figure, ax_, array_values, title_list_), interval=interval_)

    if show_: plt.show()
    if save_:
        # img_animation.save(out_filename, writer='ffmpeg', codec='rawvideo')
        img_animation.save(out_filename, metadata={'artist':'Guido'}, dpi=dpi_)
        plt.close(fig)

    print('Done')


# display / plotting
def p_plot(X_series, Y_,
           S_=5, c_='', label_=None, zorder_=None,
           x_header=None, y_header=None, t_line=False, grid_=False, cus_loc =None, cmap_='jet',
           custom_y_range_tuple=None, custom_x_range_tuple=None, figsize_ = (10,6), save_fig=False, figure_filename='',
           custom_x_ticks_start_end_step=None, custom_y_ticks_start_end_step=None, extra_text='', title_str = '',
           time_format_=None, x_as_time=True, c_header=None, add_line=False, linewidth_=2, fig_ax=None,
           line_color='black', invert_y=False, invert_x=False, log_x=False, log_y=False, transparent_=True,
           density_=False, t_line_1_1 = True, t_line_color = 'r', fit_function=None, show_cbar=False, cbar_ax=None,
           text_box_str=None, text_box_loc=None, skewt=False, filled_arr=None, linestyle_='-', alpha_=1,
           legend_show=False, legend_loc='upper left', marker_=None, marker_lw=0, rasterized_=False,
           font_size_axes_labels=14, font_size_title=16, font_size_legend=12, font_size_ticks=10, cbar_format='%.2f',
           t_line_text_color='black', vmin_=None, vmax_=None, y_ticks_on_right_side=False, cbar_orient='vertical',
           colorbar_tick_labels_list=None, add_coastlines=False, coastline_color='black',
           y_err_arr=None, y_err_color='k', fit_function_p0=None, cbar_number_of_colors=None,
           colorbar_extend='neither'):
    """
    creates plot
    :param X_series: 1D array with values of x axis
    :param Y_: 1D array (same size as X_) with values of y axis
    :param S_: 1D array (same size as X_) of integer or single integer with pixel size of marker
    :param c_: color of marker of line, can be a 1D array (same size as X_) of floats or strs, or a single string
    :param label_: string used to identify series in the legend
    :param zorder_: integer that defines the order in which series appear, larger numbers are on top of smaller
    :param x_header: string to be used as a label of the x axis
    :param y_header: string to be used as a label of the y axis
    :param t_line: if true a trend line will be added to the plot using a default linear function (see fit_function)
    :param grid_: if true grid lines will be added
    :param cus_loc: tuple with the x and y values for a custom location of the trend line fit text
    :param cmap_: color map to be used in the case that c_ is defined as a 1D array of floats (or integers)
    :param custom_y_range_tuple: tuple is the min and max y values to be displayed
    :param custom_x_range_tuple: tuple is the min and max x values to be displayed
    :param figsize_: tuple with the figure size in inches (horizontal inches, vertical inches)
    :param save_fig: if true the figure will be saved to path_output, unless figure_filename is defined
    :param figure_filename: if given, the figure will be saved to the given filename and closed
    :param custom_x_ticks_start_end_step: tuple with numbers for start, end, and step size for the x axis ticks
    :param custom_y_ticks_start_end_step: tuple with numbers for start, end, and step size for the y axis ticks
    :param extra_text: string that can be added to the fitted parameters text
    :param title_str: string that will be added to the top of the figure if defined
    :param time_format_: if provided, the x axis values will be tried to convert to days since 01-01-1970_00:00 and formated as defined
    :param x_as_time: if true, the x axis values will be tried to convert to days since 01-01-1970_00:00 and formated as time_format_ or as '%Y-%m-%d_%H:%M:%S'
    :param c_header: string used as label in the color bar
    :param add_line: if true a line connecting the markers will be added using line_color as its color
    :param linewidth_: width of the line connecting the markers, assuming add_line=True
    :param fig_ax: tuple with the figure and axis object to be used. If not provided a new figure and axis is created
    :param line_color: if provided it is used to color the line connecting the markers, assuming add_line=True
    :param invert_y: if true the y axis is inverted (max on the bottom, min on the top)
    :param invert_x: if true the x axis is inverted (max on the left, min on the right)
    :param log_x: if true the x axis is log scaled
    :param log_y: if true the y axis is log scaled
    :param transparent_: if true the figure to be saved is set to have transparent background
    :param density_: if true a shaded color is added to a scatter plot that shows where most poinst are located
    :param t_line_1_1: if true, a 1:1 dashed diagonal line is added to the figure (good for showing 1:1 correlations)
    :param t_line_color: color of the trendline, assuming t_line=True
    :param fit_function: the name of the function to be fitted, if None, then a linear function is used as default
    :param show_cbar: if true the color bar is used when needed (if c_ is an array of numbers)
    :param cbar_ax: if provided, the colorbar will be placed inside this axis instead of created to the right of the current axis
    :param text_box_str: string of text to add, uses text_box_loc to place it
    :param text_box_loc: tuple to define the location of text_box_str, if not provided will be placed in top left corner
    :param skewt: if true it will plot the figure as a meteorological skew temperature plot (not recommended, better to use p_plot_SkewT...)
    :param filled_arr: 1D array, will be used as bounds coupled with Y_ to fill within, good for showing uncertainty
    :param linestyle_: string that defines the type of line used if add_line=True (solid, dotted, dashed, dashdot)
    :param alpha_: float (0-1) to define the transparency of the markers, or lines. 0 is fully transparent, 1 is fully opaque
    :param legend_show: if true the legend is shown with any labels found
    :param legend_loc: str or pair of floats (x,y), can be 'upper left', 'upper right', 'lower left', 'lower right', 'center, 'best'
    :param marker_: defines the type of marker, default is circle, see https://matplotlib.org/stable/api/markers_api.html
    :param marker_lw: defines the size of the marker's line
    :param rasterized_: if true the figure is rasterized which can reduce the size and rendering if saved as a pdf
    :param font_size_axes_labels: number to define the font size of the axels labels
    :param font_size_title: number to define the font size of the title
    :param font_size_legend: number to define the font size of the legend text
    :param font_size_ticks: number to define the font size of the axels ticks
    :param cbar_format: the format of the numbers in the color bar, '%.2f' will show 2 decimals
    :param t_line_text_color: color of the text produced by the fitting
    :param vmin_: used to define the range of the colorbar, float with the minimum value to be shown in the colorbar
    :param vmax_: used to define the range of the colorbar, float with the maximum value to be shown in the colorbar
    :param y_ticks_on_right_side: if true the tick marks and label of the y axis are moved to the right
    :param cbar_orient: can be 'horizontal' or 'vertical'. default vertical
    :param colorbar_tick_labels_list: if provided, it will be used as tickmars for the colorbar
    :param add_coastlines: if true, coastlines will be added using the local topographical files (global or access)
    :param coastline_color: color of the coastline, string
    :param y_err_arr: 1D array with error values for errorbars. If not none, error bars will be added
    :param y_err_color: color to be used for the error bars, default is black
    :param fit_function_p0: list with initial guess of fitting variables to be pased to curve_fit
    :param cbar_number_of_colors: int with the number of colors to be used, if none, a continuous color bar is used
    :param colorbar_extend: string to specify the extend (range) of the colorbar, accepts neither, both, min, or max
    :return: matplotlib figure object, matplotlib axis object, R2 in case a fitting is done otherwise none
    """
    change_font_size_figures(font_size_axes_labels, font_size_title, font_size_legend, font_size_ticks)

    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        if skewt:
            fig = plt.figure(figsize=figsize_)
            ax = fig.add_subplot(111, projection='skewx')
        else:
            fig, ax = plt.subplots(figsize=figsize_)



    x_is_time_cofirmed = True
    if x_as_time==True and density_==False and invert_x==False and log_x==False:
        if time_format_ is None:
            time_format_ = time_format_mod
        X_ = convert_any_time_type_to_days(X_series)
        if X_ is None:
            X_ = X_series
            x_is_time_cofirmed = False
    else:
        X_ = X_series
        x_is_time_cofirmed = False

    if type(cmap_) == str:
        cmap_ = cm.get_cmap(cmap_, cbar_number_of_colors)

    if skewt:
        # Plot the data using normal plotting functions, in this case using
        # log scaling in Y, as dictated by the typical meteorological plot
        if c_ == '': c_ = 'black'
        ax.semilogy(X_, Y_, color=c_)

        # Disables the log-formatting that comes with semilogy
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set_yticks(np.linspace(100, 1000, 10))
        ax.set_ylim(1050, 100)

        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.set_xlim(-50, 50)
        x_as_time = False
        ax.grid(True)
    else:
        if density_:
            ax = p_density_scatter(X_, Y_, s = S_, fig_ax=[fig, ax], cmap_=cmap_,
                                   show_cbar=show_cbar, rasterized_=rasterized_)
        else:

            if type(c_) == str:
                if c_ == '':
                    if add_line:
                        ax.scatter(X_, Y_, s=S_, lw=marker_lw, c='black', marker=marker_, zorder=zorder_, alpha=alpha_)
                        ax.plot(X_, Y_, c=line_color, linewidth=linewidth_, label=label_, zorder=zorder_,
                                linestyle=linestyle_)
                        if y_err_arr is not None:
                            ax.errorbar(X_, Y_, yerr=y_err_arr, color=y_err_color)
                        if filled_arr is not None:
                            ax.fill_between(X_, Y_, filled_arr, facecolor=line_color, interpolate=True, alpha=alpha_)
                    else:
                        trajs_ = ax.scatter(X_, Y_, s=S_, lw=marker_lw, c='black',
                                            label=label_, marker=marker_, zorder=zorder_, alpha=alpha_)
                        if y_err_arr is not None:
                            ax.errorbar(X_, Y_, yerr=y_err_arr, color=y_err_color)
                        trajs_.set_rasterized(rasterized_)
                else:
                    if add_line:
                        ax.plot(X_, Y_, c=c_, linewidth=linewidth_, label=label_, zorder=zorder_,
                                linestyle=linestyle_)
                        trajs_ = ax.scatter(X_, Y_, s=S_, lw=marker_lw, c=c_, marker=marker_, zorder=zorder_, alpha=alpha_)
                        trajs_.set_rasterized(rasterized_)
                        if y_err_arr is not None:
                            ax.errorbar(X_, Y_, yerr=y_err_arr, color=y_err_color)
                        if filled_arr is not None:
                            ax.fill_between(X_, Y_, filled_arr, facecolor=line_color, interpolate=True, alpha=alpha_)
                    else:
                        trajs_ = ax.scatter(X_, Y_, s=S_, lw=marker_lw, c=c_, label=label_,
                                            marker=marker_, zorder=zorder_, alpha=alpha_)
                        if y_err_arr is not None:
                            ax.errorbar(X_, Y_, yerr=y_err_arr, color=y_err_color)
                        trajs_.set_rasterized(rasterized_)
                        if add_line:
                            ax.plot(X_, Y_, c=c_, linewidth=linewidth_, label=label_, zorder=zorder_,
                                    linestyle=linestyle_)

                            if filled_arr is not None:
                                ax.fill_between(X_, Y_, filled_arr, facecolor=c_, interpolate=True, alpha=alpha_)
            else:
                if vmin_ is None: vmin_ = np.nanmin(c_)
                if vmax_ is None: vmax_ = np.nanmax(c_)
                im = ax.scatter(X_, Y_, s=S_, lw=marker_lw,  c=c_, cmap=cmap_,
                                marker=marker_, zorder=zorder_, vmin=vmin_, vmax=vmax_, alpha=alpha_)

                if x_is_time_cofirmed:
                    plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
                    ax.format_coord = lambda x, y: 'x=%s, y=%g, v=%g' % (plot_format_mayor(x), y,
                                                                         c_[np.nanargmin((Y_ - y)**2 + (X_ - x)**2)])
                else:
                    ax.format_coord = lambda x, y: 'x=%g, y=%g, v=%g' % (x, y,
                                                                         c_[np.nanargmin((Y_ - y)**2 + (X_ - x)**2)])

                if y_err_arr is not None:
                    ax.errorbar(X_, Y_, yerr=y_err_arr, color=y_err_color)
                im.set_rasterized(rasterized_)
                if show_cbar:
                    if cbar_ax is None:
                        color_bar = fig.colorbar(im, format=cbar_format,
                                                 orientation=cbar_orient, extend=colorbar_extend)
                    else:
                        color_bar = fig.colorbar(im, format=cbar_format, cax=cbar_ax,
                                                 orientation=cbar_orient, extend=colorbar_extend)
                    if c_header is not None:
                        if cbar_orient == 'vertical':
                            color_bar.ax.set_ylabel(c_header)
                        elif cbar_orient == 'horizontal':
                            color_bar.ax.set_xlabel(c_header)
                    if colorbar_tick_labels_list is not None:
                        ticks_ = np.linspace(0.5, len(colorbar_tick_labels_list) - 0.5, len(colorbar_tick_labels_list))
                        color_bar.set_ticks(ticks_)
                        color_bar.set_ticklabels(colorbar_tick_labels_list)

    if x_header is not None: ax.set_xlabel(x_header)
    if y_header is not None: ax.set_ylabel(y_header)
    # ax.yaxis.set_ticks(np.arange(180, 541, 45))
    if grid_:
        ax.grid(True)
    if t_line:
        Rsqr = plot_trend_line(ax, X_, Y_, c=t_line_color, alpha=1, cus_loc = cus_loc, text_color=t_line_text_color,
                               extra_text=extra_text, t_line_1_1= t_line_1_1,
                               fit_function=fit_function, fit_function_p0=fit_function_p0)
    else:
        Rsqr = None

    if invert_y:
        ax.invert_yaxis()
    if invert_x:
        ax.invert_xaxis()
    if log_x:
        ax.set_xscale("log")#, nonposy='clip')
    if log_y:
        ax.set_yscale("log")#, nonposy='clip')


    if custom_x_ticks_start_end_step is not None:
        ax.xaxis.set_ticks(np.arange(custom_x_ticks_start_end_step[0], custom_x_ticks_start_end_step[1],
                                     custom_x_ticks_start_end_step[2]))
    if custom_y_ticks_start_end_step is not None:
        ax.yaxis.set_ticks(np.arange(custom_y_ticks_start_end_step[0], custom_y_ticks_start_end_step[1],
                                     custom_y_ticks_start_end_step[2]))

    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None:
        if x_as_time == True and density_ == False and invert_x == False and log_x == False and x_is_time_cofirmed == True:
            r_1 = convert_any_time_type_to_days(custom_x_range_tuple[0])
            r_2 = convert_any_time_type_to_days(custom_x_range_tuple[1])
            ax.set_xlim((r_1,r_2))
        else:
            ax.set_xlim(custom_x_range_tuple)


    if x_as_time==True and density_==False and invert_x==False and log_x==False and x_is_time_cofirmed==True:

        if time_format_ is None:
            plot_format_mayor = mdates.DateFormatter(time_format_mod, tz=tz_UTC)
        else:
            plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)
    else:
        ax.ticklabel_format(useOffset=False)

    if legend_show:
        ax.legend(loc=legend_loc)
    ax.set_title(title_str)

    if y_ticks_on_right_side:
        y_axis_labels_and_ticks_to_right(ax)

    if text_box_str is not None:
        if text_box_loc is None:
            x_1 = ax.axis()[0]
            y_2 = ax.axis()[3]

            text_color = 'black'
            ax.text(x_1, y_2 , str(text_box_str),
                           horizontalalignment='left',verticalalignment='top',color=text_color)
        else:
            x_1 = text_box_loc[0]
            y_2 = text_box_loc[1]
            text_color = 'black'
            ax.text(x_1, y_2 , str(text_box_str),
                           horizontalalignment='left',verticalalignment='top',color=text_color)

    if add_coastlines:
        add_coastline_to_ax(ax, coastline_color=coastline_color)

    if save_fig or figure_filename != '':
        if figure_filename == '':
            name_ = str(calendar.timegm(time.gmtime()))[:-2]
            fig.savefig(path_output + 'image_' + name_ + '.png', transparent=True, bbox_inches='tight')
        else:
            fig.savefig(figure_filename, transparent=transparent_, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

    return fig, ax, Rsqr
def p_plot_arr(array_v, array_x, array_y,
               custom_y_range_tuple=None, custom_x_range_tuple=None,
               custom_ticks_x=None, custom_ticks_y=None, x_header=None, y_header=None, title_str=None,
               show_cbar=True, cbar_format='%.2f', cbar_label = '', cbar_ax=None, cbar_orient='vertical',
               contour_=False, contourF_=False,cmap_=default_cm, figsize_= (10,6),
               vmin_=None, vmax_=None, figure_filename = None, grid_=False, time_format_ = None, fig_ax=None,
               colorbar_tick_labels_list=None, show_x_ticks=True, show_y_ticks=True,extend_='neither',
               invert_y=False, invert_x=False, levels=None, text_box_str=None,text_box_loc=None,
               font_size_axes_labels=14, font_size_title=16, font_size_legend=12, font_size_ticks=10,
               add_coastlines=False, coastline_color='black', zorder_=None, cbar_number_of_colors=None):
    """
    plots an array in vector form (not imshow)
    :param array_v: 2d array with values to be shown as colors
    :param array_x: 1d or 2d array with the x axes values
    :param array_y: 1d or 2d array with the y axes values
    :param custom_y_range_tuple: tuple with min and max y values to be shown in figure, this is just for display
    :param custom_x_range_tuple: tuple with min and max x values to be shown in figure, this is just for display
    :param custom_ticks_x: list/array with the ticks for the x axes
    :param custom_ticks_y: list/array with the ticks for the y axes
    :param x_header: str with the desired x header
    :param y_header: str with the desired y header
    :param cbar_label: str with the desired color bar label
    :param cbar_orient: str with the desired color bar orientation
    :param title_str: str with title of figure
    :param contour_: If true, the figure will be of countours, else it will be a pcolormesh
    :param contourF_: If true, the figure will be of filled countours, else it will be a pcolormesh
    :param cmap_: matplotlib object colormap
    :param figsize_: tuple with the size of the figure in inches (x, y)
    :param vmin_: minimum frequency to be displayed in the figure (sets the range of the colorbar)
    :param vmax_: maximum frequency to be displayed in the figure (sets the range of the colorbar)
    :param show_cbar: If true the cbar is shown.
    :param cbar_format: the str format for the ticks of the colorbar, if only integers wanted set to '%i'
    :param figure_filename: If set to a str with a path and filename, the figure will be saved and closed
    :param grid_: if true, the grid will be shown
    :param time_format_: str in a format like '%d-%m-%Y_%H:%M'. if not none, the array_x will be attempted to convert
                            to a datetime series and if posible the tick values will be formated following this str
    :param fig_ax: tuple with a figure and axes object from matplotlib. use this if you already have a figure and want
                    to add a CFAD to it, or for multiple panels
    :param colorbar_tick_labels_list: in case specific labels are wanted (like str showing ice, rain, SLW, hail)
    :param show_x_ticks: if true the ticks for the x axes will be shown
    :param show_y_ticks: if true the ticks for the y axes will be shown
    :param cbar_ax: axes object from matplotlib where the colorbar will be placed, usefull when multiple CFADs are in
                    the same figure and share one colorbar.
    :param invert_y: if true the y axes will be inversed in the display, usefull for CFTDs (by temperature)
    :param invert_x: if true the x axes will be inversed in the display, usefull for CFTDs (by temperature)
    :param levels: list/array with the ticks for the colorbar
    :param text_box_str: str text to be shown in the figure
    :param text_box_loc: location in x and y values to place the above text box
    :param font_size_axes_labels: size of font of axes labels in graph
    :param font_size_title: size of font of title in graph
    :param font_size_legend: size of font of legend in graph
    :param font_size_ticks: size of font of ticks in graph
    :param extend_: {'neither', 'both', 'min', 'max'}
    :param add_coastlines: if true adds coastlines (creates a map).
    :param coastline_color: color of the coastline.
    :param zorder_: integer that defines the order in which objects appear, larger numbers are on top of smaller
    :param cbar_number_of_colors: int with the number of colors to be used, if none, a continuous color bar is used
    :return:
        fig: figure objects
        ax: axes objects
        surface: the point collection from matplotlib
    """


    change_font_size_figures(font_size_axes_labels, font_size_title, font_size_legend, font_size_ticks)
    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)


    if vmin_ is None: vmin_ = np.nanmin(array_v)
    if vmax_ is None: vmax_ = np.nanmax(array_v)

    # make axis arrays 2D if needed
    if len(array_x.shape) == 1:
        array_x_reshaped = np.zeros(array_v.shape, dtype=float)
        for r_ in range(array_v.shape[0]):
            array_x_reshaped[r_, :] = array_x
    else:
        array_x_reshaped = array_x
    array_x = array_x_reshaped

    if len(array_y.shape) == 1:
        array_y_reshaped = np.zeros(array_v.shape, dtype=float)
        for c_ in range(array_v.shape[1]):
            array_y_reshaped[:, c_] = array_y
    else:
        array_y_reshaped = array_y
    array_y = array_y_reshaped

    if time_format_ is not None:
        array_x = convert_any_time_type_to_days(array_x_reshaped)

    if type(cmap_) == str:
        cmap_ = cm.get_cmap(cmap_, cbar_number_of_colors)

    if contour_:
        surf_ = ax.contour(array_x, array_y, array_v, levels=levels, cmap=cmap_,
                           vmin=vmin_, vmax=vmax_,
                           extend=extend_, zorder=zorder_)
    elif contourF_:
        surf_ = ax.contourf(array_x, array_y, array_v, levels=levels, cmap=cmap_,
                            vmin=vmin_, vmax=vmax_,
                            extend=extend_, zorder=zorder_)
    else:
        surf_ = ax.pcolormesh(array_x, array_y, array_v, cmap=cmap_,
                              vmin=vmin_, vmax=vmax_, zorder=zorder_)

    if show_cbar:
        if cbar_ax is None:
            color_bar = fig.colorbar(surf_, format=cbar_format, orientation=cbar_orient, extend=extend_)
        else:
            color_bar = fig.colorbar(surf_, format=cbar_format, cax=cbar_ax, orientation=cbar_orient, extend=extend_)
        if cbar_orient == 'vertical':
            color_bar.ax.set_ylabel(cbar_label)
        elif cbar_orient == 'horizontal':
            color_bar.ax.set_xlabel(cbar_label)
        else:
            print('Error! color bar orientation not understood. Please select vertical or horizontal')

        if colorbar_tick_labels_list is not None:
            ticks_ = np.linspace(0.5, len(colorbar_tick_labels_list) - 0.5, len(colorbar_tick_labels_list))
            try:
                color_bar.set_ticks(ticks_, extend=extend_)
                color_bar.set_ticklabels(colorbar_tick_labels_list, extend=extend_)
            except:
                color_bar.set_ticks(ticks_)
                color_bar.set_ticklabels(colorbar_tick_labels_list)

    if x_header is not None: ax.set_xlabel(x_header)
    if y_header is not None: ax.set_ylabel(y_header)
    if title_str is not None: ax.set_title(title_str)
    ax.grid(grid_)


    if time_format_ is not None:
        plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)
        ax.format_coord = lambda x, y: 'x=%s, y=%g, v=%g' % (plot_format_mayor(x),
                                                             y,
                                                             array_v[int(np.nanargmin(np.abs(array_y[:, 0] - y))),
                                                                     int(np.nanargmin(np.abs(array_x[0, :] - x)))])
    else:
        ax.ticklabel_format(useOffset=False)
        ax.format_coord = lambda x, y: 'x=%g, y=%g, v=%g' % (x,
                                                             y,
                                                             array_v[int(np.nanargmin(np.abs(array_y[:, 0] - y))),
                                                                     int(np.nanargmin(np.abs(array_x[0, :] - x)))])

    if not show_x_ticks:
        plt.setp(ax.get_xticklabels(), visible=False)
    if not show_y_ticks:
        plt.setp(ax.get_yticklabels(), visible=False)


    if invert_y:
        ax.invert_yaxis()
    if invert_x:
        ax.invert_xaxis()



    if text_box_str is not None:
        if text_box_loc is None:
            x_1 = ax.axis()[0]
            y_2 = ax.axis()[3]

            text_color = 'black'
            ax.text(x_1, y_2 , str(text_box_str),
                           horizontalalignment='left',verticalalignment='top',color=text_color)
        else:
            x_1 = text_box_loc[0]
            y_2 = text_box_loc[1]
            text_color = 'black'
            ax.text(x_1, y_2 , str(text_box_str),
                           horizontalalignment='left',verticalalignment='top',color=text_color)

    if add_coastlines:
        add_coastline_to_ax(ax, coastline_color=coastline_color)

    if custom_ticks_x is not None: ax.xaxis.set_ticks(custom_ticks_x)
    if custom_ticks_y is not None: ax.yaxis.set_ticks(custom_ticks_y)
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)

    if figure_filename is not None:
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
        return

    return fig, ax, surf_
def change_font_size_figures(font_size_axes_labels, font_size_title, font_size_legend, font_size_ticks):
    params = {'axes.labelsize': font_size_axes_labels,
              'axes.titlesize': font_size_title,
              'legend.fontsize': font_size_legend,
              'xtick.labelsize': font_size_ticks,
              'ytick.labelsize': font_size_ticks}
    matplotlib.rcParams.update(params)
def create_fig_ax(nrows=1, ncols=1, figsize=(10, 6), sharex=False, sharey=False,
                  width_ratios=None, height_ratios=None):
    fig, (ax_list) = plt.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, figsize=figsize,
                                  gridspec_kw={'width_ratios': width_ratios, 'height_ratios': height_ratios})
    return fig, ax_list
def create_ax(fig, x_start, y_start, x_width, y_width):
    ax = fig.add_axes([x_start, y_start, x_width, y_width])
    return ax
def add_text_to_ax(ax, x, y, text_, fontsize=10, ha='center', va='bottom', rotation=0, color='black',
                   facecolor='white', edgecolor='white', zorder=None):
    ax.text(x, y, text_, fontsize=fontsize, zorder=zorder,
            ha=ha, va=va, rotation=rotation, color=color, bbox={'facecolor': facecolor, 'edgecolor': edgecolor})
def add_text_to_fig(fig, x, y, text_,fontsize=10, ha='center', va='bottom', rotation=0, color='black',
                    facecolor='white', edgecolor='white'):
    fig.text(x, y, text_, fontsize=fontsize,
            ha=ha, va=va, rotation=rotation, color=color, bbox={'facecolor': facecolor, 'edgecolor': edgecolor})
def get_fig_size(fig):
    return fig.get_size_inches()
def twin_ax_x(ax):
    return ax.twinx()
def twin_ax_y(ax):
    return ax.twiny()
def add_vertical_line_to_ax(ax, x_position,  color='k', linestyle='--'):
    ax.axvline(x_position, color=color, linestyle=linestyle)
def add_horizontal_line_to_ax(ax, y_position,  color='k', linestyle='--'):
    ax.axhline(y_position, color=color, linestyle=linestyle)
def close_fig(fig):
    plt.close(fig)
def ticks_remove_x(ax):
    try:
        shape_ = ax.shape
        for ax_ in ax.flatten():
            plt.setp(ax_.get_xticklabels(), visible=False)
    except:
        try:
            len_ = len(ax)
            for ax_ in ax:
                plt.setp(ax_.get_xticklabels(), visible=False)
        except:
            plt.setp(ax.get_xticklabels(), visible=False)
def ticks_remove_y(ax):
    try:
        shape_ = ax.shape
        for ax_ in ax.flatten():
            plt.setp(ax_.get_yticklabels(), visible=False)
    except:
        try:
            len_ = len(ax)
            for ax_ in ax:
                plt.setp(ax_.get_yticklabels(), visible=False)
        except:
            plt.setp(ax.get_yticklabels(), visible=False)
def remove_ax(ax):
    try:
        shape_ = ax.shape
        for ax_ in ax.flatten():
            ax_.remove()
    except:
        try:
            len_ = len(ax)
            for ax_ in ax:
                ax_.remove()
        except:
            ax.remove()
def save_fig(fig, filename_, transparent=False, bbox_inches=None, dpi=200):
    fig.savefig(filename_, transparent=transparent, bbox_inches=bbox_inches, dpi=dpi)
def fig_adjust(fig, left=.08, right=.96, bottom=.1, top=.97, hspace=.01, wspace=.01):
    fig.subplots_adjust(left=left, right=right, bottom=bottom, top=top, hspace=hspace, wspace=wspace)
def add_colorbar_to_ax(fig, ax, plot_image_or_scatter, format='%.2f', orientation='vertical'):
    """
    adds a colorbar object to an axis
    :param fig: matplotlib figure object
    :param ax: matplotlib axes object
    :param plot_image_or_scatter:
    :param format:
    :param orientation: string, either vertical or horizontal
    :return: colorbar object
    """
    cbar_ = fig.colorbar(plot_image_or_scatter, cax=ax, format=format, orientation=orientation)
    return cbar_
def add_countour_to_ax(ax, x_, y_, arr_, countour_lines_values_list,
                       color_list=None, style_list=None, labels_=False,
                       labels_font_size=8, filled_=False, zorder_=None, line_width=1):
    x_1, x_2, y_1, y_2 = get_ax_range(ax)

    if filled_:
        contours = ax.contourf(x_, y_, arr_, countour_lines_values_list, colors=color_list,
                               linestyles=style_list,zorder=zorder_)
    else:
        contours = ax.contour(x_, y_, arr_,countour_lines_values_list, colors=color_list,
                              linestyles=style_list, zorder=zorder_, lw=line_width)
    if labels_:
        plt.rc('font', size=labels_font_size)  # controls default text sizes
        ax.clabel(contours, contours.levels, inline=True, fmt='%i')

    ax.set_xlim((x_1, x_2))
    ax.set_ylim((y_1, y_2))
    return contours
def add_coastline_aus(ax, color='black', line_width=1):
    if not aus_coastline_loaded: load_aus_coastline()
    ax.plot(aus_coast_lon, aus_coast_lat, color, lw=line_width)
def add_coastline_glob(ax, color='black', line_width=1):
    if not glob_coastline_loaded: load_global_coastline()
    ax.plot(glob_coast_lon, glob_coast_lat, color, lw=line_width)
def add_coastline_to_ax(ax, coastline_color='yellow', filled_=False,
                        filled_ocean_color='aqua', filled_land_color='saddlebrown', line_width=1):
    x_1, x_2, y_1, y_2 = get_ax_range(ax)
    x_1 -= 1
    x_2 += 1
    y_1 -= 1
    y_2 += 1

    if filled_:

        if x_1 > 110 and x_2 < 156 and y_1 > -44 and y_2 < -10:
            if not aus_topo_loaded: load_aus_topo()
            row_2 = time_to_row_sec(highres_lat, y_1)
            row_1 = time_to_row_sec(highres_lat, y_2)
            col_1 = time_to_row_sec(highres_lon, x_1)
            col_2 = time_to_row_sec(highres_lon, x_2)
            add_countour_to_ax(ax, highres_lon[col_1:col_2], highres_lat[row_1:row_2],
                               highres_topo[row_1:row_2, col_1:col_2],
                               [-99999, 0, 9999], [filled_ocean_color, filled_land_color, filled_land_color],
                               filled_=True, zorder_=0, line_width=line_width)
        else:
            if not glob_topo_loaded: load_glob_topo()
            row_1 = time_to_row_sec(topo_lat, y_1)
            row_2 = time_to_row_sec(topo_lat, y_2)
            col_1 = time_to_row_sec(topo_lon, x_1)
            col_2 = time_to_row_sec(topo_lon, x_2)
            add_countour_to_ax(ax, topo_lon[col_1:col_2], topo_lat[row_1:row_2],
                               topo_arr[row_1:row_2, col_1:col_2],
                               [-99999, 0, 9999], [filled_ocean_color, filled_land_color, filled_land_color],
                               filled_=True, zorder_=0, line_width=line_width)
    else:
        if x_1 > 100 and x_2 < 170 and y_1 > -50 and y_2 < -3:
            x_1, x_2, y_1, y_2 = get_ax_range(ax)
            add_coastline_aus(ax, color=coastline_color, line_width=line_width)
            ax.set_xlim(x_1, x_2)
            ax.set_ylim(y_1, y_2)
        else:
            x_1, x_2, y_1, y_2 = get_ax_range(ax)
            add_coastline_glob(ax, color=coastline_color, line_width=line_width)
            ax.set_xlim(x_1, x_2)
            ax.set_ylim(y_1, y_2)


def format_xaxis_ticks(ax, format_='%.2f'):
    ax.xaxis.set_major_formatter(FormatStrFormatter(format_))
def format_yaxis_ticks(ax, format_='%.2f'):
    ax.yaxis.set_major_formatter(FormatStrFormatter(format_))
def y_axis_labels_and_ticks_to_right(ax):
    try:
        shape_ = ax.shape
        for ax_ in ax.flatten():
            ax_.yaxis.tick_right()
            ax_.yaxis.set_label_position("right")
    except:
        try:
            len_ = len(ax)
            for ax_ in ax:
                ax_.yaxis.tick_right()
                ax_.yaxis.set_label_position("right")
        except:
            ax.yaxis.tick_right()
            ax.yaxis.set_label_position("right")
def x_axis_labels_and_ticks_to_top(ax):
    try:
        shape_ = ax.shape
        for ax_ in ax.flatten():
            ax_.xaxis.tick_top()
            ax_.xaxis.set_label_position("top")
    except:
        try:
            len_ = len(ax)
            for ax_ in ax:
                ax_.xaxis.tick_top()
                ax_.xaxis.set_label_position("top")
        except:
            ax.xaxis.tick_top()
            ax.xaxis.set_label_position("top")
def custom_legend(color_list, labels_list, ax, loc='lower left', ncol=1, mode="expand", borderaxespad=0.,
                  bbox_to_anchor=None, alpha=0.7, background_color='white'):
    patch_list = []
    for color_, label_ in zip(color_list, labels_list):
        patch_list.append(mpatches.Patch(color=color_, label=label_))
    ax.legend(handles=patch_list, bbox_to_anchor=bbox_to_anchor,
              loc=loc, ncol=ncol, mode=mode, borderaxespad=borderaxespad, framealpha=alpha, facecolor=background_color)
def change_ax_position(ax, x_start, y_start, x_width, y_width):
    ax.set_position([x_start, y_start, x_width, y_width])
def get_ax_position(ax):
    return ax.get_position()
def get_current_fig_axs():
    fig = plt.gcf()
    axs = fig.axes
    return fig, axs
def share_axes_range(ax_list, x_axis=True, y_axis=True):
    """
    Adjusts the shared x and/or y axis limits for a list of matplotlib axes.

    Parameters:
        ax_list (list of matplotlib.axes.Axes): A list of axes objects to modify.
        x_axis (bool, optional): Whether to adjust the x-axis limits. Defaults to True.
        y_axis (bool, optional): Whether to adjust the y-axis limits. Defaults to True.

    Notes:
        - The function computes the minimum and maximum values across all axes in `ax_list`.
        - If `x_axis` is True, it sets the x-axis limits to the computed minimum and maximum.
        - If `y_axis` is True, it sets the y-axis limits to the computed minimum and maximum.

    Example:
        import matplotlib.pyplot as plt

        # Create some sample axes
        fig, axs = plt.subplots(2, 2)
        ax1, ax2, ax3, ax4 = axs.flatten()

        # Call the function to share x-axis limits
        share_axes_range([ax1, ax2], x_axis=True, y_axis=False)

        # Call the function to share y-axis limits
        share_axes_range([ax3, ax4], x_axis=False, y_axis=True)

    """
    x_1_list = []
    x_2_list = []
    y_1_list = []
    y_2_list = []

    for ax_ in ax_list:
        x_1, x_2, y_1, y_2 = get_ax_range(ax_)
        x_1_list.append(x_1)
        x_2_list.append(x_2)
        y_1_list.append(y_1)
        y_2_list.append(y_2)

    x_min = np.min(x_1_list)
    x_max = np.max(x_2_list)
    y_min = np.min(y_1_list)
    y_max = np.max(y_2_list)

    for ax_ in ax_list:
        if x_axis:
            ax_.set_xlim((x_min, x_max))
        if y_axis:
            ax_.set_ylim((y_min, y_max))
def color_y_axis(ax, color):
    """Color your axes."""
    for t in ax.get_yticklabels():
        t.set_color(color)
    return None
def get_chart_range(ax):
    x_1 = ax.axis()[0]
    x_2 = ax.axis()[1]
    y_1 = ax.axis()[2]
    y_2 = ax.axis()[3]
    return x_1,x_2,y_1,y_2
def set_chart_range(ax_, x_range_tuple, y_range_tuple):
    if x_range_tuple is not None:
        ax_.set_xlim(x_range_tuple)
    if y_range_tuple is not None:
        ax_.set_ylim(y_range_tuple)
def ax_range_equal_x_y(ax_, pad_=0):
    x_1, x_2, y_1, y_2 = get_chart_range(ax_)
    d_x = x_2 - x_1
    d_y = y_2 - y_1
    d_max = np.max([d_x, d_y])
    x_1 = np.mean([x_1, x_2]) - d_max / 2 - pad_
    x_2 = np.mean([x_1, x_2]) + d_max / 2 + pad_
    y_1 = np.mean([y_1, y_2]) - d_max / 2 - pad_
    y_2 = np.mean([y_1, y_2]) + d_max / 2 + pad_
    ax_.set_xlim((x_1 - pad_, x_2 + pad_))
    ax_.set_ylim((y_1 - pad_, y_2 + pad_))

def plot_precip_cumulative_colored(time_secs, precip_rate, precip_type_NWS, time_step_secs=3600,
                                   x_header='Time', y_header='mm', fig_ax=None, figsize_=(10,6), x_not_time=False,
                                   time_format_=time_format, color_list=listed_cm_colors_list[1:], zorder_=5,
                                   restart_point_list=None, custom_y_range_tuple=None, custom_x_range_tuple=None,
                                   number_ticks_x=6, legend_loc='upper left', title_str='', legend_show=True,
                                   labels_=('Rain', 'Freezing Rain', 'Mix', 'Snow', 'Hail or Graupel')):
    # labels

    # create type numerical array
    if precip_type_NWS.dtype == 'O':
        precip_type_number = parsivel_convert_NWS_code_to_numbers(precip_rate, precip_type_NWS)
    elif precip_type_NWS.dtype == 'str':
        precip_type_number = parsivel_convert_NWS_code_to_numbers(precip_rate, precip_type_NWS)
    else:
        precip_type_number = precip_type_NWS

    # there are 6 types, 0-5, only precip in 1-5
    cumulative_parameter_indx_list = [0,1,2,3,4]
    averaging_y_array = np.zeros((time_secs.shape[0], 5), dtype=float)
    for type_ in range(1,6):
        temp_precip_rate = np.array(precip_rate)
        temp_precip_rate[precip_type_number!=type_]=0

        averaging_y_array[:, type_-1] = temp_precip_rate

    temp_time_mean, temp_precip_mean = mean_discrete(time_secs, averaging_y_array, time_step_secs, time_secs[0],
                                                         cumulative_parameter_indx=cumulative_parameter_indx_list)

    # combine segregated into one y array
    cumulative_y = np.nancumsum(temp_precip_mean, axis=0)

    if restart_point_list is not None:
        for restart_point in restart_point_list:
            row_ = time_to_row_sec(temp_time_mean, restart_point)
            cumulative_y[row_ :,:] = cumulative_y[row_ :,:] - cumulative_y[row_,:]
            cumulative_y[row_, :] = np.nan



    # create figure
    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)

    # plot
    # # format x axis as time
    if x_not_time:
        ax.stackplot(temp_time_mean, cumulative_y.T, labels=labels_, colors=color_list,zorder=zorder_)
    else:
        ax.stackplot(time_seconds_to_days(temp_time_mean), cumulative_y.T, labels=labels_, colors=color_list,
                     zorder=zorder_)
        plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)


    if legend_show:
        ax.legend(loc=legend_loc)

    # add axes labels
    ax.set_xlabel(x_header)
    ax.set_ylabel(y_header)

    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)

    # number of x ticks
    ax.xaxis.set_major_locator(plt.MaxNLocator(number_ticks_x))

    ax.set_title(title_str)


    plt.show()

    return fig, ax
def p_plot_map_nc(nc_file, var_name=None, lat_name='lat', lon_name='lon',
                  time_name='time', time_row=None, time_str=None, level_index=None,
                  vmin_=None, vmax_=None, title_str=None):
    # open file in case the nc_file argument is a filename, close it when done
    close_nc=False
    if type(nc_file) == str:
        nc_file = nc.Dataset(nc_file)
        close_nc = True

    var_name_list = sorted(nc_file.variables)
    if var_name is None:
        p(var_name_list)
        input_ = input('which variable to plot (input index or name)')

        if input_ in var_name_list:
            var_name = input_
        else:
            try:
                var_name = var_name_list[int(input_)]
                if var_name in var_name_list:
                    pass
                else:
                    print('variable not found! No map created')
                    if close_nc: nc_file.close()
                    return
            except:
                print('variable not found! No map created')
                if close_nc: nc_file.close()
                return

    # get lan and lon arrs
    if lat_name in var_name_list:
        lat_ = nc_file.variables[lat_name][:].data
    elif 'latitude' in var_name_list:
        lat_ = nc_file.variables['latitude'][:].data
    else:
        print('latitude not found! No map created')
        if close_nc: nc_file.close()
        return
    if lon_name in var_name_list:
        lon_ = nc_file.variables[lon_name][:].data
    elif 'longitude' in var_name_list:
        lon_ = nc_file.variables['longitude'][:].data
    else:
        print('longitude not found! No map created')
        if close_nc: nc_file.close()
        return


    if len(nc_file.variables[var_name].shape) == 4 and level_index is None:
        print('variable has shape:', nc_file.variables[var_name].shape)
        level_index = int(input('which level index should be displayed?'))



    if time_row is not None:
        arr_ = nc_file.variables[var_name][time_row,...].filled(np.nan)
        if title_str is None:
            title_str = time_row
    elif time_str is not None:
        time_stamp_sec = time_days_to_seconds(convert_any_time_type_to_days(time_str))
        time_arr_sec = time_days_to_seconds(convert_any_time_type_to_days(nc_file.variables[time_name][:].data))
        time_row = time_to_row_sec(time_arr_sec, time_stamp_sec)
        print('closest time stamp found:', time_seconds_to_str(time_arr_sec[time_row], time_format_iso))
        arr_ = nc_file.variables[var_name][time_row,...].filled(np.nan)
        if title_str is None:
            title_str = time_seconds_to_str(time_arr_sec[time_row], time_format_iso)
    if level_index is not None:
        if len(arr_.shape) == 3:
            arr_ = arr_[level_index,...]

    if close_nc: nc_file.close()

    return p_plot_arr(arr_, lon_, lat_, cbar_label=var_name, title_str=title_str, add_coastlines=True,
                      vmin_=vmin_, vmax_=vmax_)



class SelectFromCollection(object):
    """
    Select indices from a matplotlib collection using `LassoSelector`.

    Selected indices are saved in the `ind` attribute. This tool fades out the
    points that are not part of the selection (i.e., reduces their alpha
    values). If your collection has alpha < 1, this tool will permanently
    alter the alpha values.

    Note that this tool selects collection objects based on their *origins*
    (i.e., `offsets`).

    Parameters
    ----------
    ax : :class:`~matplotlib.axes.Axes`
        Axes to interact with.

    collection : :class:`matplotlib.collections.Collection` subclass
        Collection you want to select from.

    alpha_other : 0 <= float <= 1
        To highlight a selection, this tool sets all selected points to an
        alpha value of 1 and non-selected points to `alpha_other`.
    """

    def __init__(self, ax, collection, alpha_other=0.3, facecolors=None):
        self.canvas = ax.figure.canvas
        self.collection = collection
        self.alpha_other = alpha_other

        self.xys = collection.get_offsets()
        self.Npts = len(self.xys)

        # Ensure that we have separate colors for each object
        self.fc = collection.get_facecolors()
        if len(self.fc) == 0:
            raise ValueError('Collection must have a facecolor')
        elif len(self.fc) == 1:
            self.fc = np.tile(self.fc, (self.Npts, 1))

        if facecolors is not None:
            self.fc = facecolors

        self.lasso = LassoSelector(ax, onselect=self.onselect)
        self.ind = []

    def onselect(self, verts):
        path = Path(verts)
        self.ind = np.nonzero(path.contains_points(self.xys))[0]
        self.fc[:, -1] = self.alpha_other
        self.fc[self.ind, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

    def disconnect(self):
        self.lasso.disconnect_events()
        self.fc[:, -1] = 1
        self.collection.set_facecolors(self.fc)
        self.canvas.draw_idle()

def p_hist(data_, figsize_ = (10,6), fig_ax=None, title_str=None, x_header=None, y_header=None,
           x_bins=10, normed_=False, trunk_=False, figure_filename=None,
           facecolor='blue', linewidth=1, custom_x_range_tuple=None, custom_y_range_tuple=None,
           font_size_axes_labels=12, font_size_title=14, font_size_legend=12, font_size_ticks=12,
           alpha_=1):
    if type(data_) == list:
        data_display = np.array(data_)
    elif len(data_.shape) > 1:
        data_display = np.array(data_.flatten())
    else:
        data_display = np.array(data_)

    change_font_size_figures(font_size_axes_labels, font_size_title, font_size_legend, font_size_ticks)

    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)

    if type(x_bins) is not int and type(x_bins) is not str:
        if trunk_:
            data_display[data_display > x_bins[-1]] = np.nan
        else:
            data_display[data_display > x_bins[-1]] = x_bins[-1]

    counts_, edges_ = np.histogram(data_display[~np.isnan(data_display)], x_bins)

    if normed_:
        counts_ = np.array(counts_ / np.sum(counts_), dtype=float)


    for i_ in range(counts_.shape[0]):
        ax.add_patch(mpatches.Rectangle((edges_[i_],0),edges_[i_+1]-edges_[i_],counts_[i_],
                                        linewidth=linewidth,facecolor=facecolor, alpha=alpha_))



    if custom_x_range_tuple is not None:
        ax.set_xlim(custom_x_range_tuple)
    else:
        ax.set_xlim((edges_[0], edges_[-1]))
    if custom_y_range_tuple is not None:
        ax.set_ylim(custom_y_range_tuple)
    else:
        ax.set_ylim((0, np.max(counts_) + np.max(counts_)*0.05))

    if title_str is not None: ax.set_title(title_str)
    if x_header is not None: ax.set_xlabel(x_header)
    if y_header is not None: ax.set_ylabel(y_header)


    if figure_filename is not None:
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

    return fig, ax, (counts_, edges_)

def p_arr_vectorized(A_, cmap_=default_cm, figsize_= (10,6), vmin_=None,vmax_=None, cbar_label = ''):
    fig, ax = plt.subplots(figsize=figsize_)

    if vmin_ is None: vmin_ = np.nanmin(A_)
    if vmax_ is None: vmax_ = np.nanmax(A_)

    y_, x_ = np.mgrid[0:A_.shape[0], 0:A_.shape[1]]

    surf_ = ax.pcolormesh(x_, y_, A_, cmap=cmap_, vmin=vmin_, vmax=vmax_)

    color_bar = fig.colorbar(surf_)
    color_bar.ax.set_ylabel(cbar_label)

    return fig, ax
def p_arr_vectorized_2(array_v, array_x, array_y,custom_y_range_tuple=None, custom_x_range_tuple=None,
                       x_header='', y_header='', cbar_label = '', title_str='',
                       cmap_=default_cm, figsize_= (10,6), vmin_=None,vmax_=None,
                       figure_filename = None, time_format_ = None):
    fig, ax = plt.subplots(figsize=figsize_)
    # plt.close(fig)

    if vmin_ is None: vmin_ = np.nanmin(array_v)
    if vmax_ is None: vmax_ = np.nanmax(array_v)

    if len(array_x.shape) == 1:
        array_y_reshaped = np.zeros((array_v.shape[0], array_v.shape[1]), dtype=float)
        array_x_reshaped = np.zeros((array_v.shape[0], array_v.shape[1]), dtype=float)

        for r_ in range(array_v.shape[0]):
            array_y_reshaped[r_, :] = array_y
        for c_ in range(array_v.shape[1]):
            array_x_reshaped[:, c_] = array_x

    else:
        array_y_reshaped = array_y
        array_x_reshaped = array_x

    surf_ = ax.pcolormesh(array_x_reshaped, array_y_reshaped, array_v, cmap=cmap_, vmin=vmin_, vmax=vmax_)

    color_bar = fig.colorbar(surf_)
    color_bar.ax.set_ylabel(cbar_label)
    ax.set_xlabel(x_header)
    ax.set_ylabel(y_header)
    ax.set_title(title_str)
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)

    if time_format_ is not None:
        plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)

    if figure_filename is not None:
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
        return


    return fig, ax
def p_arr_vectorized_3(array_v, array_x, array_y,
                       custom_y_range_tuple=None, custom_x_range_tuple=None,
                       custom_ticks_x=None, custom_ticks_y=None, x_header='', y_header='', title_str='',
                       show_cbar=True, cbar_format='%.2f', cbar_label = '', cbar_ax=None, cbar_orient='vertical',
                       contour_=False, contourF_=False,cmap_=default_cm, figsize_= (10,6),
                       vmin_=None, vmax_=None, figure_filename = None, grid_=False, time_format_ = None, fig_ax=None,
                       colorbar_tick_labels_list=None, show_x_ticks=True, show_y_ticks=True,extend_='neither',
                       invert_y=False, invert_x=False, levels=None, text_box_str=None,text_box_loc=None,
                       font_size_axes_labels=14, font_size_title=16, font_size_legend=12, font_size_ticks=10):
    """
    plots an array in vector form (not imshow)
    :param array_v: 2d array with values to be shown as colors
    :param array_x: 1d or 2d array with the x axes values
    :param array_y: 1d or 2d array with the y axes values
    :param custom_y_range_tuple: tuple with min and max y values to be shown in figure, this is just for display
    :param custom_x_range_tuple: tuple with min and max x values to be shown in figure, this is just for display
    :param custom_ticks_x: list/array with the ticks for the x axes
    :param custom_ticks_y: list/array with the ticks for the y axes
    :param x_header: str with the desired x header
    :param y_header: str with the desired y header
    :param cbar_label: str with the desired color bar label
    :param cbar_orient: str with the desired color bar orientation
    :param title_str: str with title of figure
    :param contour_: If true, the figure will be of countours, else it will be a pcolormesh
    :param contourF_: If true, the figure will be of filled countours, else it will be a pcolormesh
    :param cmap_: matplotlib object colormap
    :param figsize_: tuple with the size of the figure in inches (x, y)
    :param vmin_: minimum frequency to be displayed in the figure (sets the range of the colorbar)
    :param vmax_: maximum frequency to be displayed in the figure (sets the range of the colorbar)
    :param show_cbar: If true the cbar is shown.
    :param cbar_format: the str format for the ticks of the colorbar, if only integers wanted set to '%i'
    :param figure_filename: If set to a str with a path and filename, the figure will be saved and closed
    :param grid_: if true, the grid will be shown
    :param time_format_: str in a format like '%d-%m-%Y_%H:%M'. if not none, the array_x will be attempted to convert
                            to a datetime series and if posible the tick values will be formated following this str
    :param fig_ax: tuple with a figure and axes object from matplotlib. use this if you already have a figure and want
                    to add a CFAD to it, or for multiple panels
    :param colorbar_tick_labels_list: in case specific labels are wanted (like str showing ice, rain, SLW, hail)
    :param show_x_ticks: if true the ticks for the x axes will be shown
    :param show_y_ticks: if true the ticks for the y axes will be shown
    :param cbar_ax: axes object from matplotlib where the colorbar will be placed, usefull when multiple CFADs are in
                    the same figure and share one colorbar.
    :param invert_y: if true the y axes will be inversed in the display, usefull for CFTDs (by temperature)
    :param invert_x: if true the x axes will be inversed in the display, usefull for CFTDs (by temperature)
    :param levels: list/array with the ticks for the colorbar
    :param text_box_str: str text to be shown in the figure
    :param text_box_loc: location in x and y values to place the above text box
    :param font_size_axes_labels: size of font of axes labels in graph
    :param font_size_title: size of font of title in graph
    :param font_size_legend: size of font of legend in graph
    :param font_size_ticks: size of font of ticks in graph
    :param extend_: {'neither', 'both', 'min', 'max'}
    :return:
        fig: figure objects
        ax: axes objects
        surface: the point colection from matplotlib
    """


    change_font_size_figures(font_size_axes_labels, font_size_title, font_size_legend, font_size_ticks)
    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)


    if vmin_ is None: vmin_ = np.nanmin(array_v)
    if vmax_ is None: vmax_ = np.nanmax(array_v)

    if len(array_x.shape) == 1:
        array_x_reshaped = np.zeros((array_v.shape[0], array_v.shape[1]), dtype=float)
        for c_ in range(array_v.shape[1]):
            array_x_reshaped[:, c_] = array_x
    else:
        array_x_reshaped = array_x
    array_x = array_x_reshaped

    if len(array_y.shape) == 1:
        array_y_reshaped = np.zeros((array_v.shape[0], array_v.shape[1]), dtype=float)
        for r_ in range(array_v.shape[0]):
            array_y_reshaped[r_, :] = array_y
    else:
        array_y_reshaped = array_y

    array_y = array_y_reshaped
    if time_format_ is not None:
        array_x = convert_any_time_type_to_days(array_x_reshaped)


    if contour_:
        surf_ = ax.contour(array_x, array_y, array_v, levels=levels, cmap=cmap_, vmin=vmin_, vmax=vmax_, extend=extend_)
    elif contourF_:
        surf_ = ax.contourf(array_x, array_y, array_v, levels=levels, cmap=cmap_, vmin=vmin_, vmax=vmax_, extend=extend_)
    else:
        surf_ = ax.pcolormesh(array_x, array_y, array_v, cmap=cmap_, vmin=vmin_, vmax=vmax_)

    if show_cbar:
        if cbar_ax is None:
            color_bar = fig.colorbar(surf_, format=cbar_format, orientation=cbar_orient, extend=extend_)
        else:
            color_bar = fig.colorbar(surf_, format=cbar_format, cax=cbar_ax, orientation=cbar_orient, extend=extend_)
        if cbar_orient == 'vertical':
            color_bar.ax.set_ylabel(cbar_label)
        elif cbar_orient == 'horizontal':
            color_bar.ax.set_xlabel(cbar_label)
        else:
            print('Error! color bar orientation not understood. Please select vertical or horizontal')

        if colorbar_tick_labels_list is not None:
            ticks_ = np.linspace(0.5, len(colorbar_tick_labels_list) - 0.5, len(colorbar_tick_labels_list))
            color_bar.set_ticks(ticks_, extend=extend_)
            color_bar.set_ticklabels(colorbar_tick_labels_list, extend=extend_)

    if x_header is not None: ax.set_xlabel(x_header)
    if y_header is not None: ax.set_ylabel(y_header)
    if title_str is not None: ax.set_title(title_str)
    ax.grid(grid_)


    if time_format_ is not None:
        plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)
        ax.format_coord = lambda x, y: 'x=%s, y=%g, v=%g' % (plot_format_mayor(x),
                                                             y,
                                                             array_v[int(np.argmin(np.abs(array_x[:, 0] - x))), int(
                                                                 np.argmin(np.abs(array_y[0, :] - y)))])
    else:
        ax.ticklabel_format(useOffset=False)
        ax.format_coord = lambda x, y: 'x=%1.2f, y=%g, v=%g' % (x,
                                                                y,
                                                                array_v[
                                                                    int(np.argmin(np.abs(array_x[:, 0] - x))), int(
                                                                        np.argmin(np.abs(array_y[0, :] - y)))])

    if not show_x_ticks:
        plt.setp(ax.get_xticklabels(), visible=False)
    if not show_y_ticks:
        plt.setp(ax.get_yticklabels(), visible=False)


    if invert_y:
        ax.invert_yaxis()
    if invert_x:
        ax.invert_xaxis()



    if text_box_str is not None:
        if text_box_loc is None:
            x_1 = ax.axis()[0]
            y_2 = ax.axis()[3]

            text_color = 'black'
            ax.text(x_1, y_2 , str(text_box_str),
                           horizontalalignment='left',verticalalignment='top',color=text_color)
        else:
            x_1 = text_box_loc[0]
            y_2 = text_box_loc[1]
            text_color = 'black'
            ax.text(x_1, y_2 , str(text_box_str),
                           horizontalalignment='left',verticalalignment='top',color=text_color)

    if custom_ticks_x is not None: ax.xaxis.set_ticks(custom_ticks_x)
    if custom_ticks_y is not None: ax.yaxis.set_ticks(custom_ticks_y)
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)

    if figure_filename is not None:
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
        return

    return fig, ax, surf_
def p_arr(A_, cmap_=default_cm, extend_x1_x2_y1_y2 =(0,1), figsize_= (10, 6), aspect_='auto', rot_=0, title_str = '',
          vmin_=None, vmax_=None, cbar_label = '', x_as_time=False, time_format_='%H:%M %d%b%y', save_fig=False,
          figure_filename='', x_header='',y_header='', x_ticks_tuple=None, y_ticks_tuple=None, fig_ax=None,
          origin_='upper', colorbar_tick_labels_list=None, tick_label_format='plain', tick_offset=False, alpha_=1,
          show_cbar=True, cbar_ax=None, cbar_orient='vertical'):
    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)

    A_copy = np.array(A_)
    if vmin_ is not None: A_copy[A_copy < vmin_] = vmin_
    if vmax_ is not None: A_copy[A_copy > vmax_] = vmax_

    if rot_ != 0:
        A_copy = np.rot90(A_copy, rot_)

    if len(extend_x1_x2_y1_y2)==2:
        img_ = ax.imshow(A_copy, interpolation='none', cmap=cmap_, aspect= aspect_,
                         vmin=vmin_, vmax=vmax_, origin=origin_, alpha=alpha_)
    else:
        img_ = ax.imshow(A_copy, interpolation='none', cmap=cmap_, aspect= aspect_, origin=origin_, vmin=vmin_, vmax=vmax_,
                         extent=[extend_x1_x2_y1_y2[0], extend_x1_x2_y1_y2[1], extend_x1_x2_y1_y2[2], extend_x1_x2_y1_y2[3]])


    if show_cbar:
        if cbar_ax is None:
            color_bar = fig.colorbar(img_, orientation=cbar_orient)
        else:
            color_bar = fig.colorbar(img_, cax=cbar_ax, orientation=cbar_orient)

        if cbar_orient == 'vertical':
            color_bar.ax.set_ylabel(cbar_label)
        elif cbar_orient == 'horizontal':
            color_bar.ax.set_xlabel(cbar_label)
        else:
            print('Error! color bar orientation not understood. Please select vertical or horizontal')


        if colorbar_tick_labels_list is not None:
            ticks_ = np.linspace(0.5, len(colorbar_tick_labels_list) - 0.5, len(colorbar_tick_labels_list))
            color_bar.set_ticks(ticks_)
            color_bar.set_ticklabels(colorbar_tick_labels_list)
    else:
        color_bar=None


    if x_as_time:
        plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)

    if x_header is not None: ax.set_xlabel(x_header)
    if y_header is not None: ax.set_ylabel(y_header)
    if title_str is not None: ax.set_title(title_str)

    if x_ticks_tuple is not None:
        ax.xaxis.set_ticks(np.arange(x_ticks_tuple[0], x_ticks_tuple[1], x_ticks_tuple[2]))
    if y_ticks_tuple is not None:
        ax.yaxis.set_ticks(np.arange(y_ticks_tuple[0], y_ticks_tuple[1], y_ticks_tuple[2]))

    ax.ticklabel_format(useOffset=tick_offset, style='plain')
    plt.tight_layout()

    if save_fig or figure_filename != '':
        if figure_filename == '':
            name_ = str(calendar.timegm(time.gmtime()))[:-2]
            fig.savefig(path_output + 'image_' + name_ + '.png', transparent=True, bbox_inches='tight')
        else:
            fig.savefig(figure_filename, transparent=False, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()
    return fig, ax, img_, color_bar
def p_plot_colored_lines(x_array, y_array, color_array, tick_labels_list, fig_ax=None, figsize_=(10, 6),
                         x_header='', y_header='', figure_filename=None, time_format='', cbar_show=True,
                         custom_y_range_tuple=None, custom_x_range_tuple=None, grid_=False, cbar_ax=None,
                         cmap=listed_cm):

    # coincidental data only
    ar_list = coincidence_multi([x_array, y_array, color_array])
    x_array, y_array, color_array = ar_list

    # plot rain rate colored by rain type
    points = np.array([x_array, y_array]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)

    # Use a boundary norm instead
    norm = BoundaryNorm(np.arange(len(tick_labels_list)+1), cmap.N)
    lc = LineCollection(segments, cmap=cmap, norm=norm)
    lc.set_array(color_array)
    lc.set_linewidth(2)
    line = ax.add_collection(lc)
    if cbar_show:
        if cbar_ax is None:
            cb2 = fig.colorbar(line, ax=ax)
        else:
            cb2 = fig.colorbar(line, cax=cbar_ax)

        ticks_ = np.linspace(0.5, len(tick_labels_list) - 0.5, len(tick_labels_list))
        cb2.set_ticks(ticks_)
        cb2.set_ticklabels(tick_labels_list)
    else:
        cb2 = None

    # x_array = convert_any_time_type_to_days(x_array)

    ax.set_xlim(x_array.min(),
                x_array.max())
    ax.set_ylim(y_array.min(), y_array.max())
    if y_header is not None: ax.set_ylabel(y_header)
    if x_header is not None: ax.set_xlabel(x_header)
    ax.grid(grid_)
    if time_format != '':
        plot_format_mayor = mdates.DateFormatter(time_format, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)
    # plt.xticks(rotation=45)
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)
    if figure_filename is not None:
        fig.savefig(figure_filename , transparent=True, bbox_inches='tight')
        plt.close(fig)
    else:
        return fig, ax, cb2, line

def p_plot_colored_bars(x_array, y_array, color_list, color_list_unique, color_tick_labels,
                        fig_ax=None, figsize_=(10, 6),
                        x_header=None, y_header=None, figure_filename=None, time_format=time_format, cbar_show=True,
                        custom_y_range_tuple=None, custom_x_range_tuple=None, grid_=False, cbar_ax=None,
                        cbar_orient='vertical', cbar_label=None):

    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)


    x_is_time_cofirmed = True
    X_ = convert_any_time_type_to_days(x_array)
    if X_ is None:
        X_ = x_array
        x_is_time_cofirmed = False

    width_ = mode(np.diff(X_))[0][0]

    img_ = ax.bar(X_, y_array, color=color_list,  width=width_, linewidth=0)
    ax.grid(grid_)



    cmap = ListedColormap(color_list_unique)
    cmap.set_over('0.25')
    cmap.set_under('0.75')

    norm = matplotlib.colors.Normalize(vmin=0, vmax=len(color_list_unique))

    if cbar_show:
        cb2 = matplotlib.colorbar.ColorbarBase(cbar_ax,
                                               orientation=cbar_orient,
                                               cmap=cmap,
                                               norm=norm,
                                               # extend='both',
                                               # label='This is a label',
                                               # ticks=color_tick_labels,
                                               )
        ticks_ = np.linspace(0.5, len(color_tick_labels) - 0.5, len(color_tick_labels))
        cb2.set_ticks(ticks_)
        cb2.set_ticklabels(color_tick_labels)
        cb2.set_label(cbar_label)


    # if cbar_show:
    #     if cbar_ax is None:
    #         cb2 = fig.colorbar(line, ax=ax)
    #     else:
    #         cb2 = fig.colorbar(line, cax=cbar_ax)
    #
    #     ticks_ = np.linspace(0.5, len(tick_labels_list) - 0.5, len(tick_labels_list))
    #     cb2.set_ticks(ticks_)
    #     cb2.set_ticklabels(tick_labels_list)
    # else:
    #     cb2 = None

    if x_is_time_cofirmed:
        plot_format_mayor = mdates.DateFormatter(time_format, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)

    if y_header is not None: ax.set_ylabel(y_header)
    if x_header is not None: ax.set_xlabel(x_header)

    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)


    if figure_filename is not None:
        fig.savefig(figure_filename , transparent=True, bbox_inches='tight')
        plt.close(fig)
    else:
        return fig, ax, img_

def plot_array_perimeter_domain(lat_arr, lon_arr, figure_filename='',
                    min_lat=None,max_lat=None,min_lon=None,max_lon=None,
                    color_='red',
                    alpha_=1,
                    grid_step=10,
                    show_grid=True,
                    fig_ax=None, map_=None
                    ):



    if len(lon_arr.shape) == 1:
        array_x_reshaped = np.zeros((lat_arr.shape[0], lon_arr.shape[0]), dtype=float)
        for r_ in range(lat_arr.shape[0]):
            array_x_reshaped[r_, :] = lon_arr
    else:
        array_x_reshaped = lon_arr

    if len(lat_arr.shape) == 1:
        array_y_reshaped = np.zeros((lat_arr.shape[0], lon_arr.shape[0]), dtype=float)
        for c_ in range(lon_arr.shape[0]):
            array_y_reshaped[:, c_] = lat_arr
    else:
        array_y_reshaped = lat_arr

    lat_arr = array_y_reshaped
    lon_arr = array_x_reshaped



    lat_perimeter = np.concatenate([lat_arr[0,:-1], lat_arr[:-1,-1], lat_arr[-1,::-1], lat_arr[-2:0:-1,0]])
    lon_perimeter = np.concatenate([lon_arr[0,:-1], lon_arr[:-1,-1], lon_arr[-1,::-1], lon_arr[-2:0:-1,0]])



    if min_lat is None: min_lat = np.nanmin(lat_perimeter)
    if max_lat is None: max_lat = np.nanmax(lat_perimeter)
    if min_lon is None: min_lon = np.nanmin(lon_perimeter)
    if max_lon is None: max_lon = np.nanmax(lon_perimeter)




    fig, ax, map_ = plot_series_over_map(lat_perimeter.flatten(),
                                         lon_perimeter.flatten(),
                                         size_=10,
                                         resolution_='i',
                                         color_=color_,
                                         projection_='lcc',
                                         show_grid=show_grid,
                                         min_lat=min_lat,
                                         max_lat=max_lat,
                                         min_lon=min_lon,
                                         max_lon=max_lon,
                                         lake_area_thresh=9999,
                                         alpha_=alpha_,
                                         grid_step=grid_step,
                                         fig_ax=fig_ax,
                                         map_=map_,
                                         )


    if figure_filename !='':
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight', dpi=500)
    return fig, ax, map_






def plot_wind_over_map(lat_series, lon_series, U_series, V_series, size_=1, resolution_='i',
                       type_='barbs', map_=None, color_='black', fig_ax=None, title_str=None,
                       figsize_= (10, 6), map_pad=0, min_lat=None, max_lat=None, min_lon=None, max_lon=None,
                       save_fig=False, figure_filename='', projection_='merc',
                       show_grid = False, grid_step=5, lake_area_thresh=9999, coast_color='blue',
                       arrow_headwidth=3, arrow_headlength=5,arrow_headaxislength=4.5):
    if not basemap_available:
        print('Optional module basemap was not found, this functions is not available. Please install basemap')
        return None

    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)


    if min_lat is None: min_lat = np.nanmin(lat_series)
    if max_lat is None: max_lat = np.nanmax(lat_series)
    if min_lon is None: min_lon = np.nanmin(lon_series)
    if max_lon is None: max_lon = np.nanmax(lon_series)

    llcrnrlat_ = min_lat - ((max_lat - min_lat) * map_pad)
    urcrnrlat_ = max_lat + ((max_lat - min_lat) * map_pad)
    llcrnrlon_ = min_lon - ((max_lon - min_lon) * map_pad)
    urcrnrlon_ = max_lon + ((max_lon - min_lon) * map_pad)

    if llcrnrlat_ < -90 : llcrnrlat_ = -89
    if urcrnrlat_ > 90: urcrnrlat_ = 89
    if llcrnrlon_ < -180: llcrnrlon_ = -179
    if urcrnrlon_ > 180: urcrnrlon_ = 179


    if map_ is None:
        if projection_ == 'merc':
            map_ = Basemap(projection='merc',
                        llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                        llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                        resolution=resolution_, area_thresh=lake_area_thresh, ax=ax)
        else:
            map_ = Basemap(projection='lcc',
                        llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                        llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                        resolution=resolution_, area_thresh=lake_area_thresh,
                        lat_1=-10., lat_2=-30, lat_0=-17.5, lon_0=140.7, ax=ax)


    map_.drawcoastlines(color=coast_color)
    # m.fillcontinents(zorder=0)

    # parallels = np.arange(0.,90,5.)
    # meridians = np.arange(0.,360.,5.)
    # m.drawmeridians(meridians, labels=[0,0,0,1])
    # m.drawparallels(parallels, labels=[1,0,0,0])
    map_.drawcountries()

    if show_grid:
        parallels = np.arange(min_lat, max_lat, grid_step)
        # labels = [left,right,top,bottom]
        map_.drawparallels(parallels, labels=[True, False, False, False])
        meridians = np.arange(min_lon, max_lon, grid_step)
        map_.drawmeridians(meridians, labels=[False, False, False, True])


    # reshaping
    if len(lon_series.shape) == 1:
        array_x_reshaped = np.zeros((lat_series.shape[0], lon_series.shape[0]), dtype=float)
        for r_ in range(lat_series.shape[0]):
            array_x_reshaped[r_, :] = lon_series
    else:
        array_x_reshaped = lon_series

    if len(lat_series.shape) == 1:
        array_y_reshaped = np.zeros((lat_series.shape[0], lon_series.shape[0]), dtype=float)
        for c_ in range(lon_series.shape[0]):
            array_y_reshaped[:, c_] = lat_series
    else:
        array_y_reshaped = lat_series

    lat_arr = array_y_reshaped
    lon_arr = array_x_reshaped






    x, y = map_(lon_arr, lat_arr)

    if type_ == 'arrow':
        q_ = ax.quiver(x, y, U_series, V_series, color=color_, scale=size_,
                       headwidth=arrow_headwidth,headlength=arrow_headlength,headaxislength=arrow_headaxislength)
    else:
        q_ = ax.barbs(x, y, U_series, V_series, color=color_, length=size_ * 7)

    ax.set_title(title_str)


    if save_fig or figure_filename != '':
        if figure_filename == '':
            name_ = str(calendar.timegm(time.gmtime()))[:-2]
            fig.savefig(path_output + 'image_' + name_ + '.png', transparent=True, bbox_inches='tight')
        else:
            fig.savefig(figure_filename, transparent=True, bbox_inches='tight')

        plt.close(fig)
    else:
        plt.show()

    return fig, ax, map_, q_


def plot_series_over_map(lat_series, lon_series, series_=None, resolution_='i', format_='%.2f', cbar_label='',
                         map_=None, cmap_ = default_cm, size_=5, color_='black', contour_=False, fig_ax=None,
                         figsize_= (10, 6), map_pad=0, min_lat=None, max_lat=None, min_lon=None, max_lon=None,
                         vmin_=None, vmax_=None, save_fig=False, figure_filename='', projection_='merc',cbar_ax=None,
                         show_grid = False, grid_step=5, add_line=False, lake_area_thresh=9999, lw_=0,show_cbar=True,
                         cbar_orient='vertical', alpha_=1, epsg_=None, color_coast='black',
                         parallels_ticks_loc=[True, False, False, False],
                         meridians_ticks_loc=[False, False, False, True],):
    if not basemap_available:
        print('Optional module basemap was not found, this functions is not available. Please install basemap')
        return None

    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)


    if min_lat is None: min_lat = np.nanmin(lat_series)
    if max_lat is None: max_lat = np.nanmax(lat_series)
    if min_lon is None: min_lon = np.nanmin(lon_series)
    if max_lon is None: max_lon = np.nanmax(lon_series)

    if series_ is not None:
        if vmin_ is None: vmin_ = np.nanmin(series_)
        if vmax_ is None: vmax_ = np.nanmax(series_)

    llcrnrlat_ = min_lat - ((max_lat - min_lat) * map_pad)
    urcrnrlat_ = max_lat + ((max_lat - min_lat) * map_pad)
    llcrnrlon_ = min_lon - ((max_lon - min_lon) * map_pad)
    urcrnrlon_ = max_lon + ((max_lon - min_lon) * map_pad)

    if llcrnrlat_ < -90 : llcrnrlat_ = -89
    if urcrnrlat_ > 90: urcrnrlat_ = 89
    if llcrnrlon_ < -180: llcrnrlon_ = -179
    if urcrnrlon_ > 180: urcrnrlon_ = 179


    if map_ is None:
        if projection_ == 'merc':
            map_ = Basemap(projection='merc',
                        llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                        llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                        resolution=resolution_, area_thresh=lake_area_thresh,ax=ax, epsg=epsg_)
        elif projection_ == 'geos':
            map_ = Basemap(projection='geos',
                            rsphere=(6378137.00, 6356752.3142),
                            resolution=resolution_, area_thresh=lake_area_thresh,
                            # llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                            # llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                            lon_0=140.7,
                            satellite_height=35785831, ax=ax)
        else:
            map_ = Basemap(projection='lcc',
                           llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                           llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                           resolution=resolution_, area_thresh=lake_area_thresh,
                           lat_1=-10., lat_2=-30, lat_0=-17.5, lon_0=140.7,ax=ax, epsg=epsg_)
    try:
        map_.drawcoastlines(color=color_coast)
    except:
        pass
    # m.fillcontinents(zorder=0)

    map_.drawcountries()

    if show_grid:
        parallels = np.arange(min_lat, max_lat, grid_step)
        # labels = [left,right,top,bottom]
        map_.drawparallels(parallels, labels=parallels_ticks_loc)
        meridians = np.arange(min_lon, max_lon, grid_step)
        map_.drawmeridians(meridians, labels=meridians_ticks_loc)


    x, y = map_(lon_series, lat_series)

    if series_ is None:
        trajs_ = ax.scatter(x, y, lw=lw_, c=color_, s=size_, alpha=alpha_)
        if add_line:
            ax.plot(x, y, color=color_)
    else:
        if len(series_.shape) == 1:
            if contour_:
                ax.tricontourf(x, y, series_, cmap=cmap_)
            else:
                trajs_ = ax.scatter(x, y, lw=lw_, c=series_, s=size_, vmin=vmin_, vmax=vmax_, cmap=cmap_, alpha=alpha_)
                ax.format_coord = lambda x_fig, y_fig: 'x=%g, y=%g, v=%g' % (
                    lon_series[int(np.argmin(np.abs(x - x_fig)))],
                    lat_series[int(np.argmin(np.abs(y - y_fig)))],
                    series_[int(np.argmin(np.abs(x - x_fig)**2 + np.abs(y - y_fig)**2))]
                )
                if show_cbar:
                    if cbar_ax is None:
                        color_bar = fig.colorbar(trajs_, format=format_, orientation=cbar_orient)
                    else:
                        color_bar = fig.colorbar(trajs_, format=format_, cax=cbar_ax, orientation=cbar_orient)
                    color_bar.ax.set_ylabel(cbar_label)



        else:
            trajs_ = ax.pcolormesh(x, y, series_, cmap=cmap_, vmin=vmin_, vmax=vmax_, alpha=alpha_)
            ax.format_coord = lambda x_fig, y_fig: 'x=%g, y=%g, v=%g' % (
                lon_series[int(np.argmin(np.abs(x - x_fig)))],
                lat_series[int(np.argmin(np.abs(y - y_fig)))],
                series_[int(np.argmin(np.abs(x - x_fig))),
                        int(np.argmin(np.abs(y - y_fig)))])
            if show_cbar:
                if cbar_ax is None:
                    color_bar = fig.colorbar(trajs_, format=format_)
                else:
                    color_bar = fig.colorbar(trajs_, format=format_, cax=cbar_ax)
                if cbar_orient == 'vertical':
                    color_bar.ax.set_ylabel(cbar_label)
                elif cbar_orient == 'horizontal':
                    color_bar.ax.set_xlabel(cbar_label)
                else:
                    print('Error! color bar orientation not understood. Please select vertical or horizontal')



    if save_fig or figure_filename != '':
        if figure_filename == '':
            name_ = str(calendar.timegm(time.gmtime()))[:-2]
            fig.savefig(path_output + 'image_' + name_ + '.png', transparent=True, bbox_inches='tight')
        else:
            fig.savefig(figure_filename, transparent=True, bbox_inches='tight')

        plt.close(fig)
    else:
        plt.show()

    return fig, ax, map_
def plot_arr_over_map(arr_, lat_arr, lon_arr, resolution_='i', format_='%.2f', cbar_label='', cmap_ = default_cm,
                      map_pad=0, min_lat=None,max_lat=None,min_lon=None,max_lon=None, vmin_=None,vmax_=None,
                      save_fig=False, figure_filename='', projection_='merc', show_grid = False, grid_step=5,
                      coast_color='black', title_str=None, colorbar_tick_labels_list=None, return_traj=False,
                      figsize_= (10, 6), parallels_=None, meridians_=None, grid_line_width=1,font_size=14,
                      lake_area_thresh=9999, fig_ax=None, show_cbar=True, cbar_ax=None, alpha_=1, map_=None,
                      cbar_orient='vertical',extend_='neither', colorbar_ticks=None,
                      parallels_ticks_loc=[True, False, False, False],
                      meridians_ticks_loc=[False, False, False, True],
                      ):
    if not basemap_available:
        print('Optional module basemap was not found, this functions is not available. Please install basemap')
        return None

    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)

    if min_lat is None: min_lat = np.nanmin(lat_arr)
    if max_lat is None: max_lat = np.nanmax(lat_arr)
    if min_lon is None: min_lon = np.nanmin(lon_arr)
    if max_lon is None: max_lon = np.nanmax(lon_arr)

    if vmin_ is None: vmin_ = np.nanmin(arr_)
    if vmax_ is None: vmax_ = np.nanmax(arr_)

    llcrnrlat_ = min_lat - ((max_lat - min_lat) * map_pad)
    urcrnrlat_ = max_lat + ((max_lat - min_lat) * map_pad)
    llcrnrlon_ = min_lon - ((max_lon - min_lon) * map_pad)
    urcrnrlon_ = max_lon + ((max_lon - min_lon) * map_pad)

    if llcrnrlat_ < -90  : llcrnrlat_ = -89
    if urcrnrlat_ > 90   : urcrnrlat_ = 89
    if llcrnrlon_ < -180 : llcrnrlon_ = -179
    if urcrnrlon_ > 180  : urcrnrlon_ = 179


    if map_ is None:
        if projection_ == 'merc':
            m = Basemap(projection='merc',
                        llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                        llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                        resolution=resolution_, area_thresh=lake_area_thresh, ax=ax)
        elif projection_ == 'lcc':
            m = Basemap(projection='lcc',
                        llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                        llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                        resolution=resolution_, area_thresh=lake_area_thresh,
                        lat_1=-10., lat_2=-30, lat_0=-17.5, lon_0=140.7, ax=ax)
        elif projection_ == 'geos':
            m = Basemap(projection='geos',
                        rsphere=(6378137.00, 6356752.3142),
                        resolution=resolution_, area_thresh=lake_area_thresh,
                        lon_0=140.7,
                        satellite_height=35785831, ax=ax)
        else:
            m = Basemap(projection=projection_,
                        llcrnrlat = llcrnrlat_, urcrnrlat = urcrnrlat_,
                        llcrnrlon = llcrnrlon_, urcrnrlon = urcrnrlon_,
                        resolution=resolution_, area_thresh=lake_area_thresh,
                        lat_1=-10., lat_2=-30, lat_0=-17.5, lon_0=140.7, ax=ax)
    else:
        m = map_

    try:
        m.drawcoastlines(color=coast_color)
        m.drawcountries()
    except:
        pass
    # m.bluemarble()

    if show_grid:
        if parallels_ is None:
            parallels_ = np.arange(min_lat, max_lat, grid_step)
        if meridians_ is None:
            meridians_ = np.arange(min_lon, max_lon, grid_step)

        m.drawparallels(parallels_, labels=parallels_ticks_loc,  linewidth=grid_line_width)
        m.drawmeridians(meridians_, labels=meridians_ticks_loc,  linewidth=grid_line_width)


    # reshaping
    if len(arr_.shape)==3:
        if arr_.shape[0] == 1:
            arr_ = arr_[0,:,:]

    if len(lon_arr.shape) == 1:
        array_x_reshaped = np.zeros((arr_.shape[0], arr_.shape[1]), dtype=float)
        for r_ in range(arr_.shape[0]):
            array_x_reshaped[r_, :] = lon_arr
    else:
        array_x_reshaped = lon_arr

    if len(lat_arr.shape) == 1:
        array_y_reshaped = np.zeros((arr_.shape[0], arr_.shape[1]), dtype=float)
        for c_ in range(arr_.shape[1]):
            array_y_reshaped[:, c_] = lat_arr
    else:
        array_y_reshaped = lat_arr

    lat_arr = array_y_reshaped
    lon_arr = array_x_reshaped



    x, y = m(lon_arr, lat_arr)

    if x.max() == float('inf') or x.min() == float('-inf'):
        x[np.isinf(x)] = np.nan
        x_mid = np.nanmean(x)
        x[np.isnan(x)] = x_mid
    if y.max() == float('inf') or y.min() == float('-inf'):
        y[np.isinf(y)] = 0

    trajs_ = ax.pcolormesh(x, y, arr_, cmap=cmap_, vmin=vmin_, vmax=vmax_, alpha=alpha_)

    if show_cbar:
        if cbar_ax is None:
            color_bar = fig.colorbar(trajs_, format=format_, orientation=cbar_orient)
        else:
            color_bar = fig.colorbar(trajs_, format=format_, cax=cbar_ax, orientation=cbar_orient)
        if cbar_orient == 'vertical':
            color_bar.ax.set_ylabel(cbar_label)
        elif cbar_orient == 'horizontal':
            color_bar.ax.set_xlabel(cbar_label)
        else:
            print('Error! color bar orientation not understood. Please select vertical or horizontal')
        color_bar.ax.tick_params(labelsize=font_size)

        if colorbar_tick_labels_list is not None:
            if colorbar_ticks is None:
                colorbar_ticks = np.linspace(0.5, len(colorbar_tick_labels_list) - 0.5, len(colorbar_tick_labels_list))
            color_bar.set_ticks(colorbar_ticks)
            color_bar.set_ticklabels(colorbar_tick_labels_list)

    if title_str is not None:
        ax.set_title(title_str)

    ax.format_coord = lambda x_fig, y_fig: 'x=%g, y=%g, v=%g' % (
        lon_arr.flatten()[np.argmin(np.abs(x - x_fig))],
        lat_arr.flatten()[np.argmin(np.abs(y - y_fig))],
        arr_.flatten()[int(np.argmin(np.abs(x - x_fig) ** 2 + np.abs(y - y_fig) ** 2))])

    if save_fig or figure_filename != '':
        if figure_filename == '':
            name_ = str(calendar.timegm(time.gmtime()))[:-2]
            fig.savefig(path_output + 'image_' + name_ + '.png', transparent=True, bbox_inches='tight')
        else:
            fig.savefig(figure_filename, transparent=True, bbox_inches='tight')

        plt.close(fig)
    else:
        plt.show()

    if return_traj:
        return fig, ax, m, trajs_
    else:
        return fig, ax, m

def plot_arr_over_map_nc(nc_file, var_name=None, lat_name='lat', lon_name='lon',
                         time_name='time', time_row=None, time_str=None, level_index=None):
    if not basemap_available:
        print('Optional module basemap was not found, this functions is not available. Please install basemap')
        return None

    # open file in case the nc_file argument is a filename, close it when done
    close_nc=False
    if type(nc_file) == str:
        nc_file = nc.Dataset(nc_file)
        close_nc = True

    var_name_list = sorted(nc_file.variables)
    if var_name is None:
        p(var_name_list)
        input_ = input('which variable to plot (input index or name)')

        if input_ in var_name_list:
            var_name = input_
        else:
            try:
                var_name = var_name_list[int(input_)]
                if var_name in var_name_list:
                    pass
                else:
                    print('variable not found! No map created')
                    if close_nc: nc_file.close()
                    return
            except:
                print('variable not found! No map created')
                if close_nc: nc_file.close()
                return

    # get lan and lon arrs
    if lat_name in var_name_list:
        lat_ = nc_file.variables[lat_name][:].data
    elif 'latitude' in var_name_list:
        lat_ = nc_file.variables['latitude'][:].data
    else:
        print('latitude not found! No map created')
        if close_nc: nc_file.close()
        return
    if lon_name in var_name_list:
        lon_ = nc_file.variables[lon_name][:].data
    elif 'longitude' in var_name_list:
        lon_ = nc_file.variables['longitude'][:].data
    else:
        print('longitude not found! No map created')
        if close_nc: nc_file.close()
        return


    if len(nc_file.variables[var_name].shape) == 4 and level_index is None:
        print('variable has shape:', nc_file.variables[var_name].shape)
        level_index = int(input('which level index should be displayed?'))



    title_ = ''
    if time_row is not None:
        arr_ = nc_file.variables[var_name][time_row,...].filled(np.nan)
        title_ = time_row
    elif time_str is not None:
        time_stamp_sec = time_days_to_seconds(convert_any_time_type_to_days(time_str))
        time_arr_sec = time_days_to_seconds(convert_any_time_type_to_days(nc_file.variables[time_name][:].data))
        time_row = time_to_row_sec(time_arr_sec, time_stamp_sec)
        print('closest time stamp found:', time_seconds_to_str(time_arr_sec[time_row], time_format_iso))
        arr_ = nc_file.variables[var_name][time_row,...].filled(np.nan)
        title_ = time_seconds_to_str(time_arr_sec[time_row], time_format_iso)

    if level_index is not None:
        if len(arr_.shape) == 3:
            arr_ = arr_[level_index,...]

    if close_nc: nc_file.close()

    return plot_arr_over_map(arr_, lat_, lon_, cbar_label=var_name, title_str=title_)


def plot_3D_scatter(x_series, y_series, z_series, label_names_tuples_xyz=tuple(''), size_ = 15, color_='b'):
    fig = plt.figure()
    ax = Axes3D(fig)

    ax.scatter(x_series, y_series, z_series,s=size_,c=color_,lw = 0)


    if len(label_names_tuples_xyz) == 3:
        ax.set_xlabel(label_names_tuples_xyz[0])
        ax.set_ylabel(label_names_tuples_xyz[1])
        ax.set_zlabel(label_names_tuples_xyz[2])



    plt.show()
    return fig, ax
def plot_3D_stacket_series_lines(x_z_series_list, y_series=None, y_as_time=False, time_format=time_format,
                                 log_z=False, invert_z=False,
                                 custom_x_range_tuple=None, custom_y_range_tuple=None, custom_z_range_tuple=None,
                                 label_names_tuples_xyz=tuple(''), color_='b'):
    fig = plt.figure()
    ax = Axes3D(fig)

    if y_series is None:
        y_series = np.arange(len(x_z_series_list))

    for t_ in range(len(x_z_series_list)):
        y_ = np.ones(len(x_z_series_list[t_][0])) * y_series[t_]
        ax.plot(x_z_series_list[t_][0], y_, x_z_series_list[t_][1], c=color_)


    if len(label_names_tuples_xyz) == 3:
        ax.set_xlabel(label_names_tuples_xyz[0])
        ax.set_ylabel(label_names_tuples_xyz[1])
        ax.set_zlabel(label_names_tuples_xyz[2])

    if y_as_time:
        plot_format_mayor = mdates.DateFormatter(time_format, tz=tz_UTC)
        ax.yaxis.set_major_formatter(plot_format_mayor)

    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_z_range_tuple is not None: ax.set_zlim(custom_z_range_tuple)

    if log_z:
        ax.set_zscale("log")#, nonposy='clip')
    if invert_z:
        ax.invert_zaxis()

    ax.yaxis.set_ticks(y_series)

    plt.show()
    return fig, ax
def plot_shared_x_axis(X_Y_list, S_=5, x_header=None,y_header_list=None, t_line=False, grid_=False, cus_loc =None,
                       c_='', custom_y_range_tuple=None, custom_x_range_tuple=None, figsize_ = (10,6), save_fig=False,
                       figure_filename='',title_str = '', cmap_=default_cm, sharex=True, sharey=False,
                       custom_x_ticks_start_end_step=None, custom_y_ticks_start_end_step=None, rot_y_label=90,
                       time_format_='%H:%M %d%b%y', x_as_time=False, add_line=False, linewidth_=2,
                       invert_y=False, invert_x=False, log_x=False,log_y=False, transparent_=True):

    fig, (ax_list) = plt.subplots(nrows=len(X_Y_list), sharex=sharex, sharey=sharey, figsize=figsize_)

    if c_=='':
        n = int(len(X_Y_list))
        color_list = cmap_(np.linspace(0, 1, n))
        for series_number in range(len(X_Y_list)):
            ax_list[series_number].scatter(X_Y_list[series_number][0],X_Y_list[series_number][1],
                                           c= color_list[series_number], s = S_, lw = 0)
            if add_line:
                ax_list[series_number].plot(X_Y_list[series_number][0], X_Y_list[series_number][1],
                                            c=color_list[series_number], linewidth=linewidth_)
    else:
        for series_number in range(len(X_Y_list)):
            ax_list[series_number].scatter(X_Y_list[series_number][0],X_Y_list[series_number][1],
                                                s = S_, lw = 0,  c = c_)

    if x_header is not None: ax_list[-1].set_xlabel(x_header)

    for series_number in range(len(X_Y_list)):
        if y_header_list is not None:
            ax_list[series_number].set_ylabel(y_header_list[series_number], rotation=rot_y_label)
        if grid_:
            ax_list[series_number].grid(True)
        if t_line:
            plot_trend_line(ax_list[series_number], X_Y_list[series_number][0],X_Y_list[series_number][1],
                            order=1, c='r', alpha=1, cus_loc = cus_loc)

        if custom_y_range_tuple is not None: ax_list[series_number].set_ylim(custom_y_range_tuple)
        if custom_x_range_tuple is not None: ax_list[series_number].set_xlim(custom_x_range_tuple)

        if custom_x_ticks_start_end_step is not None:
            ax_list[series_number].xaxis.set_ticks(np.arange(custom_x_ticks_start_end_step[0],
                                                             custom_x_ticks_start_end_step[1],
                                                             custom_x_ticks_start_end_step[2]))
        if custom_y_ticks_start_end_step is not None:
            ax_list[series_number].yaxis.set_ticks(np.arange(custom_y_ticks_start_end_step[0],
                                                             custom_y_ticks_start_end_step[1],
                                                             custom_y_ticks_start_end_step[2]))

        if x_as_time:
            plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
            ax_list[series_number].xaxis.set_major_formatter(plot_format_mayor)

        if invert_y:
            ax_list[series_number].invert_yaxis()
        if invert_x:
            ax_list[series_number].invert_xaxis()
        if log_x:
            ax_list[series_number].set_xscale("log", nonposy='clip')
        if log_y:
            ax_list[series_number].set_yscale("log", nonposy='clip')

    for series_number in range(len(X_Y_list)-1):
        plt.setp(ax_list[series_number].get_xticklabels(), visible=False)

    ax_list[0].set_title(title_str)
    fig.tight_layout()

    if save_fig or figure_filename != '':
        if figure_filename == '':
            name_ = str(calendar.timegm(time.gmtime()))[:-2]
            fig.savefig(path_output + 'image_' + name_ + '.png', transparent=True, bbox_inches='tight')
        else:
            fig.savefig(figure_filename, transparent=transparent_, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

    return fig, ax_list
def plot_shared_y_axis(X_Y_list, S_=5, x_header_list=None, y_header=None, t_line=False, grid_=False, cus_loc=None,
                       c_='', custom_y_range_tuple=None, custom_x_range_tuple=None, figsize_=(10, 6), save_fig=False,
                       figure_filename='', title_str='', cmap_=default_cm, sharex=False, sharey=True,
                       custom_x_ticks_start_end_step=None, custom_y_ticks_start_end_step=None,
                       time_format_='%H:%M %d%b%y', x_as_time=False, add_line=False, linewidth_=2,
                       invert_y=False, invert_x=False, log_x=False, log_y=False, transparent_=True):
    fig, (ax_list) = plt.subplots(ncolumns=len(X_Y_list), sharex=sharex, sharey=sharey, figsize=figsize_)

    if c_ == '':
        n = int(len(X_Y_list))
        color_list = cmap_(np.linspace(0, 1, n))
        for series_number in range(len(X_Y_list)):
            ax_list[series_number].scatter(X_Y_list[series_number][0], X_Y_list[series_number][1],
                                           c=color_list[series_number], s=S_, lw=0)
            if add_line:
                ax_list[series_number].plot(X_Y_list[series_number][0], X_Y_list[series_number][1],
                                            c=color_list[series_number], linewidth=linewidth_)
    else:
        for series_number in range(len(X_Y_list)):
            ax_list[series_number].scatter(X_Y_list[series_number][0], X_Y_list[series_number][1],
                                           s=S_, lw=0, c=c_[series_number], cmap=cmap_)

    if y_header is not None: ax_list[0].set_ylabel(y_header)

    for series_number in range(len(X_Y_list)):
        if x_header_list is not None:
            ax_list[series_number].set_ylabel(x_header_list[series_number])
        if grid_:
            ax_list[series_number].grid(True)
        if t_line:
            plot_trend_line(ax_list[series_number], X_Y_list[series_number][0], X_Y_list[series_number][1],
                            order=1, c='r', alpha=1, cus_loc=cus_loc)

        if custom_y_range_tuple is not None: ax_list[series_number].set_ylim(custom_y_range_tuple)
        if custom_x_range_tuple is not None: ax_list[series_number].set_xlim(custom_x_range_tuple)

        if custom_x_ticks_start_end_step is not None:
            ax_list[series_number].xaxis.set_ticks(np.arange(custom_x_ticks_start_end_step[0],
                                                             custom_x_ticks_start_end_step[1],
                                                             custom_x_ticks_start_end_step[2]))
        if custom_y_ticks_start_end_step is not None:
            ax_list[series_number].yaxis.set_ticks(np.arange(custom_y_ticks_start_end_step[0],
                                                             custom_y_ticks_start_end_step[1],
                                                             custom_y_ticks_start_end_step[2]))

        if x_as_time:
            plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
            ax_list[series_number].xaxis.set_major_formatter(plot_format_mayor)

        if invert_y:
            ax_list[series_number].invert_yaxis()
        if invert_x:
            ax_list[series_number].invert_xaxis()
        if log_x:
            ax_list[series_number].set_xscale("log", nonposy='clip')
        if log_y:
            ax_list[series_number].set_yscale("log", nonposy='clip')

    for series_number in range(len(X_Y_list) - 1):
        plt.setp(ax_list[series_number+1].get_xticklabels(), visible=False)

    ax_list[0].set_title(title_str)

    fig.tight_layout()
    if save_fig or figure_filename != '':
        if figure_filename == '':
            name_ = str(calendar.timegm(time.gmtime()))[:-2]
            fig.savefig(path_output + 'image_' + name_ + '.png', transparent=True, bbox_inches='tight')
        else:
            fig.savefig(figure_filename, transparent=transparent_, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

    return fig, ax_list

def scatter_custom_size(X_,Y_,S_, x_header=None,y_header=None, t_line=False, grid_=False, cus_loc =None, c_='',
                        custom_y_range_tuple=None, custom_x_range_tuple=None, figsize_ = (10,6), save_fig=False,
                        custom_x_ticks_start_end_step=None, custom_y_ticks_start_end_step=None, extra_text='',
                        time_format_='%H:%M %d%b%y', x_as_time=False, c_header=None, add_line=False, linewidth_=2,
                        line_color='black'):
    fig, ax = plt.subplots(figsize=figsize_)
    if c_=='':
        ax.scatter(X_,Y_, s = S_, lw = 0, c = 'black')
        if add_line:
            ax.plot(X_, Y_, c=line_color, linewidth=linewidth_)
    else:
        im = ax.scatter(X_,Y_, s = S_, lw = 0,  c = c_, cmap = default_cm)
        color_bar = fig.colorbar(im,fraction=0.046, pad=0.04)
        if c_header is not None: color_bar.ax.set_ylabel(c_header)
    if x_header is not None: ax.set_xlabel(x_header)
    if y_header is not None: ax.set_ylabel(y_header)
    # ax.yaxis.set_ticks(np.arange(180, 541, 45))
    if grid_:
        ax.grid(True)
    if t_line:
        plot_trend_line(ax, X_, Y_, order=1, c='r', alpha=1, cus_loc = cus_loc, extra_text=extra_text)

    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)

    if custom_x_ticks_start_end_step is not None:
        ax.xaxis.set_ticks(np.arange(custom_x_ticks_start_end_step[0], custom_x_ticks_start_end_step[1], custom_x_ticks_start_end_step[2]))
    if custom_y_ticks_start_end_step is not None:
        ax.yaxis.set_ticks(np.arange(custom_y_ticks_start_end_step[0], custom_y_ticks_start_end_step[1], custom_y_ticks_start_end_step[2]))

    if x_as_time:
        plot_format_mayor = mdates.DateFormatter(time_format_, tz=tz_UTC)
        ax.xaxis.set_major_formatter(plot_format_mayor)

    if save_fig:
        name_ = str(calendar.timegm(time.gmtime()))[:-2]
        fig.savefig(path_output + 'image_' + name_ + '.png',transparent=True, bbox_inches='tight')
    else:
        plt.show()

    return fig, ax
def Display_emission_array(filename_, variable_name):
    netcdf_file_object = nc.Dataset(filename_, 'r')
    p_arr(netcdf_file_object.variables[variable_name][0, 0, ::-1, :])

    netcdf_file_object.close()
def power_plot(X_, Y_, Size_=5, x_header='',y_header='', trend_line=False, show_line=False, lw_=2, grid_=False,
               cus_loc = '', c_='', custom_y_range_tuple=None, custom_x_range_tuple=None, cbar_label = ''):
    fig, ax = plt.subplots()
    if c_=='':
        ax.scatter(X_,Y_, s = Size_, lw = 0, c = 'black')
        if show_line:
            ax.plot(X_,Y_, lw = lw_, color = 'black')
    else:
        im = ax.scatter(X_,Y_, s = Size_, lw = 0,  c = c_, cmap = default_cm)
        ax.plot(X_,Y_, lw = lw_,  c = c_, cmap = default_cm)
        color_bar = fig.colorbar(im,fraction=0.046, pad=0.04)
        color_bar.ax.set_ylabel(cbar_label)
    ax.set_xlabel(x_header)
    ax.set_ylabel(y_header)
    if grid_:
        ax.grid(True)
    if trend_line:
        plot_trend_line(ax, X_, Y_, order=1, c='r', alpha=1, cus_loc = cus_loc)

    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)
    plt.show()
    return fig, ax
def power_plot_with_error(X_, Y_, yerr_, Size_=5, c_='', x_header='',y_header='', trend_line=False, lw_=2, grid_=False,
                          cus_loc = '', custom_y_range_tuple=None, custom_x_range_tuple=None, cbar_label = ''):
    fig, ax = plt.subplots()
    if c_=='':
        ax.scatter(X_,Y_, s = Size_, lw = 0, c = 'black')
        ax.errorbar(X_,Y_, yerr=yerr_, color = 'black')
    else:
        im = ax.scatter(X_,Y_, s = Size_, lw = 0,  c = c_, cmap = default_cm)
        ax.plot(X_,Y_, lw = lw_,  c = c_, cmap = default_cm)
        color_bar = fig.colorbar(im,fraction=0.046, pad=0.04)
        color_bar.ax.set_ylabel(cbar_label)
    ax.set_xlabel(x_header)
    ax.set_ylabel(y_header)
    if grid_:
        ax.grid(True)
    if trend_line:
        plot_trend_line(ax, X_, Y_, order=1, c='r', alpha=1, cus_loc = cus_loc)

    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)
    plt.show()
def plot_preview_x_as_time(header_,days_,values_):

    plot_format_mayor = mdates.DateFormatter('%H:%M %d%b%y', tz=tz_UTC)
    fig, ax = plt.subplots()
    if len(values_.shape) > 1:
        for c_ in range(values_.shape[1]):
            ax.plot_date(days_,values_[:,c_], markersize=2, markeredgewidth=0, label=header_[c_])
    else:
        ax.plot_date(days_,values_,'ko-', markersize=2, markeredgewidth=0, label=header_)
    ax.xaxis.set_major_formatter(plot_format_mayor)
    plt.show()
def plot_values_x_as_time(header_,values_,x_array,y_list,
                          legend_=False, plot_fmt_str0='%H:%M %d%b%y'):
    color_list = default_cm(np.linspace(0,1,len(y_list)))
    plot_format_mayor = mdates.DateFormatter(plot_fmt_str0, tz=tz_UTC)
    fig, ax = plt.subplots()
    for c_,y_ in enumerate(y_list):
        color_ = color_list[c_]
        ax.plot(x_array,values_[:,y_], color = color_,label=header_[y_])
    ax.xaxis.set_major_formatter(plot_format_mayor)
    fig.tight_layout()
    if legend_: ax.legend(loc=(.95,.0))
    plt.show()
def plot_trend_line(axes_, xd, yd, c='r', alpha=1, cus_loc = None, text_color='black', return_params=False,
                    extra_text='', t_line_1_1=True, fit_function=None, fontsize_=12, add_text=True,
                    fit_function_p0=None):
    """Make a line of best fit"""
    #create clean series
    x_, y_ = coincidence(xd,yd)



    if fit_function is not None:
        params = curve_fit(fit_function, x_, y_, p0=fit_function_p0)
        print('fitted parameters')
        print(params[0])

        fit_line_x = np.arange(int(np.nanmin(x_)),int(np.nanmax(x_))+1,.1)
        plotting_par_list = [fit_line_x]
        for fit_par in params[0]:
            plotting_par_list.append(fit_par)
        funt_par = tuple(plotting_par_list)
        fit_line_y = fit_function(*funt_par)
        axes_.plot(fit_line_x, fit_line_y, c, alpha=alpha)


        # calculate R2
        plotting_par_list = [x_]
        params_str_ = ''
        for i_, fit_par in enumerate(params[0]):
            if extra_text == '':
                params_str_ = params_str_ + 'fit parameters ' + str(i_+1) + ': ' + '$%0.2f$' % (fit_par) + '\n'
            else:
                params_str_ = params_str_ + extra_text + '$%0.2f$' % (fit_par) + '\n'
            plotting_par_list.append(fit_par)
        funt_par = tuple(plotting_par_list)
        fit_line_y = fit_function(*funt_par)
        residuals = y_ - fit_line_y
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_ - np.mean(y_))**2)
        Rsqr = float(1 - (ss_res / ss_tot))

        # Plot R^2 value
        x_1 = np.nanmin(x_)
        y_2 = np.nanmax(y_)
        error_text = '$R^2 = %0.2f$' % Rsqr
        if cus_loc is None:
            axes_.text(x_1, y_2 , params_str_ + error_text, fontsize=fontsize_,
                       horizontalalignment='left',verticalalignment='top',color=text_color,
                       bbox={'facecolor': 'white', 'edgecolor': 'none'})
        else:
            axes_.text(cus_loc[0], cus_loc[1] , params_str_ + error_text, fontsize=fontsize_,
                       horizontalalignment='left',verticalalignment='top',color=text_color,
                       bbox={'facecolor': 'white', 'edgecolor': 'none'})

    else:
        # Calculate trend line
        params = np.polyfit(x_, y_, 1)
        intercept = params[-1]
        slope = params[-2]
        minxd = np.nanmin(x_)
        maxxd = np.nanmax(x_)

        xl = np.array([minxd, maxxd])
        yl = slope * xl + intercept

        print('fitted parameters')
        print(slope, intercept)


        # Plot trend line
        axes_.plot(xl, yl, c, alpha=alpha)

        # Calculate R Squared
        poly_1d = np.poly1d(params)
        ybar = np.sum(y_) / len(y_)
        ssreg = np.sum((poly_1d(x_) - ybar) ** 2)
        sstot = np.sum((y_ - ybar) ** 2)
        Rsqr = float(ssreg / sstot)

        # Plot R^2 value
        x_1 = np.nanmin(x_)
        y_2 = np.nanmax(y_)
        if intercept >= 0:
            if extra_text=='':
                equat_text = '$Y = %0.2f*x + %0.2f$' % (slope,intercept)
            else:
                equat_text = extra_text + '\n' + '$Y = %0.2f*x + %0.2f$' % (slope,intercept)
        else:
            if extra_text=='':
                equat_text = '$Y = %0.2f*x %0.2f$' % (slope,intercept)
            else:
                equat_text = extra_text + '\n' + '$Y = %0.2f*x %0.2f$' % (slope,intercept)
        error_text = '$R^2 = %0.2f$' % Rsqr
        if add_text:
            if cus_loc is None:
                axes_.text(x_1, y_2 , equat_text + '\n' + error_text, fontsize=fontsize_,
                           horizontalalignment='left',verticalalignment='top',color=text_color)
            else:
                axes_.text(cus_loc[0], cus_loc[1] , equat_text + '\n' + error_text, fontsize=fontsize_,
                           horizontalalignment='left',verticalalignment='top',color=text_color)
    # plot 1:1 line if true
    if t_line_1_1:
        xy_min = np.min([np.nanmin(x_),np.nanmin(y_)])
        xy_max = np.max([np.nanmax(x_),np.nanmax(y_)])
        axes_.plot([xy_min, xy_max], [xy_min, xy_max], 'k--')

    if return_params:
        return Rsqr, params
    else:
        return Rsqr
def p_density_scatter( x_ , y_, fig_ax = None, cmap_=default_cm, sort = True, bins = 20, show_cbar=False,
                       rasterized_=False, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """

    x, y = coincidence(x_ , y_)

    if fig_ax is None :
        fig , ax = plt.subplots()
    else:
        fig = fig_ax[0]
        ax = fig_ax[1]
    data , x_e, y_e = np.histogram2d( x, y, bins = bins)
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data ,
                 np.vstack([x,y]).T , method = "splinef2d", bounds_error = False )

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

    im = ax.scatter( x, y, c=z, cmap=cmap_, lw=0, **kwargs)
    im.set_rasterized(rasterized_)

    if show_cbar:
        color_bar = fig.colorbar(im, fraction=0.046, pad=0.04)

    return ax


# diurnal variations
def diurnal_variability_boxplot(time_in_seconds, y_, fig_ax=None, x_header='Hours', y_header='',figure_filename='',
                                bin_size_hours=1, min_bin_population=10, start_value=0, figsize_=(10,6), title_str=''):
    # convert time to struct
    time_hour = np.zeros(time_in_seconds.shape[0], dtype=float)
    time_mins = np.zeros(time_in_seconds.shape[0], dtype=float)
    time_secs = np.zeros(time_in_seconds.shape[0], dtype=float)

    for r_ in range(time_in_seconds.shape[0]):
        time_hour[r_] = time.gmtime(time_in_seconds[r_])[3]
        time_mins[r_] = time.gmtime(time_in_seconds[r_])[4]
        time_secs[r_] = time.gmtime(time_in_seconds[r_])[5]

    time_hours = time_hour + (time_mins + (time_secs/60))/60

    # get coincidences only
    x_val,y_val = coincidence(time_hours, y_)
    # combine x and y in matrix
    M_ = np.column_stack((x_val,y_val))
    # always ascending to increase efficiency
    M_sorted = M_[M_[:,0].argsort()] # sort by first column
    M_ = M_sorted
    # convert data to list of bins
    y_binned = []
    x_binned = []

    start_bin_edge = start_value

    last_row = 0
    last_row_temp = last_row
    while start_bin_edge <= np.nanmax(x_val):
        y_val_list = []
        for row_ in range(last_row, M_.shape[0]):
            if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size_hours:
                if M_[row_, 1] == M_[row_, 1]:
                    y_val_list.append(M_[row_, 1])
                    last_row_temp = row_
            if M_[row_, 0] >= start_bin_edge + bin_size_hours:
                last_row_temp = row_
                break
        x_binned.append(start_bin_edge + (bin_size_hours / 2))
        if len(y_val_list) >= min_bin_population:
            y_binned.append(y_val_list)
        else:
            y_binned.append([])
        start_bin_edge += bin_size_hours
        last_row = last_row_temp
    # start figure
    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)
    # add series
    if bin_size_hours >= 1:
        x_binned_int = np.array(x_binned)
    else:
        x_binned_int = x_binned
    ax.boxplot(y_binned, 0, '', whis=[5,95], positions = x_binned_int,
                       showmeans = True, widths =bin_size_hours * .9, manage_xticks=False)
    # if user selected x axes as hour
    ax.xaxis.set_ticks(np.arange(0, 24, 3))

    ax.set_xlabel(x_header)
    ax.set_ylabel(y_header)
    ax.set_title(title_str)

    if figure_filename != '':
        fig.savefig(figure_filename, transparent=True, bbox_inches='tight')
        plt.close(fig)
    else:
        plt.show()

    return fig, ax, x_binned_int, y_binned

def plot_box(filename_,x_val_index,y_val_index, bin_size=1,min_bin_population=10,y_label=None,x_label=None):
    print(filename_)
    # get data
    header_, values_, time_str = load_data_to_return_return(filename_)
    x_val_original = values_[:,x_val_index]
    y_val_original = values_[:,y_val_index]

    # get coincidences only
    x_val,y_val = coincidence(x_val_original,y_val_original)

    # start figure
    fig, ax = plt.subplots()#figsize=(16, 10))

    # combine x and y in matrix
    M_ = np.column_stack((x_val,y_val))
    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(x_val.shape[0]-1):
        if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
            if x_val[x+1] < x_val[x]:
                always_ascending = 0
    if always_ascending == 0:
        M_sorted = M_[M_[:,0].argsort()] # sort by first column
        M_ = M_sorted
    # convert data to list of bins
    y_binned = []
    x_binned = []
    start_bin_edge = np.nanmin(x_val)
    last_row = 0
    last_row_temp = last_row
    while start_bin_edge <= np.nanmax(x_val):
        y_val_list = []
        for row_ in range(last_row, M_.shape[0]):
            if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                if M_[row_, 1] == M_[row_, 1]:
                    y_val_list.append(M_[row_, 1])
                    last_row_temp = row_
            if M_[row_, 0] >= start_bin_edge + bin_size:
                last_row_temp = row_
                break
        x_binned.append(start_bin_edge)
        if len(y_val_list) >= min_bin_population:
            y_binned.append(y_val_list)
        else:
            y_binned.append([])
        start_bin_edge += bin_size
        last_row = last_row_temp
    if bin_size >= 1:
        x_binned_int = np.array(x_binned, dtype=int)
    else:
        x_binned_int = x_binned
    # add series
    ax.boxplot(y_binned, 0, '', whis=[5,95], positions = x_binned_int, showmeans = True, widths = bin_size * .9)
    # axes labels
    if x_label is not None:
        ax.set_xlabel(x_label)
    else:
        ax.set_xlabel(header_[x_val_index])
    if y_label is not None:
        ax.set_ylabel(y_label)
    else:
        ax.set_ylabel(header_[y_val_index])


    fit_line_x = np.arange(0,11,.1)
    fit_line_y =  (1.8458 * (fit_line_x ** 3)) - (1.7113 * (fit_line_x ** 2)) - (22.654 * fit_line_x) + 218.04

    ax.plot(fit_line_x,fit_line_y,'k')
    ax.yaxis.set_ticks(np.arange(0, 2800, 200))

    # for i in range(len(y_binned)):
    #     print(x_binned[i])
    #     print(np.mean(y_binned[i]))
    #     print(len(y_binned[i]))
    #     print('-' * 20)

    #
    plt.show()
def plot_box_from_values(values_x, values_y, x_label=None, y_label=None, bin_size=1, min_bin_population=10,
                         fit_function = None, fit_fuction_by='mean', log_x=False,log_y=False, title_str=None,
                         custom_y_range_tuple = None, custom_x_range_tuple = None,
                         force_start=None, force_end=None, show_means=True,
                         notch=False, sym='', whis=(5,95), figsize_=(8,5), fig_ax=None,
                         custom_x_ticks_start_end_step=None, custom_x_ticks_labels_list=None, center_boxes=False,
                         ):
    x_val_original = values_x
    y_val_original = values_y

    # get coincidences only
    x_val,y_val = coincidence(x_val_original,y_val_original)

    # start figure
    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(figsize=figsize_)


    # combine x and y in matrix
    M_ = np.column_stack((x_val,y_val))
    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(x_val.shape[0]-1):
        if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
            if x_val[x+1] < x_val[x]:
                always_ascending = 0
    if always_ascending == 0:
        M_sorted = M_[M_[:,0].argsort()] # sort by first column
        M_ = M_sorted
    # convert data to list of bins
    y_binned = []
    x_binned = []
    if force_start is None:
        start_bin_edge = np.nanmin(x_val)
    else:
        start_bin_edge = force_start
    if force_end is None:
        stop_bin = np.nanmax(x_val)
    else:
        stop_bin = force_end
    last_row = 0
    last_row_temp = last_row
    while start_bin_edge <= stop_bin:
        y_val_list = []
        for row_ in range(last_row, M_.shape[0]):
            if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                if M_[row_, 1] == M_[row_, 1]:
                    y_val_list.append(M_[row_, 1])
                    last_row_temp = row_
            if M_[row_, 0] >= start_bin_edge + bin_size:
                last_row_temp = row_
                break
        x_binned.append(start_bin_edge)
        if len(y_val_list) >= min_bin_population:
            y_binned.append(y_val_list)
        else:
            y_binned.append([])
        start_bin_edge += bin_size
        last_row = last_row_temp
    if bin_size == 1:
        x_binned_arr = np.array(x_binned, dtype=int)
    else:
        x_binned_arr = np.array(x_binned)
    # offset x array if boxes are to be plotted in the center of the bin span
    if center_boxes:
        x_binned_arr = np.array(x_binned_arr, dtype=float) + (bin_size / 2)

    # plot box
    box_dict = ax.boxplot(y_binned, notch=notch, sym=sym, whis=whis, positions=x_binned_arr,
                          showmeans=show_means, widths=bin_size * .9)

    if center_boxes:
        ax.xaxis.set_ticks(np.array(x_binned_arr, dtype=float) - (bin_size / 2))

    # axes labels
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)
    if title_str is not None:
        ax.set_title(title_str)

    if custom_x_ticks_start_end_step is not None:
        ax.xaxis.set_ticks(np.arange(custom_x_ticks_start_end_step[0], custom_x_ticks_start_end_step[1],
                                     custom_x_ticks_start_end_step[2]))
    elif custom_x_ticks_labels_list is not None:
        ax.xaxis.set_ticklabels(custom_x_ticks_labels_list)


    if fit_function is not None:
        # get mean only list
        if fit_fuction_by=='mean':
            y_s = []
            for y_bin in y_binned:
                y_s.append(np.nanmean(y_bin))
        elif fit_fuction_by=='median':
            y_s = []
            for y_bin in y_binned:
                y_s.append(np.nanmedian(y_bin))
        elif fit_fuction_by=='max':
            y_s = []
            for y_bin in y_binned:
                y_s.append(np.nanmax(y_bin))
        elif fit_fuction_by=='min':
            y_s = []
            for y_bin in y_binned:
                y_s.append(np.nanmin(y_bin))
        else:
            print('error, only possible fit_by are mean, median, max, min')
            return

        x_,y_= coincidence(x_binned_arr,y_s)

        # axes labels
        if x_label is not None:
            ax.set_xlabel(x_label)
        if y_label is not None:
            ax.set_ylabel(y_label)

        if log_x:
            ax.set_xscale("log")  # , nonposy='clip')
        if log_y:
            ax.set_yscale("log")  # , nonposy='clip')


        params = curve_fit(fit_function, x_, y_)
        print('fitted parameters')
        print('%0.3f, %0.3f' % (params[0][0], params[0][1]))

        # calculate R2
        plotting_par_list = [x_]
        params_str_ = ''
        for i_, fit_par in enumerate(params[0]):
            plotting_par_list.append(fit_par)
        funt_par = tuple(plotting_par_list)
        fit_line_y = fit_function(*funt_par)
        residuals = y_ - fit_line_y
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((y_ - np.mean(y_))**2)
        Rsqr = float(1 - (ss_res / ss_tot))
        print('R2 = %0.2f' % Rsqr)

        fit_line_x = np.arange(0,int(np.max(x_))+1,.1)
        plotting_par_list = [fit_line_x]
        for fit_par in params[0]:
            plotting_par_list.append(fit_par)
        funt_par = tuple(plotting_par_list)
        fit_line_y = fit_function(*funt_par)
        # fit_line_y =  (a_ * (fit_line_x ** 3)) + (b_ * (fit_line_x ** 2)) + (c_ * fit_line_x) + d_

        ax.plot(fit_line_x,fit_line_y,'k')
        # ax.yaxis.set_ticks(np.arange(0, 2800, 200))

        for i in range(len(x_)):
            print('%0.2f, %0.2f' % (x_[i], y_[i]))

        print('-' * 20)

    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)

    if x_binned_arr[-1] - x_binned_arr[0] > 10:
        format_xaxis_ticks(ax, '%.0f')

    plt.show()

    medians_ = []
    for i_ in box_dict['medians']:
        medians_.append(i_.get_ydata()[0])
    medians_ = np.array(medians_)

    means_ = []
    for i_ in box_dict['means']:
        means_.append(i_.get_ydata()[0])
    means_ = np.array(means_)


    return fig, ax, box_dict, x_binned_arr, medians_, means_
def plot_diurnal_multi(values_array, header_array, x_index, y_index_list,add_line=None, median_=False,
                       bin_size=1, min_bin_population=10, legend_= True, y_label='',legend_loc=(.70,.80),
                       custom_y_range_tuple=None, custom_x_range_tuple=None, lw_=2,
                       return_stats=False, print_stats=False):
    color_list = default_cm(np.linspace(0,1,len(y_index_list)))
    # stats holder
    stats_list_x = []
    stats_list_y = []
    # start figure
    fig, ax = plt.subplots()#figsize=(16, 10))
    for c_, parameter_index in enumerate(y_index_list):
        color_ = color_list[c_]
        x_val_original = values_array[:,x_index]
        y_val_original = values_array[:,parameter_index]

        # get coincidences only
        x_val,y_val = coincidence(x_val_original,y_val_original)

       # combine x and y in matrix
        M_ = np.column_stack((x_val,y_val))
        # checking if always ascending to increase efficiency
        always_ascending = 1
        for x in range(x_val.shape[0]-1):
            if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
                if x_val[x+1] < x_val[x]:
                    always_ascending = 0
        if always_ascending == 0:
            M_sorted = M_[M_[:,0].argsort()] # sort by first column
            M_ = M_sorted
        # convert data to list of bins
        y_binned = []
        x_binned = []
        start_bin_edge = np.nanmin(x_val)
        last_row = 0
        last_row_temp = last_row
        while start_bin_edge <= np.nanmax(x_val):
            y_val_list = []
            for row_ in range(last_row, M_.shape[0]):
                if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                    if M_[row_, 1] == M_[row_, 1]:
                        y_val_list.append(M_[row_, 1])
                        last_row_temp = row_
                if M_[row_, 0] >= start_bin_edge + bin_size:
                    last_row_temp = row_
                    break
            x_binned.append(start_bin_edge)
            if len(y_val_list) >= min_bin_population:
                y_binned.append(y_val_list)
            else:
                y_binned.append([])
            start_bin_edge += bin_size
            last_row = last_row_temp
        # if bin_size >= 1:
        #     x_binned_int = np.array(x_binned, dtype=int)
        # else:
        #     x_binned_int = x_binned

        # get mean only list
        y_means = []
        for y_bin in y_binned:
            if median_:
                y_means.append(np.median(y_bin))
            else:
                y_means.append(np.mean(y_bin))

        x_,y_= coincidence(np.array(x_binned),np.array(y_means))

        # store stats
        stats_list_x.append(x_)
        stats_list_y.append(y_)

        # print x and y
        if print_stats:
            print(header_array[parameter_index])
            for i in range(len(x_)):
                print(x_[i],y_[i])
            print('-' * 10)
        # add means series
        ax.plot(x_, y_, color=color_, label=header_array[parameter_index], lw=lw_)

    # axes labels
    ax.set_xlabel(header_array[x_index])
    ax.set_ylabel(y_label)
    if legend_: ax.legend(loc=legend_loc)
    ax.xaxis.set_ticks(np.arange(0, 24, 3))
    #
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)

    if add_line is not None:
        ax.plot(add_line[0], add_line[1], color='black', label=add_line[2], lw=lw_)
    #
    plt.show()

    if return_stats:
        return stats_list_x, stats_list_y
def plot_diurnal_multi_wind_direction(header_array, time_array_list, wd_ws_list_list,
                       bin_size=1, min_bin_population=10, legend_= True, y_label='', x_label='',legend_loc='best',
                       custom_y_range_tuple=None, custom_x_range_tuple=None, lw_=0, size_=5):
    color_list = default_cm(np.linspace(0,1,len(time_array_list)))
    # start figure
    fig, ax = plt.subplots()#figsize=(16, 10))
    for c_ in range(len(time_array_list)):
        color_ = color_list[c_]
        x_val_original = time_array_list[c_]
        wd_val_original = wd_ws_list_list[c_][0]
        ws_val_original = wd_ws_list_list[c_][1]

        # # get coincidences only
        # wd_val,ws_val = coincidence(wd_val_original,ws_val_original)

        North_, East_ = polar_to_cart(wd_val_original, ws_val_original)
        M_ = np.column_stack((North_,East_))

        Index_mean, Values_mean = mean_discrete(x_val_original, M_, bin_size, 0, min_data=min_bin_population)

        WD_mean, WS_mean = cart_to_polar(Values_mean[:,0], Values_mean[:,1])

        # add means series
        ax.scatter(Index_mean, WD_mean, s = size_, c=color_, label=header_array[c_], lw = lw_)

    # axes labels
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.yaxis.set_ticks(np.arange(0, 361, 45))
    if legend_: ax.legend(loc=legend_loc)
    ax.xaxis.set_ticks(np.arange(0, 24, 3))
    #
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)
    #
    plt.show()
def fit_test_1(values_x, values_y, fit_func, x_label=None, y_label=None, bin_size=1,min_bin_population=10):
    x_val_original = values_x
    y_val_original = values_y

    # get coincidences only
    x_val,y_val = coincidence(x_val_original,y_val_original)

    # start figure
    fig, ax = plt.subplots()#figsize=(16, 10))

    # combine x and y in matrix
    M_ = np.column_stack((x_val,y_val))
    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(x_val.shape[0]-1):
        if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
            if x_val[x+1] < x_val[x]:
                always_ascending = 0
    if always_ascending == 0:
        M_sorted = M_[M_[:,0].argsort()] # sort by first column
        M_ = M_sorted
    # convert data to list of bins
    y_binned = []
    x_binned = []
    start_bin_edge = np.nanmin(x_val)
    last_row = 0
    last_row_temp = last_row
    while start_bin_edge <= np.nanmax(x_val):
        y_val_list = []
        for row_ in range(last_row, M_.shape[0]):
            if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                if M_[row_, 1] == M_[row_, 1]:
                    y_val_list.append(M_[row_, 1])
                    last_row_temp = row_
            if M_[row_, 0] >= start_bin_edge + bin_size:
                last_row_temp = row_
                break
        x_binned.append(start_bin_edge)
        if len(y_val_list) >= min_bin_population:
            y_binned.append(y_val_list)
        else:
            y_binned.append([])
        start_bin_edge += bin_size
        last_row = last_row_temp
    # if bin_size >= 1:
    #     x_binned_int = np.array(x_binned, dtype=int)
    # else:
    #     x_binned_int = x_binned

    # get mean only list
    y_means = []
    for y_bin in y_binned:
        y_means.append(np.mean(y_bin))

    x_,y_= coincidence(x_binned,y_means)

    # add means series
    ax.plot(x_, y_, 'rs')

    # axes labels
    if x_label is not None:
        ax.set_xlabel(x_label)
    if y_label is not None:
        ax.set_ylabel(y_label)

    params = curve_fit(fit_func, x_, y_)
    print(params[0])

    fit_line_x = np.arange(0,int(np.max(x_))+1,.1)
    plotting_par_list = [fit_line_x]
    for fit_par in params[0]:
        plotting_par_list.append(fit_par)
    funt_par = tuple(plotting_par_list)
    fit_line_y = fit_func(*funt_par)
    # fit_line_y =  (a_ * (fit_line_x ** 3)) + (b_ * (fit_line_x ** 2)) + (c_ * fit_line_x) + d_

    ax.plot(fit_line_x,fit_line_y,'k')
    # ax.yaxis.set_ticks(np.arange(0, 2800, 200))

    for i in range(len(x_)):
        print(x_[i],y_[i])

    print('-' * 20)

    #
    plt.show()
def plot_diurnal_multi_cumulative(values_array, header_array, x_index, y_index_ordered_list, alpha_=.5,add_line=None,
                                  bin_size=1, min_bin_population=10, legend_=True, y_label='',legend_loc='best',
                                  custom_color_list=None, custom_y_range_tuple=None, custom_x_range_tuple = None):
    if custom_color_list is not None:
        color_list = custom_color_list
    else:
        color_list = default_cm(np.linspace(0,1,len(y_index_ordered_list)))

    # start figure
    fig, ax = plt.subplots()#figsize=(16, 10))
    c_, parameter_index = 0, y_index_ordered_list[0]
    color_ = color_list[c_]
    x_val_original = values_array[:,x_index]
    y_val_original = values_array[:,parameter_index]
    # get coincidences only
    x_val,y_val = coincidence(x_val_original,y_val_original)
    # combine x and y in matrix
    M_ = np.column_stack((x_val,y_val))
    # checking if always ascending to increase efficiency
    always_ascending = 1
    for x in range(x_val.shape[0]-1):
        if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
            if x_val[x+1] < x_val[x]:
                always_ascending = 0
    if always_ascending == 0:
        M_sorted = M_[M_[:,0].argsort()] # sort by first column
        M_ = M_sorted
    # convert data to list of bins
    y_binned = []
    x_binned = []
    start_bin_edge = np.nanmin(x_val)
    last_row = 0
    last_row_temp = last_row
    while start_bin_edge <= np.nanmax(x_val):
        y_val_list = []
        for row_ in range(last_row, M_.shape[0]):
            if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                if M_[row_, 1] == M_[row_, 1]:
                    y_val_list.append(M_[row_, 1])
                    last_row_temp = row_
            if M_[row_, 0] >= start_bin_edge + bin_size:
                last_row_temp = row_
                break
        x_binned.append(start_bin_edge)
        if len(y_val_list) >= min_bin_population:
            y_binned.append(y_val_list)
        else:
            y_binned.append([])
        start_bin_edge += bin_size
        last_row = last_row_temp
    # if bin_size >= 1:
    #     x_binned_int = np.array(x_binned, dtype=int)
    # else:
    #     x_binned_int = x_binned
    # get mean only list
    y_means = []
    for y_bin in y_binned:
        y_means.append(np.mean(y_bin))
    # add means series
    # ax.plot(x_, y_, color=color_, label=header_array[parameter_index])
    ax.fill_between(x_binned, y_means, color=color_, label=header_array[parameter_index])
    # ax.plot(x_binned, y_means, color=color_, label=header_array[parameter_index], lw=2)

    if len(y_index_ordered_list) > 1:
        for c_ in range(len(y_index_ordered_list[1:])):
            parameter_index = y_index_ordered_list[c_ + 1]
            color_ = color_list[c_ + 1]
            x_val_original = values_array[:,x_index]
            y_val_original = values_array[:,parameter_index]
            # get coincidences only
            x_val,y_val = coincidence(x_val_original,y_val_original)
            # combine x and y in matrix
            M_ = np.column_stack((x_val,y_val))
            # checking if always ascending to increase efficiency
            always_ascending = 1
            for x in range(x_val.shape[0]-1):
                if x_val[x]==x_val[x] and x_val[x+1]==x_val[x+1]:
                    if x_val[x+1] < x_val[x]:
                        always_ascending = 0
            if always_ascending == 0:
                M_sorted = M_[M_[:,0].argsort()] # sort by first column
                M_ = M_sorted
            # convert data to list of bins
            y_binned = []
            x_binned = []
            start_bin_edge = np.nanmin(x_val)
            last_row = 0
            last_row_temp = last_row
            while start_bin_edge <= np.nanmax(x_val):
                y_val_list = []
                for row_ in range(last_row, M_.shape[0]):
                    if start_bin_edge <= M_[row_, 0] < start_bin_edge + bin_size:
                        if M_[row_, 1] == M_[row_, 1]:
                            y_val_list.append(M_[row_, 1])
                            last_row_temp = row_
                    if M_[row_, 0] >= start_bin_edge + bin_size:
                        last_row_temp = row_
                        break
                x_binned.append(start_bin_edge)
                if len(y_val_list) >= min_bin_population:
                    y_binned.append(y_val_list)
                else:
                    y_binned.append([])
                start_bin_edge += bin_size
                last_row = last_row_temp
            # if bin_size >= 1:
            #     x_binned_int = np.array(x_binned, dtype=int)
            # else:
            #     x_binned_int = x_binned
            # get mean only list
            y_means_previous = y_means
            y_means = []
            for i_, y_bin in enumerate(y_binned):
                y_means.append(np.mean(y_bin)+y_means_previous[i_])
            # add means series
            # ax.plot(x_, y_, color=color_, label=header_array[parameter_index])
            ax.fill_between(x_binned, y_means, y_means_previous,
                            color=color_, label=header_array[parameter_index],alpha = alpha_)
            # ax.plot(x_binned, y_means, color=color_, label=header_array[parameter_index], lw=2)

    # axes labels
    ax.set_xlabel(header_array[x_index])
    ax.set_ylabel(y_label)
    if add_line is not None:
        ax.plot(add_line[0], add_line[1], color='black', label=add_line[2],lw=10)
    if legend_: ax.legend(loc=legend_loc)
    ax.xaxis.set_ticks(np.arange(0, 24, 3))
    #
    if custom_y_range_tuple is not None: ax.set_ylim(custom_y_range_tuple)
    if custom_x_range_tuple is not None: ax.set_xlim(custom_x_range_tuple)


    plt.show()


# polars
def plot_wind_rose(parameter_name,wd_,va_):
    # convert data to mean, 25pc, 75pc
    wd_off = np.array(wd_)
    for i,w in enumerate(wd_):
        if w > 360-11.25:
            wd_off [i] = w - 360 #offset wind such that north is correct
    # calculate statistical distribution per wind direction bin
    # wd_bin, ws_bin_mean, ws_bin_25, ws_bin_75
    table_ = np.column_stack((median_discrete(wd_off, va_, 22.5, 0, position_=.5)))
    # repeating last value to close lines
    table_ = np.row_stack((table_,table_[0,:]))

    # start figure
    fig, ax = plt.subplots(figsize=(16, 10), subplot_kw={'projection': 'polar'})
    # ax = plt.subplot(projection='polar')
    wd_rad = np.radians(table_[:,0])
    # format chart
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    theta_angles = np.arange(0, 360, 45)
    theta_labels = ['N', 'N-E','E','S-E', 'S', 'S-W', 'W', 'N-W']
    ax.set_thetagrids(angles=theta_angles, labels=theta_labels)
    # add series
    ax.plot(wd_rad, table_[:,1], 'ko-', linewidth=3, label = 'Median')
    ax.plot(wd_rad, table_[:,2], 'b-', linewidth=3, label = '25 percentile')
    ax.plot(wd_rad, table_[:,3], 'r-', linewidth=3, label = '75 percentile')
    ax.legend(title=parameter_name, loc=(1,.75))

    plt.show()
def plot_scatter_polar(parameter_name,WD_,Y_,C_,file_name=None, custom_y_range_tuple=(0,10), title_str ='',fig_ax=None):
    # start figure
    if fig_ax is not None:
        fig, ax = fig_ax
    else:
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

    # ax = plt.subplot(projection='polar')
    WD_rad = np.radians(WD_)
    # format chart
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    theta_angles = np.arange(0, 360, 45)
    theta_labels = ['N', 'N-E','E','S-E', 'S', 'S-W', 'W', 'N-W']
    ax.set_thetagrids(angles=theta_angles, labels=theta_labels)
    # add series
    ax.scatter(WD_rad, Y_, c = C_, s=5, lw = 0, label=parameter_name)
    # color_bar = fig.colorbar(im,fraction=0.046, pad=0.08)
    # if c_header != None: color_bar.ax.set_ylabel(c_header)
    # ax.legend(loc=(-0.1,.95))
    ax.set_ylim(custom_y_range_tuple)
    ax.set_title(title_str)

    if file_name is None:
        plt.show()
    else:
        fig.savefig(path_output + '/' + 'polar_scatter_' + file_name + '.png',transparent=True, bbox_inches='tight')
    return fig, ax

# fitting functions
def line_function(x,m,b):
    return m * x + b
def linear_1_slope(x,b):
    return x + b
def hcho_fitting_2(M, a, b, c, d, e, f):
    co = M[:,0]
    o3 = M[:,1]
    so2 = M[:,2]
    no = M[:,3]
    no2 = M[:,4]

    hcho_calc = a*co + b*o3 + c*so2 + d*no + e*no2 + f
    return hcho_calc
def hcho_fitting_1(M, a, b, c, d):
    co = M[:,0]
    o3 = M[:,1]
    so2 = M[:,2]

    hcho_calc = a*co + b*o3 + c*so2 + d
    return hcho_calc
def hcho_fitting_0(M, a, b, c, d):
    s1 = M[:,0]
    s2 = M[:,1]
    s3 = M[:,2]

    return a*s1 + b*s2 + c*s3 + d
def polynomial_function_4(x,a,b,c,d,e):
    return a*(x**4) + b*(x**3) + c*(x**2) + d*(x**1) + e
def polynomial_function_3(x,a,b,c,d):
    return a*(x**3) + b*(x**2) + c*(x**1) + d
def polynomial_function_2(x,a,b,c):
    return a*(x**2) + b*(x**1) + c
def exponential_function(x,a,b):
    return a * e_constant**(b * x)
def logarithmic_function(x,a,b):
    return a * np.log(x) + b
def exponential_with_background_function(x,a,b,c):
    return (a * e_constant**(b * x)) + c
def sigmoid_for_soiling(pm_, rh_, a_, b_):
    return pm_ / (1 + (e_constant**(a_ * (rh_ + b_))))
def sigmoid_for_soiling_mod_1(pm_, rh_, rh_slope, rh_inflexion, pm_slope, pm_inflexion):
    rh_stickiness_ratio =  pm_ / (1 + (e_constant ** (rh_slope * (rh_ + rh_inflexion))))

    residual_pm = pm_ - rh_stickiness_ratio

    pm_gravity_deposition_ratio =  residual_pm / (1 + (e_constant ** (pm_slope * (residual_pm + pm_inflexion))))

    return pm_gravity_deposition_ratio + rh_stickiness_ratio
def modified_sigmoid(rh_, pm_, a_, b_, c_, d_):
    or_ = pm_ / (1 + (e_constant**(a_ * (rh_ + b_))))
    mod_ = (or_*(1- c_)*(1-d_))+ d_

    # out_ = 100 * (mod_/pm_)

    return mod_
def modified_sigmoid_2(rh_, pm_, a_, b_, c_, d_):
    # or_ = pm_ / (1 + (e_constant**(a_ * (rh_ + b_))))
    # mod_ = (or_ * (pm_ - (pm_*c_)) / pm_) + (pm_ * c_)
    # return mod_

    sig_ratio = 1 / (1 + (e_constant**(a_ * (rh_ + b_))))
    min_scale = pm_ * c_
    max_scale = ((1-d_-c_)*pm_)/pm_

    return pm_ * sig_ratio * max_scale + min_scale
def modified_sigmoid_2_for_fitting(rh_, pm_, a_, b_, c_):
    or_ = pm_ / (1 + (e_constant**(a_ * (rh_ + b_))))

    mod_ = (or_ * (pm_ - (pm_*c_)) / pm_) + (pm_ * c_)

    return mod_
def gaussian_func(x,a,x0,sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))
def double_gaussian_func(x, a_1, x0_1, sigma_1, a_2, x0_2, sigma_2):
    y_ = (a_1 * np.exp(-(x - x0_1)**2 / (2 * sigma_1**2))) + (a_2 * np.exp(-(x - x0_2)**2 / (2 * sigma_2**2)))
    return y_
def sigmoid(x_, slope_, inflex_, max_y):
    min_y = 1 / (1 + (e_constant ** (-slope_ * (0 - inflex_))))
    sigmoid_ = (((1 / (1 + (e_constant ** (-slope_ * (x_ - inflex_))))) - min_y) / (1 - min_y)) * max_y
    return sigmoid_

def DSD_gamma_dist_1(D, N_o_star, U_o, D_o):
    N_D = N_o_star * \
          ((math.gamma(4) * ((3.67 + U_o) ** (4 + U_o))) / ((3.67 ** 4) * math.gamma(4 + U_o))) * \
          ((D / D_o) ** U_o) * \
          np.exp(-(3.67 + U_o) * (D / D_o))
    return N_D
def SR_Ze_func(Ze_,a,b):
    SR_ = ((Ze_/a))**(1/b)
    return SR_

def Ze_SR_func(SR_,a,b):
    Ze_ = a * (SR_**b)
    return Ze_
def sigmoid_mod(x_, slope_, inflex_, max_y, min_y):
    sigmoid_ = 1 / (1 + (e_constant ** (-slope_ * (x_ - inflex_))))
    return min_y + sigmoid_ * (max_y - min_y)
def sigmoid_mod_2(x_, slope_, inflex_, max_y):
    min_y = 0
    sigmoid_ = 1 / (1 + (e_constant ** (-slope_ * (x_ - inflex_))))
    return min_y + sigmoid_ * (max_y - min_y)
def power_func(x_, a, b):
    return a * x_ ** b
def reciprocal_power_asymp(x_, a, b, c):
    y_ = c - 1 / ((1 + a * x_) ** b)
    return y_
def hill_model(x_, a, b, c):
    return (a * x_ ** c) / (b ** c + x_ ** c)
def log_func(x_, a, b, c):
    return a + b * np.log(1 + c ** x_)
def gaussian_distribution(x_, mean_, std_):
    f_x = (1 / (std_ * (2 * np.pi) ** (1 / 2))) * e_constant ** (-(1 / 2) * ((x_ - mean_) / std_) ** 2)
    return f_x
def gaussian_distribution_mod(x_, mean_, std_, max_y):
    f_x = (max_y / (std_ * (2 * np.pi) ** (1 / 2))) * e_constant ** (-(1 / 2) * ((x_ - mean_) / std_) ** 2)
    return f_x
def calculate_R_2(y_real, y_model):
    y_real, y_model = coincidence(y_real, y_model)
    y_real_mean = np.mean(y_real)
    Rsqr = 1 - (np.sum((y_real - y_model) ** 2) / np.sum((y_real - y_real_mean) ** 2))
    return Rsqr

p = p_

p_plot_box = plot_box_from_values

