%undefine _annotated_build

%define base_drivers nouveau,r100,r200

%ifarch %{ix86} x86_64
%define platform_drivers ,i915,i965
%define with_vmware 1
%define vulkan_drivers intel,amd
%else
%define vulkan_drivers amd
%endif

%ifarch %{arm} aarch64
%define with_etnaviv   1
%define with_freedreno 1
%define with_tegra     1
%define with_vc4       1
%endif

%ifnarch %{x86}
%global with_asm 1
%endif

%define dri_drivers %{?base_drivers}%{?platform_drivers}

%global sanitize 0

%define with_opencl 0
%define with_xa        1
%define with_omx       1

Name:           mesa
Summary:        Mesa graphics libraries
Version:        18.3.6
Release:        2
License:        MIT
URL:            https://www.mesa3d.org
Source0:        https://mesa.freedesktop.org/archive/%{name}-%{version}.tar.xz
Source3:        Makefile


Patch3:         0003-evergreen-big-endian.patch
Patch7:         0001-gallium-Disable-rgb10-configs-by-default.patch

BuildRequires:  gcc gcc-c++ automake autoconf libtool kernel-headers libdrm-devel libXxf86vm-devel expat-devel
BuildRequires:  xorg-x11-proto-devel imake libselinux-devel libXrandr-devel libXext-devel libXfixes-devel 
BuildRequires:  libXi-devel libXmu-devel libxshmfence-devel elfutils python3 gettext llvm-devel clang-devel
BuildRequires:  elfutils-libelf-devel libudev-devel bison flex meson gettext python3-devel libXdamage-devel
BuildRequires:  wayland-devel wayland-protocols-devel libvdpau-devel libva-devel zlib-devel 
BuildRequires:  libomxil-bellagio-devel libclc-devel vulkan-devel python3-mako libX11-devel 
%if 0%{?with_opencl}
BuildRequires:  opencl-filesystem
%endif

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

%package khr-devel
Summary:        Mesa Khronos development headers

%description khr-devel
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
Requires:       %{name}-khr-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
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
Requires:       %{name}-khr-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
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
Requires:       %{name}-khr-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
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

%if 0%{?with_opencl}
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
%endif

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


%build
%meson -Dcpp_std=gnu++11 \
  -Dplatforms=x11,wayland,drm,surfaceless \
  -Ddri3=true \
  -Ddri-drivers=%{?dri_drivers} \
  -Dgallium-drivers=swrast,virgl,r300,nouveau%{?with_vmware:,svga},radeonsi,r600%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv,imx}%{?with_tegra:,tegra}%{?with_vc4:,vc4} \
  -Dgallium-vdpau=true \
  -Dgallium-xvmc=false \
  -Dgallium-omx=%{?with_omx:bellagio}%{!?with_omx:disabled} \
  -Dgallium-va=true \
  -Dgallium-xa=true \
  -Dgallium-nine=true \
  -Dgallium-opencl=%{?with_opencl:icd}%{!?with_opencl:disabled} \
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dshared-glapi=true \
  -Dgles1=false \
  -Dgles2=true \
  -Dopengl=true \
  -Dgbm=true \
  -Dglx=dri \
  -Degl=true \
  -Dglvnd=true \
  -Dasm=%{?with_asm:true}%{!?with_asm:false} \
  -Dllvm=true \
  -Dshared-llvm=true \
  -Dvalgrind=%{?with_valgrind:true}%{!?with_valgrind:false} \
  -Dbuild-tests=false \
  -Dselinux=true \
  -Dosmesa=gallium \
  %{nil}
%meson_build   

%install
%meson_install

rm -f %{buildroot}%{_libdir}/vdpau/*.so
rm -f %{buildroot}%{_libdir}/libGLX_mesa.so
rm -f %{buildroot}%{_libdir}/libEGL_mesa.so
rm -f %{buildroot}%{_libdir}/libGLES*

ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

rm -f %{buildroot}%{_includedir}/GL/w*.h

mkdir -p %{buildroot}/%{_includedir}/vulkan/
rm -f %{buildroot}/%{_includedir}/vulkan/vk_platform.h
rm -f %{buildroot}/%{_includedir}/vulkan/vulkan.h

%if ! 0%{?with_opencl}
rm -f %{buildroot}%{_libdir}/libMesaOpenCL.so.*
rm -f %{buildroot}%{_sysconfdir}/OpenCL/vendors/mesa.icd
rm -f %{buildroot}%{_libdir}/libMesaOpenCL.so
%endif

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
%if 0%{?with_opencl}
%ldconfig_scriptlets libOpenCL
%endif

%files filesystem
%defattr(-,root,root)
%doc docs/libGL.txt
%license docs/license.html
%dir %{_libdir}/dri
%dir %{_libdir}/vdpau

%files khr-devel
%dir %{_includedir}/KHR
%{_includedir}/KHR/khrplatform.h

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

%if 0%{?with_opencl}
%files libOpenCL
%defattr(-,root,root)
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd

%files libOpenCL-devel
%defattr(-,root,root)
%{_libdir}/libMesaOpenCL.so
%endif

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
%dir %{_datadir}/drirc.d
%{_datadir}/drirc.d/00-mesa-defaults.conf
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
* Wed Jun 03 2020 songnannan <songnannan2@huawei.com> - 18.3.6-2
- add mesa-khr-header subpackage to hold <KHR/khrplatform.h>

* Tue Jun 02 2020 songnannan <songnannan2@huawei.com> - 18.3.6-1
- update to 18.3.6

* Wed Jan 15 2020 openEuler Buildteam <buildteam@openeuler.org> - 18.2.2-6
- disable opencl

* Sat Oct 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 18.2.2-5
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add the license file

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 18.2.2-4
- Type: enhance
- Id:NA
- SUG:NA
- DESC: rewrite it without merging packages

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 18.2.2-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC: restore previous version of 18.2.2-1

* Sat Sep 21 2019 openEuler Buildteam <buildteam@openeuler.org> - 18.2.2-2
- Package init
