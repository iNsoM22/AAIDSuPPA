# AAIDSuPPA

Automated Academic Integrity Detection System implementation scaffold for CS-437 parallel programming.

## Quick Start

1. Build C++ engine:
   ```bash
   ./scripts/build.sh
   ```
2. Create Python environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Run tests:
   ```bash
   ctest --test-dir cpp/build --output-on-failure
   pytest -q
   ```
4. Run web app:
   ```bash
   flask --app web.app:create_app run
   ```
