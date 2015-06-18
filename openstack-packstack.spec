%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global git_snaptag 1565
%global git_commit gd1211af

%{!?upstream_version:   %global upstream_version         %{version}.dev%{git_snaptag}.%{git_commit}}

# openstack-packstack ----------------------------------------------------------

Name:           openstack-packstack
Version:        2015.1
Release:        0.6.dev%{git_snaptag}.%{git_commit}%{?dist}
Summary:        Openstack Install Utility

Group:          Applications/System
License:        ASL 2.0 and GPLv2
URL:            https://github.com/stackforge/packstack
# Tarball is created by bin/release.sh
Source0:        http://mmagr.fedorapeople.org/downloads/packstack/packstack-%{upstream_version}.tar.gz

Patch1:         0001-Do-not-enable-Keystone-in-httpd-by-default.patch

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       openssh-clients
Requires:       python-netaddr
Requires:       openstack-packstack-puppet == %{version}-%{release}
Requires:       openstack-puppet-modules >= 2014.2.10
Obsoletes:      packstack-modules-puppet
Requires:       python-setuptools
Requires:       PyYAML
Requires:       python-docutils

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
%else
BuildRequires:  python-sphinx
%endif

%description doc
This package contains documentation files for Packstack.
%endif


# prep -------------------------------------------------------------------------

%prep
%setup -q -n packstack-%{upstream_version}
%patch1 -p1

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
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2015.1-0.6.dev1565.gd1211af
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Iván Chavero <ichavero@redhat.com> - 2015.1-0.5.dev1565.gd1211af
- [Neutron] use correct iface addresses on tunnel firewall rules - rhbz#1215638
- [Apache] don't purge apache configs in prescript
- [Apache] Fix apache module issues
- [Packstack] Updated LDAP doc entries
- [Packstack] Base force_interface on ipaddr instead of ipaddress
- [Packstack] Add symbolic link for latest log dir
- [Heat] Add processor process_string_nofloat
- [Nova] Fix Nova Networking with Manila Generic Driver
- [Nova] Fix instance metadata when not installing neutron
- [Swift] temporary use ipv6 address without brackets
- [memcached] fix memory consumption and add temporary IPv6 hack
- [Provision] re-enable provisioning subnets with ipv6
- [Keystone] Unite keystone admin and public url configuration
- [SSL] fix validate_writeable_directory
- [KEYSTONE] Correctly switch all admin usernames to CONFIG_KEYSTONE_ADMIN_USERNAME
- [Packstack] Refactor SSL setup to use CA to sign certificates
- [Neutron] Correct value of $public_bridge_name
- [Packstack] Add ability to enable rdo testing repo
- [Neutron] Allow CIDR instead of iterface name
- [Mongodb] Fix mongodb configuration

* Wed Jun 03 2015 Alan Pevec <apevec@redhat.com> - 2015.1-0.4.dev1537.gba5183c
- Add ability to enable rdo testing repo - rhbz#1218750

* Tue Jun 02 2015 Alan Pevec <apevec@redhat.com> - 2015.1-0.3.dev1537.gba5183c
- Do not enable Keystone in httpd by default

* Tue May 19 2015 Alan Pevec <apevec@redhat.com> - 2015.1-0.2.dev1537.gba5183c
- Fix mongodb configuration

* Sat May 02 2015 Alan Pevec <apevec@redhat.com> - 2015.1-0.1.dev1537.gba5183c
- Kilo release

* Mon Feb 23 2015 Martin Mágr <mmagr@redhat.com> - 2015.1-0.1.dev1484.g9bd9178
- Initial Kilo build
