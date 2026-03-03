# IxNetwork for Human

## How to get started

```
sajang@macpro:~/supports/IxNetwork$ docker compose build
sajang@macpro:~/supports/IxNetwork$ docker compose run --rm ixnetwork
ubuntu@d7a13ee8e448:/IxNetwork$ ls
Dockerfile    IxNetworkAPI11.00.2407.37Linux64.bin  LowLevelApi  RestApi  Utilities  docker-compose.yaml
HighLevelApi  LICENSE                               Readme       RestPy   VM
ubuntu@d7a13ee8e448:/IxNetwork$sajang@macpro:~/supports/IxNetwork$
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
