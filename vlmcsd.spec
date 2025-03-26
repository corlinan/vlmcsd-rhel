Name:           vlmcsd
Version:        svn1113
Release:        1%{?dist}
Summary:        KMS Emulator in C

License:        LGPL-2.1+
URL:            https://github.com/Wind4/vlmcsd

Source0:        https://github.com/Wind4/vlmcsd/archive/refs/tags/svn1113.zip
Source10:       %{name}.service
Source11:       %{name}.sysusers
Source12:       %{name}.firewalld

BuildRequires:  make
Requires:       firewalld       

%description
vlmcs is a program that can be used to test a KMS server that provides
activation for several Microsoft products. The KMS server may also be an
emulator. It supports KMS protocol versions 4, 5 and 6. vlmcsd is a fully
Microsoft compatible KMS server that provides product activation services
to clients. It is meant as a drop-in replacement for a Microsoft KMS server
(Windows computer with KMS key entered). It currently supports KMS protocol
versions 4, 5 and 6.
%{nil}

%prep
%setup -q

%build
export STRIP=0
%{make_build}

%install
%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}
%{__cp} etc/* %{buildroot}%{_sysconfdir}/%{name}

%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} bin/* %{buildroot}%{_bindir}

%{__mkdir_p} %{buildroot}%{_mandir}/man1
%{__cp} man/vlmcs.1 %{buildroot}%{_mandir}/man1

%{__mkdir_p} %{buildroot}%{_mandir}/man5
%{__cp} man/vlmcsd.ini.5 %{buildroot}%{_mandir}/man5  

%{__mkdir_p} %{buildroot}%{_mandir}/man7
%{__cp} man/vlmcsd.7 %{buildroot}%{_mandir}/man7

%{__mkdir_p} %{buildroot}%{_mandir}/man8
%{__cp} man/vlmcsd.8 %{buildroot}%{_mandir}/man8

%{__mkdir_p} %{buildroot}%{_unitdir}
%{__cp} %{SOURCE10} %{buildroot}%{_unitdir}

%{__mkdir_p} %{buildroot}%{_sysusersdir}
%{__install} -p -D -m 644 %{SOURCE11} %{buildroot}%{_sysusersdir}/%{name}.conf

%{__install} -p -D %{SOURCE11} %{buildroot}%{_usr}/lib/firewalld/services/%{name}.xml

%pre
%sysusers_create_compat %{SOURCE11}

%post
%firewalld_reload
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*
%{_bindir}/*
%{_mandir}/man1/vlmcs.1*
%{_mandir}/man5/vlmcsd.ini.5*
%{_mandir}/man7/vlmcsd.7*
%{_mandir}/man8/vlmcsd.8*
%{_usr}/lib/firewalld/services/%{name}.xml
%{_sysusersdir}/%{name}.conf
%{_unitdir}/%{name}.service