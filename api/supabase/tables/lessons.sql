create table if not exists lessons (
    id uuid primary key default gen_random_uuid(),
    title text not null,
    description text,
    order_number integer not null,
    created_at timestamp with time zone default now()
);