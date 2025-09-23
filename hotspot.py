#!/usr/bin/env python3
"""
show_wifi_passwords.py

Cross-platform helper to display saved Wi-Fi profiles and their passwords
for the current machine (Windows, macOS, Linux with NetworkManager).

USAGE:
    python show_wifi_passwords.py

NOTES:
- Requires administrative privileges on some systems.
- Run only on machines/networks you own or are authorized to audit.
- Tested approaches:
    - Windows: uses `netsh`
    - macOS: uses `security find-generic-password ... -gw`
    - Linux: tries `nmcli` then falls back to reading /etc/NetworkManager/system-connections/
"""

import sys
import subprocess
import platform
import os
import shlex
import re
from pathlib import Path

def run_cmd(cmd, capture_output=True, shell=False):
    try:
        if shell:
            p = subprocess.run(cmd, capture_output=capture_output, text=True, shell=True, timeout=20)
        else:
            p = subprocess.run(cmd, capture_output=capture_output, text=True, shell=False)
        return p.returncode, p.stdout or p.stderr or ""
    except Exception as e:
        return 1, str(e)

def windows_get_profiles():
    code, out = run_cmd(["netsh", "wlan", "show", "profiles"])
    if code != 0:
        print("Failed to run netsh. Are you on Windows and running with proper privileges?")
        return []
    # parse "All User Profile     : SSID_NAME"
    profiles = re.findall(r"All User Profile\s*:\s*(.+)", out)
    return [p.strip().strip('"') for p in profiles]

def windows_get_password(profile):
    code, out = run_cmd(["netsh", "wlan", "show", "profile", f'name="{profile}"', "key=clear"])
    if code != 0:
        return None
    m = re.search(r"Key Content\s*:\s*(.+)", out)
    if m:
        return m.group(1).strip()
    return None

def macos_get_profiles():
    # list network-password entries of AirPort type
    # We try to list by reading known networks via /Library/Preferences/SystemConfiguration/com.apple.airport.preferences.plist
    # Simpler: use `networksetup -listpreferredwirelessnetworks <device>` but we need the device name. Instead try parsing Keychain items.
    # We'll attempt to get SSIDs by searching the System Keychain for "AirPort network password"
    code, out = run_cmd(["/usr/bin/security", "find-generic-password", "-D", "AirPort network password", "-a", "", "-g"], capture_output=True)
    # `security` without an account will not list names reliably; fallback to using `networksetup`
    # Try to get airport device name then list preferred networks
    code_dev, dev_out = run_cmd(["/usr/sbin/networksetup", "-listallhardwareports"])
    ssids = []
    if code_dev == 0:
        # find device for Wi-Fi (called "Wi-Fi" or "AirPort")
        m = re.findall(r"Hardware Port: (.+?)\nDevice: (.+?)\n", dev_out)
        wifi_device = None
        for port, dev in m:
            if port.lower().startswith("wi") or "airport" in port.lower():
                wifi_device = dev.strip()
                break
        if wifi_device:
            code2, out2 = run_cmd(["/usr/sbin/networksetup", "-listpreferredwirelessnetworks", wifi_device])
            if code2 == 0:
                # first line is "Preferred networks on en0:"
                lines = out2.splitlines()[1:]
                ssids = [l.strip() for l in lines if l.strip()]
    # If we still have none, return empty and let user query specific SSIDs manually
    return ssids

def macos_get_password(ssid):
    # Uses security to get password; will prompt for password if required
    # Command: security find-generic-password -D "AirPort network password" -a "SSIDNAME" -gw
    cmd = ["/usr/bin/security", "find-generic-password", "-D", "AirPort network password", "-a", ssid, "-gw"]
    code, out = run_cmd(cmd)
    # If out contains "password:" or is printed as stderr, return it
    # `security -gw` prints the password to stderr on some macOS versions
    # The run_cmd returns stderr in the second element if stdout is empty
    text = out.strip()
    if not text:
        return None
    # strip potential leading 'password: "..."'
    m = re.search(r'password:\s*"?(.*?)"?\s*$', text, re.DOTALL)
    if m:
        return m.group(1)
    return text

def linux_get_profiles_nmcli():
    # try nmcli to list saved connection names
    code, out = run_cmd(["nmcli", "-t", "-f", "NAME,TYPE", "connection", "show"])
    if code != 0:
        return []
    lines = out.splitlines()
    ssids = []
    for ln in lines:
        name, typ = ln.split(":", 1) if ":" in ln else (ln, "")
        if typ.strip() == "802-11-wireless" or typ.strip() == "wifi":
            ssids.append(name.strip())
    return ssids

def linux_get_password_nmcli(ssid):
    code, out = run_cmd(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid])
    if code != 0 or not out.strip():
        # try other property names
        code2, out2 = run_cmd(["nmcli", "-s", "-g", "802-11-wireless-security.psk", "connection", "show", ssid])
        return out2.strip() if code2 == 0 else None
    return out.strip()

def linux_read_system_connections():
    path = Path("/etc/NetworkManager/system-connections")
    if not path.exists():
        return {}
    results = {}
    for f in path.glob("*"):
        try:
            txt = f.read_text(errors="ignore")
        except PermissionError:
            continue
        # parse psk= in [wifi-security] section
        # crude parse
        m = re.search(r"\[wifi-security\](.*?)\n\[", txt, re.S)
        section = m.group(1) if m else txt
        psk_m = re.search(r"psk\s*=\s*(.+)", section)
        ssid_m = re.search(r"ssid\s*=\s*(.+)", txt)
        if ssid_m:
            ssid = ssid_m.group(1).strip().strip('"')
            psk = psk_m.group(1).strip().strip('"') if psk_m else None
            results[ssid] = psk
    return results

def main():
    system = platform.system()
    print(f"Detected OS: {system}\n")
    results = []

    if system == "Windows":
        profiles = windows_get_profiles()
        if not profiles:
            print("No saved Wi-Fi profiles found or failed to query (are you on Windows?).")
            return
        for p in profiles:
            pwd = windows_get_password(p)
            results.append((p, pwd))
    elif system == "Darwin":
        ssids = macos_get_profiles()
        if not ssids:
            print("Could not detect preferred Wi-Fi networks automatically.")
            print("You can run the script again and provide an SSID as an argument, or run Keychain Access GUI.")
            # Offer interactive prompt
            ssid = input("Enter SSID to retrieve password for (or press Enter to exit): ").strip()
            if not ssid:
                return
            pwd = macos_get_password(ssid)
            results.append((ssid, pwd))
        else:
            for s in ssids:
                pwd = macos_get_password(s)
                results.append((s, pwd))
    elif system == "Linux":
        # Try nmcli first
        ssids = linux_get_profiles_nmcli()
        if ssids:
            for s in ssids:
                pwd = linux_get_password_nmcli(s)
                results.append((s, pwd))
        else:
            # fall back to reading system-connections (requires sudo)
            data = linux_read_system_connections()
            if not data:
                print("No NetworkManager connections found or permission denied.")
                print("Try running this script with sudo.")
                return
            for ssid, psk in data.items():
                results.append((ssid, psk))
    else:
        print("Unsupported OS:", system)
        return

    # Print results
    print("\nSaved Wi-Fi networks and passwords:\n")
    for ssid, pwd in results:
        if pwd:
            print(f"SSID: {ssid}\n  Password: {pwd}\n")
        else:
            print(f"SSID: {ssid}\n  Password: (not found or requires elevated privileges)\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nAborted by user.")
