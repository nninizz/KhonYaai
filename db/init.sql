CREATE TABLE IF NOT EXISTS bookings (
    booking_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(64) NOT NULL,
    driver_id VARCHAR(64),
    appointment_time TIMESTAMP,
    current_status VARCHAR(32) NOT NULL,
    deposit_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    cancellation_policy VARCHAR(32) NOT NULL DEFAULT 'standard',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cancellation_requests (
    request_id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL,
    customer_id VARCHAR(64) NOT NULL,
    reason TEXT,
    requested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    action_by VARCHAR(32) NOT NULL DEFAULT 'customer',
    result_status VARCHAR(32) NOT NULL DEFAULT 'pending',
    refund_rate NUMERIC(5,2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS driver_status (
    driver_id VARCHAR(64) PRIMARY KEY,
    trip_status VARCHAR(32) NOT NULL DEFAULT 'idle',
    departed_at TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payment_transactions (
    transaction_id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL,
    refund_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
    reference_no VARCHAR(128),
    status VARCHAR(32) NOT NULL DEFAULT 'pending',
    processed_at TIMESTAMP
);
