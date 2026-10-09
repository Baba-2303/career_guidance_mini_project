-- Run once in Supabase → SQL Editor. Creates the table the app saves responses into.
create table if not exists responses (
  id text primary key,  -- short random id set by the app; used to delete rows
  created_at timestamptz not null default now(),
  name text not null,
  grade smallint not null,
  school text,
  lang text,
  q1 smallint, q2 smallint, q3 smallint, q4 smallint, q5 smallint,
  q6 smallint, q7 smallint, q8 smallint, q9 smallint, q10 smallint,  -- option index; -1 = typed own answer
  typed_answers text,  -- JSON, e.g. {"q3": "I want to be a pilot"}
  top1 text not null,
  top2 text not null,
  route text not null,
  source text not null
);

-- RLS on with no policies: browsers/public keys get nothing; only the server-side secret key can read/write.
alter table responses enable row level security;
