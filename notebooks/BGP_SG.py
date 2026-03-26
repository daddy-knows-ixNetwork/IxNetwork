# IxNetwork version: 11.00.2504.10
# time of scriptgen: 03/17/2026, 15:55
import os
import re
import sys
import time
# sys.path.append('/path/to/hltapi/library/common/ixiangpf/python')
# sys.path.append('/path/to/ixnetwork/api/python')

from ixiatcl import IxiaTcl
from ixiahlt import IxiaHlt
from ixiangpf import IxiaNgpf
from ixiaerror import IxiaError

if os.name == 'nt':
    # Please specify tcl_dependencies if you are not using Ixia provide Python and Tcl.
    # Example: tcl_dependencies = ['C:/Program Files/Python36/tcl/tcl8.6']; ixiatcl = IxiaTcl(tcl_autopath=tcl_dependencies)
    ixiatcl = IxiaTcl()
else:
    # unix dependencies
    tcl_dependencies = [
        '/home/user/ixia/ixos/lib',
        '/home/user/ixia/ixnet/IxTclProtocol',
        '/home/user/ixia/ixnet/IxTclNetwork'
    ]
    ixiatcl = IxiaTcl(tcl_autopath=tcl_dependencies)

ixiahlt = IxiaHlt(ixiatcl, use_legacy_api = 1)
ixiangpf = IxiaNgpf(ixiahlt)

def ixnHLT_endpointMatch(ixnHLT, ixnpattern_list, handle_type='HANDLE'):
    traffic_ep_ignore_list = [
        '^::ixNet::OBJ-/vport:\d+/protocols/mld/host:\d+$',
        '^::ixNet::OBJ-/vport:\d+/protocolStack/ethernet:[^/]+/ipEndpoint:[^/]+/range:[^/]+/ptpRangeOverIp:1$'
    ]

    rval = []
    for pat in ixnpattern_list:
        if pat[ 0] != '^': pat = '^' + pat
        if pat[-1] != '$': pat = pat + '$'

        for path in set(x for x in ixnHLT if x.startswith(handle_type)):
            ixn_path = path.split(',')[1]
            parent_ixn_path = '/'.join(ixn_path.split('/')[:-1])
            parent_path = '%s,%s' % (handle_type, parent_ixn_path)

            parent_found = False
            if len(rval) > 0 and parent_path in ixnHLT and parent_path in rval:
                parent_found = True

            if not parent_found and re.match(pat, ixn_path) and len(ixnHLT[path]) > 0:
                if not any(re.match(x, ixnHLT[path]) for x in traffic_ep_ignore_list):
                    rval.append(ixnHLT[path])

    return rval

# ----------------------------------------------------------------
# Configuration procedure

try:
    ixnHLT_logger('')
except (NameError,):
    def ixnHLT_logger(msg):
        if ixiangpf.INTERACTIVE: print(msg)

try:
    ixnHLT_errorHandler('', {})
except (NameError,):
    def ixnHLT_errorHandler(cmd, retval):
        global ixiatcl
        err = ixiatcl.tcl_error_info()
        log = retval['log']
        additional_info = '> command: %s\n> tcl errorInfo: %s\n> log: %s' % (cmd, err, log)
        raise IxiaError(IxiaError.COMMAND_FAIL, additional_info)

def ixnHLT_Scriptgen_Configure(ixiahlt, ixnHLT):
    ixiatcl = ixiahlt.ixiatcl
    # //vport
    ixnHLT_logger('interface_config://vport:<1>...')
    _result_ = ixiahlt.interface_config(
        mode='config',
        port_handle=ixnHLT['PORT-HANDLE,//vport:<1>'],
        tx_gap_control_mode='average',
        transmit_mode='advanced',
        port_rx_mode='capture_and_measure',
        enable_flow_control='1',
        flow_control_directed_addr='0180.c200.0001',
        data_integrity='1',
        ignore_link='0',
        tx_ignore_rx_link_faults =0,
        intf_mode='novus_10g',
        phy_mode='fiber',
        autonegotiation=0,
        speed='ether10Gig',
        speed_autonegotiation=['ether10Gig'],
        arp_refresh_interval='60'
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_errorHandler('interface_config', _result_)
    # The last configure command did not scriptgen the following attributes:
    # [//vport:<1>]
    # n kBool -useGlobalSettings 'False'
    # n kString -assignedToDisplayName '10.36.88.110;01;03'
    # n kBool -isMapped 'True'
    # n kObjref -connectedTo '$ixNetSG_ref(253)'
    # n kString -adminMode 'Up'
    # n kInteger -internalId '1'
    # n kString -name '10GE LAN - 001'
    # n kString -ixnChassisVersion ''
    # n kString -connectionInfo 'chassis="10.36.88.110" card="1" port="3" portip="10.0.1.3"'
    # n kString -connectionStatus '10.36.88.110;01;03 RG 01'
    # n kString -location '10.36.88.110;1;3'
    # n kEnumValue -captureSupported 'dataAndControl'
    # n kBool -traceEnabled 'False'
    # n kInteger -maxStreamsSupported '512'
    # n kString -ixosChassisVersion 'IxOS 11.10.1110.11 '
    # n kString -dpdkPerformanceAcceleration ''
    # n kBool -isFramePreemptionSupported 'True'
    # n kBool -isCloudstormPort 'False'
    # n kString -ixnClientVersion ''
    # n kArray -validTxModes '{sequential} {interleaved}'
    # n kEnumValue -connectionState 'connectedLinkUp'
    # n kString -resourceMode 'normal'
    # n kEnumValue -typeDisplayName 'novusTenGigLan'
    # n kString -delayCompensation '0'
    # n kString -licenses 'obsolete, do not use'
    # n kString -lastLinkStateChangeEventTimestamp '2026-03-17 15:53:24.040'
    # n kBool -isAvailable 'True'
    # n kBool -isPullOnly 'False'
    # n kInteger -actualSpeed '10000'
    # n kBool -isVMPort 'False'
    # n kString -traceTag 'PROFILE_PCPUSYNC;TRACE_CPF_DOD;ixnetservice;StatViewer;AppErrorModule;IxNetwork'
    # n kEnumValue -traceLevel 'kInfo'
    # n kBool -macsecEnabled 'False'
    # n kBool -isConnected 'True'
    # n kString -connectionStatusDisplayName '10.36.88.110;1;3'
    # n kBool -isDirectConfigModeEnabled 'True'

    try:
    	ixnHLT['HANDLE,//vport:<1>'] = _result_['interface_handle']
    	config_handles = ixnHLT.setdefault('VPORT-CONFIG-HANDLES,//vport:<1>,interface_config', [])
    	config_handles.append(_result_['interface_handle'])
    except:
    	pass
    ixnHLT_logger('COMPLETED: interface_config')

    # //vport
    ixnHLT_logger('interface_config://vport:<2>...')
    _result_ = ixiahlt.interface_config(
        mode='config',
        port_handle=ixnHLT['PORT-HANDLE,//vport:<2>'],
        tx_gap_control_mode='average',
        transmit_mode='advanced',
        port_rx_mode='capture_and_measure',
        enable_flow_control='1',
        flow_control_directed_addr='0180.c200.0001',
        data_integrity='1',
        ignore_link='0',
        tx_ignore_rx_link_faults =0,
        intf_mode='novus_10g',
        phy_mode='fiber',
        autonegotiation=0,
        speed='ether10Gig',
        speed_autonegotiation=['ether10Gig'],
        arp_refresh_interval='60'
    )
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
    	ixnHLT_errorHandler('interface_config', _result_)
    # The last configure command did not scriptgen the following attributes:
    # [//vport:<2>]
    # n kBool -useGlobalSettings 'False'
    # n kString -assignedToDisplayName '10.36.88.110;01;04'
    # n kBool -isMapped 'True'
    # n kObjref -connectedTo '$ixNetSG_ref(254)'
    # n kString -adminMode 'Up'
    # n kInteger -internalId '2'
    # n kString -name '10GE LAN - 002'
    # n kString -ixnChassisVersion ''
    # n kString -connectionInfo 'chassis="10.36.88.110" card="1" port="4" portip="10.0.1.4"'
    # n kString -connectionStatus '10.36.88.110;01;04 RG 01'
    # n kString -location '10.36.88.110;1;4'
    # n kEnumValue -captureSupported 'dataAndControl'
    # n kBool -traceEnabled 'False'
    # n kInteger -maxStreamsSupported '512'
    # n kString -ixosChassisVersion 'IxOS 11.10.1110.11 '
    # n kString -dpdkPerformanceAcceleration ''
    # n kBool -isFramePreemptionSupported 'True'
    # n kBool -isCloudstormPort 'False'
    # n kString -ixnClientVersion ''
    # n kArray -validTxModes '{sequential} {interleaved}'
    # n kEnumValue -connectionState 'connectedLinkUp'
    # n kString -resourceMode 'normal'
    # n kEnumValue -typeDisplayName 'novusTenGigLan'
    # n kString -delayCompensation '0'
    # n kString -licenses 'obsolete, do not use'
    # n kString -lastLinkStateChangeEventTimestamp '2026-03-17 15:53:24.147'
    # n kBool -isAvailable 'True'
    # n kBool -isPullOnly 'False'
    # n kInteger -actualSpeed '10000'
    # n kBool -isVMPort 'False'
    # n kString -traceTag 'PROFILE_PCPUSYNC;TRACE_CPF_DOD;ixnetservice;StatViewer;AppErrorModule;IxNetwork'
    # n kEnumValue -traceLevel 'kInfo'
    # n kBool -macsecEnabled 'False'
    # n kBool -isConnected 'True'
    # n kString -connectionStatusDisplayName '10.36.88.110;1;4'
    # n kBool -isDirectConfigModeEnabled 'True'

    try:
    	ixnHLT['HANDLE,//vport:<2>'] = _result_['interface_handle']
    	config_handles = ixnHLT.setdefault('VPORT-CONFIG-HANDLES,//vport:<2>,interface_config', [])
    	config_handles.append(_result_['interface_handle'])
    except:
    	pass
    ixnHLT_logger('COMPLETED: interface_config')

    # The following objects had no attributes that were scriptgenned:
    # n //globals/statistics/advanced/guardRail
    # n //globals/interfaces
    # n //statistics
    # n //statistics/measurementMode
    # n //vport:<1>/l1Config/novusTenGigLan/fcoe
    # n //vport:<1>/l1Config/rxFilters/filterPalette
    # n //vport:<1>/l1Config/rxFilters/filterPalette
    # n //vport:<1>/capture/trigger
    # n //vport:<1>/capture/filter
    # n //vport:<1>/capture/filterPallette
    # n //vport:<2>/l1Config/novusTenGigLan/fcoe
    # n //vport:<2>/l1Config/rxFilters/filterPalette
    # n //vport:<2>/l1Config/rxFilters/filterPalette
    # n //vport:<2>/capture/trigger
    # n //vport:<2>/capture/filter
    # n //vport:<2>/capture/filterPallette
    # n //reporter
    # n //reporter/testParameters
    # n //reporter/generate
    # n //reporter/saveResults
    # n //globals/statistics
    # n //globals/statistics/advanced/pollingSettings
    # n //globals/statistics/advanced/csvLoggingSettings
    # n //globals/statistics/advanced/dataStoreSettings
    # n //globals/statistics/advanced/timestamp
    # n //globals/statistics/advanced/timeSynchronization
    # n //globals/statistics/advanced/customGraph
    # n //globals/statistics/advanced/egressView
    # n //globals/statistics/datacenter
    # n //globals/statistics/testInspector
    # n //globals/statistics/testInspector/collisions
    # n //globals/statistics/testInspector/crcErrors
    # n //globals/statistics/testInspector/misdirectedPacketCount
    # n //globals/statistics/testInspector/pcsSyncErrors
    # n //globals/statistics/testInspector/lostFrames
    # n //globals/statistics/testInspector/lossPercent
    # n //globals/statistics/testInspector/sequenceErrors
    # n //globals/statistics/testInspector/averageLatency
    # n //globals/statistics/reportGenerator
    # n //globals/statistics/statFilter/oamAggregatedStatistics
    # n //globals/statistics/statFilter/portStatistics
    # n //globals/statistics/statFilter/openflowSwitchAggregatedStatistics
    # n //globals/statistics/statFilter/mldQuerierAggregatedStatistics
    # n //globals/statistics/statFilter/pimsmAggregatedStatistics
    # n //globals/statistics/statFilter/cfmAggregatedStatistics
    # n //globals/statistics/statFilter/mldAggregatedStatistics
    # n //globals/statistics/statFilter/ospfAggregatedStatistics
    # n //globals/statistics/statFilter/eigrpAggregatedStatistics
    # n //globals/statistics/statFilter/ripngAggregatedStatistics
    # n //globals/statistics/statFilter/stpAggregatedStatistics
    # n //globals/statistics/statFilter/igmpQuerierAggregatedStatistics
    # n //globals/statistics/statFilter/openflowAggregatedStatistics
    # n //globals/statistics/statFilter/bgpAggregatedStatistics
    # n //globals/statistics/statFilter/bfdAggregatedStatistics
    # n //globals/statistics/statFilter/lispAggregatedStatistics
    # n //globals/statistics/statFilter/ldpAggregatedStatistics
    # n //globals/statistics/statFilter/igmpAggregatedStatistics
    # n //globals/statistics/statFilter/globalProtocolStatistics
    # n //globals/statistics/statFilter/isisAggregatedStatistics
    # n //globals/statistics/statFilter/rsvpAggregatedStatistics
    # n //globals/statistics/statFilter/ospfv3AggregatedStatistics
    # n //globals/statistics/statFilter/ripAggregatedStatistics
    # n //globals/statistics/statFilter/lacpAggregatedStatistics
    # n //globals/diagnostics/cleanup
    # n //globals/preferences
    # n //globals/preferences/statistics
    # n //globals/preferences/analyzer
    # n //globals/portTestOptions
    # n //statistics/rawData
    # n //timeline
    # n //vport:<1>/l1Config/novusTenGigLan/txLane
    # n //vport:<1>/l1Config/OAM
    # n //vport:<1>/l1Config/framePreemption
    # n //vport:<1>/l1Config/qbv
    # n //vport:<1>/l1Config/fecErrorInsertion
    # n //vport:<1>/l1Config/pcsErrorGeneration
    # n //vport:<1>/l1Config/plca
    # n //vport:<1>/protocols
    # n //vport:<1>/protocols/openFlow
    # n //vport:<1>/protocols/openFlow/hostTopologyLearnedInformation/switchHostRangeLearnedInfoTriggerAttributes
    # n //vport:<1>/protocolStack/options
    # n //vport:<2>/l1Config/novusTenGigLan/txLane
    # n //vport:<2>/l1Config/OAM
    # n //vport:<2>/l1Config/framePreemption
    # n //vport:<2>/l1Config/qbv
    # n //vport:<2>/l1Config/fecErrorInsertion
    # n //vport:<2>/l1Config/pcsErrorGeneration
    # n //vport:<2>/l1Config/plca
    # n //vport:<2>/protocols
    # n //vport:<2>/protocols/openFlow
    # n //vport:<2>/protocols/openFlow/hostTopologyLearnedInformation/switchHostRangeLearnedInfoTriggerAttributes
    # n //vport:<2>/protocolStack/options
    # n //locations:<1>
    # n //locations:<2>
    # end of list

def ixnCPF_Scriptgen_Configure(ixiangpf, ixnHLT):
    ixiatcl = ixiangpf.ixiahlt.ixiatcl

    _result_ = ixiangpf.topology_config(
        topology_name      = """BGP w/Random v4 Prefix/Length""",
        port_handle        = [ixnHLT['PORT-HANDLE,//vport:<1>']],
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)

    # n The attribute: note with the value:  is not supported by scriptgen.
    topology_1_handle = _result_['topology_handle']
    ixnHLT['HANDLE,//topology:<1>'] = topology_1_handle

    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_1_handle,
        device_group_name            = """BGP Router 1""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)

    deviceGroup_1_handle = _result_['device_group_handle']
    ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>'] = deviceGroup_1_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "00.11.01.00.00.01",
        counter_step           = "00.00.00.00.00.01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00.00.01.00.00.00"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_1_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 1""",
        protocol_handle              = deviceGroup_1_handle,
        mtu                          = "1500",
        src_mac_addr                 = multivalue_1_handle,
        vlan                         = "0",
        vlan_id                      = '%s' % ("1"),
        vlan_id_step                 = '%s' % ("0"),
        vlan_id_count                = '%s' % ("1"),
        vlan_tpid                    = '%s' % ("0x8100"),
        vlan_user_priority           = '%s' % ("0"),
        vlan_user_priority_step      = '%s' % ("0"),
        use_vpn_parameters           = "0",
        site_id                      = "0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)

    # n The attribute: useVlans with the value: False is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: connectedVia with the value: {} is not supported by scriptgen.
    # n Node: pbbEVpnParameter is not supported for scriptgen.
    ethernet_1_handle = _result_['ethernet_handle']
    ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>'] = ethernet_1_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "100.1.0.1",
        counter_step           = "0.0.0.1",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_2_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 1""",
        protocol_handle                   = ethernet_1_handle,
        ipv4_multiplier                   = "1",
        ipv4_resolve_gateway              = "1",
        ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
        ipv4_enable_gratarprarp           = "0",
        ipv4_gratarprarp                  = "gratarp",
        gateway                           = "100.1.0.2",
        gateway_step                      = "0.0.0.0",
        intf_ip_addr                      = multivalue_2_handle,
        netmask                           = "255.255.255.0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)

    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    ipv4_1_handle = _result_['ipv4_handle']
    ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>'] = ipv4_1_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "100.1.0.1",
        counter_step           = "0.0.1.0",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_3_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "00:01:01:00:00:01",
        counter_step           = "00:00:00:00:00:01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00:00:01:00:00:00"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_4_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "10.0.1.1",
        counter_step           = "0.0.0.1",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_5_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "192.0.0.1",
        counter_step           = "0.0.0.1",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_1_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_6_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.emulation_bgp_config(
        mode                                                   = "enable",
        active                                                 = "1",
        md5_enable                                             = "0",
        md5_key                                                = "",
        handle                                                 = ipv4_1_handle,
        ip_version                                             = "4",
        remote_ip_addr                                         = "100.1.0.2",
        next_hop_enable                                        = "0",
        next_hop_ip                                            = "0.0.0.0",
        enable_4_byte_as                                       = "0",
        local_as                                               = "0",
        local_as4                                              = "0",
        update_interval                                        = "0",
        count                                                  = "1",
        local_router_id                                        = multivalue_3_handle,
        hold_time                                              = "90",
        neighbor_type                                          = "internal",
        graceful_restart_enable                                = "0",
        restart_time                                           = "45",
        stale_time                                             = "0",
        tcp_window_size                                        = "8192",
        local_router_id_enable                                 = "1",
        ipv4_capability_mdt_nlri                               = "0",
        ipv4_capability_unicast_nlri                           = "1",
        ipv4_filter_unicast_nlri                               = "1",
        ipv4_capability_multicast_nlri                         = "1",
        ipv4_filter_multicast_nlri                             = "0",
        ipv4_capability_mpls_nlri                              = "1",
        ipv4_filter_mpls_nlri                                  = "0",
        ipv4_capability_mpls_vpn_nlri                          = "1",
        ipv4_filter_mpls_vpn_nlri                              = "0",
        ipv6_capability_unicast_nlri                           = "1",
        ipv6_filter_unicast_nlri                               = "1",
        ipv6_capability_multicast_nlri                         = "1",
        ipv6_filter_multicast_nlri                             = "0",
        ipv6_capability_mpls_nlri                              = "1",
        ipv6_filter_mpls_nlri                                  = "0",
        ipv6_capability_mpls_vpn_nlri                          = "1",
        ipv6_filter_mpls_vpn_nlri                              = "0",
        capability_route_refresh                               = "1",
        capability_route_constraint                            = "0",
        ttl_value                                              = "64",
        updates_per_iteration                                  = "1",
        bfd_registration                                       = "0",
        bfd_registration_mode                                  = "multi_hop",
        vpls_capability_nlri                                   = "1",
        vpls_filter_nlri                                       = "0",
        act_as_restarted                                       = "0",
        discard_ixia_generated_routes                          = "0",
        local_router_id_type                                   = "same",
        send_ixia_signature_with_routes                        = "0",
        enable_flap                                            = "0",
        flap_up_time                                           = "0",
        flap_down_time                                         = "0",
        ipv4_capability_multicast_vpn_nlri                     = "0",
        ipv4_filter_multicast_vpn_nlri                         = "0",
        ipv6_capability_multicast_vpn_nlri                     = "0",
        ipv6_filter_multicast_vpn_nlri                         = "0",
        filter_ipv4_multicast_bgp_mpls_vpn                     = "0",
        filter_ipv6_multicast_bgp_mpls_vpn                     = "0",
        ipv4_multicast_bgp_mpls_vpn                            = "0",
        ipv6_multicast_bgp_mpls_vpn                            = "0",
        advertise_end_of_rib                                   = "0",
        configure_keepalive_timer                              = "0",
        keepalive_timer                                        = "30",
        as_path_set_mode                                       = "no_include",
        router_id                                              = multivalue_6_handle,
        filter_link_state                                      = "0",
        capability_linkstate_nonvpn                            = "0",
        bgp_ls_id                                              = "0",
        instance_id                                            = "0",
        number_of_communities                                  = "1",
        enable_community                                       = "0",
        number_of_ext_communities                              = "1",
        enable_ext_community                                   = "0",
        enable_override_peer_as_set_mode                       = "0",
        bgp_ls_as_set_mode                                     = "include_as_seq",
        number_of_as_path_segments                             = "1",
        enable_as_path_segments                                = "0",
        number_of_clusters                                     = "1",
        enable_cluster                                         = "0",
        ethernet_segments_count                                = "0",
        filter_evpn                                            = "0",
        evpn                                                   = "0",
        operational_model                                      = "symmetric",
        routers_mac_or_irb_mac_address                         = multivalue_4_handle,
        capability_ipv4_unicast_add_path                       = "0",
        capability_ipv6_unicast_add_path                       = "0",
        capability_ipv4_mpls_vpn_add_path                      = "false",
        capability_ipv6_mpls_vpn_add_path                      = "false",
        ipv4_mpls_add_path_mode                                = "both",
        ipv6_mpls_add_path_mode                                = "both",
        ipv4_mpls_vpn_add_path_mode                            = "both",
        ipv6_mpls_vpn_add_path_mode                            = "both",
        ipv4_unicast_add_path_mode                             = "both",
        ipv6_unicast_add_path_mode                             = "both",
        ipv4_mpls_capability                                   = "0",
        ipv6_mpls_capability                                   = "0",
        capability_ipv4_mpls_add_path                          = "0",
        capability_ipv6_mpls_add_path                          = "0",
        custom_sid_type                                        = "40",
        srgb_count                                             = "1",
        start_sid                                              = ["16000"],
        sid_count                                              = ["8000"],
        ipv4_multiple_mpls_labels_capability                   = "0",
        ipv6_multiple_mpls_labels_capability                   = "0",
        mpls_labels_count_for_ipv4_mpls_route                  = "1",
        mpls_labels_count_for_ipv6_mpls_route                  = "1",
        noOfUserDefinedAfiSafi                                 = "0",
        capability_ipv4_unicast_flowSpec                       = "0",
        filter_ipv4_unicast_flowSpec                           = "0",
        capability_ipv6_unicast_flowSpec                       = "0",
        filter_ipv6_unicast_flowSpec                           = "0",
        always_include_tunnel_enc_ext_community                = "false",
        ip_vrf_to_ip_vrf_type                                  = "interfaceLess",
        irb_interface_label                                    = "16",
        irb_ipv4_address                                       = multivalue_5_handle,
        capability_ipv4_srte_policy                            = "0",
        filter_ipv4_srte_policy                                = "0",
        capability_ipv6_srte_policy                            = "0",
        filter_ipv6_srte_policy                                = "0",
        max_bgp_message_length_tx                              = "4096",
        capability_extended_message                            = "false",
        l3vpn_encapsulation_type                               = "mpls",
        advertise_tunnel_encapsulation_extended_community      = "1",
        udp_port_start_value                                   = "49152",
        udp_port_end_value                                     = "65535",
        number_color_flex_algo_mapping                         = "0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_bgp_config', _result_)

    # n The attribute: noOfEpePeers with the value: 0 is not supported by scriptgen.
    # n The attribute: enableEpeTraffic with the value: False is not supported by scriptgen.
    # n The attribute: enableLlgr with the value:  is not supported by scriptgen.
    # n The attribute: advertiseEvpnRoutesForOtherVtep with the value: False is not supported by scriptgen.
    # n The attribute: allowIxiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: ixiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: filterLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: capabilityLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: enableBgpLsVpnTx with the value:  is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: name with the value: BGP Peer 1 is not supported by scriptgen.
    # n Node: tlvProfile is not supported for scriptgen.
    bgpIpv4Peer_1_handle = _result_['bgp_handle']
    ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>/bgpIpv4Peer:<1>'] = bgpIpv4Peer_1_handle

    _result_ = ixiangpf.multivalue_config(
        pattern           = "random",
        nest_step         = '%s,%s' % ("0.0.0.1", "0.0.0.1"),
        nest_owner        = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
        nest_enabled      = '%s,%s' % ("0", "0"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    # n Node: random is not supported for scriptgen.
    multivalue_7_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                      = "repeatable_random",
        nest_step                    = '%s,%s' % ("1", "1"),
        nest_owner                   = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
        nest_enabled                 = '%s,%s' % ("0", "0"),
        repeatable_random_seed       = "1",
        repeatable_random_count      = "4000000",
        repeatable_random_fixed      = "24",
        repeatable_random_mask       = "31",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_8_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.network_group_config(
        protocol_handle                      = deviceGroup_1_handle,
        protocol_name                        = """v4 Random Routes""",
        multiplier                           = "5",
        enable_device                        = "1",
        connected_to_handle                  = ethernet_1_handle,
        type                                 = "ipv4-prefix",
        ipv4_prefix_network_address          = multivalue_7_handle,
        ipv4_prefix_length                   = multivalue_8_handle,
        ipv4_prefix_address_step             = "1",
        ipv4_prefix_number_of_addresses      = "100",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('network_group_config', _result_)

    ipv4PrefixPools_1_handle = _result_['ipv4_prefix_pools_handle']
    networkGroup_1_handle = _result_['network_group_handle']
    ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/networkGroup:<1>/ipv4PrefixPools:<1>'] = ipv4PrefixPools_1_handle
    ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/networkGroup:<1>'] = networkGroup_1_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "1"),
        nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
        nest_enabled           = '%s,%s' % ("0", "0"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_9_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "0"),
        nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
        nest_enabled           = '%s,%s' % ("0", "1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_10_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern             = "string",
        string_pattern      = "65550:{Inc:100,1}:10",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_11_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "0"),
        nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
        nest_enabled           = '%s,%s' % ("0", "1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_12_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "0"),
        nest_owner             = '%s,%s' % (deviceGroup_1_handle, topology_1_handle),
        nest_enabled           = '%s,%s' % ("0", "1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_13_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.emulation_bgp_route_config(
        handle                                    = networkGroup_1_handle,
        mode                                      = "create",
        protocol_route_name                       = """BGP IP Route Range 1""",
        active                                    = "1",
        ipv4_unicast_nlri                         = "1",
        max_route_ranges                          = "5",
        ip_version                                = "4",
        prefix                                    = multivalue_7_handle,
        num_routes                                = "100",
        prefix_from                               = multivalue_8_handle,
        packing_from                              = "0",
        packing_to                                = "0",
        enable_traditional_nlri                   = "1",
        next_hop_enable                           = "1",
        next_hop_set_mode                         = "same",
        next_hop_ip_version                       = "4",
        next_hop_ipv4                             = "0.0.0.0",
        next_hop_ipv6                             = "::",
        next_hop_mode                             = "fixed",
        advertise_nexthop_as_v4                   = "0",
        origin_route_enable                       = "1",
        origin                                    = "igp",
        enable_local_pref                         = "1",
        local_pref                                = "0",
        enable_med                                = "0",
        multi_exit_disc                           = "0",
        enable_weight                             = "0",
        weight                                    = "0",
        atomic_aggregate                          = "0",
        enable_aggregator                         = "0",
        aggregator_id_mode                        = "increment",
        aggregator_id                             = "0.0.0.0",
        aggregator_as                             = "0",
        originator_id_enable                      = "0",
        originator_id                             = "0.0.0.0",
        use_safi_multicast                        = "0",
        skip_multicast_routes                     = "1",
        enable_route_flap                         = "0",
        flap_up_time                              = "0",
        flap_down_time                            = "0",
        enable_partial_route_flap                 = "0",
        partial_route_flap_from_route_index       = "0",
        partial_route_flap_to_route_index         = "0",
        flap_delay                                = "0",
        communities_enable                        = "0",
        num_communities                           = "1",
        communities_as_number                     = ["0"],
        communities_last_two_octets               = ["0"],
        communities_type                          = ["no_export"],
        enable_large_communitiy                   = "0",
        num_of_large_communities                  = "1",
        large_community                           = [multivalue_11_handle],
        ext_communities_enable                    = "0",
        num_ext_communities                       = "1",
        ext_communities_as_two_bytes              = ["1"],
        ext_communities_as_four_bytes             = ["1"],
        ext_communities_assigned_two_bytes        = [multivalue_12_handle],
        ext_communities_assigned_four_bytes       = [multivalue_13_handle],
        ext_communities_ip                        = ["1.1.1.1"],
        ext_communities_opaque_data               = ["000000000000"],
        ext_communities_colorCObits               = ["00"],
        ext_communities_colorReservedBits         = ["0"],
        ext_communities_colorValue                = ["0"],
        ext_communities_colorValue_increment      = ["0"],
        ext_communities_link_bandwidth            = ["0"],
        ext_communities_type                      = ["admin_as_two_octet"],
        ext_communities_subtype                   = ["route_target"],
        cluster_list_enable                       = "0",
        num_clusters                              = "1",
        cluster_list                              = ["0.0.0.0"],
        advertise_as_bgpls_prefix                 = "0",
        route_origin                              = "static",
        advertise_as_bgp_3107                     = "0",
        label_end                                 = "1048575",
        label_step                                = "1",
        advertise_as_bgp_3107_sr                  = "0",
        segmentId                                 = "1",
        incrementMode                             = "increment",
        specialLabel                              = "none",
        enableSRGB                                = "0",
        advertise_as_rfc_8277                     = "0",
        no_of_labels                              = "1",
        enable_aigp                               = "0",
        no_of_tlvs                                = "1",
        aigp_type                                 = ["aigptlv"],
        aigp_value                                = ["0"],
        enable_add_path                           = "1",
        add_path_id                               = multivalue_9_handle,
        enable_random_as_path                     = "0",
        max_no_of_as_path_segments                = "10",
        min_no_of_as_path_segments                = "1",
        as_segment_distribution                   = "as_set",
        max_as_numbers_per_segments               = "10",
        min_as_numbers_per_segments               = "1",
        range_of_as_number_suffix                 = "1-65535",
        as_path_per_route                         = "same",
        random_as_seed_value                      = multivalue_10_handle,
        enable_as_path                            = "1",
        num_as_path_segments                      = "1",
        as_path_set_mode                          = "include_as_seq",
        as_path_segment_type                      = ["as_set"],
        num_as_numbers_in_segment                 = ["1"],
        enable_as_path_segment                    = ["1"],
        enable_as_path_segment_number             = ["1"],
        as_path_segment_numbers                   = ["1"],
        override_peer_as_set_mode                 = "0",
        label_start                               = "16",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_bgp_route_config', _result_)

    bgpIPRouteProperty_1_handle = _result_['ip_routes']
    ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/networkGroup:<1>/ipv4PrefixPools:<1>/bgpIPRouteProperty:<1>'] = bgpIPRouteProperty_1_handle

    # n The attribute: addrStepSupported with the value: True is not supported by scriptgen.
    # n The attribute: numberOfAddresses with the value: 100 is not supported by scriptgen.

    # n The attribute: advertiseAsRfc8277SR with the value: False is not supported by scriptgen.
    # n The attribute: noOfSegmentIds with the value: 1 is not supported by scriptgen.
    # n The attribute: tracerouteIdentifier with the value:  is not supported by scriptgen.
    # n The attribute: srcHostCountPerPrefix with the value:  is not supported by scriptgen.
    # n The attribute: destinationPrefix with the value:  is not supported by scriptgen.
    # n The attribute: dstPrefixLen with the value:  is not supported by scriptgen.
    # n The attribute: destinationPrefixIpv6 with the value:  is not supported by scriptgen.
    # n The attribute: dstPrefixLenIpv6 with the value:  is not supported by scriptgen.
    # n The attribute: dstAddrCnt with the value:  is not supported by scriptgen.
    # n The attribute: dstHostCountPerPrefix with the value:  is not supported by scriptgen.
    # n The attribute: meshing with the value:  is not supported by scriptgen.
    # n The attribute: mvNextHopStepIpv4 with the value:  is not supported by scriptgen.
    # n The attribute: mvNextHopStepIpv6 with the value:  is not supported by scriptgen.
    # n The attribute: mvNextHopCount with the value:  is not supported by scriptgen.
    # n The attribute: noOfCustomAttributes with the value: 0 is not supported by scriptgen.
    # n Node: Bgp8277SRSegmentIdList is not supported for scriptgen.
    # n Node: importBgpRoutesParams is not supported for scriptgen.
    # n Node: generateIpv6RoutesParams is not supported for scriptgen.
    # n Node: generateRoutesParams is not supported for scriptgen.

    _result_ = ixiangpf.topology_config(
        topology_name      = """BGP w/Random v6 Prefix/Length""",
        port_handle        = [ixnHLT['PORT-HANDLE,//vport:<2>']],
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)

    # n The attribute: note with the value:  is not supported by scriptgen.
    topology_2_handle = _result_['topology_handle']
    ixnHLT['HANDLE,//topology:<2>'] = topology_2_handle

    _result_ = ixiangpf.topology_config(
        topology_handle              = topology_2_handle,
        device_group_name            = """BGP Router 2""",
        device_group_multiplier      = "1",
        device_group_enabled         = "1",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('topology_config', _result_)

    deviceGroup_2_handle = _result_['device_group_handle']
    ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>'] = deviceGroup_2_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "00.12.01.00.00.01",
        counter_step           = "00.00.00.00.00.01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00.00.01.00.00.00"),
        nest_owner             = '%s' % (topology_2_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_14_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                = """Ethernet 2""",
        protocol_handle              = deviceGroup_2_handle,
        mtu                          = "1500",
        src_mac_addr                 = multivalue_14_handle,
        vlan                         = "0",
        vlan_id                      = '%s' % ("1"),
        vlan_id_step                 = '%s' % ("0"),
        vlan_id_count                = '%s' % ("1"),
        vlan_tpid                    = '%s' % ("0x8100"),
        vlan_user_priority           = '%s' % ("0"),
        vlan_user_priority_step      = '%s' % ("0"),
        use_vpn_parameters           = "0",
        site_id                      = "0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)

    # n The attribute: useVlans with the value: False is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: connectedVia with the value: {} is not supported by scriptgen.
    # n Node: pbbEVpnParameter is not supported for scriptgen.
    ethernet_2_handle = _result_['ethernet_handle']
    ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>'] = ethernet_2_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "100.1.0.2",
        counter_step           = "0.0.0.1",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_2_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_15_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.interface_config(
        protocol_name                     = """IPv4 2""",
        protocol_handle                   = ethernet_2_handle,
        ipv4_multiplier                   = "1",
        ipv4_resolve_gateway              = "1",
        ipv4_manual_gateway_mac           = "00.00.00.00.00.01",
        ipv4_manual_gateway_mac_step      = "00.00.00.00.00.00",
        ipv4_enable_gratarprarp           = "0",
        ipv4_gratarprarp                  = "gratarp",
        gateway                           = "100.1.0.1",
        gateway_step                      = "0.0.0.0",
        intf_ip_addr                      = multivalue_15_handle,
        netmask                           = "255.255.255.0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)

    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    ipv4_2_handle = _result_['ipv4_handle']
    ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>'] = ipv4_2_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "100.1.0.2",
        counter_step           = "0.0.1.0",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_2_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_16_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "00:01:02:00:00:01",
        counter_step           = "00:00:00:00:00:01",
        counter_direction      = "increment",
        nest_step              = '%s' % ("00:00:01:00:00:00"),
        nest_owner             = '%s' % (topology_2_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_17_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "11.0.1.1",
        counter_step           = "0.0.0.1",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_2_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_18_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "192.0.0.2",
        counter_step           = "0.0.0.1",
        counter_direction      = "increment",
        nest_step              = '%s' % ("0.1.0.0"),
        nest_owner             = '%s' % (topology_2_handle),
        nest_enabled           = '%s' % ("1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_19_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.emulation_bgp_config(
        mode                                                   = "enable",
        active                                                 = "1",
        md5_enable                                             = "0",
        md5_key                                                = "",
        handle                                                 = ipv4_2_handle,
        ip_version                                             = "4",
        remote_ip_addr                                         = "100.1.0.1",
        next_hop_enable                                        = "0",
        next_hop_ip                                            = "0.0.0.0",
        enable_4_byte_as                                       = "0",
        local_as                                               = "0",
        local_as4                                              = "0",
        update_interval                                        = "0",
        count                                                  = "1",
        local_router_id                                        = multivalue_16_handle,
        hold_time                                              = "90",
        neighbor_type                                          = "internal",
        graceful_restart_enable                                = "0",
        restart_time                                           = "45",
        stale_time                                             = "0",
        tcp_window_size                                        = "8192",
        local_router_id_enable                                 = "1",
        ipv4_capability_mdt_nlri                               = "0",
        ipv4_capability_unicast_nlri                           = "1",
        ipv4_filter_unicast_nlri                               = "1",
        ipv4_capability_multicast_nlri                         = "1",
        ipv4_filter_multicast_nlri                             = "0",
        ipv4_capability_mpls_nlri                              = "1",
        ipv4_filter_mpls_nlri                                  = "0",
        ipv4_capability_mpls_vpn_nlri                          = "1",
        ipv4_filter_mpls_vpn_nlri                              = "0",
        ipv6_capability_unicast_nlri                           = "1",
        ipv6_filter_unicast_nlri                               = "1",
        ipv6_capability_multicast_nlri                         = "1",
        ipv6_filter_multicast_nlri                             = "0",
        ipv6_capability_mpls_nlri                              = "1",
        ipv6_filter_mpls_nlri                                  = "0",
        ipv6_capability_mpls_vpn_nlri                          = "1",
        ipv6_filter_mpls_vpn_nlri                              = "0",
        capability_route_refresh                               = "1",
        capability_route_constraint                            = "0",
        ttl_value                                              = "64",
        updates_per_iteration                                  = "1",
        bfd_registration                                       = "0",
        bfd_registration_mode                                  = "multi_hop",
        vpls_capability_nlri                                   = "1",
        vpls_filter_nlri                                       = "0",
        act_as_restarted                                       = "0",
        discard_ixia_generated_routes                          = "0",
        local_router_id_type                                   = "same",
        send_ixia_signature_with_routes                        = "0",
        enable_flap                                            = "0",
        flap_up_time                                           = "0",
        flap_down_time                                         = "0",
        ipv4_capability_multicast_vpn_nlri                     = "0",
        ipv4_filter_multicast_vpn_nlri                         = "0",
        ipv6_capability_multicast_vpn_nlri                     = "0",
        ipv6_filter_multicast_vpn_nlri                         = "0",
        filter_ipv4_multicast_bgp_mpls_vpn                     = "0",
        filter_ipv6_multicast_bgp_mpls_vpn                     = "0",
        ipv4_multicast_bgp_mpls_vpn                            = "0",
        ipv6_multicast_bgp_mpls_vpn                            = "0",
        advertise_end_of_rib                                   = "0",
        configure_keepalive_timer                              = "0",
        keepalive_timer                                        = "30",
        as_path_set_mode                                       = "no_include",
        router_id                                              = multivalue_19_handle,
        filter_link_state                                      = "0",
        capability_linkstate_nonvpn                            = "0",
        bgp_ls_id                                              = "0",
        instance_id                                            = "0",
        number_of_communities                                  = "1",
        enable_community                                       = "0",
        number_of_ext_communities                              = "1",
        enable_ext_community                                   = "0",
        enable_override_peer_as_set_mode                       = "0",
        bgp_ls_as_set_mode                                     = "include_as_seq",
        number_of_as_path_segments                             = "1",
        enable_as_path_segments                                = "0",
        number_of_clusters                                     = "1",
        enable_cluster                                         = "0",
        ethernet_segments_count                                = "0",
        filter_evpn                                            = "0",
        evpn                                                   = "0",
        operational_model                                      = "symmetric",
        routers_mac_or_irb_mac_address                         = multivalue_17_handle,
        capability_ipv4_unicast_add_path                       = "0",
        capability_ipv6_unicast_add_path                       = "0",
        capability_ipv4_mpls_vpn_add_path                      = "false",
        capability_ipv6_mpls_vpn_add_path                      = "false",
        ipv4_mpls_add_path_mode                                = "both",
        ipv6_mpls_add_path_mode                                = "both",
        ipv4_mpls_vpn_add_path_mode                            = "both",
        ipv6_mpls_vpn_add_path_mode                            = "both",
        ipv4_unicast_add_path_mode                             = "both",
        ipv6_unicast_add_path_mode                             = "both",
        ipv4_mpls_capability                                   = "0",
        ipv6_mpls_capability                                   = "0",
        capability_ipv4_mpls_add_path                          = "0",
        capability_ipv6_mpls_add_path                          = "0",
        custom_sid_type                                        = "40",
        srgb_count                                             = "1",
        start_sid                                              = ["16000"],
        sid_count                                              = ["8000"],
        ipv4_multiple_mpls_labels_capability                   = "0",
        ipv6_multiple_mpls_labels_capability                   = "0",
        mpls_labels_count_for_ipv4_mpls_route                  = "1",
        mpls_labels_count_for_ipv6_mpls_route                  = "1",
        noOfUserDefinedAfiSafi                                 = "0",
        capability_ipv4_unicast_flowSpec                       = "0",
        filter_ipv4_unicast_flowSpec                           = "0",
        capability_ipv6_unicast_flowSpec                       = "0",
        filter_ipv6_unicast_flowSpec                           = "0",
        always_include_tunnel_enc_ext_community                = "false",
        ip_vrf_to_ip_vrf_type                                  = "interfaceLess",
        irb_interface_label                                    = "16",
        irb_ipv4_address                                       = multivalue_18_handle,
        capability_ipv4_srte_policy                            = "0",
        filter_ipv4_srte_policy                                = "0",
        capability_ipv6_srte_policy                            = "0",
        filter_ipv6_srte_policy                                = "0",
        max_bgp_message_length_tx                              = "4096",
        capability_extended_message                            = "false",
        l3vpn_encapsulation_type                               = "mpls",
        advertise_tunnel_encapsulation_extended_community      = "1",
        udp_port_start_value                                   = "49152",
        udp_port_end_value                                     = "65535",
        number_color_flex_algo_mapping                         = "0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_bgp_config', _result_)

    # n The attribute: noOfEpePeers with the value: 0 is not supported by scriptgen.
    # n The attribute: enableEpeTraffic with the value: False is not supported by scriptgen.
    # n The attribute: enableLlgr with the value:  is not supported by scriptgen.
    # n The attribute: advertiseEvpnRoutesForOtherVtep with the value: False is not supported by scriptgen.
    # n The attribute: allowIxiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: ixiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: filterLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: capabilityLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: enableBgpLsVpnTx with the value:  is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: name with the value: BGP Peer 2 is not supported by scriptgen.
    # n Node: tlvProfile is not supported for scriptgen.
    bgpIpv4Peer_2_handle = _result_['bgp_handle']
    ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>/bgpIpv4Peer:<1>'] = bgpIpv4Peer_2_handle

    _result_ = ixiangpf.multivalue_config(
        pattern           = "random",
        nest_step         = '%s,%s' % ("::0.0.0.1", "::0.0.0.1"),
        nest_owner        = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
        nest_enabled      = '%s,%s' % ("0", "0"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    # n Node: random is not supported for scriptgen.
    multivalue_20_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                      = "repeatable_random",
        nest_step                    = '%s,%s' % ("1", "1"),
        nest_owner                   = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
        nest_enabled                 = '%s,%s' % ("0", "0"),
        repeatable_random_seed       = "1",
        repeatable_random_count      = "4000000",
        repeatable_random_fixed      = "64",
        repeatable_random_mask       = "127",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_21_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.network_group_config(
        protocol_handle                      = deviceGroup_2_handle,
        protocol_name                        = """Network Group 1""",
        multiplier                           = "5",
        enable_device                        = "1",
        connected_to_handle                  = ethernet_2_handle,
        type                                 = "ipv6-prefix",
        ipv6_prefix_network_address          = multivalue_20_handle,
        ipv6_prefix_length                   = multivalue_21_handle,
        ipv6_prefix_address_step             = "1",
        ipv6_prefix_number_of_addresses      = "100",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('network_group_config', _result_)

    ipv6PrefixPools_1_handle = _result_['ipv6_prefix_pools_handle']
    networkGroup_3_handle = _result_['network_group_handle']
    ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/networkGroup:<1>/ipv6PrefixPools:<1>'] = ipv6PrefixPools_1_handle
    ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/networkGroup:<1>'] = networkGroup_3_handle

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "1"),
        nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
        nest_enabled           = '%s,%s' % ("0", "0"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_22_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "0"),
        nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
        nest_enabled           = '%s,%s' % ("0", "1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_23_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern             = "string",
        string_pattern      = "65550:{Inc:100,1}:10",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_24_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "0"),
        nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
        nest_enabled           = '%s,%s' % ("0", "1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_25_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.multivalue_config(
        pattern                = "counter",
        counter_start          = "1",
        counter_step           = "1",
        counter_direction      = "increment",
        nest_step              = '%s,%s' % ("1", "0"),
        nest_owner             = '%s,%s' % (deviceGroup_2_handle, topology_2_handle),
        nest_enabled           = '%s,%s' % ("0", "1"),
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('multivalue_config', _result_)

    multivalue_26_handle = _result_['multivalue_handle']

    _result_ = ixiangpf.emulation_bgp_route_config(
        handle                                    = networkGroup_3_handle,
        mode                                      = "create",
        protocol_route_name                       = """BGP IP Route Range 2""",
        active                                    = "1",
        ipv4_unicast_nlri                         = "1",
        max_route_ranges                          = "5",
        ip_version                                = "6",
        prefix                                    = multivalue_20_handle,
        num_routes                                = "100",
        prefix_from                               = multivalue_21_handle,
        packing_from                              = "0",
        packing_to                                = "0",
        enable_traditional_nlri                   = "1",
        next_hop_enable                           = "1",
        next_hop_set_mode                         = "same",
        next_hop_ip_version                       = "4",
        next_hop_ipv4                             = "0.0.0.0",
        next_hop_ipv6                             = "::",
        next_hop_mode                             = "fixed",
        advertise_nexthop_as_v4                   = "0",
        origin_route_enable                       = "1",
        origin                                    = "igp",
        enable_local_pref                         = "1",
        local_pref                                = "0",
        enable_med                                = "0",
        multi_exit_disc                           = "0",
        enable_weight                             = "0",
        weight                                    = "0",
        atomic_aggregate                          = "0",
        enable_aggregator                         = "0",
        aggregator_id_mode                        = "increment",
        aggregator_id                             = "0.0.0.0",
        aggregator_as                             = "0",
        originator_id_enable                      = "0",
        originator_id                             = "0.0.0.0",
        use_safi_multicast                        = "0",
        skip_multicast_routes                     = "1",
        enable_route_flap                         = "0",
        flap_up_time                              = "0",
        flap_down_time                            = "0",
        enable_partial_route_flap                 = "0",
        partial_route_flap_from_route_index       = "0",
        partial_route_flap_to_route_index         = "0",
        flap_delay                                = "0",
        communities_enable                        = "0",
        num_communities                           = "1",
        communities_as_number                     = ["0"],
        communities_last_two_octets               = ["0"],
        communities_type                          = ["no_export"],
        enable_large_communitiy                   = "0",
        num_of_large_communities                  = "1",
        large_community                           = [multivalue_24_handle],
        ext_communities_enable                    = "0",
        num_ext_communities                       = "1",
        ext_communities_as_two_bytes              = ["1"],
        ext_communities_as_four_bytes             = ["1"],
        ext_communities_assigned_two_bytes        = [multivalue_25_handle],
        ext_communities_assigned_four_bytes       = [multivalue_26_handle],
        ext_communities_ip                        = ["1.1.1.1"],
        ext_communities_opaque_data               = ["000000000000"],
        ext_communities_colorCObits               = ["00"],
        ext_communities_colorReservedBits         = ["0"],
        ext_communities_colorValue                = ["0"],
        ext_communities_colorValue_increment      = ["0"],
        ext_communities_link_bandwidth            = ["0"],
        ext_communities_type                      = ["admin_as_two_octet"],
        ext_communities_subtype                   = ["route_target"],
        cluster_list_enable                       = "0",
        num_clusters                              = "1",
        cluster_list                              = ["0.0.0.0"],
        advertise_as_bgpls_prefix                 = "0",
        route_origin                              = "static",
        advertise_as_bgp_3107                     = "0",
        label_end                                 = "1048575",
        label_step                                = "1",
        advertise_as_bgp_3107_sr                  = "0",
        segmentId                                 = "1",
        incrementMode                             = "increment",
        specialLabel                              = "none",
        enableSRGB                                = "0",
        advertise_as_rfc_8277                     = "0",
        no_of_labels                              = "1",
        enable_aigp                               = "0",
        no_of_tlvs                                = "1",
        aigp_type                                 = ["aigptlv"],
        aigp_value                                = ["0"],
        enable_add_path                           = "1",
        add_path_id                               = multivalue_22_handle,
        enable_random_as_path                     = "0",
        max_no_of_as_path_segments                = "10",
        min_no_of_as_path_segments                = "1",
        as_segment_distribution                   = "as_set",
        max_as_numbers_per_segments               = "10",
        min_as_numbers_per_segments               = "1",
        range_of_as_number_suffix                 = "1-65535",
        as_path_per_route                         = "same",
        random_as_seed_value                      = multivalue_23_handle,
        enable_as_path                            = "1",
        num_as_path_segments                      = "1",
        as_path_set_mode                          = "include_as_seq",
        as_path_segment_type                      = ["as_set"],
        num_as_numbers_in_segment                 = ["1"],
        enable_as_path_segment                    = ["1"],
        enable_as_path_segment_number             = ["1"],
        as_path_segment_numbers                   = ["1"],
        override_peer_as_set_mode                 = "0",
        label_start                               = "16",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_bgp_route_config', _result_)

    bgpIPRouteProperty_2_handle = _result_['ip_routes']
    ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/networkGroup:<1>/ipv6PrefixPools:<1>/bgpIPRouteProperty:<1>'] = bgpIPRouteProperty_2_handle

    # n The attribute: addrStepSupported with the value: True is not supported by scriptgen.
    # n The attribute: numberOfAddresses with the value: 100 is not supported by scriptgen.

    # n The attribute: advertiseAsRfc8277SR with the value: False is not supported by scriptgen.
    # n The attribute: noOfSegmentIds with the value: 1 is not supported by scriptgen.
    # n The attribute: tracerouteIdentifier with the value:  is not supported by scriptgen.
    # n The attribute: srcHostCountPerPrefix with the value:  is not supported by scriptgen.
    # n The attribute: destinationPrefix with the value:  is not supported by scriptgen.
    # n The attribute: dstPrefixLen with the value:  is not supported by scriptgen.
    # n The attribute: destinationPrefixIpv6 with the value:  is not supported by scriptgen.
    # n The attribute: dstPrefixLenIpv6 with the value:  is not supported by scriptgen.
    # n The attribute: dstAddrCnt with the value:  is not supported by scriptgen.
    # n The attribute: dstHostCountPerPrefix with the value:  is not supported by scriptgen.
    # n The attribute: meshing with the value:  is not supported by scriptgen.
    # n The attribute: mvNextHopStepIpv4 with the value:  is not supported by scriptgen.
    # n The attribute: mvNextHopStepIpv6 with the value:  is not supported by scriptgen.
    # n The attribute: mvNextHopCount with the value:  is not supported by scriptgen.
    # n The attribute: noOfCustomAttributes with the value: 0 is not supported by scriptgen.
    # n Node: Bgp8277SRSegmentIdList is not supported for scriptgen.
    # n Node: importBgpRoutesParams is not supported for scriptgen.
    # n Node: generateIpv6RoutesParams is not supported for scriptgen.
    # n Node: generateRoutesParams is not supported for scriptgen.

    # n Node: /globals/topology/ipv6Autoconfiguration does not have global settings.
    # n Node: /globals/topology/ipv6 does not have global settings.
    # n Node: /globals/topology/bfdRouter does not have global settings.
    # n Node: /globals/topology/ospfv2Router does not have global settings.
    # n Node: /globals/topology/ospfv3Router does not have global settings.
    # n Node: /globals/topology/pimRouter does not have global settings.
    # n Node: /globals/topology/rsvpteLsps does not have global settings.
    # n Node: /globals/topology/rsvpteIf does not have global settings.
    # n Node: /globals/topology/isisFabricPathRouter does not have global settings.
    # n Node: /globals/topology/isisL3Router does not have global settings.
    # n Node: /globals/topology/isisSpbRouter does not have global settings.
    # n Node: /globals/topology/isisTrillRouter does not have global settings.
    # n Node: /globals/topology/igmpHost does not have global settings.
    # n Node: /globals/topology/mldHost does not have global settings.
    # n Node: /globals/topology/ldpBasicRouterV6 does not have global settings.
    # n Node: /globals/topology/ldpBasicRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouterV6 does not have global settings.
    # n Node: /globals/topology/msrpListener does not have global settings.
    # n Node: /globals/topology/msrpTalker does not have global settings.
    # n Node: /globals/topology/igmpQuerier does not have global settings.
    # n Node: /globals/topology/mldQuerier does not have global settings.
    # n Node: /globals/topology/dhcpv4client does not have global settings.
    # n Node: /globals/topology/dhcpv6client does not have global settings.
    # n Node: /globals/topology/dhcpv4server does not have global settings.
    # n Node: /globals/topology/dhcpv6server does not have global settings.
    # n Node: /globals/topology/dhcpv4relayAgent does not have global settings.
    # n Node: /globals/topology/lightweightDhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/dhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/pppoxclient does not have global settings.
    # n Node: /globals/topology/pppoxserver does not have global settings.
    # n Node: /globals/topology/lac does not have global settings.
    # n Node: /globals/topology/lns does not have global settings.
    # n Node: /globals/topology/vxlangpe does not have global settings.
    # n Node: /globals/topology/vxlanv6gpe does not have global settings.
    # n Node: /globals/topology/vxlanv6 does not have global settings.
    # n Node: /globals/topology/vxlan does not have global settings.
    # n Node: /globals/topology/geneve does not have global settings.
    # n Node: /globals/topology/greoipv4 does not have global settings.
    # n Node: /globals/topology/greoipv6 does not have global settings.
    # n Node: /globals/topology/ptp does not have global settings.
    # n Node: /globals/topology/ancp does not have global settings.
    # n Node: /globals/topology/lacp does not have global settings.
    # n Node: /globals/topology/lagportlacp does not have global settings.
    # n Node: /globals/topology/staticLag does not have global settings.
    # n Node: /globals/topology/lagportstaticlag does not have global settings.
    # n Node: /globals/topology/openFlowChannel does not have global settings.
    # n Node: /globals/topology/openFlowController does not have global settings.
    # n Node: /globals/topology/pcc does not have global settings.
    # n Node: /globals/topology/pce does not have global settings.
    # n Node: /globals/topology/ovsdbcontroller does not have global settings.
    # n Node: /globals/topology/ovsdbserver does not have global settings.
    # n Node: /globals/topology/cfmBridge does not have global settings.
    # n Node: /globals/topology/netconfClient does not have global settings.
    # n Node: /globals/topology/netconfServer does not have global settings.
    # n Node: /globals/topology/eCpriRe does not have global settings.
    # n Node: /globals/topology/eCpriRec does not have global settings.
    # n Node: /globals/topology/ecpriRec does not have global settings.
    # n Node: /globals/topology/ere does not have global settings.
    # n Node: /globals/topology/dotOneX does not have global settings.
    # n Node: /globals/topology/ntpclock does not have global settings.
    # n Node: /globals/topology/macsec does not have global settings.
    # n Node: /globals/topology/staticMacsec does not have global settings.
    # n Node: /globals/topology/mka does not have global settings.
    # n Node: /globals/topology/bondedGRE does not have global settings.
    # n Node: /globals/topology/esmc does not have global settings.
    # n Node: /globals/topology/cuspCP does not have global settings.
    # n Node: /globals/topology/cuspUP does not have global settings.
    # n Node: /globals/topology/upGroupInfo does not have global settings.
    # n Node: /globals/topology/gRIBIClient does not have global settings.
    # n Node: /globals/topology/gRPCClient does not have global settings.
    # n Node: /globals/topology/twampIpv4 does not have global settings.
    # n Node: /globals/topology/twampIpv6 does not have global settings.
    # n Node: /globals/topology/ptprobeinstancesrv6 does not have global settings.
    # n Node: /globals/topology/roce6v2 does not have global settings.
    # n Node: /globals/topology/rocev2 does not have global settings.
    # n Node: /globals/topology/protocolWizards does not have global settings.
    # n Node: /globals/topology/defaultStacks:1 does not have global settings.
    # n Node: /globals/topology/defaultStacks:2 does not have global settings.
    # n Node: /globals/topology/defaultStacks:3 does not have global settings.
    # n Node: /globals/topology/defaultStacks:4 does not have global settings.
    # n Node: /globals/topology/defaultStacks:5 does not have global settings.
    # n Node: /globals/topology/defaultStacks:6 does not have global settings.
    # n Node: /globals/topology/defaultStacks:7 does not have global settings.
    # n Node: /globals/topology/defaultStacks:8 does not have global settings.
    # n Node: /globals/topology/defaultStacks:9 does not have global settings.
    # n Node: /globals/topology/defaultStacks:10 does not have global settings.
    # n Node: /globals/topology/defaultStacks:11 does not have global settings.
    # n Node: /globals/topology/defaultStacks:12 does not have global settings.
    # n Node: /globals/topology/defaultStacks:13 does not have global settings.
    # n Node: /globals/topology/defaultStacks:14 does not have global settings.
    # n Node: /globals/topology/defaultStacks:15 does not have global settings.
    # n Node: /globals/topology/defaultStacks:16 does not have global settings.
    # n Node: /globals/topology/defaultStacks:17 does not have global settings.
    # n Node: /globals/topology/defaultStacks:18 does not have global settings.
    # n Node: /globals/topology/defaultStacks:19 does not have global settings.
    # n Node: /globals/topology/defaultStacks:20 does not have global settings.
    # n Node: /globals/topology/defaultStacks:21 does not have global settings.
    # n Node: /globals/topology/defaultStacks:22 does not have global settings.
    # n Node: /globals/topology/defaultStacks:23 does not have global settings.
    # n Node: /globals/topology/defaultStacks:24 does not have global settings.
    # n Node: /globals/topology/defaultStacks:25 does not have global settings.
    # n Node: /globals/topology/defaultStacks:26 does not have global settings.
    # n Node: /globals/topology/defaultStacks:27 does not have global settings.
    # n Node: /globals/topology/defaultStacks:28 does not have global settings.
    # n Node: /globals/topology/defaultStacks:29 does not have global settings.
    # n Node: /globals/topology/defaultStacks:30 does not have global settings.
    # n Node: /globals/topology/defaultStacks:31 does not have global settings.
    # n Node: /globals/topology/defaultStacks:32 does not have global settings.
    # n Node: /globals/topology/defaultStacks:33 does not have global settings.
    # n Node: /globals/topology/defaultStacks:34 does not have global settings.
    # n Node: /globals/topology/defaultStacks:35 does not have global settings.
    # n Node: /globals/topology/defaultStacks:36 does not have global settings.
    # n Node: /globals/topology/defaultStacks:37 does not have global settings.
    # n Node: /globals/topology/defaultStacks:38 does not have global settings.
    # n Node: /globals/topology/defaultStacks:39 does not have global settings.
    # n Node: /globals/topology/defaultStacks:40 does not have global settings.
    # n Node: /globals/topology/defaultStacks:41 does not have global settings.
    # n Node: /globals/topology/defaultStacks:42 does not have global settings.
    # n Node: /globals/topology/defaultStacks:43 does not have global settings.
    # n Node: /globals/topology/defaultStacks:44 does not have global settings.
    # n Node: /globals/topology/defaultStacks:45 does not have global settings.
    # n Node: /globals/topology/defaultStacks:46 does not have global settings.
    # n Node: /globals/topology/defaultStacks:47 does not have global settings.
    # n Node: /globals/topology/defaultStacks:48 does not have global settings.
    # n Node: /globals/topology/defaultStacks:49 does not have global settings.
    # n Node: /globals/topology/defaultStacks:50 does not have global settings.
    # n Node: /globals/topology/defaultStacks:51 does not have global settings.
    # n Node: /globals/topology/defaultStacks:52 does not have global settings.
    # n Node: /globals/topology/defaultStacks:53 does not have global settings.
    # n Node: /globals/topology/defaultStacks:54 does not have global settings.
    # n Node: /globals/topology/defaultStacks:55 does not have global settings.
    # n Node: /globals/topology/defaultStacks:56 does not have global settings.
    # n Node: /globals/topology/defaultStacks:57 does not have global settings.
    # n Node: /globals/topology/defaultStacks:58 does not have global settings.
    # n Node: /globals/topology/defaultStacks:59 does not have global settings.
    # n Node: /globals/topology/defaultStacks:60 does not have global settings.
    # n Node: /globals/topology/defaultStacks:61 does not have global settings.
    # n Node: /globals/topology/defaultStacks:62 does not have global settings.
    # n Node: /globals/topology/defaultStacks:63 does not have global settings.
    # n Node: /globals/topology/defaultStacks:64 does not have global settings.
    # n Node: /globals/topology/defaultStacks:65 does not have global settings.
    # n Node: /globals/topology/defaultStacks:66 does not have global settings.
    # n Node: /globals/topology/defaultStacks:67 does not have global settings.
    # n Node: /globals/topology/defaultStacks:68 does not have global settings.
    # n Node: /globals/topology/defaultStacks:69 does not have global settings.
    # n Node: /globals/topology/defaultStacks:70 does not have global settings.
    # n Node: /globals/topology/defaultStacks:71 does not have global settings.
    # n Node: /globals/topology/defaultStacks:72 does not have global settings.
    # n Node: /globals/topology/defaultStacks:73 does not have global settings.
    # n Node: /globals/topology/defaultStacks:74 does not have global settings.
    # n Node: /globals/topology/defaultStacks:75 does not have global settings.
    # n Node: /globals/topology/defaultStacks:76 does not have global settings.
    # n Node: /globals/topology/defaultStacks:77 does not have global settings.
    # n Node: /globals/topology/defaultStacks:78 does not have global settings.
    # n Node: /globals/topology/defaultStacks:79 does not have global settings.
    # n Node: /globals/topology/defaultStacks:80 does not have global settings.
    # n Node: /globals/topology/defaultStacks:81 does not have global settings.
    # n Node: /globals/topology/defaultStacks:82 does not have global settings.
    # n Node: /globals/topology/defaultStacks:83 does not have global settings.
    # n Node: /globals/topology/defaultStacks:84 does not have global settings.
    # n Node: /globals/topology/defaultStacks:85 does not have global settings.
    # n Node: /globals/topology/defaultStacks:86 does not have global settings.
    # n Node: /globals/topology/defaultStacks:87 does not have global settings.
    # n Node: /globals/topology/defaultStacks:88 does not have global settings.
    # n Node: /globals/topology/defaultStacks:89 does not have global settings.
    # n Node: /globals/topology/defaultStacks:90 does not have global settings.
    # n Node: /globals/topology/defaultStacks:91 does not have global settings.
    # n Node: /globals/topology/defaultStacks:92 does not have global settings.
    # n Node: /globals/topology/defaultStacks:93 does not have global settings.
    # n Node: /globals/topology/defaultStacks:94 does not have global settings.
    # n Node: /globals/topology/defaultStacks:95 does not have global settings.
    # n Node: /globals/topology/defaultStacks:96 does not have global settings.
    # n Node: /globals/topology/defaultStacks:97 does not have global settings.
    # n Node: /globals/topology/defaultStacks:98 does not have global settings.
    # n Node: /globals/topology/defaultStacks:99 does not have global settings.
    # n Node: /globals/topology/defaultStacks:100 does not have global settings.
    # n Node: /globals/topology/defaultStacks:101 does not have global settings.
    # n Node: /globals/topology/defaultStacks:102 does not have global settings.
    # n Node: /globals/topology/defaultStacks:103 does not have global settings.
    # n Node: /globals/topology/defaultStacks:104 does not have global settings.
    # n Node: /globals/topology/defaultStacks:105 does not have global settings.
    # n Node: /globals/topology/defaultStacks:106 does not have global settings.
    # n Node: /globals/topology/defaultStacks:107 does not have global settings.
    # n Node: /globals/topology/defaultStacks:108 does not have global settings.
    # n Node: /globals/topology/defaultStacks:109 does not have global settings.
    # n Node: /globals/topology/defaultStacks:110 does not have global settings.
    # n Node: /globals/topology/defaultStacks:111 does not have global settings.
    # n Node: /globals/topology/defaultStacks:112 does not have global settings.
    # n Node: /globals/topology/defaultStacks:113 does not have global settings.
    # n Node: /globals/topology/defaultStacks:114 does not have global settings.
    # n Node: /globals/topology/defaultStacks:115 does not have global settings.
    # n Node: /globals/topology/defaultStacks:116 does not have global settings.
    # n Node: /globals/topology/defaultStacks:117 does not have global settings.
    # n Node: /globals/topology/defaultStacks:118 does not have global settings.
    # n Node: /globals/topology/defaultStacks:119 does not have global settings.
    # n Node: /globals/topology/defaultStacks:120 does not have global settings.

    _result_ = ixiangpf.emulation_bgp_config(
        mode                                       = "create",
        handle                                     = "/globals",
        start_rate_enable                          = "0",
        start_rate_interval                        = "1000",
        start_rate                                 = "200",
        start_rate_scale_mode                      = "port",
        stop_rate_enable                           = "0",
        stop_rate_interval                         = "1000",
        stop_rate                                  = "200",
        stop_rate_scale_mode                       = "port",
        disable_received_update_validation         = "0",
        enable_ad_vpls_prefix_length               = "0",
        ibgp_tester_as_four_bytes                  = "1",
        ibgp_tester_as_two_bytes                   = "1",
        initiate_ebgp_active_connection            = "1",
        initiate_ibgp_active_connection            = "1",
        session_retry_delay_time                   = "5",
        enable_bgp_fast_failover_on_link_down      = "0",
        mldp_p2mp_fec_type                         = "06",
        request_vpn_label_exchange_over_lsp        = "1",
        trigger_vpls_pw_initiation                 = "1",
        high_scale_route_mode                      = "0",
        srte_policy_safi                           = "73",
        srte_policy_attr_type                      = "23",
        srte_policy_type                           = "15",
        srte_remote_endpoint_type                  = "6",
        srte_color_type                            = "4",
        srte_preference_type                       = "12",
        srte_binding_type                          = "13",
        srte_segment_list_type                     = "128",
        srte_weight_type                           = "9",
        srte_mplsSID_type                          = "1",
        srte_ipv6SID_type                          = "2",
        srte_ipv4_node_address_type                = "3",
        srte_ipv6_node_address_type                = "4",
        srte_ipv4_node_address_index_type          = "5",
        srte_ipv4_local_remote_address             = "6",
        srte_ipv6_node_address_index_type          = "7",
        srte_ipv6_local_remote_address             = "8",
        srte_include_length                        = "1",
        srte_length_unit                           = "bits",
        prefix_sid_attr_type                       = "40",
        srv6_vpn_sid_tlv_type                      = "4",
        vpn_sid_type                               = "1",
        srv6_draft_num                             = "version_ietf_01",
        evpn_sid_type                              = "2",
        bgpv4_tos_diff_serv                        = "c0",
        bgpv6_traffic_class                        = "c0",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_bgp_config', _result_)

    # n The attribute: udpDestinationPort with the value:  is not supported by scriptgen.
    # n The attribute: vrfRouteImportExtendedCommunitySubType with the value:  is not supported by scriptgen.
    # n The attribute: LLGRCapabilityCode with the value:  is not supported by scriptgen.
    # n The attribute: policySegmentSubTLVTypeB with the value:  is not supported by scriptgen.
    # n The attribute: policySegmentSubTLVTypeI with the value:  is not supported by scriptgen.
    # n The attribute: policySegmentSubTLVTypeJ with the value:  is not supported by scriptgen.
    # n The attribute: policySegmentSubTLVTypeK with the value:  is not supported by scriptgen.
    # n The attribute: eNLPType with the value:  is not supported by scriptgen.
    # n The attribute: policyPriorityType with the value:  is not supported by scriptgen.
    # n The attribute: gSRv6SIDEncodingSubTlvType with the value:  is not supported by scriptgen.
    # n The attribute: policyNameType with the value:  is not supported by scriptgen.
    # n The attribute: policyPathNameType with the value:  is not supported by scriptgen.
    # n The attribute: reverseBindingType with the value:  is not supported by scriptgen.
    # n The attribute: sRv6BindingSIDType with the value:  is not supported by scriptgen.
    # n The attribute: protoclIdType with the value:  is not supported by scriptgen.
    # n The attribute: bgpRouterId with the value:  is not supported by scriptgen.
    # n The attribute: bgpConfMemType with the value:  is not supported by scriptgen.
    # n The attribute: peerNodeSidType with the value:  is not supported by scriptgen.
    # n The attribute: peerAdjSidType with the value:  is not supported by scriptgen.
    # n The attribute: peerSetSidType with the value:  is not supported by scriptgen.
    # n The attribute: BIERTunnelType with the value:  is not supported by scriptgen.
    # n The attribute: useUnicastDestMacForBierTraffic with the value:  is not supported by scriptgen.
    # n The attribute: ipv6FlowspecDraftVersion with the value:  is not supported by scriptgen.
    # n The attribute: RedirectIPv6Type with the value:  is not supported by scriptgen.
    # n The attribute: RedirectIPv6NHopType with the value:  is not supported by scriptgen.
    # n The attribute: RedirectIPv4NHopType with the value:  is not supported by scriptgen.
    # n The attribute: enableTraceroute with the value:  is not supported by scriptgen.
    # n The attribute: maxTtl with the value:  is not supported by scriptgen.
    # n The attribute: waitTime with the value:  is not supported by scriptgen.
    # n The attribute: queryCount with the value:  is not supported by scriptgen.
    # n The attribute: probeInterval with the value:  is not supported by scriptgen.
    # n The attribute: executionMode with the value:  is not supported by scriptgen.
    # n Node: tlvEditor is not supported for scriptgen.

    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        arp_on_linkup                       = "0",
        single_arp_per_gateway              = "1",
        ipv4_send_arp_rate                  = "200",
        ipv4_send_arp_interval              = "1000",
        ipv4_send_arp_max_outstanding       = "400",
        ipv4_send_arp_scale_mode            = "port",
        ipv4_attempt_enabled                = "0",
        ipv4_attempt_rate                   = "200",
        ipv4_attempt_interval               = "1000",
        ipv4_attempt_scale_mode             = "port",
        ipv4_diconnect_enabled              = "0",
        ipv4_disconnect_rate                = "200",
        ipv4_disconnect_interval            = "1000",
        ipv4_disconnect_scale_mode          = "port",
        ipv4_re_send_arp_on_link_up         = "true",
        ipv4_permanent_mac_for_gateway      = "false",
        ipv4_gratarp_transmit_count         = "1",
        ipv4_gratarp_transmit_interval      = "3000",
        ipv4_rarp_transmit_count            = "1",
        ipv4_rarp_transmit_interval         = "3000",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)

    # n The attribute: reSendGratArpOnLinkUp with the value:  is not supported by scriptgen.

    _result_ = ixiangpf.interface_config(
        protocol_handle                     = "/globals",
        ethernet_attempt_enabled            = "0",
        ethernet_attempt_rate               = "200",
        ethernet_attempt_interval           = "1000",
        ethernet_attempt_scale_mode         = "port",
        ethernet_diconnect_enabled          = "0",
        ethernet_disconnect_rate            = "200",
        ethernet_disconnect_interval        = "1000",
        ethernet_disconnect_scale_mode      = "port",
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('interface_config', _result_)


    # n Node: /globals/topology/ipv6Autoconfiguration does not have global settings.
    # n Node: /globals/topology/ipv6 does not have global settings.
    # n Node: /globals/topology/bfdRouter does not have global settings.
    # n Node: /globals/topology/ospfv2Router does not have global settings.
    # n Node: /globals/topology/ospfv3Router does not have global settings.
    # n Node: /globals/topology/pimRouter does not have global settings.
    # n Node: /globals/topology/rsvpteLsps does not have global settings.
    # n Node: /globals/topology/rsvpteIf does not have global settings.
    # n Node: /globals/topology/isisFabricPathRouter does not have global settings.
    # n Node: /globals/topology/isisL3Router does not have global settings.
    # n Node: /globals/topology/isisSpbRouter does not have global settings.
    # n Node: /globals/topology/isisTrillRouter does not have global settings.
    # n Node: /globals/topology/igmpHost does not have global settings.
    # n Node: /globals/topology/mldHost does not have global settings.
    # n Node: /globals/topology/ldpBasicRouterV6 does not have global settings.
    # n Node: /globals/topology/ldpBasicRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouter does not have global settings.
    # n Node: /globals/topology/ldpTargetedRouterV6 does not have global settings.
    # n Node: /globals/topology/msrpListener does not have global settings.
    # n Node: /globals/topology/msrpTalker does not have global settings.
    # n Node: /globals/topology/igmpQuerier does not have global settings.
    # n Node: /globals/topology/mldQuerier does not have global settings.
    # n Node: /globals/topology/dhcpv4client does not have global settings.
    # n Node: /globals/topology/dhcpv6client does not have global settings.
    # n Node: /globals/topology/dhcpv4server does not have global settings.
    # n Node: /globals/topology/dhcpv6server does not have global settings.
    # n Node: /globals/topology/dhcpv4relayAgent does not have global settings.
    # n Node: /globals/topology/lightweightDhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/dhcpv6relayAgent does not have global settings.
    # n Node: /globals/topology/pppoxclient does not have global settings.
    # n Node: /globals/topology/pppoxserver does not have global settings.
    # n Node: /globals/topology/lac does not have global settings.
    # n Node: /globals/topology/lns does not have global settings.
    # n Node: /globals/topology/vxlangpe does not have global settings.
    # n Node: /globals/topology/vxlanv6gpe does not have global settings.
    # n Node: /globals/topology/vxlanv6 does not have global settings.
    # n Node: /globals/topology/vxlan does not have global settings.
    # n Node: /globals/topology/geneve does not have global settings.
    # n Node: /globals/topology/greoipv4 does not have global settings.
    # n Node: /globals/topology/greoipv6 does not have global settings.
    # n Node: /globals/topology/ptp does not have global settings.
    # n Node: /globals/topology/ancp does not have global settings.
    # n Node: /globals/topology/lacp does not have global settings.
    # n Node: /globals/topology/lagportlacp does not have global settings.
    # n Node: /globals/topology/staticLag does not have global settings.
    # n Node: /globals/topology/lagportstaticlag does not have global settings.
    # n Node: /globals/topology/openFlowChannel does not have global settings.
    # n Node: /globals/topology/openFlowController does not have global settings.
    # n Node: /globals/topology/pcc does not have global settings.
    # n Node: /globals/topology/pce does not have global settings.
    # n Node: /globals/topology/ovsdbcontroller does not have global settings.
    # n Node: /globals/topology/ovsdbserver does not have global settings.
    # n Node: /globals/topology/cfmBridge does not have global settings.
    # n Node: /globals/topology/netconfClient does not have global settings.
    # n Node: /globals/topology/netconfServer does not have global settings.
    # n Node: /globals/topology/eCpriRe does not have global settings.
    # n Node: /globals/topology/eCpriRec does not have global settings.
    # n Node: /globals/topology/ecpriRec does not have global settings.
    # n Node: /globals/topology/ere does not have global settings.
    # n Node: /globals/topology/dotOneX does not have global settings.
    # n Node: /globals/topology/ntpclock does not have global settings.
    # n Node: /globals/topology/macsec does not have global settings.
    # n Node: /globals/topology/staticMacsec does not have global settings.
    # n Node: /globals/topology/mka does not have global settings.
    # n Node: /globals/topology/bondedGRE does not have global settings.
    # n Node: /globals/topology/esmc does not have global settings.
    # n Node: /globals/topology/cuspCP does not have global settings.
    # n Node: /globals/topology/cuspUP does not have global settings.
    # n Node: /globals/topology/upGroupInfo does not have global settings.
    # n Node: /globals/topology/gRIBIClient does not have global settings.
    # n Node: /globals/topology/gRPCClient does not have global settings.
    # n Node: /globals/topology/twampIpv4 does not have global settings.
    # n Node: /globals/topology/twampIpv6 does not have global settings.
    # n Node: /globals/topology/ptprobeinstancesrv6 does not have global settings.
    # n Node: /globals/topology/roce6v2 does not have global settings.
    # n Node: /globals/topology/rocev2 does not have global settings.
    # n Node: /globals/topology/protocolWizards does not have global settings.
    # n Node: /globals/topology/defaultStacks:1 does not have global settings.
    # n Node: /globals/topology/defaultStacks:2 does not have global settings.
    # n Node: /globals/topology/defaultStacks:3 does not have global settings.
    # n Node: /globals/topology/defaultStacks:4 does not have global settings.
    # n Node: /globals/topology/defaultStacks:5 does not have global settings.
    # n Node: /globals/topology/defaultStacks:6 does not have global settings.
    # n Node: /globals/topology/defaultStacks:7 does not have global settings.
    # n Node: /globals/topology/defaultStacks:8 does not have global settings.
    # n Node: /globals/topology/defaultStacks:9 does not have global settings.
    # n Node: /globals/topology/defaultStacks:10 does not have global settings.
    # n Node: /globals/topology/defaultStacks:11 does not have global settings.
    # n Node: /globals/topology/defaultStacks:12 does not have global settings.
    # n Node: /globals/topology/defaultStacks:13 does not have global settings.
    # n Node: /globals/topology/defaultStacks:14 does not have global settings.
    # n Node: /globals/topology/defaultStacks:15 does not have global settings.
    # n Node: /globals/topology/defaultStacks:16 does not have global settings.
    # n Node: /globals/topology/defaultStacks:17 does not have global settings.
    # n Node: /globals/topology/defaultStacks:18 does not have global settings.
    # n Node: /globals/topology/defaultStacks:19 does not have global settings.
    # n Node: /globals/topology/defaultStacks:20 does not have global settings.
    # n Node: /globals/topology/defaultStacks:21 does not have global settings.
    # n Node: /globals/topology/defaultStacks:22 does not have global settings.
    # n Node: /globals/topology/defaultStacks:23 does not have global settings.
    # n Node: /globals/topology/defaultStacks:24 does not have global settings.
    # n Node: /globals/topology/defaultStacks:25 does not have global settings.
    # n Node: /globals/topology/defaultStacks:26 does not have global settings.
    # n Node: /globals/topology/defaultStacks:27 does not have global settings.
    # n Node: /globals/topology/defaultStacks:28 does not have global settings.
    # n Node: /globals/topology/defaultStacks:29 does not have global settings.
    # n Node: /globals/topology/defaultStacks:30 does not have global settings.
    # n Node: /globals/topology/defaultStacks:31 does not have global settings.
    # n Node: /globals/topology/defaultStacks:32 does not have global settings.
    # n Node: /globals/topology/defaultStacks:33 does not have global settings.
    # n Node: /globals/topology/defaultStacks:34 does not have global settings.
    # n Node: /globals/topology/defaultStacks:35 does not have global settings.
    # n Node: /globals/topology/defaultStacks:36 does not have global settings.
    # n Node: /globals/topology/defaultStacks:37 does not have global settings.
    # n Node: /globals/topology/defaultStacks:38 does not have global settings.
    # n Node: /globals/topology/defaultStacks:39 does not have global settings.
    # n Node: /globals/topology/defaultStacks:40 does not have global settings.
    # n Node: /globals/topology/defaultStacks:41 does not have global settings.
    # n Node: /globals/topology/defaultStacks:42 does not have global settings.
    # n Node: /globals/topology/defaultStacks:43 does not have global settings.
    # n Node: /globals/topology/defaultStacks:44 does not have global settings.
    # n Node: /globals/topology/defaultStacks:45 does not have global settings.
    # n Node: /globals/topology/defaultStacks:46 does not have global settings.
    # n Node: /globals/topology/defaultStacks:47 does not have global settings.
    # n Node: /globals/topology/defaultStacks:48 does not have global settings.
    # n Node: /globals/topology/defaultStacks:49 does not have global settings.
    # n Node: /globals/topology/defaultStacks:50 does not have global settings.
    # n Node: /globals/topology/defaultStacks:51 does not have global settings.
    # n Node: /globals/topology/defaultStacks:52 does not have global settings.
    # n Node: /globals/topology/defaultStacks:53 does not have global settings.
    # n Node: /globals/topology/defaultStacks:54 does not have global settings.
    # n Node: /globals/topology/defaultStacks:55 does not have global settings.
    # n Node: /globals/topology/defaultStacks:56 does not have global settings.
    # n Node: /globals/topology/defaultStacks:57 does not have global settings.
    # n Node: /globals/topology/defaultStacks:58 does not have global settings.
    # n Node: /globals/topology/defaultStacks:59 does not have global settings.
    # n Node: /globals/topology/defaultStacks:60 does not have global settings.
    # n Node: /globals/topology/defaultStacks:61 does not have global settings.
    # n Node: /globals/topology/defaultStacks:62 does not have global settings.
    # n Node: /globals/topology/defaultStacks:63 does not have global settings.
    # n Node: /globals/topology/defaultStacks:64 does not have global settings.
    # n Node: /globals/topology/defaultStacks:65 does not have global settings.
    # n Node: /globals/topology/defaultStacks:66 does not have global settings.
    # n Node: /globals/topology/defaultStacks:67 does not have global settings.
    # n Node: /globals/topology/defaultStacks:68 does not have global settings.
    # n Node: /globals/topology/defaultStacks:69 does not have global settings.
    # n Node: /globals/topology/defaultStacks:70 does not have global settings.
    # n Node: /globals/topology/defaultStacks:71 does not have global settings.
    # n Node: /globals/topology/defaultStacks:72 does not have global settings.
    # n Node: /globals/topology/defaultStacks:73 does not have global settings.
    # n Node: /globals/topology/defaultStacks:74 does not have global settings.
    # n Node: /globals/topology/defaultStacks:75 does not have global settings.
    # n Node: /globals/topology/defaultStacks:76 does not have global settings.
    # n Node: /globals/topology/defaultStacks:77 does not have global settings.
    # n Node: /globals/topology/defaultStacks:78 does not have global settings.
    # n Node: /globals/topology/defaultStacks:79 does not have global settings.
    # n Node: /globals/topology/defaultStacks:80 does not have global settings.
    # n Node: /globals/topology/defaultStacks:81 does not have global settings.
    # n Node: /globals/topology/defaultStacks:82 does not have global settings.
    # n Node: /globals/topology/defaultStacks:83 does not have global settings.
    # n Node: /globals/topology/defaultStacks:84 does not have global settings.
    # n Node: /globals/topology/defaultStacks:85 does not have global settings.
    # n Node: /globals/topology/defaultStacks:86 does not have global settings.
    # n Node: /globals/topology/defaultStacks:87 does not have global settings.
    # n Node: /globals/topology/defaultStacks:88 does not have global settings.
    # n Node: /globals/topology/defaultStacks:89 does not have global settings.
    # n Node: /globals/topology/defaultStacks:90 does not have global settings.
    # n Node: /globals/topology/defaultStacks:91 does not have global settings.
    # n Node: /globals/topology/defaultStacks:92 does not have global settings.
    # n Node: /globals/topology/defaultStacks:93 does not have global settings.
    # n Node: /globals/topology/defaultStacks:94 does not have global settings.
    # n Node: /globals/topology/defaultStacks:95 does not have global settings.
    # n Node: /globals/topology/defaultStacks:96 does not have global settings.
    # n Node: /globals/topology/defaultStacks:97 does not have global settings.
    # n Node: /globals/topology/defaultStacks:98 does not have global settings.
    # n Node: /globals/topology/defaultStacks:99 does not have global settings.
    # n Node: /globals/topology/defaultStacks:100 does not have global settings.
    # n Node: /globals/topology/defaultStacks:101 does not have global settings.
    # n Node: /globals/topology/defaultStacks:102 does not have global settings.
    # n Node: /globals/topology/defaultStacks:103 does not have global settings.
    # n Node: /globals/topology/defaultStacks:104 does not have global settings.
    # n Node: /globals/topology/defaultStacks:105 does not have global settings.
    # n Node: /globals/topology/defaultStacks:106 does not have global settings.
    # n Node: /globals/topology/defaultStacks:107 does not have global settings.
    # n Node: /globals/topology/defaultStacks:108 does not have global settings.
    # n Node: /globals/topology/defaultStacks:109 does not have global settings.
    # n Node: /globals/topology/defaultStacks:110 does not have global settings.
    # n Node: /globals/topology/defaultStacks:111 does not have global settings.
    # n Node: /globals/topology/defaultStacks:112 does not have global settings.
    # n Node: /globals/topology/defaultStacks:113 does not have global settings.
    # n Node: /globals/topology/defaultStacks:114 does not have global settings.
    # n Node: /globals/topology/defaultStacks:115 does not have global settings.
    # n Node: /globals/topology/defaultStacks:116 does not have global settings.
    # n Node: /globals/topology/defaultStacks:117 does not have global settings.
    # n Node: /globals/topology/defaultStacks:118 does not have global settings.
    # n Node: /globals/topology/defaultStacks:119 does not have global settings.
    # n Node: /globals/topology/defaultStacks:120 does not have global settings.


def ixnHLT_Scriptgen_RunTest(ixiahlt, ixnHLT):
    ixiatcl = ixiahlt.ixiatcl
    # #######################
    # start phase of the test
    # #######################
    ixnHLT_logger('Waiting 60 seconds before starting protocol(s) ...')
    time.sleep(60)

    ixnHLT_logger('Starting all protocol(s) ...')

    _result_ = ixiahlt.test_control(action='start_all_protocols')
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('ixiahlt::traffic_control', _result_)




    time.sleep(30)
    _result_ = ixiangpf.emulation_bgp_info(
        mode        = "stats",
        handle      = ixnHLT['HANDLE,//topology:<1>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>/bgpIpv4Peer:<1>'],
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_bgp_info', _result_)

    # n The attribute: noOfEpePeers with the value: 0 is not supported by scriptgen.
    # n The attribute: enableEpeTraffic with the value: False is not supported by scriptgen.
    # n The attribute: enableLlgr with the value:  is not supported by scriptgen.
    # n The attribute: advertiseEvpnRoutesForOtherVtep with the value: False is not supported by scriptgen.
    # n The attribute: allowIxiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: ixiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: filterLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: capabilityLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: enableBgpLsVpnTx with the value:  is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: name with the value: BGP Peer 1 is not supported by scriptgen.
    # n Node: tlvProfile is not supported for scriptgen.

    ixnHLT_logger('-----------------------------------')
    ixnHLT_logger('ixiangpf.emulation_bgp_info')
    for (k, v) in _result_.items():
        ixnHLT_logger('{0:40s} = {1}'.format(k, v))
    ixnHLT_logger('')

    _result_ = ixiangpf.emulation_bgp_info(
        mode        = "stats",
        handle      = ixnHLT['HANDLE,//topology:<2>/deviceGroup:<1>/ethernet:<1>/ipv4:<1>/bgpIpv4Peer:<1>'],
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('emulation_bgp_info', _result_)

    # n The attribute: noOfEpePeers with the value: 0 is not supported by scriptgen.
    # n The attribute: enableEpeTraffic with the value: False is not supported by scriptgen.
    # n The attribute: enableLlgr with the value:  is not supported by scriptgen.
    # n The attribute: advertiseEvpnRoutesForOtherVtep with the value: False is not supported by scriptgen.
    # n The attribute: allowIxiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: ixiaSignatureSuffix with the value:  is not supported by scriptgen.
    # n The attribute: filterLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: capabilityLinkStateVpn with the value:  is not supported by scriptgen.
    # n The attribute: enableBgpLsVpnTx with the value:  is not supported by scriptgen.
    # n The attribute: stackedLayers with the value: {} is not supported by scriptgen.
    # n The attribute: name with the value: BGP Peer 2 is not supported by scriptgen.
    # n Node: tlvProfile is not supported for scriptgen.

    ixnHLT_logger('-----------------------------------')
    ixnHLT_logger('ixiangpf.emulation_bgp_info')
    for (k, v) in _result_.items():
        ixnHLT_logger('{0:40s} = {1}'.format(k, v))
    ixnHLT_logger('')




    # ################################
    # protocol stats phase of the test
    # ################################

    #  stats for:
    #  packet_config_buffers handles
    ixnHLT_logger('getting stats for packet_config_buffers configuration elements')
    # ######################
    # stop phase of the test
    # ######################
    # ###############################
    # traffic stats phase of the test
    # ###############################
    ixnHLT_logger('Stopping all protocol(s) ...')

    _result_ = ixiahlt.test_control(action='stop_all_protocols')
    # Check status
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('ixiahlt::traffic_control', _result_)

# ----------------------------------------------------------------
# This dict keeps all generated handles and other info
ixnHLT = {}

# ----------------------------------------------------------------
#  chassis, card, port configuration
#
#  port_list needs to match up with path_list below
#
chassis = ['10.36.88.110']
#tcl_server = '10.36.88.110'
ixnetwork_tcl_server='10.36.94.225'
port_list = [['1/3', '1/4']]
vport_name_list = [['10GE LAN - 001', '10GE LAN - 002']]
aggregation_mode = [['normal', 'normal']]
aggregation_resource_mode = [['normal', 'normal']]
guard_rail = 'statistics'
#
#  this should match up w/ your port_list above
#
ixnHLT['path_list'] = [['//vport:<1>', '//vport:<2>']]
#
#
_result_ = ixiangpf.connect(
    reset=1,
    device=chassis,
    aggregation_mode=aggregation_mode,
    aggregation_resource_mode=aggregation_resource_mode,
    port_list=port_list,
    ixnetwork_tcl_server=ixnetwork_tcl_server,
    #tcl_server=tcl_server,
    guard_rail=guard_rail,
    return_detailed_handles=0,
    user_name='seunyang',      # Linux
    user_password='seunyang'   # Linux
)
# Check status
if _result_['status'] != IxiaHlt.SUCCESS:
	ixnHLT_errorHandler('connect', _result_)
porthandles = []
for (ch, ch_ports, ch_vport_paths) in zip(chassis, port_list, ixnHLT['path_list']):
    ch_porthandles = []
    for (port, path) in zip(ch_ports, ch_vport_paths):
        try:
            ch_key = _result_['port_handle']
            for ch_p in ch.split('.'):
                ch_key = ch_key[ch_p]
            if '.' not in str(port):
                porthandle = ch_key[port]
            else:
                s_port = str(port).split('.')
                porthandle = ch_key[s_port[0]][s_port[1]]
        except:
            errdict = {'log': 'could not connect to chassis=%s,port=<%s>' % (ch, port)}
            ixnHLT_errorHandler('connect', errdict)

        ixnHLT['PORT-HANDLE,%s' % path] = porthandle
        ch_porthandles.append(porthandle)
    porthandles.append(ch_porthandles)

for (ch_porthandles, ch_vport_names) in zip(porthandles, vport_name_list):
    _result_ = ixiahlt.vport_info(
        mode='set_info',
        port_list=[ch_porthandles],
        port_name_list=[ch_vport_names]
    )
    if _result_['status'] != IxiaHlt.SUCCESS:
        ixnHLT_errorHandler('vport_info', _result_)


# ----------------------------------------------------------------

#call the procedure that configures legacy implementation
ixnHLT_Scriptgen_Configure(ixiahlt, ixnHLT)

#call the procedure that configures CPF
#this should be called after the call to legacy implementation
ixnCPF_Scriptgen_Configure(ixiangpf, ixnHLT)

ixnHLT_Scriptgen_RunTest(ixiahlt, ixnHLT)
