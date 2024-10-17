Summary:	Fast NTLM authentication proxy with tunneling
Name:		cntlm
Version:	0.92.3
Release:	1
License:	GPLv2+
Group:		System Environment/Daemons
URL:		https://cntlm.sourceforge.net/
Source0:	http://sourceforge.net/projects/cntlm/files/cntlm/%{name}-%{version}.tar.bz2
Source1:	cntlm.init
Source2:	cntlm.init.fedora
Source3:	cntlm.sysconfig
Patch0:		cntlm-0.35.1-Makefile.patch
Requires(pre):	shadow-utils

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
%make

%install
%makeinstall_std

install -D -m 0755 %{SOURCE2} %{buildroot}%{_initddir}/cntlmd
install -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/sysconfig/cntlmd
mkdir -p -m 0755 %{buildroot}%{_var}/run/%{name}

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || \
  useradd -r -g %{name} -d %{_var}/run/%{name} -s /sbin/nologin \
    -c "%{name} daemon" %{name}

%files
%doc LICENSE README COPYRIGHT
%{_sbindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_initddir}/cntlmd
%attr(-,cntlm,cntlm) %{_localstatedir}/run/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf
%config(noreplace) %{_sysconfdir}/sysconfig/cntlmd



