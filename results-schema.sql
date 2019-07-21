
CREATE TABLE run (
    run_id              TEXT   NOT NULL,
    timestamp           DATETIME DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (run_id)
);

CREATE TABLE endpoint_test (
    test_id             INTEGER   NOT NULL,
    run_id              TEXT      NOT NULL,
    name                TEXT      NOT NULL,
    status_code         INTEGER   NOT NULL,
    duration            INTEGER   NOT NULL,
    hash                TEXT      NOT NULL,
    size                INTEGER   NOT NULL,

    PRIMARY KEY (test_id),

    FOREIGN KEY (run_id) REFERENCES run (run_id) ON DELETE CASCADE
);

