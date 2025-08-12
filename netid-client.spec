Name:		netid-client
Version:	1.3.1.16
Release:	1%{?dist}
Summary:	SecMaker Netid PKCS#11

License:	Commercial
URL:		https://www.secmaker.com
Source0:	iidsetup_v6.8.2.38_%{company}_x64.tar.gz
Source0:	netidsetup_v%{version}_linux_%{company}.tar.gz

Provides:	libnetid.so()(64bit)

%global		versionraw 06080238

%description
Pointsharp Net iD client PKCS#11 module. A next generation card driver for just about any smartcard.

%prep
%setup -n netidsetup
exit


%install
# install libraries
install -m 755 -d %{buildroot}/%{_libdir}/netid
install -m 755 -d %{buildroot}/%{_libdir}/pkcs11
install -m 755 libnetid.so -t %{buildroot}/%{_libdir}/netid
ln -sf netid/libnetid.so %{buildroot}/%{_libdir}/libiidp11.so
ln -sf ../netid/libnetid.so %{buildroot}/%{_libdir}/pkcs11/libnetid.so

# install binaries
install -m 755 -d %{buildroot}/%{_bindir}
install -m 755 netid -t %{buildroot}/%{_bindir}
ln -sf ../lib/netid/netid %{buildroot}/%{_bindir}/netid

# /usr/lib seems to be hardcoded somwhere
install -m 755 -d %{buildroot}/%{_exec_prefix}/lib
ln -sf %{_libdir}/netid %{buildroot}/%{_exec_prefix}/lib/netid

# install desktop icon
install -m 755 -d %{buildroot}/%{_datadir}/applications
./create_desktop_icon.sh %{buildroot}/%{_datadir}/applications/netid.desktop %{_bindir} %{_libdir} %{_sysconfdir} %{_sysconfdir}/iid gui 0x01400200

# install license
install -m 755 -d %{buildroot}/%{_defaultlicensedir}/%{name}-%{version}
install -m 644 license-en_US.html -t %{buildroot}/%{_defaultlicensedir}/%{name}-%{version}
install -m 644 license-sv_SE.html -t %{buildroot}/%{_defaultlicensedir}/%{name}-%{version}

# fix configuration
%{buildroot}/%{_bindir}/iid -setconfig -file %{buildroot}/%{_sysconfdir}/iid.conf -section "Install" -entry "Directory" -value "%{_libdir}/netid/"
%{buildroot}/%{_bindir}/iid -setconfig -file %{buildroot}/%{_sysconfdir}/iid.conf -section "SmartCardReader PCSC" -entry "ModeCheckInfoAllow" -value "any"

%post

%preun

%files
%{_bindir}/netid
%{_libdir}/lib*.so*
%{_libdir}/pkcs11/lib*.so*
%{_sysconfdir}/netid.conf
%{_defaultlicensedir}/%{name}-%{version}/*

%changelog

