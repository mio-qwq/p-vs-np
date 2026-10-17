"""Residual UNSAT certificates; frozen normalizer is part of the specification.

JSON FALSE token is null. Integer references address local-coordinate node keys.
This is not an EF/SF proof emitter or an independently implemented normalizer.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys

SOLVER = Path(os.environ.get('ARB_PC_SOURCE',
    str(Path(__file__).resolve().parents[1] / 'affine-residual-pc/design/arb_pc.py')))
FROZEN_SHA256 = '32ba57a17c8af1fc1045314fd89b849743bd6ba810fdfdb96f3a4ac9cde577c5'
_source = SOLVER.read_bytes()
if hashlib.sha256(_source).hexdigest() != FROZEN_SHA256:
    raise RuntimeError('Frozen solver source hash has changed')
spec = importlib.util.spec_from_file_location('frozen_arb_pc_certificate', SOLVER)
frozen = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = frozen
# Execute verified source directly: never create bytecode beside frozen solver.
exec(compile(_source, str(SOLVER), 'exec'), frozen.__dict__)

class InvalidCertificate(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidCertificate(message)


def preprocess(cnf, n=None):
    require(type(cnf) in (list, tuple), 'CNF must be an array')
    require(all(type(c) in (list, tuple) for c in cnf), 'clauses must be arrays')
    require(all(type(x) is int and x != 0 for c in cnf for x in c), 'nonzero integer literals required')
    names = sorted({abs(x) for c in cnf for x in c})
    if n is not None:
        require(type(n) is int and n >= max(names, default=0), 'invalid input dimension')
    # Crucially no shifts indexed by original labels precede this dense map.
    mapping = {v: i + 1 for i, v in enumerate(names)}
    dense = tuple(tuple(mapping[abs(x)] if x > 0 else -mapping[abs(x)] for x in c) for c in cnf)
    expanded, dim = frozen.to_3cnf(dense, len(names))
    clauses, equations, _ = frozen.extract_parity(expanded)
    return clauses, dim, equations


def generate(cnf, n=None):
    """Return an UNSAT certificate, or None if SAT. Iterative exact search replay."""
    clauses, dim, equations = preprocess(cnf, n)
    memo, nodes, stack = {}, [], []
    work = (clauses, dim, equations)
    while True:
        if work is not None:
            cs, d, eq = work
            work = None
            key = frozen.normalize(cs, d, eq)
            if key is True or key is False:
                answer, ref = key, None
            elif key in memo:
                answer, ref = memo[key]
            else:
                d, cs = key
                components = frozen.split_components(key)
                if len(components) > 1:
                    kind = 'component'
                    tasks = [(pc, pd, ()) for pd, pc in components]
                else:
                    kind = 'branch'
                    mask, const = cs[0][0]
                    tasks = [(cs, d, ((mask, const),)), (cs, d, ((mask, const ^ 1),))]
                stack.append({'key': key, 'kind': kind, 'tasks': tasks, 'next': 1, 'refs': []})
                work = tasks[0]
                continue
        if not stack:
            if answer:
                return None
            # Drop irrelevant UNSAT nodes visited during a SAT component proof.
            reachable, todo = set(), [ref]
            while todo:
                r = todo.pop()
                if r is None or r in reachable:
                    continue
                reachable.add(r)
                nd = nodes[r]
                todo.extend(nd['children'] if nd['kind'] == 'branch' else [nd['child']])
            order = sorted(reachable)
            rename = {old: new for new, old in enumerate(order)}
            def remap(r): return None if r is None else rename[r]
            kept = []
            for old in order:
                nd = nodes[old].copy()
                if nd['kind'] == 'branch': nd['children'] = [remap(r) for r in nd['children']]
                else: nd['child'] = remap(nd['child'])
                kept.append(nd)
            return {'version': 1, 'solver_sha256': FROZEN_SHA256, 'root': remap(ref), 'nodes': kept}
        f = stack[-1]
        f['refs'].append(ref)
        short = (f['kind'] == 'branch' and answer) or (f['kind'] == 'component' and not answer)
        if not short and f['next'] < len(f['tasks']):
            work = f['tasks'][f['next']]
            f['next'] += 1
            continue
        stack.pop()
        ref = None
        if not answer:
            d, cs = f['key']
            nd = {'dimension': d, 'clauses': [[list(lit) for lit in c] for c in cs], 'kind': f['kind']}
            if f['kind'] == 'branch':
                nd.update(query=list(cs[0][0]), children=f['refs'])
            else:
                nd.update(index=f['next'] - 1, child=f['refs'][-1])
            ref = len(nodes)
            nodes.append(nd)
        memo[f['key']] = answer, ref


def verify(cnf, certificate, n=None):
    """Raise InvalidCertificate on rejection; return True on a valid refutation.

    Validate *all* supplied dimensions, masks, references and edge ranks before
    normalization or splitting any supplied key. Input preprocessing uses only
    trusted input-size-bounded dense dimensions.
    """
    cs, D, eq = preprocess(cnf, n)
    c = certificate
    require(type(c) is dict and set(c) == {'version', 'solver_sha256', 'root', 'nodes'}, 'certificate fields')
    require(type(c['version']) is int and c['version'] == 1, 'version')
    require(c['solver_sha256'] == FROZEN_SHA256, 'frozen solver hash')
    nodes = c['nodes']
    require(type(nodes) is list, 'nodes array')
    keys, edges = [], []
    def reference(r):
        require(r is None or (type(r) is int and 0 <= r < len(nodes)), 'bad reference')
    reference(c['root'])
    for nd in nodes:
        require(type(nd) is dict, 'node object')
        kind = nd.get('kind')
        require(kind in ('branch', 'component'), 'node kind')
        fields = {'dimension', 'clauses', 'kind'} | ({'query', 'children'} if kind == 'branch' else {'index', 'child'})
        require(set(nd) == fields, 'node fields')
        d = nd['dimension']
        require(type(d) is int and 0 <= d <= D, 'dimension bound')
        clauses = nd['clauses']
        require(type(clauses) is list, 'clauses array')
        converted = []
        for clause in clauses:
            require(type(clause) is list, 'clause array')
            forms = []
            for lit in clause:
                require(type(lit) is list and len(lit) == 2, 'affine literal')
                mask, const = lit
                require(type(mask) is int and mask >= 0 and mask.bit_length() <= d, 'mask bound')
                require(type(const) is int and const in (0, 1), 'constant bit')
                forms.append((mask, const))
            converted.append(tuple(forms))
        keys.append((d, tuple(converted)))
        if kind == 'branch':
            q = nd['query']
            require(type(q) is list and len(q) == 2, 'query encoding')
            require(type(q[0]) is int and 0 < q[0] and q[0].bit_length() <= d, 'query mask')
            require(type(q[1]) is int and q[1] in (0, 1), 'query constant')
            require(type(nd['children']) is list and len(nd['children']) == 2, 'branch arity')
            refs = nd['children']
        else:
            require(type(nd['index']) is int and nd['index'] >= 0, 'component index')
            refs = [nd['child']]
        for r in refs: reference(r)
        edges.append(refs)
    for i, refs in enumerate(edges):
        for r in refs:
            require(r is None or keys[r][0] < keys[i][0], 'strict dimension rank')
    seen, todo = set(), [c['root']]
    while todo:
        r = todo.pop()
        if r is not None and r not in seen:
            seen.add(r)
            todo.extend(edges[r])
    require(len(seen) == len(nodes), 'unreachable nodes')
    def match(result, ref):
        require(result is not True, 'TRUE cannot prove UNSAT')
        if result is False: require(ref is None, 'FALSE needs terminal token')
        else: require(ref is not None and result == keys[ref], 'residual key mismatch')
    match(frozen.normalize(cs, D, eq), c['root'])
    for i, nd in enumerate(nodes):
        d, clauses = keys[i]
        require(frozen.normalize(clauses, d) == keys[i], 'noncanonical key')
        components = frozen.split_components(keys[i])
        if nd['kind'] == 'component':
            require(len(components) > 1 and nd['index'] < len(components), 'component selection')
            pd, pc = components[nd['index']]
            match(frozen.normalize(pc, pd), nd['child'])
        else:
            require(len(components) == 1, 'prescribed decomposition required')
            require(tuple(nd['query']) == clauses[0][0], 'prescribed branch required')
            mask, const = clauses[0][0]
            for value, ref in enumerate(nd['children']):
                match(frozen.normalize(clauses, d, ((mask, const ^ value),)), ref)
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['generate', 'check'])
    parser.add_argument('input', help='JSON object with clauses and optional n')
    parser.add_argument('certificate', nargs='?')
    args = parser.parse_args()
    try:
        data = json.loads(Path(args.input).read_text())
        require(type(data) is dict and 'clauses' in data and
                set(data) <= {'clauses', 'n'}, 'input object requires clauses and optional n')
        if args.mode == 'generate':
            result = generate(data['clauses'], data.get('n'))
            print(json.dumps(result, sort_keys=True))
            return 0 if result is not None else 2
        require(args.certificate is not None, 'certificate path required')
        verify(data['clauses'], json.loads(Path(args.certificate).read_text()), data.get('n'))
        print('VALID UNSAT residual certificate')
        return 0
    except (InvalidCertificate, json.JSONDecodeError, OSError) as e:
        print('REJECTED: ' + str(e), file=sys.stderr)
        return 1

if __name__ == '__main__':
    sys.exit(main())
