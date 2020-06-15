import os, glob, re
from pathlib import Path
from shutil import copy2

module = Path(os.getcwd()).parent.name
url_dict = {}
stepnum_dict = {}
toc_steps_dict = {}

files = [file for file in glob.glob('*.png')]
files.sort(key=os.path.splitext)

for i,file in enumerate(files):
    new_fn = f'{module}_' + str(i).zfill(3) + '.png'
    url_dict[i] = f'https://tetration.guru/cisco-tetration-hol/labguide/{module}/images/{new_fn}'
    stepnum = str(i).zfill(3)
    stepnum_dict[i] = f'{stepnum}'

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
    f.write('  \n\n')
    f.write('### Steps for this Module')
    f.write('  \n')

    for key in sorted(url_dict.keys()):
        toc_steps_dict[i] = f.write(f'<a href="#step-{stepnum_dict[key]}" style="font-weight:bold">Step {stepnum_dict[key]}</a>')
        f.write('  \n')

    f.write('\n\n')

    for key in sorted(url_dict.keys()):
        f.write(f'<div class="step" id="step-{stepnum_dict[key]}">')
        f.write(f'<a href="#step-{stepnum_dict[key]}" style="font-weight:bold">Step {stepnum_dict[key]}</a>')
        f.write(f'</div>')
        f.write('  \n\n')
        f.write(f'<a href="{url_dict[key]}"><img src="{url_dict[key]}" style="width:100%;height:100%;"></a>  \n')
        f.write('  \n\n\n')

    f.write('  \n\n')
    module_num = re.split('[a-zA-Z]+' , module)
    module_num_int = int(module_num[1])
    next_module_num = module_num_int + 1
    next_module = 'module' + str(next_module_num).zfill(2)
    f.write(f'| [Return to Table of Contents](https://tetration.guru/cisco-tetration-hol/labguide/) | [Go to Top of the Page](https://tetration.guru/cisco-tetration-hol/labguide/{module}/) | [Continue to the Next Module](https://tetration.guru/cisco-tetration-hol/labguide/{next_module}/) |')