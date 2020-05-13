%global pypiname rstdiary
Name:           python-%{pypiname}
Version:        2.0
Release:        0%{?dist}
Summary:        Create a simple HTML diary from an RST input file

Group:          Applications/Publishing
License:        MIT
URL:            http://www.github.com/ianw/rstdiary
Source0:        http://pypi.python.org/packages/source/r/%{pypiname}/%{pypiname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel

%description
A program to create a simple daily diary from a flat RST file input.
The output is chunked into months and lightly styled with bootstrap.

%package -n python3-%{pypiname}
Summary:  %{sum}
%{?python_provide:%python_provide python2-%{pypiname}}

Requires:  python3-docutils
Requires:  python3-jinja2

%description -n python3-%{pypiname}
A program to create a simple daily diary from a flat RST file input.
The output is chunked into months and lightly styled with bootstrap.

%prep
%autosetup -n %{pypiname}-%{version}

%build
%py3_build

%install
%py3_install

%check

%files -n python3-%{pypiname}
%doc README.md example/diary.rst example/diary.cfg example/Makefile example/README
%{python3_sitelib}/*
/usr/bin/rstdiary


%changelog
* Wed May 13 2020 Ian Wienand <iwienand@fedora19> - 2.0-0
- 2.0 release

* Wed Dec  6 2017 Ian Wienand <ian@wienand.org> - 1.0-0
- 1.0 release

* Tue Nov 18 2014 Ian Wienand <ian@wienand.org> - 0.2-1
- 0.2 release

* Tue Nov 18 2014 Ian Wienand <ian@wienand.org> - 0.1-1
- Initial release
