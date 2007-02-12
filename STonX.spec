#
# Conditional build:
%bcond_without	svga	# without svgalib support
#
%define		tosarchname	tos206us.zip
%define		tosfilename	Tos206.img

Summary:	Atari ST on Unix/X
Summary(pl.UTF-8):   Atari ST pod Uniksem/X
Name:		STonX
Version:	0.6.5
Release:	2
License:	GPL (except TOS image)
Group:		Applications/Emulators
Source0:	http://www.complang.tuwien.ac.at/nino/stonx/%{name}-%{version}.tar.gz
# Source0-md5:	54ce49f5a64f0e7779000245a9b903a6
# to use TOS image legally, one probably must own real Atari ST...
Source1:	%{tosarchname}
NoSource:	1
Patch0:		%{name}-nox.patch
Patch1:		%{name}-svga.patch
Patch2:		%{name}-link.patch
Patch3:		%{name}-segv.patch
URL:		http://www.complang.tuwien.ac.at/nino/stonx.html
BuildRequires:	autoconf >= 2.59-9
BuildRequires:	rpmbuild(macros) >= 1.268
%{?with_svga:BuildRequires:	svgalib-devel}
BuildRequires:	unzip
BuildRequires:	xorg-lib-libXext-devel
Requires(post,postun):	fontpostinst
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
STonX is a software emulator, which runs on Unix workstations with the
X Window system%{?with_svga: or svgalib}, and emulates an Atari ST
computer.

%description -l pl.UTF-8
STonX jest programowym emulatorem komputera Atari ST, działającym na
Uniksach z X Window System%{?with_svga: lub svgalib}.

%prep
%setup -q -a1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

mv -f %{tosfilename} tos.img

%build
%{__autoconf}
%configure

%{__make} \
	OPT="%{rpmcflags}" \
	REGS="%{!?debug:-fomit-frame-pointer}" \
	%{?with_svga:USE_SVGALIB=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir}/STonX,%{_bindir},%{_fontsdir}/misc}

install stonx tos.img cartridge.img Keysyms $RPM_BUILD_ROOT%{_libdir}/STonX

gzip -9nf data/*.pcf
install data/*.pcf.gz $RPM_BUILD_ROOT%{_fontsdir}/misc

cat > $RPM_BUILD_ROOT%{_bindir}/stonx <<'EOF'
#!/bin/sh
cd %{_libdir}/STonX

%{?with_svga:if [ -z "$DISPLAY" ]; then exec ./stonx -svga ; fi}
exec ./stonx
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
fontpostinst misc

%postun
fontpostinst misc

%files
%defattr(644,root,root,755)
%doc docs/{PROGRAMS,README,RELEASE_NOTES,TOS-VERSIONS}
%attr(755,root,root) %{_bindir}/*
%dir %{_libdir}/STonX
%attr(755,root,root) %{_libdir}/STonX/stonx
%{_libdir}/STonX/*.img
%{_libdir}/STonX/Keysyms
%{_fontsdir}/misc/*.pcf.gz
