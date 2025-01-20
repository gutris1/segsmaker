# Stable Diffusion Webui, Forge, ReForge, ComfyUI and SwarmUI<br />for SageMaker Studio Lab, Kaggle and Google Colab
<a href="https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Fpantat88%2Fsegsmaker"><img src="https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Fpantat88%2Fsegsmaker&countColor=%232ccce4"/></a><br>
<a href="https://www.paypal.com/paypalme/gutris1"><img alt="paypal" src="https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=black"/></a>
<a href="https://ko-fi.com/gutris1"><img alt="ko-fi" src="https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=black"/></a>
<a href="https://discord.gg/k5BwmmvJJU"><img alt="Discord" src="https://img.shields.io/badge/Discrod-5865F2?style=for-the-badge&logo=discord&logoColor=black"/></a><br>


| SageMaker Studio Lab | [![Open in Studio Lab](https://studiolab.sagemaker.aws/studiolab.svg)](https://studiolab.sagemaker.aws/import/github/gutris1/segsmaker/blob/main/notebook/Segsmaker.ipynb) |
| :---------------------------------------- | :-----------------------------------------------------------------------------------------------------------------: |
| Google Colab | [![Open in Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/gutris1/segsmaker/blob/main/notebook/Segsmaker_COLAB.ipynb) |
| Kaggle | [![Open in Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/jejejojo/asdasd) |

<br />


# Changelog
### 2077-01-35
- Torch 2.5.1
- Portable Python 3.10.15 for Colab and Kaggle.
- Added $UNET and $CLIP variables %cd command for FLUX.
- Fixed Controlnet Widget buggy display in Kaggle.
- Recolor Aria2 downloader.
- Fixed scripts.

<details><summary>2025-01-10</summary><br>

- Added NGROK and ZROK tunnel for Colab and Kaggle.<br>

![1](https://github.com/user-attachments/assets/2acaf9bb-7414-4b8d-a121-1442c3a474bf)

</details>

<details><summary>2024-11-13</summary><br>

- Added SwarmUI for Colab, Kaggle and Studio Lab notebook.<br>

![Screenshot_1](https://github.com/user-attachments/assets/1b65ec70-a6d7-4a37-921d-2f5c7f71b0c3)

</details>

<details><summary>2024-11-04</summary><br>

- Notebook for colab and kaggle.
</details>

<details><summary>2024-10-05</summary><br>

- <code>[SD-Trainer](https://github.com/Akegarasu/lora-scripts)</code> webui added.<br>

![Screenshot_1](https://github.com/user-attachments/assets/055a5391-834f-4343-b0af-3c180df480dd)
</details>

<details><summary>2024-10-01</summary><br>

- ReForge and Face Fusion webui Added.

![Screenshot_1](https://github.com/user-attachments/assets/869d4277-da52-46f4-a53e-ba530a7a1df3)
</details>

<details><summary>2024-07-25</summary><br>

- Notebooks combined.
</details>

<details><summary>2024-07-10</summary><br>

- added multi Notebook Segsmaker_1+2<br /><br />
![image](https://github.com/gutris1/segsmaker/assets/132797949/1a15250b-39ad-483c-9ad2-f92023c8a3c3)
</details>

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
  <img src="https://github.com/user-attachments/assets/e5c54a3a-69b4-4835-9d4b-cf9302b15b62", width=1000px>
  <img src="https://github.com/gutris1/segsmaker/blob/main/script/preview/fastpnginfo.png", width=1000px>
  <img src="https://github.com/gutris1/segsmaker/blob/main/script/preview/cn.png", width=1000px>
</p>
