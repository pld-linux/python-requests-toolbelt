#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	module		requests_toolbelt
%define	egg_name	requests_toolbelt
%define	pypi_name	requests-toolbelt
Summary:	Utility belt for advanced users of python-requests
Name:		python-%{pypi_name}
Version:	0.8.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/sigmavirus24/requests-toolbelt/archive/%{version}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	de9bf7fbcc6ae341a5c4fd9f8912bcac
URL:		https://toolbelt.readthedocs.io
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-betamax
BuildRequires:	python-mock
BuildRequires:	python-pytest
BuildRequires:	python-requests
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-betamax
BuildRequires:	python3-mock
BuildRequires:	python3-pytest
BuildRequires:	python3-requests
%endif
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is just a collection of utilities for python-requests, but don't
really belong in requests proper.

%package -n python3-%{pypi_name}
Summary:	%{summary}

%description -n python3-%{pypi_name}
This is just a collection of utilities for python-requests, but don't
really belong in requests proper.

%prep
%setup -q -n toolbelt-%{version}

%build
%if %{with python2}
%py_build
%if %{with tests}
py.test-%{py_ver} -v
%endif
%endif

%if %{with python3}
%py3_build
%if %{with tests}
py.test-%{py3_ver} -v
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%py_install
%py3_install

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
