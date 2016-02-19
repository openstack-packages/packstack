%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global git_snaptag 1699
%global git_commit g8f54936

%{!?upstream_version:   %global upstream_version         %{version}.dev%{git_snaptag}.%{git_commit}}

# openstack-packstack ----------------------------------------------------------

Name:           openstack-packstack
Epoch:          1
Version:        7.0.0
Release:        0.12.dev%{git_snaptag}.%{git_commit}%{?dist}
Summary:        Openstack Install Utility

Group:          Applications/System
License:        ASL 2.0 and GPLv2
URL:            https://github.com/stackforge/packstack
# Tarball is created by bin/release.sh
Source0:        http://mmagr.fedorapeople.org/downloads/packstack/packstack-%{upstream_version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       openssh-clients
Requires:       python-netaddr
Requires:       openstack-packstack-puppet == %{epoch}:%{version}-%{release}
Requires:       openstack-puppet-modules >= 2014.2.10
Obsoletes:      packstack-modules-puppet
Requires:       python-setuptools
Requires:       PyYAML
Requires:       python-docutils
Requires:       pyOpenSSL
Requires:       iproute
Requires:       libselinux-utils
Requires:       initscripts


%description
Packstack is a utility that uses Puppet modules to install OpenStack. Packstack
can be used to deploy various parts of OpenStack on multiple pre installed
servers over ssh.


# openstack-packstack-puppet ---------------------------------------------------

%package puppet
Summary:        Packstack Puppet module
Group:          Development/Libraries

%description puppet
Puppet module used by Packstack to install OpenStack


# openstack-packstack-doc ------------------------------------------------------

%if 0%{?with_doc}
%package doc
Summary:          Documentation for Packstack
Group:            Documentation

%if 0%{?rhel} == 6
BuildRequires:  python-sphinx10
%endif
BuildRequires:  /usr/bin/sphinx-build

%description doc
This package contains documentation files for Packstack.
%endif


# prep -------------------------------------------------------------------------

%prep
%setup -q -n packstack-%{upstream_version}

# Sanitizing a lot of the files in the puppet modules
find packstack/puppet/modules \( -name .fixtures.yml -o -name .gemfile -o -name ".travis.yml" -o -name .rspec \) -exec rm {} +
find packstack/puppet/modules \( -name "*.py" -o -name "*.rb" -o -name "*.pl" \) -exec sed -i '/^#!/{d;q}' {} + -exec chmod -x {} +
find packstack/puppet/modules \( -name "*.sh" \) -exec sed -i 's/^#!.*/#!\/bin\/bash/g' {} + -exec chmod +x {} +
find packstack/puppet/modules -name site.pp -size 0 -exec rm {} +
find packstack/puppet/modules \( -name spec -o -name ext \) | xargs rm -rf

# Moving this data directory out temporarily as it causes setup.py to throw errors
rm -rf %{_builddir}/puppet
mv packstack/puppet %{_builddir}/puppet


# build ------------------------------------------------------------------------

%build
%{__python} setup.py build

%if 0%{?with_doc}
cd docs
%if 0%{?rhel} == 6
make man SPHINXBUILD=sphinx-1.0-build
%else
make man
%endif
%endif


# install ----------------------------------------------------------------------

%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

# Install Puppet module
mkdir -p %{buildroot}/%{_datadir}/openstack-puppet/modules
cp -r %{_builddir}/puppet/modules/packstack  %{buildroot}/%{_datadir}/openstack-puppet/modules/

# Move packstack documentation
mkdir -p %{buildroot}/%{_datadir}/packstack
install -p -D -m 644 docs/packstack.rst %{buildroot}/%{_datadir}/packstack

# Move Puppet manifest templates back to original place
mkdir -p %{buildroot}/%{python_sitelib}/packstack/puppet
mv %{_builddir}/puppet/templates %{buildroot}/%{python_sitelib}/packstack/puppet/

%if 0%{?with_doc}
mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/
%endif

# Remove docs directory
rm -fr %{buildroot}%{python_sitelib}/docs

# files ------------------------------------------------------------------------

%files
%doc LICENSE
%{_bindir}/packstack
%{_datadir}/packstack
%{python_sitelib}/packstack
%{python_sitelib}/packstack-*.egg-info

%files puppet
%defattr(644,root,root,755)
%{_datadir}/openstack-puppet/modules/packstack

%if 0%{?with_doc}
%files doc
%{_mandir}/man1/packstack.1.gz
%endif


# changelog --------------------------------------------------------------------

%changelog
* Thu Feb 18 2016 Iván Chavero <ichavero@redhat.com> - 7.0.0-0.12.dev1699.g8f54936
- Enable VPN tab in Horizon when enabling VPNaaS (rhbz#1297733)
- Fix Trove api-paste.ini path
- Use absolute path for Trove's api-paste.ini (rhbz#1282928)
- Add notification driver (rhbz#1283261)
- Drop dependancy on puppet-galera (rhbz#1283261)

* Sun Jan 31 2016 Iván Chavero <ichavero@redhat.com> - 7.0.0-0.11.dev1692.g1b5e83b
- Add package dependencies (rhbz#1285502)
- Install service_plugins packages on neutron api node (rhbz#1301680)
- Remove nova-network workarounds (rhbz#1298964)
- Fix lvm.conf edition (rhbz#1297712)
- Switch to PyMySQL (rhbz#1266028)

* Fri Dec 18 2015 Iván Chavero <ichavero@redhat.com> - 7.0.0-0.10.dev.dev1682.g42b3426
- Add Adapt to newest puppet-keystone (rhbz#1292923)

* Thu Dec 10 2015 Iván Chavero <ichavero@redhat.com> - 7.0.0-0.9.dev.dev1680.gd8a98dd
- Remove 0001-Add-symlink-to-support-hiera-3.0.patch
- Remove 0002-Do-not-enable-EPEL-when-installing-RDO.patch
- Dashboard's local_settings file should not be world readable (rhbz#1217089)
- Add support for Neutron ML2 SR-IOV mechanism driver (rhbz#1167099)
- Do not enable EPEL when installing RDO
- Add symlink to support hiera >= 3.0 (rhbz#1284978)

* Thu Nov 26 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:7.0.0-0.8.dev.dev1661.gaf13b7e
- Require sphinx-build directly instead of a package name

* Wed Nov 25 2015 Javier Peña <jpena@redhat.com> - 7.0.0-0.7.dev.dev1661.gaf13b7e
- Adapt man build to updated sphinx package, by using python3-sphinx

* Wed Nov 25 2015 Javier Peña <jpena@redhat.com> - 7.0.0-0.6.dev.dev1661.gaf13b7e
- Do not enable EPEL when installing RDO

* Wed Nov 25 2015 Alan Pevec <apevec@redhat.com> - 7.0.0-0.5.dev.dev1661.gaf13b7e
- Add symlink to support hiera >= 3.0 rhbz#1284978

* Thu Oct 29 2015  Javier Pena <jpena@redhat.com> - 7.0.0-0.4.dev1661.gaf13b7e
- Use epoch in dependency for openstack-packstack-puppet

* Mon Oct 26 2015  Martin Magr <mmagr@redhat.com> - 7.0.0-0.3.dev1661.gaf13b7e
-  Liberty rebase

* Sat Oct 10 2015  Alan Pevec <apevec@redhat.com> - 2015.2-0.1.dev.dev1654.gcbbf46e
-  Liberty release candidate

