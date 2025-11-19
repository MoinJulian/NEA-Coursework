create table if not exists questions (
    id uuid primary key default gen_random_uuid(),
    lesson_id uuid references lessons(id) on delete cascade not null,
    question_text text not null,
    question_order integer not null,
    created_at timestamp with time zone default now()
);

-- Create index for lesson lookups
create index if not exists idx_questions_lesson_id on questions(lesson_id);