# AVTOY KOREA — YDB schema contract test report (2026-11-15)

## Change under test
GitLab project `sokfrut/avtoY-korea-auto`, branch `deploy/russian-tuqo-static-2026-11-15`.

Added test:
`standby/test/ydb-schema-contract.test.mjs`

The test asserts exact ordered DDL lines for:
- `standby_enquiries` columns, types, NOT NULL declarations, both GLOBAL queue indexes, index keys/COVER lists, and primary key;
- `standby_idempotency`;
- `standby_schema_migrations`;
- `standby_max_webhook_events`;
- `standby_operator_auth_rate_limits`;
- `standby_operator_audit_events`.

It also checks that migration v3 retains read probes for runtime tables and both explicit queue-index probes.

## Execution evidence
- Environment: Node.js v22.16.0, isolated local temporary test harness.
- Command: `node --test /tmp/ydb-contract/test/ydb-schema-contract.test.mjs`
- Result: **4 passed, 0 failed**.
- The fixture files were populated from the exact GitLab migration DDL and newly committed test source retrieved for this review.
- This is a focused contract-test execution, not the complete repository test suite and not GitLab CI.

## Important limitations
- No actual YDB engine was contacted.
- No YQL parser, Managed YDB endpoint, IAM, effective ACL, transaction concurrency, index execution or backup/restore behavior was tested.
- The test compares checked-in DDL against a separately stated expected contract; it cannot detect a mismatch between the deployed database and checked-in migrations.
- No production resource or data was changed.

## Next
1. Review every SQL statement in `storage/ydb-request-store.mjs` against table DDL and YDB semantics.
2. Add/execute real read-only `SHOW CREATE TABLE` inspection when a Russian YDB database exists.
3. Verify runtime identity effective permissions and inherited ACLs.
4. Run real serializable concurrency and retry/idempotency tests before production.
