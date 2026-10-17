---
name: netsupport-school-control
description: Help connect to, view, and control an authorized remote computer using NetSupport School Tutor and Student, including setup and connection troubleshooting.
---

# NetSupport School remote control

Help the user control a specific computer they are authorized to manage using NetSupport School. Identify the target by its displayed name and confirm the requested action and scope before interacting. Respect any Student-side connection acknowledgment, credentials, and access controls; do not bypass them. Do not deploy software, change security or network policy, transfer files, lock devices, or affect multiple computers unless the user has requested or authorized that action.

## Work with the available interface

Determine whether a usable desktop-control tool is actually available. If it is, inspect the current screen and operate the Tutor interface within the user's authorization, checking the selected target and result at each consequential step. If no such tool is available, give the user actionable steps and ask for the specific screen or error needed to continue; do not claim to have controlled a computer. Never assume command-line automation or an API exists based on this guide.

For an existing connection, locate the intended Student in the Tutor console, select it, and inspect the available view/control options. Choose the option that actually permits interaction if the user requested control, rather than assuming viewing grants control. Follow displayed prompts, including any acknowledgment on the remote device. The supplied getting-started guide does not document the exact Windows control menu or mouse/keyboard procedure: verify the installed interface or the product manual instead of inventing a sequence. Stop when the requested task is complete and close the remote session if appropriate.

## Authorized software inventory or removal

Only inventory or uninstall software when the user explicitly requests that change and identifies the target computer or group. Keep the Tutor out of a Student-wide operation unless the user specifically includes it. In Tech Console, verify the selected Student before opening its Remote PowerShell window. If the credentials dialog describes credentials as optional for running as another user and offers Cancel, Cancel continues with the current session identity; it is not an authentication or elevation bypass. Check the effective identity and elevation before attempting an operation that requires admin rights, and stop if the session lacks the required access.

For package-managed Windows software, a specific query such as `Get-Package -Name '*OpenOffice*'` can provide an inventory in the remote PowerShell session. Review the returned package names and versions before removal. If the requested product has associated language packs or components, include them only when they are clearly part of that product and within the user's request. A command such as `Get-Package -Name '*OpenOffice*' | Uninstall-Package -Force` removes all matching packages; use a specific product pattern and never use a broad wildcard. MSI removals can take several minutes per package: let the command finish before issuing another command or closing the session. Re-run the inventory afterward; a 'No package found' result means no matching package remains. Record per-computer results and distinguish machines where the product was absent from machines where it was removed.

## Connect Windows computers

The 2018 NetSupport School Getting Started Guide, pages 3, 8-12 and 20-21, describes the following; labels and compatibility may differ in the installed version:

- The controlling computer needs the **Tutor (Control)** component; each target needs **Student (Client)**. The Student starts with Windows in the documented installation. A valid license or evaluation is required.
- Open **NetSupport School Tutor Console**. In the Welcome Wizard choose **Start** to open the Class Wizard. Select a class and its connection method. Room Mode is the guide's recommended quick method: configure matching room identifiers on the Tutor and Student, using the Student Configurator as needed. The guide also names Browse, PC, User and SIS modes but refers their details to the product manual.
- The Tutor searches for Students and shows connected Students in the Control window. A warning icon identifies a failed connection; hover over it to see the reason. Verify the correct machine before opening its view.
- If a Student is missing, check that its Student component is running, both machines have network connectivity, the chosen discovery method and room settings match, and any displayed error. The guide notes Windows Firewall rules apply to the active network and may require adjustment after a network change. Diagnose before suggesting changes; do not disable firewalls or weaken security as a shortcut.
- The guide says **Enable User Acknowledge** in the Client Configurator can require confirmation for a Tech Console connection. Honor existing acknowledgment requirements without assuming this setting covers all Tutor connections.

## Other devices and versions

The guide describes Chrome and mobile Students separately, with different feature sets. It does not establish full interactive remote control on those platforms. Ask for the device and installed Tutor/Student versions, then check the applicable product documentation or visible interface before promising a feature. For Chrome, the 2018 guide calls for a Name and Connectivity Server and matching gateway settings; for Android it notes screen viewing features may depend on manufacturer signing. Avoid treating this old guide's OS requirements and defaults as current compatibility claims.

Source: `C:\Users\USO\Downloads\NetSupport-School-Getting-Started-Guide.pdf` (copyright 2018). If unavailable or more detailed/current instructions are needed, consult the installed product help or official NetSupport documentation. Do not expose passwords or license keys in output.
