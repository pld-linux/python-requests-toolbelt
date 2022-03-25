#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (some failing as of 0.9.1)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	module		requests_toolbelt
%define	egg_name	requests_toolbelt
%define	pypi_name	requests-toolbelt
Summary:	Utility belt for advanced users of python-requests
Summary(pl.UTF-8):	Pasek narzędzi dla zaawansowanych użytkowników python-requests
Name:		python-%{pypi_name}
Version:	0.9.1
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/requests-toolbelt/
Source0:	https://files.pythonhosted.org/packages/source/r/requests-toolbelt/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	b1509735c4b4cf95df2619facbc3672e
URL:		https://toolbelt.readthedocs.io/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-betamax
BuildRequires:	python-mock
BuildRequires:	python-pyOpenSSL
BuildRequires:	python-pytest
BuildRequires:	python-requests >= 2.0.1
BuildRequires:	python-requests < 3
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-betamax
BuildRequires:	python3-pyOpenSSL
BuildRequires:	python3-pytest
BuildRequires:	python3-requests >= 2.0.1
BuildRequires:	python3-requests < 3
%endif
%endif
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is just a collection of utilities for python-requests, but don't
really belong in requests proper.

%description -l pl.UTF-8
Zbiór narzędzi dla python-requests, nie należących do samych requests.

%package -n python3-%{pypi_name}
Summary:	Utility belt for advanced users of python-requests
Summary(pl.UTF-8):	Pasek narzędzi dla zaawansowanych użytkowników python-requests
Group:		Libraries/Python

%description -n python3-%{pypi_name}
This is just a collection of utilities for python-requests, but don't
really belong in requests proper.

%description -n python3-%{pypi_name} -l pl.UTF-8
Zbiór narzędzi dla python-requests, nie należących do samych requests.

%package apidocs
Summary:	API documentation for Python requests_toolbelt module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona requests_toolbelt
Group:		Documentation

%description apidocs
API documentation for Python requests_toolbelt module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona requests_toolbelt.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="betamax.fixtures.pytest" \
%{__python} -m pytest -v tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__sed} -i -e 's/import mock/from unittest import mock/; s/from mock import/from unittest.mock import/' \
	tests/*.py tests/threaded/*.py

PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS="betamax.fixtures.pytest" \
%{__python3} -m pytest -v tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst HISTORY.rst LICENSE
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst HISTORY.rst LICENSE
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
