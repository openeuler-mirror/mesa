%global llvm_toolset %{nil}
%global llvm_pkg_prefix %{nil}

%ifarch s390x
%define with_hardware 0
%else
%define with_hardware 1
%define with_vdpau 1
%endif

%ifarch %{ix86} x86_64
%define platform_drivers i965
%define with_vmware 1
%define with_xa     1
%define with_iris   1
%endif

%ifarch %{ix86} x86_64
%define with_vulkan_hw 1
%else
%define with_vulkan_hw 0
%endif

%ifarch %{arm} aarch64
%define with_xa        1
%endif

%global dri_drivers %{?platform_drivers}

%if 0%{?with_vulkan_hw}
%define vulkan_drivers swrast,intel,amd
%else
%define vulkan_drivers swrast
%endif

%global sanitize 0

Name:           mesa
Summary:        Mesa graphics libraries
Version:        21.3.1
Release:        1

License:        MIT
URL:            http://www.mesa3d.org
Source0:        https://mesa.freedesktop.org/archive/%{name}-%{version}.tar.xz

Patch1:         backport-fix-build-err-on-arm.patch
Patch2:         0001-evergreen-big-endian.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++

BuildRequires:  meson >= 0.45
%if %{with_hardware}
BuildRequires:  kernel-headers
%endif
BuildRequires:  libdrm-devel >= 2.4.103
BuildRequires:  libXxf86vm-devel
BuildRequires:  expat-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libselinux-devel
BuildRequires:  libXext-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXmu-devel
BuildRequires:  libxshmfence-devel
BuildRequires:  elfutils
BuildRequires:  python3-devel
BuildRequires:  gettext
BuildRequires: %{llvm_pkg_prefix}llvm-devel >= 3.4-7
%if 0%{?with_opencl}
BuildRequires: %{llvm_pkg_prefix}clang-devel >= 3.0
%endif
BuildRequires: elfutils-libelf-devel
BuildRequires: libudev-devel
BuildRequires: bison flex
BuildRequires: pkgconfig(wayland-client)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(wayland-protocols)
%if 0%{?with_vdpau}
BuildRequires: libvdpau-devel
%endif
%if 0%{?with_vaapi}
BuildRequires: libva-devel
%endif
BuildRequires: pkgconfig(zlib)
%if 0%{?with_omx}
BuildRequires: libomxil-bellagio-devel
%endif
%if 0%{?with_opencl}
BuildRequires: libclc-devel opencl-filesystem
%endif
BuildRequires: python3-mako
%ifarch %{valgrind_arches}
BuildRequires: pkgconfig(valgrind)
%endif
BuildRequires: pkgconfig(libglvnd) >= 1.2.0

%if 0%{?rhel} == 7
BuildRequires: llvm-toolset-7-runtime
%enable_llvmtoolset7
%endif

%description
%{summary}.

%package filesystem
Summary:        Mesa driver filesystem
Provides:       mesa-dri-filesystem = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      mesa-dri-filesystem < %{?epoch:%{epoch}:}%{version}-%{release}

%description filesystem
%{summary}.

%package libGL
Summary:        Mesa libGL runtime libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-glx%{?_isa} >= 1:1.2.0-1
 
%description libGL
%{summary}.

%package libGL-devel
Summary:        Mesa libGL development package
Requires:       %{name}-libGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa} >= 1:1.2.0-1
Provides:       libGL-devel
Provides:       libGL-devel%{?_isa}

%description libGL-devel
%{summary}.

%package libEGL
Summary:        Mesa libEGL runtime libraries
Requires:       libglvnd-egl%{?_isa} >= 1:1.2.0-1

%description libEGL
%{summary}.

%package libEGL-devel
Summary:        Mesa libEGL development package
Requires:       %{name}-libEGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       libglvnd-devel%{?_isa} >= 1:1.2.0-1
Provides:       libEGL-devel
Provides:       libEGL-devel%{?_isa}

%description libEGL-devel
%{summary}.

%package dri-drivers
Summary:        Mesa-based DRI drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	libdrm >= 2.4.103

%description dri-drivers
%{summary}.

%if 0%{?with_omx}
%package omx-drivers
Summary:        Mesa-based OMX drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description omx-drivers
%{summary}.
%endif

%if 0%{?with_vdpau}
%package        vdpau-drivers
Summary:        Mesa-based VDPAU drivers
Requires:       %{name}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description vdpau-drivers
%{summary}.
%endif

%package libOSMesa
Summary:        Mesa offscreen rendering libraries
Requires:       %{name}-libglapi%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libOSMesa
Provides:       libOSMesa%{?_isa}

%description libOSMesa
%{summary}.

%package libOSMesa-devel
Summary:        Mesa offscreen rendering development package
Requires:       %{name}-libOSMesa%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libOSMesa-devel
%{summary}.

%package libgbm
Summary:        Mesa gbm runtime library
Provides:       libgbm
Provides:       libgbm%{?_isa}

%description libgbm
%{summary}.

%package libgbm-devel
Summary:        Mesa libgbm development package
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libgbm-devel
Provides:       libgbm-devel%{?_isa}

%description libgbm-devel
%{summary}.

%if 0%{?with_xa}
%package libxatracker
Summary:        Mesa XA state tracker
Provides:       libxatracker
Provides:       libxatracker%{?_isa}

%description libxatracker
%{summary}.

%package libxatracker-devel
Summary:        Mesa XA state tracker development package
Requires:       %{name}-libxatracker%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       libxatracker-devel
Provides:       libxatracker-devel%{?_isa}

%description libxatracker-devel
%{summary}.
%endif

%package libglapi
Summary:        Mesa shared glapi
Provides:       libglapi
Provides:       libglapi%{?_isa}

%description libglapi
%{summary}.

%if 0%{?with_opencl}
%package libOpenCL
Summary:        Mesa OpenCL runtime library
Requires:       ocl-icd%{?_isa}
Requires:       libclc%{?_isa}
Requires:       %{name}-libgbm%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       opencl-filesystem

%description libOpenCL
%{summary}.

%package libOpenCL-devel
Summary:        Mesa OpenCL development package
Requires:       %{name}-libOpenCL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libOpenCL-devel
%{summary}.
%endif

%if 0%{?with_nine}
%package libd3d
Summary:        Mesa Direct3D9 state tracker

%description libd3d
%{summary}.

%package libd3d-devel
Summary:        Mesa Direct3D9 state tracker development package
Requires:       %{name}-libd3d%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description libd3d-devel
%{summary}.
%endif

%package vulkan-drivers
Summary:        Mesa Vulkan drivers
Requires:       vulkan%{_isa}

%description vulkan-drivers
The drivers with support for the Vulkan API.

%if 0%{?with_vulkan_hw}
%package vulkan-devel
Summary:        Mesa Vulkan development files
Requires:       %{name}-vulkan-drivers%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       vulkan-devel

%description vulkan-devel
Headers for development with the Vulkan API.
%endif

%prep
%autosetup -n %{name}-%{version} -p1

# Make sure the build uses gnu++14 as llvm 10 headers require that
sed -i -e 's/cpp_std=gnu++11/cpp_std=gnu++14/g' meson.build

%build
export ASFLAGS="--generate-missing-build-notes=yes"
%meson -Dcpp_std=gnu++14 \
  -Db_ndebug=true \
  -Dplatforms=x11,wayland \
  -Ddri3=enabled \
  -Ddri-drivers=%{?dri_drivers} \
  -Dosmesa=true \
%if 0%{?with_hardware}
  -Dgallium-drivers=swrast%{?with_iris:,iris},virgl,nouveau%{?with_vmware:,svga},radeonsi,r600%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_kmsro:,kmsro} \
%else
  -Dgallium-drivers=swrast,virgl \
%endif
  -Dgallium-vdpau=%{?with_vdpau:true}%{!?with_vdpau:false} \
  -Dgallium-xvmc=false \
  -Dgallium-omx=%{?with_omx:bellagio}%{!?with_omx:disabled} \
  -Dgallium-va=%{?with_vaapi:true}%{!?with_vaapi:false} \
  -Dgallium-xa=%{?with_xa:true}%{!?with_xa:false} \
  -Dgallium-nine=%{?with_nine:true}%{!?with_nine:false} \
  -Dgallium-opencl=%{?with_opencl:icd}%{!?with_opencl:disabled} \
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dvulkan-layers=device-select \
  -Dshared-glapi=enabled \
  -Dgles1=disabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=true \
  -Dglvnd=true \
  -Dmicrosoft-clc=disabled \
  -Dllvm=true \
  -Dshared-llvm=true \
  -Dvalgrind=%{?with_valgrind:true}%{!?with_valgrind:false} \
  -Dbuild-tests=false \
  -Dselinux=true \
  %{nil}
%meson_build

%check
%meson_test

%install
%meson_install
# libvdpau opens the versioned name, don't bother including the unversioned
rm -vf %{buildroot}%{_libdir}/vdpau/*.so
# likewise glvnd
rm -vf %{buildroot}%{_libdir}/libGLX_mesa.so
rm -vf %{buildroot}%{_libdir}/libEGL_mesa.so
# XXX can we just not build this
rm -vf %{buildroot}%{_libdir}/libGLES*

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

# strip out useless headers
rm -f %{buildroot}%{_includedir}/GL/w*.h

# these are shipped already in vulkan-devel
rm -f %{buildroot}/%{_includedir}/vulkan/vk_platform.h
rm -f %{buildroot}/%{_includedir}/vulkan/vulkan.h

# remove .la files
find %{buildroot} -name '*.la' -delete

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd %{buildroot}%{_libdir}
for i in libOSMesa*.so libGL.so ; do
    eu-findtextrel $i && exit 1
done

%files filesystem
%dir %{_libdir}/dri
%if %{with_hardware}
%if 0%{?with_vdpau}
%dir %{_libdir}/vdpau
%endif
%endif

%files libGL
%{_libdir}/libGLX_mesa.so.0*
%{_libdir}/libGLX_system.so.0*
%files libGL-devel
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h
%{_libdir}/pkgconfig/dri.pc
%{_libdir}/libglapi.so

%files libEGL
%{_datadir}/glvnd/egl_vendor.d/50_mesa.json
%{_libdir}/libEGL_mesa.so.0*
%files libEGL-devel
%dir %{_includedir}/EGL
%{_includedir}/EGL/eglmesaext.h
%{_includedir}/EGL/eglextchromium.h

%post libglapi -p /sbin/ldconfig
%postun libglapi -p /sbin/ldconfig
%files libglapi
%{_libdir}/libglapi.so.0
%{_libdir}/libglapi.so.0.*

%post libOSMesa -p /sbin/ldconfig
%postun libOSMesa -p /sbin/ldconfig
%files libOSMesa
%{_libdir}/libOSMesa.so.8*
%files libOSMesa-devel
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%post libgbm -p /sbin/ldconfig
%postun libgbm -p /sbin/ldconfig
%files libgbm
%{_libdir}/libgbm.so.1
%{_libdir}/libgbm.so.1.*
%files libgbm-devel
%{_libdir}/libgbm.so
%{_includedir}/gbm.h
%{_libdir}/pkgconfig/gbm.pc

%if 0%{?with_xa}
%post libxatracker -p /sbin/ldconfig
%postun libxatracker -p /sbin/ldconfig
%files libxatracker
%if %{with_hardware}
%{_libdir}/libxatracker.so.2
%{_libdir}/libxatracker.so.2.*
%endif

%files libxatracker-devel
%if %{with_hardware}
%{_libdir}/libxatracker.so
%{_includedir}/xa_tracker.h
%{_includedir}/xa_composite.h
%{_includedir}/xa_context.h
%{_libdir}/pkgconfig/xatracker.pc
%endif
%endif

%if 0%{?with_opencl}
%post libOpenCL -p /sbin/ldconfig
%postun libOpenCL -p /sbin/ldconfig
%files libOpenCL
%{_libdir}/libMesaOpenCL.so.*
%{_sysconfdir}/OpenCL/vendors/mesa.icd
%files libOpenCL-devel
%{_libdir}/libMesaOpenCL.so
%endif

%if 0%{?with_nine}
%files libd3d
%dir %{_libdir}/d3d/
%{_libdir}/d3d/*.so.*
 
%files libd3d-devel
%{_libdir}/pkgconfig/d3d.pc
%{_includedir}/d3dadapter/
%{_libdir}/d3d/*.so
%endif

%files dri-drivers
%dir %{_datadir}/drirc.d
%{_datadir}/drirc.d/00-mesa-defaults.conf
%if %{with_hardware}
%{_libdir}/dri/r600_dri.so
%{_libdir}/dri/radeonsi_dri.so
%ifarch %{ix86} x86_64
%{_libdir}/dri/i965_dri.so
%{_libdir}/dri/iris_dri.so
%endif
%if 0%{?with_vc4}
%{_libdir}/dri/vc4_dri.so
%endif
%if 0%{?with_freedreno}
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%endif
%if 0%{?with_etnaviv}
%{_libdir}/dri/etnaviv_dri.so
%{_libdir}/dri/imx-drm_dri.so
%endif
%{_libdir}/dri/nouveau_dri.so
%if 0%{?with_vmware}
%{_libdir}/dri/vmwgfx_dri.so
%endif
%endif
%{_libdir}/dri/kms_swrast_dri.so
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/virtio_gpu_dri.so

%if %{with_hardware}
%if 0%{?with_omx}
%files omx-drivers
%{_libdir}/bellagio/libomx_mesa.so
%endif
%if 0%{?with_vdpau}
%files vdpau-drivers
%{_libdir}/vdpau/libvdpau_nouveau.so.1*
%{_libdir}/vdpau/libvdpau_r600.so.1*
%{_libdir}/vdpau/libvdpau_radeonsi.so.1*
%endif
%endif

%files vulkan-drivers
%if 0%{?with_vulkan_hw}
%{_libdir}/libvulkan_intel.so
%{_libdir}/libvulkan_radeon.so
%ifarch x86_64
%{_datadir}/vulkan/icd.d/intel_icd.x86_64.json
%{_datadir}/vulkan/icd.d/radeon_icd.x86_64.json
%else
%{_datadir}/vulkan/icd.d/intel_icd.i686.json
%{_datadir}/vulkan/icd.d/radeon_icd.i686.json
%endif
%endif
%{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json
%{_libdir}/libVkLayer_MESA_device_select.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_device_select.json

%if 0%{?with_vulkan_hw}
%files vulkan-devel
%endif

%changelog
* Thu Sep 16 2021 hanhui <hanhui15@huawei.com> - 21.3.1-1
- upgrade to mesa-21.3.1
- enable check

* Thu Mar 25 2021 yanan <yanan@huawei.com> - 20.1.4-2
- optimize the mesa spec

* Sat Oct 10 2020 hanhui <hanhui15@huawei.com> - 20.1.4-1
- update to 20.1.4

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
