import nox


@nox.session
def lint(session: nox.Session) -> None:
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "ruff", "check")


@nox.session
def test(session: nox.Session) -> None:
    session.install("poetry")
    session.run("poetry", "install")

    cmd = "poetry run django-app-helper djangocms_haystack test --cms --extra-settings tests/settings.py"
    session.run(*cmd.split(" "))
