import os
for name in ['test_ml_out.txt', 'orchestrator_out.txt', 'tmp_check.py']:
    if os.path.exists(name):
        os.remove(name)
try:
    os.remove(__file__)
except OSError:
    pass
