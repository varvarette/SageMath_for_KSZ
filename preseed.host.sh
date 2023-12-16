### Localization
d-i debian-installer/language string en
d-i debian-installer/country string CH
d-i debian-installer/locale string en_US.UTF-8

# Keyboard selection.
d-i console-setup/ask_detect boolean false
d-i keyboard-configuration/layoutcode string de_CH

### Network configuration
d-i netcfg/choose_interface select auto

# If you have a slow dhcp server and the installer times out waiting for      
# it, this might be useful.
#d-i netcfg/dhcp_timeout string 60

# Any hostname and domain names assigned from dhcp take precedence over       
# values set here. However, setting the values still prevents the questions   
# from being shown, even if values come from dhcp.
d-i netcfg/get_hostname string schostvm
d-i netcfg/get_domain string unassigned-domain

### Mirror settings
d-i mirror/country string manual
d-i mirror/http/hostname string ubuntu.ethz.ch/
d-i mirror/http/mirror select ubuntu.ethz.ch/
d-i mirror/http/hostname string ubuntu.ethz.ch/
d-i mirror/http/directory string /ubuntu/
#d-i mirror/http/proxy string APTPROXY
d-i mirror/suite select focal (20.04)

### Clock and time zone setup
# Controls whether or not the hardware clock is set to UTC.
d-i clock-setup/utc boolean true

# You may set this to any valid setting for $TZ; see the contents of
# /usr/share/zoneinfo/ for valid values.
d-i time/zone string Europe/Zurich

# Controls whether to use NTP to set the clock during the install
d-i clock-setup/ntp boolean true
# NTP server to use. The default is almost always fine here.
#d-i clock-setup/ntp-server string ntp.example.com

### Partitioning
d-i partman-auto/method string regular
d-i partman-lvm/device_remove_lvm boolean true
d-i partman-md/device_remove_md boolean true
d-i partman-lvm/confirm boolean true
#d-i partman-auto/choose_recipe select atomic
#d-i partman/default_filesystem string btrfs

d-i partman-auto/expert_recipe string small-swap : \
        16384 65536 -1 btrfs \
            $primary{ } $bootable{ } \
            method{ format } format{ } \
            use_filesystem{ } filesystem{ btrfs } \
            options/compress{ } \
            mountpoint{ / } . \
        64 512 50% linux-swap \
	method{ swap } format{ } .
	
	
# This makes partman automatically partition without confirmation, provided      
# that you told it what to do using one of the methods above.
d-i partman-partitioning/confirm_write_new_label boolean true
d-i partman/choose_partition select finish
d-i partman/confirm boolean true
d-i partman/confirm_nooverwrite boolean true

### Account setup
d-i passwd/root-login boolean true
# Root password, either in clear text
d-i passwd/root-password password disabled
d-i passwd/root-password-again password disabled
# or encrypted using an MD5 hash.
#d-i passwd/root-password-crypted password [MD5 hash]
d-i passwd/make-user boolean false

### Package selection
tasksel tasksel/first multiselect openssh-server, server, standard

# Individual additional packages to install
d-i pkgsel/include string haproxy lxc python3-lxc python3-psutil rsyslog-relp    

# Whether to upgrade packages after debootstrap.
# Allowed values: none, safe-upgrade, full-upgrade
d-i pkgsel/upgrade select safe-upgrade

# Policy for applying updates. May be "none" (no automatic updates),
# "unattended-upgrades" (install security updates automatically), or
# "landscape" (manage system with Landscape).
d-i pkgsel/update-policy select unattended-upgrades

# By default, the system's locate database will be updated after the
# installer has finished installing most packages. This may take a while, so     
# if you don't want it, you can set this to "false" to turn it off.
d-i pkgsel/updatedb boolean false

### Boot loader installation
# This is fairly safe to set, it makes grub install automatically to the MBR     
# if no other operating system is detected on the machine.
d-i grub-installer/only_debian boolean true
# This one makes grub-installer install to the MBR if it also finds some other   
# OS, which is less safe as it might not be able to boot that other OS.
d-i grub-installer/with_other_os boolean true

### Finishing up the installation
# During installations from serial console, the regular virtual consoles
# (VT1-VT6) are normally disabled in /etc/inittab. Uncomment the next
# line to prevent this.
d-i finish-install/keep-consoles boolean true

# Avoid that last message about the install being complete.
d-i finish-install/reboot_in_progress note

#### Advanced options
### Running custom commands during the installation
# This command is run just before the install finishes, but when there is  
# still a usable /target directory. You can chroot to /target and use it   
# directly, or use the apt-install and in-target commands to easily install
# packages and run commands in the target system.
#d-i preseed/late_command string apt-install zsh; in-target chsh -s /bin/zsh     

d-i preseed/late_command string \
    cd /target/root; \
    mkdir .ssh; \
    chmod 0700 .ssh; \
    echo 'SSHKEY' > .ssh/authorized_keys; \
    chmod 0600 .ssh/authorized_keys; \
    in-target /usr/bin/passwd -l root
