from IPython.display import display, HTML
from nenen88 import download, tempe
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import os

from cn15 import controlnet_15_list
from cnxl import controlnet_xl_list

CSSCN = Path(__file__).parent / 'controlnet.css'
SyS = get_ipython().system
CD = os.chdir
SM = None

try:
    from KANDANG import TEMPPATH, HOMEPATH
    TMPCN = Path(TEMPPATH) / 'controlnet'
    HOME = Path(HOMEPATH)
    SM = False
except ImportError:
    TMPCN = '/tmp/controlnet'
    HOME = Path.home()
    SM = True

output = widgets.Output()

options = ['btn-cn-15', 'btn-cn-xl']
buttons = []

for btn in options:
    button = widgets.Button(description='')
    button.add_class(btn.lower())
    button.on_click(lambda x, btn=btn: Controlnet_Buttons(btn))
    buttons.append(button)

cn_main_panel = widgets.HBox(layout=widgets.Layout(width='460px', height='405px'))

half_xl = len(controlnet_xl_list) // 2
left_xl = dict(list(controlnet_xl_list.items())[:half_xl])
right_xl = dict(list(controlnet_xl_list.items())[half_xl:])
checkbox1_xl = widgets.VBox([widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in left_xl], layout=widgets.Layout(left='0px'))
checkbox2_xl = widgets.VBox([widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in right_xl], layout=widgets.Layout(left='20px'))
checkbox_layout_xl = widgets.HBox([checkbox1_xl, checkbox2_xl], layout=widgets.Layout(align_items='flex-start'))
download_button_xl = widgets.Button(description='Download', layout=widgets.Layout(left='130px'))
select_all_button_xl = widgets.Button(description='Select All', layout=widgets.Layout(left='30px'))
unselect_all_button_xl = widgets.Button(description='Unselect All', layout=widgets.Layout(left='35px'))
bottom_box_xl = widgets.Button(description='', disabled=True)
button_layout_xl = widgets.HBox([select_all_button_xl, unselect_all_button_xl, download_button_xl, bottom_box_xl])
cnxl_panel = widgets.Box([button_layout_xl, checkbox_layout_xl], layout=widgets.Layout(display='none', flex_flow='column', width='660px', height='580px', padding='15px'))

half_15 = len(controlnet_15_list) // 2
left_15 = dict(list(controlnet_15_list.items())[:half_15])
right_15 = dict(list(controlnet_15_list.items())[half_15:])
checkbox1_15 = widgets.VBox([widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in left_15], layout=widgets.Layout(left='10px'))
checkbox2_15 = widgets.VBox([widgets.Checkbox(value=False, description=name, style={'description_width': '0px'}) for name in right_15], layout=widgets.Layout(left='-60px'))
checkbox_layout_15 = widgets.HBox([checkbox1_15, checkbox2_15], layout=widgets.Layout(align_items='flex-start'))
download_button_15 = widgets.Button(description='Download', layout=widgets.Layout(width='130px', left='110px'))
select_all_button_15 = widgets.Button(description='Select All', layout=widgets.Layout(width='130px', left='15px'))
unselect_all_button_15 = widgets.Button(description='Unselect All', layout=widgets.Layout(width='130px', left='20px'))
bottom_box_15 = widgets.Button(description='', disabled=True)
button_layout_15 = widgets.HBox([select_all_button_15, unselect_all_button_15, download_button_15, bottom_box_15])
cn15_panel = widgets.Box([button_layout_15, checkbox_layout_15], layout=widgets.Layout(display='none', flex_flow='column', width='550px', height='490px', padding='15px'))

cn_main_panel.add_class('cn-panel')

cn15_panel.add_class('cn-15')
checkbox_layout_15.add_class('checkbox_layout_15')
checkbox1_15.add_class('checkbox')
checkbox2_15.add_class('checkbox')
select_all_button_15.add_class('select-all-button-15')
unselect_all_button_15.add_class('unselect-all-button-15')
download_button_15.add_class('download-button-15')
bottom_box_15.add_class('bottom-box-15')

cnxl_panel.add_class('cn-xl')
checkbox_layout_xl.add_class('checkbox_layout_xl')
checkbox1_xl.add_class('checkbox')
checkbox2_xl.add_class('checkbox')
select_all_button_xl.add_class('select-all-button-xl')
unselect_all_button_xl.add_class('unselect-all-button-xl')
download_button_xl.add_class('download-button-xl')
bottom_box_xl.add_class('bottom-box-xl')

def Controlnet_Buttons(btn):
    cn_main_panel.close()
    if btn == 'btn-cn-15': cn15_panel.layout.display = 'flex'
    elif btn == 'btn-cn-xl': cnxl_panel.layout.display = 'flex'

def SelectAll(b):
    if cn15_panel.layout.display == 'flex':
        for check in checkbox1_15.children + checkbox2_15.children: check.value = True
    elif cnxl_panel.layout.display == 'flex':
        for check in checkbox1_xl.children + checkbox2_xl.children: check.value = True

def UnselectAll(b):
    if cn15_panel.layout.display == 'flex':
        for check in checkbox1_15.children + checkbox2_15.children: check.value = False
    elif cnxl_panel.layout.display == 'flex':
        for check in checkbox1_xl.children + checkbox2_xl.children: check.value = False

def Download_Model(b):
    cn15_panel.close()
    cnxl_panel.close()
    tempe()

    download_list = []

    if cn15_panel.layout.display == 'flex':
        cn15_panel.layout.display = 'none'
        for check, key in zip(checkbox1_15.children + checkbox2_15.children, list(controlnet_15_list.keys())):
            if check.value: download_list.extend(controlnet_15_list[key])

    elif cnxl_panel.layout.display == 'flex':
        cnxl_panel.layout.display = 'none'
        for check, key in zip(checkbox1_xl.children + checkbox2_xl.children, list(controlnet_xl_list.keys())):
            if check.value: download_list.extend(controlnet_xl_list[key])

    with output:
        CD(TMPCN)
        for url in download_list: download(url)
        CD(HOME)

def load_css():
    if SM or not Path(CSSCN).exists(): SyS(f'curl -sLo {CSSCN} https://github.com/gutris1/segsmaker/raw/main/script/controlnet.css')
    display(HTML(f'<style>{Path(CSSCN).read_text()}</style>'))

load_css()
cn_main_panel.children = buttons
display(cn_main_panel, cn15_panel, cnxl_panel, output)

select_all_button_15.on_click(SelectAll)
unselect_all_button_15.on_click(UnselectAll)
download_button_15.on_click(Download_Model)
select_all_button_xl.on_click(SelectAll)
unselect_all_button_xl.on_click(UnselectAll)
download_button_xl.on_click(Download_Model)
