%global pkg_name jansi-native
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global bits 32
%global debug_package %{nil}

%ifarch x86_64 ppc64 s390x sparc64 aarch64
  %global bits 64
%endif

Name:             %{?scl_prefix}%{pkg_name}
Version:          1.4
Release:          10.6%{?dist}
Summary:          Jansi Native implements the JNI Libraries used by the Jansi project
License:          ASL 2.0
URL:              http://jansi.fusesource.org/

# git clone git://github.com/fusesource/jansi-native.git
# cd jansi-native && git archive --format=tar --prefix=jansi-native-1.4/ jansi-native-1.4 | xz > jansi-native-1.4.tar.xz
Source0:          jansi-native-%{version}.tar.xz

Patch0:           0001-Fixing-archiver-requires-AM_PROG_AR-in-configure.ac-.patch

BuildRequires:    %{?scl_prefix}javapackages-tools
BuildRequires:    %{?scl_prefix}maven-local
BuildRequires:    %{?scl_prefix}maven-compiler-plugin
BuildRequires:    %{?scl_prefix}maven-javadoc-plugin
BuildRequires:    %{?scl_prefix}maven-surefire-plugin
BuildRequires:    %{?scl_prefix}maven-surefire-report-plugin
BuildRequires:    %{?scl_prefix}maven-project-info-reports-plugin
BuildRequires:    %{?scl_prefix}maven-clean-plugin
BuildRequires:    %{?scl_prefix}maven-plugin-bundle
BuildRequires:    %{?scl_prefix}maven-plugin-jxr
BuildRequires:    %{?scl_prefix}junit
BuildRequires:    %{?scl_prefix}hawtjni
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    libtool
BuildRequires:    make
BuildRequires:    %{?scl_prefix}fusesource-pom
BuildRequires:    %{?scl_prefix}maven-surefire-provider-junit
BuildRequires:    %{?scl_prefix}maven-hawtjni-plugin
BuildRequires:    %{?scl_prefix}maven-resources-plugin
BuildRequires:    %{?scl_prefix}felix-parent

%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences. 

%package javadoc
Summary:          Javadocs for %{pkg_name}

%description javadoc
This package contains the API documentation for %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%patch0 -p1

%mvn_file :jansi-native %{pkg_name}
%mvn_package :::linux%{bits}: __default
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install

# JAR
mkdir -p $RPM_BUILD_ROOT%{_jnidir}
cp -p target/%{pkg_name}-%{version}-linux%{bits}.jar $RPM_BUILD_ROOT%{_jnidir}/%{pkg_name}-linux.jar
%{?scl:EOF}

%files -f .mfiles
%{_jnidir}/%{pkg_name}-linux.jar
%doc readme.md license.txt changelog.md

%files javadoc -f .mfiles-javadoc
%doc license.txt

%changelog
* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10.6
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10.4
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10.3
- Remove requires on java

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-10.1
- First maven30 software collection build

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.4-10
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.4-9
- Mass rebuild 2013-12-27

* Mon Nov 11 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-8
- Install attached artifacts for proper classifier provides
- Enable aarch64 support
- Resolves: rhbz#1028551

* Tue Aug 27 2013 Michal Srb <msrb@redhat.com> - 1.4-7
- Migrate away from mvn-rpmbuild (Resolves: #997522)

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.4-6
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.4-4
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Wed Dec 19 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-3
- revbump after jnidir change

* Wed Dec 12 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.4-2
- Move normal jar from javajnidir to javadir

* Wed Sep 19 2012 Marek Goldmann <mgoldman@redhat.com> - 1.4-1
- Upstream release 1.4
- Fixing "archiver requires 'AM_PROG_AR' in 'configure.ac'" error
- FTBFS: config.status: error: cannot find input file: `Makefile.in' RHBZ#858377

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Dan Horák <dan[at]danny.cz> 1.2-2
- fix build on non-x86 64-bit arches

* Thu Jul 28 2011 Marek Goldmann <mgoldman@redhat.com> 1.2-1
- Upstream release 1.2
- Using new jnidir

* Tue May 31 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-2
- Updated summary
- Removed debuginfo package
- Added license to javadoc package
- Fixed dependency on maven-hawtjni-plugin

* Fri May 27 2011 Marek Goldmann <mgoldman@redhat.com> 1.1-1
- Initial packaging

