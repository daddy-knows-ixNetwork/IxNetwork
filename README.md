# IxNetwork for Human

## How to get started

```
seunyang@SY-ubuntu24:~/supports/IxNetwork$ docker compose build
seunyang@SY-ubuntu24:~/supports/IxNetwork$ docker compose run --rm ixnetwork
Container ixnetwork-ixnetwork-run-44b92091e841 Creating 
Container ixnetwork-ixnetwork-run-44b92091e841 Created 
ubuntu@655794ae48c4:/IxNetwork$ python HighLevelApi/Ngpf/Python/Traffic/demo_ngpf_traffic.py 
ixiatcl:info: Tcl version: 8.6.12
Tcl 8.6 is installed on 64bit architecture.
IXIA_VERSION env variable is set to 26.0, but this value is not matching any HLTSET. Using default HLTSET (HLTSET289) instead.
Using products based on HLTSET289
IxTclHal is not be used for current HLTSET.
Loaded IxTclNetwork 26.0.2601.6
Mpexpr is not installed.
HLT release 26.0.2601.5
Loaded ixia_hl_lib-26.0 
.
.
.
==== flow count:   2
==== flow:  2  ====
        tx total_pkts:  82305995
        rx total_pkts:  82305995
        rx loss_pkts:  0
==== flow:  1  ====
        tx total_pkts:  82305995
        rx total_pkts:  82305995
        rx loss_pkts:  0

---Flow 1 RX total_pkts:  82305995


Script ended SUCCESSFULLY!
ubuntu@655794ae48c4:/IxNetwork$
```

# The orginal README from the upstream

PlEASE READ:

The IxNetRestApi library in this level /IxNetwork/RestApi is deprecated in favor of using /IxNetwork/RestPy.
RestPy is superior and easier to automate.
It is a library that comes with all IxNetwork class objects for automation.
This means you don't have to request for any wrappers to perform any CRUDs.

See RestPy sample scripts in https://github.com/OpenIxia/IxNetwork/tree/master/RestPy/SampleScripts
loadConfigFile.py and bgpNgpf.py would be great starting points.

With tha said, the IxNetRestApi library is no longer maintained.
There will not be having new functions and enhancements.
