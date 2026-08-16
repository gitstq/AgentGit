# Contributing to AgentGit

Thanks for your interest in making AgentGit better! 🎉

## Ways to contribute

- **Report bugs** — open an issue with a clear reproduction steps.
- **Request features** — describe the problem you are solving and a proposed UX.
- **Submit code** — fork, branch, commit, and open a pull request.
- **Improve docs** — typo fixes, better examples, new language translations.

## Development setup

AgentGit is zero-dependency Python (3.8+). No virtualenv required.

```bash
git clone https://github.com/gitstq/AgentGit.git
cd AgentGit
python -m unittest discover -s tests -v   # run tests
python bin/agentgit --help                # try the CLI
```

## Commit conventions

We follow the [Angular commit convention](https://www.conventionalcommits.org/):

```
feat: add new command
fix: correct snapshot diff ordering
docs: update quick start
refactor: simplify storage layer
test: add revert dry-run coverage
```

## Pull request checklist

- [ ] Tests pass locally (`python -m unittest discover -s tests -v`)
- [ ] Code is zero-dependency (stdlib only)
- [ ] No secrets or local paths committed
- [ ] README updated if user-facing behaviour changed

## Issue reporting

Please include:

- AgentGit version (`agentgit --version`)
- OS / Python version
- Steps to reproduce
- Expected vs actual behaviour
