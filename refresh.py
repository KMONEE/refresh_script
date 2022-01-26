import pandas as pd
import numpy as np
import json
import cloudscraper
import time
import ast
import dropbox

#dropbox token
dbx = dropbox.Dropbox('')


def scrape_new(collection_address, csv_name):
    scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'android',
        'desktop': False
        }
    )
    #scraper = cloudscraper.create_scraper()
    counter = 0
    while counter != 1:
        try:
            max_page = json.loads(scraper.get(f"https://randomearth.io/api/items?collection_addr={collection_address}&page=99999").text)['pages']
            counter += 1
        except Exception as e:
            time.sleep(3)
            pass

    for page in range(1, max_page+1):
        counter = 0
        while counter != 1:
            try:
                page_data = scraper.get(f"https://randomearth.io/api/items?collection_addr={collection_address}&page={page}").text
                

                final_df = pd.concat([pd.read_csv(f'{csv_name}.csv'), pd.DataFrame.from_dict(json.loads(page_data)['items'])])
                final_df.to_csv(f'{csv_name}.csv', index=False)
                time.sleep(.30) #yeah yeah it's not efficient, sue me!
                counter += 1
                
            except Exception as e:
                print(page)
                time.sleep(3)
                pass

collections = {
    'terra1k0y373yxqne22pc9g7jvnr4qclpsxtafevtrpg':'egg_nfts',
    'terra1vhuyuwwr4rkdpez5f5lmuqavut28h5dt29rpn6':'nested_egg_nfts',
    'terra14gfnxnwl0yz6njzet4n33erq5n70wt79nm24el':'loot_nfts',
    'terra1chrdxaef0y2feynkpq63mve0sqeg09acjnp55v':'meteor_nfts',
    'terra1p70x7jkqhf37qa7qm4v23g4u4g8ka4ktxudxa7':'meteor_dust_nfts'
    }


for address, file_name in collections.items():
    print(f'starting {file_name}')
    new_df = pd.read_csv('headers.csv')
    new_df.to_csv(f'{file_name}.csv', index=False)
    scrape_new(address, file_name)
    
    dbx.files_delete_v2(fr'/Levana/{file_name}.csv')
    with open(f'{file_name}.csv', "rb") as f:
        dbx.files_upload(f.read(), fr'/Levana/{file_name}.csv', mute = True)
    
    print(f'Done with {file_name}')

