# Control: TOOL-01 (declare tool permissions), TOOL-02 (enforce at the gateway),
#          TOOL-03 (constrain tool parameters), DEL-01 (least delegation)
# Layer: AIRS Layer 01 - Guardrails (tool-call gateway, deny by default)
#
# Enforce the tool manifest at the gateway rather than trusting the agent. A tool
# call is permitted only when: the agent declares the tool, the action is within
# the agent's granted permissions, and every parameter is inside its declared
# bounds. Deny by default. For delegated calls, the effective permission set is
# the intersection of the caller and callee (no privilege escalation).
#
# Test with: opa eval -d tool_permission_boundary.rego -i input.json 'data.airs.tools.decision'
package airs.tools

import rego.v1

default allow := false

# input.manifest maps agent -> allowed tools and per-parameter bounds.
# input.call describes the requested tool invocation.
allow if {
	tool := input.manifest[input.call.agent][input.call.tool]
	tool != null
	params_within_bounds(tool, input.call.parameters)
	not delegation_violation
}

params_within_bounds(tool, params) if {
	# Every supplied parameter must be declared and within its bound.
	every name, value in params {
		bound := tool.parameters[name]
		bound != null
		within(bound, value)
	}
}

within(bound, value) if {
	bound.type == "enum"
	value in bound.allowed
}

within(bound, value) if {
	bound.type == "number"
	value >= bound.min
	value <= bound.max
}

within(bound, value) if {
	bound.type == "string"
	regex.match(bound.pattern, value)
}

# When a call is delegated, the effective permission is the INTERSECTION of the
# caller's grant and the callee's, so two things must hold. The delegating agent
# must hold the tool at all, and the parameters must sit inside the delegator's
# bounds as well as the callee's. Checking only the tool name lets a callee with
# a wider range act outside what its delegator was ever granted, which is the
# privilege escalation this rule exists to stop. No delegation means no
# violation.
delegation_violation if {
	input.call.delegated_from != null
	caller := input.manifest[input.call.delegated_from]
	not input.call.tool in object.keys(caller)
}

delegation_violation if {
	input.call.delegated_from != null
	caller_tool := input.manifest[input.call.delegated_from][input.call.tool]
	not params_within_bounds(caller_tool, input.call.parameters)
}

decision := {
	"allow": allow,
	"agent": input.call.agent,
	"tool": input.call.tool,
	"reason": reason,
}

reason := "tool call within declared manifest and parameter bounds" if allow

reason := "tool, action, or parameter outside declared manifest, or outside the delegator's grant (default deny)" if not allow
