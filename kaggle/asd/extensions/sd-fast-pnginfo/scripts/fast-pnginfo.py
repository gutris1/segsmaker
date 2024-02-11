import modules.generation_parameters_copypaste as parameters_copypaste
from modules import script_callbacks
from modules import extensions
import gradio as gr
import os

def get_self_extension():
    if '__file__' in globals():
        filepath = __file__
    else:
        import inspect
        filepath = inspect.getfile(lambda: None)
    for ext in extensions.active():
        if ext.path in filepath:
            return ext

def on_ui_tabs():
    ext = get_self_extension()
    if ext is None:
        return []
    
    js_ = [f'{x.path}?{os.path.getmtime(x.path)}' for x in ext.list_files('js', '.js')]
    js_.insert(0, ext.path)
    
    with gr.Blocks(analytics_enabled=False) as fast_pnginfo:
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML(elem_id="fastpng_js_path", value='\n'.join(js_), visible=False)

        with gr.Row(equal_height=False):
            with gr.Column(variant='panel'):
                image = gr.Image(
                    elem_id="fastpnginfo_image",
                    source="upload",
                    interactive=True,
                    type="pil")

                with gr.Row(variant='compact'):
                    buttons = parameters_copypaste.create_buttons(
                        ["txt2img", "img2img", "inpaint", "extras"])
        
            with gr.Column(scale=2):
                submit = gr.Button(
                    elem_id="fastpnginfo_submit",
                    label="submit",
                    interactive=True,
                    variant="primary",
                    visible=False)
              
                with gr.Row(style={"flex": 1.5}):
                    fast_geninfo = gr.Textbox(
                        elem_id="fastpnginfo_geninfo",
                        visible=True,
                        show_label=False,
                        max_lines=16,
                        interactive=False)

                for tabname, button in buttons.items():
                    parameters_copypaste.register_paste_params_button(
                        parameters_copypaste.ParamBinding(
                        paste_button=button,
                            tabname=tabname,
                            source_text_component=fast_geninfo,
                            source_image_component=image))

        js = """
        (e) => {  
            fastpngprocess(e);
            document.querySelector("#fastpnginfo_submit").click();
            document.querySelector("#fastpnginfo_geninfo").style.visibility = "visible";
        }
        """
        image.change(fn=None, inputs=[image], _js=js, outputs=[fast_geninfo])
        
    return [(fast_pnginfo, "Fast PNG Info", "fast_pnginfo")]

script_callbacks.on_ui_tabs(on_ui_tabs)