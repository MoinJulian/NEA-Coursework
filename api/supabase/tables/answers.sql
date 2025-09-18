create table if not exists answers (
    id uuid primary key default gen_random_uuid(),
    answer_text text not null,
    is_correct boolean not null,
    question_id uuid references questions(id) on delete cascade
)