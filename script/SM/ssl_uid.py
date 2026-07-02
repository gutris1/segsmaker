from pathlib import Path

HOME = Path.home()
TMP = Path('/tmp')

URL = {
    'D': [
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-Torch2120-cu130-part1.tar.lz4',
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-Torch2120-cu130-part2.tar.lz4'
    ],

    'FC': 'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FC-Python311-Torch260-cu124.tar.lz4',

    'FN': [
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FN-Torch2121-cu130-part1.tar.lz4',
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-FN-Torch2121-cu130-part2.tar.lz4'
    ],

    'CS': [
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-CS-Torch2121-cu130-part1.tar.lz4',
        'https://huggingface.co/gutris1/webui/resolve/main/env/SSL-CS-Torch2121-cu130-part2.tar.lz4'
    ],
}

UID = {
    'A1111': {
        'repo': 'https://github.com/gutris1/A1111',
        'branch': 'master',

        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet')
        ],

        'env': TMP / 'venv',
        'url': URL['D'],

        'title': 'A1111',
        'args': '--xformers',
        'cpu': '--use-cpu all --precision full --no-half --skip-torch-cuda-test',
    },

    'Forge': {
        'repo': 'https://github.com/lllyasviel/stable-diffusion-webui-forge Forge',
        'branch': 'main',

        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
            f"rm -rf {M / 'svd'} {M / 'z123'} {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'}",
            f"rm -rf {M / 'diffusion_models'} {M / 'text_encoder'} {M / 'unet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet'),
            (TMP / 'z123', M / 'z123'),
            (TMP / 'svd', M / 'svd'),
            (TMP / 'clip', M / 'clip'),
            (TMP / 'clip_vision', M / 'clip_vision'),
            (TMP / 'diffusers', M / 'diffusers'),
            (TMP / 'diffusion_models', M / 'diffusion_models'),
            (TMP / 'text_encoders', M / 'text_encoder'),
            (TMP / 'unet', M / 'unet')
        ],

        'env': TMP / 'venv',
        'url': URL['D'],

        'title': 'Forge',
        'args': '--disable-xformers --opt-sdp-attention --cuda-stream',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'ReForge': {
        'repo': 'https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge',
        'branch': 'main',

        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}",
            f"rm -rf {M / 'svd'} {M / 'z123'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet'),
            (TMP / 'z123', M / 'z123'),
            (TMP / 'svd', M / 'svd')
        ],

        'env': TMP / 'venv',
        'url': URL['D'],

        'title': 'ReForge',
        'args': '--xformers --cuda-stream',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'ReForge-old': {
        'repo': '-b main-old https://github.com/Panchovix/stable-diffusion-webui-reForge ReForge-old',
        'branch': 'main-old',

        'env': TMP / 'venv',
        'url': URL['D'],

        'title': 'ReForge old',
        'args': '--xformers --cuda-stream',
        'cpu': '--always-cpu --skip-torch-cuda-test',
    },

    'Forge-Classic': {
        'repo': '-b classic https://github.com/Haoming02/sd-webui-forge-classic Forge-Classic',
        'branch': 'classic',

        'sym': lambda M: [
            f"rm -rf {M / 'Stable-diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'ControlNet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'ControlNet')
        ],

        'env': TMP / 'python311',
        'url': URL['FC'],

        'title': 'Forge Classic',
        'args': '--xformers --cuda-stream --persistent-patches',
        'cpu': '--always-cpu --skip-torch-cuda-test',
        'ld': True,
    },

    'Forge-Neo': {
        'repo': '-b neo https://github.com/Haoming02/sd-webui-forge-classic Forge-Neo',
        'branch': 'neo',

        'env': TMP / 'NEO',
        'url': URL['FN'],

        'title': 'Forge Neo',
        'args': '--xformers --cuda-stream',
        'cpu': '--cpu --skip-torch-cuda-test',
        'ld': True,
        'cm': True,
    },

    'ComfyUI': {
        'repo': 'https://github.com/comfyanonymous/ComfyUI',
        'branch': 'master',

        'sym': lambda M: [
            f"rm -rf {M / 'checkpoints/tmp_ckpt'} {M / 'loras/tmp_lora'} {M / 'controlnet'}",
            f"rm -rf {M / 'clip'} {M / 'clip_vision'} {M / 'diffusers'} {M / 'diffusion_models'}",
            f"rm -rf {M / 'text_encoders'} {M / 'unet'}"
        ],
        'links': lambda M: [
            (M / 'checkpoints', M / 'checkpoints_symlink'),
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'checkpoints/tmp_ckpt'),
            (TMP / 'lora', M / 'loras/tmp_lora'),
            (TMP / 'controlnet', M / 'controlnet'),
            (TMP / 'clip', M / 'clip'),
            (TMP / 'clip_vision', M / 'clip_vision'),
            (TMP / 'diffusers', M / 'diffusers'),
            (TMP / 'diffusion_models', M / 'diffusion_models'),
            (TMP / 'text_encoders', M / 'text_encoders'),
            (TMP / 'unet', M / 'unet')
        ],

        'env': TMP / 'Comfy-Swarm',
        'url': URL['CS'],

        'title': 'ComfyUI',
        'args': '--dont-print-server --use-pytorch-cross-attention',
        'port': 8188,
        'cpu': '--cpu',
    },

    'SwarmUI': {
        'repo': 'https://github.com/mcmonkeyprojects/SwarmUI',
        'branch': 'master',

        'sym': lambda M: [
            f"rm -rf {M / 'Stable-Diffusion/tmp_ckpt'} {M / 'Lora/tmp_lora'} {M / 'controlnet'}",
            f"rm -rf {M / 'clip'} {M / 'unet'}"
        ],
        'links': lambda M: [
            (TMP, HOME / 'tmp'),
            (TMP / 'ckpt', M / 'Stable-Diffusion/tmp_ckpt'),
            (TMP / 'lora', M / 'Lora/tmp_lora'),
            (TMP / 'controlnet', M / 'controlnet'),
            (TMP / 'clip', M / 'clip'),
            (TMP / 'unet', M / 'unet')
        ],

        'env': TMP / 'Comfy-Swarm',
        'url': URL['CS'],

        'title': 'SwarmUI',
        'args': '--launch_mode none',
        'port': 7801,
        'var': {'SWARMPATH': lambda: str(Path.cwd()), 'SWARM_NO_VENV': 'true'},
    },
}
