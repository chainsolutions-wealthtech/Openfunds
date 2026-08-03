-- MINIMAL REFERENCE TABLES REQUIRED TO TEST THE 004 ENDPOINT MODEL FIRST.

create schema if not exists ref;
create schema if not exists source;

create table if not exists ref.organization (
    organization_id uuid primary key,
    organization_code text not null unique
);

create table if not exists ref.organization_role (
    role_code text primary key
);
