"""Check the explicit canonical one-pair construction, not the general lower theorem."""
for m in (2,4,6,8,10):
 V={v for v in range(1<<m) if v.bit_count()%2==0}
 A=V-{0};B=V-{(1<<m)-1}
 for x in range(1<<m):
  if x.bit_count()%2==0:continue
  matches=[{v for v in V if (v>>i&1)==(x>>i&1)} for i in range(m)]
  assert all(matches)
  assert any(M<=A for M in matches) and any(M<=B for M in matches)
  assert not any(M<=A&B for M in matches)
 print('PASS canonical cover',m)
# Deliberately using A=B=V defeats no proper semifilter.
assert all(M<=V for M in matches)
assert any(M<=V&V for M in matches)
print('PASS rejected incorrect full/full pair')
