import requests
import base64
import json
import numpy as np
from PIL import Image
import io
def get_skin_data(mcid):
    uuid = get_uuid(mcid)
    if uuid:
        # スキンデータのURLを取得
        skin_url = get_skin_url(uuid)
        if skin_url:
            # スキンデータをダウンロード
            return download_skin(skin_url, mcid)
        else:
            print(f'Failed to retrieve skin URL for {mcid}.')
    else:
        print(f'Failed to retrieve UUID for {mcid}.')

def get_uuid(mcid):
    url = f'https://api.mojang.com/users/profiles/minecraft/{mcid}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['id']
    else:
        print("UUIDが見つかりませんでした。")
        return None

def get_skin_url(uuid):
    url = f'https://sessionserver.mojang.com/session/minecraft/profile/{uuid}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        properties = data['properties']
        for prop in properties:
            if prop['name'] == 'textures':
                textures_data = prop['value']
                #print(textures_data)
                textures = base64.b64decode(textures_data.encode())
                textures=json.loads(textures.decode())
                return textures['textures']['SKIN']['url']
    return None

def download_skin(url, mcid):
    response = requests.get(url)
    if response.status_code == 200:
        binary_io = io.BytesIO(response.content)
        rgba_image = Image.open(binary_io).convert('RGBA')
        return rgba_image
        #with open(f'SkinData/{mcid}.png', 'wb') as skin_file:
        #    skin_file.write(response.content)
        print(f'Skin for {mcid} downloaded successfully.')
    else:
            print(f'Failed to download skin for {mcid}.')

if __name__=="__main__":
    with open("mcid-list.txt","r") as f:
        list1=f.readlines()
    list1=[x.replace("\n","") for x in list1]
    for mcid in list1:
        get_skin_data(mcid)
    
