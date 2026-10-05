# model-drift-detection — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does model-drift-detection address, and what can you demonstrate?

Compare a current batch with a reference batch. Drift is true when the mean moves by at least two reference standard deviations. The check does not retrain a model.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/drift/main.py`](src/drift/main.py): Implementation or supporting configuration.
- [`src/drift/detect.py`](src/drift/detect.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`src/drift/__init__.py`](src/drift/__init__.py): Implementation or supporting configuration.
- [`tests/test_drift.py`](tests/test_drift.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `detect` and explain the decision it makes?

The main walkthrough here is `detect(reference, current)` in [`src/drift/detect.py`](src/drift/detect.py#L9).

```python
def detect(reference, current):
    shift = abs(_mean(current) - _mean(reference)) / _std(reference)
    return {"mean_shift": round(shift, 4), "drift": shift >= 2, "retrained": False}
```

The implementation calls `_mean`, `_std`, `abs`, `round`. In an interview, trace those calls in execution order using a fixture input.

## 4. Where would you add input-validation tests?

Start with the handlers `post_drift` in [`src/drift/main.py`](src/drift/main.py#L7). Use the request schema or body access in each handler to build valid, missing-field, wrong-type, and boundary inputs. I would inspect existing tests before claiming coverage.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_drift.py`](tests/test_drift.py#L4) contains `test_shift_and_stable_batch`:

```python
def test_shift_and_stable_batch():
    client = TestClient(app)
    reference = [10, 11, 9, 10, 12]
    moved = client.post("/drift", json={"reference": reference, "current": [30, 31, 29, 30, 32]}).json()
    assert moved["drift"] is True
    assert moved["retrained"] is False
    stable = client.post("/drift", json={"reference": reference, "current": reference}).json()
    assert stable["drift"] is False
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `POST /drift` → `post_drift` in [`src/drift/main.py`](src/drift/main.py#L7).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `detect`?

In [`src/drift/detect.py`](src/drift/detect.py#L9), `detect(reference, current)` receives the inputs. The function computes these intermediate values:

- `shift = abs(_mean(current) - _mean(reference)) / _std(reference)`

Its result is defined by:

- `{'mean_shift': round(shift, 4), 'drift': shift >= 2, 'retrained': False}`
