import internetarchive 
from datetime import datetime
import pytz
import re
import os
import time
dir = r'YOUR_DIR'
def shorten_filename(filename):
    if len(filename) > 90:
        filename = filename[:90]
    return filename
language = 'DESIRED_LANGUAGE'
subject = 'DESIRED_SUBJECT'
results = internetarchive.search_items(f'{subject} AND mediatype:texts AND language:{language}')
for result in results:
    item = internetarchive.get_item(result['identifier'])
    pdf_file = next((file['name'] for file in item.files if file['name'].endswith('.pdf')), None)
    if pdf_file:
        print(result['identifier'])
        berlin = datetime.now(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S %Z')
        adas = shorten_filename(re.sub(r"[^\w\s]", " ", result['identifier'])).replace("\r", "").strip()
        folder_path = os.path.join(dir, adas)
        suffix = 1
        while os.path.exists(folder_path):
            folder_path = os.path.join(dir, f'{adas}({suffix})')
            suffix += 1
        os.makedirs(folder_path)
        try:
            item.get_file(pdf_file).download(os.path.join(folder_path, f'{adas}.pdf'))
        except:
            os.rmdir(folder_path)
            continue
        po = []
        for k,v in item.metadata.items():
            po.append(f'{k} : {v}')
        about = '\n'.join(po)
        with open(os.path.join(folder_path, f'{adas}.txt'), "w", encoding="utf-8") as file:
            file.write(f"Berlin time: {berlin}\n")
            file.write(about)
            