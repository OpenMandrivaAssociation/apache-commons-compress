%global base_name       compress
%global short_name      commons-%{base_name}

Name:             apache-%{short_name}
Version:          1.1
Release:          2
Summary:          Java API for working with tar, zip and bzip2 files
Group:            Development/Java
License:          ASL 2.0
URL:              http://commons.apache.org/%{base_name}/
Source0:          http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
BuildArch:        noarch

BuildRequires:    java-devel >= 0:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:    apache-commons-parent
Requires:         java >= 0:1.6.0
Requires:         jpackage-utils
Requires(post):   jpackage-utils
Requires(postun): jpackage-utils


# Upstream name change
Provides:         jakarta-%{short_name} = %{version}-%{release}
Obsoletes:        jakarta-%{short_name} < 1.0-2

%description
The code in this component came from Avalon's Excalibur, but originally
from Ant, as far as life in Apache goes. The tar package is originally
Tim Endres' public domain package. The bzip2 package is based on the
work done by Keiron Liddle. It has migrated via:
Ant -> Avalon-Excalibur -> Commons-IO -> Commons-Compress. 


%package javadoc
Summary:        Javadocs for %{name}
Group:          Development/Java
Requires:       jpackage-utils

# Upstream name change
Provides:         jakarta-%{short_name}-javadoc = %{version}-%{release}
Obsoletes:        jakarta-%{short_name}-javadoc < 1.0-2

%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n %{short_name}-%{version}-src

%build
mvn-rpmbuild install javadoc:aggregate

%install
# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{short_name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar
ln -sf %{name}.jar %{buildroot}%{_javadir}/%{short_name}.jar

# poms
install -d -m 0755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml %{buildroot}%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%{_javadir}/*
%{_mavenpomdir}/JPP-%{short_name}.pom
%{_mavendepmapfragdir}/*

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt NOTICE.txt
%doc %{_javadocdir}/%{name}

