# uma
**uma** is a Python package to collect pyomo results as pandas dataframe for easier access.

## Installation
**uma** can be installed from PyPI using:

```
pip install uma
```
**uma** requires numpy and pandas to work.

## Usage
**uma** works if the model solution is optimal. If the solution is infeasible, an error will be returned.

```python
from uma import get_df, get_dict, get_value
from pyomo.environ import * 
from pyomo.opt import SolverFactory

model = ConcreteModel() 
model.x = Var(initialize=-1.2, bounds=(-2, 2))
model.y = Var(initialize= 1.0, bounds=(-2, 2))
model.obj = Objective( expr= (1-model.x)**2 + 100*(model.y-model.x**2)**2, sense= minimize)

solver = SolverFactory('ipopt')
solver.solve(model)

df = get_df(model)
print(df.head())

dict1 = get_dict(model)
print(dict1)

x = get_value(model.x)
print(x)
```

