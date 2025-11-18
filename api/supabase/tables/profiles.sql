create table if not exists profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    username text unique not null,
    handicap integer not null,
    xp integer not null default 0,
    streak integer not null default 0,
    hearts integer not null default 5,
    last_lesson_date date,
    streak_freezes_used integer not null default 0,
    created_at timestamp with time zone default now(),
    updated_at timestamp with time zone default now()
);

-- Create index for username lookups
create index if not exists idx_profiles_username on profiles(username);

-- Create index for leaderboard queries
create index if not exists idx_profiles_xp on profiles(xp desc);
