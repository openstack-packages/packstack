
%global git_revno 653

Name:           openstack-packstack
Version:        2013.1.1
#Release:       1%{?dist}
Release:        0.22.dev%{git_revno}%{?dist}
Summary:        Openstack Install Utility

Group:          Applications/System
License:        ASL 2.0 and GPLv2
URL:            https://github.com/stackforge/packstack
# Tarball is created by bin/release.sh
Source0:        http://mmagr.fedorapeople.org/downloads/packstack/packstack-%{version}dev%{git_revno}.tar.gz

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?rhel}
BuildRequires:  python-sphinx10
%else
BuildRequires:  python-sphinx
%endif

Requires:       openssh-clients

%description
Packstack is a utility that uses puppet modules to install openstack
packstack can be used to deploy various parts of openstack on multiple
pre installed servers over ssh. It does this by using puppet manifests to
apply Puppet Labs modules (https://github.com/puppetlabs/)


%package -n packstack-modules-puppet
Summary:        Set of Puppet modules for OpenStack

%description -n packstack-modules-puppet
Set of Puppet modules used by Packstack to install OpenStack


%prep
#%setup -n packstack-%{version}
%setup -n packstack-%{version}dev%{git_revno}

# Sanitizing a lot of the files in the puppet modules, they come from seperate upstream projects
find packstack/puppet/modules \( -name .fixtures.yml -o -name .gemfile -o -name ".travis.yml" -o -name .rspec \) -exec rm {} +
find packstack/puppet/modules \( -name "*.py" -o -name "*.rb" -o -name "*.pl" \) -exec sed -i '/^#!/{d;q}' {} + -exec chmod -x {} +
find packstack/puppet/modules \( -name "*.sh" \) -exec sed -i 's/^#!.*/#!\/bin\/bash/g' {} + -exec chmod +x {} +
find packstack/puppet/modules -name site.pp -size 0 -exec rm {} +
find packstack/puppet/modules \( -name spec -o -name ext \) | xargs rm -rf

# Moving this data directory out temporarily as it causes setup.py to throw errors
rm -rf %{_builddir}/puppet
mv packstack/puppet %{_builddir}/puppet


%build
# puppet on fedora already has this module, using this one causes problems
%if 0%{?fedora}
    rm -rf %{_builddir}/puppet/modules/create_resources
%endif

%{__python} setup.py build

cd docs
%if 0%{?rhel}
make man SPHINXBUILD=sphinx-1.0-build
%else
make man
%endif


%install
%{__python} setup.py install --skip-build --root %{buildroot}

# Delete tests
rm -fr %{buildroot}%{python_sitelib}/tests

mkdir -p %{buildroot}/%{_datadir}/packstack/
mv %{_builddir}/puppet %{buildroot}/%{python_sitelib}/packstack/puppet
cp -r %{buildroot}/%{python_sitelib}/packstack/puppet/modules  %{buildroot}/%{_datadir}/packstack/modules

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/


%files
%doc LICENSE
%{_bindir}/packstack
%{python_sitelib}/packstack
%{python_sitelib}/packstack-%{version}*.egg-info
%{_mandir}/man1/packstack.1.gz


%files -n packstack-modules-puppet
%defattr(644,root,root,755)
%{_datadir}/packstack/modules/


%changelog
* Thu Aug 01 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.22.dev653
- Enable qpidd on boot (#988803)

* Thu Jul 25 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.21.dev651
- Swithed to https://github.com/packstack/puppet-qpid (#977786)
- If allinone and quantum selected, install basic network (#986024)

* Wed Jul 10 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.20.dev642
- Fixed provider network option (#976380)
- Made token_format configurable (#978853)
- Enable LVM snap autoextend (#975894)
- MariaDB support (#981116)

* Tue Jun 18 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.19.dev632
- Restart openstack-cinder-volume service (#975007)

* Wed Jun 12 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.17.dev631
- Updated Keystone puppet module to have token_format=PKI as default

* Tue Jun 11 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.16.dev630
- Always update kernel package (#972960)

* Mon Jun 10 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.15.dev625
- Omit Nova DB password only on compute nodes (#966325)
- Find free device during host startup (#971145)

* Mon Jun 10 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.14.dev622
- Reverted Nova sql_connection changes because of introduced regression (#966325, #972365)

* Thu Jun 06 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.12.dev621
- Install qemu-kvm before libvirt (#957632)
- Add template for quantum API server (#968513)
- Removed SQL password in sql_connection for compute hosts (#966325)
- Fixed color usage (#971075)
- Activate cinder-volumes VG and scan PVs after reboot (#971145)

* Tue Jun 05 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.9.dev605
- Added whitespace filter to Nova and Quantum plugins (rhbz#970674)
- Removed RDO repo installation procedure

* Tue Jun 04 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.8.dev601
- Updated to packstack-2013.1.1dev601
- Fixes: rhbz#953157, rhbz#966560, rhbz#967291, rhbz#967306, rhbz#967307,
         rhbz#967344, rhbz#967348, rhbz#969975, rhbz#965787

* Thu May 23 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.7.dev580
- Removing call to setenforce (rhbz#954188)
- Synchronize time using all ntp servers (rhbz#956939)
- Fix for nagios multiple installation failures (rhbz#957006)

* Tue Apr 09 2013 Martin Mágr <mmagr@redhat.com> - 2013.1.1-0.4.dev538
- Updated to  packstack-2013.1.1dev538.tar.gz
- Fixes: rhbz#946915, rhbz#947427

* Sun Mar 31 2013 Derek Higgins <derekh@redhat.com> - 2013.1.1-0.3.dev527
- update to packstack-2013.1.1dev527.tar.gz
- no longer require openstack-utils
- packstack now has its own copy of the puppet modules, the symbolic link
  causes problems with package updates

* Fri Mar 15 2013 Derek Higgins <derekh@redhat.com> - 2013.1.1-0.2.dev502
- remove tests

* Fri Mar 15 2013 Derek Higgins <derekh@redhat.com> - 2013.1.1-0.1.dev502
- Udated to grizzly (packstack-2013.1.1dev502.tar.gz)

* Wed Mar 13 2013 Martin Magr <mmagr@redhat.com> - 2012.2.3-0.5.dev475
- Updated to version 2012.2.3dev475

* Wed Feb 27 2013 Martin Magr <mmagr@redhat.com> - 2012.2.3-0.1.dev454
- Updated to version 2012.2.3dev454
- Fixes: rhbz#865347, rhbz#888725, rhbz#892247, rhbz#893107, rhbz#894733,
         rhbz#896618, rhbz#903545, rhbz#903813, rhbz#904670, rhbz#905081,
         rhbz#905368, rhbz#908695, rhbz#908771, rhbz#908846, rhbz#908900,
         rhbz#910089, rhbz#910210, rhbz#911626, rhbz#912006, rhbz#912702,
         rhbz#912745, rhbz#912768, rhbz#915382

* Mon Feb 18 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-1.0.dev408
- Updated to version 2012.2.2dev408

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2012.2.2-0.9.dev406
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 13 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.8.dev406
- Updated to version 2012.2.2dev406

* Tue Jan 29 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.7.dev346
- Updated to version 2012.2.2dev346

* Mon Jan 28 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.6.dev345
- Updated to version 2012.2.2dev345

* Mon Jan 21 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.5.dev318
- Updated to version 2012.2.2dev318

* Fri Jan 18 2013 Martin Magr <mmagr@redhat.com> - 2012.2.2-0.4.dev315
- Added openstack-utils to Requires
- Updated to version 2012.2.2dev315

* Fri Jan 11 2013 Derek Higgins <derekh@redhat.com> - 2012.2.2-0.3.dev281
- updated to version 2012.2.2dev281

* Fri Dec 07 2012 Derek Higgins <derekh@redhat.com> - 2012.2.2-0.2.dev211
- Fixed packaging, shebang in .sh files was being removed
- updated to version 2012.2.2dev211

* Wed Dec 05 2012 Derek Higgins <derekh@redhat.com> - 2012.2.2-0.1.dev205
- Fixing pre release versioning
- updated to version 2012.2.2dev205

* Fri Nov 30 2012 Derek Higgins <derekh@redhat.com> - 2012.2.1-1dev197
- cleaning up spec file
- updated to version 2012.2.1-1dev197

* Wed Nov 28 2012 Derek Higgins <derekh@redhat.com> - 2012.2.1-1dev186
- example packaging for Fedora / Redhat
