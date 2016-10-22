%{?scl:%scl_package jansi-native}
%{!?scl:%global pkg_name %{name}}

%global bits 32
%global debug_package %{nil}
%global _enable_debug_packages 0

%ifarch x86_64 ppc64 s390x sparc64 aarch64
  %global bits 64
%endif

%{?scl:%thermostat_find_provides_and_requires}

Name:             %{?scl_prefix}jansi-native
Version:          1.4
Release:          14%{?dist}
Summary:          Jansi Native implements the JNI Libraries used by the Jansi project
Group:            Development/Libraries
License:          ASL 2.0
URL:              http://jansi.fusesource.org/

# git clone git://github.com/fusesource/jansi-native.git
# cd jansi-native && git archive --format=tar --prefix=jansi-native-1.4/ jansi-native-1.4 | xz > jansi-native-1.4.tar.xz
Source0:          jansi-native-%{version}.tar.xz

Patch0:           0001-Fixing-archiver-requires-AM_PROG_AR-in-configure.ac-.patch

BuildRequires:    jpackage-utils
BuildRequires:    java-devel
BuildRequires:    maven-local
BuildRequires:    maven-compiler-plugin
BuildRequires:    maven-javadoc-plugin
BuildRequires:    maven-surefire-plugin
BuildRequires:    maven-surefire-report-plugin
BuildRequires:    maven-project-info-reports-plugin
BuildRequires:    maven-clean-plugin
BuildRequires:    maven-plugin-bundle
BuildRequires:    maven-plugin-jxr
BuildRequires:    junit4
BuildRequires:    %{?scl_prefix}hawtjni
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    libtool
BuildRequires:    make
BuildRequires:    fusesource-pom
BuildRequires:    maven-surefire-provider-junit4
# We need the hawtjni maven plugin for this package to build.
# Comes from the hawtjni SRPM.
BuildRequires:    %{?scl_prefix}maven-hawtjni-plugin
BuildRequires:    maven-resources-plugin
BuildRequires:    felix-parent

%description
Jansi is a small java library that allows you to use ANSI escape sequences
in your Java console applications. It implements ANSI support on platforms
which don't support it like Windows and provides graceful degradation for
when output is being sent to output devices which cannot support ANSI sequences. 

%package javadoc
Summary:          Javadocs for %{name}
Group:            Documentation

%description javadoc
This package contains the API documentation for %{name}.

%prep
%{?scl:scl enable %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{version}
%patch0 -p1

%mvn_file :jansi-native %{pkg_name}
%mvn_package :::linux%{bits}: __default
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - << "EOF"}
%mvn_build
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - << "EOF"}
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
* Mon Jan 20 2014 Severin Gehwolf <sgehwolf@redhat.com>  - 1.4-14
- Rebuild in order to fix osgi()-style provides.
- Resolves: RHBZ#1054813

* Wed Nov 27 2013 Omair Majid <omajid@redhat.com>  - 1.4-13
- Properly enable SCL.

* Mon Nov 25 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.4-12
- Don't produce debug info package.

* Wed Nov 20 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.4-11
- Fix BRs in order to keep this package buildable with
  newer, dep-reduced hawtjni.

* Mon Nov 18 2013 Severin Gehwolf <sgehwolf@redhat.com>  - 1.4-10
- Add macro for java auto-requires/provides.
- Use SCL-ized packages as BRs.

* Mon Nov 11 2013 Severin Gehwolf <sgehwolf@redhat.com> - 1.4-9
- Install attached artifacts for proper classifier provides.
- Enable aarch64 support. 

* Fri Nov 08 2013 Severin Gehwolf <sgehwolf@redhat.com> - 1.4-8
- SCL-ize package.

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

