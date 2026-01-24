# Repository Guidelines

## Project Structure & Module Organization
- `gewechat_client/` contains the Python package.
  - `gewechat_client/client.py` is the main client entry point.
  - `gewechat_client/api/` groups API modules (e.g., `message_api.py`, `login_api.py`).
  - `gewechat_client/util/` holds helpers such as HTTP utilities and terminal printing.
- `demo.py` shows an end-to-end usage flow (login, fetch contacts, send message).
- `docs/` holds documentation assets (e.g., `docs/images/`).
- `setup.py` and `build.sh` are used for packaging and distribution.

## Build, Test, and Development Commands
- `pip install -e .` installs the package in editable mode for local development.
- `python demo.py` runs the sample client flow; configure `BASE_URL`, `GEWECHAT_TOKE`, and `APP_ID` env vars first.
- `./build.sh` builds source and wheel distributions (`sdist` + `bdist_wheel`).
- `python setup.py sdist bdist_wheel` is the direct equivalent of the build script.

## Coding Style & Naming Conventions
- Python 3.6+ codebase with 4-space indentation.
- Prefer `snake_case` for functions/variables and `PascalCase` for classes (see `GewechatClient`).
- Keep modules focused by API surface area; add new endpoints under `gewechat_client/api/`.
- Match existing patterns: methods return dicts with `ret`, `msg`, and `data` keys where applicable.

## Testing Guidelines
- There are no automated tests in this repository currently.
- If adding tests, place them under a new `tests/` directory and name files `test_*.py`.
- Keep tests lightweight and focused on API method behavior and error handling.

## Commit & Pull Request Guidelines
- Recent commits use conventional prefixes like `feat:`, `fix:`, and `docs:`; follow the same pattern.
- Keep commit subjects short and action-oriented (e.g., `fix: handle login error type`).
- PRs should include: a clear description, linked issues (if any), and a brief test note (e.g., “manual run: `python demo.py`”).

## Configuration & Security Notes
- The demo relies on environment variables for API endpoint and credentials; avoid hardcoding tokens.
- If you introduce new configuration, document it in `README.md` and prefer env vars.

# 重要，必须遵守的规则
- 请使用中文回答我的提问
- 循序渐进写代码，实现一部分代码停下来总结一下你的代码，方便我及时review
