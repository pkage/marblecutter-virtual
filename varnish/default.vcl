vcl 4.0;

backend default {
    .host = "marblecutter";
    .port = "8085";
}

sub vcl_hash {
    hash_data(req.url);
    return (lookup);
}


sub vcl_recv {
    if (req.url ~ "^/tiles/") {
        return (hash);
    } else {
        return (pass);
    }
}
