#
# Conditional build:
%bcond_without	tests		# do not perform "make test"
#
%define		pdir	RT
%define		pnam	Authen-Token
Summary:	RT-Authen-Token - token-based authentication
Name:		perl-RT-Authen-Token
Version:	0.04
Release:	1
License:	GPL
Group:		Development/Languages/Perl
Source0:	http://www.cpan.org/modules/by-module/RT/%{pdir}-%{pnam}-%{version}.tar.gz
# Source0-md5:	f48180cc663fcc8fc5eb7e72933ecc9e
URL:		https://metacpan.org/release/RT-Authen-Token
BuildRequires:	perl-devel >= 1:5.8.0
BuildRequires:	rpm-perlprov >= 4.1-13
BuildRequires:	rpmbuild(macros) >= 1.745
BuildRequires:	rt < 5.0.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This module adds the ability for users to generate and login with
authentication tokens. Users with the ManageAuthTokens permission
will see a new "Auth Tokens" menu item under "Logged in as ____" ->
Settings. On that page they will be able to generate new tokens and
modify or revoke existing tokens.

Once you have an authentication token, you may use it in place of a
password to log into RT. (Additionally, RT::Extension::REST2 allows
for using auth tokens with the Authorization: token HTTP header.) One
common use case is to use an authentication token as an
application-specific password, so that you may revoke that application's
access without disturbing other applications. You also need not change
your password, since the application never received it.

If you have the AdminUsers permission, along with
ManageAuthTokens, you may generate, modify, and revoke tokens for
other users as well by visiting Admin -> Users -> Select -> (user) ->
Auth Tokens.

Authentication tokens are stored securely (hashed and salted) in the
database just like passwords, and so cannot be recovered after they are
generated.

%prep
%setup -q -n %{pdir}-%{pnam}-%{version}

%build
%{__perl} Makefile.PL \
	INSTALLDIRS=vendor
%{__make}

%{?with_tests:%{__make} test}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/rt

%{__make} pure_install \
	INSTALLVENDORLIB=%{perl_vendorlib} \
	DESTDIR=$RPM_BUILD_ROOT

cp -a html static $RPM_BUILD_ROOT%{_datadir}/rt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes README etc
%{perl_vendorlib}/RT/Auth*.pm
%{perl_vendorlib}/RT/Authen/Token.pm
%{_mandir}/man3/RT::Auth*.3pm*
%{_datadir}/rt/html/*/*.html
%{_datadir}/rt/html/*/*/*.html
%{_datadir}/rt/html/Callbacks/RT-Authen-Token
%{_datadir}/rt/html/Elements/AuthToken
%{_datadir}/rt/html/Helpers/AuthToken
%{_datadir}/rt/static/*/*.css
%{_datadir}/rt/static/*/*.gif
%{_datadir}/rt/static/*/*.js
