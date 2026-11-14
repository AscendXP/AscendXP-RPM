# AscendXP-RPM

**RPM packaging by AscendXP.**

A collection of RPM packages and build configurations developed for my own use and shared with fellow Linux users, primarily targeting Fedora.

## Installation (Fedora / RHEL Standard)

Enable the Copr repository and install all required packages:

```bash
sudo dnf copr enable ascendxps/AscendXP
sudo dnf install (the package you want)
```

## Installation (Fedora Atomic / Universal Blue / Bazzite)

Fedora Atomic, Universal Blue, and Bazzite systems use `rpm-ostree` for package layering.

Enable the Copr repository and install the AKMOD package:

```bash
sudo curl -sL https://copr.fedorainfracloud.org/coprs/ascendxps/AscendXP/repo/fedora-$(rpm -E %fedora)/ascendxps-AscendXP-fedora-$(rpm -E %fedora).repo -o /etc/yum.repos.d/_copr_ascendxps-AscendXP.repo
sudo rpm-ostree install (the package you want)
```
