# Stable Diffusion Webui, Forge and ComfyUI notebook<br />for SageMaker Studio Lab
[<img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fpantat88%2Fsegsmaker&label=Visitors&countColor=%232ccce4&style=flat">](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Fpantat88%2Fsegsmaker)<br>[<img src="https://img.shields.io/badge/Support%20me%20on%20Ko--fi-F16061?logo=ko-fi&logoColor=white&style=flat">](https://ko-fi.com/gutris1)

| SD | [![Open in Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/gutris1/segsmaker/blob/main/Segsmaker.ipynb) |
| :---------------------------------------- | :-----------------------------------------------------------------------------------------------------------------: |
| SD Forge | [![Open in Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/gutris1/segsmaker/blob/main/Segsmaker_Forge.ipynb) |
| ComfyUI | [![Open in Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/gutris1/segsmaker/blob/main/Segsmaker_ComfyUI.ipynb) |
<br />

you can find me here https://discord.gg/k5BwmmvJJU <br /><br />
![image](https://github.com/gutris1/segsmaker/assets/132797949/670da491-58f7-4fc0-b5ef-b2cde93f79bf)


# Changelog

<details><summary>2024-06-24</summary><br>

- Improved Notebook.
- Save all your things from there and Please NUKE☢️ your current environment with command below, before using new Notebook with venv.
```python
!rm -rf ~
```
- Old Notebooks won't work anymore.
- PINGGY and ZROK URLs will be printed after the local URL.
</details>

<details><summary>2024-05-29</summary><br>
  
- Fixed Conda Installation.
</details>

<details><summary>2024-05-18</summary><br>

- Upgraded Torch to version 2.2.0+cu121.
- Added Pinggy tunnel.
- Removed Segsmaker animatediff notebook.
</details>

<details><summary>2024-04-17</summary><br>

- Updated AUTO1111 SD Webui to 1.9.3
- Removed [batchlinks-webui](https://github.com/etherealxx/batchlinks-webui) from pre-install extension list.
- Removed [Stable-Diffusion-Webui-Civitai-Helper](https://github.com/zixaphir/Stable-Diffusion-Webui-Civitai-Helper) from pre-install extension list.
- Added [sd-hub](https://github.com/gutris1/sd-hub) to pre-install extension list.
- Added [sd-civitai-browser-plus](https://github.com/BlafKing/sd-civitai-browser-plus) to pre-install extension list.
</details>

<details><summary>2024-03-11</summary><br>

- Minor changes, SDXL notebook removed.
- Select either SD 1.5 or SDXL for installation in Segsmaker.ipynb and Segsmaker_Forge.ipynb using the widget.
</details>

<details><summary>2024-03-02</summary><br>

- Add notebook for [SD Forge](https://github.com/lllyasviel/stable-diffusion-webui-forge)
- Update AUTO1111 SD Webui to 1.8.0.
- Update Conda script to install Torch 2.1.2+cu121.
</details>

<details><summary>2024-02-09</summary><br>

- Switch to aria2 for civitai.com downloads.
- Add gdown for Google Drive downloads. For Google Drive file or folder, simply paste the public URL directly.
- Else default to Curl.

Usage:
```python
# only url
%download URL

# url and filename
%download URL 123456.safetensors

# url and path
%download URL ~/asd/models/asdasd

# url path and filename
%download URL ~/asd/models/zzzzzz 789789.txt
```
</details>

<details><summary>2024-02-07</summary><br>

- For the safety of all of us, especially my account, from now on please enter your own API key by rerunning the Conda cell. <br />
  <img src="https://github.com/gutris1/segsmaker/assets/132797949/7420b6ff-7080-46f2-bd20-cd2088d64ff6" width="486" height="169">
- Get your own API key at https://civitai.com/user/account click the 'Add API Key' button, give it a name and then copy. <br />
  <img src="https://github.com/gutris1/segsmaker/assets/132797949/d3fa05b6-4cdd-4ffc-9a50-43bf550de627" width="367" height="169">
- Don't worry, you only need to do that once. next time you reinstall Conda, you will not be prompted again.
</details>

# Preview
<p align="center">
  <img src="https://github.com/gutris1/segsmaker/assets/132797949/4ecc8360-a3ba-4564-8acc-64638acb3e35", widht=1000px>
  <img src="https://github.com/gutris1/segsmaker/assets/132797949/e19cc982-67ea-447f-a505-4efc932c822a", widht=1000px>
  <img src="https://github.com/gutris1/segsmaker/blob/main/pre/fastpnginfo.png", widht=1000px>
  <img src="https://github.com/gutris1/segsmaker/blob/main/pre/cn.png", widht=1000px>
</p>
