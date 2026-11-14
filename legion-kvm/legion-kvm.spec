Name:           legion-kvm
Version:        0.0.0
Release:        1%{?dist}
Summary:        Run Windows applications through Proton in a Linux KVM guest

# Provisional license; bundled component licenses still need auditing.
License:        AGPL-3.0-only
URL:            https://github.com/brcly/legion-kvm

Source0:        https://github.com/AscendXP/AscendXP-RPM/raw/main/legion-kvm/legion

ExclusiveArch:  x86_64
%global debug_package %{nil}
%global __strip /bin/true
%define _build_id_links none

%description
Legion runs Windows applications through Proton inside a Linux KVM
guest, providing local desktop windows and shared graphics access.

%prep
# Nothing to extract or patch

%build
# Nothing to compile; using pre-built binary from GitHub Actions

%install
%__install -Dpm0755 %{SOURCE0} %{buildroot}%{_bindir}/legion

%files
%{_bindir}/legion
