create table if not exists completed_lessons (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete cascade not null,
    lesson_id uuid references lessons(id) on delete cascade not null,
    accuracy numeric(5,2) not null,
    xp_earned integer not null,
    time_taken integer not null, -- in seconds
    mistakes integer not null default 0,
    completed_at timestamp with time zone default now(),
    unique(user_id, lesson_id, completed_at)
);

create index if not exists idx_completed_lessons_user_id on completed_lessons(user_id);
create index if not exists idx_completed_lessons_completed_at on completed_lessons(completed_at);