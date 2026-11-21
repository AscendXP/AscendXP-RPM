%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%global __akmods_install true
%endif

Name:           artitux-kmod
Version:        0.1.2
Release:        1%{?dist}
Summary:        Per-process XCR0 and UMIP kernel module

License:        AGPL-3.0-only
URL:            https://github.com/Lumice/artitux
Source0:        https://github.com/Lumice/artitux/archive/refs/heads/main.zip

BuildRequires:  kmodtool
BuildRequires:  unzip
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  elfutils-libelf-devel
BuildRequires:  systemd-rpm-macros

Requires:       akmods

ExclusiveArch:  x86_64

%{?systemd_ordering}
%{expand:%(kmodtool --target %{_target_cpu} --repo fedora --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null)}

%description
Artitux kernel module providing per-process XCR0=0x7
and UMIP SGDT/SIDT handling.

%package common
Summary:        Common files for Artitux kernel module
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description common
This package provides the systemd service and Polkit rule
for managing the Artitux kernel module.

%prep
%setup -q -c -T
unzip -q %{SOURCE0}

for kernel_version in %{?kernel_versions}; do
    kver="${kernel_version%%___*}"
    mkdir -p "_kmod_build_${kver}"
    cp -a artitux-main/kmod/. "_kmod_build_${kver}/"
done

%build
for kernel_version in %{?kernel_versions}; do
    kdir="${kernel_version##*___}"
    kver="${kernel_version%%___*}"

    make V=1 %{?_smp_mflags} \
        -C "_kmod_build_${kver}" \
        KREL="${kver}" \
        KDIR="${kdir}" \
        all
done

%install
for kernel_version in %{?kernel_versions}; do
    kver="${kernel_version%%___*}"

    install -D -m 0644 \
        "_kmod_build_${kver}/artitux_kmod.ko" \
        %{buildroot}%{kmodinstdir_prefix}/${kver}/%{kmodinstdir_postfix}/artitux_kmod.ko
done

%{?akmod_install}

# Systemd service
mkdir -p %{buildroot}/usr/lib/systemd/system

cat > %{buildroot}/usr/lib/systemd/system/artitux.service <<'EOF'
[Unit]
Description=Artitux Kernel Module
After=systemd-modules-load.service
Before=display-manager.service

[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/sbin/modprobe artitux_kmod
ExecStop=/usr/sbin/modprobe -r artitux_kmod

[Install]
WantedBy=multi-user.target
EOF

# Polkit rule
mkdir -p %{buildroot}/usr/share/polkit-1/rules.d

cat > %{buildroot}/usr/share/polkit-1/rules.d/10-artitux.rules <<'EOF'
polkit.addRule(function(action, subject) {
    if (action.id == "org.freedesktop.systemd1.manage-units" &&
        action.lookup("unit") == "artitux.service") {
        var verb = action.lookup("verb");
        if (verb == "start" || verb == "stop" || verb == "restart") {
            if (subject.isInGroup("wheel")) {
                return polkit.Result.YES;
            }
        }
    }
});
EOF

%post common
%systemd_post artitux.service

%preun common
%systemd_preun artitux.service

%postun common
%systemd_postun_with_restart artitux.service

%files common
/usr/lib/systemd/system/artitux.service
/usr/share/polkit-1/rules.d/10-artitux.rules

%changelog
* Sat Nov 21 2026 Lumice <maintainer@example.com> - 0.1.2-1
- Initial Fedora akmod packaging
- Add systemd service
- Add Polkit rule
