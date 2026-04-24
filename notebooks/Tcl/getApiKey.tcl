namespace eval ::ixia {
    set ixApiServer 10.36.94.225
    set ixApiPort   443
    # set ports       {{10.36.77.154 1 1} {10.36.77.154 1 5}}
}

puts "Load IxNetwork API package"
package req Ixia

puts "Get the API key"
# ixNet getApiKey hostname -username user -password pass [-port 443] [-apiKeyFile api.key]
set apiKey [ixNet getApiKey $::ixia::ixApiServer -username admin -password admin]
puts $apiKey

#puts "Connect to IxNetwork API server"
#ixNet connect $::ixia::ixApiServer -port $::ixia::ixApiPort -apiKey $apiKey
