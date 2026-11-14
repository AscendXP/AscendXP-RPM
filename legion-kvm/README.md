# Legion KVM

Legion KVM was originally developed by [brcly](https://github.com/brcly).

Legion runs Windows applications through Proton inside a Linux KVM guest, with a local desktop window and shared graphics access. The launcher detects CPU topology and selects the graphics backend independently of CPU vendor.

The runtime includes NVIDIA and AMD graphics paths, guest initialization, CPU compatibility profiles, display transport, input, audio and directory sharing. AVX-512 is not a host requirement. The guest uses reduced XSTATE. Hardware and graphics-driver support depend on the selected backend.

For more information, documentation, and the original project, visit the [upstream Legion KVM repository](https://github.com/brcly/legion-kvm).
