import random
from typing import TypeVar, Callable, Tuple, List

from heare.histograms import Histogram

RetVal = TypeVar('RetVal')


def generate_test_histogram(size: int, type_var: Callable[[], RetVal]) -> Tuple[Histogram[RetVal], List[RetVal]]:
    randfunc = random.random
    data: List[RetVal] = []
    hist: Histogram[RetVal] = Histogram[RetVal](max_size=size)
    if type_var == int:
        randfunc = lambda: random.randint(0, size * 10)

    for _ in range(size):
        v = randfunc()
        data.append(v)
        hist.observe(v)

    return hist, data