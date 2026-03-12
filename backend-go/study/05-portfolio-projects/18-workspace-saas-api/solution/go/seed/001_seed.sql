INSERT INTO users (id, email, password_hash, display_name)
VALUES (
    'seed-admin',
    'seed-admin@example.com',
    '$2a$10$eImiTXuWVxfM37uY4JANjQ==',
    'Seed Admin'
)
ON CONFLICT (email) DO NOTHING;
