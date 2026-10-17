"""The unique-token hypothesis is essential: direct output bypass realizes OR."""
from check_bottleneck_minor import output,allowed
gates=[({0},{1})]
table=tuple(output(gates,[a,b],{0,1}) for a,b in ((0,0),(0,1),(1,0),(1,1)))
assert table==(0,1,1,1) and table not in allowed
print("PASS detected OR after forbidden direct-token output bypass")
