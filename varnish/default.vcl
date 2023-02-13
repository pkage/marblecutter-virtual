vcl 4.0;

backend default {
    .host = "marblecutter";
    .port = "8085";
}

sub vcl_hash {
    hash_data(req.url);
    return (lookup);
}

sub vcl_backend_response {
    set beresp.ttl = 3d;
}

sub vcl_recv {
    if (req.url ~ "^/tiles/") {
        set    req.http.X-Tiler-Cached = "cached";
        return (hash);
    } else {
        set    req.http.X-Tiler-Cached = "not cached";
        return (pass);
    }
}
