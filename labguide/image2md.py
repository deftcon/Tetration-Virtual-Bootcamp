import os, glob
from pathlib import Path
from shutil import copy2

module = Path(os.getcwd()).parent.name
url_dict = {}

files = [file for file in glob.glob('*.png')]
files.sort(key=os.path.getmtime)

for i,file in enumerate(files):
    new_fn = f'{module}_' + str(i).zfill(3) + '.png'
    os.rename(file,new_fn)
    url_dict[i] = f'https://tetration.guru/cisco-tetration-hol/labguide/{module}/images/{new_fn}'

os.chdir('..')

if os.path.exists('README.md'):
    print("Backing up README.md")
    copy2('README.md', 'README.bak.md') 
else:
    pass

with open('README.md','w') as f:
    f.write('# Cisco Tetration - Hands-On Lab\n')
    f.write('  \n')
    f.write(f'## {module.capitalize()}\n')
    f.write('  \n')

    for key in sorted(url_dict.keys()):
        f.write(f'![Alt Text]({url_dict[key]})  \n')
        f.write('  \n')

    f.write('  \n')
    f.write('[Return to Table of Contents](https://tetration.guru/cisco-tetration-hol/labguide/)')

