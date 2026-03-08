CREATE SCHEMA IF NOT EXISTS ${flyway:defaultSchema};
CREATE SCHEMA IF NOT EXISTS raw_zone;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS data_quality;

COMMENT ON SCHEMA ${flyway:defaultSchema} IS 'Schéma technique administré par Flyway pour data-forge';
COMMENT ON SCHEMA raw_zone IS 'Zone brute alimentée par les pipelines d''ingestion';
COMMENT ON SCHEMA analytics IS 'Zone analytique et de transformation';
COMMENT ON SCHEMA data_quality IS 'Zone dédiée aux contrôles qualité de données';
