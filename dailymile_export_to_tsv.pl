use LWP::UserAgent;
use JSON::PP;
#use JSON qw (decode_json);
use Text::CSV;
use Getopt::Long;
use POSIX qw(strftime);
use Log::Message::Simple qw[msg error debug];
use Data::Dumper; # mostly during debugging and testing

use strict;
use warnings;

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
    --debug, -d       Enable debug level output.
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
    print "\nINFO: Gear option is not yet available.\n";
    usage();
}

if ($help) {
    usage();
}

if (!($dm_user)) {
    print "\n** ERROR: Dailymile username is required. **\n";
    usage();
}


if ($debug) {
    debug ("DEBUG enabled.",1);
}


# Begin

my $now_string = strftime "%Y%m%d%H%M%S", localtime;

my $outputfilename = $dm_user."_dailymile_export_p5.".$now_string.".tsv";

my $headerrow = ["id","url","timestamp","title","activity_type","felt","duration_seconds","distance","distance_units","description"];
#["id","url","timestamp","title","activity_type","felt","duration_seconds","distance","distance_units","description"]

my $csv = Text::CSV->new ( { binary => 1 } );
$csv->column_names ($headerrow);

# If cannot write to file, might as well stop here
open my $fh, ">:encoding(utf8)", $outputfilename or die "Could not write to ".$outputfilename." ".$!;

my $status = $csv->print ($fh, $headerrow) or die "Could not write to ".$outputfilename." ".$!;

my $page = 1;

my $api_url_entries = "https://api.dailymile.com/people/" . $dm_user . "/entries.json?page=" . $page;

msg ( "First API Request: ". $api_url_entries , 1 );


my $ua = LWP::UserAgent->new;
my $response = $ua->get($api_url_entries);

my $json = decode_json $response->decoded_content;
print Dumper($json);

__END__

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
