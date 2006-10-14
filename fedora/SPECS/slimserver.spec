# Following was set by makerelease.pl for Slimdevices generic Linux RPM
%define version 6.5.0
%define POE_XS_Queue_Array_version 0.003

# Slimdevices generic Linux RPM disables stripping, not sure why
%define __spec_install_post /usr/lib/rpm/brp-compress

# Don't build debuginfo packages
%define debug_package %{nil}

# Do we need to include the firmware and graphics?
%define include_firmware %{?_with_firmware:1}0

Name:           slimserver
Packager:       Slim Devices <support@slimdevices.com>
Version:        %{version}
# My guess is we'll want to set the 'dist' macro to differentiate the Fedora
# RPM from the generic linux RPM, but that would seem to mean that somebody
# out there will be building the RPM on a Fedora box and placing it on the
# Slim website to support all the different machine architectures Fedora runs
# on...
Release:        1%{?dist}
Summary:        This is the Slim Devices server software
Group:          System Environment/Daemons
License:        GPL
URL:            http://www.slimdevices.com/
Source0:        SlimServer_v%{version}.tar.gz
Source1:        slimserver.init
Source2:        slimserver.config
Source3:	POE-XS-Queue-Array-%{POE_XS_Queue_Array_version}.tar.gz
Patch0:		slimserver-POE-XS-Queue-Array-%{POE_XS_Queue_Array_version}.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

# There is no BuildRequires: tag yet. Ideally, the rpmbuild process will
# include some testing (I haven't yet reviewed how unit-testing works with
# the slimserver source tree), so there are no BuildRequires.

# slimserver original .spec disabled automatic dependency processing, not
# commented out yet(?)
AutoReqProv: no

# The following requires are available in base, core, extras, or RpmForge repositories
Requires:       perl >= 5.8.3
Requires:       perl(Cache::Cache)
Requires:       perl(Carp::Clan)
Requires:       perl(Class::Accessor)
Requires:       perl(Class::Accessor::Chained)
Requires:       perl(Class::Inspector)
Requires:       perl(Class::Singleton)
Requires:       perl(Class::Virtual)
Requires:       perl(Compress::Zlib)
Requires:       perl(Data::Dump)
Requires:       perl(DBD::MySQL)
Requires:       perl(DBI)
Requires:       perl(Digest::SHA1)
Requires:       perl(Error)
Requires:       perl(File::BOM)
Requires:       perl(File::Find::Rule)
Requires:       perl(File::Slurp)
Requires:       perl(GD)
Requires:       perl(HTML::Parser.)
Requires:       perl(libwww::perl) >= 5.803
Requires:       perl(Net::DNS)
Requires:       perl(Net::IP)
Requires:       perl(Net::UPnP)
Requires:       perl(Number::Compare)
Requires:       perl(Path::Class)
Requires:       perl(Proc::Background)
Requires:       perl(Readonly)
Requires:       perl(RPC::XML)
Requires:       perl(SQL::Abstract)
Requires:       perl(SQL::Abstract::Limit)
Requires:       perl(Template::Toolkit)
Requires:       perl(Term::ReadKey)
Requires:       perl(Text::Glob)
Requires:       perl(Text::Unidecode)
Requires:       perl(Tie::Cache)
Requires:       perl(Tie::LLHash)
Requires:       perl(TimeDate)
Requires:       perl(Time::HiRes)
Requires:       perl(URI)
Requires:       perl(XML::NamespaceSupport)
Requires:       perl(XML::Parser)
Requires:       perl(XML::SAX.)
Requires:       perl(XML::Writer)
Requires:       perl(YAML::Syck)
Requires:       flac
Requires:       sox
Requires:       mysql-server >= 5.0.22
#Requires:       lame
#Requires:       shorten

# The following requires are in RPMS built by Al Pacifico, but not yet in any
# Fedora base, extras, or RpmForge:
Requires:       perl(Algorithm::C3)
Requires:       perl(Class::C3)
Requires:       perl(Class::Data::Accessor)
Requires:       perl(Data::Page)
Requires:       perl(Data::VString)
Requires:       perl(DBIx::Class)
Requires:       perl(DBIx::Migration)
Requires:       perl(File::Which)
Requires:       perl(Locale::Hebrew)
Requires:       perl(Module::Find)
Requires:       perl(MP4::Info)
Requires:       perl(MPEG::Audio::Frame)
Requires:       perl(Tie::Cache::LRU::Expires)
Requires:       perl(Tie::RegexpHash)
Requires:       perl(URI::Find)
Requires:       perl(XML::XSPF)
Requires:       alac_decoder

%description
This is the Slim Devices server software.
Point your web browser to http://localhost:9000/ to configure the server.
* Open-source server, written in Perl (GPL)
* Optional HTTP interface - control the player and manage your playlists from 
  a web browser!
* Internet radio - Shoutcast, Icecast, RadioIO, and Live365
* Unlimited capacity - it doesn't matter if your mp3 collection is a
  megabyte or a terabyte. Your files are not stored on the player, so there's
  no limit to the amount of music you can access, and you don't need to
  hassle with copying your files onto the player.
* Easy to use hierarchical browser interface
* Random mode
* Supports .pls and .m3u playlist files


%prep
%setup -q -n SlimServer_v%{version}
tar -xzf %{S:3}
pushd POE-XS-Queue-Array-%{POE_XS_Queue_Array_version}
patch -p1 < %{P:0}
popd

%build
[ "%buildroot" != "/" ] && rm -rf %buildroot
# The Bin directory of the source tarball contains compiled (and therefore 
# architecture-dependent) executables. We will use the system's binaries or 
# rebuild these when the RPM is built. Since some plug-ins use this directory,
# we'll keep the directory as part of the RPM, though.
rm -rf Bin/*

# The CPAN directory of the source contains unmodified perl modules from CPAN, 
# but not neccessarily intact CPAN modules. We've chosen for some of these to
# use the versions in the tarball rather than system packages, to reduce the 
# disk footprint of the installed package and installed dependencies. The 
# modified CPAN modules for which we will use the source versions are:
#    POE::XS::Queue::Array
# and we therefore must use the modules that they depend on from the source
# as well:
#    POE::Queue
# These will be rebuilt because they contain C Perl extensions that need to
# compile for the target architecture. Therefore, we will remove the entire
# CPAN directory and start over. remaining contents of the CPAN directory are 
# removed.

# Remove the perl stuff that system packages provide
rm -rf CPAN/*

# remake the modified CPAN modules we wish to use
cp -a POE-XS-Queue-Array-%{POE_XS_Queue_Array_version}/POE CPAN
mkdir -p CPAN/arch/$(perl -MConfig -e 'print "$Config{version}";')
pushd POE-XS-Queue-Array-%{POE_XS_Queue_Array_version}
perl Makefile.PL LIB=%buildroot%_libdir/slimserver/CPAN/arch/$(perl -MConfig -e 'print "$Config{version}";')
make
make test
popd

# Do we need to remove the firmware and Graphics?
%if ! %{include_firmware}
# Remove the firmware and Graphics per the License.txt
rm -rf Firmware
rm -rf Graphics
# Recreate directories though so user can get them from SlimDevices and put
# them there if desired
mkdir Firmware
mkdir Graphics
%endif

# The lib/README file won't make sense outside of the context of lib
# We plan to move it to a specific documentation directory
# change its name
mv lib/README README.lib
# change its contents to reflect the move
sed -i 's#This#The %_libdir/slimserver/lib#' README.lib
# Ideally, the file would be patched to remove the stuff about
# the top-level CPAN directory which doesn't make sense in the
# context of a Fedora RPM or just removed, as it makes the most sense
# in its initial context for developers.

%install
rm -rf %buildroot
mkdir -p %buildroot%_initrddir
#mkdir -p %buildroot%_sysconfdir/slimserver
mkdir -p %buildroot%_libdir/slimserver
%if ! %{include_firmware}
mkdir -p %buildroot%_libdir/slimserver/Firmware
mkdir -p %buildroot%_libdir/slimserver/Graphics
%endif
mkdir -p %buildroot%_sbindir
mkdir -p %buildroot%{_var}/cache/slimserver/playlists
# music directory (FHS specifies /srv for readonly, many services use /var)
mkdir -p %buildroot/srv/slimserver

# copy over stuff that belongs in the RPM
cp -R Bin %buildroot%_libdir/slimserver
cp -R Changelog*.html %buildroot%_libdir/slimserver
cp -R HTML %buildroot%_libdir/slimserver
cp -R IR %buildroot%_libdir/slimserver
cp -R lib %buildroot%_libdir/slimserver
cp -R MySQL %buildroot%_libdir/slimserver
cp -R Plugins %buildroot%_libdir/slimserver
cp -R Slim %buildroot%_libdir/slimserver
cp -R SQL %buildroot%_libdir/slimserver
%if %{include_firmware}
cp -R Firmware %buildroot%_libdir/slimserver
cp -R Graphics %buildroot%_libdir/slimserver
%endif
cp convert.conf %buildroot%_libdir/slimserver
cp revision.txt %buildroot%_libdir/slimserver
cp strings.txt %buildroot%_libdir/slimserver
cp types.conf %buildroot%_libdir/slimserver

# install our newly built CPAN stuff
cp -a POE-XS-Queue-Array-%{POE_XS_Queue_Array_version}/POE %buildroot%_libdir/slimserver/CPAN
pushd POE-XS-Queue-Array-%{POE_XS_Queue_Array_version}
make install
popd
# get rid of unneeded documentation and metadata/markers
find %buildroot%_libdir/slimserver/CPAN -type f -name .packlist -exec rm -f {} ';'
find %buildroot%_libdir/slimserver/CPAN -type f -name perllocal.pod -exec rm -f {} ';'
find %buildroot%_libdir/slimserver/CPAN -type f -name '*.bs' -a -size 0 -exec rm -f {} ';'
find %buildroot%_libdir/slimserver/CPAN -type d -depth -exec rmdir {} 2>/dev/null ';'

# put slimserver.pl in /usr/sbin
mv slimserver.pl %buildroot%_sbindir
chmod +x %buildroot%_sbindir/slimserver.pl
# put scanner.pl in /usr/sbin
mv scanner.pl %buildroot%_sbindir
chmod +x %buildroot%_sbindir/scanner.pl

# install and modify configuration files
install -D -m755 %SOURCE1 %buildroot%_initrddir/slimserver
install -D -m644 %SOURCE2 %buildroot%_sysconfdir/sysconfig/slimserver
touch %buildroot%_sysconfdir/slimserver.conf
echo "cachedir = %{_var}/cache/slimserver" > %buildroot%_sysconfdir/slimserver.conf
echo "playlistdir = %{_var}/cache/slimserver/playlists" >> %buildroot%_sysconfdir/slimserver.conf

# Note for future reference:
# rpm macro %%_libexecdir expands to /usr/libexec for locating mysqld binary
# see http://sourceforge.net/mailarchive/forum.php?thread_id=24302360&forum_id=3128 re
# location of mysql in /usr/libexec

%clean
rm -rf $RPM_BUILD_ROOT

# The following lines are from the Slim Devices generic Linux RPM.
# They're included here, but commented out, for future assessment
# The practice of removing the build directory doesn't seem to be
# part of the Fedora skeleton .spec files. Remember the escaping
# of '%' with '%%' if uncommenting

#[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -r $RPM_BUILD_ROOT
#cd ..
#[ "$RPM_BUILD_DIR" != "/" ] && [ -d $RPM_BUILD_DIR/SlimServer_v%%{version} ] \
#&& rm -r $RPM_BUILD_DIR/SlimServer_v%%{version}

###############################################################################
# The following sections copied verbatim from the Slimdevices generic Linux RPM
# and will need tweaking, including for SELinux
###############################################################################

%pre
export SLIMSERVER_USER=slimserver

# Someone might have changed the default.  Lets make sure we use it.
if [ -f /etc/sysconfig/slimserver ]; then
        . /etc/sysconfig/slimserver;
fi

# Add the $SLIMSERVER_USER if there is not one
if [ `grep -c "^$SLIMSERVER_USER:" /etc/passwd` -eq 0 ]; then
        /usr/sbin/groupadd $SLIMSERVER_USER
        /usr/sbin/useradd -c "SlimServer" -g $SLIMSERVER_USER -m -d %{slimdir} -s /sbin/nologin $SLIMSERVER_USER
fi

# Remove the old Favorites plugin
rm -rf /usr/local/slimserver/Plugins/Favorites

%post
export SLIMSERVER_USER=slimserver

# Someone might have changed the default.  Lets make sure we use it.
if [ -f /etc/sysconfig/slimserver ]; then
        . /etc/sysconfig/slimserver;
fi

# Make sure we have the correct SLIMSERVER_HOME in /etc/sysconfig/slimserver
# Convert / to \/ for the sed substitution
if [ `grep -c PREFIX /etc/sysconfig/slimserver` -gt 0 ]; then
        DEST_FILE=/etc/sysconfig/slimserver
        SLIMSERVER_PREFIX=`echo %{slimdir} | sed 's/\//\\\\\//g'`
        sed "s/PREFIX/$SLIMSERVER_PREFIX/" $DEST_FILE > /tmp/slimserver.$$
        if [ -s /tmp/slimserver.$$ ]; then
                cp /tmp/slimserver.$$ $DEST_FILE
                rm /tmp/slimserver.$$
        fi
fi

if [ ! -s /etc/slimserver.conf ] && [ -e /etc/slimp3.pref ]; then
        cp /etc/slimp3.pref /etc/slimserver.conf
fi

# Now that everything is installed, make sure the permissions are right
chown -R $SLIMSERVER_USER.$SLIMSERVER_USER %{slimdir}

# Allow the RPM to be installed on SuSE
if [ -x /sbin/chkconfig ]; then
        /sbin/chkconfig --add slimserver
fi

if [ -x /sbin/service ]; then

        /sbin/service slimserver restart >/dev/null 2>&1 || :

        PORT=`awk '/^httpport/ {print $2}' /etc/slimserver.conf`
fi

# Set a default port if one doesn't exist.
if [ ! -z "$PORT" -o ! -s /etc/slimserver.conf ]; then
        PORT=9000
fi

HOSTNAME=`uname -n`

echo "Point your web browser to http://$HOSTNAME:$PORT/ to configure your server."

if [ -e /tmp/slimserver.log ]; then
        rm /tmp/slimserver.log
fi

%preun
# Only if we are not upgrading...
if [ "$1" -eq "0" ] ; then

        if [ -x /sbin/service ]; then
                /sbin/service slimserver stop >/dev/null 2>&1 || :
        fi

        if [ -x /sbin/chkconfig ]; then

                /sbin/chkconfig --del slimserver
        fi
fi

%postun
# Only if we are upgrading...
if [ "$1" -ge "1" ]; then

        if [ -x /sbin/service ]; then
                /sbin/service slimserver restart >/dev/null 2>&1 || :
        fi

else
        SLIMSERVER_USER="slimserver"
        SLIMSERVER_CFG="/etc/slimserver.conf"

        if [ -f /etc/sysconfig/slimserver ]; then
                . /etc/sysconfig/slimserver;
        fi

        userdel $SLIMSERVER_USER 2>/dev/null || :

        # assume the group name is the same as the user, it's not in sysconfig
        groupdel $SLIMSERVER_USER 2>/dev/null || :
fi

###############################################################################
# End of verbatim from the Slimdevices generic Linux RPM
###############################################################################


%files
%defattr(-,root,root)

# documentation files
%doc Installation.txt License.txt README.lib

# library files
%_libdir/slimserver

# config files
# %%_sysconfdir/slimserver

# empty directories
%dir %{_var}/cache/slimserver
%dir /srv/slimserver

# executables
%_sbindir/slimserver.pl
%_sbindir/scanner.pl

# configuration files and init scripts
%attr(-, slimserver, slimserver)
%config(noreplace) %_sysconfdir/slimserver.conf
%config %_initrddir/slimserver
%config(noreplace) %_sysconfdir/sysconfig/slimserver


%changelog
* Thu Jul 6 2006 adpacifico@users.sourceforge.net - 6.5.0-1
- began modifying RPM for Fedora Core 5
- started with skeleton file generated by fedora-newrpmspec
- then with generic Linux RPM from SlimDevices
- then some of the changes from Michael Peters' spec file

* Sat Apr 23 2005 Michael A. Peters <mpeters@mac.com>
- changed perl-Time-HiRes requires to 1.65 (from 1.66)

* Fri Apr 15 2005 Michael A. Peters <mpeters@mac.com>
- clean up init script to fedora rpmdevtools template
- do not actually start the service on install, just
- chkconfig --add the service
- start cleanup of specfile to match (as much as possible)
- the fedora spectemplate-minimal.spec file
-
- update version to 6.0.2 maintenance branch
- updated convert.conf - upstream started using sox to decode
- ogg files - which is fine for wav and flac transcode, but
- not fine for mp3 transcode since Fedora sox is not linked
- against lame for mp3 encoding.

* Tue Apr 11 2005 dsully
- Make the RPM more SuSE friendly.
- Fix an error with printing the port number on install/upgrade. (bug 974)

* Fri Apr 04 2005 Michael A. Peters <mpeters@mac.com>
- Requires File::BOM

* Fri Apr 01 2005 Michael A. Peters <mpeters@mac.com>
- updated to release version nightly build

* Fri Mar 25 2005 Michael A. Peters <mpeters@mac.com>
- put confif files into /etc/slimserver
- patch convert.conf to be properly set up for linux - at least
- for mp3 capabilities

* Thu Mar 24 2005 Michael A. Peters <mpeters@mac.com>
- updated the convert.conf patch so apes would transcode to lame
- better (removed -x switch from lame)

* Tue Mar 22 2005 Michael A. Peters <mpeters@mac.com>
- do NOT remove iTunes plugin.
- create a directory in /var for slimserver home and cache
- use getent to check for existance of slimserver user
- put cachedir in /var/cache and make that slimserver home
- create a default playlist dir that slimserver can write to.
- create the /etc/sysconfig file in the install macro, using the
- macros we defined in the spec file.

* Mon Mar 21 2005 Michael A. Peters <mpeters@mac.com>
- Change default in convert.conf to use faad for aac
- Remove iTunes plugin until iTunes for Linux is released

* Sun Mar 20 2005 Michael A. Peters <mpeters@mac.com>
- removed dependencies on specific version of perl modules that
- were installed in CPAN/arch
- with binaries no longer needed in slimserver home, moved
- prefix to /usr/share

* Fri Mar 18 2005 Michael A. Peters <mpeters@mac.com>
- cleaned up some harmless errors in scriplets.
- Use /usr/sbin/adduser with the -r switch instead of
- /usr/sbin/useradd - thus creating a user w/ UID belows
- common users. It will be a UID > 99 still, so no conflict
- with system UID's.
- define slimuser macro at top of file, use throughout.

* Sun Mar 13 2005 Michael A. Peters <mpeters@mac.com>
- prep work and cleanup began for extras or livna.
- not a public release.
- changed prefix to /var
- added comment support for nightly vs release
- commented out message to console on install
- removing firmware, removing Bin

* Thu Nov 6 2003 dean
- Renaming slimd to slimserver

* Mon Sep 15 2003 kdf
- Patch submitted by many for custom port message on install
- remove /tmp/slimd.log if it exists, avoid server crash if its locked.

* Fri Aug 1 2003 kdf
- Change user to slim, install to /usr/local/slimd for consistency
- Copy old slimp3.pref if it exists and slimd.conf is zero length (new)

* Thu May 22 2003 dean
Victor Brilon submitted a patch:
- Got rid of the -r param. On RedHat this creates a system account w/a
UID lower than value of UID_MIN. I don't see why we need to do this as
the slimp3 user is not a priviledged user. Also, with this param, the -d
flag will never create a home dir for security reasons.

- Got rid of the -s flag as this will force the system to use the
default shell for the user.

- Also with useradd, if a passwd is not specified (which is exactly what
we're doing), the default action is to lock the account so you can't
login into it. This should work ok as we can still su into it to start
the slimp3 player.

- The slimp3 directory hierarchy should be owned by the slimp3 user not
by root. Changed that as well. This should prevent some of the problems
people were having with saving playlists and such.

* Mon Feb 10 2003 DV <datavortex@datavortex.net>
- Remove tag database on full uninstall.  db.pag gets big.
- Fixed postinstall substitution
- Remove nondefault user and group

* Sun Feb 09 2003       Mike Arnold <mike@razorsedge.org>
- Cleaned up DV's changes to the preinstall script.
- Added %config(noreplace) to /etc/sysconfig/slimp3.
- Fixed two changes in the postinstall script that broke relocation.

* Thu Oct 24 2002   DV <datavortex@datavortex.net>
- changed account to a system account and shell to nologin.
- don't add user with default name if the admin changed it.

* Tue Oct 22 2002       Mike Arnold <mike@razorsedge.org>
- Fixed a problem with doing a package "upgrade" and losing the
  passwd entry for the slimp3 user in %preun and %postun.
- Made sure an existing /etc/slimp3.pref was not replaced by a newer package.
- Got rid of all the commented, tarball-removal stuff in %pre.
- Beautified the spec file for final release.

* Sun Oct 20 2002   Dean Blackketter <dean@slimdevices.com>
- Mike Arnold told me to take out the postun directive that removes the
  passwd entry to fix upgrades.

* Tue Oct 01 2002       Mike Arnold <mike@razorsedge.org>
- Made the slimp3 user's $HOME be in the correct place even with
  a relocatable package.

* Wed Sep 11 2002       Dean Blackketter <dean@slimdevices.com>
- Made the default install back to /usr/local/bin instead of /opt

* Sun Sep 08 2002       Mike Arnold <mike@razorsedge.org>
- Made the RPM relocatable for those who do not want to use /opt
  including a %post hack to mod /etc/sysconfig/slimp3
- Made sure slimp3.pl was chmod +x, even if the tarball was wrong
- Cleaned up the BUILD_DIR after the rpms are built
- Changed localhost to "uname -n" in post-install commandline echo
- Disabled the deletion of old (pre-RPM) files as the procs may
  still be running. Should we just assume no preexisting installs?
- Pulled _topdir out and let the build system or user specify it.

* Wed Sep 04 2002       Dean Blackketter <dean@slimdevices.com>
- Disabling the shutdown of old (pre-RPM) processes.
- Added AutoReqProv: no, because all we really need is perl
- Disabled the documentation install until we have some better docs.
  (until then, use the built-in documentation, available via the web interface)

* Mon Sep 02 2002       Mike Arnold <mike@razorsedge.org>
- Changed the slimp3dir to /opt as this is where "packages" should go
- Added an external startup config file in /etc/sysconfig
- Added documentation to the RPM
- Kept %postun from deleteing the %config file as rpm takes care of this
- Changed software group to System Environment/Daemons
- Added a nice description
- Added %clean

* Wed Aug 28 2002       Victor Brilon <victor@vail.net>
- First release