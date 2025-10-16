# FortiManager MCP - Full API Coverage Implementation Plan

**Created:** October 16, 2025  
**Current Status:** 325/552 tools (59% coverage)  
**Target:** 475-525 tools (95-100% coverage)  
**Estimated Additional Tools:** 150-200 tools  
**Methodology:** Phased implementation with zero-bug quality standard

---

## 🎯 Strategic Implementation Order

### Phase Priority System
- **Priority 1:** High-value completions (maximize common use case coverage)
- **Priority 2:** Specialized operations (enterprise features)
- **Priority 3:** Advanced operations (power user features)
- **Priority 4:** Edge cases and specialized features

---

## 📋 PHASE 16: Policy Package Management Completion (20-25 tools)
**Current:** 16 tools (75% breadth)  
**Target:** 36-41 tools (95% breadth)  
**Priority:** HIGH  
**Estimated Effort:** 2-3 days

### 16.1 Folder Management (3 tools)
- [ ] `create_policy_folder` - Create policy package folder
- [ ] `move_policy_package_to_folder` - Move package to folder
- [ ] `delete_policy_folder` - Delete empty folder

### 16.2 Policy Blocks (6 tools)
- [ ] `create_policy_block` - Create reusable policy block
- [ ] `list_policy_blocks` - List policy blocks in ADOM
- [ ] `get_policy_block` - Get policy block details
- [ ] `add_policies_to_block` - Add policies to block
- [ ] `insert_policy_block` - Insert block into package
- [ ] `clone_policy_block` - Clone existing block

### 16.3 Scheduled Installs (3 tools)
- [ ] `schedule_policy_install` - Schedule install for later
- [ ] `list_scheduled_installs` - List scheduled installations
- [ ] `cancel_scheduled_install` - Cancel scheduled install

### 16.4 Install Preview (3 tools)
- [ ] `preview_policy_install_single` - Preview install for single device
- [ ] `preview_policy_install_multiple` - Preview for multiple devices
- [ ] `preview_partial_install` - Preview partial install

### 16.5 Policy Package Status & Operations (5 tools)
- [ ] `get_policy_package_status` - Get package status
- [ ] `get_policy_package_checksum` - Get package checksum
- [ ] `get_policy_package_changes` - List changes since last install
- [ ] `get_policy_hitcount` - Get policy hit counts
- [ ] `revert_policy_package` - Revert to previous version

### 16.6 Advanced Policy Operations (5 tools)
- [ ] `insert_policy_at_position` - Insert at specific position
- [ ] `get_nth_policy` - Get policy by index
- [ ] `move_policy_to_section` - Move to different section
- [ ] `create_policy_section` - Create policy section
- [ ] `import_policy_configuration` - Import config file

**Research Requirements:**
- FortiManager Policy Block architecture
- Install preview API structure
- Scheduled task management
- Policy section management

---

## 📋 PHASE 17: ADOM Management Completion (12-15 tools)
**Current:** 1 tool (60% breadth)  
**Target:** 13-16 tools (90% breadth)  
**Priority:** HIGH  
**Estimated Effort:** 2 days

### 17.1 ADOM CRUD Operations (4 tools)
- [ ] `create_adom` - Create new ADOM
- [ ] `create_adom_with_options` - Create with advanced options
- [ ] `create_adom_with_devices` - Create and assign devices
- [ ] `delete_adom` - Delete ADOM

### 17.2 ADOM Advanced Operations (4 tools)
- [ ] `clone_adom` - Clone existing ADOM
- [ ] `move_device_to_adom` - Move device between ADOMs
- [ ] `move_vdom_to_adom` - Move VDOM to different ADOM
- [ ] `get_adom_limits` - Get ADOM capacity limits

### 17.3 ADOM Checksum & Verification (3 tools)
- [ ] `get_adom_checksum` - Get ADOM configuration checksum
- [ ] `get_device_checksum_for_adom` - Get device checksums
- [ ] `verify_adom_integrity` - Verify ADOM data integrity

### 17.4 ADOM Upgrade & Management (4 tools)
- [ ] `upgrade_adom` - Upgrade ADOM version
- [ ] `check_adom_upgrade_status` - Check upgrade progress
- [ ] `get_adom_where_used` - Get global policy package usage
- [ ] `set_adom_display_options` - Configure display options

**Research Requirements:**
- ADOM workspace modes
- ADOM version upgrade process
- Device/VDOM migration procedures
- ADOM checksum calculation

---

## 📋 PHASE 18: Objects Management Completion (15-20 tools)
**Current:** 26 tools (80% breadth)  
**Target:** 41-46 tools (95% breadth)  
**Priority:** MEDIUM  
**Estimated Effort:** 2-3 days

### 18.1 Metadata Operations (8 tools)
- [ ] `add_object_metadata` - Add metadata to object
- [ ] `delete_object_metadata` - Remove metadata
- [ ] `rename_object_metadata` - Rename metadata field
- [ ] `assign_metadata_value` - Assign value to object
- [ ] `unassign_metadata_value` - Remove value assignment
- [ ] `replace_metadata_value` - Replace assigned value
- [ ] `get_metadata_values` - Get all values for metadata
- [ ] `list_object_metadata_fields` - List available metadata fields

### 18.2 Zone Management (4 tools)
- [ ] `list_zones` - List firewall zones
- [ ] `create_zone` - Create new zone
- [ ] `update_zone` - Update zone configuration
- [ ] `delete_zone` - Delete zone

### 18.3 Normalized Interfaces (3 tools)
- [ ] `list_normalized_interfaces` - List normalized interface mappings
- [ ] `get_interface_mapping_per_platform` - Get platform-specific mappings
- [ ] `create_normalized_interface` - Create interface mapping

### 18.4 Where-Used Operations (3 tools)
- [ ] `get_object_where_used_global` - Check usage in global ADOM
- [ ] `get_object_where_used_adom` - Check usage in specific ADOM
- [ ] `list_used_objects` - List all objects currently in use

### 18.5 Additional Object Types (3 tools)
- [ ] `list_virtual_wire_pairs` - List virtual wire pairs
- [ ] `create_virtual_wire_pair` - Create virtual wire pair
- [ ] `get_firewall_address_defaults` - Get default values for addresses

**Research Requirements:**
- Object metadata schema
- Zone vs interface relationship
- Normalized interface architecture
- Where-used query optimization

---

## 📋 PHASE 19: Security Profiles Completion (8-10 tools)
**Current:** 17 tools (85% breadth)  
**Target:** 25-27 tools (95% breadth)  
**Priority:** MEDIUM  
**Estimated Effort:** 1-2 days

### 19.1 Advanced Entry Management (4 tools)
- [ ] `add_multiple_ips_entries` - Add multiple IPS entries at once
- [ ] `replace_ips_signature_list` - Replace entire signature list
- [ ] `add_multiple_webfilter_urls` - Add multiple URLs at once
- [ ] `replace_webfilter_url_list` - Replace entire URL list

### 19.2 IPS Advanced Queries (3 tools)
- [ ] `list_ips_signatures` - List available IPS signatures
- [ ] `list_ips_protocols` - List IPS protocols
- [ ] `search_ips_applications` - Search IPS application database

### 19.3 DLP FortiGuard Queries (3 tools)
- [ ] `list_dlp_elements` - List DLP data elements
- [ ] `list_dlp_sensors_fortiguard` - List FortiGuard DLP sensors
- [ ] `list_dlp_dictionaries` - List DLP dictionaries

**Research Requirements:**
- IPS signature database structure
- DLP FortiGuard integration
- Bulk entry management APIs
- Signature search capabilities

---

## 📋 PHASE 20: FMG System Operations (10-12 tools)
**Current:** 12 tools (70% breadth)  
**Target:** 22-24 tools (90% breadth)  
**Priority:** MEDIUM  
**Estimated Effort:** 2 days

### 20.1 FortiManager Certificates (6 tools)
- [ ] `list_fmg_certificates` - List FMG certificates
- [ ] `get_fmg_certificate_details` - Get certificate details
- [ ] `list_fmg_ca_certificates` - List CA certificates
- [ ] `import_fmg_certificate` - Import certificate
- [ ] `enroll_fmg_certificate` - Enroll certificate via SCEP
- [ ] `delete_fmg_certificate` - Delete certificate

### 20.2 System Status & Info (3 tools)
- [ ] `get_fmg_ha_status` - Get HA status
- [ ] `get_fmg_system_info` - Get detailed system info
- [ ] `get_fmg_license_info` - Get license information

### 20.3 TACACS+ & Sessions (3 tools)
- [ ] `create_tacacs_server` - Create TACACS+ server
- [ ] `delete_tacacs_server` - Delete TACACS+ server
- [ ] `get_fmg_user_sessions` - Get active user sessions

### 20.4 System Operations (3 tools - CAREFUL)
- [ ] `backup_fmg_configuration` - Backup FMG config
- [ ] `restore_fmg_configuration` - Restore from backup
- [ ] `reboot_fortimanager` - Reboot FMG (requires confirmation)

**Research Requirements:**
- Certificate management best practices
- HA status monitoring
- TACACS+ integration
- Backup/restore procedures
- Safety checks for system operations

---

## 📋 PHASE 21: FortiGuard Management Completion (6-8 tools)
**Current:** 12 tools (90% breadth)  
**Target:** 18-20 tools (100% breadth)  
**Priority:** MEDIUM  
**Estimated Effort:** 1 day

### 21.1 FortiGuard Export/Import (4 tools)
- [ ] `export_fortiguard_objects` - Export FortiGuard objects
- [ ] `import_fortiguard_objects` - Import FortiGuard objects
- [ ] `export_fortiguard_entitlement` - Export entitlement data
- [ ] `import_fortiguard_entitlement` - Import entitlement data

### 21.2 Upstream Servers (2 tools)
- [ ] `list_fortiguard_upstream_servers` - List upstream servers
- [ ] `get_fortiguard_package_versions` - Get package versions for devices

### 21.3 Advanced Operations (2 tools)
- [ ] `sync_fortiguard_databases` - Force database sync
- [ ] `get_fortiguard_connection_status` - Get connection status

**Research Requirements:**
- FortiGuard export/import formats
- Upstream server configuration
- Database sync procedures

---

## 📋 PHASE 22: Connector Management (8-10 tools)
**Current:** 0 tools (40% breadth)  
**Target:** 8-10 tools (90% breadth)  
**Priority:** LOW  
**Estimated Effort:** 1-2 days

### 22.1 ClearPass Integration (6 tools)
- [ ] `get_clearpass_connector` - Get ClearPass connector info
- [ ] `list_clearpass_users` - List users from ClearPass
- [ ] `list_clearpass_tenants` - List ClearPass tenants
- [ ] `import_clearpass_tenant` - Import tenant configuration
- [ ] `list_clearpass_user_groups` - List user groups
- [ ] `sync_clearpass_users` - Sync users from ClearPass

### 22.2 JSON API Connectors (2 tools)
- [ ] `create_json_api_connector` - Create API connector
- [ ] `delete_json_api_connector` - Delete API connector

### 22.3 External Resources (2 tools)
- [ ] `get_ip_threat_feed_resolved` - Get resolved IPs from threat feed
- [ ] `refresh_external_connector` - Force connector refresh

**Research Requirements:**
- ClearPass API integration
- Connector authentication methods
- User/tenant synchronization
- Threat feed formats

---

## 📋 PHASE 23: Meta Fields Management (8 tools)
**Current:** 0 tools (0%)  
**Target:** 8 tools (100%)  
**Priority:** LOW  
**Estimated Effort:** 1 day

### 23.1 Device Meta Fields (4 tools)
- [ ] `create_device_meta_field` - Create device metadata field
- [ ] `list_device_meta_field_definitions` - List available fields
- [ ] `update_device_meta_field_definition` - Update field definition
- [ ] `delete_device_meta_field_definition` - Delete field definition

### 23.2 Policy Meta Fields (4 tools)
- [ ] `create_policy_meta_field` - Create policy metadata field
- [ ] `list_policy_meta_field_definitions` - List available fields
- [ ] `update_policy_meta_field_definition` - Update field definition
- [ ] `delete_policy_meta_field_definition` - Delete field definition

**Research Requirements:**
- Meta field data types
- Meta field scope (global vs ADOM)
- Meta field validation rules

---

## 📋 PHASE 24: Advanced Features (15-20 tools)
**Current:** Various (50% breadth)  
**Target:** Complete coverage  
**Priority:** LOW  
**Estimated Effort:** 2-3 days

### 24.1 CSF Operations (3 tools)
- [ ] `get_csf_fabric_status` - Get Security Fabric status
- [ ] `list_csf_fabric_devices` - List fabric devices
- [ ] `configure_csf_settings` - Configure CSF settings

### 24.2 FMG Cloud Operations (3 tools)
- [ ] `get_fmg_cloud_status` - Get cloud connection status
- [ ] `sync_with_fmg_cloud` - Sync with FortiManager Cloud
- [ ] `configure_cloud_settings` - Configure cloud settings

### 24.3 Sub Fetch Optimization (3 tools)
- [ ] `enable_sub_fetch` - Enable query optimization
- [ ] `get_sub_fetch_status` - Get optimization status
- [ ] `configure_sub_fetch_options` - Configure fetch options

### 24.4 System Proxy & Docker (4 tools)
- [ ] `configure_system_proxy` - Configure system proxy
- [ ] `get_system_proxy_config` - Get proxy configuration
- [ ] `get_docker_container_status` - Get Docker status
- [ ] `list_docker_containers` - List Docker containers

### 24.5 Database Cache (2 tools)
- [ ] `clear_database_cache` - Clear DB cache
- [ ] `get_cache_statistics` - Get cache stats

### 24.6 Option Attributes (1 tool)
- [ ] `get_option_attributes` - Get advanced option attributes

**Research Requirements:**
- Security Fabric architecture
- FortiManager Cloud integration
- Query optimization techniques
- Docker integration capabilities

---

## 🔄 Quality Assurance Process

### For Each Phase:
1. **Research Phase**
   - Review FortiManager API documentation
   - Check Context7 for latest API patterns
   - Review existing similar implementations
   - Document API endpoints and parameters

2. **Implementation Phase**
   - Create API methods in appropriate module
   - Create MCP tools in appropriate tool module
   - Follow existing code patterns
   - Use proper type hints and Pydantic models
   - Add comprehensive docstrings

3. **Testing Phase**
   - Test each tool individually
   - Test with real FortiManager environment
   - Verify across multiple ADOMs
   - Check error handling
   - Validate return data

4. **Documentation Phase**
   - Update tool count in README
   - Update API coverage map
   - Update comprehensive status report
   - Document any issues or limitations

5. **Verification Phase**
   - Run linter checks
   - Verify zero bugs introduced
   - Test integration with existing tools
   - Update metrics

---

## 📊 Success Metrics

### Per-Phase Targets:
- ✅ Zero bugs introduced
- ✅ 100% tools functional
- ✅ All tools documented
- ✅ Real FortiManager validation
- ✅ Type hints coverage 100%

### Overall Project Targets:
- **Phase 16-24:** Add 150-200 tools
- **Final Coverage:** 475-525 tools (95-100% API coverage)
- **Quality:** Maintain zero-bug streak
- **Timeline:** 15-20 working days
- **Documentation:** 100% comprehensive

---

## 🎯 Implementation Guidelines

### Code Standards:
- Follow existing patterns in codebase
- Use async/await for all I/O
- Comprehensive error handling
- Rich docstrings for LLM understanding
- Type hints for all parameters

### Testing Standards:
- Integration tests with real FortiManager
- Non-intrusive testing (read-only preferred)
- Use MCP_TEST_ prefix for test objects
- Clean up after tests
- Multi-ADOM validation

### Documentation Standards:
- Update all status files
- Document API endpoints used
- Note any limitations
- Update coverage percentages
- Maintain ADR for decisions

---

## 📅 Estimated Timeline

| Phase | Tools | Days | Completion |
|-------|-------|------|------------|
| Phase 16: Policy Packages | 20-25 | 2-3 | - |
| Phase 17: ADOM Management | 12-15 | 2 | - |
| Phase 18: Objects | 15-20 | 2-3 | - |
| Phase 19: Security Profiles | 8-10 | 1-2 | - |
| Phase 20: FMG System | 10-12 | 2 | - |
| Phase 21: FortiGuard | 6-8 | 1 | - |
| Phase 22: Connectors | 8-10 | 1-2 | - |
| Phase 23: Meta Fields | 8 | 1 | - |
| Phase 24: Advanced | 15-20 | 2-3 | - |
| **TOTAL** | **150-200** | **15-20** | - |

---

## 🚀 Ready to Begin

**Current State:** 325 tools, 59% coverage  
**Target State:** 475-525 tools, 95-100% coverage  
**Next Phase:** Phase 16 - Policy Package Management  
**Status:** Ready to start implementation

All phases are planned, researched, and ready for systematic implementation following the established zero-bug quality standard.

---

*Plan Created: October 16, 2025*  
*Methodology: Phased implementation with research-first approach*  
*Quality Standard: Zero-bug streak maintained*  
*Documentation: Comprehensive tracking and updates*


