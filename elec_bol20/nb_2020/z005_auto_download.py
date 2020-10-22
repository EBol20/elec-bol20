# -*- coding: utf-8 -*-
# %% [markdown]
# # thanks to Joshua :)

# %%
from __future__ import print_function
from datetime import datetime, timedelta
from os import makedirs, walk
from os.path import join, dirname, abspath, sep, exists
import time
import sys
import requests
import json
import elec_bol20.util as ebu
import os
import pandas as pd


# %%
SLEEP_SECONDS_PER_LOOP = 10 * 60  # feel free to randomize this, lmao.
BASE_DIR = os.path.join(ebu.DATA_PATH0_2020, 'comp')

# %% [markdown]
# sample response to POST: {"fecha":"18/10/2020 18:53:22","correcto":true,"notificacion":"Transacción satisfactoria","datoAdicional":{"nombreArchivo":"exportacion/EG2020_20201018_184655_1350241095801193940.csv","tipoArchivo":"CSV","hash":"d41d8cd98f00b204e9800998ecf8427e","archivo":"https://s3.amazonaws.com/archivo.computo/exportacion/EG2020_20201018_184655_1350241095801193940.csv","fecha":"18/10/2020 06:46:55"}}

# %%
# sorry, i straight-up copied these while skimming my own outgoing http requests. i'm an idiot, i apologize. i know most don't matter.
POST_HEADERS = {
    'Accept': "application/json, text/plain, */*",
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,es-419;q=0.7',
    'Captcha': 'nocaptcha',
    'Content-Length': '21',
    'Content-Type': 'application/json',
    'Origin': 'https://computo.oep.org.bo',
    'Referer': 'https://computo.oep.org.bo/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0'
}
GET_HEADERS = {
    'Accept': "*/*",
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,es-419;q=0.7',
    'Connection': 'keep-alive',
    'Host': 's3.amazonaws.com',
    'Origin': 'https://computo.oep.org.bo',
    'Referer': 'https://computo.oep.org.bo/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

# %%
POST_PAYLOAD = {'tipoArchivo': "CSV"}

# %%
while True:
    r = requests.post('https://computo.oep.org.bo/api/v1/descargar',
                      headers=POST_HEADERS, json=POST_PAYLOAD)
    print("POST response => {0}".format(r))
    print("headers = {0}".format(r.headers))
    print("content = {0}".format(r.content))
    jresp = json.loads(r.content)
    real_url = jresp['datoAdicional']['archivo']
    fn = jresp['datoAdicional']['nombreArchivo']
    print("making GET request on {0}".format(real_url))

    with requests.get(real_url, headers=GET_HEADERS) as r:
        # out_path ="data\\" + fn[:fn.rindex('.')] + str(int(time.time())) + fn[fn.rindex('.'):]
        p = fn[:fn.rindex('.')] + str(int(time.time())) + fn[
                                                          fn.rindex('.'):]
        p = p.replace('/','_')
        print(f"Writing '{p}' to file.")
        out_path = os.path.join(BASE_DIR, p)
        makedirs(dirname(out_path), exist_ok=True)
        open(out_path, 'wb').write(r.content)


    pp = pd.read_csv(out_path,
                escapechar=r'"', 
                encoding='ISO-8859-1'
               )
    pp.to_csv(out_path)

    a,b = out_path.split('.')
    c = os.path.dirname(a)+'/'
    a = os.path.basename(a)
    b='.'+b
    d = os.path.join(ebu.DATA_PATH1_2020,'comp')+'/'

    s = os.path.join(ebu.DIR,'R_','scripts','z062R_fun_translator_Diego_script.R')
    import subprocess
    l = ['Rscript' ,'--vanilla' ,f'{s}', f'{a}', f'{b}', f'{c}', f'{d}']
    p = subprocess.run(l,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    print('going to sleep')
    time.sleep(SLEEP_SECONDS_PER_LOOP) # 10 min.

# %%



    

# %%
