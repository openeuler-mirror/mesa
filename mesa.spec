%undefine _annotated_build

%define base_drivers swrast,nouveau,radeon,r200

%ifarch %{ix86} x86_64
%define platform_drivers ,i915,i965
%define with_vmware 1
%define vulkan_drivers --with-vulkan-drivers=intel,radeon
%else
%define vulkan_drivers --with-vulkan-drivers=radeon
%endif

%ifarch %{arm} aarch64
%define with_etnaviv   1
%define with_freedreno 1
%define with_tegra     1
%define with_vc4       1
%endif

%define dri_drivers --with-dri-drivers=%{?base_drivers}%{?platform_drivers}

%global sanitize 0

Name:           mesa
Summary:        Mesa graphics libraries
Version:        18.2.2
Release:        4
License:        MIT
URL:            https://www.mesa3d.org
Source0:        %{name}-%{version}.tar.xz
Source1:        vl_decoder.c
Source2:        vl_mpeg12_decoder.c
Source3:        Makefile
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source4 contains email correspondence clarifying the license terms.
Source4:        Mesa-MLAA-License-Clarification-Email.txt

Patch1:         0001-llvm-SONAME-without-version.patch
Patch3:         0003-evergreen-big-endian.patch
Patch4:         0004-bigendian-assert.patch

# Disable rgb10 configs by default:
# https://bugzilla.redhat.com/show_bug.cgi?id=1560481
Patch7:         0001-gallium-Disable-rgb10-configs-by-default.patch

BuildRequires:  gcc gcc-c++ automake autoconf libtool kernel-headers libdrm-devel libXxf86vm-devel expat-devel
BuildRequires:  xorg-x11-proto-devel imake libselinux-devel libXrandr-devel libXext-devel libXfixes-devel libXdamage-devel
BuildRequires:  libXi-devel libXmu-devel libxshmfence-devel elfutils python3 python2 gettext llvm-devel clang-devel
BuildRequires:  elfutils-libelf-devel python3-libxml2 python2-libxml2 libudev-devel bison flex
BuildRequires:  wayland-devel wayland-protocols-devel libvdpau-devel libva-devel zlib-devel
BuildRequires:  libomxil-bellagio-devel libclc-devel opencl-filesystem vulkan-devel python3-mako python2-mako
%ifarch %{valgrind_arches}
BuildRequires:  valgrind-devel
%endif
BuildRequires:  libglvnd-devel

%description
%{summary}.

%package        filesystem
Summary:        Mesa driver filesystem
Provides:       mesa-dri-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-dri-filesystem < %{?epoch:%{epoch}:}%{version}-%{release}

%description    filesystem
%{summary}.

%package        libGL
Summary:        Mesa libGL runtime libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-glx%{?_isa} >= 1:1.0.1-0.9

%description    libGL
%{summary}.

%package        libGL-devel
Summary:        Mesa libGL development package
Requires:       %{name}-libGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa}
Provides:       libGL-devel libGL-devel%{?_isa}

%description    libGL-devel
%{summary}.

%package        libEGL
Summary:        Mesa libEGL runtime libraries
Requires:       libglvnd-egl%{?_isa}

%description    libEGL
%{summary}.

%package        libEGL-devel
Summary:        Mesa libEGL development package
Requires:       %{name}-libEGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa}
Provides:       libEGL-devel libEGL-devel%{?_isa}

%description    libEGL-devel
%{summary}.

%package        libGLES
Summary:        Mesa libGLES runtime libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-gles%{?_isa}

%description    libGLES
%{summary}.

%package        libGLES-devel
Summary:        Mesa libGLES development package
Requires:       %{name}-libGLES%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa}
Provides:       libGLES-devel libGLES-devel%{?_isa}

%description    libGLES-devel
%{summary}.

%package        dri-drivers
Summary:        Mesa-based DRI drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    dri-drivers
%{summary}.

%package        omx-drivers
Summary:        Mesa-based OMX drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    omx-drivers
%{summary}.

%package        vdpau-drivers
Summary:        Mesa-based VDPAU drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description vdpau-drivers
%{summary}.

%package        libOSMesa
Summary:        Mesa offscreen rendering libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libOSMesa libOSMesa%{?_isa}

%description    libOSMesa
%{summary}.

%package        libOSMesa-devel
Summary:        Mesa offscreen rendering development package
Requires:       %{name}-libOSMesa%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    libOSMesa-devel
%{summary}.

%package        libgbm
Summary:        Mesa gbm runtime library
Provides:       libgdm libgbm%{?_isa}

%description    libgbm
%{summary}.

%package        libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm-devel libgbm-devel%{?_isa}

%description    libgbm-devel
%{summary}.

%package        libxatracker
Summary:        Mesa XA state tracker
Provides:       libxatracker libxatracker%{?_isa}

%description    libxatracker
%{summary}.

%package        libxatracker-devel
Summary:        Mesa XA state tracker development package
Requires:       %{name}-libxatracker%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libxatracker-devel libxatracker-devel%{?_isa}

%description    libxatracker-devel
%{summary}.

%package        libglapi
Summary:        Mesa shared glapi
Provides:       libglapi libglapi%{?_isa}

%description    libglapi
%{summary}.

%package        libOpenCL
Summary:        Mesa OpenCL runtime library
Requires:       ocl-icd%{?_isa}
Requires:       libclc%{?_isa}
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       opencl-filesystem

%description    libOpenCL
%{summary}.

%package        libOpenCL-devel
Summary:        Mesa OpenCL development package
Requires:       %{name}-libOpenCL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    libOpenCL-devel
%{summary}.

%package        libd3d
Summary:        Mesa Direct3D9 state tracker

%description    libd3d
%{summary}.

%package        libd3d-devel
Summary:        Mesa Direct3D9 state tracker development package
Requires:       %{name}-libd3d%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description    libd3d-devel
%{summary}.

%package        vulkan-drivers
Summary:        Mesa Vulkan drivers
Requires:       vulkan%{?_isa}

%description    vulkan-drivers
The drivers with support for the Vulkan API.

%package        vulkan-devel
Summary:        Mesa Vulkan development files
Requires:       %{name}-vulkan-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       vulkan-devel

%description    vulkan-devel
Headers for development with the Vulkan API.

%prep
%autosetup -n %{name}-%{version} -p1

cmp %{SOURCE1} src/gallium/auxiliary/vl/vl_decoder.c
cmp %{SOURCE2} src/gallium/auxiliary/vl/vl_mpeg12_decoder.c
cp %{SOURCE4} docs/

%build
cmp %{SOURCE1} src/gallium/auxiliary/vl/vl_decoder.c
cmp %{SOURCE2} src/gallium/auxiliary/vl/vl_mpeg12_decoder.c

autoreconf -ivf

%ifarch %{ix86}
%global asm_flags --disable-asm
%endif

%configure \
    %{?asm_flags} \
    --enable-libglvnd \
    --enable-selinux \
    --enable-gallium-osmesa \
    --with-dri-driverdir=%{_libdir}/dri \
    --enable-egl \
    --disable-gles1 \
    --enable-gles2 \
    --disable-xvmc \
    --enable-vdpau \
    --enable-va \
    --with-platforms=x11,drm,surfaceless,wayland \
    --enable-shared-glapi \
    --enable-gbm \
    --enable-omx-bellagio \
    --enable-opencl --enable-opencl-icd \
    --enable-glx-tls \
    --enable-texture-float=yes \
    %{?vulkan_drivers} \
    --enable-llvm \
    --enable-llvm-shared-libs \
    --enable-dri \
    --enable-xa \
    --enable-nine \
    --with-gallium-drivers=%{?with_vmware:svga,}radeonsi,r600,swrast,%{?with_freedreno:freedreno,}%{?with_etnaviv:etnaviv,imx,}%{?with_tegra:tegra,}%{?with_vc4:vc4,}virgl,r300,nouveau \
    %{?dri_drivers}

%make_build MKDEP=/bin/true V=1

%install
%make_install

rm -f %{buildroot}%{_libdir}/vdpau/*.so
rm -f %{buildroot}%{_libdir}/libGLX_mesa.so
rm -f %{buildroot}%{_libdir}/libEGL_mesa.so
rm -f %{buildroot}%{_libdir}/libGLES*

ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

rm -f %{buildroot}%{_includedir}/GL/w*.h

mkdir -p %{buildroot}/%{_includedir}/vulkan/
rm -f %{buildroot}/%{_includedir}/vulkan/vk_platform.h
rm -f %{buildroot}/%{_includedir}/vulkan/vulkan.h

%delete_la

pushd %{buildroot}%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd

%ldconfig_scriptlets libglapi
%ldconfig_scriptlets libOSMesa
%ldconfig_scriptlets libgbm
%ldconfig_scriptlets libxatracker
%ldconfig_scriptlets libOpenCL

%files filesystem
%defattr(-,root,root)
%doc docs/Mesa-MLAA-License-Clarification-Email.txt
%dir %{_libdir}/dri
%dir %{_libdir}/vdpau

%files libGL
%defattr(-,root,root)
%{_libdir}/libGLX_mesa.so.0*
%{_libdir}/libGLX_system.so.0*

%files libGL-devel
%defattr(-,root,root)
%{_includedir}/GL/gl*.h
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/libglapi.so
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/pkgconfig/gl.pc

%files libEGL
%defattr(-,root,root)
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libEGL_mesa.so.0*

%files libEGL-devel
%defattr(-,root,root)
%{_includedir}/EGL/egl*.h
%{_includedir}/KHR/khrplatform.h
%{_libdir}/pkgconfig/egl.pc

%files libGLES
%defattr(-,root,root)

%files libGLES-devel
%defattr(-,root,root)
%{_includedir}/GLES*/gl*.h
%{_libdir}/pkgconfig/glesv2.pc

%files libglapi
%defattr(-,root,root)
%{_libdir}/libglapi.so.0*

%files libOSMesa
%defattr(-,root,root)
%{_libdir}/libOSMesa.so.8*

%files libOSMesa-devel
%defattr(-,root,root)
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%files libgbm
%defattr(-,root,root)
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*

%files libgbm-devel
%defattr(-,root,root)
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%files libxatracker
%defattr(-,root,root)
%{_libdir}/libxatracker.so.2*

%files libxatracker-devel
%defattr(-,root,root)
%{_libdir}/libxatracker.so
%{_includedir}/xa_*.h
%{_libdir}/pkgconfig/xatracker.pc

%files libOpenCL
%defattr(-,root,root)
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd

%files libOpenCL-devel
%defattr(-,root,root)
%{_libdir}/libMesaOpenCL.so

%files libd3d
%defattr(-,root,root)
%{_libdir}/d3d/*.so.*

%files libd3d-devel
%defattr(-,root,root)
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so

%files dri-drivers
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/drirc
%{_libdir}/dri/radeon_dri.so
%{_libdir}/dri/r200_dri.so
%{_libdir}/dri/nouveau_vieux_dri.so
%{_libdir}/dri/r300_dri.so
%{_libdir}/dri/r600_dri.so
%{_libdir}/dri/radeonsi_dri.so
%{_libdir}/dri/nouveau_dri.so
%{_libdir}/dri/nouveau_drv_video.so
%{_libdir}/dri/r600_drv_video.so
%{_libdir}/dri/radeonsi_drv_video.so
%{_libdir}/gallium-pipe/*.so
%{_libdir}/dri/kms_swrast_dri.so
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/virtio_gpu_dri.so
%ifarch %{ix86} x86_64
%{_libdir}/dri/i915_dri.so
%{_libdir}/dri/i965_dri.so
%{_libdir}/dri/vmwgfx_dri.so
%endif
%ifarch %{arm} aarch64
%{_libdir}/dri/vc4_dri.so
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%{_libdir}/dri/etnaviv_dri.so
%{_libdir}/dri/imx-drm_dri.so
%{_libdir}/dri/tegra_dri.so
%endif

%files omx-drivers
%defattr(-,root,root)
%{_libdir}/bellagio/libomx_mesa.so

%files vdpau-drivers
%defattr(-,root,root)
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%{_libdir}/vdpau/libvdpau_r*.so.1*
%if 0%{?with_tegra}
%{_libdir}/vdpau/libvdpau_tegra.so.1*
%endif

%files vulkan-drivers
%ifarch %{ix86} x86_64
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%endif
%{_libdir}/libvulkan_radeon.so
%{_datadir}/vulkan/icd.d/radeon_icd.*.json

%files vulkan-devel
%{_includedir}/vulkan/

%changelog
* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 19.2.2-4
- Type: enhance
- Id:NA
- SUG:NA
- DESC: rewrite it without merging packages

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 19.2.2-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: restore previous version of 18.2.2-1

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 18.2.2-2
- Package init
