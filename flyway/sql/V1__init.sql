CREATE TABLE account (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_number VARCHAR(255) NOT NULL
);

CREATE TABLE operation_type (
    id          INTEGER PRIMARY KEY,
    description VARCHAR(255) NOT NULL
);

INSERT INTO operation_type (id, description) VALUES
    (1, 'Normal Purchase'),
    (2, 'Purchase with installments'),
    (3, 'Withdrawal'),
    (4, 'Credit Voucher');

CREATE TABLE transaction (
    id                UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id        UUID        NOT NULL REFERENCES account(id),
    operation_type_id INTEGER     NOT NULL REFERENCES operation_type(id),
    amount            NUMERIC(18, 2) NOT NULL,
    event_date        TIMESTAMP   NOT NULL DEFAULT NOW()
);
