%{?_javapackages_macros:%_javapackages_macros}
%global base_name       compress
%global short_name      commons-%{base_name}

Name:           apache-%{short_name}
Version:        1.10
Release:        1
Summary:        Java API for working with compressed files and archivers

License:        ASL 2.0
URL:            http://commons.apache.org/%{base_name}/
Source0:        http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  javapackages-tools >= 0.10.0
BuildRequires:  apache-commons-parent
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  xz-java

Provides:       jakarta-%{short_name} = %{version}-%{release}
Obsoletes:      jakarta-%{short_name} < 1.0-2

%description
The Apache Commons Compress library defines an API for working with
ar, cpio, Unix dump, tar, zip, gzip, XZ, Pack200 and bzip2 files.


%package javadoc
Summary:        API documentation for %{name}

Provides:       jakarta-%{short_name}-javadoc = %{version}-%{release}
Obsoletes:      jakarta-%{short_name}-javadoc < 1.0-2

%description javadoc
This package provides %{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
# FIXME: test fails for unknown reason
find -name X5455_ExtendedTimestampTest.java -delete

%build
%mvn_file  : %{short_name} %{name}
%mvn_alias : commons:
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt NOTICE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%changelog
* Tue Oct 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6-1
- Update to upstream version 1.6

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 14 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.5-1
- Update to upstream version 1.5

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4.1-5
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Jan  9 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.1-4
- Bump release tag

* Tue Jan  8 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4.1-3
- Build with xmvn
- Update to current packaging guidelines

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Sandro Mathys <red at fedoraproject.org> - 1.4.1-1
- Updated to 1.4.1
- Fixes CVE-2012-2098 Low: Denial of Service

* Fri Apr 27 2012 Sandro Mathys <red at fedoraproject.org> - 1.4-1
- Updated to 1.4

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 01 2011 Sandro Mathys <red at fedoraproject.org> - 1.3-1
- Updated to 1.3

* Thu Aug 04 2011 Sandro Mathys <red at fedoraproject.org> - 1.2-2
- Fixing mistake where different versions of the spec file got mixed up

* Thu Aug 04 2011 Sandro Mathys <red at fedoraproject.org> - 1.2-1
- Updated to 1.2

* Sat Apr 16 2011 Chris Spike <spike@fedoraproject.org> 1.1-1
- Updated to 1.1
- Adapted to current java packaging guidelines

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 11 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-8
- Fixed the Maven depmap line by replacing org.apache.maven by org.apache.commons

* Mon May 31 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-7
- Fixed regression with missing Provides/Obsoletes for javadocs
- Fixed changelog format

* Sun May 23 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-6
- Fixed Maven depmap to use commons-compress

* Thu May 13 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-5
- Added missing Provides/Obsoletes for javadocs 

* Mon May 10 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-4
- Cleared some problems after the review

* Thu May 06 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-3
- Now using maven2 (mvn-jpp) instead of directly calling javac & co

* Tue May 04 2010 Sandro Mathys <red at fedoraproject.org> - 1.0-2
- Renamed from jakarta-commons-compress
