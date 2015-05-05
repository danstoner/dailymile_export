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

# do the real work

my $page = 1;
my $api_url_entries = "https://api.dailymile.com/people/" . $dm_user . "/entries.json?page=" . $page;
msg ( "First API Request: ". $api_url_entries , 1 );

my $ua = LWP::UserAgent->new;
my $response = $ua->get($api_url_entries);

my $json = decode_json $response->decoded_content; # $json becomes a hash

# print Dumper($json);

for my $entry ( @{$json->{entries}} )
{
    print $entry->{id} . "," . $entry->{url} . "\n";
}


#while (($response->is_success) and (exists $jsonscalar->{entries})) {
#    print $response->decoded_content;  # or whatever

#}

die "die... debugging";
#}
#else {
#    die $response->status_line;
#}




__END__


my $api_url_entries = "http://api.dailymile.com/people/" ~ $dm_user ~ "/entries.json?page=" ~ $page;

say "First API Request: " ~ $api_url_entries;

my $ua = HTTP::UserAgent.new;
my $response = $ua.get($api_url_entries);

if ! $response.is-success {
  die $response.status-line;
} else {
# do someting
}


say "**** Terminating on purpose.***";
exit;
# code below here not used or not ready


##### sample of json (output by Dumper($json)
# $VAR1 = {
#           'entries' => [
#                          {
#                            'id' => 32646089,
#                            'user' => {
#                                        'username' => 'danstoner',
#                                        'display_name' => 'Dan S.',
#                                        'photo_url' => 'https://dnetd3r67cewl.cloudfront.net/unsafe/48x48/https://d2d6zexjsynj7u.cloudfront.net/pictures/users/93956/1429899791.jpg',
#                                        'url' => 'http://www.dailymile.com/people/danstoner'
#                                      },
#                            'url' => 'http://www.dailymile.com/entries/32646089',
#                            'geo' => {
#                                       'coordinates' => [
#                                                          '-82.36792',
#                                                          '29.676735'
#                                                        ],
#                                       'type' => 'Point'
#                                     },
#                            'workout' => {
#                                           'title' => 'Brywood to NW 31st Blvd ( Glen Springs Rd ) out and back',
#                                           'duration' => 2520,
#                                           'activity_type' => 'Running',
#                                           'distance' => {
#                                                           'units' => 'miles',
#                                                           'value' => '4.04'
#                                                         },
#                                           'felt' => 'alright'
#                                         },
#                            'likes' => [],
#                            'comments' => [
#                                            {
#                                              'created_at' => '2015-05-04T14:27:45Z',
#                                              'body' => 'Nice Monday miles!',
#                                              'user' => {
#                                                          'url' => 'http://www.dailymile.com/people/BarbaraW',
#                                                          'photo_url' => 'https://dnetd3r67cewl.cloudfront.net/unsafe/48x48/https://d2d6zexjsynj7u.cloudfront.net/pictures/users/99552/1409113516.jpg',
#                                                          'username' => 'BarbaraW',
#                                                          'display_name' => 'Barbara W.'
#                                                        }
#                                            }
#                                          ],
#                            'location' => {
#                                            'name' => 'Gainesville, FL'
#                                          },
#                            'at' => '2015-05-04T10:25:29Z'
#                          },
#                          {
#                            'url' => 'http://www.dailymile.com/entries/32637156',
#                            'user' => {
#                                        'display_name' => 'Dan S.',
#                                        'username' => 'danstoner',
#                                        'photo_url' => 'https://dnetd3r67cewl.cloudfront.net/unsafe/48x48/https://d2d6zexjsynj7u.cloudfront.net/pictures/users/93956/1429899791.jpg',
#                                        'url' => 'http://www.dailymile.com/people/danstoner'
#                                      }
