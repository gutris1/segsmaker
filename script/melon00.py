from PIL import Image, PngImagePlugin
from pathlib import Path
import numpy as np
import hashlib
import base64
import io

class ImageEncryption:
    def __init__(self):
        self.password = '82a973c04367123ae98bd9abdf80d9eda9b910e2'
        self.tag_list = ['parameters', 'UserComment']
        self.mismatch = "axes don't match array"

    def get_range(self, i: str, o: int, r=4):
        o = o % len(i)
        return (i * 2)[o:o + r]

    def get_sha256(self, pw: str):
        return hashlib.sha256(pw.encode('utf-8')).hexdigest()

    def shuffle_array(self, a, k):
        l = len(a)
        for i in range(l):
            d = l - i - 1
            t = int(self.get_range(self.get_sha256(k), i, r=8), 16) % (l - i)
            a[d], a[t] = a[t], a[d]
        return a

    def encrypt_tag(self, m, pw):
        t = m.copy()
        for k in self.tag_list:
            if k in m:
                v = str(m[k])
                ev = base64.b64encode(''.join(chr(ord(c) ^ ord(pw[i % len(pw)])) for i, c in enumerate(v)).encode('utf-8')).decode('utf-8')
                t[k] = f'OPPAI:{ev}'
        return t

    def encrypt_image(self, img: Image.Image, pw):
        try:
            w, h = img.width, img.height
            x = np.arange(w)
            self.shuffle_array(x, pw)
            y = np.arange(h)
            self.shuffle_array(y, self.get_sha256(pw))
            a = np.array(img)
            p = a.copy()
            for v in range(h): a[v] = p[y[v]]
            a = np.transpose(a, axes=(1, 0, 2))
            p = a.copy()
            for v in range(w): a[v] = p[x[v]]
            a = np.transpose(a, axes=(1, 0, 2))
            return a
        except Exception as e:
            if self.mismatch in str(e): return np.array(img)
            raise e

    def save_image(self, b, o):
        img = Image.open(b)

        if img.format != 'PNG' or img.mode != 'RGBA':
            png_img = Image.new('RGBA', img.size)
            png_img.paste(img)
            img = png_img
            img.format = 'PNG'

        imginfo = img.info or {}
        if imginfo.get('Encrypt') == 'pixel_shuffle_3':
            img.save(o, format='PNG')
            return

        einfo = self.encrypt_tag(imginfo, self.password)

        pnginfo = PngImagePlugin.PngInfo()
        for k, v in einfo.items():
            if v: pnginfo.add_text(k, str(v))

        try:
            p = self.encrypt_image(img, self.get_sha256(self.password))
            eimg = Image.fromarray(p)
        except Exception as e:
            if self.mismatch in str(e): eimg = img
            else: raise e

        pnginfo.add_text('Encrypt', 'pixel_shuffle_3')
        pnginfo.add_text('EncryptPwdSha', self.get_sha256(f'{self.get_sha256(self.password)}Encrypt'))

        eimg.save(o, format='PNG', pnginfo=pnginfo)
        if eimg is not img: eimg.close()
        img.close()

def image_encryption(img, path):
    app = ImageEncryption()
    app.save_image(img, path)