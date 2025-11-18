create table if not exists options (
    id uuid primary key default gen_random_uuid(),
    question_id uuid references questions(id) on delete cascade not null,
    option_text text not null,
    is_correct boolean not null default false,
    option_order integer not null
);

-- Create index for question lookups
create index if not exists idx_options_question_id on options(question_id);
