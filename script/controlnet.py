from IPython.display import display, HTML
from nenen88 import download, tempe
from IPython import get_ipython
from ipywidgets import widgets
from pathlib import Path
import os

from cn15 import controlnet_15_list
from cnxl import controlnet_xl_list

SyS = get_ipython().system
CD = os.chdir
SM = None

CSS = Path(__file__).parent / 'controlnet.css'

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

PANELS = [
    {
        'btn_class': 'btn-cn-15',
        'panel_class': 'cn-15',
        'model_list': controlnet_15_list,
        'layout': dict(display='none', flex_flow='column', width='550px', height='430px', padding='15px'),
        'btn_layout': dict(width='130px', left='104px'),
        'sel_layout': dict(width='130px', left='15px'),
        'unsel_layout': dict(width='130px', left='20px'),
        'css_classes': [
            ('checkbox_layout', 'checkbox-layout-15'),
            ('checkbox1', 'checkbox'),
            ('checkbox2', 'checkbox'),
            ('select_all_btn', 'select-all-button-15'),
            ('unselect_all_btn', 'unselect-all-button-15'),
            ('download_btn', 'download-button-15'),
            ('bottom_box', 'bottom-box-15'),
        ],
    },
    {
        'btn_class': 'btn-cn-xl',
        'panel_class': 'cn-xl',
        'model_list': controlnet_xl_list,
        'layout': dict(display='none', flex_flow='column', width='660px', height='558px', padding='15px'),
        'btn_layout': dict(left='130px'),
        'sel_layout': dict(left='30px'),
        'unsel_layout': dict(left='35px'),
        'css_classes': [
            ('checkbox_layout', 'checkbox-layout-xl'),
            ('checkbox1', 'checkbox'),
            ('checkbox2', 'checkbox'),
            ('select_all_btn', 'select-all-button-xl'),
            ('unselect_all_btn', 'unselect-all-button-xl'),
            ('download_btn', 'download-button-xl'),
            ('bottom_box', 'bottom-box-xl'),
        ],
    },
]

def _build_panel(cfg):
    model_list = cfg['model_list']

    half = len(model_list) // 2
    left_models = dict(list(model_list.items())[:half])
    right_models = dict(list(model_list.items())[half:])

    checkbox1 = widgets.VBox([widgets.Checkbox(value=False, description=name) for name in left_models])
    checkbox2 = widgets.VBox([widgets.Checkbox(value=False, description=name) for name in right_models])
    checkbox_layout = widgets.HBox([checkbox1, checkbox2])

    download_btn = widgets.Button(description='Download', layout=widgets.Layout(**cfg['btn_layout']))
    select_all_btn = widgets.Button(description='Select All', layout=widgets.Layout(**cfg['sel_layout']))
    unselect_all_btn = widgets.Button(description='Unselect All', layout=widgets.Layout(**cfg['unsel_layout']))
    bottom_box = widgets.HBox([select_all_btn, unselect_all_btn, download_btn])

    panel = widgets.Box([checkbox_layout, bottom_box], layout=widgets.Layout(**cfg['layout']))

    ns = dict(
        panel=panel,
        checkbox_layout=checkbox_layout,
        checkbox1=checkbox1,
        checkbox2=checkbox2,
        select_all_btn=select_all_btn,
        unselect_all_btn=unselect_all_btn,
        download_btn=download_btn,
        bottom_box=bottom_box,
    )

    panel.add_class(cfg['panel_class'])
    for attr, cls in cfg['css_classes']:
        ns[attr].add_class(cls)

    return {
        'cfg': cfg,
        'panel': panel,
        'checkbox1': checkbox1,
        'checkbox2': checkbox2,
        'select_all_btn': select_all_btn,
        'unselect_all_btn': unselect_all_btn,
        'download_btn': download_btn,
    }

panels = [_build_panel(cfg) for cfg in PANELS]
cn_box = {p['cfg']['btn_class']: p['panel'] for p in panels}

main_panel = widgets.HBox(layout=widgets.Layout(width='466px', height='405px'))
main_panel.add_class('cn-main-panel')

buttons = []
for p in panels:
    btn_class = p['cfg']['btn_class']
    button = widgets.Button(description='')
    button.add_class(btn_class)
    button.on_click(lambda x, bc=btn_class: Controlnet_Buttons(bc))
    buttons.append(button)

def Controlnet_Buttons(btn_class):
    main_panel.close()
    cn_box[btn_class].layout.display = 'flex'

def selection():
    for p in panels:
        if p['panel'].layout.display == 'flex':
            return p['checkbox1'].children + p['checkbox2'].children
    return []

def set_(v: bool):
    boxes = selection()
    if not v: boxes = boxes[::-1]
    for cb in boxes:
        cb.value = v

def SelectAll(b):
    set_(True)

def UnselectAll(b):
    set_(False)

def Download_Model(b):
    tempe()
    download_list = []

    for p in panels:
        pw = p['panel']
        if pw.layout.display == 'flex':
            pw.layout.display = 'none'
            l = p['cfg']['model_list']
            c = p['checkbox1'].children + p['checkbox2'].children
            for cb, k in zip(c, list(l.keys())):
                if cb.value: download_list.extend(l[k])
            break

    with output:
        CD(TMPCN)
        for url in download_list: download(url)
        CD(HOME)

def load_css():
    if SM or not Path(CSS).exists(): SyS(f'curl -sLo {CSS} https://github.com/gutris1/segsmaker/raw/main/script/controlnet.css')
    display(HTML(f'<style>{Path(CSS).read_text()}</style>'))

def cn_loaded():
    display(HTML("""
    <script>
    setTimeout(() => document.querySelector('.cn-panel')?.classList.add('loaded'), 1000);
    setTimeout(() => {
      document.querySelectorAll('[class*="btn-cn-"]').forEach(btn => {
        btn.onclick = () => {
          const panel = '.' + btn.className.match(/btn-cn-\\S+/)[1].replace('btn-', '');
          setTimeout(() => document.querySelector(panel)?.classList.add('loaded'), 1100);
        };
      });
    }, 10);
    </script>
    """))

for p in panels:
    p['select_all_btn'].on_click(SelectAll)
    p['unselect_all_btn'].on_click(UnselectAll)
    p['download_btn'].on_click(Download_Model)

load_css()
main_panel.children = buttons
cn_loaded()
display(main_panel, *[p['panel'] for p in panels], output)
