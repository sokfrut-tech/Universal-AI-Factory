#!/usr/bin/env ruby
# Parse the workflow as YAML and assert effective structure, not substrings.
require "yaml"

path = ".github/workflows/factory-runner.yml"
doc = YAML.safe_load_file(path, permitted_classes: [], permitted_symbols: [], aliases: false)
abort "workflow root must be a mapping" unless doc.is_a?(Hash)

# Psych uses YAML 1.1 and reads the GitHub Actions key "on" as boolean true.
triggers = doc[true] || doc["on"]
abort "workflow_dispatch trigger missing" unless triggers.is_a?(Hash) && triggers.key?("workflow_dispatch")
permissions = doc.fetch("permissions")
abort "workflow must have contents: read only" unless permissions == {"contents" => "read"}

jobs = doc.fetch("jobs")
job = jobs.fetch("read-only-audit")
abort "unexpected job permissions" if job.key?("permissions") && job["permissions"] != {"contents" => "read"}
steps = job.fetch("steps")
abort "steps must be a sequence" unless steps.is_a?(Array)

factory_checkout = steps.find { |step| step["name"] == "Checkout factory" }
target_checkout = steps.find { |step| step["name"] == "Checkout allowlisted target (read-only)" }
abort "factory checkout missing" unless factory_checkout
abort "target checkout missing" unless target_checkout
abort "target checkout must use checkout action" unless target_checkout["uses"] == "actions/checkout@v4"

target_with = target_checkout.fetch("with")
abort "target checkout must fetch full history" unless target_with["fetch-depth"].to_s == "0"
abort "target checkout must not persist credentials" unless target_with["persist-credentials"] == false
abort "target checkout must use scoped read token" unless target_with["token"] == "${{ secrets.FACTORY_TARGETS_READ_TOKEN }}"
abort "target checkout repository must come from validated output" unless target_with["repository"] == "sokfrut-tech/${{ steps.validate.outputs.target_repo }}"

validate = steps.find { |step| step["id"] == "validate" }
abort "input validation step missing" unless validate
validate_env = validate.fetch("env")
abort "target-read token must be injected through environment" unless validate_env["TARGETS_READ_TOKEN"] == "${{ secrets.FACTORY_TARGETS_READ_TOKEN }}"

report = steps.find { |step| step["name"] == "Produce factual audit report" }
abort "factual report step missing" unless report
run_script = report.fetch("run")
abort "report must enumerate fetched remote refs" unless run_script.include?("for-each-ref") && run_script.include?("refs/remotes/origin")
abort "report must not claim task dispatch" unless run_script.include?("not dispatched")

upload = steps.find { |step| step["name"] == "Upload report artifact" }
abort "report artifact upload missing" unless upload && upload["uses"] == "actions/upload-artifact@v4"

puts "OK: YAML parsed; effective permissions, checkout scope, credentials, branch inventory and artifact structure validated."
