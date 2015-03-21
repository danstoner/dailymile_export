use LWP::UserAgent;
use JSON::PP;
use Text::CSV;
use Getopt::Long;

# command-line options
my $dm_user;
my $help;
my $debug;
my $gear;

my $usage_text = <<END;

Description:

  Script to download entries from the dailymile API for a particular user into a CSV.

Usage: dailymile_export_to_tsv.pl [OPTIONS] <PARAMETERS>

  Parameters:
    --help, -h        Display this usage help.
    --username, -u    The dailymile.com username to export.

  Options:
    --debug, -d       Enable debug level logging.
    --gear, -g        Enable download of gear info (not yet available)

END


sub usage {
    print $usage_text;
    exit;
}

GetOptions ("help" => \$help,
	    "debug" => \$debug,
	    "gear"  => \$gear,
	    "username=s" => \$dm_user)
or usage();

if ($gear) {
    print "\nGear option is not yet available.\n";
    usage();
}

if ($usage|$help) {
    usage();
}

if (!($dm_user)) {
    print "\nDailymile username is required.\n";
    usage();
}


if ($debug) {
    print "\nDEBUG enabled.\n";
}



print "hello $dm_user!  \n";



__END__

#### below this is the cloned perl6 code

# replace this with proper args parsing
if ! @*ARGS[0] {
 say "Usage:\n \n perl6 dailymile_export_to_tsv.p6 dailymile_username";
 exit;
}
if (@*ARGS[0] eq "-h") | (@*ARGS[0] eq "--help") {
 say "\nUsage:\n perl6 dailymile_export_to_tsv.p6 dailymile_username\n\n";
 exit;
}

my $dm_user = @*ARGS[0]; 


my $page = 1;

my $nowtime = DateTime.new(now);
my $nowtimestring = $nowtime.year ~ $nowtime.month ~ $nowtime.day ~ $nowtime.hour ~ $nowtime.minute ~ $nowtime.second;

## try to create output file here
##
##

my $api_url_entries = "http://api.dailymile.com/people/" ~ $dm_user ~ "/entries.json?page=" ~ $page;

say "First API Request: " ~ $api_url_entries;

my $ua = HTTP::UserAgent.new;
my $response = $ua.get($api_url_entries);

if ! $response.is-success {
  die $response.status-line;
} else {

say from-json('{ "a": 42 }').perl;
say to-json { a => [1, 2, 'b'] };

# save this line for now
my %rjson = %(from-json($response.content));


#  my @rjson = %(from-json($response.content)){'entries'};

### Whether I use an array or a hash, from-json seems to be stuffing everything
### into a single element.
#  say "................................................................";

#   for %rjson{@x} {            
#     $_.say;
# }

  

#  my @entries = %(from-json($response.content)){'entries'}[0];
#  my @entries = %(from-json($response.content)){'entries'}[1];
 
#  for @entries {
# #    say $_ => 'id';
#     say $_{'id'};
#     # say "..................";
#     }

}



say "**** Terminating on purpose.***";
exit;
# code below here not used or not ready
