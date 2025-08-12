Name:		netid-client
Version:	1.3.1.16
Release:	1%{?dist}
Summary:	Pointsharp Net iD client PKCS#11

License:	Commercial
URL:		https://www.pointsharp.com
Source0:	netidsetup_v%{version}_linux_%{company}.tar.gz

Provides:	libnetid.so()(64bit)

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
ln -sf netid/libnetid.so %{buildroot}/%{_libdir}/libnetid.so
ln -sf ../netid/libnetid.so %{buildroot}/%{_libdir}/pkcs11/libnetid.so

# install binaries
install -m 755 -d %{buildroot}/%{_bindir}
install -m 755 netid -t %{buildroot}/%{_libdir}/netid
ln -sf ../lib64/netid/netid %{buildroot}/%{_bindir}/netid

# /usr/lib seems to be hardcoded somewhere
install -m 755 -d %{buildroot}/%{_exec_prefix}/lib
ln -sf ../lib64/netid %{buildroot}/%{_exec_prefix}/lib/netid
ln -sf ../lib64/netid/libnetid.so %{buildroot}/%{_exec_prefix}/lib/libnetid.so

# user service autostart
install -m 755 -d %{buildroot}/%{_datadir}/applications

# install license
install -m 755 -d %{buildroot}/%{_defaultlicensedir}/%{name}-%{version}
install -m 644 license-en_US.html -t %{buildroot}/%{_defaultlicensedir}/%{name}-%{version}
install -m 644 license-sv_SE.html -t %{buildroot}/%{_defaultlicensedir}/%{name}-%{version}

# install p11-kit module definition
install -m 755 -d %{buildroot}/%{_datadir}/p11-kit/modules
cat << EOF >  %{buildroot}/%{_datadir}/p11-kit/modules/netid-client.module
module: libnetid.so
trust-policy: no
priority: 2
EOF

# install autostarted user service
install -m 755 -d %{buildroot}/%{_sysconfdir}/xdg/autostart
cat << EOF > %{buildroot}/%{_sysconfdir}/xdg/autostart/netid-client.desktop
[Desktop Entry]
Name=Net iD Monitor
Comment=Net iD Monitor
Exec=/usr/bin/netid -service user
Terminal=false
Type=Application
X-GNOME-Autostart-enabled=true
EOF

# install config
install -m 755 -d %{buildroot}/%{_sysconfdir}
install -m 644 netid.conf -t %{buildroot}/%{_sysconfdir}

# fix configuration
sed -i -e 's!Directory=.*!Directory=/usr/lib64/netid/!' \
       -e 's!ModeCheckInfoAllow=.*!ModeCheckInfoAllow=any!' \
          %{buildroot}/%{_sysconfdir}/netid.conf
#%{buildroot}/%{_bindir}/netid -config set -file %{buildroot}/%{_sysconfdir}/netid.conf -section "Install" -entry "Directory" -value "%{_libdir}/netid/"
#%{buildroot}/%{_bindir}/netid -config set -file %{buildroot}/%{_sysconfdir}/netid.conf -section "SmartCardReader PCSC" -entry "ModeCheckInfoAllow" -value "any"

%post

%preun

%files
%{_bindir}/netid
%{_libdir}/*
%{_libdir}/pkcs11/lib*.so
%{_exec_prefix}/lib/*
%{_sysconfdir}/netid.conf
%{_sysconfdir}/xdg/autostart/*
%{_defaultlicensedir}/%{name}-%{version}/*
%{_datadir}/p11-kit/modules/*

%changelog

