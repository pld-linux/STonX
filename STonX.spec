#
# Conditional build:
# _without_svga		without svgalib support
#

%ifnarch %{ix86}
%define _without_svga 1
%endif

%define		tosarchname	tos206us.zip
%define		tosfilename	Tos206.img

Summary:	Atari ST on Unix/X
Summary(pl):	Atari ST pod Uniksem/X
Name:		STonX
Version:	0.6.5
Release:	1
License:	GPL (except TOS image)
Group:		Applications/Emulators
Source0:	http://www.complang.tuwien.ac.at/nino/stonx/%{name}-%{version}.tar.gz
# to use TOS image legally, one probably must own real Atari ST...
Source1:	%{tosarchname}
NoSource:	1
Patch0:		%{name}-nox.patch
Patch1:		%{name}-svga.patch
URL:		http://www.complang.tuwien.ac.at/nino/stonx.html
BuildRequires:	XFree86-devel
%{!?_without_svga:BuildRequires:	svgalib-devel}
BuildRequires:	autoconf
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6

%description
STonX is a software emulator, which runs on Unix workstations with the
X Window system%{!?_without_svga: or svgalib}, and emulates an Atari ST computer.

%description -l pl
STonX jest programowym emulatorem komputera Atari ST, dzia³aj±cym na
Uniksach z X Window System%{!?_without_svga: lub svgalib}.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1

mv -f %{tosfilename} tos.img

%build
autoconf
%configure

%{__make} \
	OPT="%{rpmcflags}" \
	REGS="%{!?debug:-fomit-frame-pointer}" \
	%{!?_without_svga:USE_SVGALIB=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/STonX,%{_bindir},%{_fontsdir}/misc}

install stonx tos.img cartridge.img Keysyms $RPM_BUILD_ROOT%{_libdir}/STonX

gzip -9nf data/*.pcf
install data/*.pcf.gz $RPM_BUILD_ROOT%{_fontsdir}/misc

cat > $RPM_BUILD_ROOT%{_bindir}/stonx <<EOF
#!/bin/sh
cd %{_libdir}/STonX

%{!?_without_svga:if [ -z "\$DISPLAY" ]; then exec ./stonx -svga ; fi}
exec ./stonx
EOF

gzip -9nf docs/{PROGRAMS,README,RELEASE_NOTES,TOS-VERSIONS}

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/share/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
if [ -f /var/lock/subsys/xfs ]; then
	/etc/rc.d/init.d/xfs reload
fi

%postun
if [ -x /usr/X11R6/bin/mkfontdir ]; then
	(cd /usr/share/fonts/misc; /usr/X11R6/bin/mkfontdir)
fi
if [ -f /var/lock/subsys/xfs ]; then
	/etc/rc.d/init.d/xfs reload
fi

%files
%defattr(644,root,root,755)
%doc docs/*.gz
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/STonX
%attr(755,root,root) %{_libdir}/STonX/stonx
%{_libdir}/STonX/*.img
%{_libdir}/STonX/Keysyms
%{_fontsdir}/misc/*
