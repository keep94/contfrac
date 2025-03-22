import math

class _Cont(object):
  def __init__(self, r, ir, a, b):
    self._r = r
    self._ir = ir
    self._a = a
    self._b = b

  def AsTuple(self):
    return self._r, self._a, self._b

  def Flip(self):
    q = self._r - self._a * self._a
    self._b = q // self._b
    self._a = -self._a

  def Normalize(self):
    if self._b < 0:
      result = (self._a + self._ir + 1) // self._b
    else:
      result = (self._a + self._ir) // self._b
    self._a -= result * self._b
    return result

  def IsStandard(self):
    return _IsStandard(self._ir, self._a, self._b)


def _IsStandard(ir, a, b):
  if b < 0 or a >= 0:
    return False
  return b > a + ir and b <= ir - a 


def _CheckR(r):
  if type(r) != int:
    raise RuntimeError('r must be an int')
  if r < 0:
    raise RuntimeError('r must be positive')


def _CheckB(b):
  if type(b) != int:
    raise RuntimeError('b must be an int')
  if b == 0:
    raise RuntimeError('b must be non-zero')


def _CheckA(a):
  if type(a) != int:
    raise RuntimeError('a must be an int')


def Expand(r, a, b):
  _CheckR(r)
  _CheckA(a)
  _CheckB(b)
  r, a, b = _NormalizeUp(r, a, b)
  ir = int(math.sqrt(r))
  if ir * ir == r:
    raise RuntimeError('r cannot be a perfect square')
  if b > 0 and (a + ir >= b or a + ir < 0):
    raise RuntimeError('Quantity not between 0 and 1')
  if b < 0 and (a + ir < b or a + ir >= 0):
    raise RuntimeError('Quantity not between 0 and 1')
  cont = _Cont(r, ir, a, b)
  initial = []
  while not cont.IsStandard():
    cont.Flip()
    initial.append(cont.Normalize())
  repeating = []
  start = cont.AsTuple()
  cont.Flip()
  repeating.append(cont.Normalize())
  while cont.AsTuple() != start:
    cont.Flip()
    repeating.append(cont.Normalize())
  return initial, repeating


def _NormalizeUp(r, a, b):
  q = b // math.gcd(r - a*a, b)
  return r * q * q, q * a, q * b


def _GCD(r, a, b):
  q = (r - a*a) // b
  d = math.gcd(math.gcd(a, b), q)
  if d < 0:
    return -d
  return d


def _NormalizeDown(r, a, b):
  d = _GCD(r, a, b)
  return r // d // d, a // d, b // d


def Normalize(r, a, b):
  _CheckR(r)
  _CheckA(a)
  _CheckB(b)
  if (r - a*a) % b != 0:
    r, a, b = _NormalizeUp(r, a, b)
  return _NormalizeDown(r, a, b)


def Characteristic(r, a, b):
  r, a, b = Normalize(r, a, b)
  ir = int(math.sqrt(r))
  if ir * ir == r:
    return 0
  if not _IsStandard(ir, a, b):
    return 0
  return r


def AllWith(r):
  _CheckR(r)
  result = []
  root = int(math.sqrt(r))
  if root * root == r:
    return result
  for i in range(1, root+1):
    j = root - i + 1
    top = r - i*i
    while j*j < top:
      if top % j == 0 and _GCD(r, -i, j) == 1:
          result.append((r, -i, j))
          result.append((r, -i, top // j))
      j += 1
    if j*j == top and _GCD(r, -i, j) == 1:
      result.append((r, -i, j))
  return result


def AllWithReduced(r):
    m, nr = _ReduceScalar(r)
    return [_Reduce(m, nr, a, b)  for _, a, b in AllWith(r)]


def Partition(r):
  pivots = AllWith(r)
  cycles = []
  used = set()
  cont = _Cont(r, int(math.sqrt(r)), 0, 0)
  for pivot in pivots:
    if pivot in used:
      continue
    _, cont._a, cont._b = pivot
    round = []
    while pivot not in used:
      round.append(pivot)
      used.add(pivot)
      cont.Flip()
      cont.Normalize() 
      pivot = cont.AsTuple()
    cycles.append(round)
  return cycles


def PartitionReduced(r):
    m, nr = _ReduceScalar(r)
    result = []
    for part in Partition(r):
      result.append([_Reduce(m, nr, a, b)  for _, a, b in part])
    return result


def _ReduceScalar(n):
  result = 1
  idx = 2
  prod = idx*idx
  while prod <= n:
    if n % prod == 0:
      n //= prod
      result *= idx
    else:
      idx += 1
      prod = idx*idx
  return result, n


def _Reduce(m, nr, a, b):
  d = math.gcd(math.gcd(a, b), m)
  return m//d*m//d*nr, a//d, b//d
