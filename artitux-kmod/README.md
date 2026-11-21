# Fedora Artitux Kernel Module

This project provides kernel module packaging for Artitux, specifically targeted at **Universal Blue** and **Fedora Atomic Desktop** images, where **DKMS is not available**.

**Description:**  
Artitux kernel module (Developed by Lumice). Provides per-process XCR0 and UMIP SGDT/SIDT handling through a native kernel module and systemd service integration.

## Installation (Fedora / RHEL Standard)

Enable the Copr repository, install the required packages, and run the upstream installer:

```bash
sudo dnf copr enable ascendxps/AscendXP
sudo dnf install akmod-artitux artitux-kmod-common
curl -fsSL https://raw.githubusercontent.com/Lumice/artitux/main/install.sh | bash
```

## Installation (Fedora Atomic / Universal Blue / Bazzite)

Fedora Atomic, Universal Blue, and Bazzite systems use `rpm-ostree` for package layering.

Enable the Copr repository, install the AKMOD package, and run the upstream installer:

```bash
sudo curl -sL https://copr.fedorainfracloud.org/coprs/ascendxps/AscendXP/repo/fedora-$(rpm -E %fedora)/ascendxps-AscendXP-fedora-$(rpm -E %fedora).repo -o /etc/yum.repos.d/_copr_ascendxps-AscendXP.repo
sudo rpm-ostree install akmod-artitux artitux-kmod-common
curl -fsSL https://raw.githubusercontent.com/Lumice/artitux/main/install.sh | bash
```

**Reboot the system to apply the changes:**

```bash
systemctl reboot
```

**After installation, enable and start the Artitux service:**

```bash
sudo systemctl enable --now artitux.service
```
