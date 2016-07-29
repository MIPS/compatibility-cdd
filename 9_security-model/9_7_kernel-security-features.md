## 9.7\. Kernel Security Features

The Android Sandbox includes features that use the Security-Enhanced Linux
(SELinux) mandatory access control (MAC) system and other security features in
the Linux kernel. SELinux or any other security features implemented below the
Android framework:

*   MUST maintain compatibility with existing applications.
*   MUST NOT have a visible user interface when a security violation is
detected and successfully blocked, but MAY have a visible user interface when
an unblocked security violation occurs resulting in a successful exploit.
*   SHOULD NOT be user or developer configurable.

If any API for configuration of policy is exposed to an application that can
affect another application (such as a Device Administration API), the API MUST
NOT allow configurations that break compatibility.

Devices MUST implement SELinux or, if using a kernel other than Linux, an
equivalent mandatory access control system. Devices MUST also meet the
following requirements, which are satisfied by the reference implementation in
the upstream Android Open Source Project.

Device implementations:

*   MUST set SELinux to global enforcing mode.
*   MUST configure all domains in enforcing mode. No permissive mode domains
are allowed, including domains specific to a device/vendor.
*   MUST NOT modify, omit, or replace the neverallow rules present within the
external/sepolicy folder provided in the upstream Android Open Source Project
(AOSP) and the policy MUST compile with all neverallow rules present, for both
AOSP SELinux domains as well as device/vendor specific domains.

Device implementations SHOULD retain the default SELinux policy provided in the
external/sepolicy folder of the upstream Android Open Source Project and only
further add to this policy for their own device-specific configuration. Device
implementations MUST be compatible with the upstream Android Open Source
Project.
