from pathlib import Path

HOME = Path.home()
SRC = ''
TMP = Path('/tmp')

H = 'https://huggingface.co/gutris1/webui/resolve/main/env'

PY = {
    'D': {
        'v': '3.10.20',
        'p': TMP / 'PY-310',
        'url': [
            f'{H}/PY310-Torch2121-cu130-1.tar.lz4',
            f'{H}/PY310-Torch2121-cu130-2.tar.lz4'
        ],
    },

    'RF': {
        'v': '3.12.13',
        'p': TMP / 'R-F',
        'url': [
            f'{H}/RF-Torch2121-cu130-1.tar.lz4',
            f'{H}/RF-Torch2121-cu130-2.tar.lz4'
        ],
    },

    'FC': {
        'v': '3.11.15',
        'p': TMP / 'CLASSIC',
        'url': [
            f'{H}/FC-Torch2121-cu130-1.tar.lz4',
            f'{H}/FC-Torch2121-cu130-2.tar.lz4'
        ],
    },

    'FN': {
        'v': '3.13.12',
        'p': TMP / 'NEO',
        'url': [
            f'{H}/FN-Torch2121-cu130-1.tar.lz4',
            f'{H}/FN-Torch2121-cu130-2.tar.lz4'
        ],
    },

    'CS': {
        'v': '3.12.13',
        'p': TMP / 'Comfy-Swarm',
        'url': [
            f'{H}/CS-Torch2121-cu130-1.tar.lz4',
            f'{H}/CS-Torch2121-cu130-2.tar.lz4'
        ],
    },
}

UID = {
    'A1111': {
        'repo': 'https://github.com/gutris1/A1111',
        'branch': 'master',

        'sym': lambda M: ['rm -rf ' + ' '.join(str(M / t) for _, t in LINKS['A1111'])],
        'links': lambda M: ((TMP / p, M / t) for p, t in LINKS['A1111']),

        'py': PY['D'],

        'title': 'A1111',
        'args': '--xformers',
        'cpu': '--use-cpu all --precision full --no-half --skip-torch-cuda-test',
    },

    'Forge': {
        'repo': 'https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
        'branch': 'main',

        'sym': lambda M: ['rm -rf ' + ' '.join(str(M / t) for _, t in LINKS['Forge'])],
        'links': lambda M: ((TMP / p, M / t) for p, t in LINKS['Forge']),

        'py': PY['D'],

        'title': 'Forge',
        'args': '--disable-xformers --opt-sdp-attention --cuda-stream',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'ReForge-old': {
        'repo': '-b main-old https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge-old',
        'branch': 'main-old',

        'py': PY['D'],

        'title': 'ReForge old',
        'args': '--xformers --cuda-stream',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'ReForge': {
        'repo': 'https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
        'branch': 'main',

        'sym': lambda M: ['rm -rf ' + ' '.join(str(M / t) for _, t in LINKS['ReForge'])],
        'links': lambda M: ((TMP / p, M / t) for p, t in LINKS['ReForge']),

        'py': PY['RF'],

        'title': 'ReForge',
        'args': '--xformers --cuda-stream',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'Forge-Classic': {
        'repo': '-b classic https://github.com/Haoming02/sd-webui-forge-classic Forge-Classic',
        'branch': 'classic',

        'sym': lambda M: ['rm -rf ' + ' '.join(str(M / t) for _, t in LINKS['Forge-Classic'])],
        'links': lambda M: ((TMP / p, M / t) for p, t in LINKS['Forge-Classic']),

        'py': PY['FC'],

        'title': 'Forge Classic',
        'args': '--xformers --cuda-stream --persistent-patches',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'Forge-Neo': {
        'repo': '-b neo https://github.com/Haoming02/sd-webui-forge-classic Forge-Neo',
        'branch': 'neo',

        'py': PY['FN'],

        'title': 'Forge Neo',
        'args': '--xformers --cuda-stream',
        'cpu': '--cpu --skip-torch-cuda-test',
        'cm': True,
    },

    'ComfyUI': {
        'repo': 'https://github.com/comfyanonymous/ComfyUI',
        'branch': 'master',

        'sym': lambda M: ['rm -rf ' + ' '.join(str(M / t) for _, t in LINKS['ComfyUI'])],
        'links': lambda M: [
            (M / 'checkpoints', M / 'checkpoints_symlink'),
            *((TMP / p, M / t) for p, t in LINKS['ComfyUI']),
        ],

        'py': PY['CS'],

        'title': 'ComfyUI',
        'args': '--dont-print-server --use-pytorch-cross-attention',
        'port': 8188,
        'cpu': '--cpu',
    },

    'SwarmUI': {
        'repo': 'https://github.com/mcmonkeyprojects/SwarmUI',
        'branch': 'master',

        'sym': lambda M: ['rm -rf ' + ' '.join(str(M / t) for _, t in LINKS['SwarmUI'])],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            *((TMP / p, M / t) for p, t in LINKS['SwarmUI']),
        ],

        'py': PY['CS'],

        'title': 'SwarmUI',
        'args': '--launch_mode none',
        'port': 7801,
        'var': {'SWARMPATH': lambda: str(Path.cwd()), 'SWARM_NO_VENV': 'true'},
    },
}

LINKS = {
    'A1111': (
        ('ckpt', 'Stable-diffusion/tmp_ckpt'),
        ('lora', 'Lora/tmp_lora'),
        ('controlnet', 'ControlNet'),
    ),

    'Forge': (
        ('ckpt', 'Stable-diffusion/tmp_ckpt'),
        ('lora', 'Lora/tmp_lora'),
        ('controlnet', 'ControlNet'),
        ('z123', 'z123'),
        ('svd', 'svd'),
        ('clip', 'clip'),
        ('clip_vision', 'clip_vision'),
        ('diffusers', 'diffusers'),
        ('diffusion_models', 'diffusion_models'),
        ('unet', 'unet'),
    ),

    'ReForge': (
        ('ckpt', 'Stable-diffusion/tmp_ckpt'),
        ('lora', 'Lora/tmp_lora'),
        ('controlnet', 'ControlNet'),
        ('z123', 'z123'),
        ('svd', 'svd'),
    ),

    'Forge-Classic': (
        ('ckpt', 'Stable-diffusion/tmp_ckpt'),
        ('lora', 'Lora/tmp_lora'),
        ('controlnet', 'ControlNet'),
    ),

    'ComfyUI': (
        ('ckpt', 'checkpoints/tmp_ckpt'),
        ('lora', 'loras/tmp_lora'),
        ('controlnet', 'controlnet'),
        ('clip', 'clip'),
        ('clip_vision', 'clip_vision'),
        ('diffusers', 'diffusers'),
        ('diffusion_models', 'diffusion_models'),
        ('unet', 'unet'),
    ),

    'SwarmUI': (
        ('ckpt', 'Stable-Diffusion/tmp_ckpt'),
        ('lora', 'Lora/tmp_lora'),
        ('controlnet', 'controlnet'),
        ('clip', 'clip'),
        ('unet', 'unet'),
    ),
}
