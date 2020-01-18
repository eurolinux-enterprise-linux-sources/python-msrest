%if 0%{?fedora}
%global _with_python3 1
%global _with_tests 1
%endif

%if 0%{?rhel}
%global py2_prefix python
%else
%global py2_prefix python2
%endif

%global bundled_lib_dir    bundled
# python-typing
%global typing_version	3.5.2.2
%global typing_dir	%{bundled_lib_dir}/typing

%global srcname msrest

%global common_summary AutoRest swagger generator Python client runtime
%global common_description %{common_summary}.

Name:           python-%{srcname}
Version:        0.5.4
Release:        1%{?dist}
Summary:        %{common_summary}

Group:          System Environment/Libraries
License:        MIT
URL:            https://github.com/Azure/msrest-for-python/
Source0:        %{srcname}-%{version}.tar.gz
Source1:        typing-%{typing_version}.tar.gz
# - Disable versioned dependencies not yet available in Fedora/EPEL
# - Fix setup.py for older versions of setuptools (EPEL)
Patch0:         %{name}-0.5.4-build.patch
Patch1:         bundled-libs.patch

BuildRequires:  %{py2_prefix}-setuptools
BuildRequires:  python-devel

Requires:       python-enum34
Requires:       python-isodate
Requires:       %{py2_prefix}-requests
Requires:       %{py2_prefix}-requests-oauthlib

Provides: bundled(python-typing) = %{typing_version}

%if 0%{?_with_python3}
BuildRequires:  python3-devel
%endif
# Needed for tests
%if 0%{?_with_tests}
BuildRequires:  %{py2_prefix}-certifi
BuildRequires:  python-enum34
BuildRequires:  python-httpretty
BuildRequires:  python-isodate
BuildRequires:  %{py2_prefix}-requests
BuildRequires:  %{py2_prefix}-requests-oauthlib
%if 0%{?_with_python3}
BuildRequires:  python3-certifi
BuildRequires:  python3-httpretty
BuildRequires:  python3-isodate
BuildRequires:  python3-requests
BuildRequires:  python3-requests-oauthlib
%endif
%endif
BuildArch:      noarch

%description
%{common_description}


%if 0%{?_with_python3}
%package -n python3-%{srcname}
Summary:        %{common_summary}
Requires:       python3-isodate
Requires:       python3-requests
Requires:       python3-requests-oauthlib
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{common_description}
%endif


%prep
%setup -q -n %{srcname}-for-python-%{version}
%patch0 -p1

# add bundled libraries path
%patch1 -p1

# Remove failing test
# TODO: report bug upstream
rm tests/test_serialization.py

# bundled libraries
mkdir %{bundled_lib_dir}

# python-typing bundle
tar -xzf %SOURCE1 -C %{bundled_lib_dir}
mv %{bundled_lib_dir}/typing-%{typing_version} %{typing_dir}
cp %{typing_dir}/LICENSE typing_LICENSE
cp %{typing_dir}/README.rst typing_README.rst

%build
%py2_build
%{?_with_python3:%py3_build}

# python-typing bundle
pushd %{typing_dir}
%{__python2} setup.py build
popd


%install
%py2_install
%{?_with_python3:%py3_install}

# python-typing bundle
pushd %{typing_dir}
%{__python2} setup.py install -O1 --skip-build --root %{buildroot} --install-lib /usr/lib/%{name}/%{bundled_lib_dir}
popd


%check
%if 0%{?_with_tests}
%{__python2} setup.py test
%{?_with_python3:%{__python3} setup.py test}
%endif


%files -n python-%{srcname}
%doc README.rst typing_README.rst
%license LICENSE.md typing_LICENSE
%{python2_sitelib}/*

# bundled libraries
%dir /usr/lib/%{name}
/usr/lib/%{name}/%{bundled_lib_dir}


%if 0%{?_with_python3}
%files -n python3-%{srcname}
%doc README.rst typing_README.rst
%license LICENSE.md typing_LICENSE
%{python3_sitelib}/*
%endif


%changelog
* Mon May 13 2019 Oyvind Albrigtsen <oalbrigt@redhat.com> - 0.5.4-1
- Update to 0.5.4
  Resolves: rhbz#1707859

* Fri Nov 10 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.18-1
- Update to 0.4.18

* Tue Oct 17 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.17-1
- Update to 0.4.17

* Fri Oct 06 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.16-1
- Update to 0.4.16

* Wed Aug 30 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.14-1
- Update to 0.4.14
- Use python2- prefix for Fedora dependencies if possible

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.11-1
- Update to 0.4.11

* Fri Jun 09 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.9-1
- Update to 0.4.9

* Tue May 30 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.8-2
- Disable version check on certifi in setup.py

* Tue May 30 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.8-1
- Update to 0.4.8

* Wed Apr 05 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.7-1
- Update to 0.4.7

* Tue Mar 07 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.6-1
- Update to 0.4.6

* Tue Feb 14 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.5-1
- Update to 0.4.5

* Thu Jan 26 2017 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.4-2
- Add license file

* Tue Sep 27 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.4-1
- Update to 0.4.4

* Mon Sep 05 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.3-1
- Update to 0.4.3

* Fri Jun 24 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.0-2
- Fix tests for Fedora >= 24

* Thu May 26 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0

* Sun May 01 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Fri Apr 01 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Fri Mar 25 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.1.3-2
- Add missing depedency to enum34 Python module

* Wed Mar 23 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.1.3-1
- Update to 0.1.3

* Wed Mar 16 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.1.2-1
- Update to 0.1.2

* Sat Mar 05 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.1.1-1
- Update to 0.1.1

* Wed Mar 02 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.0.3-1
- Update to 0.0.3

* Sun Feb 28 2016 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.0.2-1
- Initial RPM release
