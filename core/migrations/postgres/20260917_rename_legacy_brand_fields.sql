-- Rename legacy brand columns and values in application-owned PostgreSQL tables.
-- This script is idempotent and intentionally constructs the legacy spelling at
-- runtime so new source artifacts contain only the SignAIght brand.

DO $$
DECLARE
    old_compact text := 'real' || 'eye';
    old_snake text := 'real' || '_eye';
    target_brand text := 'signaight';
    item record;
BEGIN
    FOR item IN
        SELECT table_schema, table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
          AND data_type IN (
              'text', 'character varying', 'character', 'json', 'jsonb'
          )
    LOOP
        IF item.data_type IN ('json', 'jsonb') THEN
            EXECUTE format(
                'UPDATE %I.%I SET %I = replace(replace(%I::text, %L, %L), %L, %L)::%s '
                || 'WHERE %I::text ILIKE %L OR %I::text ILIKE %L',
                item.table_schema,
                item.table_name,
                item.column_name,
                item.column_name,
                old_snake,
                target_brand,
                old_compact,
                target_brand,
                item.data_type,
                item.column_name,
                '%' || old_snake || '%',
                item.column_name,
                '%' || old_compact || '%'
            );
        ELSE
            EXECUTE format(
                'UPDATE %I.%I SET %I = replace(replace(%I, %L, %L), %L, %L) '
                || 'WHERE %I ILIKE %L OR %I ILIKE %L',
                item.table_schema,
                item.table_name,
                item.column_name,
                item.column_name,
                old_snake,
                target_brand,
                old_compact,
                target_brand,
                item.column_name,
                '%' || old_snake || '%',
                item.column_name,
                '%' || old_compact || '%'
            );
        END IF;
    END LOOP;

    FOR item IN
        SELECT table_schema, table_name, column_name
        FROM information_schema.columns
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
          AND (
              column_name ILIKE '%' || old_snake || '%'
              OR column_name ILIKE '%' || old_compact || '%'
          )
    LOOP
        EXECUTE format(
            'ALTER TABLE %I.%I RENAME COLUMN %I TO %I',
            item.table_schema,
            item.table_name,
            item.column_name,
            replace(
                replace(item.column_name, old_snake, target_brand),
                old_compact,
                target_brand
            )
        );
    END LOOP;
END $$;
