"""One call that fixes every random number generator we use.

numpy and torch are optional: the generation environment (requirements-generation.txt)
has neither, so they are seeded only when installed.
"""

from __future__ import annotations

import os
import random


def set_seed(seed: int, deterministic: bool = False) -> int:
    """Seed random, numpy and torch (CPU and GPU). Returns the seed so it can be logged."""
    os.environ["PYTHONHASHSEED"] = str(seed)
    random.seed(seed)

    try:
        import numpy as np
        np.random.seed(seed)
    except ImportError:
        pass

    try:
        import torch
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        if deterministic:
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
    except ImportError:
        pass

    return seed