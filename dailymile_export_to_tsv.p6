use v6;
use JSON::Tiny;
use HTTP::UserAgent;
use Text::CSV;

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


## HTTP::Client does not support HTTPS. Will need to look at other libraries.
my $ua = HTTP::UserAgent.new;
my $response = $ua.get($api_url_entries);

if $response.is-success {
  say $response.content;
} else {
  die $response.status-line;
}


#my %rjson = %(from-json($response.content));

#  if ($response.success) {
#     my %rjson = %(from-json($response.content));
#
#     say (%rjson{'id'});
#  }
#  else {
#    say "An error occured.";
# }



say "**** Terminating on purpose.***";
exit;
# code below here not used or not ready
