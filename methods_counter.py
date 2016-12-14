import inspect
import importlib
import sys
import traceback
from pathlib import Path
from pprint import pprint
import matplotlib
import matplotlib.pyplot as plt

import pandas as pd


libs = [
    'pandas',
    # 'django',
    # 'flask',
    # 'matplotlib',
]


def main():
    counter = []
    total = 0
    failed = 0

    for lib in libs:
        _counter, _total, _failed = calculate(lib)
        counter += _counter
        total += _total
        failed += _failed

    pprint(counter)
    print('Toatal: {}; Failed: {}'.format(total, failed))
    analyze(counter)

def calculate(lib):
    counter = []
    total = 0
    failed = 0

    main_module = importlib.import_module(lib)
    base_dir = main_module.__spec__.submodule_search_locations[0]
    path = Path(base_dir)

    for module_path in path.glob('**/*.py'):
        total += 1
        try:
            if '__' not in module_path.name:
                package = '{}.{}'.format(lib, str(module_path)[len(base_dir)+1:-3].replace('/', '.'))
                print(package)
                if '.tests.' in package:
                    continue
                module = importlib.import_module(package)
                classes = {k: v for k, v in module.__dict__.items()
                              if isinstance(v, type) and v.__module__ == package}
                if classes:

                    print(module)
                    counter += [('{}.{}'.format(package, k), count_methods(v)) for k, v in classes.items()]

        except Exception:
            failed += 1
            traceback.print_exc()

    return counter, total, failed



def count_methods(_class):
    functions = [x for x in _class.__dict__.values() if inspect.ismethod(x) or inspect.isfunction(x)]
    # pprint(functions)
    return len(functions)

def analyze(data):
    df = pd.DataFrame(data)
    print('Quantiles')
    print(df.quantile([0, .25, 0.5, 0.75, 1]))

    df.groupby(1).count().plot()

    print('\n' + df.sort_values(by=1, ascending=False).head(10).to_string(index=False, header=False))
    plt.show()


if __name__ == '__main__':
    main()
