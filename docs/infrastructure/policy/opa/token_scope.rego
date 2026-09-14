# Control: SEC-02 (short-lived, scoped tokens), IAM-06 (session-scoped credentials),
#          DEL-05 (propagate user identity through chains)
# Layer: AIRS Layer 01 - Guardrails (validate the token before the call proceeds)
#
# Validate that a delegation / session token is short-lived, scoped to the task,
# and carries the originating user identity down the agent execution tree.
# Reject tokens that are long-lived, over-scoped, or missing principal
# propagation. This is the runtime counterpart to the pre-runtime requirement
# that credentials are session-scoped and never wildcard.
#
# input.token is the decoded claim set; input.now is the current unix time.
# input.required_scopes lists the scopes this specific call needs.
#
# Test with: opa eval -d token_scope.rego -i input.json 'data.airs.token.decision'
package airs.token

import rego.v1

# Maximum acceptable token lifetime, in seconds (15 minutes).
max_lifetime := 900

default valid := false

valid if {
	count(violations) == 0
}

# Every check below tests a claim's *value*. In Rego a body that references an
# absent field is undefined rather than false, so without these presence rules a
# token that simply omits `exp`, `iat`, `scopes`, `sid`, or `sub` produces an
# empty violation set and is accepted. Absence is a violation, not a pass.
required_claims := {"sub", "exp", "iat", "scopes", "sid"}

violations contains sprintf("token missing required claim: %s", [claim]) if {
	some claim in required_claims
	not claim in object.keys(input.token)
}

violations contains "token missing the act (delegation actor) claim" if {
	not "act" in object.keys(input.token)
}

violations contains "token scopes claim is not a set of strings" if {
	"scopes" in object.keys(input.token)
	not is_array(input.token.scopes)
	not is_set(input.token.scopes)
}

violations contains "policy input is missing session_id to bind against" if {
	not "session_id" in object.keys(input)
}

violations contains "token expired" if {
	input.token.exp <= input.now
}

violations contains "token lifetime exceeds policy maximum" if {
	input.token.exp - input.token.iat > max_lifetime
}

violations contains "token grants wildcard scope" if {
	"*" in input.token.scopes
}

violations contains "token missing a required scope" if {
	some required in input.required_scopes
	not required in input.token.scopes
}

violations contains "token does not propagate an originating principal" if {
	"act" in object.keys(input.token)
	not input.token.act.sub # RFC 8693 actor / delegation claim
}

violations contains "token not bound to the current session" if {
	input.token.sid != input.session_id
}

# `subject` is looked up defensively. Reading input.token.sub directly makes the
# whole decision undefined for a token that omits it, so a malformed token would
# yield no decision at all rather than an explicit deny with its reasons.
subject := object.get(input, ["token", "sub"], "<absent>")

decision := {
	"valid": valid,
	"subject": subject,
	"violations": violations,
}
