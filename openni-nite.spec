#define gitrev 894cea01

# Disable debuginfo because
# Empty %%files file /builddir/build/BUILD/NITE-1.4.1.2/debugsourcefiles.list
%global                debug_package %{nil}


Name:           openni-nite
Version:        1.4.1.2
Release:        13%{?dist}
Summary:        OpenNI-based toolbox for hand movement tracking
Group:          System Environment/Libraries
License:        Proprietary
URL:            http://www.openni.org
Source0:        http://www.openni.org/downloads/NITE-Bin-Linux64-v%{version}.tar.bz2
Source1:        http://www.openni.org/downloads/NITE-Bin-Linux32-v%{version}.tar.bz2
Patch0:         NITE-1.4.1.2-fedora.patch
ExclusiveArch:  x86_64 i386 i686

Requires:       openni >= 1.3.2.1

%description
NITE is a toolbox to allow application to build flows based on the user's
hands movement. The hand movement is understood as gestures and is tracked,
to provide hand points. NITE works over OpenNI.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        examples
Summary:        Sample programs for %{name}
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}

%description    examples
The %{name}-examples package contains sample programs for OpenNI Nite.


%prep
%ifarch x86_64
%define srcnum 0
%else
%define srcnum 1
%endif
%setup -q -c -n NITE-%{version} -T -a %{srcnum}
%patch0 -p1 -b .fedora


%build
sed -i "s|^make$|make CFLAGS_EXT=\\\"%{optflags} -I$PWD/Include\\\" LDFLAGS_EXT=\\\"-L$RPM_BUILD_ROOT%{_libdir}\\\" SSE_GENERATION=2 DEBUG=1|" install.sh


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}/nite
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/openni/XnVFeatures
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/openni/XnVHandGenerator

# We omit .net stuff for now
#rm -f $RPM_BUILD_ROOT%{_libdir}/XnVNite.net.dll

for l in XnVCNITE XnVFeatures XnVHandGenerator XnVNite; do
  install -m 0755 Bin/lib${l}_1_4_1.so $RPM_BUILD_ROOT%{_libdir}
done

cp -a Data/* $RPM_BUILD_ROOT%{_sysconfdir}/openni
cp -a Features_1_4_1/Data/* $RPM_BUILD_ROOT%{_sysconfdir}/openni/XnVFeatures
cp -a Hands_1_4_1/Data/* $RPM_BUILD_ROOT%{_sysconfdir}/openni/XnVHandGenerator

cp -a Include/* $RPM_BUILD_ROOT%{_includedir}/nite

for s in Boxes CircleControl Players PointServer PointViewer SceneAnalysis SingleControl TrackPad; do
  install -m 0755 Samples/Bin/Release/Sample-$s $RPM_BUILD_ROOT%{_bindir}/Nite$s;
done


%post
/sbin/ldconfig
if [ $1 == 1 ]; then
  for l in XnVCNITE XnVFeatures XnVHandGenerator XnVNite; do
    niReg %{_libdir}/lib${l}_1_4_1.so %{_sysconfdir}/openni/XnVFeatures
  done
  niLicense PrimeSense "0KOIk2JeIBYClPWVnMoRKn5cdY4="
fi


%preun
if [ $1 == 0 ]; then
  for l in XnVCNITE XnVFeatures XnVHandGenerator XnVNite; do
    niReg -u %{_libdir}/lib${l}_1_4_1.so
  done
fi


%postun -p /sbin/ldconfig


%files
%config(noreplace) %{_sysconfdir}/openni/*
%{_libdir}/*.so*

%files devel
%doc Documentation/html
%{_includedir}/*

%files examples
%{_bindir}/*

%changelog
* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1.2-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.4.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 18 2017 Sérgio Basto <sergio@serjux.com> - 1.4.1.2-8
- Fixup rpm setup macro use -a instead -b
- Package clean up
- Disable debuginfo due a build error with empty file debugsourcefiles.list

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.4.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 1.4.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1.2-4
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Mar 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1.2-3
- Rebuilt for c++ ABI breakage

* Wed Feb 08 2012 Tim Niemueller <tim@niemueller.de> - 1.4.1.2-2
- Apply minor updates from rpmfusion review

* Tue Aug 30 2011 Tim Niemueller <tim@niemueller.de> - 1.4.1.2-1
- Update to 1.4.1.2

* Thu Mar 03 2011 Tim Niemueller <tim@niemueller.de> - 1.3.0.18-2
- Mark config files
- Comment with original download URLs

* Tue Jan 25 2011 Tim Niemueller <tim@niemueller.de> - 1.3.0.18-1
- Initial revision

