%global pypiname rstdiary
Name:           python-rstdiary
Version:        0.1
Release:        1%{?dist}
Summary:        Create a simple HTML diary from an RST input file

Group:          Applications/Publishing
License:        MIT
URL:            http://www.github.com/ianw/rstdiary
Source0:        http://pypi.python.org/packages/source/r/%{pypiname}/%{pypiname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:  python-docutils
Requires:  python-jinja2

%description

A program to create a simple "daily-diary" from a flat RST file input.
The output is chunked into months and lightly styled with bootstrap.

%prep
%setup -q -n %{pypiname}-%{version}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%check

%files
%defattr(-,root,root,-)
%doc README.md example.cfg example.rst
%{python2_sitelib}/rstdiary
%{python2_sitelib}/%{pypiname}-%{version}-py2.?.egg-info
/usr/bin/rstdiary

%changelog
* Tue Nov 18 2014 Ian Wienand <iwienand@redhat.com> - 0.1-1
- Initial release
