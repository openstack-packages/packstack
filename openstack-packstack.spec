
%global git_revno 406

Name:           openstack-packstack
Version:        2012.2.2
#Release:       1%{?dist}
Release:        0.9.dev%{git_revno}%{?dist}
Summary:        Openstack Install Utility

Group:          Applications/System
License:        ASL 2.0
URL:            https://github.com/fedora-openstack/packstack
#Source0:        http://derekh.fedorapeople.org/downloads/packstack/packstack-%{version}.tar.gz
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
Requires:       openstack-utils

%description
Packstack is a utility that uses puppet modules to install openstack
packstack can be used to deploy various parts of openstack on multiple
pre installed servers over ssh. It does this be using puppet manifests to
apply puppet labs modules (https://github.com/puppetlabs/)

%prep
#%setup -n packstack-%{version}
%setup -n packstack-%{version}dev%{git_revno}

# Sanitizing a lot of the files in the puppet modules, they come from seperate upstream projects
find packstack/puppet/modules \( -name .fixtures.yml -o -name .gemfile -o -name ".travis.yml" -o -name .rspec \) -exec rm {} \;
find packstack/puppet/modules \( -name "*.py" -o -name "*.rb" -o -name "*.pl" \) -exec sed -i '/^#!/{d;q}' {} \; -exec chmod -x {} \;
find packstack/puppet/modules \( -name "*.sh" \) -exec sed -i 's/^#!.*/#!\/bin\/bash/g' {} \; -exec chmod +x {} \;
find packstack/puppet/modules -name site.pp -size 0 -exec rm {} \;

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
mv %{_builddir}/puppet %{buildroot}/%{python_sitelib}/packstack/puppet

mkdir -p %{buildroot}%{_mandir}/man1
install -p -D -m 644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/

%files
%doc LICENSE
%{_bindir}/packstack
%{python_sitelib}/packstack
%{python_sitelib}/packstack-%{version}*.egg-info
%{_mandir}/man1/packstack.1.gz

%changelog
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

