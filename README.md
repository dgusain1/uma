# uma

[![CI](https://github.com/dgusain1/uma/actions/workflows/ci.yml/badge.svg)](https://github.com/dgusain1/uma/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/uma)](https://pypi.org/project/uma/)

**uma** collects [Pyomo](https://www.pyomo.org/) results as pandas DataFrames, dictionaries and NumPy arrays for easier access.

## Installation

```
pip install uma
```

Requires Python 3.9+, `numpy>=1.22`, `pandas>=1.5` and `pyomo>=6.4` (installed automatically).

> **Upgrading from 1.x:** the functions were renamed (`get_df` -> `get_results_df`, `get_dict` -> `get_results_dict`, `get_value` -> `get_results_array`). The old names still work but emit a `DeprecationWarning`.
>
> `get_results_df` also now keys rows by each variable's Pyomo index instead of position, so variables with different index sets are no longer stacked from row 0.

## Usage

Call these after solving your model. Variables that have no value are returned as `NaN`.

- `get_results_df(model)`: DataFrame with one column per variable and one row per Pyomo index. Variables over different index sets are aligned on their keys (`NaN` where a key doesn't exist for a variable). Scalar variables use the row key `None`.
- `get_results_dict(model)`: `{variable name: np.ndarray}`.
- `get_results_array(var)`: `np.ndarray` for a single variable.

By default only variables on active blocks are included; pass `active=False` to include deactivated blocks too.

```python
import pyomo.environ as pyo
from uma import get_results_df, get_results_dict, get_results_array

model = pyo.ConcreteModel()
model.x = pyo.Var(initialize=-1.2, bounds=(-2, 2))
model.y = pyo.Var(initialize=1.0, bounds=(-2, 2))
model.obj = pyo.Objective(
    expr=(1 - model.x) ** 2 + 100 * (model.y - model.x**2) ** 2, sense=pyo.minimize
)

pyo.SolverFactory("ipopt").solve(model)

res_df = get_results_df(model)       # DataFrame, rows keyed by Pyomo index
res = get_results_dict(model)        # {variable name: np.ndarray}
x = get_results_array(model.x)       # np.ndarray for a single variable
```

For tuple-indexed variables, select the column first: `res_df["z"][("a", 2)]`. pandas reads `res_df.loc[("a", 2), "z"]` as (row, column) and fails.

## Development

```
pip install -e ".[test]"
pytest
```

## License

MIT
