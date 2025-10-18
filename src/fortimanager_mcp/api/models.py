"""Pydantic models for FortiManager API entities."""

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field


class APIResponse(BaseModel):
    """Standard API response wrapper."""

    id: int = Field(description="Request ID")
    result: list[dict[str, Any]] = Field(description="Response results")
    session: str | int | None = Field(default=None, description="Session ID (can be string or int)")

    @property
    def is_success(self) -> bool:
        """Check if response indicates success."""
        if not self.result:
            return False
        return self.result[0].get("status", {}).get("code") == 0

    @property
    def error_code(self) -> int | None:
        """Get error code from response."""
        if not self.result:
            return None
        return self.result[0].get("status", {}).get("code")

    @property
    def error_message(self) -> str | None:
        """Get error message from response."""
        if not self.result:
            return None
        return self.result[0].get("status", {}).get("message")

    @property
    def data(self) -> Any:
        """Get data from response."""
        if not self.result:
            return None
        return self.result[0].get("data")


class Device(BaseModel):
    """FortiGate device managed by FortiManager."""

    name: str = Field(description="Device name")
    os_type: str | None = Field(default=None, description="Operating system type")
    os_ver: str | None = Field(default=None, description="Operating system version")
    mr: int | None = Field(default=None, description="Maintenance release number")
    build: int | None = Field(default=None, description="Build number")
    platform_str: str | None = Field(default=None, description="Platform description")
    sn: str | None = Field(default=None, description="Serial number")
    ip: str | None = Field(default=None, description="Management IP address")
    conn_status: int | str | None = Field(default=None, description="Connection status (1='up', 0='down')")
    ha_mode: int | str | None = Field(default=None, description="HA mode (e.g., 'standalone', 'active-passive')")
    vdom: list[dict] | None = Field(default=None, description="VDOMs on device")
    oid: int | None = Field(default=None, description="Object ID")

    @property
    def is_connected(self) -> bool:
        """Check if device is connected."""
        return self.conn_status == 1 or self.conn_status == "up"


class ADOM(BaseModel):
    """Administrative Domain (ADOM)."""

    name: str = Field(description="ADOM name")
    desc: str | None = Field(default=None, description="Description")
    mr: int | None = Field(default=None, description="Maintenance release")
    os_ver: str | None = Field(default=None, description="FortiOS version")
    restricted_prds: str | None = Field(default=None, description="Restricted products")
    state: int | None = Field(default=None, description="ADOM state")
    oid: int | None = Field(default=None, description="Object ID")
    create_time: int | None = Field(default=None, description="Creation timestamp")
    workspace_mode: int | None = Field(default=None, description="Workspace mode")


class FirewallAddress(BaseModel):
    """Firewall address object."""

    name: str = Field(description="Address name")
    type: str | int = Field(default=0, description="Address type (0=ipmask, 1=iprange, etc.)")
    subnet: list[str] | str | None = Field(
        default=None, description="IP subnet [ip, netmask] or CIDR"
    )
    start_ip: str | None = Field(default=None, description="Start IP (for iprange)")
    end_ip: str | None = Field(default=None, description="End IP (for iprange)")
    fqdn: str | None = Field(default=None, description="FQDN (for fqdn type)")
    country: str | None = Field(default=None, description="Country code (for geography)")
    comment: str | None = Field(default=None, description="Comment")
    visibility: str | None = Field(default=None, description="Visibility")
    color: int | None = Field(default=0, description="Color index")
    uuid: str | None = Field(default=None, description="Unique identifier")
    oid: int | None = Field(default=None, description="Object ID")


class FirewallAddressGroup(BaseModel):
    """Firewall address group object."""

    name: str = Field(description="Address group name")
    member: list[str] | list[dict] = Field(
        default_factory=list, description="Group members"
    )
    comment: str | None = Field(default=None, description="Comment")
    visibility: str | None = Field(default=None, description="Visibility")
    color: int | None = Field(default=0, description="Color index")
    uuid: str | None = Field(default=None, description="Unique identifier")
    oid: int | None = Field(default=None, description="Object ID")


class FirewallService(BaseModel):
    """Firewall service object."""

    name: str = Field(description="Service name")
    protocol: str | int | None = Field(default=None, description="Protocol (TCP/UDP/ICMP)")
    tcp_portrange: str | None = Field(default=None, description="TCP port range")
    udp_portrange: str | None = Field(default=None, description="UDP port range")
    icmptype: int | None = Field(default=None, description="ICMP type")
    comment: str | None = Field(default=None, description="Comment")
    visibility: str | None = Field(default=None, description="Visibility")
    color: int | None = Field(default=0, description="Color index")
    uuid: str | None = Field(default=None, description="Unique identifier")
    oid: int | None = Field(default=None, description="Object ID")


class FirewallPolicy(BaseModel):
    """Firewall policy rule."""

    policyid: int | None = Field(default=None, description="Policy ID")
    name: str | None = Field(default=None, description="Policy name")
    srcintf: list[str] | list[dict] = Field(
        default_factory=list, description="Source interfaces"
    )
    dstintf: list[str] | list[dict] = Field(
        default_factory=list, description="Destination interfaces"
    )
    srcaddr: list[str] | list[dict] = Field(
        default_factory=list, description="Source addresses"
    )
    dstaddr: list[str] | list[dict] = Field(
        default_factory=list, description="Destination addresses"
    )
    service: list[str] | list[dict] = Field(default_factory=list, description="Services")
    action: str | int = Field(default=1, description="Action (0=deny, 1=accept)")
    status: str | int = Field(default=1, description="Status (0=disable, 1=enable)")
    schedule: str | list[str] | None = Field(default="always", description="Schedule (can be string or list)")
    comments: str | None = Field(default=None, description="Comments")
    logtraffic: str | int | None = Field(default=None, description="Log traffic setting")
    nat: str | int | None = Field(default=None, description="NAT setting")
    uuid: str | None = Field(default=None, description="Unique identifier")
    oid: int | None = Field(default=None, description="Object ID")


class PolicyPackage(BaseModel):
    """Policy package."""

    name: str = Field(description="Package name")
    type: str | None = Field(default="pkg", description="Package type")
    scope_member: list[dict] | None = Field(
        default=None, description="Devices assigned to package"
    )
    package_settings: dict | None = Field(default=None, description="Package settings")
    oid: int | None = Field(default=None, description="Object ID")


class TaskStatus(BaseModel):
    """Task execution status."""

    id: int = Field(description="Task ID")
    title: str = Field(description="Task title")
    state: str = Field(description="Task state (running/done/error/cancelled)")
    percent: int = Field(default=0, description="Overall progress percentage")
    num_lines: int = Field(default=0, description="Number of sub-tasks")
    num_done: int = Field(default=0, description="Number of completed sub-tasks")
    num_err: int = Field(default=0, description="Number of failed sub-tasks")
    num_warn: int = Field(default=0, description="Number of warnings")
    tot_percent: int = Field(default=0, description="Total progress (num_lines * 100)")
    start_tm: int | None = Field(default=None, description="Start timestamp")
    end_tm: int | None = Field(default=None, description="End timestamp")
    history: list[dict] | None = Field(default=None, description="Task history")
    line: list[dict] | None = Field(default=None, description="Sub-task details")

    @property
    def is_running(self) -> bool:
        """Check if task is still running."""
        return self.state == "running"

    @property
    def is_complete(self) -> bool:
        """Check if task is complete (done, error, or cancelled)."""
        return self.state in ("done", "error", "cancelled")

    @property
    def is_successful(self) -> bool:
        """Check if task completed successfully."""
        return self.state == "done" and self.num_err == 0

    @property
    def has_errors(self) -> bool:
        """Check if task has errors."""
        return self.num_err > 0

    @property
    def duration(self) -> int | None:
        """Get task duration in seconds."""
        if self.start_tm and self.end_tm:
            return self.end_tm - self.start_tm
        return None


class SystemStatus(BaseModel):
    """FortiManager system status."""

    version: str | None = Field(default=None, description="FortiManager version")
    hostname: str | None = Field(default=None, description="Hostname")
    serial: str | None = Field(default=None, description="Serial number")
    admin_domain: str | None = Field(default=None, description="Admin domain")
    ha_mode: str | None = Field(default=None, description="HA mode")
    license_status: str | None = Field(default=None, description="License status")


class InstallRequest(BaseModel):
    """Request for device or package installation."""

    adom: str = Field(description="ADOM name")
    scope: list[dict] = Field(description="Installation scope (devices/vdoms)")
    flags: list[str] = Field(default_factory=lambda: ["none"], description="Install flags")
    pkg: str | None = Field(default=None, description="Package name (for package install)")
    dev_rev_comments: str | None = Field(default=None, description="Device revision comments")


class JSONRPCRequest(BaseModel):
    """JSON-RPC request payload."""

    id: int = Field(description="Request ID")
    method: Literal["get", "add", "set", "update", "delete", "exec", "clone", "move"] = Field(
        description="RPC method"
    )
    params: list[dict[str, Any]] = Field(description="Request parameters")
    session: str | None = Field(default=None, description="Session ID")
    verbose: int = Field(default=1, description="Verbose mode (1=symbolic values)")

