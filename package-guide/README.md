# flet-package-guide
FletPackageGuide control for Flet

## Installation

Add dependency to `pyproject.toml` of your Flet app:

* **Git dependency**

Link to git repository:

```
dependencies = [
  "flet-package-guide @ git+https://github.com/MyGithubAccount/flet-package-guide",
  "flet>=0.28.3",
]
```

* **PyPi dependency**  

If the package is published on pypi.org:

```
dependencies = [
  "flet-package-guide",
  "flet>=0.28.3",
]
```

Build your app:
```
flet build macos -v
```

## Documentation

[Link to documentation](https://MyGithubAccount.github.io/flet-package-guide/)
