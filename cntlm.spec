Summary:        Fast NTLM authentication proxy with tunneling
Name:           cntlm
Version:        0.35.1
Release:        4%{?dist}
License:        GPLv2+
Group:          System Environment/Daemons
URL:            http://cntlm.sourceforge.net/
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1:        cntlm.init
Source2:        cntlm.init.fedora
Source3:        cntlm.sysconfig
Patch0:         cntlm-0.35.1-Makefile.patch
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires(post):  chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(pre):   shadow-utils

%description
Cntlm is a fast and efficient NTLM proxy, with support for TCP/IP tunneling,
authenticated connection caching, ACLs, proper daemon logging and behavior
and much more. It has up to ten times faster responses than similar NTLM
proxies, while using by orders or magnitude less RAM and CPU. Manual page
contains detailed information.

%prep
%setup -q
%patch0 -p1

%build
%configure
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make BINDIR=%{buildroot}%{_sbindir} MANDIR=%{buildroot}%{_mandir} SYSCONFDIR=%{buildroot}%{_sysconfdir} install

install -D -m 0755 %{SOURCE2} %{buildroot}%{_initddir}/cntlmd
install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/cntlmd
mkdir -p -m 0755 %{buildroot}%{_localstatedir}/run/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE README COPYRIGHT
%{_sbindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_initddir}/cntlmd
%attr(-,cntlm,cntlm) %{_localstatedir}/run/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/cntlmd

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
  useradd -r -g %{name} -d %{_localstatedir}/run/%{name} -s /sbin/nologin \
    -c "%{name} daemon" %{name}
exit 0

%post
/sbin/chkconfig --add cntlmd
exit 0

%preun
if [ $1 = 0 ]; then
  /sbin/service cntlmd stop  > /dev/null 2>&1
  /sbin/chkconfig --del cntlmd
fi
exit 0

%postun
if [ "$1" -ge "1" ]; then
   /sbin/service cntlmd condrestart > /dev/null 2>&1 || :
fi
exit 0

%changelog
* Thu Aug 26 2010 Matt Domsch <mdomsch@fedoraproject.org> - 0.35.1-4
- initscript: use pidfile to killproc

* Wed Aug 25 2010 Matt Domsch <mdomsch@fedoraproject.org> - 0.35.1-3
- additional fixes per package review

* Tue Aug 24 2010 Matt Domsch <mdomsch@fedoraproject.org> - 0.35.1-2
- updated spec to match Fedora packaging guidelines

* Fri Jul 27 2007 Radislav Vrnata <vrnata at gedas.cz>
- added support for SuSE Linux

* Wed Jul 26 2007 Radislav Vrnata <vrnata at gedas.cz>
- fixed pre, post, preun, postun macros bugs affecting upgrade process

* Mon May 30 2007 Since 0.28 maintained by <dave@awk.cz>

* Mon May 28 2007 Radislav Vrnata <vrnata at gedas.cz>
- Version 0.27
- First release
