#! /usr/bin/perl -w

# Example: egroup2anything.pl -egroup lxsoft-admins -user mejias -format "%s@CERN.CH"

# TODO: 
#  - include newline in format...
#  
#

use strict;
use diagnostics;
use Getopt::Long;
use Data::Dumper;

sub egroup2username(@);

my $debug = my $unique = my $outfile = my $recursion = my $chkaccount = my $attribute = undef;
my @egroup = my @username = (); #qw(lxsoft-admins it-dep-pes-ps);
my $FORMAT = "%s";

my %opts = ("debug"                => \$debug,
            "unique"               => \$unique,
            "format=s"             => \$FORMAT,
            "egroup=s@"            => \@egroup,
            "user=s@"              => \@username,
            "outfile=s"            => \$outfile,
            "allow-nested-egroups" => \$recursion,
            "check-account"        => \$chkaccount,
            "attribute=s"          => \$attribute,
           );

my $options = GetOptions(%opts);
print "\$FORMAT = \"$FORMAT\"\n" if $debug;

print "0 \@username = @username\n" if $debug;
push(@username,egroup2username({recursion => $recursion,
                                attribute => $attribute},
                               @egroup)) if @egroup;

# prune the list of usernames

print "1 \@username = @username\n" if $debug;
@username = sort keys %{{map{$_=>1} @username}} if $unique;  # remove duplicate entries
print "2 \@username = @username\n" if $debug;
@username = grep {getpwnam($_) && $_} @username if $chkaccount;  # remove non-existent accounts
print "3 \@username = @username\n" if $debug;


if ($outfile){
    open(F,"> $outfile") or die "Cannot open $outfile: $!";
    map {printf F "$FORMAT\n",$_} @username;
    close(F);
}else{
    map {printf STDOUT "$FORMAT\n",$_} @username;
}


sub egroup2username(@){
    my %opt = ();
    if (ref($_[0]) eq "HASH"){
        my $href = shift @_;
        %opt = %$href;
    }
    my @egroup = @_;
    #print Dumper(\%opt,\@egroup);exit;

    @egroup = keys %{{map{$_=>1} @egroup}};  # remove duplicate entries

    my $recursion = $opt{recursion};
    my $attribute = $opt{attribute} || "sAMAccountName";
    my @result = ();

    # Set up LDAP connection

    use Net::LDAP;
    use Net::LDAP::Control::Paged;
    use Net::LDAP::Constant qw( LDAP_CONTROL_PAGED );

    my $ldapserver = "xldap.cern.ch";
    my $ldap = Net::LDAP->new($ldapserver,
                              version    => 3,
                              multihomed => 1,
                              timeout    => 15 );
    if (not $ldap){
        print SDTERR "Error connecting to LDAP: $@\n";
        return undef;
    }
    my $page = Net::LDAP::Control::Paged->new( size => 1000 );
    my $mesg = $ldap->bind;
    if (not $mesg){
        print SDTERR "Error binding to LDAP: $@\n";
        return undef;
    }

    # Define the query

    my $query = undef;
    if (scalar(@egroup) == 1){
        $query = "memberOf". ($recursion ? ":1.2.840.113556.1.4.1941:" : "") ."=CN=" . $egroup[0] . ",OU=e-groups,OU=Workgroups,DC=cern,DC=ch";
    }else{
        $query = "|";
        for my $egroup (@egroup){
            $query .= "(memberOf". ($recursion ? ":1.2.840.113556.1.4.1941:" : "") ."=CN=" . $egroup . ",OU=e-groups,OU=Workgroups,DC=cern,DC=ch)";
        }
    }
    print "\$query = \"$query\"\n" if $debug;
    my @args = (base    => "ou=users,ou=organic units,dc=cern,dc=ch",
                scope   => "sub",
                filter  => "$query",
                attrs   => [$attribute],
                control => [$page],
               );
    my $cookie;
    while (1) {
        # Perform query
        my $mesg = $ldap->search(@args);
	
        # Only continue on LDAP_SUCCESS
        $mesg->code and last;

        # Process the result
        my @entries = $mesg->entries;
        printf "LDAP return: %d entries.\n",scalar(@entries) if $debug;

        foreach my $entr (@entries) {
            my $result = $entr->get_value($attribute);
            push(@result,$result) if $result;
        }

        # Get cookie from paged control
        my ($resp) = $mesg->control( LDAP_CONTROL_PAGED ) or last;
        $cookie    = $resp->cookie or last;
    
        # Set cookie in paged control
        $page->cookie($cookie);
    }
    
    if ($cookie) {
        # We had an abnormal exit, so let the server know we do not want any more
        $page->cookie($cookie);
        $page->size(0);
        $ldap->search(@args);
    }

    return @result;
}


__END__


